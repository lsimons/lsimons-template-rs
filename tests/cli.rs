//! End-to-end tests that spawn the compiled binary.
//!
//! Cargo makes `CARGO_BIN_EXE_lsimons-$project` available to integration tests;
//! `assert_cmd` uses it under the hood via `Command::cargo_bin`.

use assert_cmd::Command;
use predicates::str::contains;

#[test]
fn greets_named_arg() {
    Command::cargo_bin("lsimons-$project")
        .unwrap()
        .arg("Rust")
        .assert()
        .success()
        .stdout(contains("hello, Rust"));
}

#[test]
fn greets_default() {
    Command::cargo_bin("lsimons-$project")
        .unwrap()
        .assert()
        .success()
        .stdout(contains("hello, world"));
}

#[test]
fn rejects_empty_name() {
    Command::cargo_bin("lsimons-$project")
        .unwrap()
        .arg("")
        .assert()
        .failure()
        .stderr(contains("name must not be empty"));
}
