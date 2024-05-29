"""
Raw formalisms directly extracted from the article
"""
import math

gas_constant = 0.00831  # [kJ.K-1.mol-1]


def eq1(vc, ci, o, tau, rd):
    """Net CO2 assimilation.

    Args:
        vc (float): [µmol CO2.m-2.s-1] rate of carboxylation
        ci (float): [Pa] partial pressure of CO2 in the intercellular space
        o (float): [Pa] partial pressure of O2 in the intercellular space
        tau (float): [-] Specificity factor for Rubisco
        rd (float): [Pa] rate of CO2 evolution in the light resulting from processes
                    other than photorespiration

    Returns:
        (float): A [µmol CO2.m-2.s-1]
    """
    return vc * (1 - 0.5 * o / tau / ci) - rd


def eq2(wc, wj, wp):
    """Rate of carboxylation.

    Args:
        wc (float): [µmol CO2.m-2.s-1] rate of carboxylation limited solely by
                    the amount, activation state and kinetic properties of Rubisco
        wj (float): [µmol CO2.m-2.s-1] rate of carboxylation limited solely by
                    the rate of RuBP regeneration in the Calvin cycle
        wp (float): [µmol CO2.m-2.s-1] rate of carboxylation limited solely by
                    inorganic phosphate

    Returns:
        (float): Vc [µmol CO2.m-2.s-1]
    """
    return min(wc, wj, wp)


def eq4(vc_max, ci, o, kc, ko):
    """rate of carboxylation limited solely by kinetic properties of Rubisco.

    Args:
        vc_max (float): [µmol CO2.m-2.s-1] maximum rate of carboxylation
        ci (float): [Pa] partial pressure of CO2 in the intercellular space
        o (float): [kPa] partial pressure of O2 in the intercellular space
        kc (float): [Pa CO2] Michaelis constant for carboxylation
        ko (float): [kPa O2] Michaelis constant for oxygenation

    Returns:
        (float): Wc [µmol CO2.m-2.s-1]
    """
    return vc_max * ci / (ci + kc * (1 + o / ko))


def eq5(j, ci, o, tau):
    """rate of carboxylation limited solely by the rate of RuBP regeneration.

    Args:
        j (float): [µmol e-.m-2.s-1] rate of electron transport
        ci (float): [Pa] partial pressure of CO2 in the intercellular space
        o (float): [Pa] partial pressure of O2 in the intercellular space
        tau (float): [-] Specificity factor for Rubisco

    Returns:
        (float): Wj [µmol CO2.m-2.s-1] because factor 4 in equation below
    """
    return j * ci / 4 / (ci + o / tau)


def eq6(tpu, vc, ci, o, tau):
    """rate of carboxylation limited solely by inorganic phosphate.

    Args:
        tpu (float): [µmol CO2.m-2.s-1] rate of phosphate release in triose phosphate utilization
        vc (float): [µmol CO2.m-2.s-1] rate of carboxylation
        ci (float): [Pa] partial pressure of CO2 in the intercellular space
        o (float): [Pa] partial pressure of O2 in the intercellular space
        tau (float): [-] Specificity factor for Rubisco

    Returns:
        (float): Wp [µmol CO2.m-2.s-1]
    """
    return 3 * tpu + vc * 0.5 * o / ci / tau


def eq7(alpha, irr, j_max):
    """Electron transport.

    Args:
        alpha (float): [mol e-.mol photon-1] Efficiency of light energy conversion
                       on an incident light basis.
        irr (float): [µmol photon.m-2.s-1] Amount of light
        j_max (float): [µmol e-.m-2.s-1] light saturated rate of electron transport.

    Returns:
        (float): J [µmol e-.m-2.s-1]
    """
    return alpha * irr / math.sqrt(1 + alpha ** 2 * irr ** 2 / j_max ** 2)


def eq8(tk, c, deltaha):
    """Temperature dependency for Kc, Ko, Rd and tau.

    Args:
        tk (float): [K] leaf temperature
        c (float): scaling constant
        deltaha (float): activation energy

    Returns:
        (float): [-]
    """
    return math.exp(c - deltaha / gas_constant / tk)


