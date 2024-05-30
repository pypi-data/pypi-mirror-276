"""
External formalisms used in the article without explicit formulation
"""
import math

atm_pressure = 101325
"""[Pa] Atmospheric pressure

References: https://en.wikipedia.org/wiki/Atmospheric_pressure
"""

cp_air = 1.012
"""[J.g-1.K-1] Isobaric mass heat capacity of air (Cp)

References: https://en.wikipedia.org/wiki/Table_of_specific_heat_capacities (room conditions)
"""

gas_constant = 8.31446
"""[J.K-1.mol-1] Ideal gas constant

References: https://en.wikipedia.org/wiki/Gas_constant
"""

water_latent_heat_vaporization = 2264.705
"""[kJ.kg-1] Latent heat of vaporisation of water (λ)

References: https://en.wikipedia.org/wiki/Latent_heat#Specific_latent_heat
"""

air_molar_mass = 28.9652
"""[g.mol-1] Molar mass of dry air

References: https://en.wikipedia.org/wiki/Density_of_air
"""

water_molar_mass = 18.01528
"""[g.mol-1] Molecular mass of water

References: https://en.wikipedia.org/wiki/Properties_of_water
"""

water_liquid_density = 0.9970474
"""[kg.l-1] Liquid water density at 25°C

References: https://en.wikipedia.org/wiki/Properties_of_water
"""

stephan_boltzmann = 5.670367e-08
"""[W.m-2.K-4] Stefan-Boltzmann constant per surface area (σ).

References: scipy.constants.physical_constants['Stefan-Boltzmann constant']
"""

water_air_diffusivity = 0.26
"""[cm2.s-1] Water vapour diffusivity in air

References: https://en.wikipedia.org/wiki/Mass_diffusivity#Example_values
"""

_kelvin = 273.15
"""[°C] temperature of 0°C in K

References: https://en.wikipedia.org/wiki/Kelvin
"""


def kelvin(temp):
    """Conversion to Kelvin

    Args:
        temp (float): [°C]

    Returns:
        (float): [K]
    """
    return temp + _kelvin


def celsius(temp):
    """Conversion to Celsius

    Args:
        temp (float): [K]

    Returns:
        (float): [°C]
    """
    return temp - _kelvin


def vap_sat(temp):
    """Saturation water vapour pressure.

    References: https://en.wikipedia.org/wiki/Vapour_pressure_of_water

    Args:
        temp (float): [°C] air temperature

    Returns:
        (float): [Pa] Saturated vapor pressure
    """
    # Tetens equation
    vs = 0.61078 * math.exp(17.27 * temp / (temp + 237.3))

    return vs * 1e3  # [kPa] to [Pa]


def air_density(temp, rh, pressure):
    """Air density

    References: https://en.wikipedia.org/wiki/Density_of_air

    Args:
        temp (float): [°C] air temperature
        rh (float): [-] relative humidity
        pressure (float): [Pa] atmospheric pressure

    Returns:
        (float): [kg.m-3]
    """
    pv = rh * vap_sat(temp)
    pd = pressure - pv

    return (pd * air_molar_mass + pv * water_molar_mass) / (gas_constant * kelvin(temp)) * 1e-3  # [g.m-3] to [kg.m-3]


def black_body(temp):
    """Amount of energy radiated by black body

    Args:
        temp (float): [K] temperature of black body

    Returns:
        (float): [W.m-2]
    """
    return stephan_boltzmann * temp ** 4


_hnu_550 = 0.2175028466158127
"""[J.µmol photon-1] Energy in mol of photon @ 550 [nm]

References: https://sun-r.gitlab.io/paper/energy_balance/pyranometer.html#conversion-to-par
"""

_par_frac = 0.45
"""[-] Fraction of PAR in global solar radiation

Theoretical fraction considering PAR in [350:720] [nm]

References: https://sun-r.gitlab.io/paper/energy_balance/pyranometer.html#conversion-to-par
"""


def rg_to_ppfd(rg):
    """Convert solar global radiation to PAR

    References
        - `Reis et al. (2020)`_ (see formula 34)
        - corrected: https://sun-r.gitlab.io/paper/energy_balance/pyranometer.html#conversion-to-par

    Args:
        rg (float): [W.m-2] global radiation intensity

    Returns:
        (float): [µmol photon.m-2.s-1] PPFD
    """
    return rg * _par_frac / _hnu_550


def ppfd_to_rg(ppfd):
    """Convert PAR to solar global radiation

    References
        - `Reis et al. (2020)`_ (see formula 38)
        - corrected: https://sun-r.gitlab.io/paper/energy_balance/pyranometer.html#conversion-to-par

    Args:
        ppfd (float): [µmol photon.m-2.s-1] PPFD

    Returns:
        (float): [W.m-2] global radiation intensity
    """
    return ppfd * _hnu_550 / _par_frac
