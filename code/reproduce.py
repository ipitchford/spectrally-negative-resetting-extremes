"""Replay every resetting check into a NEW output directory.

Usage (from the release root):
    uv run --python 3.12 --with-requirements requirements.txt python -I code/reproduce.py --out OUTDIR [--pdf] [--chunks 40]

The shipped evidence in checks/ and figures/ is never written.  OUTDIR must not
exist yet (or be empty) and must lie outside checks/ and figures/.  With --pdf the
manuscript is compiled inside OUTDIR/latex from a copy of the sources.
Compare OUTDIR/*.json with checks/*.json to confirm the replay.
"""
from pathlib import Path
import argparse
import json
import platform
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PROTECTED = [ROOT / "checks", ROOT / "figures"]


def run(script, out, *extra):
    cmd = [sys.executable, "-I", str(ROOT / "code" / script), "--out", str(out), *extra]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.stderr.write(r.stdout[-4000:] + r.stderr)
        raise SystemExit(r.returncode)
    print(f"PASS {script}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--pdf", action="store_true")
    ap.add_argument("--chunks", default="40")
    args = ap.parse_args()
    out = args.out.resolve()
    for p in PROTECTED:
        if out == p or p in out.parents:
            raise SystemExit(f"refusing to write inside shipped evidence directory {p}")
    if out.exists() and any(out.iterdir()):
        raise SystemExit(f"{out} is not empty; choose a new directory")
    out.mkdir(parents=True, exist_ok=True)
    import numpy, scipy, matplotlib  # noqa: E401
    (out / "runtime_versions.json").write_text(json.dumps(
        {"python": platform.python_version(), "numpy": numpy.__version__, "scipy": scipy.__version__,
         "matplotlib": matplotlib.__version__}, indent=2) + "\n")
    run("independent_checks.py", out)
    run("profile_checks.py", out)
    run("exact_mc.py", out, "--chunks", args.chunks)
    run("bv_replicate.py", out)
    if args.pdf:
        tex = out / "latex"
        tex.mkdir()
        for name in ("levy_reset_extremes.tex", "levy_reset_extremes_header.tex"):
            shutil.copy2(ROOT / name, tex / name)
        shutil.copytree(ROOT / "figures", tex / "figures")
        for _ in range(3):
            r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                                "levy_reset_extremes.tex"], cwd=tex, capture_output=True, text=True)
            if r.returncode:
                sys.stderr.write(r.stdout[-6000:])
                raise SystemExit(r.returncode)
        log = (tex / "levy_reset_extremes.log").read_text(errors="replace")
        issues = [ln for ln in log.splitlines() if "Overfull" in ln or "undefined" in ln]
        print("REVIEW latex: " + " | ".join(issues) if issues else "PASS latex; no overfull boxes or undefined references")
    print(f"Complete; outputs in {out}. These checks support, and do not replace, the proofs.")


if __name__ == "__main__":
    main()
