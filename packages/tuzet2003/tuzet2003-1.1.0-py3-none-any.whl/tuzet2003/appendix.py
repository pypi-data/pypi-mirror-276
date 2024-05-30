"""
Equation from all Appendix
"""
import math

from scipy.integrate import quad

from .external import (air_density, atm_pressure, black_body, celsius, cp_air, gas_constant, kelvin, vap_sat,
                       water_air_diffusivity, water_latent_heat_vaporization, water_liquid_density, water_molar_mass)
from .raw import eq5_hi


def eq_a1_a(ts_s, ta_v, r_s, rh):
    """Sensible heat flux from soil surface.

    Args:
        ts_s (float): [K] soil surface temperature
        ta_v (float): [K] temperature of the air surrounding leaves
        r_s (float): [s.m-1] turbulent transport resistance from the ground to h_s
        rh (float): [-] relative humidity

    Returns:
        hs (float): [W.m-2]
    """
    cp = cp_air * 1e3  # [J.g-1.K-1] to [J.kg-1.K-1]
    return air_density(celsius(ta_v), rh, atm_pressure) * cp * (ts_s - ta_v) / r_s


def eq_a1_b(ts_v, ta_v, rb_v, rh):
    """Sensible heat flux from foliage layer.

    Args:
        ts_v (float): [K] foliage temperature
        ta_v (float): [K] temperature of the air surrounding leaves
        rb_v (float): [s.m-1] bulk boundary layer resistance
        rh (float): [-] relative humidity

    Returns:
        hv (float): [W.m-2]
    """
    cp = cp_air * 1e3  # [J.g-1.K-1] to [J.kg-1.K-1]
    return air_density(celsius(ta_v), rh, atm_pressure) * cp * (ts_v - ta_v) / rb_v


def eq_a1_c(ta_v, ta, rv, ra, rh):
    """Total sensible heat flux from canopy plus soil.

    Args:
        ta_v (float): [K] temperature of the air surrounding leaves
        ta (float): [K] temperature of the air at the ref level
        rv (float): [s.m-1] turbulent transport resistance from hs to the top of canopy
        ra (float): [s.m-1] aerodynamic resistance for heat and mass above the canopy
        rh (float): [-] relative humidity

    Returns:
        h (float): [W.m-2]
    """
    cp = cp_air * 1e3  # [J.g-1.K-1] to [J.kg-1.K-1]
    return air_density(celsius(ta), rh, atm_pressure) * cp * (ta_v - ta) / (rv + ra)


def damping_depth(lambda_w, c_soil):
    """Damping depth.

    Args:
        lambda_w (float): [W.m-1.K-1] thermal conductivity of the wet layer
        c_soil (float): [J.m-3.K-1] soil volumetric heat capacity

    Returns:
        dd (float): [m]
    """
    omega = 2 * math.pi / 86400  # frequency of temperature variation (diurnal)
    return math.sqrt(2 * lambda_w / c_soil / omega)


def eq_a2(dm, tortuosity, porosity):
    """resistance to water vapour transfer through the dry soil layer.

    Args:
        dm (float): [m] top of wet layer
        tortuosity (float): [-] dry layer tortuosity factor
        porosity (float): [-] dry layer porosity

    Returns:
        rm (float): [s.m-1]
    """
    dv = water_air_diffusivity * 1e-4  # [cm2.s-1] to [m2.s-1]
    return tortuosity * dm / dv / porosity


def dm_var(evap, theta_s):
    """Speed of variation of dm.

    Args:
        evap (float): [kg.m-2.s-1] total evaporation flux density
        theta_s (float): [m3.m-3] soil water content

    Returns:
        (float): [m.s-1]
    """
    rho_v = water_liquid_density * 1e3  # [kg.l-1] to [kg.m-3]
    return evap / (rho_v * theta_s)


