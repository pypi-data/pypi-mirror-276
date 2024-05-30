"""
Raw formalisms as described in the article
"""
from . import appendix as app


def algo(ppfd, vpd, j_max, vc_max, tpu, gamma_star, rd, kc, ko, gb, alpha, g0, a1, d0, ca, oxygen):
    """Photosynthesis solution.

    Use iterative approach as explained p1315 in model calibration and description.

    Args:
        ppfd (float): [µmol photon.m-2.s-1] Amount of light
        vpd (float): [Pa] vapor pressure deficit
        j_max (float): [µmol.m-2.s-1] Maximum electron transport rate
        vc_max (float): [µmol.m-2.s-1] Maximum rate of Rubisco carboxylation
        tpu (float): [µmol.m-2.s-1] Triose phosphate utilization rate
        gamma_star (float): [Pa] Compensation point for CO2 in the absence of dark respiration
        rd (float): [µmol.m-2.s-1] Dark respiration in the light
        kc (float): [Pa]  Michaelis–Menten constant of Rubisco for CO2
        ko (float): [kPa]  Michaelis–Menten constant of Rubisco for O2
        gb (float): [mol H2O.m-2.s-1] boundary layer conductance
        alpha (float): [mol CO2.mol photon-1] Photochemical efficiency or initial quantum yield
        g0 (float): [mmol H2O.m-2.s-1] Residual stomatal conductance when A -> 0
        a1 (float): [?] Empirical stomatal conductance factor
        d0 (float): [?] Empirical factor assessing stomata sensitivity to VPD
        ca (float): [Pa] CO2 partial concentration in the atmosphere
        oxygen (float): [kPa] O2 partial concentration in the atmosphere

    Returns:
        (float,float,float):
          - an: [µmol CO2.m-2.s-1] Net carbon assimilation
          - ci: [Pa] Partial pressure of CO2 in the intercellular space
          - gs: [mmol H2O.m-2.s-1] Stomatal conductance to H2O flux
    """
    ci_next = ca * 0.7  # init value
    for i in range(1000):
        ci = ci_next

        j = app.eq6(ppfd, alpha, j_max)

        ac = app.eq3(vc_max, ci, oxygen, kc, ko)
        aj = app.eq4(j, ci, gamma_star)
        ap = app.eq5(tpu, ci, gamma_star)

        vc = app.eq2(ac, aj, ap)
        an = app.eq1(vc, ci, gamma_star, rd)

        cs = app.eq11(an, ca, gb)
        gs = app.eq10(an, vpd, cs, gamma_star, g0, a1, d0)

        ci_next = app.eq12(an, ca, gb, gs)
        if abs(ci_next - ci) < 1e-2:  # [Pa]
            return an, ci, gs

    raise ArithmeticError("algo didn't converge")
