"""Analytic Brownian formulas for 'Spectrally negative Levy resetting extremes'.

Equation numbers refer to the revised manuscript.  Pure functions only; no I/O.
"""
import math

from scipy.integrate import quad
from scipy.special import log_ndtr, ndtr


def pars(mu, lam, sig):
    """kappa, beta, a of (6.1)."""
    k = math.sqrt(mu * mu + 2 * lam * sig * sig)
    return k, (k - mu) / (sig * sig), (k + mu) / (2 * k)


def A(t, mu=0.0, lam=1.0, sig=1.0):
    """A(t) of (6.2)."""
    k, _, _ = pars(mu, lam, sig)
    return float(ndtr(k * math.sqrt(t) / sig)
                 + (mu / k) * math.exp(-lam * t) * ndtr(-mu * math.sqrt(t) / sig))


def int_A0(T, lam=1.0):
    """Closed form of int_0^T Phi(sqrt(2 lam s)) ds (driftless case)."""
    if T == 0:
        return 0.0
    z = math.sqrt(2 * lam * T)
    phi = math.exp(-z * z / 2) / math.sqrt(2 * math.pi)
    return (T - 1 / (2 * lam)) * float(ndtr(z)) + math.sqrt(T / (2 * lam)) * phi + 1 / (4 * lam)


def D(T, mu=0.0, lam=1.0, sig=1.0):
    """D_T of (2.5)."""
    if mu == 0.0:
        return A(T, 0.0, lam, sig) + lam * int_A0(T, lam)
    return A(T, mu, lam, sig) + lam * quad(lambda s: A(s, mu, lam, sig), 0, T, epsabs=1e-13)[0]


def C_closed(T, lam=1.0):
    """C_T of (6.7) for mu = r = 0."""
    z = math.sqrt(2 * lam * T)
    phi = math.exp(-z * z / 2) / math.sqrt(2 * math.pi)
    return (0.75 + lam * T / 2) * float(ndtr(z)) + math.sqrt(lam * T / 8) * phi + 0.125


def q(w, T, mu=0.0, lam=1.0, sig=1.0):
    """Translated no-reset density q_T(w) of (2.7)/(6.3)."""
    k, be, a = pars(mu, lam, sig)
    if w >= 0:
        return a * be * math.exp(-be * w)
    x = -w
    v = sig * math.sqrt(T)
    t1 = math.exp(be * x + log_ndtr(-(x + k * T) / v))
    t2 = math.exp((be - 2 * k / sig ** 2) * x + log_ndtr(-(x - k * T) / v))
    return a * be * (t1 + t2)


def Q_tail(w0, T, mu=0.0, lam=1.0, sig=1.0):
    """Q_T((w0, infinity))."""
    _, be, a = pars(mu, lam, sig)
    if w0 >= 0:
        return a * math.exp(-be * w0)
    return a + quad(lambda w: q(w, T, mu, lam, sig), w0, 0, epsabs=1e-13, limit=200)[0]


def k_density0(y, T, lam=1.0):
    """Density of K_T at y for driftless, unit-variance BM reset to r = 0.

    K_T(dy) = lam int_0^T A(s) P_0(X_{T-s} in dy) ds; after conditioning on the
    last reset this equals lam int_0^T e^{-lam t} D_{T-t} phi_t(y) dt, and t = v^2
    removes the heat-kernel singularity.
    """
    def f(v):
        if v == 0:
            return 0.0
        return (2 * lam / math.sqrt(2 * math.pi) * math.exp(-lam * v * v - y * y / (2 * v * v))
                * D(T - v * v, 0.0, lam))
    return quad(f, 0, math.sqrt(T), epsabs=1e-11, limit=200)[0]


def remainder_brownian(b, T, mu=0.0, lam=1.0, sig=1.0):
    """Explicit Brownian bound (6.6); +inf when b <= kappa T."""
    k, be, a = pars(mu, lam, sig)
    if b <= k * T:
        return math.inf
    return (a * be * sig ** 2 * T / (b - k * T) + lam * T) * math.exp(-(b - mu * T) ** 2 / (2 * sig ** 2 * T))


def remainder_sharp(b, T, gamma, mu=0.0, lam=1.0, sig=1.0):
    """Sharper bound tilde-R_gamma of Remark 3.3."""
    k, be, a = pars(mu, lam, sig)
    qq = mu * gamma + sig ** 2 * gamma ** 2 / 2
    if qq == lam:
        el = 1 + lam * T
    else:
        el = math.exp((qq - lam) * T) + lam * (math.exp((qq - lam) * T) - 1) / (qq - lam)
    return math.exp(-gamma * b) * (a * be / (gamma - be) * el + lam * (math.exp(qq * T) - 1) / qq)


def best_sharp(b, T, mu=0.0, lam=1.0, sig=1.0):
    """Minimise tilde-R_gamma over a log-spaced grid of gamma > beta."""
    _, be, _ = pars(mu, lam, sig)
    best = math.inf
    for i in range(1, 400):
        g = be * (1 + 10 ** (-3 + 6 * i / 400))
        try:
            best = min(best, remainder_sharp(b, T, g, mu, lam, sig))
        except OverflowError:
            pass
    return best
