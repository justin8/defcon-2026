# Pre-Task Setup Requirements

Before performing any development task, code modification, building, or testing in this repository, you MUST follow the steps in AGENTS.md and DEVELOPMENT.md exactly as written.

## Mandatory Pre-Task Checklist

Work through every item in order before touching any code, running any build, or executing any test:

1. **Read AGENTS.md** in full — it is the authoritative source of pre-task requirements.
2. **Read DEVELOPMENT.md** in full — it defines the toolchain, setup, and verification procedures.
3. **Verify Homebrew**: Run `brew --version`. Must succeed before proceeding.
4. **Verify devtools**: Run `devtools`. If not found or fails, run the full install sequence from DEVELOPMENT.md. Do not skip this — missing devtools causes silent build and test failures.
5. **Verify Go**: Run `go version`. The binary must come from `/opt/homebrew/bin/go` (Apple Silicon) or `/usr/local/bin/go` (Intel). Install or upgrade via Homebrew if missing or outdated.

## Rules

- Do not assume any step is already complete. Verify each one explicitly.
- Do not skip devtools verification. It is required for builds and tests to work.
- Do not use system Go, a Go version manager, or a manually downloaded binary.
- Follow `make` targets as documented in DEVELOPMENT.md for building, testing, linting, and running.
