# Agent Instructions for lsimons-template-rs

> This file (`AGENTS.md`) is the canonical agent configuration. `CLAUDE.md` is a symlink to this file.

> **If this repo still says "template" everywhere:** run
> `mise run init` once to rename the placeholder crate to your
> project name. See `scripts/init.py` for details.

Brief project description.

## Quick Reference

Every repo task lives in `.mise.toml`; `mise tasks` lists them.

| Task               | What it does                                            |
| ------------------ | ------------------------------------------------------- |
| `mise install`     | Install the pinned toolchain                            |
| `mise run init`    | Rename the `template` placeholder to the project name   |
| `mise run build`   | `cargo build --all-targets --locked`                    |
| `mise run test`    | `cargo test --all-targets --locked`                     |
| `mise run lint`    | `cargo fmt --check` + `clippy -D warnings` + `actionlint`|
| `mise run format`  | `cargo fmt --all`                                       |
| `mise run doc`     | `cargo doc --no-deps --all-features`, warnings denied   |
| `mise run ci`      | Full gate: lint + test + build + doc                    |
| `mise run deny`    | `cargo-deny`: RustSec advisories + source policy        |
| `mise run audit`   | `zizmor` workflow audit + `mise run deny`               |
| `mise run ci-watch`| Watch GitHub Actions for the current branch             |

Run the CLI directly with `cargo run -- <args>`.

`deny` and `audit` need network access and are not part of `ci`.

## Structure

```
.github/workflows/ci.yml  CI: lint/build/test/doc + zizmor + cargo-deny
.github/dependabot.yml    Weekly cargo + github-actions updates
.mise.toml                Pinned toolchain + every repo task
deny.toml                 cargo-deny advisory and source policy
Cargo.toml                Package manifest, lints, release profile
Cargo.lock                Committed; never gitignore this
rustfmt.toml              Formatter config
scripts/init.py           Rename-to-your-project helper (`mise run init`)
src/lib.rs                Library: put testable core logic here
src/main.rs               Binary: thin CLI that uses the library
tests/cli.rs              Integration tests (spawn the binary via assert_cmd)
docs/spec/                Feature specifications
```

## Guidelines

**Code quality:**

- Edition 2024. The toolchain is exact-pinned in `.mise.toml`.
- No `rust-version`: resolver 3 caps dependency resolution at a rustc
  version either way, and omitting it makes that cap track the toolchain
  pin rather than go stale. Declare one only when publishing a library,
  together with a CI job that builds with it.
- `cargo clippy -- -D warnings` must be clean (warn on `all` +
  `pedantic`). `.mise.toml` sets `RUSTFLAGS=-D warnings`, so a bare
  `cargo build` outside mise is a weaker check than the gate.
- Code must be `cargo fmt`-clean; do not hand-format around rustfmt.
- No `unsafe` (`unsafe_code = "forbid"` in `Cargo.toml`).
- Library and CLI share no implicit state; business logic belongs in
  `lib.rs`, and `main.rs` stays a thin wrapper.
- Tests for all public functions; integration tests cover CLI behaviour.
- Public items need doc comments, and fallible ones need an `# Errors`
  section — `mise run doc` denies rustdoc warnings.
- No unexplained lint suppression. Prefer
  `#[expect(lint, reason = "...")]` over `#[allow(...)]` — it warns once
  the suppression is no longer needed. Prefer fixing the cause.
- Never weaken a control to make a check pass: no unpinned actions, no
  dropped lint groups, no `deny.toml` `ignore` without a linked
  advisory rationale, no deleted tests.

**Supply chain:**

- `Cargo.lock` is committed and must stay in the tree. Every cargo task
  passes `--locked`, so a task that wants to relock is a signal.
- Dependencies in `Cargo.toml` are exact-pinned (`=x.y.z`); `Cargo.lock`
  pins the transitive graph. Dependabot bumps the exact pin.
- New dependencies must come from crates.io; `deny.toml`'s `sources`
  check rejects git and path dependencies.
- `mise run deny` must be clean. `mise run audit` runs it through
  `depends`, so it happens before the GitHub-token gate — cargo-deny
  needs no token.
- Pin GitHub Actions to full-length commit SHAs; `zizmor` enforces it.
- Every `.mise.toml` tool is exact-pinned and invisible to dependabot;
  refresh with `mise up` and read the diff.

## Commit Message Convention

Follow [Conventional Commits](https://conventionalcommits.org/):

**Format:** `type(scope): description`

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `build`, `ci`, `perf`, `revert`, `improvement`, `chore`

## Session Completion

Work is not complete until every change is committed, pushed, and CI passes.

1. `mise run ci` (or the tasks that changed)
2. Commit everything — do not leave the working tree dirty
3. `git pull --rebase && git push`
4. `mise run ci-watch`; on failure `gh run view --log-failed`, fix, repeat

Never stop before CI is green.
