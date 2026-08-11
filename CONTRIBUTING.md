# Contributing

Thank you for investing your time in contributing to our project!

Any contributions you make are governed by our [License](LICENSE).

Please follow our [Code of Conduct](CODE_OF_CONDUCT.md) to keep our community approachable and respectable.

To report a security problem, follow [SECURITY.md](SECURITY.md) instead of opening a public issue.

## Working on a change

```bash
mise trust            # once per clone: trust this repo's .mise.toml
mise install          # install the pinned toolchain
mise run ci           # lint + test + build + doc — must pass before you push
```

Commit messages follow [Conventional Commits](https://conventionalcommits.org/):
`type(scope): description`.

Open a pull request against `main`. CI runs the same `mise run ci` gate,
plus a [zizmor](https://docs.zizmor.sh/) audit of the GitHub Actions
workflows and a [cargo-deny](https://embarkstudios.github.io/cargo-deny/)
audit of `Cargo.lock`; all three must be green.

`Cargo.lock` is committed. If your change moves a dependency, commit the
updated lock file with it.

AI agents: see [AGENTS.md](AGENTS.md).

You could read the [GitHub Docs Contributing Guide](https://github.com/github/docs/blob/main/CONTRIBUTING.md) for general advice on how to contribute.

Since this is a small hobby project, your contribution may not be noticed for a while if we are busy elsewhere. Sorry!
