# lsimons-template-rs

Project template for Rust CLI tools with a library core, standardized
tooling, and strict lints. Single crate with both `lib` and `bin` targets —
the CLI is a thin wrapper around the library, so business logic stays
testable in isolation and reusable by other consumers.

## Using This Template

1. Copy this repository to create a new project
2. Replace placeholders throughout:
   - `$project` - project name hyphenated (e.g., `myproject`)
   - `$project` in `lsimons_$project` imports — Rust converts hyphens to
     underscores automatically for the library crate name (declared in
     `Cargo.toml`), so `lsimons-foo` becomes `lsimons_foo` in code
   - `$shortDescription` - one-line description

3. Update `Cargo.toml`:
   - Change `name`, `description`, and the `[lib]`/`[[bin]]` names

4. Replace `src/lib.rs` and `src/main.rs` with real code. The template will
   not build until the `$project` placeholders are substituted — that is
   intentional.

5. Update `AGENTS.md` (and `CLAUDE.md` symlink) with project-specific
   instructions.

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

> **Note:** CI is red on this template repo itself — the `$project`
> placeholder in `Cargo.toml` makes the package name malformed on purpose.
> Once you fork and do the search/replace described above, CI turns green.

## Project Structure

```
lsimons-$project/
├── .github/workflows/ci.yml  # CI pipeline
├── docs/spec/                # Feature specifications
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
# Build
cargo build --all-targets

# Run the CLI
cargo run -- <args>

# Test (library unit tests + integration tests)
cargo test --all-targets

# Lint (strict: all + pedantic, warnings denied)
cargo clippy --all-targets --all-features -- -D warnings

# Format
cargo fmt            # apply
cargo fmt --check    # verify (used in CI)

# Docs (warnings denied)
RUSTDOCFLAGS="-D warnings" cargo doc --no-deps --all-features
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
