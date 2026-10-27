"""Independent replicate (seed 99, 6e7 paths) of the bounded-variation exactness test.

Usage: python -I code/bv_replicate.py --out DIR   (writes DIR/bv_replicate.json)
"""
from pathlib import Path
import argparse, json, math, sys
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
import exact_mc as E  # noqa: E402

ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True, type=Path); args = ap.parse_args()
args.out.mkdir(parents=True, exist_ok=True)
t = args.out / "bv_replicate.json"
if t.exists():
    raise SystemExit(f"refusing to overwrite {t}")
rng = np.random.default_rng(99); beta = (1 + 5 ** .5) / 2; c = {1.0: 0, 2.5: 0}; M = 0
for _ in range(60):
    H = E.bv(rng, E.CHUNK); M += H.size
    for u in c:
        c[u] += int((H > u).sum())
out = {str(u): {"scaled_H_gt_u": k / M * math.exp(beta * u), "se": math.sqrt(k / M / M) * math.exp(beta * u)}
       for u, k in c.items()}
out.update(seed=99, paths=M)
t.write_text(json.dumps(out, indent=1) + "\n"); print(json.dumps(out))
