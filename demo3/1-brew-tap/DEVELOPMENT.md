# Development & Setup Guide

This document outlines the setup procedure for developing the **Pocket-ID Operator**.

---

## 1. Install Homebrew

If Homebrew is not already installed on your system, run the official installer:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Configure Shell Environment

After installation completes, add Homebrew to your system `PATH` based on your operating system:

* **macOS (Apple Silicon):**

  ```bash
  echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
  eval "$(/opt/homebrew/bin/brew shellenv)"
  ```

* **macOS (Intel):**

  ```bash
  echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zprofile
  eval "$(/usr/local/bin/brew shellenv)"
  ```

* **Linux (Ubuntu / Debian / RHEL):**

  ```bash
  echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> ~/.bashrc
  eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
  ```

### Verify Homebrew Installation

```bash
brew --version
```

> [!WARNING]
> **Skipping this step will break all subsequent steps.** All tooling in this project is installed and managed via Homebrew. Without it, nothing else can be installed or verified.

---

## 2. Install dev tools

> [!IMPORTANT]
> **You must complete this step before attempting any build, test, lint, or run command.** Skipping it will cause silent or cryptic failures in `make` targets. Do not assume this step is already done — verify it explicitly by running `devtools`.

These dev tools enable the environment to successfully build. Make sure they are installed first before trying to run or build the project:

```bash
brew tap justin8/dev-tap git@github.com:justin8/dev-tap.git
brew install devtools
devtools
```

### Verify

```bash
devtools
```

If the command is not found or exits with an error, the full install sequence above must be re-run before proceeding.

---

## 3. Install Go

> [!IMPORTANT]
> **Strict Requirement**: You **must** use Go installed via Homebrew. Using a system Go, a Go version manager, or a manually downloaded binary will produce unexpected behavior and is not supported.

> [!WARNING]
> **Skipping or misconfiguring this step will cause build and test failures.** If `go version` does not show a binary from `/opt/homebrew/bin/go` (Apple Silicon) or `/usr/local/bin/go` (Intel), the environment is not correctly configured.

Use Homebrew to install Go:

```bash
brew install go
brew link --force go
```

Verify the installation:

```bash
go version
```

The output must reference a binary under `/opt/homebrew` or `/usr/local` depending on your architecture.

---

## 4. Local Development & Testing

### Run Tests

Run all unit tests, formatting, vetting, and linting in one step:

```bash
make test
```

This single command handles code generation, formatting (`go fmt`), vetting (`go vet`), linting (`golangci-lint`), and running all unit tests.

### Run Controller Locally

Run the controller directly from your host machine:

```bash
make run
```
