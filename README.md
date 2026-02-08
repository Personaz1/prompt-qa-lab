# prompt-qa-lab

[![CI](https://img.shields.io/github/actions/workflow/status/Personaz1/prompt-qa-lab/tests.yml?branch=master)](https://github.com/Personaz1/prompt-qa-lab/actions)
[![Release](https://img.shields.io/github/v/release/Personaz1/prompt-qa-lab)](https://github.com/Personaz1/prompt-qa-lab/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

## Summary

Prompt QA Lab is a production-oriented scaffold for prompt/agent regression testing.

## Features

- Installable CLI: `pqalab`
- Run and diff workflows (`run`, `diff`)
- Automated tests + CI
- End-to-end demo artifacts

## Install

```bash
pip install -e .
```

## Test

```bash
pytest -q
```

## Demo

```bash
bash demo/run_demo.sh
```

## AI Evaluation Signals

- Deterministic outputs for benchmark-style checks
- CI-enforced regression gate support
- Release and changelog discipline

## Project status

See [PROJECT_STATUS.md](./PROJECT_STATUS.md).

## Roadmap

See [ROADMAP.md](./ROADMAP.md).

## Contributing

See [docs/CONTRIBUTING.md](./docs/CONTRIBUTING.md).

## License

MIT
