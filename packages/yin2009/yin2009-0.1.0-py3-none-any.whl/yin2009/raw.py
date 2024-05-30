"""
Raw formalisms as written in paper
"""
import math

from evers2010.constants import gas_constant


def eq2(cc, gamma_star, vcmax, kmc, oxygen, kmo, rd):
    return (cc - gamma_star) * vcmax / (cc + kmc(1 + oxygen / kmo)) - rd


def eq3a(cc, gamma_star, j_maj, rd):
    return (cc - gamma_star) * j_maj / (4 * cc + 8 * gamma_star) - rd


def eq3b(cc, gamma_star, j_maj, rd):
    return (cc - gamma_star) * j_maj / (4.5 * cc + 10.5 * gamma_star) - rd


def eq4(alpha_ll, i_abs, jmax, theta):
    fac = alpha_ll * i_abs + jmax
    return (fac + math.sqrt(fac * 2 - 4 * theta * jmax * alpha_ll * i_abs)) / (2 * theta)


def eq5(temp, v25, e_act):
    tk = 273.15 + temp
    t25 = 273.15 + 25
    return v25 * math.exp((tk - t25) * e_act / (t25 * gas_constant * tk))


def _eq6(tk, d, s):
    return 1 + math.exp((tk * s - d) / (gas_constant * tk))


def eq6(temp, v25, e, d, s):
    tk = 273.15 + temp
    t25 = 273.15 + 25

    sca1 = math.exp((tk - t25) * e / (t25 * tk * gas_constant))
    sca2 = _eq6(t25, d, s) / _eq6(tk, d, s)

    return v25 * sca1 * sca2


def eq7(oxygen, sco):
    return 0.5 * oxygen / sco


def eq8(alpha_ll, cc, gamma_star):
    return alpha_ll * (cc - gamma_star) / (4.5 * cc + 10.5 * gamma_star)


def eq9(cc, gamma_star, vcmax, kmc, oxygen, kmo):
    return (cc - gamma_star) * vcmax / (cc + kmc(1 + oxygen / kmo))


def eq13(s, phi2_ll):
    return s * phi2_ll


def eq14(kappa_ll, i_abs, jmax, theta):
    fac = kappa_ll * i_abs + jmax

    return (fac - math.sqrt(fac ** 2 - 4 * theta * jmax * kappa_ll * i_abs)) / (2 * theta)


def eq15(g0, an, rd, ci, ci_star, fvpd):
    return g0 + (an + rd) / (ci - ci_star) * fvpd


def eq15a(vpd, a1, b1):
    return 1 / (1 / (a1 - b1 * vpd) - 1)


def eq16(ca, an, gb, gs):
    return ca - an * (1 / gb + 1 / gs)


def eq17(ci, an, gm):
    return ci - an / gm


def eq18(cc, gamma_star, x1, x2, rd):
    return (cc - gamma_star) * x1 / (cc + x2) - rd


# appendix A
def eq19(p, q, r):
    qmaj = (p ** 2 - 3 * q) / 9
    umaj = (2 * p ** 3 - 9 * p * q + 27 * r) / 54
    psi = math.acos(umaj / math.sqrt(qmaj ** 3))

    return [-2 * math.sqrt(qmaj) * math.cos((psi + 2 * i * math.pi) / 3) - p / 3 for i in range(3)]


# appendix B
def app_b(ca, x1, x2, gamma_star, rd, g0, gm, gb, fvpd):
    a = g0 * (x2 + gamma_star) + (g0 / gm + fvpd) * (x1 - rd)
    b = ca * (x1 - rd) - gamma_star * x1 - rd * x2
    c = ca + x2 + (1 / gm + 1 / gb) * (x1 - rd)
    d = x2 + gamma_star + (x1 - rd) / gm
    m = 1 / gm + (g0 / gm + fvpd) * (1 / gm + 1 / gb)

    p = -(d + (x1 - rd) / gm + a * (1 / gm + 1 / gb) + (g0 / gm + fvpd) * c) / m
    q = (d * (x1 - rd) + a * c + (g0 / gm + fvpd) * b) / m
    r = -a * b / m

    return p, q, r
