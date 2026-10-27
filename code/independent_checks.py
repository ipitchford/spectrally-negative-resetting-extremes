"""Deterministic analytic checks for the resetting manuscript (Section 8).

Usage:  python -I code/independent_checks.py --out DIR
Writes DIR/independent_checks.json.  Floating-point quadrature supports the
proofs; it is not an interval-certified computation.
"""
from pathlib import Path
import argparse
import json
import math
import sys

import numpy as np
from scipy.integrate import quad
from scipy.special import ndtr

sys.path.insert(0, str(Path(__file__).resolve().parent))
import levy_reset_lib as L  # noqa: E402


def brownian_constants():
    lam, T = 1.0, 1.0
    closed = L.C_closed(T, lam)
    integrated = L.A(T) + lam / 2 * quad(L.A, 0, T, epsabs=1e-13)[0]
    assert abs(closed - integrated) < 1e-11
    q_mass = (quad(lambda w: L.q(w, T), -np.inf, 0, epsabs=1e-13)[0]
              + quad(lambda w: L.q(w, T), 0, np.inf, epsabs=1e-13)[0])
    assert abs(q_mass - L.A(T)) < 1e-10
    return {"parameters": {"lambda": lam, "sigma": 1, "T": T, "r": 0, "mu": 0},
            "constant_closed_form": closed, "constant_independent_quadrature": integrated,
            "q_integrated_mass": q_mass, "A_T": L.A(T), "D_T": L.D(T),
            "conditional_no_reset_weight": L.A(T) / L.D(T), "mean_excess_1_over_beta": 1 / math.sqrt(2)}


def reflection_brackets():
    """L_u <= e^{sqrt2 u} P(H_1>u, Y_1>0) <= U_u (Section 8); first-cycle only plus union bound."""
    T, beta = 1.0, math.sqrt(2.0)
    dens = lambda x: beta / 2 * math.exp(-beta * abs(x))

    def initial_max_prob(u, t):
        if t == 0:
            return .5 * math.exp(-beta * u)
        v = math.sqrt(t)
        f = lambda x: dens(x) * 2 * ndtr((x - u) / v)
        return .5 * math.exp(-beta * u) + quad(f, -np.inf, 0, epsabs=1e-14)[0] + quad(f, 0, u, epsabs=1e-14)[0]

    def no_reset_joint(u):
        v = math.sqrt(T)
        lo = lambda x: dens(x) * (2 * ndtr((x - u) / v) - ndtr((x - 2 * u) / v))
        hi = lambda x: dens(x) * ndtr(x / v)
        return math.exp(-T) * (quad(lo, -np.inf, 0, epsabs=1e-14)[0] + quad(lo, 0, u, epsabs=1e-14)[0]
                               + quad(hi, u, np.inf, epsabs=1e-14)[0])

    out = []
    for u in [2., 3., 4., 5., 6.]:
        low = no_reset_joint(u) + .5 * quad(lambda t: math.exp(-t) * initial_max_prob(u, t), 0, T, epsabs=1e-13)[0]
        high = low + T * 2 * float(ndtr(-u / math.sqrt(T)))
        s = math.exp(beta * u)
        lead = L.Q_tail(-u, T) + 0.5 * (L.D(T) - L.A(T))
        out.append({"u": u, "scaled_probability_lower_bound": s * low, "scaled_probability_upper_bound": s * high,
                    "finite_u_leading_term": lead, "limiting_constant": L.C_closed(T)})
    return out


def onset_table():
    """Smallest b with relative bound <= 1% (driftless, sigma = 1), and dimensionless forms."""
    rows = []
    for lam in [0.25, 1.0, 4.0]:
        for T in [0.25, 1.0, 4.0]:
            k, be, _ = L.pars(0.0, lam, 1.0)
            DT = L.D(T, 0.0, lam)
            rel36 = lambda b: L.remainder_brownian(b, T, 0.0, lam) / (math.exp(-be * b) * DT)
            relsh = lambda b: L.best_sharp(b, T, 0.0, lam) / (math.exp(-be * b) * DT)

            def first(f):
                b = k * T + 1e-6
                while f(b) > 0.01:
                    b += 0.01
                return round(b, 2)
            b36, bsh = first(rel36), first(relsh)
            rows.append({"lambda": lam, "T": T, "lambda_T": lam * T, "beta": be, "D_T": DT,
                         "A_over_D": L.A(T, 0.0, lam) / DT,
                         "b_1pct_bound_6_6": b36, "beta_b_1pct_bound_6_6": round(be * b36, 2),
                         "b_1pct_sharp_bound": bsh, "beta_b_1pct_sharp_bound": round(be * bsh, 2),
                         "two_lambda_T": 2 * lam * T})
    return rows


def random_reset_constants():
    """Section 7.3 example: R ~ Uniform[-1, 1], driftless BM, lambda = T = 1."""
    beta = math.sqrt(2.0)
    m = math.sinh(beta) / beta
    return {"reset_law": "Uniform[-1,1]", "m_rho": m, "coefficient_H": m * L.D(1.0),
            "coefficient_H_and_Y_T_positive": m * L.C_closed(1.0),
            "no_reset_weight": L.A(1.0) / L.D(1.0)}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    target = args.out / "independent_checks.json"
    if target.exists():
        raise SystemExit(f"refusing to overwrite {target}")
    report = {"brownian": brownian_constants(), "reflection_brackets": reflection_brackets(),
              "onset_of_asymptotic_regime": onset_table(), "random_reset_positions": random_reset_constants(),
              "interpretation": "Brackets keep first-cycle exceedances exactly and add a union bound for later "
                                "cycles. Quadrature is floating point, not interval-certified."}
    target.write_text(json.dumps(report, indent=2) + "\n")
    print(f"wrote {target}")


if __name__ == "__main__":
    main()
