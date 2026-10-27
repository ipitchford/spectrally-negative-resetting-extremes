# Assurance

| Dimension | State | Note |
|---|---|---|
| Written proofs | present | Complete written proofs of every theorem; not machine-checked. The proofs do not depend on any computation |
| Proof audit | internal | Two AI-assisted proof audits of the revised manuscript checked every result line by line; the gaps they found (Theorem 7.3 path/mark transfer, Proposition 5.2(i) uniform integrability, state space, Theorem 5.1 wording, Lemma 3.2 wording) were repaired in this version |
| High-precision and closed-form checks | passed | `code/independent_checks.py`, `code/profile_checks.py`: closed form against independent quadrature of C_T, profile masses, onset table, random-reset constants |
| Reflection brackets | passed (floating point) | Not interval-certified |
| Exact-sampling Monte Carlo | passed | `code/exact_mc.py`, `code/bv_replicate.py`: original process sampled without time discretisation; agrees with theory within sampling error once u is moderately large |
| Producer replay | passed | `code/reproduce.py` from a clean copy of the final package; deterministic outputs equal `checks/` to 1e-9 relative |
| Negative controls | passed | `negative_controls.py`: the DHM bounds are rejected as values of C_1; the uncorrected m(β)D_T normalisation (mass 0.73) is rejected; one-digit tampering is detected |
| Independent rerun | not assessed | No unaffiliated rerun |
| Formal verification | not assessed | No proof assistant |
| Specialist review | not assessed | AI-assisted review is not external specialist review |
| Editorial peer review | not assessed | None |
| Prior art | bounded | Dated bounded searches in [RESEARCH_GATES.json](RESEARCH_GATES.json); no priority claim |

Trust boundary: the general statements rest on the written proofs. Numerical values are deterministic floating-point or Monte Carlo estimates, not enclosures. The Kuznetsov–Kyprianou–Rivero theorem pointer in Lemma 3.2's side remark was not re-checked against the chapter; no result depends on it.