def eq_a3_a(tm, tr_v, ta_v, rs, rm):
    """Latent heat fluxes from the soil surface.

    Args:
        tm (float): [K] soil temperature at the dry–wet layer interface
        tr_v (float): [K] dew point temperature of the air surrounding leaves
        ta_v (float): [K] temperature of the air surrounding leaves
        rs (float): [s.m-1] turbulent transport resistance from the ground to hs
        rm (float): [s.m-1] resistance to water vapour transfer through the dry soil layer

    Returns:
        le_s (float): [W.m-2]
    """
    lambda_v = water_latent_heat_vaporization * 1e3  # [kJ.kg-1] to [J.kg-1]
    mv = water_molar_mass * 1e-3  # [g.mol-1] to [kg.mol-1]
    cond = lambda_v * mv / gas_constant / (rs + rm)
    return cond * (vap_sat(celsius(tm)) / tm - vap_sat(celsius(tr_v)) / ta_v)


def eq_a3_b(psi_v, ts_v, tr_v, ta_v, rs_h2o, rb_v):
    """Latent heat fluxes from foliage layer.

    Args:
        psi_v (float): [MPa] leaf water potential
        ts_v (float): [K] foliage temperature
        tr_v (float): [K] dew point temperature of the air surrounding leaves
        ta_v (float): [K] temperature of the air surrounding leaves
        rs_h2o (float): [s.m-1] bulk stomatal resistance for H2O
        rb_v (float): [s.m-1] bulk boundary layer resistance

    Returns:
        le_v (float): [W.m-2]
    """
    lambda_v = water_latent_heat_vaporization * 1e3  # [kJ.kg-1] to [J.kg-1]
    mv = water_molar_mass * 1e-3  # [g.mol-1] to [kg.mol-1]
    cond = lambda_v * mv / gas_constant / (rs_h2o + rb_v)
    return cond * (eq5_hi(psi_v, ts_v) * vap_sat(celsius(ts_v)) / ts_v - vap_sat(celsius(tr_v)) / ta_v)


def eq_a3_c(tr_v, ta_v, tr, ta, rv, ra):
    """Total latent heat flux.

    Args:
        tr_v (float): [K] dew point temperature of the air surrounding leaves
        ta_v (float): [K] temperature of the air surrounding leaves
        tr (float): [K] dew point temperature at the reference level
        ta (float): [K] air temperature at the reference level
        rv (float): [s.m-1] turbulent transport resistance from hs to the top of canopy
        ra (float): [s.m-1] aerodynamic resistance for heat and mass above the canopy

    Returns:
        le (float): [W.m-2]
    """
    lambda_v = water_latent_heat_vaporization * 1e3  # [kJ.kg-1] to [J.kg-1]
    mv = water_molar_mass * 1e-3  # [g.mol-1] to [kg.mol-1]
    cond = lambda_v * mv / gas_constant / (rv + ra)
    return cond * (vap_sat(celsius(tr_v)) / ta_v - vap_sat(celsius(tr)) / ta)


def eq_a5_a(rg, ra, ts_v, ts_s, av, k, lai):
    """Net absorption of radiation in the foliage layer.

    Args:
        rg (float): [W.m-2] global solar radiation above the canopy
        ra (float): [W.m-2] long-wave radiation of the atmosphere
        ts_v (float): [K] foliage temperature
        ts_s (float): [K] soil surface temperature
        av (float): [-] average canopy albedo
        k (float): [-] extinction coefficient of radiation
        lai (float): [-] leaf area index of foliage

    Returns:
        Rn_v (float): [W.m-2]
    """
    epsilon = 0.95  # [-] reflectivity of soil (see https://sun-r.gitlab.io/paper/energy_balance/radiative.html#ground)

    vis = (1 - av) * rg * (1 - math.exp(-k * lai))
    therm = (ra - 2 * black_body(ts_v) + epsilon * black_body(ts_s)) * (1 - math.exp(-k * lai))
    return vis + therm


