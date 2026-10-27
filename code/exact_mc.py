"""Exact-sampling Monte Carlo of the ORIGINAL reset process (Section 8, Figure 1).

Usage:  python -I code/exact_mc.py --out DIR [--chunks 40]

No time discretisation enters the probabilities.  Brownian cycles are sampled
exactly through the joint law of the endpoint and the maximum of a Brownian
segment (Brownian-bridge maximum); bounded-variation inputs are simulated
event by event.  Writes DIR/exact_mc.json and DIR/resetting_endpoint_profiles.{pdf,png}.
The Brownian and bounded-variation samplers follow the methodology referee's
independent script (round-1 review); the random-reset-position test is new.
Only the illustrative sample paths in panel (a) of Figure 1 use a time grid.
"""
from pathlib import Path
import argparse
import json
import math
import os
import sys
import tempfile

import numpy as np

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "levy_reset_mpl"))
import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import levy_reset_lib as L  # noqa: E402

T, LAM = 1.0, 1.0
BETA = math.sqrt(2.0)
CHUNK = 1_000_000


def brownian(rng, n, reset_pos):
    """Driftless unit BM, rate-1 resetting to reset_pos(rng, k), stationary start."""
    y = reset_pos(rng, n) + rng.laplace(0.0, 1 / BETA, n)   # Y_0 = R_0 + xi_{e_lambda}
    H = y.copy()
    t = np.zeros(n)
    first = np.full(n, np.inf)
    alive = np.ones(n, bool)
    while alive.any():
        idx = np.flatnonzero(alive)
        e = rng.exponential(1 / LAM, idx.size)
        ell = np.maximum(np.minimum(e, T - t[idx]), 0.0)
        Bn = rng.standard_normal(idx.size) * np.sqrt(ell)
        U = rng.random(idx.size)
        m = (Bn + np.sqrt(Bn * Bn - 2 * ell * np.log(U))) / 2     # exact segment maximum
        H[idx] = np.maximum(H[idx], y[idx] + m)
        reset = t[idx] + e < T
        new = reset_pos(rng, idx.size)
        H[idx] = np.where(reset, np.maximum(H[idx], new), H[idx])
        isfirst = reset & np.isinf(first[idx])
        first[idx[isfirst]] = (t[idx] + e)[isfirst]
        y[idx] = np.where(reset, new, y[idx] + Bn)
        t[idx] = np.where(reset, t[idx] + e, T)
        alive[idx] = reset
    return H, y, first


def fixed0(rng, k):
    return np.zeros(k)


def unif(rng, k):
    return rng.uniform(-1.0, 1.0, k)


def bv_free(rng, ell, rate, jmean):
    """xi_t = t - S_t, S compound Poisson(rate) with Exp(mean jmean) jumps; endpoint and max on [0, ell]."""
    x = np.zeros(ell.size)
    mx = np.zeros(ell.size)
    s = np.zeros(ell.size)
    go = np.ones(ell.size, bool)
    while go.any():
        i = np.flatnonzero(go)
        g = rng.exponential(1 / rate, i.size)
        jump = s[i] + g < ell[i]
        dt = np.where(jump, g, ell[i] - s[i])
        x[i] += dt
        mx[i] = np.maximum(mx[i], x[i])
        x[i] -= np.where(jump, rng.exponential(jmean, i.size), 0.0)
        s[i] += dt
        go[i] = jump
    return x, mx


def bv(rng, n):
    y, _ = bv_free(rng, rng.exponential(1 / LAM, n), 1.0, 1.0)
    H = y.copy()
    t = np.zeros(n)
    alive = np.ones(n, bool)
    while alive.any():
        idx = np.flatnonzero(alive)
        e = rng.exponential(1 / LAM, idx.size)
        ell = np.minimum(e, T - t[idx])
        x, mx = bv_free(rng, ell, 1.0, 1.0)
        H[idx] = np.maximum(H[idx], y[idx] + mx)
        reset = t[idx] + e < T
        y[idx] = np.where(reset, 0.0, y[idx] + x)
        t[idx] = np.where(reset, t[idx] + e, T)
        alive[idx] = reset
    return H


def binom(k, n, scale=1.0):
    p = k / n
    return {"estimate": p * scale, "se": math.sqrt(p * (1 - p) / n) * scale}


def ks_exp(x, rate):
    x = np.sort(x)
    F = 1 - np.exp(-rate * x)
    n = x.size
    return float(max(np.max(np.arange(1, n + 1) / n - F), np.max(F - np.arange(n) / n)))