def eq9(tk, c, deltaha, deltahd, deltas):
    """Temperature dependency for j_max, vc_max, tpu.

    Args:
        tk (float): [K] leaf temperature
        c (float): scaling constant
        deltaha (float): activation energy
        deltahd (float): energy of deactivation
        deltas (float): entropy term

    Returns:
        (float): [-]
    """
    return eq8(tk, c, deltaha) / (1 + math.exp((deltas * tk - deltahd) / gas_constant / tk))


def eq10(a, ca, gs):
    """Partial pressure of CO2 in the intercellular space.

    Args:
        a (float): [µmol CO2.m-2.s-1] Net carbon assimilation
        ca (float): [Pa] partial pressure of CO2 in the air outside the leaf boundary
        gs (float): [mmol H2O.m-2.s-1] Leaf conductance to H2O flux

    Returns:
        (float): Ci [Pa]
    """
    return ca - a * 1.6 * 100 / gs  # TODO potentially 1000 instead of 100


def eq11_surf(a, hs, cs, g0, gt):
    """Stomatal conductance to H2O flux.

    Args:
        a (float): [µmol CO2.m-2.s-1] Net carbon assimilation
        hs (float): [-] relative humidity at the leaf surface
        cs (float): [?] partial pressure of CO2 at the leaf surface
        g0 (float): [mmmol H2O.m-2.s-1] minimum stomatal conductance to H20 when A=0
        gt (float): empirical coefficient

    Returns:
        (float): gs [mmmol H2O.m-2.s-1]
    """
    return g0 + gt * a * hs / cs


def eq11_ext(a, rh, ca, g0, gt):
    """Stomatal conductance to H2O flux.

    Args:
        a (float): [µmol CO2.m-2.s-1] Net carbon assimilation
        rh (float): [%] relative humidity in the air
        ca (float): [Pa] partial pressure of CO2 in the air outside the leaf boundary
        g0 (float): [mmmol H2O.m-2.s-1] minimum stomatal conductance to H20 when A=0
        gt (float): [mmol H2O.Pa CO2.µmol CO2-1] empirical coefficient

    Returns:
        (float): gs [mmmol H2O.m-2.s-1]
    """
    return g0 + gt * a * rh / ca


def algo(irr, rh, ca, o, g0, gt, tau, rd, vc_max, kc, ko, alpha, j_max, tpu):
    """Algo to find An and Ci from p273 end of model description.

    Args:
        irr (float): [µmol photon.m-2.s-1] Amount of light
        rh (float): [%] relative humidity in the air
        ca (float): [Pa] partial pressure of CO2 in the air outside the leaf boundary
                    leaf.
        o (float): [Pa] partial pressure of O2 in the intercellular space
        g0 (float): [mmol H2O.m-2.s-1] minimum stomatal conductance to H20 when A=0
        gt (float): [mmol H2O.Pa CO2.µmol CO2-1] empirical coefficient
        tau (float): [-] Specificity factor for Rubisco
        rd (float): [Pa] rate of CO2 evolution in the light resulting from processes
                    other than photorespiration
        vc_max (float): [µmol CO2.m-2.s-1] maximum rate of carboxylation
        kc (float): [Pa CO2] Michaelis constant for carboxylation
        ko (float): [kPa O2] Michaelis constant for oxygenation
        alpha (float): [mol e-.mol photon-1] Efficiency of light energy conversion
                       on an incident light basis.
        j_max (float): [µmol e-.m-2.s-1] light saturated rate of electron transport.
        tpu (float): [µmol CO2.m-2.s-1] rate of phosphate release in triose phosphate
                     utilization

    Returns:
        (float, float, float):
          - an: [µmol CO2.m-2.s-1] Net carbon assimilation
          - ci: [Pa] Partial pressure of CO2 in the intercellular space
          - gs: [mmol H2O.m-2.s-1] Stomatal conductance to H2O flux
    """
    ci_next = ca  # init value
    vc = 0  # init value
    for i in range(1000):
        ci = ci_next

        j = eq7(alpha, irr, j_max)

        wc = eq4(vc_max, ci, o * 1e-3, kc, ko)
        wj = eq5(j, ci, o, tau)
        wp = eq6(tpu, vc, ci, o, tau)

        vc = eq2(wc, wj, wp)
        an = eq1(vc, ci, o, tau, rd)

        gs = eq11_ext(an, rh, ca, g0, gt)

        ci_next = eq10(an, ca, gs)
        if abs(ci_next - ci) < 0.01:  # [Pa]
            return an, ci, gs

    raise ArithmeticError("algo didn't converge")
