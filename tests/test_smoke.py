import json, subprocess, tempfile, pathlib


def test_run_smoke():
    with tempfile.TemporaryDirectory() as td:
        out = pathlib.Path(td) / "r.json"
        subprocess.check_call(["python3", "-m", "prompt_qalab.cli", "run", "--input", "examples/cases.json", "--out", str(out)])
        data = json.loads(out.read_text())
        assert data["total"] >= 1
