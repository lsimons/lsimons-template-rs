# Agent Instructions for lsimons-template-rs

> This file (`AGENTS.md`) is the canonical agent configuration. `CLAUDE.md` is a symlink to this file.

> **If this repo still says "template" everywhere:** run
> `mise run init` once to rename the placeholder crate to your
> project name. See `scripts/init.py` for details.

Brief project description.

## Quick Reference

- **One-time**: `mise install`
- **Build**: `mise run build` (or `cargo build --all-targets`)
- **Run CLI**: `cargo run -- <args>`
- **Test**: `mise run test` (or `cargo test --all-targets`)
- **Lint**: `mise run lint` (fmt check + clippy -D warnings)
- **Format**: `mise run format` (or `cargo fmt`)
- **Doc check**: `mise run doc`
- **Full CI gate**: `mise run ci`

## Structure

- `src/lib.rs` — library: put testable core logic here
- `src/main.rs` — binary: thin CLI that uses the library
- `tests/` — integration tests (spawn the binary via `assert_cmd`)

## Guidelines

**Code quality:**
- Edition 2024; tracks latest stable Rust (`rust = "latest"` in
  `.mise.toml`), no MSRV pin
- `cargo clippy -- -D warnings` must be clean (warn on `all` + `pedantic`)
- Code must be `cargo fmt`-clean
- No `unsafe` by default (`unsafe_code = "forbid"` in `Cargo.toml`)
- Library and CLI share no implicit state; business logic belongs in `lib.rs`
- Tests for all public functions; integration tests cover CLI behavior

## Commit Message Convention

Follow [Conventional Commits](https://conventionalcommits.org/):

**Format:** `type(scope): description`

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `build`, `ci`, `perf`, `revert`, `improvement`, `chore`

## Session Completion

Work is NOT complete until `git push` succeeds.

1. **Quality gates** (if code changed):
   ```bash
   mise run ci
   ```

2. **Push**:
   ```bash
   git pull --rebase && git push
   git status  # must show "up to date with origin"
   ```

Never stop before pushing. If push fails, resolve and retry.
