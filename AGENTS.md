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

- Edition 2024. The toolchain is pinned exactly in `.mise.toml`, and
  `rust-version` in `Cargo.toml` mirrors it — bump both together.
- `cargo clippy -- -D warnings` must be clean (warn on `all` +
  `pedantic`). `RUSTFLAGS=-D warnings` is set by `.mise.toml` and by the
  CI workflow, so every `warn` level in `Cargo.toml` is in practice a
  `deny` there. A bare `cargo build` in a shell without mise active does
  not get this, so a warning can look harmless locally and still fail CI.
- Code must be `cargo fmt`-clean; do not hand-format around rustfmt.
- No `unsafe` (`unsafe_code = "forbid"` in `Cargo.toml`).
- Library and CLI share no implicit state; business logic belongs in
  `lib.rs`, and `main.rs` stays a thin wrapper.
- Tests for all public functions; integration tests cover CLI behaviour.
- Public items need doc comments, and fallible ones need an `# Errors`
  section — `mise run doc` denies rustdoc warnings.
- Do not silence a lint without a written justification on the same
  line. Prefer `#[expect(lint, reason = "...")]` over `#[allow(...)]`:
  `expect` warns once the suppression stops being necessary, so it
  cleans itself up. Suppress when the cause is outside this repo; fix
  the cause when it is inside.
- Never weaken a control to make a check pass: do not unpin an action,
  drop a lint group from `Cargo.toml`, add an `ignore` to `deny.toml`
  without a linked advisory rationale, or delete a failing test.

**Supply chain:**

- `Cargo.lock` is committed and must stay in the tree. Every cargo task
  in `.mise.toml` (`build`, `test`, `lint`, `doc`) passes `--locked`, so
  a task that wants to change the lock is a signal, not a nuisance.
- Dependencies stay on caret ranges in `Cargo.toml`. `Cargo.lock` is the
  pin — it fixes an exact version and checksum for each crate — and
  dependabot's `cargo` ecosystem updates the lock directly. Hard-pinning
  the manifest would fight it.
- Every tool in `.mise.toml` is pinned to an exact version, the Rust
  toolchain included. Nothing there is covered by dependabot, so refresh
  it deliberately with `mise up` and read the diff.
- GitHub Actions are pinned to full-length commit SHAs with a `# vX.Y.Z`
  comment, and `zizmor` enforces that in CI.
- New dependencies must come from crates.io; `deny.toml`'s `sources`
  check rejects git and path dependencies.

## Commit Message Convention

Follow [Conventional Commits](https://conventionalcommits.org/):

**Format:** `type(scope): description`

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `build`, `ci`, `perf`, `revert`, `improvement`, `chore`

## Session Completion

Work is NOT complete until every change is committed, pushed, and CI passes.

1. **Quality gates** (if code changed):
   ```bash
   mise run ci
   ```

2. **Commit**: stage and commit every change from this session. Do not leave the working tree dirty.
   ```bash
   git status              # review untracked and unstaged files
   git add <files>
   git commit -m "<type>(<scope>): <description>"
   ```

3. **Push**:
   ```bash
   git pull --rebase && git push
   git status  # must show "up to date with origin"
   ```

4. **Verify CI**:
   ```bash
   mise run ci-watch
   ```
   On failure, inspect with `gh run view --log-failed`, fix, commit, push, and re-watch.

Never stop before CI is green. If anything fails, resolve and retry.
