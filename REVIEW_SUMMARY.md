# Revision response: "Fixed-horizon extremes of spectrally negative Lévy processes with Poisson resetting"

Single revision round, 27 October 2026. Every finding from the five reviews and the proof audit is merged below.

- **Format.** Each item gives R (the review point), A (the action we took) and C (where the change is, in the revised manuscript `levy_reset_extremes.tex` and PDF).
- **Reviewer IDs.**
  - EIC = editor-in-chief
  - METH = methodology
  - DOM = domain
  - PERSP = perspective
  - DA = devil's advocate
  - SOL = a separate AI proof audit (its report is not shipped; its findings are summarised here)
- **Status.** This is a public summary of internal AI-assisted review. It is not external peer review.
- **Numbering.** Labels refer to the revised numbering. Old equation numbers are given in brackets.

## A. Scope, novelty and framing

**1. Restrict the claim to spectrally negative inputs** (DA M1; PERSP S1).
- R: The title and opening say "Lévy processes", but only spectrally negative inputs are covered.
- A: The title, running head and abstract now say "spectrally negative". A new paragraph, "Why no upward jumps", explains how upward jumps break the two facts the proof uses:
  - With light upward jumps, the stationary tail is not exactly exponential and there is no density continuation.
  - With heavy upward jumps there is no β, and a single big jump can occur in any cycle.
- C: Title; abstract; §1 "Why no upward jumps"; §9 item 1.

**2. Credit the renewal method; state the new content** (DOM M2; DA M3; PERSP S1; SOL II.1–II.2).
- R: The leading term is a standard first-cycle computation, so the new content should be isolated.
- A: §1 now says plainly that the constant comes from the standard renewal/first-cycle computation that DHM use for their Theorem 5. The listed contributions are:
  - the uniform total-variation error bound;
  - the conditional path law and its quantitative corollaries;
  - bounded-variation exactness;
  - random reset positions.

  Remark 3.5 explains what a direct renewal argument gives and what it does not. Table 1 compares this work with Singh–Pal, Mori et al. and DHM by initialisation, horizon, observable, mode of statement and path law.
- C: §1 "What is standard and what is new"; Table 1; Remark 3.5.

**3. Drop the "resolution of the conjecture" overselling** (DA M3; EIC minor 6).
- A: "Resolution" no longer appears anywhere. The paper now says it supplies the constant and proves that DHM's bounds are strict. In the final editorial round the subtitle was changed from "…the constant in a Brownian conjecture" to "…the constant in Remark 3 of Dębicki, Hashorva and Michna" (the first revision had not yet changed it), and Corollary 6.1 is titled "The constant in Remark 3 of [DHM]".
- C: Subtitle; abstract; §1; Corollary 6.1.

**4. Dependence on λ and T; when the asymptotic regime begins** (DA M4; METH minor 6; PERSP §4).
- A: New §6.1:
  - Brownian scaling reduces everything to λT and βb.
  - Bound (6.5) is informative only for βb > 2λT.
  - The no-reset share A/D falls like 1/(λT).
  - Table 4 gives the βb at which the relative bound reaches 1%, for λT from 0.0625 to 16, using both (6.5) and the sharper Remark 3.4.

  §8 notes that the actual relative error is about 0.02% at u = 3 when λT = 1.
- C: §6.1, Table 4; `checks/independent_checks.json` → `onset_of_asymptotic_regime`.

**5. Notation clash with α; the DHM dictionary** (DA m1; PERSP R10; EIC minor 2; SOL II.3).
- A: All conventions are gathered in one paragraph in §1:
  - unit variance, W_t − ct, rate λ to x_R;
  - stationary start, supremum over [0, T], strict event inequalities (H_T > u, Y_T > 0); DHM's bounds on C_T are non-strict, and their strictness is this paper's result;
  - α = β at σ = 1 ("the same number, not a correction"), x_R = r, c = −μ.

  The reason for avoiding α is also stated there.
- C: §1 "The source question".

**6. Uniqueness of the invariant law** (DOM minor 1).
- A: Added a one-line coupling argument: two copies driven by the same clock coincide after the first reset.
- C: §2.

**7. Stable inputs** (DA M1, observations).
- A: New Remark 2.1 covers:
  - β = λ^{1/α} and a = 1/α;
  - α = 2 is Brownian motion with σ² = 2;
  - α < 1 with drift falls under Corollary 7.2.
