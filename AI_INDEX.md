# Agent navigation

## Identity

- Release slug: `spectrally-negative-resetting-extremes`; version `1.0.0-candidate`; DOI 10.5281/zenodo.23689354 (concept DOI 10.5281/zenodo.23689353)
- Scholarly creator: Anonymous. Status: unrefereed candidate ([STATUS.md](STATUS.md))
- Manuscript: [PDF](levy_reset_extremes.pdf), [LaTeX source](levy_reset_extremes.tex) with [header](levy_reset_extremes_header.tex); human summary: [README.md](README.md)
- Machine-readable claims: [CLAIMS.json](CLAIMS.json)
- Assurance limits: [ASSURANCE.md](ASSURANCE.md); internal review summary: [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md)
- Provenance: [PROVENANCE.md](PROVENANCE.md); prior art and limitation triage: [RESEARCH_GATES.json](RESEARCH_GATES.json)
- Citation: [CITATION.cff](CITATION.cff), [Zenodo metadata](.zenodo.json); licences: [LICENSES.md](LICENSES.md)

## Scientific map

Object: Y_t = Y_0 + ξ_t + ∫(r − Y_{s−}) dN_s, with ξ spectrally negative Lévy (Laplace exponent ψ), N Poisson of rate λ, Y_0 stationary. β solves ψ(β) = λ, a = λ/(βψ'(β)), A(t) = a e^{−λt} E e^{βM_t}, D_T = A(T) + λ∫_0^T A. H_T = sup_{[0,T]} Y. Source: Dębicki, Hashorva and Michna (MCAP 2026, doi:10.1007/s11009-026-10316-4), Remark 3.

- **Endpoint theorem** (Theorem 3.1, proof): ‖P(H_T>u, Y_T∈·) − e^{−β(u−r)}{Q_T(·−u)+K_T}‖_var ≤ (aβ/(γ−β)+λT) e^{Tψ(γ)−γ(u−r)}, every γ>β, uniform over all sets.
- **Conditional path** (Theorem 5.1, Propositions 5.2–5.3, proof): no-reset odds A(T):(D_T−A(T)); overshoot Exp(β) independent of marks; mean overshoot → 1/β.
- **Brownian constant** (Corollary 6.1, proof): C_T in closed form; both DHM bounds strict; C_1 = 1.3285764327711… ([checks/independent_checks.json](checks/independent_checks.json)).
- **Extensions** (Corollary 7.2, Theorem 7.3, proof): exactness for bounded variation when u − r ≥ dT; random reset positions with tilted initial position and unchanged mark law.

Do not read: the leading constant as a hard new computation (it is standard first-cycle); numerical values as enclosures; any claim for upward jumps, renewal clocks or growing horizons.

## Replay

Python 3.12 with numpy, scipy, matplotlib ([requirements.txt](requirements.txt); [ENVIRONMENT.txt](ENVIRONMENT.txt)):

```sh
python3 -B -O negative_controls.py                       # standard library; wrong constants and normalisation are rejected
uv run --python 3.12 --with-requirements requirements.txt python -I code/reproduce.py --out NEW_EMPTY_DIR --pdf
shasum -a 256 -c SHA256SUMS
```

Scripts: [code/levy_reset_lib.py](code/levy_reset_lib.py), [code/independent_checks.py](code/independent_checks.py), [code/profile_checks.py](code/profile_checks.py), [code/exact_mc.py](code/exact_mc.py), [code/bv_replicate.py](code/bv_replicate.py), [code/reproduce.py](code/reproduce.py); outputs: [checks/](checks/), [figures/](figures/).

## Useful next research question

Extend the endpoint theorem to light-tailed upward jumps (ladder-overshoot profiles) or to renewal reset clocks, or quantify the left tail of Q_T for spectrally negative stable inputs.
