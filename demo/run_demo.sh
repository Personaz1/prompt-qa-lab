#!/usr/bin/env bash
set -euo pipefail

python3 -m prompt_qalab.cli run --input examples/cases.json --out demo/report-baseline.json

cat > /tmp/pqalab_regress.json <<'JSON'
{
  "cases": [
    {
      "id": "format-check-1",
      "prompt": "Return a concise launch checklist",
      "mock_output": "Checklist: scope only",
      "checks": {
        "must_contain": ["Checklist", "owner"],
        "must_not_contain": ["<script>"]
      }
    }
  ]
}
JSON

python3 -m prompt_qalab.cli run --input /tmp/pqalab_regress.json --out demo/report-regressed.json
python3 -m prompt_qalab.cli diff --old demo/report-baseline.json --new demo/report-regressed.json > demo/diff.txt || true

echo "Demo artifacts generated in demo/"