- C: Remark 2.1; Corollary 7.2.

## B. Proofs

**8. State (29)–(31) as propositions with full proofs and error bounds, including the fixed terminal threshold** (EIC M2; METH minor 1; DOM minor 4; DA M2; SOL I.3).
- A: These are now Proposition 5.2 and Proposition 5.3.
  - **Proposition 5.2** covers the overshoot, the first-reset mark and the tilted pre-reset increments, conditioned on {H_T>u, Y_T>y} for every y ∈ [−∞, ∞). It gives an explicit total-variation bound (5.5) against Exp(β) ⊗ Γ_y with three terms:
    - e^{βb}R_γ;
    - Q_T((−∞, y−u]), the term EIC asked for;
    - 2(D_T−A(T))(1+λT)e^{Tψ(γ)−γb}, for post-reset exceedances.

    Independence is stated as joint convergence, as SOL asked. The case y = −∞ is old (29), and fixed y is old (31).
  - **Proposition 5.3** is the J1 path limit (old (30)), with a full proof.
- C: §5.2.

**9. Make the "richer marked space" claim well posed** (DA M2; SOL I.1, I.3).
- A: The proof of Theorem 3.1 now builds the probability space explicitly from independent ingredients (x, Θ). It defines the measures μ_u, V_u, C_u and L_u, and proves the identity μ_u − V_u = L_u − C_u (3.4).
  Theorem 5.1 defines the space E = D[0,T] × ((0,T] ∪ {†}) with its σ-field, and states the bound on the (x, Θ) space explicitly. That statement replaces the vague "richer space" sentence.
- C: §3.2 "The probability space", "Three measures"; Theorem 5.1.

**10. Expand step (14)** (METH minor 2; DOM minor 3).
- A: The new proof of (3.5) gives one argument, not two. It names the independence of each post-reset driver ξ^(k) from the clock (the strong Markov property at reset epochs), explains why the cycle length is at most T, and sums to E N_T · P(M_T > b).
- C: (3.5).

**11. Expand step (17)** (METH minor 3).
- A: The new proof of (3.6) says explicitly that C_u lives on x < 0. It also says that E_u uses the clock through τ∧T, and that the clock weight is at most one and is dropped via the inclusion in {x + M_T > b}.
- C: (3.6).

**12. Doob step** (SOL I.1).
- A: New Lemma 3.3 applies Doob's inequality to the nonnegative submartingale e^{γξ}, and also covers z ≤ 0.
- C: Lemma 3.3.

**13. Sharper remainder** (EIC minor 3; SOL I.1).
- A: Remark 3.4 gives R̃_γ, which uses Campbell's formula and E e^{q(τ∧T)}, and notes that aβ = λ/ψ'(β). Table 4 uses it.
- C: Remark 3.4.

**14. Strict versus non-strict indicator in (12)** (SOL I.1).
- A: Lemma 3.2 now uses 1{I<x} and notes that atoms of I form a null set.
- C: Lemma 3.2.

**15. Monotone, not dominated, convergence for E e^{βI}** (METH table, row (11)–(13)).
- A: Changed to monotone convergence, since I ≤ 0.
- C: Lemma 3.2.

**16. Stopped Esscher argument in (39)** (SOL I.5).
- A: Rewritten as Proposition 7.1, with:
  - τ_x = inf{t : ξ_t ≥ x} and ξ_{τ_x} = x;
  - optional stopping at τ_x ∧ T;
  - the integration by parts written out;
  - the null-level caveat stated explicitly.
- C: Proposition 7.1.

**17. Corollary 4 wording** (SOL I.6; PERSP S3).
- A: The corollary now states the exact identity rather than saying "(9) is an equality". It also notes that S is driftless and d > 0, and that infinite-activity S still has bounded variation.
- C: Corollary 7.2.

**18. "Error O(R_γ)" in (10) is really an exact bound** (DOM minor 2).
- A: Now stated as |P(H_T>u) − D_T e^{−βb}| ≤ R_γ.
- C: Theorem 3.1.

**19. Weak convergence on the compactified line** (SOL I.2).
- A: Stated explicitly.
- C: §4, after (4.4).

