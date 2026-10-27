# Status

Version: 1.0.0-candidate (27 October 2026). DOI: [10.5281/zenodo.23689354](https://doi.org/10.5281/zenodo.23689354). Scholarly creator: Anonymous.

**Unrefereed research candidate.** The manuscript has not been peer reviewed by a journal or by named human specialists. It was checked by internal AI-assisted review in several roles, AI-assisted proof audits and a verification re-review (see [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md)). That is not peer review, independent reproduction or formal verification.

Object: a spectrally negative Lévy process reset to a fixed (or random) position at the jumps of an independent Poisson clock, started in its invariant law; the joint law of the maximum H_T over a fixed window and the endpoint Y_T as the threshold u → ∞. Source question: Dębicki, Hashorva and Michna, *Distributional and extremal behaviour of Brownian motion with exponential resetting*, Methodology and Computing in Applied Probability 28(3), article 79 (2026), doi:10.1007/s11009-026-10316-4, Remark 3.

* **Proved in writing:** Theorem 3.1 (two-profile endpoint decomposition with explicit total-variation error, uniform over all endpoint sets); Theorem 5.1 (conditional marked-path law); Propositions 5.2–5.3 (overshoot, first reset, fixed terminal thresholds, mean overshoot, J1 path limit); Corollary 6.1 (the constant C_T of Remark 3 of Dębicki–Hashorva–Michna; their two bounds are strict); Proposition 7.1 (fluctuation identity for D_T; standard tools); Corollary 7.2 (exactness for bounded-variation inputs); Theorem 7.3 (random reset positions, including the path and mark versions).
* **Numerical:** analytic constants by closed form and independent quadrature; floating-point reflection brackets (not interval-certified); exact-sampling Monte Carlo of the original process (4×10⁷ Brownian paths per experiment, bounded-variation replicate).
* **Open:** upward jumps; renewal reset clocks; joint limits in u and T; the time of the maximum; moving reset positions; heavy left tails.

The leading constant is a standard first-cycle computation; the new content is the uniform error bound, the conditional path law and the extensions. Novelty is bounded by the searches in [RESEARCH_GATES.json](RESEARCH_GATES.json) and is stated as "we are not aware of", not as priority.
