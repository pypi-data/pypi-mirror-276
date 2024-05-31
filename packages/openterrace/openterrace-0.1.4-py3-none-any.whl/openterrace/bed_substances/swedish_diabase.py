"""
Data for Swedish Diabase.

cp = 1272 (specific heat capacity at constant pressure)
rho = 3007 (density)
k = 1.75 (thermal conductivity)
"""

def h(T:float) -> float:
    """Mass specific enthalpy as function of temperature at 1 atm (fit assumes constant cp).

    Args:
        T (float): Temperature in K

    Returns:
        Specific enthalpy in J/kg
    """
    return 1272*T

def T(h:float, p:float=None) -> float:
    """Temperature as function of mass specific enthalpy at 1 atm (fit assumes constant cp).

    Args:
        h (float): Specific enthalpy in J/kg
        p (float): Pressure in Pa

    Returns:
        Temperature in kelvin
    """
    return 1/1272*h

def rho(h:float, p:float=None) -> float:
    """Density as function of mass specific entahlpy at 1 atm (fit assumes constant density).

    Args:
        h (float): Specific enthalpy in J/kg
        p (float): Pressure in Pa

    Returns:
        Density in kg/m^3
    """
    return 3007*h**0

def k(h:float, p:float=None) -> float:
    """Thermal conductivity as function of mass specific enthalpy at 1 atm (fit assumes constant thermal conductivity).

    Args:
        h (float): Specific enthalpy in J/kg
        p (float): Pressure in Pa

    Returns:
        float: Thermal conductivity in W/(m K)
    """
    return 1.75*h**0

def cp(h:float, p:float=None) -> float:
    """Specific heat capacity as function of mass specific enthalpy at 1 atm (fit assumes constant specific heat capacity).

    Args:
        h (float): Specific enthalpy in J/kg
        p (float): Pressure in Pa

    Returns:
        float: Specific heat capacity in J/(kg K)
    """
    return 1272*h**0