**20. Finiteness of ψ makes the error superexponential** (DA m5).
- A: Stated after Theorem 3.1, together with why the claim fails when positive jumps are allowed.
- C: §3.

**21. The event E_u needs a displayed definition** (DA m2).
- A: Now displayed, with the a.s. equality of sup_{v<s} and M_s.
- C: §3.2.

**22. Table row reasons** (DA m3; PERSP R8).
- A: Table 3 now has an "In words" column, and its caption gives the two extra limits K_T((u+w,∞)) → 0 and Q_T((y_u−u,∞)) → A(T).
- C: Table 3.

**23. Normalisation inequality** (METH table).
- A: Displayed as (4.3), with a one-line proof.
- C: (4.3).

**24. Strictness of the DHM bounds** (DOM §1).
- A: Corollary 6.1 proves strictness from 0 < p_t(0) < 1.
- C: Corollary 6.1.

## C. Extension

**25. Raise significance with one fully proved extension** (EIC; DOM; PERSP; DA; METH, all under extensions).
- A: **Random reset positions** (Theorem 7.3), with a complete proof. Reset positions are i.i.d. with law ρ, where E e^{γR} < ∞ for some γ > β. Results:
  - leading term m(β)e^{−βu}{Q_T(·−u) + K^ρ_T};
  - explicit error m(γ)(aβ/(γ−β) + λT)e^{Tψ(γ)−γu};
  - the conditional law of the initial reset position is tilted by e^{βz};
  - the no-reset odds and the Exp(β) overshoot do not depend on ρ;
  - exactness for bounded variation when ρ has bounded support above.

  Exact Monte Carlo with ρ = U[−1,1] agrees: 1.8192(36) against 1.81789, and 2.3772(41) against 2.37510.

  Renewal clocks, the time of the maximum, joint (u, T) limits, upward jumps, moving reset positions and heavy left tails are listed as open problems.
- C: §7.3, Table 6, §9.

## D. Simulation and reproducibility

**26. Add an exact-sampling Monte Carlo of the original process** (METH M1; EIC minor 5; DA m4; PERSP ext. 6).
- A: New script `code/exact_mc.py --out DIR`. It adapts the methodology referee's sampler (credited in §8): exact Brownian-bridge maxima, no discretisation bias, and event-by-event bounded-variation paths. It needs about 2 GB of RAM; the run reserved 3 GB (`research-run --cpu 1 --memory-gb 3`), with 4×10⁷ Brownian paths per experiment and 2×10⁷ bounded-variation paths. It checks:
  - the scaled joint probability and the tail of H;
  - the no-reset fraction;
  - the first-reset CDF;
  - the mean excess and the KS distance to Exp(β);
  - bounded-variation exactness, with D_T from Proposition 7.1;
  - random reset positions.

  Table 6 and Figure 1(b), which overlays the histogram at u = 3, report the results. One bounded-variation value at u = 2.5 came out 2.4 standard errors low. An independent replicate, `code/bv_replicate.py` (seed 99, 6×10⁷ paths), agrees with D_T to within one standard error, and both runs are reported.
- C: §8, Table 6, Figure 1; `checks/exact_mc.json`, `checks/bv_replicate.json`.

**27. reproduce.py overwrites the shipped evidence** (METH minor 4).
- A: All scripts now require `--out DIR` and refuse to overwrite existing files. `reproduce.py` refuses an output directory that is not empty or that lies inside `checks/` or `figures/`. LaTeX is compiled from a copy inside the output directory.
- C: `code/reproduce.py`, `code/*.py`.

**28. Pin the Python version** (METH minor 4).
- A: Added `.python-version` (3.12), a header in `requirements.txt` and a README note. `runtime_versions.json` records the exact interpreter used.
- C: `.python-version`, `requirements.txt`, `README.md`.

**29. Tabulate u = 2 and 3** (METH minor 5).
- A: Table 5 now covers u = 2–6 and adds the finite-u leading term.
- C: Table 5.

**30. Rename "Independent numerical checks"** (PERSP R11).
- A: Renamed "Numerical checks".
- C: §8.

**31. The figure caption should state the plot convention** (EIC minor 7; DOM minor 6).
- A: The caption gives the bin width, says the humps are u apart for every u because the no-reset profile is a translate, and labels the "no reset" and "reset" components.
- C: Figure 1.

