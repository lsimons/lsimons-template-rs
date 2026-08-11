# lsimons-template-rs

Project template for Rust CLI tools with a library core, standardized
tooling, and strict lints. Single crate with both `lib` and `bin` targets —
the CLI is a thin wrapper around the library, so business logic stays
testable in isolation and reusable by other consumers.

## Using This Template

1. Click **Use this template** on GitHub (or clone this repo).
2. Clone your new repo locally and run:

   ```bash
   mise trust            # once per clone: trust this repo's .mise.toml
   mise install          # install the pinned toolchain and audit tools
   mise run init         # rename `template` → your project name
   mise run build        # confirm it compiles
   ```

   `mise run init` auto-detects your project name from the git remote
   (or directory name), stripping `lsimons-` / `-rs` suffixes. Pass
   `--name foo` to override. Rust converts hyphens to underscores for
   the library crate name (`lsimons-foo` becomes `lsimons_foo` in
   `use` statements); init handles both forms. See `scripts/init.py`.

3. Update `AGENTS.md` (and `CLAUDE.md` symlink) with project-specific
   instructions, `README.md` with what the project actually is, and
   `Cargo.toml`'s `description` and `repository`.
4. Replace `src/lib.rs` and `src/main.rs` with real code.
5. Run `/setup` in your agent of choice. Repository settings — issue
   labels, private vulnerability reporting, Dependabot alerts and
   security updates — are GitHub state rather than files, so
   `Use this template` does not copy them and nothing in this repo can
   create them. `/setup` configures them against the new repo directly.

## Included Configuration

- **Rust edition 2024**, toolchain pinned to an exact version in
  `.mise.toml` and mirrored by `rust-version` in `Cargo.toml`
- **Single crate, dual target**: `src/lib.rs` holds the library, `src/main.rs`
  is the CLI binary that calls into it. `cargo test` exercises both.
- **clap 4 (derive)** for CLI argument parsing
- **`unsafe_code = "forbid"`** by default; clippy at `warn(all + pedantic)`,
  and `-D warnings` everywhere so a warning fails the build
- **rustfmt** pinned to edition 2024 via `rustfmt.toml`
- **assert_cmd + predicates** for end-to-end tests that spawn the compiled
  binary via `CARGO_BIN_EXE_<name>`
- **Release profile** with thin LTO, single codegen unit, and stripped
  symbols for small binaries
- **GitHub Actions CI** on push/PR to main, with actions pinned to
  full-length commit SHAs, an [actionlint](https://github.com/rhysd/actionlint)
  workflow check and a [zizmor](https://docs.zizmor.sh/) workflow-security
  audit
- **[cargo-deny](https://embarkstudios.github.io/cargo-deny/)** checks
  `Cargo.lock` against the RustSec advisory database and restricts
  dependency sources to crates.io — see `deny.toml`
- **Dependabot** for `cargo` and `github-actions`, weekly, with a 7-day
  cooldown. The `cargo` ecosystem updates `Cargo.lock` directly, so
  dependencies stay on caret ranges in `Cargo.toml`
- **`.mise.toml`** pins every tool to an exact version — the Rust
  toolchain included — and defines every repo task
- **`.editorconfig`** so editors that are not running rustfmt still
  agree with it

## Project Structure

```
lsimons-template-rs/
├── .github/workflows/ci.yml  # CI: lint/build/test/doc + zizmor + cargo-deny
├── .github/dependabot.yml    # Weekly cargo + github-actions updates
├── .editorconfig             # Editor defaults
├── .mise.toml                # Toolchain pin + every repo task
├── deny.toml                 # cargo-deny advisory and source policy
├── docs/spec/                # Feature specifications
├── scripts/init.py           # Rename-to-your-project helper
├── src/
│   ├── lib.rs                # Library code (testable core)
│   └── main.rs               # CLI binary, thin wrapper over the lib
├── tests/
│   └── cli.rs                # End-to-end CLI tests (assert_cmd)
├── AGENTS.md                 # AI agent instructions
├── CLAUDE.md -> AGENTS.md    # Claude Code compatibility
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE                   # Apache-2.0
├── SECURITY.md               # Vulnerability reporting route
├── Cargo.toml                # Package manifest
├── Cargo.lock                # Committed; never gitignore this
├── rustfmt.toml              # Formatter config
└── README.md
```

`CLAUDE.md` is a git symlink (mode `120000`). A Windows clone needs
`core.symlinks` enabled to get a real link rather than a text file
containing the target path.

## Development Commands

```bash
mise trust            # once per clone
mise install          # one-time: install the pinned toolchain
mise run build        # cargo build --all-targets --locked
mise run test         # cargo test --all-targets --locked
mise run lint         # cargo fmt --check + clippy -D warnings + actionlint
mise run format       # cargo fmt
mise run doc          # cargo doc --no-deps --all-features
mise run ci           # full CI gate: lint + test + build + doc
mise run deny         # cargo-deny: RustSec advisories + source policy
mise run audit        # zizmor workflow audit + mise run deny
mise run init         # rename the template to your project name
mise run ci-watch     # watch GitHub Actions for the current branch
```

`mise run audit` and `mise run deny` need network access — the first for
zizmor's online audits, both for the advisory database — which is why
they are not part of `mise run ci`. `audit` refuses to run without a
GitHub token rather than silently falling back to the weaker offline
check.

## When to Promote to a Workspace

Stay single-crate for as long as possible — it keeps builds fast and
navigation trivial. Convert to a Cargo workspace only when you need one of:

- Multiple binaries that share non-trivial code
- Publishing the library independently of the CLI
- Feature-gated subcrates (e.g., optional GPU / WASM targets)

## License

See [LICENSE](./LICENSE) (Apache-2.0).

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md). AI agents see
[AGENTS.md](./AGENTS.md).

## Security

See [SECURITY.md](./SECURITY.md).