def eq_a5_b(rg, ra, ts_v, ts_s, av, k, lai):
    """Net absorption of radiation the soil surface.

    Args:
        rg (float): [W.m-2] global solar radiation above the canopy
        ra (float): [W.m-2] long-wave radiation of the atmosphere
        ts_v (float): [K] foliage temperature
        ts_s (float): [K] soil surface temperature
        av (float): [-] average canopy albedo
        k (float): [-] extinction coefficient of radiation
        lai (float): [-] leaf area index of foliage

    Returns:
        Rn_s (float): [W.m-2]
    """
    epsilon = 0.95  # [-] reflectivity of soil (see https://sun-r.gitlab.io/paper/energy_balance/radiative.html#ground)

    vis = (1 - av) * rg * math.exp(-k * lai)
    therm = ra * math.exp(-k * lai) + black_body(ts_v) * (1 - math.exp(-k * lai)) - epsilon * black_body(ts_s)
    return vis + therm


def eq_a6_a(ts_s, tm, dm, lambda_d):
    """Surface Soil heat flux

    Args:
        ts_s (float): [K] soil surface temperature
        tm (float): [K] soil temperature at the dry–wet layer interface
        dm (float): [m] depth of dry-wet interface
        lambda_d (float): [W.m-1.K-1] thermal conductivity of the dry layer

    Returns:
        g0 (float): [W.m-2]
    """
    return lambda_d * (ts_s - tm) / dm


def eq_a6_b(tm, td, dm, dd, lambda_w):
    """Soil heat flux in wet horizon.

    Args:
        tm (float): [K] soil temperature at the dry–wet layer interface
        td (float): [K] temperature of deep soil
        dm (float): [m] depth of dry-wet interface
        dd (float): [m] damping depth
        lambda_w (float): [W.m-1.K-1] thermal conductivity of the wet layer

    Returns:
        gs (float): [W.m-2]
    """
    return lambda_w * (tm - td) / (dd - dm)


def eq_a7(an, f_soil):
    """CO2 flux between the reference height and the canopy airspace.

    Args:
        an (float): [mol CO2.m-2.s-1] Net canopy photosynthesis (positive toward
                    the canopy)
        f_soil (float): [mol CO2.m-2.s-1] soil respiration (positive upward)

    Returns:
         f_co2 (float): [mol CO2.m-2.s-1]
    """
    return an - f_soil


def eq_a8(vc, vj, rd):
    """Net photosynthesis.

    Args:
        vc (float): [mol CO2.m-2.s-1] Rubisco activity at the sites of carboxylation
        vj (float): [mol CO2.m-2.s-1] electron transport
        rd (float): [mol CO2.m-2.s-1] rate of CO2 evolution from processes other
                    than photorespiration

    Returns:
        an (float): [mol CO2.m-2.s-1]
    """
    return min(vc, vj) - rd


def eq_a9(ci, gamma_star, kc, ko, vl_max, oi):
    """Rubisco activity at the sites of carboxylation.

    Args:
        ci (float): [mol.mol-1] CO2 concentration in the intercellular spaces
        gamma_star (float): [mol.mol-1] CO2 compensation point in the absence of
                            day respiration
        kc (float): [mol.mol-1] Michaelis coefficient for CO2
        ko (float): [mol.mol-1] Michaelis coefficient for O2
        vl_max (float): [mol CO2.m-2.s-1] maximum carboxylation rate per unit leaf area
        oi (float): [mol.mol-1] intercellular oxygen concentration

    Returns:
        vc (float): [mol CO2.m-2.s-1]
    """
    return vl_max * (ci - gamma_star) / (ci + kc * (1 + oi / ko))


def eq_a10(j, ci, gamma_star):
    """Maximum carboxylation rate per unit leaf area when RuBP is saturated

    Args:
        j (float): [mol CO2.m-2.s-1] electron transport rate for a given absorbed
                   photon irradiance
        ci (float): [mol.mol-1] CO2 concentration in the intercellular spaces
        gamma_star (float): [mol.mol-1] CO2 compensation point in the absence of
                            day respiration

    Returns:
        vc (float): [mol CO2.m-2.s-1]
    """
    return j / 4 * (ci - gamma_star) / (ci + 2 * gamma_star)


def eq_a11(lai, vl_max, kn):
    """Maximum canopy photosynthetic capacity.

    Args:
        lai (float): [-] Leaf area index
        vl_max (float): [mol CO2.m-2.s-1] maximum photosynthetic capacity per
                        unit leaf area
        kn (float): [-] coefficient of leaf nitrogen allocation

    Returns:
        vc_max (float): [mol CO2.m-2.s-1]
    """
    return lai * vl_max * (1 - math.exp(-kn)) / kn


