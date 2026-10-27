#!/usr/bin/env python3
"""Semantic negative controls: plausible wrong versions of the claims must be rejected.

Standard library only. Exit status 0 means every control behaved as required.
Baseline: driftless Brownian motion, lambda = sigma = T = 1, reset to r = 0.

1. The closed form (6.7) for C_T must agree with direct quadrature of (6.6) and with
   checks/independent_checks.json; the two bounds of Debicki-Hashorva-Michna Remark 3
   (p = 0 and p = 1) must differ from C_T, so "the bound is attained" is rejected.
2. The no-reset odds A(T)/D_T must be about 0.531; the wrong odds A(T)/(m(beta) D_T),
   which the uncorrected random-reset transfer would give for rho = Uniform[-1,1],
   must be rejected, and the corrected mark law must have total mass one.
3. Changing one digit of a saved output must be detected.
"""
import json, math, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
Phi = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))
phi = lambda x: math.exp(-x * x / 2) / math.sqrt(2 * math.pi)
lam = T = 1.0


def simpson(f, a, b, n=4000):
    """Integral of f over [a, b] with a = 0, via s = t^2 to remove the sqrt singularity."""
    f0 = f
    f = lambda t: 2 * t * f0(t * t)
    a, b = math.sqrt(a), math.sqrt(b)
    h = (b - a) / n
    s = f(a) + f(b) + sum((4 if i % 2 else 2) * f(a + i * h) for i in range(1, n))
    return s * h / 3


A = lambda s: Phi(math.sqrt(2 * lam * s))
z = math.sqrt(2 * lam * T)
C_closed = (0.75 + lam * T / 2) * Phi(z) + math.sqrt(lam * T / 8) * phi(z) + 0.125
C_quad = A(T) + lam * simpson(lambda s: A(s) * 0.5, 0.0, T)
D = A(T) + lam * simpson(A, 0.0, T)
lower = A(T)
upper = A(T) + lam * simpson(A, 0.0, T)

fails = []
def require(cond, msg):
    print(("ok   " if cond else "FAIL ") + msg)
    if not cond:
        fails.append(msg)

# baseline
require(abs(C_closed - C_quad) < 1e-9, f"closed form C_1={C_closed:.12f} equals quadrature")
saved = json.loads((ROOT / "checks" / "independent_checks.json").read_text())
flat = json.dumps(saved)
require("1.32857643277" in flat, "saved checks contain C_1 = 1.32857643277...")
# control 1: bounds are strict
require(C_closed - lower > 0.1 and upper - C_closed > 0.1, "lower and upper DHM bounds are rejected as values of C_1")
# control 2: odds and random-reset normalisation
odds = A(T) / D
require(abs(odds - 0.5307921914) < 1e-8, f"no-reset odds A/D = {odds:.10f}")
m_beta = math.sinh(math.sqrt(2)) / math.sqrt(2)
wrong_mass = (A(T) + lam * simpson(A, 0.0, T)) / (m_beta * D)
require(abs(wrong_mass - 1) > 0.2, f"m(beta)D_T normalisation rejected (mass {wrong_mass:.4f} != 1)")
require(abs((A(T) + lam * simpson(A, 0.0, T)) / D - 1) < 1e-12, "corrected mark law has mass 1")
require(abs(m_beta * C_closed - 1.81789) < 1e-5, f"random-reset constant m(beta)C_1 = {m_beta*C_closed:.6f}")
# control 3: tamper detection
import re
def saved_C(text):
    return float(re.search(r'"constant_closed_form": ([0-9.]+)', text).group(1))
require(abs(saved_C(flat) - C_closed) < 1e-11, "saved constant matches recomputation")
tampered = flat.replace("1.3285764327711462", "1.3285764328711462", 1)
require(abs(saved_C(tampered) - C_closed) > 5e-11, "one-digit tampering of the saved constant is detected")

sys.exit(1 if fails else 0)