def run_brownian(rng, chunks, reset_pos, us, hist_u=None, edges=None):
    N = 0
    acc = {u: dict(joint=0, H=0, noreset=0, exc=0.0, S=np.zeros(3)) for u in us}
    excess = {u: [] for u in us}
    hist = np.zeros(len(edges) - 1) if edges is not None else None
    for _ in range(chunks):
        H, Y, first = brownian(rng, CHUNK, reset_pos)
        N += H.size
        for u in us:
            c = H > u
            a = acc[u]
            a["joint"] += int((c & (Y > 0)).sum())
            a["H"] += int(c.sum())
            a["noreset"] += int((c & np.isinf(first)).sum())
            a["exc"] += float((H[c] - u).sum())
            for j, s in enumerate((0.25, 0.5, 0.75)):
                a["S"][j] += int((c & (first <= s)).sum())
            if len(excess[u]) < 40:
                excess[u].append(H[c] - u)
        if hist is not None:
            hist += np.histogram(Y[H > hist_u], bins=edges)[0]
    return N, acc, {u: np.concatenate(v) for u, v in excess.items()}, hist


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--chunks", type=int, default=40, help="millions of Brownian paths per experiment")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    for name in ("exact_mc.json", "resetting_endpoint_profiles.pdf", "resetting_endpoint_profiles.png"):
        if (args.out / name).exists():
            raise SystemExit(f"refusing to overwrite {args.out / name}")
    rng = np.random.default_rng(20261027)
    DT, AT = L.D(T), L.A(T)
    out = {"seed": 20261027, "paths_per_brownian_experiment": args.chunks * CHUNK}

    # 1. Brownian, fixed reset point r = 0 (Theorem 1, Corollary 3.4, Propositions 5.2-5.3).
    us = [2.0, 3.0, 4.0]
    edges = np.linspace(-4.5, 8.5, 131)
    N, acc, exc, hist = run_brownian(rng, args.chunks, fixed0, us, hist_u=3.0, edges=edges)
    res = {}
    for u in us:
        a = acc[u]
        sc = math.exp(BETA * u)
        lead_joint = L.Q_tail(-u, T) + 0.5 * (DT - AT)
        res[str(u)] = {
            "scaled_joint_H_gt_u_YT_gt_0": binom(a["joint"], N, sc), "theory_finite_u_leading": lead_joint,
            "theory_limit_C_1": L.C_closed(T),
            "scaled_H_gt_u": binom(a["H"], N, sc), "theory_D_1": DT,
            "no_reset_fraction_given_H": binom(a["noreset"], a["H"]), "theory_A_over_D": AT / DT,
            "first_reset_cdf_given_H": {str(s): binom(int(a["S"][j]), a["H"]) for j, s in enumerate((0.25, .5, .75))},
            "theory_first_reset_cdf": {str(s): LAM * L.int_A0(s) / DT for s in (0.25, .5, .75)},
            "mean_excess": a["exc"] / a["H"], "theory_mean_excess": 1 / BETA,
            "excess_ks_vs_exp_beta": ks_exp(exc[u], BETA), "n_conditional": a["H"]}
    out["brownian_fixed_reset"] = res

    # 2. Random reset positions R ~ Uniform[-1,1] (Theorem 7.3).
    m = math.sinh(BETA) / BETA
    N2, acc2, exc2, _ = run_brownian(rng, args.chunks, unif, [3.0, 4.0])
    res2 = {"m_rho": m}
    for u, a in acc2.items():
        sc = math.exp(BETA * u)
        res2[str(u)] = {"scaled_joint_H_gt_u_YT_gt_0": binom(a["joint"], N2, sc), "theory_limit": m * L.C_closed(T),
                        "scaled_H_gt_u": binom(a["H"], N2, sc), "theory_limit_H": m * DT,
                        "no_reset_fraction_given_H": binom(a["noreset"], a["H"]), "theory_A_over_D": AT / DT,
                        "mean_excess": a["exc"] / a["H"], "theory_mean_excess": 1 / BETA,
                        "excess_ks_vs_exp_beta": ks_exp(exc2[u], BETA), "n_conditional": a["H"]}
    out["brownian_uniform_reset_positions"] = res2

    # 3. Bounded variation xi = t - S (Corollary 7.2): exact for u >= dT = 1.
    beta_bv = (1 + math.sqrt(5)) / 2
    psi_p = (beta_bv ** 2 + 2 * beta_bv) / (1 + beta_bv) ** 2
    a_bv = LAM / (beta_bv * psi_p)
    # D_T by identity (7.1): tilted law has drift 1, jump rate 1/(1+beta), Exp(1+beta) jumps.
    Mt = np.concatenate([bv_free(rng, np.full(CHUNK, T), 1 / (1 + beta_bv), 1 / (1 + beta_bv))[1]
                         for _ in range(4)])
    D_bv = a_bv * (1 + beta_bv * Mt.mean())
    D_bv_se = a_bv * beta_bv * Mt.std() / math.sqrt(Mt.size)
    cnt = {1.0: 0, 1.5: 0, 2.5: 0}
    M = 0
    exs = []
    for _ in range(max(1, args.chunks // 2)):
        H = bv(rng, CHUNK)
        M += H.size
        for u in cnt:
            cnt[u] += int((H > u).sum())
        exs.append(H[H > 1.0] - 1.0)
    exs = np.concatenate(exs)
    out["bounded_variation"] = {
        "model": "xi_t = t - S_t, S compound Poisson rate 1, Exp(1) jumps; lambda = T = 1, r = 0",
        "beta": beta_bv, "a": a_bv, "D_T_via_identity_7_1": {"estimate": D_bv, "se": D_bv_se},
        "scaled_H_gt_u": {str(u): binom(c, M, math.exp(beta_bv * u)) for u, c in cnt.items()},
        "mean_excess_u1": float(exs.mean()), "theory_mean_excess": 1 / beta_bv,
        "excess_ks_vs_exp_beta": ks_exp(exs, beta_bv), "n_excess": int(exs.size)}

    # Figure 1.
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(11.6, 4.3), constrained_layout=True,
                                   gridspec_kw={"width_ratios": [1, 1.25]})
    grng = np.random.default_rng(7)
    dt = 1e-3
    grid = np.arange(0, T + dt / 2, dt)
    want = {"no reset": None, "reset": None}
    u_ill = 2.5
    while any(v is None for v in want.values()):
        y = grng.laplace(0, 1 / BETA)
        path = [y]
        resets = []
        for tt in grid[1:]:
            if grng.random() < LAM * dt:
                y = 0.0
                resets.append(tt)
            else:
                y += math.sqrt(dt) * grng.standard_normal()
            path.append(y)
        path = np.array(path)
        if path.max() > u_ill:
            k = "no reset" if not resets else "reset"
            if k == "reset" and (not 0.3 < resets[0] < 0.7 or path[: int(resets[0] / dt)].max() <= u_ill):
                continue
            if want[k] is None:
                want[k] = (path, resets)
    ax0.axhline(u_ill, color="#777777", lw=.8, ls=":")
    ax0.text(0.01, u_ill + 0.08, "level u", color="#555555", fontsize=9)
    ax0.plot(grid, want["no reset"][0], color="#9b4e9f", lw=1.1, label="no reset: ends near the peak")
    ax0.plot(grid, want["reset"][0], color="#137c79", lw=1.1, label="reset after the peak: ends low")
    for rt in want["reset"][1]:
        ax0.axvline(rt, color="#137c79", lw=.6, alpha=.35)
    ax0.set(xlabel="time t", ylabel="position", title="(a) The two ways to have a high maximum")
    ax0.legend(frameon=False, fontsize=8.5, loc="lower left")

    u = 3.0
    centres = (edges[1:] + edges[:-1]) / 2
    width = edges[1] - edges[0]
    ncond = acc[u]["H"]
    ax1.bar(centres, hist / (ncond * width), width=width, color="#cccccc", edgecolor="none",
            label=f"exact Monte Carlo, {ncond:,} paths with H > 3")
    xs = np.linspace(-4.5, 8.5, 400)
    low = np.array([L.k_density0(x, T) for x in xs]) / DT
    high = np.array([L.q(x - u, T) for x in xs]) / DT
    ax1.plot(xs, low, color="#137c79", label="reset profile K/D")
    ax1.plot(xs, high, color="#9b4e9f", label="no-reset profile q(y-u)/D")
    ax1.plot(xs, low + high, color="#b57a12", ls="--", lw=1.3, label="leading conditional density")
    ax1.axvline(u, color="#777777", lw=.8, ls=":")
    ax1.set(xlabel="endpoint Y_T", ylabel="conditional density given H_T > u",
            title="(b) Endpoint law at u = 3: theory and exact simulation")
    ax1.legend(frameon=False, fontsize=8, loc="upper left")
    for ext in ("pdf", "png"):
        fig.savefig(args.out / f"resetting_endpoint_profiles.{ext}", dpi=180)
    plt.close(fig)

    (args.out / "exact_mc.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