def eq_a12(ts_10, f0_soil, ea_soil):
    """CO2 flux from the soil surface.

    Args:
        ts_10 (float): [K] soil temperature at 10cm
        f0_soil (float): [mol CO2.m-2.s-1] CO2 flux from the soil at T0 = 298 K
        ea_soil (float): [J.mol-1] activation energy

    Returns:
        f_soil (float): [mol CO2.m-2.s-1]
    """
    t0 = kelvin(25)
    return f0_soil * math.exp(ea_soil * (ts_10 - t0) / (gas_constant * ts_10 * t0))


def eq_a13_a(tv, cv, ci, mu, rbv, g_co2):
    """Canopy photosynthesis.

    Args:
        tv (float) [K] leaf temperature
        cv (float): [mol.mol-1] CO2 concentration at the surface of leaves
        ci (float): [mol.mol-1] CO2 concentration in the intercellular space
        mu (float): [-] ratio of diffusivity of CO2 and H2O
        rbv (float): [s.m-1] bulk boundary layer resistance
        g_co2 (float): [mol CO2.m-2.s-1] stomatal conductance for CO2

    Returns:
        an (float): [mol CO2.m-2.s-1]
    """
    beta = atm_pressure / gas_constant / tv
    return (cv - ci) / (mu * rbv / beta + 1 / g_co2)


def eq_a13_b(ta, ca, cv, rv, ra):
    """Net CO2 flux from the canopy plus soil.

    Args:
        ta (float) [K] air temperature
        ca (float): [mol.mol-1] CO2 concentration in the atmosphere
        cv (float): [mol.mol-1] CO2 concentration at the surface of leaves
        rv (float): [s.m-1] turbulent transport resistance from hs to the top of canopy
        ra (float): [s.m-1] aerodynamic resistance for heat and mass above the canopy

    Returns:
        f_co2 (float): [mol CO2.m-2.s-1]
    """
    beta = atm_pressure / gas_constant / ta
    return (ca - cv) / (rv + ra) * beta


def eq_b1(ppfd, jl_max, alpha, theta):
    """Electron transport rate

    Args:
        ppfd (float): [mol photon.m-2.s-1] absorbed photon irradiance
        jl_max (float): [mol CO2.m-2.s-1]  potential rate of whole-chain electron
                        transport per unit leaf area
        alpha (float): [mol CO2.mol photon-1] quantum yield
        theta (float): [-] parameter of the hyperbola

    Returns:
        j (float): [mol CO2.m-2.s-1]
    """
    alpha_q = alpha * ppfd
    discrim = (alpha_q + jl_max) ** 2 - 4 * alpha_q * jl_max * theta

    return (alpha_q + jl_max - math.sqrt(discrim)) / (2 * theta)


def eq_b2(tv, v_ref, ea, t_ref):
    """Kc, Ko dependency on temperature

    Args:
        tv (float): [K] leaf temperature
        v_ref (float): [mol.mol-1] value of Kc or Ko at t_ref (25°C)
        ea (float): [J.mol-1] activation energy
        t_ref (float): [K] reference temperature for v_ref

    Returns:
        kc or ko (float): [mol.mol-1]
    """
    return v_ref * math.exp(ea / (gas_constant * t_ref) * (1 - t_ref / tv))


def eq_b3(tv, v_ref, ea, ed, s, t_ref):
    """Vlmax, Jmax dependency on temperature

    Args:
        tv (float): [K] leaf temperature
        v_ref (float): [mol.mol-1] value of Kc or Ko at t_ref (25°C)
        ea (float): [J.mol-1] activation energy
        ed (float): [J.mol-1] deactivation energy
        s (float): [J.mol-1.K-1] entropy term
        t_ref (float): [K] reference temperature for v_ref

    Returns:
        vl_max or j_max (float): [mol CO2.m-2.s-1]
    """
    num = math.exp(ea / (gas_constant * t_ref) * (1 - t_ref / tv))
    denom = 1 + math.exp((s * tv - ed) / (gas_constant * tv))
    return v_ref * num / denom


