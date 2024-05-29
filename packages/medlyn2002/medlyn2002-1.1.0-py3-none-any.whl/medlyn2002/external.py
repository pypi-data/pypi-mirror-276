"""
External formalisms used in the article without explicit formulation
"""

gas_constant = 8.31446
"""[J.K-1.mol-1] Ideal gas constant

References: https://en.wikipedia.org/wiki/Gas_constant
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
