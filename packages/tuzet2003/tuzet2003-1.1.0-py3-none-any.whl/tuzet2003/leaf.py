"""
Formalisms from paper at leaf scale
"""
from dataclasses import dataclass
from typing import List

from . import appendix, external, raw
from .external import black_body


@dataclass
class Params:
    ca: float = 37 / external.atm_pressure
    """[mol.mol-1]
    
    References: value around year 2000
    """

    oxygen: float = 210e-3
    """[mol.mol-1]
    
    References: table3
    """

    t_ref: float = external.kelvin(20)
    """[K] reference temperature for temp formalisms
    """

    kc_ref: float = 3.02e-4
    """[mol.mol-1]
    """

    kc_ea: float = 5.943e4
    """[J.mol-1]
    """

    ko_ref: float = 2.56e-1
    """[mol.mol-1]
    """

    ko_ea: float = 3.6e4
    """[J.mol-1]
    """

    vl_max_ref: float = 1e-4
    """[mol CO2.m-2.s-1]
    """

    vl_ea: float = 5.852e4
    """[J.mol-1]
    """

    vl_ed: float = 2.2e5
    """[J.mol-1]
    """

    jl_max_ref: float = 1e-4 * 2  # vl_max_ref * 2 from text p1114 (Leuning 1997)
    """[mol CO2.m-2.s-1]
    """

    jl_ea: float = 3.7e4
    """[J.mol-1]
    """

    jl_ed: float = 2.2e5
    """[J.mol-1]
    """

    s: float = 7e2
    """[J.mol-1.K-1]
    """

    gamma: List[float] = (2.8e-5, 5.09e-2, 1e-3)
    """[mol.mol-1][-][-]
    """

    alpha: float = 0.2
    """[-]
    """

    theta: float = 0.9
    """[-]
    """

    g0: float = 3e-4
    """[mol CO2.m-2.s-1]
    """

    g_sca: float = 2
    """[-]
    """

    k_plant: float = 1e-7
    """[m.s-1.MPa-1]
    """

    psi_ref: float = -1.9
    """[MPa] from fig6
    """

    sf: float = 3.2
    """[MPa] from fig6
    """

    z0g: float = 0.
    """[m] no reason for this value
    """

    lai: float = 3
    """[m.m-1] leaf area index
    """

    canopy_height: float = 0.8
    """[m]
    """

    dl: float = 1e-1
    """[m]
    """

    l_c: float = 0.2
    """[m]
    """

    drag: float = 0.01
    """[-] leaf drag coefficient
    
    References: Albayraketal 2014
    """

    albedo: float = 0.23
    """[-]
    """


def bulk_resistance(ws, params):
    """Bulk resistance of canopy.

    Args:
        ws (float): [m.s-1] wind speed
        params (Params): set of parameters for model

    Returns:
        rbv (float): [s.m-1]
    """
    eta = appendix.eq_c2(params.lai, params.canopy_height, params.l_c, params.drag)
    rbv = appendix.eq_c4(params.z0g, params.dl, ws, params.canopy_height, eta)

    return rbv


