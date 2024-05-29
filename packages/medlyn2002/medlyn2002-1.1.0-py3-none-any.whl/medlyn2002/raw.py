"""
Raw formalisms from article
"""
import math

from .external import gas_constant, kelvin


def eq1(ac, aj, rd):
    """Net photosynthesis.

    Args:
        ac (float): [µmol CO2.m-2.s-1] rubisco activity limiting
        aj (float): [µmol CO2.m-2.s-1] RuBP regeneration limited
        rd (float): [µmol CO2.m-2.s-1] rate of mitochondrial respiration

    Returns:
        an (float): [µmol CO2.m-2.s-1]
    """
    return min(ac, aj) - rd


def eq2(ci, vc_max, gamma_star, kc, ko, oi):
    """Rubisco activity limited photosynthesis.

    Args:
        ci (float): [µmol.mol-1] CO2 intercellular concentration
        vc_max (float): [µmol CO2.m-2.s-1] maximum activity of Rubisco
        gamma_star (float): [µmol.mol-1] CO2 compensation point in the absence of
                            mitochondrial respiration
        kc (float): [µmol.mol-1] Michaelis coefficient for CO2
        ko (float): [mmol.mol-1] Michaelis coefficient for O2
        oi (float): [mmol.mol-1] O2 intercellular concentration

    Returns:
        ac (float): [µmol CO2.m-2.s-1]
    """
    denom = ci + kc * (1 + oi / ko)
    return vc_max * (ci - gamma_star) / denom


def eq3(j, ci, gamma_star):
    """RuBP regeneration limited photosynthesis.

    Args:
        j (float): [mol electron.m-2.s-1] electron transport rate for a given absorbed
                   photon irradiance
        ci (float): [mol.mol-1] CO2 concentration in the intercellular spaces
        gamma_star (float): [mol.mol-1] CO2 compensation point in the absence of
                            mitochondrial respiration

    Returns:
        aj (float): [mol CO2.m-2.s-1]
    """
    return j / 4 * (ci - gamma_star) / (ci + 2 * gamma_star)


def eq4(ppfd, j_max, alpha, theta):
    """Electron transport rate

    Args:
        ppfd (float): [mol photon.m-2.s-1] absorbed photon irradiance
        j_max (float): [mol electron.m-2.s-1] potential rate of whole-chain electron
                        transport per unit leaf area
        alpha (float): [mol electron.mol photon-1] quantum yield of electron transport
        theta (float): [-] parameter of the hyperbola

    Returns:
        j (float): [mol electron.m-2.s-1]
    """
    alpha_q = alpha * ppfd
    discrim = (alpha_q + j_max) ** 2 - 4 * alpha_q * j_max * theta
    # if discrim < 0:  # hopefully only happening for small values of ppfd
    #     return alpha_q

    return (alpha_q + j_max - math.sqrt(discrim)) / (2 * theta)


def eq5(tk):
    """Michaelis coefficient for CO2.

    Notes: valid only in the range 10-40 °C

    Args:
        tk (float): [K] leaf temperature

    Returns:
        kc (float): [µmol.mol-1]
    """
    t_ref = 298
    ha = 79430
    kc_ref = 404.9

    return kc_ref * math.exp(ha * (tk - t_ref) / (gas_constant * t_ref * tk))


def eq6(tk):
    """Michaelis coefficient for O2.

    Notes: valid only in the range 10-40 °C

    Args:
        tk (float): [K] leaf temperature

    Returns:
        ko (float): [mmol.mol-1]
    """
    t_ref = 298
    ha = 36380
    ko_ref = 278.4

    return ko_ref * math.exp(ha * (tk - t_ref) / (gas_constant * t_ref * tk))


def eq7_8(tk):
    """Michaelis coefficient for CO2.

    Notes: valid only in the range 5-35 °C

    Args:
        tk (float): [K] leaf temperature

    Returns:
        kc (float): [µmol.mol-1]
    """
    t_ref = 298
    if tk > kelvin(15):
        ha = 59536
        kc_ref = 460
    else:
        ha = 109700
        kc_ref = 920

    return kc_ref * math.exp(ha * (tk - t_ref) / (gas_constant * t_ref * tk))


def eq9(tk):
    """Michaelis coefficient for O2.

    Notes: valid only in the range 5-35 °C

    Args:
        tk (float): [K] leaf temperature

    Returns:
        ko (float): [mmol.mol-1]
    """
    t_ref = 298
    ha = 35948
    ko_ref = 330

    return ko_ref * math.exp(ha * (tk - t_ref) / (gas_constant * t_ref * tk))


def eq10(tk):
    """Michaelis coefficient for CO2.

    Notes: valid only in the range 5-40 °C

    Args:
        tk (float): [K] leaf temperature

    Returns:
        kc (float): [µmol.mol-1]
    """
    t_ref = 298
    ha = 80500
    kc_ref = 274.6

    return kc_ref * math.exp(ha * (tk - t_ref) / (gas_constant * t_ref * tk))