**32. Standalone packaging** (EIC M3).
- A: The resetting material was copied on its own into `revised/`, with no Kuramoto or phase-retrieval content. `independent_checks.py` was rewritten to cover resetting only, and the release has its own README.
- C: Release layout.

## E. Literature and novelty check

**33. Add the core resetting and applied literature** (DOM MAJOR-1; EIC minor 1; PERSP §3).
- A: Added the following references. Every field was taken from Crossref on 27 Oct 2026.
  - Evans–Majumdar 2011
  - Evans–Majumdar–Schehr 2020
  - Kusmierz–Majumdar–Sabhapandit–Schehr 2014
  - Majumdar–Pal–Schehr 2020
  - Majumdar–Mounaix–Sabhapandit–Schehr 2022
  - Pal–Kundu–Evans 2016
  - Pal–Kuśmierz–Reuveni 2020
  - Di Crescenzo–Giorno–Nobile–Ricciardi 2003 (a queue with catastrophes)
  - Avrachenkov–Piunovskiy–Zhang 2013
  - Luby–Sinclair–Zuckerman 1993
  - Goldman–Sosin–Gatto 1979
  - Asmussen–Albrecher 2010
  - Kyprianou 2014

  We did not add the following:
  - Partial resetting (arXiv:2412.15626, suggested by DOM) and Avram–Kyprianou–Pistorius (suggested by PERSP) were not verified in this round.
  - No Crossref search found a genuine Lévy or risk model with catastrophes, so we cite only the verified catastrophe-queue paper.
- C: §1, references.

**34. Re-run the forward-citation check** (EIC M1; PERSP S1; SOL II.3).
- A: Checked on **27 October 2026** using Crossref cited-by (0), OpenCitations COCI (empty), Semantic Scholar (none) and an arXiv search. **Result:** no work cites DHM or identifies C_T. arXiv v3 (27 Sep 2026) is the latest version. The result is recorded in the paper.
- C: "Novelty check" section.

**35. Spelling of Żbik** (DOM minor 7).
- A: The arXiv record spells the name "Zbik", without the Polish letter. We follow the record, as the brief requires ("exact authors from the record").
- C: References.

**36. Page numbers for Kuznetsov et al.** (DOM minor 8).
- A: Pages 97–186 are kept. We did not open the chapter to confirm the section and theorem numbers, so those pointers are unchanged.
- C: References.

**37. Cross-link to the QSD release** (EIC cross-check; DOM §5).
- A: Added a "Related releases" section linking https://evidencepress.org/releases/levy-qsd-exponential-moments-restart/, under that page's title, "Restart from a quasi-stationary law: the exact constant and the real budget scale". It states that that release restarts a simulation from a QSD, while this paper resets the process.
- C: "Related releases" section; README.

## F. Readability

**38. External motivation** (PERSP R1, §3).
- A: §1 opens with search, foraging, catastrophes, restarts, ruin theory and lookback options. It notes that we do not claim resetting is a good price model.
- C: §1.

**39. A plain one-line result, an informal display and a roadmap** (PERSP R2, R3, §4, S2).
- A: §1 now contains:
  - "The result in one sentence": the 53:47 odds and the memoryless overshoot with mean 1/β;
  - the informal display (1.1);
  - a roadmap paragraph.

  The abstract was rewritten for non-specialists.
- C: Abstract; §1.

**40. Glosses for β, a, A, D, Q and K** (PERSP R4).
- A: Table 2 is a glossary with a plain-words meaning for each symbol.
- C: Table 2.

**41. Picture of the two kinds of path** (PERSP R5).
- A: Figure 1(a) shows two simulated paths with a high maximum, one with no reset and one reset after its peak.
- C: Figure 1.

**42. Theorem environments and numbering** (PERSP R6; SOL III).
- A: Rebuilt as a clean LaTeX document, with `\documentclass` first and amsthm environments. Numbering is automatic, and there are no empty headings.
- C: Whole source.

**43. A strategy sentence in the proof** (PERSP R7).
- A: Added before the proof of Theorem 3.1.
- C: §3.2.

**44. Variation-norm convention** (PERSP R9).
- A: The paper now says that readers who prefer the sup convention can halve every bound.
- C: §2.

