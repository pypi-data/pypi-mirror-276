"""
Raw formalisms directly extracted from the article
"""
import math

from .external import atm_pressure, celsius, gas_constant, vap_sat, water_liquid_density, water_molar_mass


def eq1(a, ci, psi_fac, gamma, g0, alpha):
    """Stomatal response.

    Args:
        a (float): [mol CO2.m-2.s-1] assimilation rate
        ci (float): [mol.mol-1] CO2 concentration in intercellular space
        psi_fac (float): [-] sensitivity of stomata to leaf water potential)
        gamma (float): [mol.mol-1] CO2 compensation point
        g0 (float): [mol CO2.m-2.s-1] residual conductance
        alpha (float): [-] shape factor

    Returns:
        g_co2 (float): [mol CO2.m-2.s-1] stomatal conductance for CO2
    """
    return g0 + alpha * a / (ci - gamma) * psi_fac


def eq2(psi_v, psi_f, s_f):
    """Sensitivity of stomata to leaf water potential.

    Args:
        psi_v (float): [MPa] leaf water potential
        psi_f (float): [MPa] reference potential
        s_f (float): [MPa-1] sensitivity parameter

    Returns:
        f_psi_v (float): [-]
    """
    return (1 + math.exp(s_f * psi_f)) / (1 + math.exp(s_f * (psi_f - psi_v)))


def eq4a(theta_s, theta_sat, psi_e, b):
    """Soil water potential.

    References: Campbell 1985

    Args:
        theta_s (float): [m3.m-3] soil water content
        theta_sat (float): [m3.m-3] saturation water content of the soil
        psi_e (float): [MPa] air entry water potential of the soil
        b (float): [-] empirical shape parameter

    Returns:
        psi_s (float): [MPa] soil water potential
    """
    return psi_e * (theta_sat / theta_s) ** b


def eq4b(theta_s, theta_sat, k_sat, b):
    """Soil hydraulic conductivity.

    References: Campbell 1985

    Args:
        theta_s (float): [m3.m-3] soil water content
        theta_sat (float): [m3.m-3] saturation water content of the soil
        k_sat (float): [s-1.MPa-1.m2] matric flux potential
        b (float): [-] empirical shape parameter

    Returns:
        k_s (float): [s-1.MPa-1.m2]
    """
    return k_sat * (theta_s / theta_sat) ** (2 * b + 3)


def eq5a(psi_r, psi_v, chi_v):
    """Water flow through plant canopy.

    Args:
        psi_r (float): [MPa] water potential at the boundary between the plant
                             roots and the soil
        psi_v (float): [MPa] leaf water potential
        chi_v (float): [MPa.s.m-1] leaf-specific resistance to water flow through
                                   plant from the roots to the stomata

    Returns:
        f (float): [m.s-1]
    """
    return (psi_r - psi_v) / chi_v


def eq5b(rs_h2o, rb_v, hi, ts_v, tr_v, ta_v):
    """Transpiration.

    Args:
        rs_h2o (float): [s.m-1] bulk stomatal resistance for H2O
        rb_v (float): [s.m-1] bulk boundary layer resistance
        hi (float): [-]  fractional relative humidity in the intercellular spaces
        ts_v (float): [K] foliage temperature
        tr_v (float): [K] dew point temperature of the air surrounding leaves
        ta_v (float): [K] temperature of the air surrounding leaves

    Returns:
        f (float): [m.s-1]
    """
    rho_v = water_liquid_density * 1e3  # [kg.l-1] to [kg.m-3]
    mv = water_molar_mass * 1e-3  # [g.mol-1] to [kg.mol-1]
    cond = mv / gas_constant / rho_v / (rs_h2o + rb_v)
    return cond * (hi * vap_sat(celsius(ts_v)) / ts_v - vap_sat(celsius(tr_v)) / ta_v)


def eq5b_alt(rs_h2o, rb_v, hi, ts_v, ta_v, rh):
    """Transpiration.

    Args:
        rs_h2o (float): [s.m-1] bulk stomatal resistance for H2O
        rb_v (float): [s.m-1] bulk boundary layer resistance
        hi (float): [-]  fractional relative humidity in the intercellular spaces
        ts_v (float): [K] foliage temperature
        ta_v (float): [K] temperature of the air surrounding leaves
        rh (float): [-] relative humidity in atmosphere between 0 and 1

    Returns:
        f (float): [m.s-1]
    """
    rho_v = water_liquid_density * 1e3  # [kg.l-1] to [kg.m-3]
    mv = water_molar_mass * 1e-3  # [g.mol-1] to [kg.mol-1]
    cond = mv / gas_constant / rho_v / (rs_h2o + rb_v)
    return cond * (hi * vap_sat(celsius(ts_v)) / ts_v - rh * vap_sat(celsius(ta_v)) / ta_v)


def eq5_rsh2o(g_co2, ts_v):
    """bulk stomatal resistance for H2O.

    Args:
        g_co2 (float): [mol CO2.m-2.s-1] stomatal conductance for CO2
        ts_v (float): [K] leaf temperature

    Returns:
        rs_h2o (float): [s.m-1]
    """
    beta = atm_pressure / (gas_constant * ts_v)
    return beta / (1.6 * g_co2)


def eq5_hi(psi_v, ts_v):
    """Fractional relative humidity in the intercellular spaces.

    Args:
        psi_v (float): [MPa] leaf water potential
        ts_v (float): [K] leaf temperature

    Returns:
        hi (float): [-]
    """
    rho_v = water_liquid_density * 1e3  # [kg.l-1] to [kg.m-3]
    mv = water_molar_mass * 1e-3  # [g.mol-1] to [kg.mol-1]
    psi_leaf = psi_v * 1e6  # [MPa] to [Pa]
    return math.exp(mv * psi_leaf / rho_v / gas_constant / ts_v)