def eq11(tk):
    """Michaelis coefficient for O2.

    Notes: valid only in the range 5-40 °C

    Args:
        tk (float): [K] leaf temperature

    Returns:
        ko (float): [mmol.mol-1]
    """
    t_ref = 298
    ha = 14500
    ko_ref = 419.8

    return ko_ref * math.exp(ha * (tk - t_ref) / (gas_constant * t_ref * tk))


def eq12(tk):
    """CO2 compensation point.

    Args:
        tk (float): [K] leaf temperature

    Returns:
        gamma_star (float): [µmol.mol-1]
    """
    t_ref = 298
    ha = 37830
    gamma_star_ref = 42.75

    return gamma_star_ref * math.exp(ha * (tk - t_ref) / (gas_constant * t_ref * tk))


def eq13(kc, ko, oi):
    """CO2 compensation point.

    Args:
        kc (float): [µmol.mol-1] Michaelis coefficient for CO2
        ko (float): [mmol.mol-1] Michaelis coefficient for O2
        oi (float): [mmol.mol-1] O2 intercellular concentration

    Returns:
        gamma_star (float): [µmol.mol-1]
    """
    vo_max_vc_max = 0.21  # text under eq13

    return kc * oi * vo_max_vc_max / (2 * ko)


def eq14(tk):
    """CO2 specificity factor.

    Warnings: typo in paper, tau = Ko Vcmax / (Kc Vomax) (inverse of formula in paper)

    Args:
        tk (float): [K] leaf temperature

    Returns:
        tau (float): [-]
    """
    t_ref = 298
    ha = -29000
    tau_ref = 2.321

    return tau_ref * math.exp(ha * (tk - t_ref) / (gas_constant * t_ref * tk))


def eq15(tk):
    """CO2 compensation point.

    Notes: valid only in the range 15-30 °C

    Args:
        tk (float): [K] leaf temperature

    Returns:
        gamma_star (float): [µmol.mol-1]
    """
    t_ref = 298

    return 42.7 + 1.68 * (tk - t_ref) + 0.0012 * (tk - t_ref) ** 2


def eq16(tk, k25, ea):
    """Arrhenius law.

    Args:
        tk (float): [K] leaf temperature
        k25 (float): [unit] value of parameter at 25 °C
        ea (float): [J.mol-1] exponential rate of rise of the function

    Returns:
        (float): [unit]
    """
    t_ref = 298

    return k25 * math.exp(ea * (tk - t_ref) / (gas_constant * t_ref * tk))


def eq17(tk, k25, ha, hd, delta_s):
    """Peaked Arrhenius law.

    Args:
        tk (float): [K] leaf temperature
        k25 (float): [unit] value of parameter at 25 °C
        ha (float): [J.mol-1] exponential rate of rise of the function
        hd (float): [J.mol-1] exponential rate of decrease of the function
        delta_s (float): [J.mol-1.K-1] non interpretable

    Returns:
        (float): [unit]
    """
    t_ref = 298
    num = 1 + math.exp((t_ref * delta_s - hd) / (t_ref * gas_constant))
    denom = 1 + math.exp((tk * delta_s - hd) / (tk * gas_constant))

    return eq16(tk, k25, ha) * num / denom


def eq18(tk, t_opt, k_opt, ha, hd):
    """Peaked Arrhenius law.

    Args:
        tk (float): [K] leaf temperature
        t_opt (float): [K] optimum leaf temperature
        k_opt (float): [unit] value of parameter at t_opt
        ha (float): [J.mol-1] exponential rate of rise of the function
        hd (float): [J.mol-1] exponential rate of decrease of the function

    Returns:
        (float): [unit]
    """
    num = hd * math.exp(ha * (tk - t_opt) / (tk * gas_constant * t_opt))
    denom = hd - ha * (1 - math.exp(hd * (tk - t_opt) / (tk * gas_constant * t_opt)))
    return k_opt * num / denom


def eq19(ha, hd, delta_s):
    """Optimal temperature.

    Args:
        ha (float): [J.mol-1] activation energy
        hd (float): [J.mol-1] deactivation energy
        delta_s (float): [J.mol-1.K-1] entropy

    Returns:
        t_opt (float): [K]
    """
    return hd / (delta_s - gas_constant * math.log(ha / (hd - ha)))


def eq19_inv(ha, hd, t_opt):
    """Entropy term in formalism from optimal temperature.

    Args:
        ha (float): [J.mol-1] activation energy
        hd (float): [J.mol-1] deactivation energy
        t_opt (float): [K] optimal temperature

    Returns:
        delta_s (float): [J.mol-1.K-1] entropy
    """
    return hd / t_opt + gas_constant * math.log(ha / (hd - ha))