**45. Choppy, machine-like rhythm** (PERSP R12).
- A: The prose was rewritten with explicit connectives ("because", "so", "which means") and longer linked sentences, especially in §§1, 2 and 4.
- C: Throughout.

**46. Mixture of normalisations, the ruin reading, rare-event simulation** (PERSP §3.6, DA stakeholders, METH and EIC extensions).
- A: Added:
  - one sentence linking (4.5) to conditional extremes;
  - the surplus-process reading after Corollary 7.2;
  - Remark 5.4 on rare-event simulation.
- C: §4, §7.2, §5.

**47. Rename c in the deterministic check** (DOM minor 5).
- A: Renamed to d.
- C: §7.2.

## G. Hygiene

**48. Declarations, AI provenance, Anonymous author.**
- A: Added a Declarations section.
- C: End of the paper.

**49. Private editorial material is not shipped.**
- A: Only this summary is public; the review reports themselves are not shipped. Checked by scan over the release.
- C: All files.

## Points not adopted (with reasons)

1. **DA m6: quantify the left tail of Q_T for stable inputs.** Not proved in this round. It is listed under open problems rather than asserted.
2. **DA "ignored alternative": a scale-function route.** Out of scope for one round. It is not needed for any result.
3. **Positive jumps, renewal clocks, the time of the maximum, joint (u, T) limits, moving r_u** (various reviewers). These are not proved, so they are listed as open problems (§9), following the brief.
4. **SOL II.2: a full Palm and tail-process literature survey.** Not attempted. The novelty claim is narrowed instead to the explicit statements in Table 1 and the list in §1.
5. **Unverified references (partial resetting; Avram–Kyprianou–Pistorius; a risk model with catastrophes).** Omitted because they were not verified against Crossref or arXiv in this round.

## Final editorial round (27 October 2026)

A re-review and two further AI proof audits of the revised manuscript found no fatal defect in the endpoint theorem, its remainder, the Brownian constant, Proposition 7.1 or the bounded-variation exactness. They raised the following points, all now addressed.

1. **Theorem 7.3, transfer of the path and mark results.** The revision said Theorem 5.1 and Proposition 5.2 hold "with D_T replaced by m(β)D_T". That replacement would make the first-reset sampler a sub-probability law of mass 1/m(β) (about 0.73 for ρ = Uniform[−1, 1]). Theorem 7.3 now states the random-reset sampler explicitly (R₀ from the tilted law e^{βz}ρ(dz)/m(β); the mark law unchanged, with denominator D_T; post-reset restart from ρ), its total-variation bound 2e^{βu}R^ρ/(m(β)D_T), and the full random-reset analogue of Proposition 5.2 with p^ρ, L^ρ_T and a post-reset term carrying m(γ)/m(β). The endpoint bound and the constants were already correct and are unchanged.
2. **Proposition 5.2(i), mean overshoot.** Uniform integrability was asserted by reference to numerics. It is now proved for every input from Theorem 3.1: P(H_T − u > v | H_T > u) ≤ 3e^{−βv} for large u. The "whenever … uniformly integrable" caveat is removed.
3. **Proposition 5.2, state space.** The pre-reset path is now a killed path in D([0, T], ℝ ∪ {Δ}), so the total-variation distance is defined on one standard Borel space.
4. **Theorem 5.1, later reset epochs.** The absolute later epochs are not independent of S. The statement now says that, given S, the reset epochs after S form a Poisson process on (S, ∞), with residual times and later drivers independent of (E, ζ, S).
5. **Lemma 3.2.** The Wiener–Hopf factors are now described as independent variables with the laws of the supremum and infimum (not the coupled supremum and infimum of one path), and the limit θ ↑ β uses dominated, not monotone, convergence.
6. **Novelty wording.** Table 1 no longer says "only this paper"; Proposition 7.1 is described as a standard fluctuation-theoretic consequence and Corollary 7.2 as a sharp special case; the novelty check now states what the forward-citation search does not exclude.
7. **Text.** The subtitle is changed (item 3 above); "strict inequalities" now reads "strict event inequalities", making clear that strictness of the bounds is this paper's result; Pal–Kundu–Evans (2016) is now cited in §1; the Related releases title matches the live page; Table 1 columns are widened so that no word breaks; README and this response give the same memory figure.
