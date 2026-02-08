#!/usr/bin/env python3
import argparse, json, pathlib, datetime


def load_cases(path):
    p = pathlib.Path(path)
    data = json.loads(p.read_text(encoding="utf-8"))
    return data.get("cases", [])


def eval_case(case):
    # offline deterministic evaluator for scaffold stage
    output = case.get("mock_output", "")
    checks = case.get("checks", {})
    passed = True
    reasons = []

    for token in checks.get("must_contain", []):
        if token not in output:
            passed = False
            reasons.append(f"missing token: {token}")

    for token in checks.get("must_not_contain", []):
        if token in output:
            passed = False
            reasons.append(f"forbidden token present: {token}")

    return {
        "id": case.get("id", "unknown"),
        "passed": passed,
        "reasons": reasons,
        "output": output,
    }


def run(input_file, out_file):
    cases = load_cases(input_file)
    results = [eval_case(c) for c in cases]
    passed = sum(1 for r in results if r["passed"])
    total = len(results)

    report = {
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "results": results,
    }
    pathlib.Path(out_file).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved report: {out_file}")
    print(f"Pass rate: {passed}/{total}")


def main():
    ap = argparse.ArgumentParser(prog="pqalab")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="Run offline prompt QA checks")
    r.add_argument("--input", default="examples/cases.json")
    r.add_argument("--out", default="report.json")
    args = ap.parse_args()

    if args.cmd == "run":
        run(args.input, args.out)


if __name__ == "__main__":
    main()