def photo_net(ppfd, t_leaf, gs_water_stress, rd, ci_ini, params):
    """Net photosynthesis

    Args:
        ppfd (float): [µmol photon.m-2.s-1]
        t_leaf (float): [K] leaf temperature
        gs_water_stress (float): [-] dependency of gs on water stress
        rd (float): [mol CO2.m-2.s-1] respiration
        ci_ini (float): [mol.mol-1] initial guess for ci
        params (Params): set of parameters for model

    Returns:
        (float, float, float): [mol CO2.m-2.s-1]
    """
    if ppfd < 40:  # night time
        return -rd, params.ca * 0.75, params.g0

    kc = appendix.eq_b2(t_leaf, params.kc_ref, params.kc_ea, params.t_ref)
    ko = appendix.eq_b2(t_leaf, params.ko_ref, params.ko_ea, params.t_ref)
    gamma_star = appendix.eq_b4(t_leaf, params.gamma[0], params.gamma[1], params.gamma[2], params.t_ref)
    vl_max = appendix.eq_b3(t_leaf, params.vl_max_ref, params.vl_ea, params.vl_ed, params.s, params.t_ref)
    jl_max = appendix.eq_b3(t_leaf, params.jl_max_ref, params.jl_ea, params.vl_ed, params.s, params.t_ref)
    j = appendix.eq_b1(ppfd * 1e-6, jl_max, params.alpha, params.theta)

    ci = ci_ini
    for i in range(1000):
        vc = appendix.eq_a9(ci, gamma_star, kc, ko, vl_max, params.oxygen)
        vj = appendix.eq_a10(j, ci, gamma_star)

        an = appendix.eq_a8(vc, vj, rd)

        g_co2 = raw.eq1(an, ci, gs_water_stress, gamma_star, params.g0, params.g_sca)
        g_co2 = max(g_co2, params.g0)

        ci_new = params.ca - an / g_co2
        if abs(ci - ci_new) < 1e-8:
            return an, ci, g_co2
        else:
            ci = ci_new

    raise UserWarning("Termination error An")


def gas_exchange(ppfd, t_atm, rh, ws, t_leaf, psi_soil, rd, ci_ini, params):
    """Gas exchange between leaf and atmosphere.

    Args:
        ppfd (float): [µmol photon.m-2.s-1]
        t_atm (float): [K] temperature of atmosphere
        rh (float): [-] relative humidity between 0 and 1
        ws (float): [m.s-1] wind speed
        t_leaf (float): [K] leaf temperature
        psi_soil (float): [MPa] water potential in soil
        rd (float): [mol CO2.m-2.s-1] respiration
        ci_ini (float): [mol.mol-1] initial guess for ci
        params (Params): set of parameters for model

    Returns:
        (float, float, float, float, float): [mol CO2.m-2.s-1], [MPa], [kg.m-2.s-1]
    """
    eta = appendix.eq_c2(params.lai, params.canopy_height, params.l_c, params.drag)

    ci = ci_ini
    psi_leaf_new = psi_soil
    for i in range(1000):
        psi_leaf = psi_leaf_new
        psi_fac = raw.eq2(psi_leaf, params.psi_ref, params.sf)

        # compute photosynthesis
        an, ci, g_co2 = photo_net(ppfd, t_leaf, psi_fac, rd, ci, params)

        # water fluxes
        rbv = appendix.eq_c4(params.z0g, params.dl, ws, params.canopy_height, eta)
        rsh2o = raw.eq5_rsh2o(g_co2, t_leaf)
        hi = raw.eq5_hi(psi_leaf, t_leaf)
        transpi = raw.eq5b_alt(rsh2o, rbv, hi, t_leaf, t_atm, rh)

        psi_leaf_new = psi_soil - transpi / params.k_plant
        if abs(psi_leaf - psi_leaf_new) < 1e-2:
            return an, ci, g_co2, psi_leaf, transpi

    raise UserWarning("Termination error An,transpi")


def gas_exchange_alt(ppfd, t_atm, rh, t_leaf, psi_soil, rbv, rd, ci_ini, params):
    """Gas exchange between leaf and atmosphere.

    Args:
        ppfd (float): [µmol photon.m-2.s-1]
        t_atm (float): [K] temperature of atmosphere
        rh (float): [-] relative humidity between 0 and 1
        t_leaf (float): [K] leaf temperature
        psi_soil (float): [MPa] water potential in soil
        rbv (float): [s.m-1] bulk boundary resistance
        rd (float): [mol CO2.m-2.s-1] respiration
        ci_ini (float): [mol.mol-1] initial guess for ci
        params (Params): set of parameters for model

    Returns:
        (float, float, float, float, float): [mol CO2.m-2.s-1], [MPa], [kg.m-2.s-1]
    """
    ci = ci_ini
    psi_leaf_new = psi_soil
    for i in range(1000):
        psi_leaf = psi_leaf_new
        psi_fac = raw.eq2(psi_leaf, params.psi_ref, params.sf)

        # compute photosynthesis
        an, ci, g_co2 = photo_net(ppfd, t_leaf, psi_fac, rd, ci, params)

        # water fluxes
        rsh2o = raw.eq5_rsh2o(g_co2, t_leaf)
        hi = raw.eq5_hi(psi_leaf, t_leaf)
        transpi = raw.eq5b_alt(rsh2o, rbv, hi, t_leaf, t_atm, rh)

        psi_leaf_new = psi_soil - transpi / params.k_plant
        if abs(psi_leaf - psi_leaf_new) < 1e-2:
            return an, ci, g_co2, psi_leaf, transpi

    raise UserWarning("Termination error An,transpi")


