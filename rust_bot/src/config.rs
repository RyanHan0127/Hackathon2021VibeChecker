use std::io::prelude::*;

// Within a module in Rust, functions are kept private while the data inside
// is not. The concept of ownership is HUGE in Rust, with "borrowing" being
// the safest way to do things.
//
// For the safest implementation, the function would not return a String, but
// rather a &'static str, which borrows the primitive string literal. As things
// are now, the code is inefficient and unsafe, yet changing it runs into issues
// with the serde crate. (& = borrowing, 'static = lives in memory 4eva)
//
// i.e. ideally we would like the Config struct to only borrow the token
mod private {
    pub fn token() -> String {
        return String::from("ODI0MTgwODI4MTg2ODY5Nzcw.YFroNQ.yK7VjBdHH0NsfkqKQhgUIIciU3o");
    }
    pub fn prefix() -> String {
        return String::from("*");
    }
}

// Rusty Object Notation (RON) is merely a way of storing data in a readable
// filetype, like a JSON or YAML or something
//
// Serde is a SERialization and DEserialization framework. We use the methods
// from RON and the traits from serde combined
use ron::{ser, de};
use serde::{Serialize, Deserialize};

// Implement serde traits for this struct
#[derive(Debug, Serialize, Deserialize)]
pub struct Config {
  token: String,
  prefix: String,
}

// Implement a function for the struct
impl Config {
  pub fn new() -> Self {
    return Config {
      token: private::token(),
      prefix: private::prefix(),
    }
  }

  // Realistically this should be removed when we have our final bot,
  // as we only need to load from the config.ron in most cases
  pub fn save(&self) -> std::io::Result<()> {
    let pretty = ser::PrettyConfig::new()
      .with_depth_limit(2)
      .with_separate_tuple_members(true)
      .with_enumerate_arrays(true);
    let s = ser::to_string_pretty(&self, pretty)
      .expect("Serialization failed!");
    let mut file = std::fs::File::create("config.ron")?;
    if let Err(why) = write!(file, "{}", s) {
      println!("Failed writing to file: {}", why);
    } else {
      println!("Write operation succeeded!");
    }
    return Ok(());
  }

  pub fn load() -> std::io::Result<Config> {
    let input_path = format!("{}/config.ron", env!("CARGO_MANIFEST_DIR"));
    let f = std::fs::File::open(&input_path)
        .expect("Failed opening file");
    let config: Config = match de::from_reader(f) {
      Ok(x) => x,
      Err(e) => {
        println!("Failed to load config: {}", e);
        std::process::exit(1);
      }
    };
  
    return Ok(config);
  }

  // String inherets all of str's methods, so borrowing works fine.
  pub fn token(&self) -> &str {
    return &self.token;
  }
  
  pub fn prefix(&self) -> &str {
    return &self.prefix;
  }
}
