"""Test-guided repair of a bundled, synthetic Python demonstration project."""

import difflib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from .mutations import generate_mutations

ROOT = Path(__file__).resolve().parent.parent
DEMO = ROOT / "sample_project"
TARGET = "calculator.py"


def _run_tests(project_dir: Path) -> dict:
    """Execute only this repository's trusted sample tests in a temporary copy."""
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
            cwd=project_dir,
            text=True,
            capture_output=True,
            timeout=15,
            check=False,
        )
        return {
            "passed": proc.returncode == 0,
            "return_code": proc.returncode,
            "log": (proc.stdout + proc.stderr)[-4000:],
        }
    except subprocess.TimeoutExpired:
        return {"passed": False, "return_code": None, "log": "Tests timed out."}


def repair_demo(output_dir: Path | None = None) -> dict:
    """Find a validated one-operator patch. Never modify the original demo."""
    output_dir = Path(output_dir) if output_dir else ROOT / "artifacts"
    output_dir.mkdir(parents=True, exist_ok=True)
    original_text = (DEMO / TARGET).read_text(encoding="utf-8")
    mutations = generate_mutations(original_text)

    with tempfile.TemporaryDirectory(prefix="repair-demo-") as tmp:
        working_dir = Path(tmp) / "sample_project"
        shutil.copytree(DEMO, working_dir)
        baseline = _run_tests(working_dir)
        report = {
            "project": "Bundled synthetic calculator demo",
            "baseline_passed": baseline["passed"],
            "baseline_log": baseline["log"],
            "repair_found": False,
            "candidates_considered": 0,
            "limitation": "Deterministic operator mutations; not an LLM or Docker sandbox.",
        }

        if baseline["passed"]:
            report["message"] = "No repair needed; baseline tests already pass."
        else:
            target_file = working_dir / TARGET
            for mutation in mutations:
                target_file.write_text(mutation.code, encoding="utf-8")
                result = _run_tests(working_dir)
                report["candidates_considered"] += 1
                if result["passed"]:
                    report["repair_found"] = True
                    report["validated_change"] = {
                        "line": mutation.line,
                        "from": mutation.original,
                        "to": mutation.replacement,
                    }
                    report["validation_log"] = result["log"]
                    (output_dir / "proposed_fix.py").write_text(
                        mutation.code, encoding="utf-8"
                    )
                    patch = "".join(difflib.unified_diff(
                        original_text.splitlines(keepends=True),
                        mutation.code.splitlines(keepends=True),
                        fromfile=f"a/{TARGET}",
                        tofile=f"b/{TARGET}",
                    ))
                    (output_dir / "proposed_fix.patch").write_text(
                        patch, encoding="utf-8"
                    )
                    break
            if not report["repair_found"]:
                report["message"] = "No single-operator change passed the tests."

    (output_dir / "report.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    return report
