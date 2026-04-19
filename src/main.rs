//! Thin CLI wrapper around the [`lsimons_template`] library.

use std::process::ExitCode;

use clap::Parser;
use lsimons_template::greet;

/// Command-line arguments.
#[derive(Debug, Parser)]
#[command(author, version, about, long_about = None)]
struct Cli {
    /// Who to greet.
    #[arg(default_value = "world")]
    name: String,
}

fn main() -> ExitCode {
    let cli = Cli::parse();
    match greet(&cli.name) {
        Ok(message) => {
            println!("{message}");
            ExitCode::SUCCESS
        }
        Err(err) => {
            eprintln!("error: {err}");
            ExitCode::FAILURE
        }
    }
}
