# Agent Instructions for lsimons-$project

> This file (`AGENTS.md`) is the canonical agent configuration. `CLAUDE.md` is a symlink to this file.

Brief project description.

## Quick Reference

- **Build**: `cargo build --all-targets`
- **Run CLI**: `cargo run -- <args>`
- **Test**: `cargo test --all-targets`
- **Lint**: `cargo clippy --all-targets --all-features -- -D warnings`
- **Format**: `cargo fmt`
- **Format check**: `cargo fmt --check`
- **Doc check**: `cargo doc --no-deps --all-features`

## Structure

- `src/lib.rs` — library: put testable core logic here
- `src/main.rs` — binary: thin CLI that uses the library
- `tests/` — integration tests (spawn the binary via `assert_cmd`)

## Guidelines

**Code quality:**
- Edition 2024; MSRV tracked via `rust-version` in `Cargo.toml`
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
   cargo fmt --check
   cargo clippy --all-targets --all-features -- -D warnings
   cargo test --all-targets
   ```

2. **Push**:
   ```bash
   git pull --rebase && git push
   git status  # must show "up to date with origin"
   ```

Never stop before pushing. If push fails, resolve and retry.