def eq_b4(tv, gamma_0, gamma_1, gamma_2, t_ref):
    """CO2 compensation point in the absence of day respiration.

    Args:
        tv (float): [K] leaf temperature
        gamma_0 (float): [mol.mol-1]
        gamma_1 (float): [K-1]
        gamma_2 (float): [K-2]
        t_ref (float): [K] reference temperature

    Returns:
        gamma_star (float): [mol.mol-1]
    """
    dt = tv - t_ref
    return gamma_0 * (1 + gamma_1 * dt + gamma_2 * dt ** 2)


def eq_c1_a(z, u_hc, hc, eta):
    """Wind speed at altitude z.

    Args:
        z (float): [m] altitude to compute
        u_hc (float): [m.s-1]  wind speed at canopy height
        hc (float): [m] height of canopy
        eta (float): [-] extinction factor

    Returns:
        u_z (float): [m.s-1]
    """
    return u_hc * math.exp(eta * (z / hc - 1))


def eq_c1_b(z, k_hc, hc, eta):
    """Eddy diffusivity at altitude z.

    Args:
        z (float): [m] altitude to compute
        k_hc (float): [m2.s-1]  Eddy diffusivity at canopy height
        hc (float): [m] height of canopy
        eta (float): [-] extinction factor

    Returns:
        k_z (float): [m2.s-1]
    """
    return k_hc * math.exp(eta * (z / hc - 1))


def eq_c2(lai, hc, lc, cd):
    """Extinction factor.

    Args:
        lai (float): [-] leaf area index
        hc (float): [m] height of canopy
        lc (float): [m] canopy mixing length
        cd (float): [-] leaf drag coefficient

    Returns:
        eta (float): [-]
    """
    return hc * (cd * lai / hc / 2 / lc ** 2) ** (1 / 3)


def eq_c3_a(z0g, hs, k_hc, hc, eta):
    """Turbulent transport resistance from the ground to hs

    Args:
        z0g (float): [m] roughness length of soil surface
        hs (float): [m] canopy source-sink height
        k_hc (float): [m2.s-1]  Eddy diffusivity at canopy height
        hc (float): [m] height of canopy
        eta (float): [-] extinction factor

    Returns:
        rs (float): [s.m-1]
    """
    val, abserr = quad(lambda z: 1 / eq_c1_b(z, k_hc, hc, eta), z0g, hs)
    return val


def eq_c3_b(hs, k_hc, hc, eta):
    """Turbulent transport resistance from hs to canopy

    Args:
        hs (float): [m] canopy source-sink height
        k_hc (float): [m2.s-1]  Eddy diffusivity at canopy height
        hc (float): [m] height of canopy
        eta (float): [-] extinction factor

    Returns:
        rv (float): [s.m-1]
    """
    val, abserr = quad(lambda z: 1 / eq_c1_b(z, k_hc, hc, eta), hs, hc)
    return val


def eq_c3_c(zr, k_hc, hc, eta):
    """Turbulent transport resistance from canopy to zref

    Args:
        zr (float): [m] reference level above canopy
        k_hc (float): [m2.s-1]  Eddy diffusivity at canopy height
        hc (float): [m] height of canopy
        eta (float): [-] extinction factor

    Returns:
        ra (float): [s.m-1]
    """
    val, abserr = quad(lambda z: 1 / eq_c1_b(z, k_hc, hc, eta), hc, zr)
    return val


def eq_c4(z0g, dl, u_hc, hc, eta):
    """Bulk boundary layer resistance.

    Args:
        z0g (float): [m] roughness length of soil surface
        dl (float): [m] average leaf width
        u_hc (float): [m.s-1]  wind speed at canopy height
        hc (float): [m] height of canopy
        eta (float): [-] extinction factor

    Returns:
        rb_v (float): [s.m-1]
    """
    ct = 156.2  # transfer coefficient, from text
    val, abserr = quad(lambda z: math.sqrt(eq_c1_a(z, u_hc, hc, eta)) / dl, z0g, hc)
    return ct * (hc - z0g) / val