def leaf_temp(rg, transpi, t_atm, t_soil, rbv, alpha_soil, params):
    """Energy balance around leaf.

    Args:
        rg (float): [W.m-2] global radiation in visible
        transpi (float): [m3.m-2.s-1] rate of transpiration
        t_atm (float): [K] air temperature
        t_soil (float): [K] soil temperature
        rbv (float): [s.m-1] bulk boundary resistance
        alpha_soil (float): [-] fraction of leaf that actually see the soil between 0 and 1
        params (Params): set of parameters for model

    Returns:
        (float): [K]
    """
    lambda_v = external.water_latent_heat_vaporization * 1e3  # [kJ.kg-1] to [J.kg-1]
    rho_v = external.water_liquid_density * 1e3  # [kg.l-1] to [kg.m-3]

    vis = (1 - params.albedo) * rg  # [W.m-2] contribution from visible radiations
    therm = alpha_soil * black_body(t_soil) - alpha_soil * black_body(t_atm)  # [W.m-2] known thermal radiation
    le = transpi * rho_v * lambda_v  # [W.m-2] latent heat

    cond_forced = rho_v * external.cp_air / rbv

    delta_t = (vis + therm - le) / (cond_forced + 8 * external.stephan_boltzmann * t_atm ** 3)

    return t_atm + delta_t


def energy_balance(ppfd, t_atm, rh, t_soil, psi_soil, rbv, rd, t_leaf_ini, ci_ini, alpha_soil, params):
    """Full gas exchange with energy balance.

    Args:
        ppfd (float): [µmol photon.m-2.s-1]
        t_atm (float): [K] temperature of atmosphere
        rh (float): [-] relative humidity between 0 and 1
        t_soil (float): [K] soil temperature
        psi_soil (float): [MPa] water potential in soil
        rbv (float): [s.m-1] bulk boundary resistance
        rd (float): [mol CO2.m-2.s-1] respiration
        t_leaf_ini (float): [K] initial guess for t_leaf
        ci_ini (float): [mol.mol-1] initial guess for ci
        alpha_soil (float): [-] fraction of leaf that actually see the soil between 0 and 1
        params (Params): set of parameters for model

    Returns:
        (float, float, float, float, float, float): [mol CO2.m-2.s-1], [MPa], [kg.m-2.s-1], [K]
    """
    r_vis = external.ppfd_to_rg(ppfd) / 2.  # [W.m-2]

    ci = ci_ini
    t_leaf = t_leaf_ini

    for i in range(1000):
        an, ci, g_co2, psi_leaf, transpi = gas_exchange_alt(ppfd,
                                                            t_atm,
                                                            rh,
                                                            t_leaf,
                                                            psi_soil,
                                                            rbv,
                                                            rd,
                                                            ci,
                                                            params)

        t_leaf_new = leaf_temp(r_vis, transpi, t_atm, t_soil, rbv, alpha_soil, params)
        if abs(t_leaf - t_leaf_new) < 1e-2:
            return an, ci, g_co2, psi_leaf, transpi, t_leaf
        else:
            t_leaf = t_leaf_new

    raise UserWarning("Termination error energy balance")
