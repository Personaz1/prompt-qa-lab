#!/usr/bin/env python3
import argparse, json, pathlib, datetime, sys


def load_cases(path):
    p = pathlib.Path(path)
    data = json.loads(p.read_text(encoding="utf-8"))
    return data.get("cases", [])


def eval_case(case):
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


def diff(old_file, new_file, fail_on_regression=False):
    old = json.loads(pathlib.Path(old_file).read_text(encoding="utf-8"))
    new = json.loads(pathlib.Path(new_file).read_text(encoding="utf-8"))

    old_map = {r["id"]: r for r in old.get("results", [])}
    new_map = {r["id"]: r for r in new.get("results", [])}

    regressions = []
    improvements = []
    unchanged = []

    for cid, n in new_map.items():
        o = old_map.get(cid)
        if not o:
            continue
        if o["passed"] and not n["passed"]:
            regressions.append(cid)
        elif (not o["passed"]) and n["passed"]:
            improvements.append(cid)
        else:
            unchanged.append(cid)

    print("Diff summary")
    print(f"- regressions: {len(regressions)}")
    print(f"- improvements: {len(improvements)}")
    print(f"- unchanged: {len(unchanged)}")

    if regressions:
        print("Regressed cases:")
        for cid in regressions:
            print("-", cid)

    if fail_on_regression and regressions:
        sys.exit(2)


def main():
    ap = argparse.ArgumentParser(prog="pqalab")
    sub = ap.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run", help="Run offline prompt QA checks")
    r.add_argument("--input", default="examples/cases.json")
    r.add_argument("--out", default="report.json")

    d = sub.add_parser("diff", help="Compare two reports")
    d.add_argument("--old", required=True)
    d.add_argument("--new", required=True)
    d.add_argument("--fail-on-regression", action="store_true")

    args = ap.parse_args()
    if args.cmd == "run":
        run(args.input, args.out)
    elif args.cmd == "diff":
        diff(args.old, args.new, args.fail_on_regression)


if __name__ == "__main__":
    main()
