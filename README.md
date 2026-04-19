# lsimons-template-rs

Project template for Rust CLI tools with a library core, standardized
tooling, and strict lints. Single crate with both `lib` and `bin` targets —
the CLI is a thin wrapper around the library, so business logic stays
testable in isolation and reusable by other consumers.

## Using This Template

1. Click **Use this template** on GitHub (or clone this repo).
2. Clone your new repo locally and run:

   ```bash
   mise install          # pin + install rust toolchain
   mise run init         # rename `template` → your project name
   mise run build        # confirm it compiles
   ```

   `mise run init` auto-detects your project name from the git remote
   (or directory name), stripping `lsimons-` / `-rs` suffixes. Pass
   `--name foo` to override. Rust converts hyphens to underscores for
   the library crate name (`lsimons-foo` becomes `lsimons_foo` in
   `use` statements); init handles both forms. See `scripts/init.py`.

3. Update `AGENTS.md` (and `CLAUDE.md` symlink) with project-specific
   instructions.
4. Replace `src/lib.rs` and `src/main.rs` with real code.

## Included Configuration

- **Rust edition 2024**, tracks latest stable Rust (no MSRV pin)
- **Single crate, dual target**: `src/lib.rs` holds the library, `src/main.rs`
  is the CLI binary that calls into it. `cargo test` exercises both.
- **clap 4 (derive)** for CLI argument parsing
- **`unsafe_code = "forbid"`** by default; clippy at `warn(all + pedantic)`
- **rustfmt** pinned to edition 2024 via `rustfmt.toml`
- **assert_cmd + predicates** for end-to-end tests that spawn the compiled
  binary via `CARGO_BIN_EXE_<name>`
- **Release profile** with thin LTO, single codegen unit, and stripped
  symbols for small binaries
- **GitHub Actions CI** on push/PR to main, with actions pinned to
  full-length commit SHAs (the repo setting *Require actions to be
  pinned to a full-length commit SHA* is enabled)
- **`.mise.toml`** pins toolchain + defines every repo task

## Project Structure

```
lsimons-template-rs/
├── .github/workflows/ci.yml  # CI pipeline (mise-action)
├── .mise.toml                # Toolchain pin + task runner
├── docs/spec/                # Feature specifications
├── scripts/init.py           # Rename-to-your-project helper
├── src/
│   ├── lib.rs                # Library code (testable core)
│   └── main.rs               # CLI binary, thin wrapper over the lib
├── tests/
│   └── cli.rs                # End-to-end CLI tests (assert_cmd)
├── AGENTS.md                 # AI agent instructions
├── CLAUDE.md -> AGENTS.md    # Claude Code compatibility
├── Cargo.toml                # Package manifest
├── rustfmt.toml              # Formatter config
└── README.md
```

## Development Commands

```bash
mise install          # one-time: pin + install toolchain
mise run build        # cargo build --all-targets --locked
mise run test         # cargo test --all-targets --locked
mise run lint         # cargo fmt --check + clippy -D warnings
mise run format       # cargo fmt
mise run doc          # cargo doc --no-deps --all-features
mise run ci           # full CI gate
```

## When to Promote to a Workspace

Stay single-crate for as long as possible — it keeps builds fast and
navigation trivial. Convert to a Cargo workspace only when you need one of:

- Multiple binaries that share non-trivial code
- Publishing the library independently of the CLI
- Feature-gated subcrates (e.g., optional GPU / WASM targets)

## License

See [LICENSE.md](./LICENSE.md).

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).
