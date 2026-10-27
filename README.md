# Fixed-horizon extremes of spectrally negative Lévy processes with Poisson resetting

Version 1.0.0-candidate, 27 October 2026. DOI [10.5281/zenodo.23689354](https://doi.org/10.5281/zenodo.23689354). Creator: Anonymous. **Unrefereed research candidate** (see [STATUS.md](STATUS.md) and [ASSURANCE.md](ASSURANCE.md)).

Given that a stationary spectrally negative Lévy process with Poisson resetting has a very high maximum in a fixed window, where does it end? Up to an error smaller than any exponential order, either no reset has happened and it ends near the peak, or it was reset and ends at an ordinary level. The paper gives the odds, both endpoint laws, a total-variation bound uniform over all endpoint sets, the conditional path law, and, for Brownian motion, the constant left open in Remark 3 of Dębicki, Hashorva and Michna (2026), with proof that their two bounds are strict.

## Files

- `levy_reset_extremes.tex`, `levy_reset_extremes_header.tex`, `levy_reset_extremes.pdf`: the manuscript.
- `code/levy_reset_lib.py`: the Brownian formulas (6.1)–(6.7).
- `code/independent_checks.py`: computes:
  - the constants;
  - the reflection brackets (Table 5);
  - the onset table (Table 4);
  - the random-reset constants.
- `code/profile_checks.py`: checks profile masses and the closed form of C_T over a grid of parameters.
- `code/exact_mc.py`: an exact-sampling Monte Carlo of the original process (Table 6), which also draws Figure 1.
- `code/bv_replicate.py`: an independent bounded-variation replicate.
- `code/reproduce.py`: replays every check into a new directory.
- `checks/`, `figures/`: the shipped evidence produced by these scripts.
- `negative_controls.py`: standard-library semantic negative controls.
- Release records: `STATUS.md`, `ASSURANCE.md`, `PROVENANCE.md`, `AI_INDEX.md`, `CLAIMS.json`, `RESEARCH_GATES.json`, `CITATION.cff`, `.zenodo.json`, `LICENSES.md`, `ENVIRONMENT.txt`, `SHA256SUMS`.
- `REVIEW_SUMMARY.md`: a public summary of the internal AI-assisted review findings and the response to each (not external peer review).

## Main claims

| Claim | Location | Status |
|---|---|---|
| Two-profile endpoint decomposition with an explicit total-variation error, uniform over all endpoint sets | Theorem 3.1 | Proved |
| Conditional marked-path law | Theorem 5.1 | Proved |
| Overshoot, first-reset and fixed-threshold laws, with bounds | Proposition 5.2 | Proved |
| J1 path limit | Proposition 5.3 | Proved |
| C_T in Remark 3 of Dębicki–Hashorva–Michna (2026); the bounds there are strict | Corollary 6.1 | Proved (standard first-cycle computation) |
| D_T = a(1 + β E^(β) M_T) | Proposition 7.1 | Proved |
| Exactness for bounded-variation inputs | Corollary 7.2 | Proved |
| Random reset positions | Theorem 7.3 | Proved |

Numerical support is in §8 of the manuscript. It consists of analytic values, reflection brackets, and exact Monte Carlo with 4×10⁷ Brownian paths per experiment.

## Reproduce

Run from the release root:

```
uv run --python 3.12 --with-requirements requirements.txt python -I code/reproduce.py --out NEW_EMPTY_DIR --pdf
```

- The scripts need Python 3.12 (pinned in `.python-version`) and the package versions in `requirements.txt`.
- `reproduce.py` refuses to write into `checks/` or `figures/`, and refuses any directory that is not empty.
- The Monte Carlo step takes several minutes on one CPU and needs about 2 GB of RAM (3 GB was reserved for the reference run).
- The JSON output of the deterministic checks matches `checks/` to floating-point precision.
- The Monte Carlo uses fixed seeds.

## Related releases

Evidence Press, *Restart from a quasi-stationary law: the exact constant and the real budget scale*: https://evidencepress.org/releases/levy-qsd-exponential-moments-restart/

That release restarts a **simulation** from a quasi-stationary distribution. This paper resets the **process itself** at Poisson times. The two papers share the Esscher and Wiener–Hopf toolkit, but neither result implies the other.

## Novelty check

On 27 October 2026 we checked for works citing Dębicki–Hashorva–Michna (DOI 10.1007/s11009-026-10316-4, arXiv:2603.03050) in Crossref, OpenCitations, Semantic Scholar and arXiv. None was found, and no work was found that identifies the constant. This search is narrow and does not establish novelty beyond "we are not aware of"; see the manuscript's Novelty check.

## Licences

Text, manuscript, figures and data: CC0-1.0 ([LICENSE](LICENSE)). Code: MIT ([LICENSE-CODE](LICENSE-CODE)). See [LICENSES.md](LICENSES.md).

## AI provenance

The manuscript, code and this revision were produced with substantial AI assistance under human direction. See the Declarations section of the manuscript.
