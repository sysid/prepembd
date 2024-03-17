# rust
[quick reference guide for the Pythonista in the process of becoming a Rustacean](https://github.com/rochacbruno/py2rs)
[Learn Rust in Y Minutes](https://learnxinyminutes.com/docs/rust/)

- closures are structs and can be eaten
- if you can't find a method on the container, look for a method on the iterator
- greeting.borrow().len() is fine since method calls will dereference implicitly

---
<!--ID:1689137981109-->
1. What output format options are there?
> ```rust
> {} calls display on an object
> {:?} calls debug on an object
> {:#?} pretty-print the debug formatting
> ```
<!--ID:1689137981111-->
1. What is the difference between :: and . ?
> . is used when you have a value on the left-hand-side. :: is used when you have a type or module.
>
> Or: . is for value member access, :: is for namespace member access.

---

# Styleguide .......................................................................................
- [Underscore - Rust Community Wiki](https://runrust.miraheze.org/wiki/Underscore): ignore value, wildcard pattern
- [Naming Convention, Terminology, Style](https://rust-lang.github.io/api-guidelines/naming.html)
- snake_case
- leading underscore: name is unused

## Comments

---
<!--ID:1690266651781-->
1. How to use docstring?
> - for `functions, structs, enums, traits, type aliases, macros, constant` items
> - do not use for code blocks
> ```rust
> /// This function prints a message.
> fn my_function() {
>     let my_integer = 10;
>     println!("{}", my_integer);
> }
> ```

---


# Infrastructure/Operations .......................................................................
```bash
# rustup.
rustup update  # upgrade to latest version.
rustup doc  # open offline documentation
rustup doc --std --cargo --core --reference --rust-by-example --test

# local documention of project crates:
cargo clean; cargo doc --open
# compile project and run
cargo run -- args

# run examples
cargo run --example confirm_simple
```
```rust
// debug
println!("ints_ints {:?}", ints_ints);

# create new project NOT lib
cargo init --bin proj
```
## Cargo/Structure
[cargo]($HOME/.cache/tldr/pages/common/cargo.md)


## Testing
[rust_testing.md]($VIMWIKI_PATH/dev/rust_testing.md)


## Environment, Configuration

---
<!--ID:1690266651784-->
1. How to list, set and read environment variables?
> ```rust
> // list it
> for (key, value) in env::vars() {
>    println!("{}: {}", key, value);
> }
> // use it safely
> let s = env::var("ENV_VAR").unwrap_or("default".to_string());
> // set it
> env::set_var("VAR_NAME", "value");
> ```

---

### Config Singleton and create config

---
<!--ID:1690041467827-->
1. How to create a mutable global Config singleton?
> - use the [config - Rust](https://docs.rs/config/latest/config/) crate: allows for stacked config
> - mutability via RW lock
> ```rust
> use config::Config;
> use lazy_static::lazy_static;
> use std::error::Error;
> use std::sync::RwLock;
>
> lazy_static! {
>     static ref SETTINGS: RwLock<Config> = RwLock::new(Config::default());
> }
> fn try_main() -> Result<(), Box<dyn Error>> {
>     // Set property
>     SETTINGS.write()?.set("property", 42)?;
>     // Get property
>     println!("property: {}", SETTINGS.read()?.get::<i32>("property")?);
>     Ok(())
> }
> fn main() {
>     try_main().unwrap();
> }
> ```
<!--ID:1691587766939-->
2. What does `lazy_static!` do?
> - Rust guarantees static variables are initialized in a thread-safe manner, but must be constants
> - possible to have statics that require code to be executed at runtime in order to be initialized
> - Any type in them needs to fulfill the `Sync` trait.
> - If the type has a destructor, then it will not run when the process exits.
> ```rust
> lazy_static! {
>     static ref HASHMAP: HashMap<u32, &'static str> = {
>         let mut m = HashMap::new();
>         m.insert(0, "foo");
>         m.insert(1, "bar");
>         m
>     };
>     static ref COUNT: usize = HASHMAP.len();
>     static ref NUMBER: u32 = times_two(21);
> }
> ```

<!--ID:1696062726216-->
1. what is difference between `OnceCell` and `lazy_static!`
> Both `OnceCell` and `lazy_static!` in Rust are used for lazy initialization, but they have different capabilities and use-cases:
>
> ### OnceCell
> 1. **Explicit Initialization**: You can decide when to initialize `OnceCell`. It provides methods like `get_or_init` and `set` for this.
> 2. **Mutable After First Assignment**: `OnceCell` itself is not mutable after the first assignment, but the value inside can be if it is of a mutable type.
> 3. **No Macros**: It's a struct, not a macro.
> 4. **Scoped to Functions**: You can use it in function or method scopes.
> 5. **Thread Safety**: `sync::OnceCell` is thread-safe, `unsync::OnceCell` is not.
> 6. **No Global State**: Works without defining a global/static variable.
> 7. **Standard Library**: As of Rust 1.57, it's part of the standard library.
> ```rust
> use once_cell::sync::OnceCell;
>
> static CELL: OnceCell<String> = OnceCell::new();
>
> // Later in the code
> let value = CELL.get_or_init(|| "hello".to_string());
> ```
> ### lazy_static!
> 1. **Implicit Initialization**: It's initialized automatically the first time you use it.
> 2. **Immutable After First Assignment**: The value is immutable after the first assignment.
> 3. **Macro-based**: Uses a macro to achieve its functionality.
> 4. **Static Scope**: Generally used for global static variables.
> 5. **Thread Safety**: It's thread-safe.
> 6. **Global State**: Usually used to define global state.
> 7. **External Dependency**: Requires adding an external crate.
>
> ```rust
> #[macro_use]
> extern crate lazy_static;
>
> lazy_static! {
>     static ref VALUE: String = "hello".to_string();
> }
>
> // Later in the code
> let value = &*VALUE;
> ```
> ### Summary
> - Use `OnceCell` when you want more control over the initialization process and/or you're not defining a static/global variable.
> - Use `lazy_static!` for a simpler, macro-based approach to initialize global static variables.

---

```rust
#[derive(Debug)]
pub struct Config {
    pub db_url: String,
    pub port: u16,
}

impl Config {
    fn new() -> Config {
        let db_url = env::var("DATABASE_URL").unwrap_or("../db_twbm.db".to_string());
        let port = env::var("PORT").unwrap_or("9999".to_string()).parse().expect("PORT must be a number");

        Config { db_url, port }
    }
}

// Create a global configuration singleton
lazy_static! {
    pub static ref CONFIG: Config = Config::new();
}
```


### dotenv
- `dotenv().ok()` should be called as early as possible in your program's execution, ideally at the beginning of your main function
- reads the environment variables from the .env file and loads them into the process's environment.
- These variables are then available to be accessed using the std::env module, just like any other environment variables.
- note that the dotenv crate will only load environment variables that are not already set in the current environment.
```rust
use dotenv::dotenv;
use std::env;
fn main() {
    let env = env::var("ENV").unwrap_or("development".to_string());
    let path = format!(".env.{}", env);
    dotenv().ok();
    dotenv::from_path(path).ok();
    // use the environment variables
}
```
### Platform Specific Code
```rust
fn open_uri(uri: String) {
    let output = if cfg!(target_os = "windows") {
        println!("Not implemented on Windows.")
    } else if cfg!(target_os = "linux") {
        println!("Not implemented on linux.")
    } else if cfg!(target_os = "macos") {
        let output = Command::new("open")
            .arg(uri)
            .output()
            .expect("failed to execute process");
        println!("status: {}", output.status);
        println!("stdout: {}", String::from_utf8_lossy(&output.stdout));
        println!("stderr: {}", String::from_utf8_lossy(&output.stderr));
    } else {
        println!("Unknown OS.")
    };
}

```

## Logging
[Logging in Rust - How to Get Started](https://www.shuttle.rs/blog/2023/09/20/logging-in-rust)
- the `log` crate only provides the API (facade), not implementations. You must pick a library that implements a logger.
- function name only via additonal crate, cannot be part of Formatter, must be passed in.
```rust
use log::{ info, warn, error, debug, };
fn main() {
    env_logger::init();  // RUST_LOG=debug
    debug!("Mary has a little lamb");
    error!("{}", "Its fleece was white as snow");
    info!("{:?}", "And every where that Mary went");
    warn!("{:#?}", "The lamb was sure to go");
}
```
### Programmatic Setup
- [Test Setup for env_logger](https://github.com/rust-cli/env_logger/blob/main/examples/in_tests.rs)
- run tests with `--nocapture`
- Initialization via drop-in attribute/annotation: `use test_log::test;` [test-log](https://crates.io/crates/test-log)
- Use global constructor/destructor function: [ctor](https://crates.io/crates/ctor)
```rust
#[cfg(test)]
#[ctor::ctor]
fn init() {
    env::set_var("SKIM_LOG", "info");
    env::set_var("TUIKIT_LOG", "info");
    let _ = env_logger::builder()
        // Include all events in tests
        .filter_level(log::LevelFilter::max())
        .filter_module("skim", log::LevelFilter::Info)
        .filter_module("tuikit", log::LevelFilter::Info)
        // Ensure events are captured by `cargo test`
        .is_test(true)
        // Ignore errors initializing the logger if tests race to configure it
        .try_init();
}
```

## Debugging, Fixing
```bash
cargo clean
export RUST_BACKTRACE=1  # top: most recently executed functions
```

## Including Resources into Binary

---
<!--ID:1690041467828-->
1. How to include resources into the final binary?
> - `include_bytes!()` macro
> - path provided to `include_bytes!()` is relative to the location of the Cargo.toml
> - reads content at compile time (!!)
> - crate 'include_dir' allows to include directory
> ```rust
> use include_bytes::include_bytes;
> let my_file_contents: &'static [u8] = include_bytes!("path/to/myfile.txt");
> fn main() {
>     let content = std::str::from_utf8(my_file_contents).unwrap();
>     println!("{}", content);

>     let config_bytes = include_bytes!("resources/config.json");
>     let image_bytes = include_bytes!("resources/image.png");
>     // use the config and image bytes
> }
> ```
>

---

## Documentation
- all offline, just run `cargo doc --open`
- Gotcha: make sure in Cargo.toml documentation is not configured
- dev-dependencies: `cargo doc --all-features`

- "required methods" refer to methods that must be implemented in order for a type to satisfy a particular trait
- "provided methods" refer to methods that are automatically implemented by compiler, ala default implementation by
- Implementors of a trait are types that have implemented the methods defined in the trait.

### Code Documentation
- doc-comments: `/// or /** */` treated the same way and are converted to HTML documentation
- uses markdown (backticks for code)
- Arguments: to list the function's arguments and provide a brief description of what they do.
- Examples: provides an example of how to use the function, including a code snippet and an assertion to check the result.
```rust
/**
 * Adds two numbers together and returns the result.
 *
 * # Arguments
 *
 * * `a` - The first number to add.
 * * `b` - The second number to add.
 *
 * # Returns
 *
 * # Examples
 *
 * '''
 * let result = add(2, 3);
 * assert_eq!(result, 5);
 * '''
 */
fn add(a: i32, b: i32) -> i32 {
    a + b
}
```


## Attributes

---
<!--ID:1690266651785-->
1. What are inner vs outer attributes?
> - Inner attributes, written with a bang (!) after the hash (#), apply to the item that the attribute is declared within.
> - Scope entire module/crate/binary: Exclamation mark: `#![allow(unused_imports)]`
>    - a library -- the crate root will be a file called lib.rs
>    - an application -- main.rs
>    - an integration test - the crate root is each file in tests/
>    - an example - the crate root is each file in examples/
> - Outer attributes, written without the bang after the hash, apply to the thing that follows the attribute.

---


### Structs Examples
```rust
use serde::{Serialize, Deserialize};

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub struct Person {
    pub first_name: String,
    pub last_name: String,
    pub age: u32,
    #[serde(default)]
    pub height: Option<f32>,
}
```
`#[serde(rename_all = "snake_case")]`: We've used the serde attribute to specify that field names should be converted to snake_case when serialized and deserialized.

`#[serde(default)]`: We've used the serde attribute to specify that the height field should default to None if it is not present during deserialization.

```rust
#[derive(Debug, Clone, Copy)]
pub struct Point {
    pub x: f32,
    pub y: f32,
    #[deprecated(since = "1.0.0", note = "Use `z` instead")]
    pub z_coord: f32,
    #[cfg(feature = "2d-only")]
    pub z: f32,
}
```
`#[deprecated(since = "1.0.0", note = "Use z instead")]`: We've used the deprecated attribute to mark the z_coord field as deprecated, and to provide a message that suggests using the z field instead. This can help prevent users of our code from using deprecated fields and APIs.

`#[cfg(feature = "2d-only")]`: We've used the cfg attribute to conditionally include the z field in the struct based on a compile-time feature flag. This can help reduce code size and complexity when certain features are not needed.


---
<!--ID:1690266651786-->
1. What are important derive attributes?
> ```rust
> #[derive(Copy, Clone)]
> #[derive(Debug)]
> #[derive(Default)]
> #[derive(PartialEq, Eq)]
> #[derive(PartialOrd, Ord)]
> #[derive(Serialize, Deserialize)]
> ```

<!--ID:1696754223912-->
1. Explain `PartialOrd` vs `Ord`.
> ### PartialOrd
> - for some pairs of values, it might be undecidable how they relate to each other in terms of ordering.
> - example: floating-point numbers include NaN (Not-a-Number)
> - comparison can return an `Option<Ordering>` instead of an `Ordering`. The Option can be `None`, indicating that the values couldn't be ordered:
>
> ### Ord
> - types that have a total order, meaning that any two values can be meaningfully compared.
>
> ### Summary
> - Use PartialOrd when you have a type that might have incomparable values (like floating-point numbers).
> - Use Ord when you know that all values of a type can be meaningfully compared to each other.
> - Implementing `Ord` allows to use methods such as `sort` for sorting a vector, while PartialOrd would only allow you to use `partial_sort`.
> - when implementing `Ord`, you are also required to implement `PartialOrd, PartialEq, Eq`.

---

> `#[derive(new)]`: attribute creates a new constructor function for the annotated type. That function takes an argument for each field in the type giving a trivial constructor

`#[doc = "some documentation"]`: add documentation to your struct that will be included in the generated documentation
`#[macro_use]`: attribute tells the Rust compiler to make all the macros defined in the given crate available for use in the current crate.
`#[non_exhaustive]`: marks a struct as non-exhaustive, which means that it can have additional fields added in the future without breaking backward compatibility
`#[repr(C)]`: specifies the memory layout of your struct to be compatible with the C language
`#[repr(transparent)]`: specifies that struct has the same memory layout as its single field

`#[serde(rename_all = "snake_case")]`: specifies that field names should be converted to snake_case when serialized and deserialized

### Cfg
`#[cfg(debug_assertions)]`: This attribute enables code only when the debug_assertions flag is set. This flag is enabled by default in debug builds and disabled in release builds.
`#[cfg(target_os = "windows")]`: This attribute enables code only when the target operating system is Windows.
`#[cfg(target_os = "macos")]`: This attribute enables code only when the target operating system is macOS.
`#[cfg(target_os = "linux")]`: This attribute enables code only when the target operating system is Linux.
`#[cfg(target_arch = "x86")]`: This attribute enables code only when the target architecture is x86.
`#[cfg(target_arch = "x86_64")]`: This attribute enables code only when the target architecture is x86_64.
`#[cfg(all(unix, not(target_os = "macos")))]`: This attribute enables code only when the target operating system is a Unix-like system other than macOS.
`#[cfg(any(target_os = "windows", target_os = "macos"))]`: This attribute enables code only when the target operating system is Windows or macOS.
`#[cfg(feature = "foo")]`: This attribute enables code only when the foo feature is enabled in the Cargo.toml file.

### Allow

---
<!--ID:1690266651787-->
1. What are important allow properties?
> ```rust
> #[allow(dead_code)]
> #[allow(unused_imports)]
> #[allow(unused_variables)]
> ```

---

`#[allow(unused_mut)]`: This attribute tells the Rust compiler to ignore variables that are declared as mutable but not modified in the code.
`#[allow(unused_parens)]`: This attribute tells the Rust compiler to ignore unnecessary parentheses in expressions.
`#[allow(unused_assignments)]`: This attribute tells the Rust compiler to ignore assignments to variables that are not used in the code.
`#[allow(unused_must_use)]: This attribute tells the Rust compiler to ignore the #[must_use]` attribute for functions that are not used in the code.
`#[allow(unused_attributes)]`: This attribute tells the Rust compiler to ignore attributes that are not being used in the code.
`#[allow(non_snake_case)]`: Gotcha: not working per field, but per module
`#[allow(non_camel_case_types)]`


## Macro
[rust_macro.md]($VIMWIKI_PATH/dev/rust_macro.md)


## Filesystem, Path

---
<!--ID:1690041467829-->
1. What is difference between Path and PathBuf?
> - std::path::Path and std::path::PathBuf in Rust are somewhat similar to str and String.
> - Path is an immutable borrowed reference to a path like &str. It's basically a read-only view into a string slice, where the underlying data is stored somewhere else.
> - safe for sharing across multiple threads
> - PathBuf, is like String - it's an owned, mutable buffer. It owns the data and you can change it, push to it, etc.
> - This means that you can use methods like push or pop to add or remove parts of the path.
>
> If your function needs to modify or keep the path, you should take a PathBuf.
> If your function just needs to read the path and doesn't need to keep it around, you should take a &Path.
> both types do not create/delete paths, use `std::fs`

---

### std::fs

---
<!--ID:1690041467830-->
1. What is difference between `std::fs` and `std::path`?
> - `std::fs` interacting with the filesystem, such as creating, reading, and writing files and directories.
> - functions for querying metadata about files and directories
> - Examples of functions provided by the std::fs crate include `create_dir, create_dir_all, read_to_string, write, metadata`.
> - use camino to work with UTF8: `Utf8Path`
>
> - `std::path`: joining paths, splitting paths, and normalizing paths.
> - It also provides types for working with different parts of a file path, such as the root and the file name.
> ```rust
> // file exists
> if Path::new("path/to/file.txt").exists() {
>     println!("The file exists");
> } else {
>     println!("The file does not exist");
> }
> // create path recursivley unconditionally
> fs::create_dir_all(dir_path).unwrap_or_else(|_| {});
> ```
<!--ID:1690777097436-->
1. How to read or create a file?
> ```rust
> // Open the .gitignore file, or create it if it does not exist.
> let file = OpenOptions::new().write(true)
>     .create(true)
>     .read(true)
>     .open(&gitignore_path)
>     .context("Cannot create/read file.")?;
> let reader = BufReader::new(file);
> // Gather all lines into a HashSet for fast lookup
> let gitignore_entries: std::collections::HashSet<String> =
>     reader.lines().filter_map(Result::ok).collect();
> ```
<!--ID:1692204458542-->
1. What is the best way to read file into `Vec<String>`?
> ```rust
> // reads the file line by line, which is memory-efficient and can handle very large files
> fn read_lines<P>(filename: P) -> io::Result<Vec<String>>
> where
>     P: AsRef<Path>,
> {
>     let file = File::open(filename)?;
>     let buf_reader = io::BufReader::new(file);
>     buf_reader.lines().collect()
> }
>
> // one-liner
> fn read_lines(filename: &str) -> Result<Vec<String>, std::io::Error> {
>     let content = fs::read_to_string(filename)?;
>     Ok(content.lines().map(|s| s.to_string()).collect())
> }
> ```
<!--ID:1692204458543-->
1. How to write `Vec<String>` to a file?
> - Open the file in write mode, which will create the file if it doesn't exist or truncate the file if it does.
> - This is the "overwrite" behavior.
> ```rust
> // write entire buffer
> fn write_lines(filename: &str, lines: &Vec<String>) -> io::Result<()> {
>     let mut file = File::create(filename)?;
>     let content = lines.join("\n");
>     file.write_all(content.as_bytes())?;
>     Ok(())
> }
> // memory efficient
> fn write_lines(filename: &str, lines: &Vec<String>) -> io::Result<()> {
>     let mut file = File::create(filename)?;
>     for line in lines {
>         writeln!(file, "{}", line)?;
>     }
>     Ok(())
> }
> ```

---


# Gotcha ...........................................................................................
- import attributes `#[rstest]` before using them
- returning within if {} requires `return`
- `Termination` trait: `main` must only return `Result<(), Error>`, no actual result values



# Concepts .........................................................................................
The unifying principles behind Rust are:
- strictly enforcing safe borrowing of data
- functions, methods and closures to operate on data
- tuples, structs and enums to aggregate data
- pattern matching to select and destructure data
- traits to define behaviour on data

- memory safety not via Garbage Collector (Go) but via Ownership rules
- borrow checker--the part of the compiler that ensures that references do not outlive the data to which they refer
- each reference has a lifetime
- Safe Rust and Unsafe Rust: Safe Rust imposes additional restrictions on the programmer (e.g. object ownership management)
- If a given object access does not support many threads (i.e. is not marked with an appropriate trait), it needs to be synchronized by a mutex that will lock access to this particular object for other threads.
- To ensure that operations performed on an object will not break it, only one thread has access to it.

## Ownership
- main purpose of ownership is to manage heap data
- Each value in Rust has a variable that's called its owner.
- There can only be one owner at a time.
- When the owner goes out of scope, the value will be dropped.
- memory is automatically returned once the variable that owns it goes out of scope
- when a variable goes out of scope, Rust automatically calls the drop function
- move instead of shallow-copy (stack-copy) (originator loses access)
- deep-copy: heap copy
- special annotation called the `Copy` trait that we can place on types that are stored on the stack (eg int)
- types with `Copy` make them still valid after assignment to another variable
- Rust won't let us annotate a type with Copy if the type, or any of its parts, has implemented the Drop trait
- Passing a variable to a function will move or copy, just as assignment does
- returning values can also transfer ownership
- feature for using a value without transferring ownership, called references
- ownership controls the lifetime of values and their associated resources
- ensures that a value can only be used in one place at a time, and that its resources are automatically freed when the value goes out of scope.

is really just the idea of “the responsibility for deallocating this data must be well-defined”:
- Literals, statics and leaking are "this is never deallocated". Rc is "this is deallocated when all of the shared-owners are gone".
- More variations are possible; the important thing is that the responsibility is always defined.

### Refernces, Borrowing
- borrowed value has a lifetime
- is like a pointer in that it's an address we can follow to access the data stored at that address; that data is owned by some other variable.
- Unlike a pointer, a reference is guaranteed to point to a valid value of a particular type for the life of that reference.
- We call the action of creating a reference 'borrowing'
- Just as variables are immutable by default, so are references. We're not allowed to modify something we have a reference to.
- cannot have a mutable reference while we have an immutable one to the same value.
- reference's scope starts from where it is introduced and continues through the last time that reference is used
- references are only complete types with a lifetime annotation. `&T` is not a type; it's a type constructor that only becomes a proper type when the lifetime is known, so `&'a T` is a type.
- While move semantics are the default, certain types are copied by default: `Copy` trait
```rust
fn main() {
    let mut s = String::from("hello");

    let r1 = &s; // no problem
    let r2 = &s; // no problem
    println!("{} and {}", r1, r2);
    // variables r1 and r2 will not be used after this point

    let r3 = &mut s; // no problem
    println!("{}", r3);
}
```

---
<!--ID:1688539670821-->
1. How to change a String variable within a function for outer scope?
> ```rust
> fn xxx(x: &mut String) {
>     *x = "new string".to_string();
> }
>
> fn main() {
>     let mut s = "old string".to_string();
>     xxx(&mut s);
>     println!("{}", s);
> }
> ```
> The reason for using `*x` instead of x is that in Rust, x is a mutable reference to a String, not the String value itself.
> To change the String value, you have to dereference x with the `*` operator to get to the actual value. This is also why you need to use `to_string()`. You're assigning a new String value, not a `&str` reference.

---

#### Lifetime
[I don't able to understand lifetime specifiers](https://users.rust-lang.org/t/i-dont-able-to-understand-lifetime-specifiers/95603/17)
[Lifetimes - Comprehensive Rust 🦀](https://google.github.io/comprehensive-rust/ownership/lifetimes.html)
[Lifetime intuition](https://quinedot.github.io/rust-learning/lifetime-intuition.html)
[Lifetime Misconceptions](https://github.com/pretzelhammer/rust-blog/blob/master/posts/common-rust-lifetime-misconceptions.md)

A borrowed value has a lifetime:
- The lifetime can be implicit: add(p1: &Point, p2: &Point) -> Point.
- Read `&'a Point` as "a borrowed Point which is valid for at least the lifetime a".
- Lifetime parameters are generic parameters, just like type parameters: `'a` is a placeholder for the lifetime of the reference.
- Lifetimes are always inferred by the compiler: you cannot assign a lifetime yourself.
- Lifetime annotations create constraints; the compiler verifies that there is a valid solution.
- Lifetimes for function arguments and return values must be fully specified, but Rust allows
    lifetimes to be elided in most cases with a [few simple rules](https://doc.rust-lang.org/nomicon/lifetime-elision.html).
- connecting the lifetimes of parameters and return values
- If you need every reference to be potentially valid for a different lifetime, then you need multiple lifetime parameters
- borrow checker uses explicit lifetime annotations to determine how long REFERENCES should be valid.
- lifetime != scope
     The borrow has a lifetime that is determined by where it is declared, valid as long as it ends before the lender is destroyed.
     However, the scope of the borrow is determined by where the reference is used.
- Any input which is borrowed (=lender) must outlive the borrower.
- references are only complete types with a lifetime annotation. `&T` is not a type; it's a type constructor that only
    becomes a proper type when the lifetime is known, so `&'a T` is a type. `&String` is actually sugar syntax for `&'a String`
- compiler will have to assign the lifetime that satisfies all references, ie. their intersection, ie. the shortest of the lifetimes.
- Since the compiler doesn't equate lifetimes with scopes (NLL = non-lexical lifetimes), it can arbitrarily decide to shorten the borrow of `first_num` even though it's still in scope

usually inferred:
In local context (e.g., function arguments and local variables), the compiler can usually infer the lifetime parameter of references, so you can get away with writing &T and the compiler will actually infer a correct lifetime.
But in a global context, e.g. a type declaration, there's no information from which the compiler could infer the lifetimes, just like it couldn't infer the types of struct fields. I.e., neither the following two declarations compile for exactly the same reason:
```rust
struct BadType {
    field: _, // no explicit type given
}
struct BadLifetime {
    field: &i32, // no explicit lifetime given
}
```
`T: 'a`         : All references in T must outlive lifetime 'a.
`T: Trait + 'a` : Type T must implement trait Trait and all references in T must outlive 'a.
`'static`       : data pointed to by the reference lives for the entire lifetime of the running program

function signatures with lifetimes have a few constraints:
- any reference must have an annotated lifetime.
- any reference being returned must have the same lifetime as an input or be static.
- returning references without input is banned if it would result in returning references to invalid data.
```rust
// lifetime of foo cannot exceed that of either 'a or 'b.
foo<'a, 'b>

// `'static` lifetime refers to the lifetime of the entire program.
let s: &'static str = "Hello, world!";

// lifetime parameter 'a is used to specify that both references must have the same lifetime.
// This means that the reference returned by the function will also have the same lifetime as x and y.
fn foo<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}
// Wrong, does not compile:
// the "same lifetimes" constraint can only be satisfied if the compiler takes the intersection of both lifetimes, ie. the shortest one. 
// That however means that the struct itself isn't valid for long enough to be accessed outside of the scope of y
struct S<'a> {
    x: &'a i32,
    y: &'a i32
}
fn main() {
    let x = 10;
    let r;
    {
        let y = 20;
        {
            let s = S { x: &x, y: &y };
            r = s.x;
        }
    }
    println!("{}", r);  // moved x cannot exist here any more
}
```
- lifetimes markup in Rust is somewhere between comments in other languages and code of program. Some compilers just ignore these completely, some may use them to do verification of you program (like doctests hidden in your comments can be used, too), but they don't directly affect the generated code
- [non-lexical lifetimes (NLL).](https://users.rust-lang.org/t/i-dont-able-to-understand-lifetime-specifiers/95603/21)

#### Exclusive Borrows
it doesn't matter what the return type exactly is, all that matters is that the function API demands an exclusive borrow of the String which lasts as long as the return value will be valid
```rust
fn demo1<'a>(s1:&'a mut String, a: &'a i32) -> &'a i32 {
    a
}
```

#### Static

---
<!--ID:1692204458544-->
1. What means `static` ?
> - static is a keyword.
> - When used in the context of lifetimes (as in `&'static str`), `'static` denotes a lifetime that lasts for the entire duration of the program.
> - When used in the context of variable declaration (as in `static GLOBAL_VARIABLE: i32`), static is a keyword that defines a global variable with a fixed memory location and 'static lifetime.

---

#### Gotcha
`'static`       : as trait bound `fn print_it( input: impl Debug + 'static )`: type does not contain any non-static references
[Static - Rust By Example](https://doc.rust-lang.org/rust-by-example/scope/lifetime/static_lifetime.html)


### Pass by reference vs Pass by value
- it is generally better to pass references because save memory and improve performance
- does not violate encapsulation because ownership model ensures that references are immutable by default.
- Passing by value is generally simpler and more self-contained, as it makes it clear that the function operates on its own copy of the data, and it does not affect the original data.
- if the function should take ownership of the data and move it out, pass by value is the only way


### Slice

---
<!--ID:1689137981112-->
1. What is a Slice?
> - [T] is a slice type, denotes a slice of type T.
> - is a dynamically-sized view into a contiguous sequence, array, other slice.
> - used to borrow a section of a collection, whether it be a part of a list, string, or array.
> - Slices are similar to arrays, but their length is not known at compile time.
> - Instead, a slice is a two-word object, the first word pointing to the data, and the second word being the length of the slice.
> - It doesn't have an identity or standalone existence separate from the array it's referring to
> - Because of this, slices cannot be used directly and must be used through some kind of pointer. Very common type is &[T], a reference to a slice (fat pointer)
> ```rust
> fn main() {
>     let a = [1, 2, 3, 4, 5];
>     let slice = &a[1..3];
>     println!("{:?}", slice);
> }
> ```

---

### clone, cloned
#### clone: deep copy
- many complex types such as String, Vec, and HashMap.
- It is generally used when you want to create a new value that is an independent copy of an existing value.
- use to create a copy of the value stored in the reference, which will also change `&Option<String> -> Option<String>`
```rust
let reference: &Option<String> = &Some("hello".to_string());
let cloned: Option<String> = reference.clone();

// alternative: as_ref + cloned:  !!!
// .as_ref() method, that will convert the reference to an Option<&String> and then you can use .cloned() to convert it to an Option<String>.
let cloned: Option<String> = reference.as_ref().cloned();
```

#### cloned
- used when you want to create an iterator that clones the elements of another iterator.
- It is implemented for iterators that produce elements that implement the Clone trait, and it can be useful when you want to create a new collection from the elements of an iterator.
```rust
let x = 5;
let y = x.clone();

assert_eq!(x, y);

let v = vec![1, 2, 3];

// cloned() creates an iterator that clones the elements of v
let v_cloned: Vec<i32> = v.iter().cloned().collect();

assert_eq!(v, v_cloned);
```

### to_owned (to_string, clone)
- is a method on the `ToOwned` trait that creates an owned value from a borrowed value.
- The owned value is a deep copy of the borrowed value, and it is allocated on the heap rather than the stack.
- used when you want to create a new owned value that is an independent copy of an existing borrowed value.
```rust
let s: &str = "hello";
let s_owned: String = s.to_owned();

assert_eq!(s, s_owned);
```
In this example, the `to_owned` method is used to create an owned String from a borrowed &str. The resulting String is a deep copy of the original &str, and it is allocated on the heap.


### AsRef, as_ref, and &
- in both cases the result is a reference to a value on the heap
- The main difference is in how the reference is created and what types it can be called on.
- `as_ref()` allows for conversion from a type to a borrowed version of itself and can be used to convert owned value to a reference,
- `as_ref()` is a more flexible and generic way of handling references.
- `&` is an operator that creates a reference to ANY value and it can be used to create a reference to an existing value.
   can be used on both owned types or other references
- advantage of `as_ref()` is that it allows for a more consistent and predictable way of handling references, as it provides a common way to convert an owned value to a reference regardless of the type.
- Another advantage is that `as_ref()` can be used in generic contexts, where the type of the value is not known at compile time.
- By using the `AsRef` trait, the function can accept a wide range of types and handle them in a consistent way. This can make the code more reusable and less dependent on the specific types.
- Additionally, using `as_ref()` also allows to convert between different types of references as well.
   For example, you can use `as_ref()` to convert String to `&str` or `Vec<i32>` to `&[i32]` etc.
- can be particularly useful when working with types that implement both the ToOwned and ToRef traits, as it allows to convert between owned and borrowed values.

- `s.as_ref()` and `&s` are both used to create a reference to a String s, but they differ in the type of reference they return.
- `s.as_ref()` returns a `&str` reference. A `&str` reference is a slice of a string, which is a reference to a contiguous sequence of characters.
- `&s` creates a `&String` reference. It's a reference to the whole String object.
- important to note that `&str` is a more lightweight type than String, as &str is just a reference to the data, whereas String is a heap-allocated, mutable object.
- So in most cases, if you just need to pass a string as a reference, it's better to use s.as_ref() rather than &s
```rust
let s = String::from("hello");
let s_ref: &str = s.to_ref();
assert_eq!(s, s_ref);
```
In this example, the `to_ref` method is used to create a borrowed `&str` from an owned String.
The resulting `&str` is a reference to the original String, and it is allocated on the stack.

---
<!--ID:1690348275068-->
1. How to not consume an Option via `ok_or`?
> - `ok_or` consumes the Option, which isn't allowed when you have a reference to it.
> - resolve this issue by creating a reference to the inner value of the Option using `as_ref()`
> ```rust
> let target_dir = self.target_dir.as_ref().ok_or(anyhow!("target_dir is None"))?;
> let mut target_file_path = target_dir.join("dot.envrc");
> ```
> - `as_ref` converts the `Option<T>` to `Option<&T>,` and thus we are not moving the value out of `self.target_dir`.
> - `target_dir` is a reference to the inner value of the Option, and no ownership is transferred

<!--ID:1690777097437-->
1. Explain: `fn load_file<S: AsRef<str>>(file: S) -> Result<Box<dyn io::Read + Send + Sync>>`
> - function takes generic parameter S that implements the `AsRef<str>` trait.
> - This is a way of saying "this function will accept any type that can be referenced as a string". Common types that implement AsRef<str> are String and &str.
> - the `Ok(T)` type is `Box<dyn io::Read + Send + Sync>`, a trait object.
> - This represents a heap-allocated instance of a type that implements the `io::Read, Send, Sync` traits.
> - The `io::Read` trait represents a type that can be read from, like a file or a network socket.
> - `Send, Sync` are marker traits: Send means that ownership of the type can be transferred safely between threads, and Sync means it is safe to reference the type from multiple threads.

<!--ID:1691587766940-->
1. What does the trait bound mean?
```rust
pub fn file_do<P>(filename: P, expected_lines: &[&str]) -> Result<()>
where
    P: AsRef<Path>,
```
> The `P: AsRef<Path>` constraint means that the filename parameter can be any type that implements the `AsRef<Path>` trait
> `AsRef<T>` in function parameters provides a flexible API without burdening the caller to convert their type to a specific type, all while avoiding unnecessary allocations or data ownership transfers.
> ```rust
> &str
> String
> Path
> &Path
> PathBuf
> 
> file_do("/path/to/file", &["line1", "line2"]);
> file_do(String::from("/path/to/file"), &["line1", "line2"]);
> file_do(Path::new("/path/to/file"), &["line1", "line2"]);
> file_do(&Path::new("/path/to/file"), &["line1", "line2"]);
> file_do(PathBuf::from("/path/to/file"), &["line1", "line2"]);
> ```

---

### Passing Vector of Objects as Parameter
- using more references will increase the complexity and can make the code harder to reason about, so it's important to use the most appropriate level of referencing for the task at hand.
- in most cases, passing a vector of references `&Vec<&Xxx>` is not the best practice
- passing a vector of owned objects or a reference to the vector of owned objects is more appropriate.

#### modify the contents of the vector:
pass a `Vec<Xxx>` as a parameter, which allows the function to take ownership of the vector and modify it.
function takes ownership of the vector and can modify its contents.

#### read the contents of the vector and doesn't modify it:
pass a `&Vec<Xxx>` as a parameter, which allows the function to borrow the vector without taking ownership.
function borrows the vector, so it can read its contents, but cannot modify it.

#### modify the contents of the objects in the vector, but not the vector itself:
pass a `Vec<&mut Xxx>` as a parameter, which allows the function to borrow the objects in the vector mutably.

#### needs to read the contents of the objects in the vector:
pass a `Vec<&Xxx>` as a parameter, which allows the function to borrow the objects in the vector immutably.
function can read the contents of the objects, but cannot modify the objects themselves, or the vector.

### Vec<&Xxx> vs &Vec<Xxx>
`Vec<&Xxx>` is preferrable when the function needs to take ownership of the vector of references to the objects of type Xxx and keep it for future usage.
This allows the function to modify the order or elements within the vector, but not the objects themselves.

`&Vec<Xxx>` is preferrable when the function only needs to read the contents of the vector of objects of type Xxx and it's not necessary for the function to take ownership of the vector.
This allows the function to borrow the vector so it can read its contents, but cannot modify it. This is a good choice when the vector is going to be used in multiple places, and it would be wasteful to clone it.


## Generics, Trait Bounds, Lifetimes
- generics abstract over the concrete field type
- traits abstract over types. They’re similar to interfaces
- In the context of the `impl<T: ?Sized> AsRef<T>` syntax, the `?Sized` indicates that the type T in the `AsRef<T>` implementation is unsized.
- An unsized type is a type whose size is not known at compile time, such as a slice `[T]` or a trait object `dyn Trait`
- the `?Sized` marker is used to indicate that a type can either be a sized type or an unsized type.
- By using the `?Sized` marker, the definition of Cow can be made generic and flexible enough to work with both sized and unsized types.

```rust
// full example
use std::fmt::Display;
fn longest_with_an_announcement<'a, T>(
    x: &'a str,
    y: &'a str,
    ann: T,
) -> &'a str
where
    T: Display,
{
    println!("Announcement! {}", ann);
    if x.len() > y.len() {
        x
    } else {
        y
    }
}
```
### Trait
- a value that implements a trait is a value of a specific type that has implemented the methods defined in the trait.
- A trait object, on the other hand, is a runtime value that represents any type that implements a particular trait.
- "required methods" refer to methods that must be implemented in order for a type to satisfy a particular trait
- "provided methods" refer to methods that are automatically implemented by compiler, ala default implementation by
- can also be implemented for types from external crates
```rust
fn alice_and_bob(mut empty_repository: impl Repository) -> impl Repository {
    empty_repository.add("Bob", 21);
    empty_repository.add("Alice", 22);
    empty_repository
}
struct InMemoryRepository { // Implementation details...  }
impl Repository for InMemoryRepository { // Method definitions...  }

struct SqliteRepository { // Implementation details...  }
impl Repository for SqliteRepository { // Method definitions...  }

fn main() {
    let in_memory_repository = InMemoryRepository { /* Initialize fields */ };
    let in_memory_repository = alice_and_bob(in_memory_repository);

    let sqlite_repository = SqliteRepository { /* Initialize fields */ };
    let sqlite_repository = alice_and_bob(sqlite_repository);
}
```
#### associated types
- are a way to define a type that is used within a trait, but is not specified in the trait itself. Instead, the actual type is specified when the trait is implemented.
- type placeholder such that the trait method definitions can use these placeholder types in their signatures.
- The implementor of a trait will specify the concrete type to be used instead of the placeholder type for the particular implementation
```rust
trait MyTrait {
    type MyType = i32;  // default type specification
    fn my_method(&self) -> Self::MyType;
}
// Implementation
struct MyStruct {
    data: i32,
}
impl MyTrait for MyStruct {
    type MyType = f32;  // specification
    fn my_method(&self) -> Self::MyType {
        self.data as f32
    }
}
```
- `<Type as Trait>::Item` is "associated item syntax".
- `<Type as Trait>` refers to a specific implementation of the `Trait` for the type `Type`.
- The `::Item` syntax is then used to refer to the associated item `Item` of the trait implementation.

Example:
associated type `Owned` is associated with the `ToOwned` trait, and `<B as ToOwned>::Owned` refers to the specific implementation of the Owned associated type for the type B.

#### Trait Object (dyn)
[dyn Trait overview - Learning Rust](https://quinedot.github.io/rust-learning/dyn-trait-overview.html)
- `dyn MyTrait` is a way to tell the compiler about a dynamically sized type that implements MyTrait
- runtime value that represents any type that implements a particular trait (enum, struct)
- Fat Pointer: points to both an instance of a type implementing specified trait and a table used to look up trait methods on that type at runtime.
- created by specifying some sort of pointer: `&` reference `Box<T>` smart pointer, then the `dyn` keyword
- [dynamic dispatch](https://doc.rust-lang.org/book/ch17-02-trait-objects.html#trait-objects-perform-dynamic-dispatch) in Rust, which allows to call methods on a value without knowing the specific type of the value at compile time.
```rust
trait MyTrait { fn my_method(&self); }

struct MyStruct1;
struct MyStruct2;
impl MyTrait for MyStruct1 {
    fn my_method(&self) { println!("MyStruct1"); }
}
impl MyTrait for MyStruct2 {
    fn my_method(&self) { println!("MyStruct2"); }
}

fn main() {
    let x = MyStruct1;  // values of specific types that have implemented the MyTrait trait, and they can only be used as values of those specific types.
    let y = MyStruct2;
    x.my_method(); // prints "MyStruct1"
    y.my_method(); // prints "MyStruct2"

    // trait object of type Box<dyn MyTrait>, can hold any value that implements the MyTrait trait.
    // The specific type of the value is determined at runtime, and can be different for each trait object.
    let x: Box<dyn MyTrait> = Box::new(MyStruct1);
    let y: Box<dyn MyTrait> = Box::new(MyStruct2);

    x.my_method(); // prints "MyStruct1"
    y.my_method(); // prints "MyStruct2"
}
```
#### Trait Bounds
[Trait Bounds - Comprehensive Rust 🦀](https://google.github.io/comprehensive-rust/traits/trait-bounds.html)
When working with generics, you often want to require the types to implement some trait, so that you can call this trait's methods.
```rust
// use clone
fn duplicate<T: Clone>(a: T) -> (T, T) {
    (a.clone(), a.clone())
}
// where syntax
fn duplicate<T>(a: T) -> (T, T)
where
    T: Clone,
{
    (a.clone(), a.clone())
}
```
#### impl Trait
[impl Trait - Comprehensive Rust 🦀](https://google.github.io/comprehensive-rust/traits/impl-trait.html)
`impl Trait` allows to work with types which you cannot name.
for parameter, it is like an anonymous generic parameter with a trait bound.
```rust
fn get_x(name: impl Display) -> impl Display {
    format!("Hello {name}")
}
```
#### Important, Standard Traits
- Copy, Clone (not the same thing)
- Cloning is a more general operation and also allows for custom behavior by implementing the Clone trait.
- Copying does not work on types that implement the Drop trait.

#### Sized
- `Sized` trait is implicitly added to all generic bounds in Rust unless explicitly opted out using the special syntax ?Sized.
- by default, generic functions in Rust work only on types whose size is known at compile time.
- If you want to be able to use a function with dynamically-sized types, you need to use a pointer like &T or Box<T> and specify `T: ?Sized`
- An unsized type is a type whose size is not known at compile time, such as a slice `[T]` or a trait object `dyn Trait`
- By using the `?Sized` marker, the definition of `Cow` can be made generic and flexible enough to work with both sized and unsized types.
- can't use Vec<T> or Box<T> with `T: ?Sized` because Rust needs to know how much memory to allocate for T.
- If you need to store a dynamically-sized type on the heap, you can use Box<dyn Trait> (a trait object)
```rust
fn function<T>(value: T) {
    // ...
}
// is equivalent to:
fn function<T: Sized>(value: T) {
    // ...
}
// accept references to dynamically-sized types. But note that even in this case, the &T itself is Sized
// it's a thin pointer that contains just enough information to refer to T, regardless of T's actual size.
fn function<T: ?Sized>(value: &T) {
    // ...
}
```

---
<!--ID:1688811538528-->
1. Explain trait 'Sized' and provide examples of types which are not 'Sized'.
> The Sized trait is an automatically implemented trait that indicates types with a constant size known at compile time.
> This trait is automatically added to types for which the size is known at compile time, and it is used as a bound for generic types by default.
> If type does not implement 'Sized', t has to be a reference because the compiler needs to know the size of all variables, and the size of a reference is always known.
> Most types in Rust are Sized.
>
> ```rust
> fn example<T>(t: T) { /* ... */ }
> // Even though we haven't written T: Sized, the function above is equivalent to:
> fn example<T: Sized>(t: T) { /* ... */ }
> // This is because Sized is a default constraint on T.
>
> // If we want T to be able to be a type that does not implement Sized (such as slices or trait objects), we have to explicitly opt out by writing T: ?Sized.
> fn example<T: ?Sized>(t: &T) { /* ... */ }
> ```
> Examples of types that are not Sized:
> - Box<dyn Trait> (a trait object)
> - slices (like [T], not to be confused with [T; N], which is Sized)
> - raw, unsized types (like str, not to be confused with &str, which is Sized).

---

##### Iterator


##### Read, Write
[Read and Write - Comprehensive Rust 🦀](https://google.github.io/comprehensive-rust/traits/read-write.html)
- abstract over u8 sources (Read) and sinks (Write)

#### From/Into
[From in std::convert - Rust](https://doc.rust-lang.org/std/convert/trait.From.html)
- for a type to define how to create itself from another type
- `as` can only be used in a small, fixed set of [transformations](https://doc.rust-lang.org/1.49.0/reference/expressions/operator-expr.html#type-cast-expressions)
- can be implemented for own types and is thus able to be applied in more situations.
- pairs with `Into. TryFrom and TryInto`
- only implemented for lossless conversions (e.g. you can convert from i32 to i64 with From, but not the other way around),
- `as` works for both lossless and lossy conversions (if the conversion is lossy, it truncates)

---
<!--ID:1695398050007-->
1. What is the difference between `From::from(e)` and `MyError::from(e)` ?
> The syntax `From::from(e)` is using the fully qualified syntax for associated functions in traits. In this form, you specify the trait name (From), followed by the associated function (from).
> This syntax is often used for disambiguation when the function name may coincide with other functions in the scope.
> However, you can indeed `use MyError::from(e)` if you prefer. This syntax relies on Rust's type inference to know that it should use the implementation of the From trait for the MyError type.
> 
> Both forms are equivalent when there's no ambiguity:
> `From::from(e)` -- Explicitly saying you want to use the From trait's from function.
> `MyError::from(e)` -- Relying on Rust's type inference to use the From trait implemented for MyError.
> The choice between the two generally depends on context and personal or project style guidelines.

<!--ID:1695398050008-->
1. What is an "associated function"?
> - associated with a type rather than an instance of that type.
> - defined within impl blocks for the type, and they don't take a self parameter.
> - similar to static functions in other programming languages.
> - are called using the trait/struct name and double colons: `let my_string = String::default();`

---

#### Trait Object (dyn)
- runtime value that represents any type that implements a particular trait (enum, struct)
- points to both an instance of a type implementing our specified trait and a table used to look up trait methods on that type at runtime.
- created by specifying some sort of pointer: `&` reference `Box<T>` smart pointer, then the `dyn` keyword
- can hold any value that implements the trait.
- The specific type of the value is determined at runtime
- form of [dynamic dispatch](https://doc.rust-lang.org/book/ch17-02-trait-objects.html#trait-objects-perform-dynamic-dispatch) in Rust, which allows to call methods on a value without knowing the specific type of the value at compile time.
```rust
// Reader: abstract over u8 sources
fn count_lines<R: Read>(reader: R) -> usize {
    let buf_reader = BufReader::new(reader);
    buf_reader.lines().count()
}
// Writer: abstract over u8 sinks
fn log<W: Write>(writer: &mut W, msg: &str) -> Result<()> {
    writer.write_all(msg.as_bytes())?;
    writer.write_all("\n".as_bytes())
}
```
##### Operators (Mult, Add...)
[Operators: Add, Mul, ... - Comprehensive Rust 🦀](https://google.github.io/comprehensive-rust/traits/operators.html)

##### Drop
[Drop - Comprehensive Rust 🦀](https://google.github.io/comprehensive-rust/traits/drop.html)

##### Default
- produces a default value for a type.
- It can be implemented directly or it can be derived via `#[derive(Default)]`.
- This means all types in the struct must implement Default too.

##### Dynamic Dispatch
Dynamic dispatch has a few trade-offs compared to static dispatch, which is the typical way Rust handles polymorphism:

- Performance:
    Dynamic dispatch can be slightly slower than static dispatch because it requires looking up function addresses at runtime
- Memory Usage:
        Trait objects like `Box<dyn Trait>` need to store a pointer to the data and a pointer to a vtable, a table of methods for the dynamic type
- Trait Limitations:
    Trait objects can only be constructed from traits that are object-safe. 
    This means the trait cannot include methods that reference the Self type (other than in box or reference form like `&self` or `Box<Self>`) 
    cannot require Sized, 
    cannot have generic methods.
- Lack of Compile-Time Checking

---
<!--ID:1695398050009-->
1. Explain dynamic vs static dispatch in Rust.
> In Rust, "dynamic dispatch" and "static dispatch" refer to two different ways that the compiler can resolve calls to methods or functions.
> ### Static Dispatch
> - occurs at **compile time**.
> - compiler knows the exact type that a method is being called on and therefore can directly call the method for that type.
> - Generics and traits with trait bounds often utilize static dispatch.
> - more performant because the method to call is determined at compile time, leading to a direct function call, and it allows for compiler optimizations like inlining.
> ```rust
> // Example using generics and trait bounds:
> trait Speak {
>     fn speak(&self);
> }
> 
> struct Dog;
> struct Cat;
> 
> impl Speak for Dog {
>     fn speak(&self) {
>         println!("Woof!");
>     }
> }
> 
> impl Speak for Cat {
>     fn speak(&self) {
>         println!("Meow!");
>     }
> }
> 
> fn animal_speak<T: Speak>(animal: T) {
>     animal.speak();
> }
> 
> fn main() {
>     let dog = Dog;
>     let cat = Cat;
> 
>     animal_speak(dog);  // Output: Woof!
>     animal_speak(cat);  // Output: Meow!
> }
> ```
> ### Dynamic Dispatch
> - occurs at runtime.
> - compiler doesn't know the exact type that a method is being called on, so it uses a vtable (virtual method table) to look up the method at runtime. 
> - Dynamic dispatch is used when you work with trait objects like `Box<dyn Trait>, &dyn Trait`.
> - comes with a runtime cost because of the vtable lookup, prohibits inlining
> ```rust
> // Example using trait objects:
> trait Speak {
>     fn speak(&self);
> }
> 
> struct Dog;
> struct Cat;
> 
> impl Speak for Dog {
>     fn speak(&self) {
>         println!("Woof!");
>     }
> }
> 
> impl Speak for Cat {
>     fn speak(&self) {
>         println!("Meow!");
>     }
> }
> 
> fn animal_speak(animal: &dyn Speak) {
>     animal.speak();
> }
> 
> fn main() {
>     let dog: Box<dyn Speak> = Box::new(Dog);
>     let cat: Box<dyn Speak> = Box::new(Cat);
> 
>     animal_speak(&*dog);  // Output: Woof!
>     animal_speak(&*cat);  // Output: Meow!
> }
> ```

<!--ID:1695398050010-->
1. What is the difference between `dyn Fn(&str), impl Fn(&str)`?
> ```rust
> // trait bound: static dispatch
> fn call_with_hello<F: Fn(&str)>(f: F) {
>     f("Hello");
> }
> // trait object: dynamic dispatch
> fn call_with_hello(f: &dyn Fn(&str)) {
>     f("Hello");
> }
> ```

---


#### Debug Implementation
```rust
use std::fmt;

struct Point {
    x: i32,
    y: i32,
}

impl fmt::Debug for Point {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "({}, {})", self.x, self.y)
    }
}

fn main() {
    let point = Point { x: 10, y: 20 };
    println!("{:?}", point);
}
```
#### Blanket Implementation
- way to implement a trait for a wide range of types in a single statement, rather than implementing the trait for each type individually
```rust
trait MyTrait {
    fn foo(&self);
}
// the implementation of MyTrait will apply to all types that implement the Copy trait.
impl<T> MyTrait for T where T: Copy {
    fn foo(&self) {
        println!("This is the default implementation of MyTrait for types that implement the Copy trait");
    }
}
```

## Method Idioms, Consistent Naming
- usually associated with types like Option or Result

### Combinators
or, or_else, or_default
or_insert, or_insert_with
unwrap_or, unwarp_or_default, unwrap_or_else

and, and_then
and_modify

map, map_ok, map_err, map_or_else
map_split, map_while

### try_
- return Result, can fail
try_new, try_from
try_find, try_fold

as_xxx: Convert to a reference of a different type, without taking ownership.
Example: str::as_bytes, Path::as_os_str.

to_xxx: Convert to a different type, often implying some form of ownership transfer or cloning.
Example: str::to_string, OsStr::to_str.

into_xxx: Convert into another type, consuming the original value. This idiom often signifies a transformation that takes ownership.
Example: Into::into, String::into_bytes.

is_xxx: Query methods that return a boolean to check if the object has a specific property or state.
Example: str::is_empty, Path::is_absolute.

with_xxx: Constructors or functions that initialize an object with a specific property or value.
Example: String::with_capacity.

from_xxx: Constructors or functions that create an instance of a type from another representation.
Example: String::from, Vec::from.

try_xxx: Methods or functions that might fail and return a Result type.
Example: fs::File::try_clone.

iter and into_iter: These idioms are about producing iterators. While iter() produces an iterator over references, into_iter() typically consumes the collection and produces an iterator over its items.
Example: Vec::iter, Vec::into_iter.

---
<!--ID:1691587766941-->
1. What does "checked" mean?
> refers to operations or methods that allow for explicit, non-panicking error handling.
> ```rust
> let x: u32 = u32::MAX;
> let result = x.checked_add(1); // result will be None because of overflow
> ```

---


## Static dispatch
- Emphasis on data over behavior. Aka, Rust is not an OOP language.
- The core idea of OOP is that of dynamic dispatch -- which code is invoked by a function call is decided at runtime (late binding).
- This is a powerful pattern which allows for flexible and extensible system.
- The problem is, extensibility is costly! It's better only to apply it in certain designated areas.
- Designing for extensibility by default is not cost effective.
- Rust puts static dispatch front and center: it is mostly clear whats going on by just reading the code, as it is independent of runtime types of the objects.


## Async
- async in Rust is multi-threaded programming with syntactic sugar.
- A Future may move between threads, so any variables used in async bodies must be able to travel between threads, i.e. trait `Send`.
- there are multiple async runtimes in Rust. Arguably, actix, async-std and tokio are the three most widely used


## Drop Trait, ContextManager Equivalent
- `Drop` defines a custom behavior to be run when an object goes out of scope. This can be used to implement the "enter-exit" behavior of a context manager.

Here's an example of how you might implement a simple context manager in Rust:
- FileContextManager can be used in a similar way to a context manager, by creating a new instance within a block of code and using it to access the File object.
- When the FileContextManager goes out of scope (at the end of the block), the custom behavior specified in the Drop trait implementation will be run.
```rust
use std::fs::File;
use std::io::{self, Write};

struct FileContextManager {
    file: File,
}

impl FileContextManager {
    fn new(path: &str) -> Result<Self, io::Error> {
        let file = File::create(path)?;
        Ok(Self { file })
    }
}

impl Drop for FileContextManager {
    fn drop(&mut self) {
        // This code will be run when the FileContextManager goes out of scope
        self.file.sync_all().unwrap();
    }
}

fn main() {
    let mut file_cm = FileContextManager::new("foo.txt").unwrap();
    writeln!(file_cm.file, "Hello, world!").unwrap();
    // The file will be synced and closed when file_cm goes out of scope here
}
```

## None, Option Handling

---
<!--ID:1692204458545-->
1. Which options do you have to get the value out of `Option` or default?
> ```rust
> let value = option.unwrap_or(3);  // more idiomatic
>
> let value = if let Some(x) = option {
>     x
> } else {
>     3
> };
> ```

---
```rust
match option {
    Some(x) => println!("The option is Some({})", x),
    None => println!("The option is None!"),
}

// if-let
fn print_string(s: Option<String>) {
    if let Some(value) = s {
        println!("{}", value);
    } else {
        println!("Value is None.");
    }
}

// work with a Option downstream (map, and_then)
let sorted_ids = ids.map(|mut v| {
   v.sort_by(|a, b| b.cmp(a));
   v  // !!!! Important to return v !!!!
}).unwrap();

// Use a default value: unwrap_or
fn option_unwrap_or() {
    let _port = std::env::var("PORT").ok().unwrap_or(String::from("8080"));
}

// Use a default Option value: or, config.port is an Option<String>
let _port = config.port.or(std::env::var("PORT").ok());
// _port is an Option<String>

// Call a function if Option is Some: and_then
fn port_to_address() -> Option<String> {
    // ...
}
let _address = std::env::var("PORT").ok().and_then(port_to_address);

// Call a function if Option is None: or_else
fn get_default_port() -> Option<String> {
    // ...
}
let _port = std::env::var("PORT").ok().or_else(get_default_port);

// is_some returns true if an Option is Some (contains a value):
let a: Option<u32> = Some(1);
if a.is_some() {
    println!("will be printed");
}

let b: Option<u32> = None;
if b.is_some() {
    println!("will NOT be printed");
}

let a: Option<u32> = Some(1);
if a.is_none() {
    println!("will NOT be printed");
}


let b: Option<u32> = None;
if b.is_none() {
    println!("will be printed");
}
```

---
<!--ID:1688831572218-->
1. How to change the value T inside and not Option itself: `mut Option<T>`
> `as_mut(&mut self) -> Option<&mut T>`
> Converts from &mut Option<T> to Option<&mut T>
> ```rust
> let mut x = Some(2);
> match x.as_mut() {
>     Some(v) => *v = 42,
>     None => {},
> }
> assert_eq!(x, Some(42));
> ```

---

## Error Handling
- The `?` operator can be used to propagate an error value up the call stack to the caller
- error values will always be string literals that have the `'static` lifetime
- panic: unrecoverable, [stack unwinding can be caught](https://google.github.io/comprehensive-rust/error-handling/panic-unwind.html)
- [aliases for Result - Rust By Example](https://doc.rust-lang.org/rust-by-example/error/result/result_alias.html)

---
<!--ID:1690561463834-->
1. Does `?` consume/move the Result?
> No, but an assignement does. It just extracts the `Ok` value or fails fast.
> ```rust
> // The ? operator does indeed "move" the String out of the Result into moved_result
> let r: Result<String, Err> = Ok("xxx".to_string());
> let moved_results = r?;
> ```

---

```rust
do_sth(bm).unwrap_or_else(|e| error!(e));  // logging

// function return
fn divide(a: i32, b: i32) -> Result<i32, String> {
    if b == 0 {
        return Err(String::from("Cannot divide by zero"));
    }
    Ok(a / b)
}

// match caller handling
let result = divide(10, 2);
match result {
    Ok(value) => println!("The result is: {}", value),
    Err(error) => println!("Error: {}", error),
}

// gracefull exit
build(&args).unwrap_or_else(|err| {
   println!("Problem parsing arguments: {err}");
   process::exit(1);
}

// General Idiom
fn run(config: Config) -> Result<(), Box<dyn Error>> {
    let contents = fs::read_to_string(config.file_path)?;  // return Error via ?
    Ok(())  // return Ok
}
if let Err(e) = run(config) {
   println!("Application error: {e}");
   process::exit(1);
}

// Convert a Result to an Option with ok:
fn result_ok() {
    let _port: Option<String> = std::env::var("PORT").ok();
}

// Use a default Result if Result is Err with or:
fn result_or() {
    let _port: Result<String, std::env::VarError> =
        std::env::var("PORT").or(Ok(String::from("8080")));
}

// map_err converts a Result<T, E> to a Result<T, F> by calling a function:
fn convert_error(err: ErrorType1) -> ErrorType2 {
    // ...
}
let _port: Result<String, ErrorType2> = std::env::var("PORT").map_err(convert_error);

// Call a function if Results is Ok: and_then.
fn port_to_address() -> Option<String> {
    // ...
}
let _address = std::env::var("PORT").and_then(port_to_address);

// Call a function and default value: map_or
let http_port = std::env::var("PORT")
    .map_or(Ok(String::from("8080")), |env_val| env_val.parse::<u16>())?;

// Chain a function if Result is Ok: map
let master_key = std::env::var("MASTER_KEY")
    .map_err(|_| env_not_found("MASTER_KEY"))
    .map(base64::decode)??;

// is_ok returns true if an Result is Ok:
if std::env::var("DOES_EXIST").is_ok() {
    println!("will be printed");
}
if std::env::var("DOES_NOT_EXIST").is_ok() {
    println!("will NOT be printed");
}

// is_err returns true if an Result is Err:
if std::env::var("DOES_NOT_EXIST").is_err() {
    println!("will be printed");
}
if std::env::var("DOES_EXIST").is_err() {
    println!("will NOT be printed");
}
```
### unwrap_or_else (Better)
- does not panic by itself.
- It is a method that provides a way to handle the error case of a Result in a way that avoids panicking.
- However, if the closure passed to unwrap_or_else itself panics, then the `unwrap_or_else` call will propagate that panic
```rust
fn main() {
    let greeting_file = File::open("hello.txt").unwrap_or_else(|error| {
        if error.kind() == ErrorKind::NotFound {
            File::create("hello.txt").unwrap_or_else(|error| {
                panic!("Problem creating the file: {:?}", error);
            })
        } else {
            panic!("Problem opening the file: {:?}", error);
        }
    });
}
```

### thiserror:
[Rust: Structuring and handling errors in 2020 - Nick's Blog and Digital Garden](https://nick.groenen.me/posts/rust-error-handling/#the-library-error-type)

---
<!--ID:1689137981113-->
1. How to use crate 'thiserror'?
> - create custom error types for libs (not binaries)
> - uses derive to generate implementation of trait `std::error::Error` based on custom error type's definition.
> ```rust
> use thiserror::Error;
> #[derive(Error, Debug)]
> pub enum MyError {
>     #[error("failed to read string from  {0}")]
>     ReadError(String),
>     #[error("unknown data: {data}")]
>     UnknownData { data: String },  // use named field
>     #[error(transparent)]
>     IOError(#[from] std::io::Error),  // automatically convert from std::io::Error into MyError, useful when using the ? operator.
>     // More variants...
> }
> ```

---

### anyhow:
[error handling with anyhow](https://antoinerr.github.io/blog-website/2023/01/28/rust-anyhow.html#why-anyhow)

---
<!--ID:1689137981114-->
1. How to use crate 'anyhow'?
> - provides flexible error handling for application code.
> - `anyhow::Result<V>` is a type alias for `Result<V, anyhow::Error>`.
> - `anyhow::Error` is essentially a wrapper around `Box<dyn Error>`, can hold any error type (hence the name 'anyhow').
> - use macros `bail, ensure` for early return
> - add `.with_context(), .context("..")?`
> - downcast to react on specific error type
> ```rust
> use anyhow::{Context, Result};
> fn main() -> Result<()> {
>     ...
>     it.detach().context("Failed to detach the important thing")?;
>
>     let content = std::fs::read(path)
>         .with_context(|| format!("Failed to read instrs from {}", path))?;  // enclosed path variable
>     ...
> }
> ```

---

#### Downcasting, Error Selection
[Matching on different Errors](https://doc.rust-lang.org/book/ch09-02-recoverable-errors-with-result.html#matching-on-different-errors)

---
<!--ID:1690561463835-->
1. How to downcast an error for specific error handling?
> ```rust
> // Match
> match todo {
>     Ok(todo) => { Ok(Some(todo)) }
>     Err(e) => match e.kind() {
>         DatabaseErrorKind::NotFound => {}
>         _ => {}
> }
> // if-let
> match result {
>     Ok(data) => { /* handle success */ },
>     Err(err) => {
>         if let DatabaseError(UniqueViolation, _) = err {
>             /* handle unique constraint violation */
>         } else {
>             /* handle general error */
>         }
>     }
> }
> // long
> let result = /* ... */;
> if let Err(DatabaseError(UniqueViolation, _)) = result {
>     /* handle unique constraint violation */
> } else if let Err(err) = result {
>     /* handle general error */
> } else {
>     /* handle success */
> }
> ```

---

## Reference, Pointer
- not smart, only adress, no metadata/functionality
- no ownership, only borrow data,
- &&i32
```rust
fn main() {
    let x = 5;
    let y = &x;
    let z = &&y;

    println!("x = {}", x);
    println!("y = {}", y);
    println!("z = {}", z);
}
```

## Smart Pointer

---
<!--ID:1692204458546-->
1. What is a smart pointer?
> What makes these pointers "smart" is their additional metadata and capabilities.
> They encapsulate not just the data they point to, but also behaviors around that data, ensuring various invariants (like memory safety, reference rules, or synchronization) are upheld.
> - typically come with ownership semantics (Box<T>, Arc<T>) or shared ownership semantics (Rc<T>),
> - can own the data they point to.
>
> Treating a Type Like a Reference by Implementing the `Deref` Trait:
> `*sp` is replaced with `*(sp.deref())`:
> - `deref()` method returns a reference, which can be dereferenced with `*`
> - If the deref method returned the value directly instead of a reference to the value, the value would be moved out of self.
> - We don't want to take ownership of the inner value inside MyBox<T>
>
> Here is a recap of the reasons to choose `Box<T>, Rc<T>, or RefCell<T>`:
> - Rc<T> enables multiple owners of the same data; Box<T> and RefCell<T> have single owners.
> - Box<T> allows immutable or mutable borrows checked at compile time;
> - Rc<T> allows only immutable borrows checked at compile time;
> - RefCell<T> allows immutable or mutable borrows checked at runtime.
> - Because RefCell<T> allows mutable borrows checked at runtime, you can mutate the value inside the RefCell<T> even when the RefCell<T> is immutable.

---

### Box
[Box - Comprehensive Rust 🦀](https://google.github.io/comprehensive-rust/std/box.html)

---
<!--ID:1688831572219-->
1. What is `Box` and what is difference to plain reference?
> - Both `Box<T>` and `&T` allow to refer to data that is not stored in the current stack frame
> - Box has ownership, does not need another owner
> - `Box<T>` type is a smart pointer because it implements `Deref` trait, which allows values to be treated like references.
> - implements `Deref<Target = T>`, which means that you can call methods from `T` directly on `Box<T>`.
> - When a Box<T> value goes out of scope, the heap data that the box is pointing to is cleaned up as well because of the Drop trait implementation
> ```rust
> fn main() {
>     let x = 5;
>     let y = Box::new(x);  // Box pointing to copied x-value rather than a reference pointing to the value of x
>     let z = *x;
>
>     assert_eq!(5, x);
>     assert_eq!(5, *y);
>     assert_eq!(5, *z);
> }
> ```
>
> 1. **Ownership and Lifetimes**: `Box<T>` indicates ownership. On the other hand, `&T` does not own the data it points to. The data referred to by a `&T` must be owned by something else and must live at least as long as the reference itself.
>
> 2. **Use Cases**: `Box<T>` is generally used to allocate data on the heap, or when you want to transfer ownership of data, for example, to return data from a function or to store data in a data structure. 
> `&T` is used when you want to borrow data, i.e., have a temporary, read-only view into some data without taking ownership of it.
>
> 3. **Sizedness**: `Box<T>` requires `T` to be Sized (i.e., its size is known at compile time), but `&T` can refer to types that are not Sized.

<!--ID:1689137981115-->
1. What are use-cases for Box?
> - have a type whose size that can't be known at compile time, but the Rust compiler wants to know an exact size.
> - want to transfer ownership of a large amount of data. To avoid copying large amounts of data on the stack, instead store the data on the heap in a Box so only the pointer is moved.

---

### Rc reference-count
[Rc - Comprehensive Rust 🦀](https://google.github.io/comprehensive-rust/std/rc.html)
It is generally not possible to create cyclic data structures using references in Rust because it would create a reference cycle that would prevent the values from being dropped when they are no longer needed.
- Rc lets us create cyclic data structure by using reference counting to keep track of the number of references to each value.
- Rc reference owns a so called 'inner value'.
- we can clone borrowed references to Rc references and thus can have many such clones referring to the same Rc's inner value.


```rust
let ref = Rc::new(value); // moves 'value' into Rc
let clone1 = Rc::clone(&ref); // create a clone of a reference
let clone2 = Rc::clone(&ref); // creates another clone
```
If we just had moved the shared value into one of the others, and had provided a borrowed reference to the others, the compiler would have complained for not being able to ensure the reference to always point to a still existing value. For instance, the new owner of the moved value could be dropped somewhere without the borrowed reference being aware of it.

---
<!--ID:1689137981116-->
1. What is Rc<T>?
> - immutable shared reference (despite ownership)
> - multiple ownership of a value, shared.
> - `Rc::clone` doesn't make a deep copy of all the data like most types' implementations of clone do (cheap)
> - use-case: share data between multiple parts of program

---

### Arc
[Arc in std::sync - Rust](https://doc.rust-lang.org/std/sync/struct.Arc.html)
- provides shared ownership of a value of type T, allocated in the heap.
- Invoking clone on Arc produces a new Arc instance, which points to the same allocation on the heap as the source Arc, while increasing a reference count.
- When the last Arc pointer to a given allocation is destroyed, the value stored in that allocation (often referred to as "inner value") is also dropped.
- Shared references in Rust disallow mutation by default, and Arc is no exception: you cannot generally obtain a mutable reference to something inside an Arc


### RefCell<T> and the Interior Mutability Pattern
- RefCell and Cell are both types in Rust that allow you to have interior mutability, which means you can change the value of a variable that is otherwise immutable.
- type that provides more flexible and powerful interior mutability for values that are stored in the heap.
- Unlike Cell, it can be used to mutate values of any type, not just types that implement the Copy trait.
- enforces the borrowing rules at runtime instead of compile time
- uses a runtime borrowing mechanism for ensuring that you don't violate the rules of interior mutability, and it provides protection against data races and other synchronization issues.
- more expensive than Cell in terms of performance and runtime overhead.
- Similar to Rc<T>, RefCell<T> is only for use in single-threaded scenarios and will give you a compile-time error if you try using it in a multithreaded context.

#### Interior Mutability

---
<!--ID:1692204458547-->
1. Explain the 'Interior Mutability' Pattern.
> The interior mutability pattern in Rust is a design pattern that allows to mutate data even when you have an immutable reference to that data.
>
> ### Why is it needed?
> there are cases where modifying data through an immutable reference is beneficial, especially when:
> - Concurrency: For safe concurrent modifications, sometimes you need to modify shared state. Rust's borrowing rules make this difficult to do safely without interior mutability.
> - Lazy Initialization: When you need to initialize data lazily and the object is otherwise immutable.
> - Caching/Memoization: When you want to cache results in an immutable structure for performance optimization.
> - Implementation Details: Sometimes, an object needs to maintain internal state that changes even when the object is logically immutable.
>
> #### `Cell<T>`
> - For single-threaded scenarios.
> - Offers `get` and `set` methods for data operations.
> - Works only with `Copy` types.
>
> #### `RefCell<T>`
> - For single-threaded scenarios.
> - Provides `borrow` and `borrow_mut` methods to obtain immutable or mutable references to contained data.
> - Enforces Rust's borrowing rules at runtime. A program will panic if rules are violated.
>
> #### `Mutex<T>`
> - Provides locked access to data, ensuring one-thread-at-a-time mutation.
>
> #### `RwLock<T>`
> - Allows multiple threads to read the data, but only one thread can write simultaneously.
> 
> #### Atomic Types: 
> - For lock-free, thread-safe programming.
> ```rust
> use std::sync::atomic::{AtomicUsize, Ordering};
> let x = AtomicUsize::new(0);
> x.store(5, Ordering::SeqCst);
> ```
> 
> #### OnceCell/Lazy:
> For lazy initialization and one-time assignment.
> ```rust
> use once_cell::sync::OnceCell;
> static CELL: OnceCell<String> = OnceCell::new();
> ```
> ### Safety
> Safety of interior mutability is ensured via:
> - **Compile-time checks**: Rust's borrowing rules are verified at compile time.
> - **Runtime checks**: Types like `RefCell<T>` check borrowing rules during runtime. If violated, the program panics.
> - **Synchronization**: Types such as `Mutex<T>` and `RwLock<T>` synchronize access to ensure safety during concurrent operations.

---


### Cell
- A mutable memory location.
- enables mutation inside an immutable struct. In other words, it enables "interior mutability".
- type that provides simple and cheap interior mutability for values that are stored in the stack.
- It can be used to mutate values of any type that implements the Copy trait, which includes types like integers and floating-point numbers.
- Cell uses a simple type-based mechanism for ensuring that you don't violate the rules of interior mutability, but it does not provide any protection against data races or other synchronization issues.
- In general, if you need to mutate a value that is stored in the stack, you should use Cell, as it is the simpler and more efficient option.


### Cow
- providing clone-on-write functionality:
- can enclose and provide immutable access to borrowed data, and clone the data lazily when mutation or ownership is required.
- The type is designed to work with general borrowed data via the Borrow trait.


## Implicit Deref Coercion
Rust does deref coercion when it finds types and trait implementations in three cases:
1. From &T to &U when T: Deref<Target=U>
2. From &mut T to &mut U when T: DerefMut<Target=U>
3. From &mut T to &U when T: Deref<Target=U>
first case states that if you have a `&t`, and t implements `deref` to some type `U`, you can get a `&U` transparently.
third case is trickier: Rust will also coerce a mutable reference to an immutable one.
But the reverse is not possible: immutable references will never coerce to mutable references.
Because of the borrowing rules, if you have a mutable reference, that mutable reference must be the only reference to that data (otherwise, the program wouldn't compile).
Converting one mutable reference to one immutable reference will never break the borrowing rules.
When a type implements Deref<Target = T>, the compiler will let you transparently call methods from T

## Drop
avoid double free error
you have to call the `std::mem::drop` function if you want to force a value to be dropped before the end of its scope
ownership system ensures that drop gets called only once when the value is no longer being used.


## Downcasting
is the process of converting a value of a parent type (e.g. a trait) to a value of a child type (e.g. an implementation of that trait).
the `downcast_ref` method is used to downcast a value of the parent type `Error` to a value of the child type `DataStoreError`.
The `downcast_ref` method is a method provided by the `std::any::Any` trait, which is implemented by the `Error` trait.
This method returns an Option containing a reference to the child type, if the value is of that child type. If the value is not of that child type, it returns None.
```rust
// If the error was caused by redaction, then return a tombstone instead of the content.
match root_cause.downcast_ref::<DataStoreError>() {
    Some(DataStoreError::Censored(_)) => Ok(Poll::Ready(REDACTED_CONTENT)),
    None => Err(error),
}


## How Do Raw Pointers Work?
Raw pointers in Rust (*const T and *mut T) behave a lot like pointers in languages like C or C++:

Dereferencing: To access the data a raw pointer points to, you need to dereference it. In Rust, dereferencing raw pointers is unsafe because the compiler can't guarantee the memory's validity.

No Automatic Cleanup: Raw pointers don't have any cleanup mechanism like Box or Rc. This means you're responsible for ensuring that the memory the pointer points to is correctly managed.

No Borrow Checks: Raw pointers don't participate in Rust's borrowing system. You can have multiple mutable raw pointers to the same data, and it's up to you to ensure you don't cause data races or other undefined behaviors.

Creating from References: You can create raw pointers from standard references, allowing you to bypass some of Rust's safety guarantees.

Here's a basic example:

```rust
let x = 5;
let r = &x;  // A regular reference
let raw = r as *const i32;  // Convert to a raw pointer

unsafe {
    assert!(*raw == 5);  // Dereference the raw pointer inside an unsafe block
}
```
Risks and Precautions:
Raw pointers are inherently unsafe:

Dangling Pointers: If the data a raw pointer references is dropped or moved, the pointer can dangle, leading to undefined behavior if dereferenced.
Uninitialized and Null Pointers: Raw pointers can be uninitialized or null, and trying to access them can lead to undefined behavior.
Data Races: Since raw pointers bypass Rust's borrowing rules, you can end up with data races if you're not careful.
Due to these risks, Rust mandates the use of the unsafe keyword when performing operations with raw pointers, like dereferencing. This is a signal that the programmer needs to manually uphold Rust's safety guarantees.

In conclusion, while raw pointers can offer solutions to certain complex problems, especially when dealing with intricate data structures or interfacing with other languages, they come with significant risks. It's essential to be aware of these risks and use them judiciously, and when possible, look for safer alternatives.

```
## OO
### Inheritance
- no inheritance


# Data Types, Structures ..........................................................................
- primitive types are stored on the stack
- Constant cannot be shadowed

## Type Hint/Specification for compiler
if compile cannot infer the type:
1. specifiy type at variable definition
2. turbofish: `::<T>` is a way to specify the type of a generic value, when the type cannot be inferred from context.
    It allows to specify the type of a generic value by adding `::<Type>` after the value.
```rust
let x = vec![1, 2, 3];
let y = x.iter().sum::<i32>();
```
- `fn collect<B>(self) -> B ` allows turbofish due to generic
- `fn into(self) -> T` does not allow turbofish (no generics)
- think of the things inside `( . )` to be the “value arguments” to a function and the things inside `::< . >` to be “type arguments”.

## Numbers
Integers: If a specific type is expected, then they can become u64, i8, or whatever else - but if not, it defaults to i32.
Floating point literals (like 0.0) will default to f64

## String
- is an owned, heap-allocated, growable sequence of characters.
- It's a more complex type that includes the length, capacity, and a pointer to the heap memory.

### Scope, Ownership, Borrowing,  String vs &str
- difference is that `String` is a owned string type, while `&str` is a borrowed string type.
- This means that when you have a `Vec<String>`, the vector owns the strings and is responsible for freeing the memory
- `Vec<String>` is more convenient to use because you don't have to worry about managing the lifetime of the strings yourself.
- `Vec<&str>` more efficient because it avoids copying the strings into the vector.
```rust
// Wrong: "replace" method returns a 'temporary', which is dropped at block's end and cannot be used in trim
let tags = bm.tags.replace(",", " ").trim();
// Correct: allokate memory in outer block
let tags = bm.tags.clone().replace(",", " ");
```

---
<!--ID:1688811538529-->
1. `let s = String::from("Hello, World!")[1..2];` gives 'cannot move'. Why?
> Rust doesn't allow it because the indexing syntax [] attempts to move a temporary value. Here's what's happening in your line of code:
>
> `String::from("Hello, World!")` creates a new (tmp) String.
> The `[1..2]` attempts to slice this String (not allowed, because of UTF-8 encoding)
> The problem is that the new String is a temporary value.
> 1. In Rust, you cannot take a slice of a temporary value because the value will be deallocated immediately, and the slice would reference deallocated memory.
> 2. indexing is not allowed directly on String because it is UTF-8 encoded, i.e variable-width encoding
> ```rust
> // To fix this, you need to bind the String to a variable before slicing it:
> let s = String::from("Hello, World!");
> let s2 = &s[1..2];
> ```
> This way, the String s is not a temporary value, so it's safe to take a (byte!) slice, which is stored in s2.
>
> Remember that the indices in slicing refer to bytes, not characters.
> Be careful when working with Unicode strings, because a single character can span multiple bytes.
> Attempting to create a slice in the middle of a character will cause a panic at runtime.

<!--ID:1690777097438-->
1. How to convert from `&String` to `&str`?
> Given `entry` is `&String`
> `&*entry` is a way to convert a type to a type that implements the same trait, but with a different ownership. In this case, it's used to convert from &String to &str.
>
> Let's break it down:
> `*entry` is dereferencing entry to get the String value it points to. This is because entry is a reference (&String), so we need to dereference it to get the underlying String.
> `&*entry` is then taking a reference to that String, giving us a &str.
> The `&*` pattern takes advantage of Rust's deref coercion to turn the `&String` into a `&str`.
> the dereference acs as an "interruption" that gives Rust another context which requires it to decide type: apply Deref coercion

<!--ID:1694674317665-->
1. What is the difference betwen `&String` and `&*&String`?
> The difference in outcome arises from the context in which the `&` operator is applied
> 
> 1. **Direct Reference (`let e = &"xxx".to_string();`)**:
>    - `"xxx".to_string()` produces a `String`.
>    - When you take a reference directly using `&`, there is no context provided that would push Rust to treat it as anything other than a `&String`. It's a direct reference to a `String` object, so you get a `&String`.
> 
> 2. **Dereference, then Reference (`let s = &*e;`)**:
>    - `*e` first dereferences the `&String`, essentially accessing the underlying `String`.
>    - The subsequent `&` then takes a reference. Given that there's been an explicit dereference already, this isn't just a direct reference anymore. Instead, Rust has to decide what the resulting type of the reference should be.
>    - Due to `Deref` implementation for `String`, which returns a `str`, and given the preceding dereference context, Rust chooses to give a `&str`.
> 
> In essence, the intermediate dereferencing in the second scenario gives Rust an "opportunity" to apply the `Deref` trait when subsequently re-referencing, whereas the direct reference in the first scenario does not.

---

### Test for Whitespace
```rust
use regex::Regex;

fn main() {
    let s = "mystring";
    let re = Regex::new(r"\S").unwrap();

    if re.is_match(s) {
        println!("The string contains a non-whitespace character.");
    } else {
        println!("The string contains only whitespace characters.");
    }

    if s.find(|c:char| !c.is_whitespace()).is_some() {
        println!("The string contains a non-whitespace character.");
    } else {
        println!("The string contains only whitespace characters.");
    }
}
```

### Multiline, RawString
- [GitHub - dtolnay/indoc: Indented document literals for Rust](https://github.com/dtolnay/indoc)
- string literals can be broken across several lines
```rust
let s = "This is a string
that spans multiple
lines.";
let string = "multiple\n\
              lines\n\
              with\n\
              indentation";

// You can also use the include_str! macro to include a multiline string from a file:
let s = include_str!("file.txt");

// these multiline strings do not interpret any escape sequences, so you will need to use raw strings if you want to include characters like \n in your string. To create a raw string, you can use triple quotes with an r before the opening quote:
let shader = r#"
    #version 330

    in vec4 v_color;
    out vec4 color;

    void main() {
        color = v_color;
    };
"#;

// If you have sequences of double quotes and hash symbols within your string, you can denote an arbitrary number of hashes as a delimiter:
let crazy_raw_string = r###"
    My fingers #"
    can#"#t stop "#"" hitting
    hash##"#
"###;
```
### String Templates

---
<!--ID:1692204458548-->
1. What are 'String Templates'?
> ```rust
> let s = format!(
>     "This is a
>      multi-line string
>      template. It allows
>      you to write string
>      templates that span
>      multiple lines.");
>
> let s = format!("{0} + {1} = {2}", "1", "1", 2);
>
> let s = format!("{arg1} + {arg2} = {result}", arg1=1, arg2=1, result=2);
> ```

---

## Enum
- way to define ONE type with a fixed set of possible values/variants.
- A tag/discriminant is synonym for variant
- variants can carry additional information/fields
- can have `impl` function block
- when having a value of type WebEvent, it must be one of the defined variants
```rust
#[derive(Debug)]
enum WebEvent {
    PageLoad,                 // Variant without payload
    KeyPress(char),           // Tuple struct variant
    Click { x: i64, y: i64 }, // Full struct variant
}
#[rustfmt::skip]
fn inspect(event: WebEvent) {
    match event {  // extract data from variants
        // The values in the enum variants can only be accessed after being pattern matched.
        // The pattern binds references to the fields in the “match arm” after the =>
        WebEvent::PageLoad       => println!("page loaded"),
        WebEvent::KeyPress(c)    => println!("pressed '{c}'"),
        WebEvent::Click { x, y } => println!("clicked at x={x}, y={y}"),
    }
}
fn main() {
    let load = WebEvent::PageLoad;  // is variable of type WebEvent and tag PageLoad
    let press = WebEvent::KeyPress('x');
    let click = WebEvent::Click { x: 20, y: 80 };  // is WebEvent, specifically a Click and carries fields

    inspect(load);
    inspect(press);
    inspect(click);
}
```

## Struct
- no inheritance
- field mutability determined by struct
- associated methods: don't need to be called with an instance, used as ctor
- It is common and expected for types to implement both `Default` and an empty `new` constructor.
- should OWN their members (no ref/borrows -> lifetime parameter required)
- no default value, but `Default` trait
```rust
#[derive(Debug)]
struct Person {
    name: String,
    age: u8,
}
impl Person {
    fn new(name: String, age: u8) -> Self {  // ctor
        Self { name, age }  // shorthand syntax
    }
}
impl Default for Person {  // Default trait
    fn default() -> Person {
        Person {
            name: "Bot".to_string(),
            age: 0,
        }
    }
}
fn create_default() {
    let tmp = Person {
        ..Default::default()  // multiple values
    };
    let tmp = Person {
        name: "Sam".to_string(),
        ..Default::default()
    };
}
```

### Zero Size
- only traits matter, no data


### Tuple Struct, Named Tuple, single-field wrappers (called newtypes)
The main difference between tuple structs and classic (or C-style) structs is that the latter have named fields, whereas the former do not.
Tuple structs are useful when you want to bundle together some values and give them a name for type checking, but you don't necessarily care about naming each individual part
```rust
struct PoundsOfForce(f64);  // newtype

struct Color(i32, i32, i32);
let black = Color(0, 0, 0);
println!("Red is: {}", black.0);
println!("Green is: {}", black.1);
println!("Blue is: {}", black.2);
```
### Getter/Setter
```rust
struct Example {
    x: i32,  // private field
}

impl Example {
    pub fn new(x: i32) -> Example {
        Example { x }
    }

    pub fn get_x(&self) -> i32 {
        self.x
    }

    pub fn set_x(&mut self, x: i32) {
        self.x = x;
    }
}

// "field accessors" or "field methods".
impl Example {
    pub fn new(x: i32) -> Example {
        Example { x }
    }

    pub fn x(&self) -> i32 {
        self.x
    }

    pub fn set_x(&mut self, x: i32) {
        self.x = x;
    }
}

// Usage
let mut example = Example::new(5);
let x = example.get_x();
let x = example.x();
example.set_x(10);
```

### Attributes .....................................................................................
Debug       : enables the use of the {:?} or {:#?} debug format specifier
Clone       : enables the use of the .clone() method to create a copy of the struct
Copy        : enables the use of the struct in a "copy" semantic rather than "move" semantic
Eq          : enables the use of the == operator to compare struct instances for equality
PartialEq   : enables the use of the <, >, <=, >= operators to compare struct instances
Hash        : enables the use of the struct as a key in a hash map or a hash set.
Ord         : enables the use of the <, >, <=, >= operators to compare struct instances
PartialOrd  : enables the use of the <, >, <=, >= operators to compare struct instances
Default     : enables the use of the Default::default() method to create a default-initialized instance of the struct.

### Returning a struct
- Sometimes, a function may return several possible structs, which occurs when several structs implement the same trait.
- To write this type of function, just type the return value of a struct that implements the desired trait.
- use the Box type for the return value, which allows us to allocate enough memory for any struct implementing the Pet trait.
- We can define a function that returns any type of Pet struct in our function as long as we wrap it in a new Box.
```rust
// We dynamically return Pet inside a Box object
fn new_pet(species: &str, name: String) -> Box<dyn Pet> {
```

## Methods
[Method Receiver - Comprehensive Rust 🦀](https://google.github.io/comprehensive-rust/methods/receiver.html)
- special wrapper types can be method receivers, e.g. Box, Rc, Arc
```rust
#[derive(Debug)]
struct Race {
    name: String,
    laps: Vec<i32>,
}
impl Race {
    fn new(name: &str) -> Race {  // No receiver, a static method
        Race { name: String::from(name), laps: Vec::new() }
    }
    fn add_lap(&mut self, lap: i32) {  // Exclusive borrowed read-write access to self
        self.laps.push(lap);
    }
    fn print_laps(&self) {  // Shared and read-only borrowed access to self
        println!("Recorded {} laps for {}:", self.laps.len(), self.name);
        for (idx, lap) in self.laps.iter().enumerate() {
            println!("Lap {idx}: {lap} sec");
        }
    }
    fn finish(self) {  // Exclusive ownership of self
        let total = self.laps.iter().sum::<i32>();
        println!("Race {} is finished, total lap time: {}", self.name, total);
    }
}
fn main() {
    let mut race = Race::new("Monaco Grand Prix");
    race.add_lap(70);
    race.add_lap(68);
    race.print_laps();
    race.add_lap(71);
    race.print_laps();
    race.finish();
    // race.add_lap(42);
}
```


## range
```rust
// exclusive
let range = std::ops::Range { start: 0, end: 10 };
let range = 0..10;
// inclsuive
let range = std::ops::RangeInclusive::new(0, 10);
let range = 0..=10;
```


## Lists
```rust
// check el is in list
fn main() {
    let list1 = [1, 2, 3];
    let list2 = [3, 4, 5];

    for element in list1 {
        if list2.contains(&element) {
            println!("Element {} is in both lists.", element);
        }
    }
}
fn main() {
    let list1 = [1, 2, 3];
    let list2 = [3, 4, 5];

    if list1.iter().any(|&x| list2.contains(&x)) {
        println!("There is an element common to both lists.");
    }
}
// check on list is in other list
use std::collections::HashSet;

fn main() {
    let list1: HashSet<i32> = [1, 2, 3].iter().cloned().collect();  // convert to HashSets
    let list2: HashSet<i32> = [1, 2, 3, 4].iter().cloned().collect();

    if list1.is_subset(&list2) {
        println!("List 1 is subset of list 2.");
    } else {
        println!("List 1 is not subset of list 2.");
    }
}
```
## Collections, Vector
- get iterator via `.iter()`, `.iter_mut()`, orrowed iterator. Here key and value variables are references
- consume: `iter_into` owned iterator: the collection is moved, and you can no longer use the original variable
- `vec!(), vec![]`
- chaining instead of for..in has the advantage of working with immutable data
```rust
// mutating while loopoing
let mut vec = vec![1, 2, 3];
for x in vec.iter_mut() {
    *x += 1;
} // vec is now [2, 3, 4]
for (i, x) in vec.enumerate() {
    vec[i] = x + 1;
}

// looping over Dict
for (key, value) in map.iter() {
    println!("key: {} value: {}", key, value);
}

// create new vec based on fields from struct
fn main() {
    let mut v = Vec::new();

    let points = vec![
        Point { x: 1, y: 2 },
        Point { x: 3, y: 4 },
        Point { x: 5, y: 6 },
    ];

    for p in points {  // moves p
        v.push(p);
    }
    println!("{:?}", v);

    // let mut xs = Vec::new();
    // for p in v {
    //     xs.push(p.x);  // moves p
    // }
    let xs: Vec<i32> = v.iter().map(|p| p.x).collect();

    println!("{:?}", xs);
}
```
### Combinators
#### inspect the values flowing through an iterator

---
<!--ID:1701417632209-->
1. How to see values flowing through an iterator?
> ```rust
> fn inspect() {
>     let v = vec![-1, 2, -3, 4, 5].into_iter();
> 
>     let _positive_numbers: Vec<i32> = v
>         .inspect(|x| println!("Before filter: {}", x))
>         .filter(|x: &i32| x.is_positive())
>         .inspect(|x| println!("After filter: {}", x))
>         .collect();
> }
> ```

---

```rust
// chain
fn chain() {
    let x = vec![1, 2, 3, 4, 5].into_iter();
    let y = vec![6, 7, 8, 9, 10].into_iter();

    let z: Vec<u64> = x.chain(y).collect();
    assert_eq!(z.len(), 10);
}
```
### Vec<String> from Vec<&str>
```rust
let strs = vec!["a", "b", "c"];
let strings: Vec<String> = strs.into_iter().map(String::from).collect();
println!("{:?}", strings)
```

### Set
```rust
use std::collections::HashSet;

let words = vec!["apple", "banana", "cherry"];
let set: HashSet<&str> = words.iter().collect();
let set: HashSet<&str> = HashSet::from_iter(words.iter());
// set now contains ["apple", "banana", "cherry"]

// create HashSet by iterating over iterator and dereferencing each element before collecting it into the set.
// This allows you to create the HashSet without borrowing the iterator.
let set: HashSet<&str> = iterator.map(|s| *s).collect();
```


## Singleton
### immutable
```rust
// creates global static variable named SINGLETON that is initialized with a new instance of the Singleton struct when it is first accessed.
// The clone method is used to create a copy of the singleton, because the lazy_static crate stores the singleton as an Arc
// (atomic reference counted) smart pointer, which is a type of data structure that allows multiple owners of the same data.
use lazy_static::lazy_static;
struct Singleton { // fields go here }
impl Singleton {
    fn new() -> Self {
        // return a new instance of the singleton
    }
}
lazy_static! {
    static ref SINGLETON: Singleton = Singleton::new();
}

fn main() {
    let singleton = SINGLETON.clone();
    // use the singleton
}
```
### mutable
```rust
// creates a static mutable variable named SINGLETON and a Once object named INIT.
// call_once method of the Once object is used to initialize the SINGLETON variable with a new instance of the Singleton struct the first time it is called.
use std::sync::{Once, ONCE_INIT};
struct Singleton { // fields go here }
impl Singleton {
    fn new() -> Self {
        // return a new instance of the singleton
    }
}

static mut SINGLETON: Option<Singleton> = None;
static INIT: Once = ONCE_INIT;

fn main() {
    INIT.call_once(|| {
        unsafe {
            SINGLETON = Some(Singleton::new());
        }
    });
    let singleton = unsafe { SINGLETON.as_ref().unwrap() };
    // use the singleton
}
```
## Datetime
```rust
extern crate chrono;
use chrono::{Utc, TimeZone, DateTime};
use chrono::{NaiveDate, NaiveDateTime};

fn main() {
   // format YYYY-MM-DDTHH:MM:SSZ
    let now = Utc::now();
    println!("The current UTC time is: {}", now);

    let formatted_time = now.format("%Y-%m-%d %H:%M:%S").to_string();
    println!("The current UTC time is: {}", formatted_time);

   // NaiveDateTime is commonly created from NaiveDate.
   let dt: NaiveDateTime = NaiveDate::from_ymd_opt(2016, 7, 8).unwrap().and_hms_opt(9, 10, 11).unwrap();
}

```
## Function Type
### Closures
[Closures: Fn, FnMut, FnOnce - Comprehensive Rust 🦀](https://google.github.io/comprehensive-rust/traits/closures.html)
- Closures or lambda expressions have types which cannot be named.
- However, they implement special `Fn, FnMut, FnOnce` traits:
- can return values like functions
- by default borrow stuff that they close over, but you can move that stuff to the closure instead with the move keyword. If I understand correctly, it's an all-or-nothing move; no mix and match.
```rust
// impl Trait
fn apply_with_log(func: impl FnOnce(i32) -> i32, input: i32) -> i32 {
    println!("Calling function on {input}");
    func(input)
}

let mut count = 0;  // captured
let mut inc = || {
    count += 1;
    println!("count = {}", count);
};
inc();
inc();
assert_eq!(2, count);
```

---
<!--ID:1689137981117-->
1. What Traits implement Closures/Lamdas?
> `Fn` neither consumes nor mutates captured values. It can be called multiple times concurrently.
> `FnMut` (e.g. accumulate) might mutate captured values. You can call it multiple times, but not concurrently.
> `FnOnce` may only call it once. It might consume captured values.
> ```rust
> fn call_function<F: Fn()>(f: F) {
>     f();
> }
> fn main() {
>     let x = 10;
>     let y = 20;
>     // Pass a closure as a parameter to the `call_function` function
>     call_function(|| {
>         println!("x + y = {}", x + y);
>     });
> }
> ```
<!--ID:1689137981118-->
2. How do Closures capture (by value or by reference)?
> capture by reference. The move keyword makes them capture by value.
> ```rust
> fn make_greeter(prefix: String) -> impl Fn(&str) {
>     return move |name| println!("{} {}", prefix, name)
> }
> fn main() {
>     let hi = make_greeter("Hi".to_string());
>     hi("there");
> }
> ```
> to force the closure to take ownership of *any* referenced variables, use the `move` keyword 
>
> `impl Fn(&str)` is a type signature that indicates a type implementing the Fn trait (no trait object!), taking a borrowed string as an argument.
> The Fn trait is one of the three function traits (`Fn, FnMut, FnOnce`) to represent closures or function pointers
<!--ID:1698125271968-->
1. Explain the difference:
```rust
fn call_function<F: Fn()>(f: F) {
    f();
}
fn call_function(f: fn()) {
    f();
}
```
> First version is trait based, sedond uses function pointer.
> This approach is less flexible compared to using the Fn trait because it won't accept closures that capture their environment;
> it only accepts standalone functions and closures without captures.

---

### Function Pointer Syntax:

---
<!--ID:1689137981119-->
1. how to pass a functiona as parameter (fn pointer syntax)?
> You can pass a function as a parameter by using the function pointer syntax, which is fn(args) -> return_type.
> ```rust
> fn call_function(f: fn(i32) -> i32, x: i32) -> i32 {
>     f(x)
> }
> fn main() {
>     // Pass the `add_one` function as a parameter to the `call_function` function
>     let result = call_function(add_one, 10);
>     println!("Result: {}", result);
> }
> fn add_one(x: i32) -> i32 {
>     x + 1
> }
> ```

---

## Conversion
```rust
// as
let i: i32 = 10;
let u: usize = i as usize;

// TryInto trait from the std::convert
let i: i32 = 10;
let u: usize = i.try_into().unwrap();
// parse
```

## Tree
[rust_tree.md]($VIMWIKI_PATH/dev/rust_tree.md)



# Control Flow .....................................................................................
[Control Flow - Comprehensive Rust 🦀](https://google.github.io/comprehensive-rust/control-flow.html)
## Block
- has a value and a type, which are those of the last expression of the block
- If the last expression ends with ;, then the resulting value and type is ().
```rust
fn main() {
    let x = {
        let y = 10;
        println!("y: {y}");
        let z = {
            let w = {
                3 + 4
            };
            println!("w: {w}");
            y * w
        };
        println!("z: {z}");
        z - y
    };
    println!("x: {x}");
}
```
## if expression
- because if is an expression and must have a particular type, both of its branch blocks must have the same type.
```rust
fn main() {
    let mut x = 10;
    if x % 2 == 0 {
        x = x / 2;
    } else {
        x = 3 * x + 1;
    }
}
// equivalent as expression (extract x)
fn main() {
    let mut x = 10;
    x = if x % 2 == 0 {
        x / 2
    } else {
        3 * x + 1
    };
}
```
### if-let, if let
- lets you execute different code depending on whether a value matches a pattern
- shorthand for a match statement that only has one arm, need not be exhaustive
- refutable, does not match `None`
- extract the value from an `Option` or a `Result` and bind it to a variable, and then execute a block of code only if the value is `Some` or `Ok`.
- works for enum types
```rust
// the if-let statement extracts the value from the x variable, which has the type Option<i32>.
// If x is Some, the value is bound to the value variable, and the block of code inside the if block is executed.
let optional = Some(42);
if let Some(value) = optional {
    // ^^^^^^^^^^ pattern to match
    println!("optional is Some, and its value is {}", value);
}
// with else
if let Some(value) = x {
    println!("x has a value of {}", value);
} else {
    println!("x is None");
}
// multiple if-let
if let Some(value) = x {
    println!("x has a value of {}", value);
} else if let None = x {
    println!("x is None");
}

// extract result OK
let x: Result<i32, String> = Ok(42);
if let Ok(value) = x {
    println!("x is Ok, and its value is {}", value);
}
```

## Loops, Iterator

---
<!--ID:1688811538530-->
1. print a range in functional style (no for loop)
> ```rust
> (1..=5).for_each(|i| println!("{}", i));
> ```
> - functional: `for_each` takes a lambda as argument
> - range is already an interator

<!--ID:1690266651788-->
1. What are the three kinds of iterators (implict and explict)?
> ```rust
> // borrows the collection and allows you to iterate over the items by reference.
> // After the iteration, you can still use the original collection because it was not consumed. Here's an example:
> for s in vec.iter() {...} // &String
>
> // allows to iterate over mutable references, so you can actually modify the items in the original collection:
> let mut vec = vec![1, 2, 3, 4, 5];
> for item in vec.iter_mut() {
>     *item *= 2;  // item is of type &mut i32, so by dereferencing item (*item), you can modify the items in the original vec.
> }
> // vec is now [2, 4, 6, 8, 10]
>
> // consumes the collection and allows you to iterate over the items by value, taking ownership of each item.
> // After the iteration, the original collection is gone. Here's an example:
> for s in vec.into_iter() {...} // String
>
> // implicit syntax:
> for s in &vec {...} // &String
> for s in &mut vec {...} // &mut String
> for s in vec {...} // String
> ```

---

### filter
- The closure passed to the filter method has the signature `FnMut(&T) -> bool`
- T is the type of the elements being iterated over.
- the element is passed to the closure as a reference.
- The reference is captured by the closure and stored in a borrow.
- The type of the closure's argument is &&T, which is a reference to a reference to an element of type T.
```rust
// example of using the filter method with a closure that takes a reference to a reference as an argument:
let v = vec![1, 2, 3];
let evens: Vec<i32> = v.into_iter().filter(|x| **x % 2 == 0).collect();
println!("Even numbers: {:?}", evens);
```
### for loop
- automatically call `into_iter()` on the expression and then iterate over it:
```rust
fn main() {
    let v = vec![10, 20, 30];

    for x in v {
        println!("x: {x}");
    }
    // range implements Iterator trait, step_by returns also Interator
    for i in (0..10).step_by(2) {
        println!("i: {i}");
    }
}
```
### loop
- guaranteed to be entered at least once (unlike while and for loops).
```rust
fn main() {
    let mut x = 10;
    loop {
        x = if x % 2 == 0 {
            x / 2
        } else {
            3 * x + 1
        };
        if x == 1 {
            break;
        }
    }
    println!("Final x: {x}");
}
```

## Pattern Match

---
<!--ID:1694674317666-->
1. Explain `match `and `@`.
> - Variable binding: captures the value that fits the pattern and stores it in a variable for use within the code block.
> - You can bind variables to values within a pattern using the `@` symbol.
> - `@` in `match` statement used for pattern binding: allows to both destructure a value and create a variable binding for the value or a part of it. This is useful when you want to check a value against a pattern while also capturing a part of the value for further use.
> - Returns a value. The value is the last expression in the match arm which was executed.
> - Match Guards: additional conditionals after pattern
> - Must be exhaustive.
> ```rust
> enum Event {
>     Click { x: i32, y: i32 },
>     Keypress(char),
>     None,
> }
>
> fn main() {
>     let event = Event::Click { x: 10, y: 20 };
>
>     match event {
>         Event::Click { x, y } if x > 0 && y > 0 => println!("Positive Click at x: {}, y: {}", x, y),
>         Event::Click { x, y } => println!("Click event at x: {}, y: {}", x, y),
>         Event::Keypress(c @ 'a'..='z') => println!("Lowercase letter: {}", c),
>         Event::Keypress(c @ 'A'..='Z') => println!("Uppercase letter: {}", c),
>         _ => println!("Other event"),
>     }
> }
> ```

---

- direct matching using `let` should be used cautiously and is typically reserved for when you're sure about the shape of the data. For more uncertain scenarios, match or if let are safer choices.
```rust
// irrefutalbe: always matches
let y = 1;  // y: pattern which matches value 1 and binds it to y
let (x, y, z) = (1, 2, 3);  //  tuple (x, y, z) is a strcutural pattern that matches against the value (1, 2, 3), binding 1 to x, 2 to y, and 3 to z.
```
Gotcha: cannot match against String, only String literal
`as_deref()` transforms an `Option<T>` to `Option<&T::Target>`, i.e. this turns `Option<String>` into `Option<&str>`.


### Ownership
- usually we don't want to take ownership or move the value, especially for heap-allocated values like String. Instead, we want to borrow a reference to the value and match against that

---
<!--ID:1690777097439-->
1. Explain ownership in the context of matching.
> - the way you match on values can determine whether you're moving the value or just borrowing it.
> - `match cli.command`, you're taking ownership of cli.command during the match.
> - This means that after this operation, cli.command will no longer be available for use because its ownership has been moved into the match block.
>
> - `match &cli.command`, you're borrowing a reference to cli.command.
> - This means you do not take ownership, and cli.command remains valid for use after the match.
>
> - Consider this: if cli.command is of a type that implements the Copy trait, then these two versions would be effectively the same, because copying a value is the same as moving it.

---

### Binding and Destructuring
```rust
let pair = (1, 2);
match pair {
    (x, y) if x == y => println!("Both are equal"),
    (x, _) if x == 1 => println!("First is one"),
    (_, y) if y == 2 => println!("Second is two"),
    _ => println!("No match"),
}
```

### Destructuring Enum
```rust
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(i32, i32, i32),
}
let msg = Message::ChangeColor(0, 160, 255);

match msg {
   Message::Quit => {
      println!("The Quit variant has no data to destructure.");
   }
   Message::Move { x, y } => {
      println!(
            "Move in the x direction {x} and in the y direction {y}"
      );
   }
   Message::Write(text) => {
      println!("Text message: {text}");
   }
   Message::ChangeColor(r, g, b) => println!(
      "Change the color to red {r}, green {g}, and blue {b}",
   ),
}
```


### Destructuring Struct
```rust
struct Point {
    x: i32, y: i32,
}
let p = Point { x: 0, y: 7 };
match p {
   Point { x, y: 0 } => println!("On the x axis at {x}"),
   Point { x: 0, y } => println!("On the y axis at {y}"),
   Point { x, y } => {
      println!("On neither axis: ({x}, {y})");
   }
}
// ignore values
match origin {
   Point { x, .. } => println!("x is {}", x),
}
```
### if assignement
```rust
let tokens = if tokens.len() == 0 {
   (1..=bms.len()).map(|i| i.to_string()).collect()
} else {
   tokens
};
```

### Match Guards
- arbitrary Boolean expression which will be executed if the pattern matches:
- are not the same as separate if expression inside of the match arm. 
    An if expression inside of the branch block (after =>) happens after the match arm is selected. 
    Failing the if condition inside of that block won't result in other arms of the original match expression being considered.
- The condition defined in the guard applies to every expression in a pattern with an |.
```rust
#[rustfmt::skip]
fn main() {
    let pair = (2, -2);
    println!("Tell me about {pair:?}");
    match pair {
        (x, y) if x == y     => println!("These are twins"),
        (x, y) if x + y == 0 => println!("Antimatter, kaboom!"),
        (x, _) if x % 2 == 1 => println!("The first one is odd"),
        _                    => println!("No correlation..."),
    }
}
```

## Global Initialization, ctor
- the crate uses various attributes and linker sections to ensure that the constructor function is run before main and the destructor function is run after main
- It will run before the main function or, in the case of tests, before any test function.
- it collects all ctor blocks
- for logging in tests just one iniit block in #[cfg(test)] is enough, e.g. in lib.rs


### Multiple ctor blocks:
- No matter where they're located, all ctor-attributed functions will run before any tests execute.
- Order is Undefined: unless they're in a defined sequence in a single compilation unit.
- Shared State: If multiple constructors modify shared state, it can lead to unpredictable results due to the undefined order of execution
- Destructors: If you're also using the dtor attribute for destructors, these will run after all tests have completed. Like constructors, their order of execution is also undefined.

### Best Practices:
- Idempotence: Make sure that each constructor function can run multiple times without causing issues, as it provides resilience against inadvertent multiple initializations.
- Avoid Dependencies Between Constructors: If you find that one constructor needs to run after another, consider merging them into a single constructor or rethinking the design to avoid such dependencies.


# Functions ........................................................................................
- return: bare expression WITHOUT semicolon
- no kwargs, but can use struct as workaround
- no variadic fn
```rust
// struct decomposition for kwargs and default values
struct Foo { bar: i32}
fn baz({bar}: Foo) -> i32 { bar * 2 }

// kwargs
struct NamedParams {
    param1: i32,
    param2: i32,
}
fn my_function(params: NamedParams) { ...  }
my_function(NamedParams { param2: 3, param1: 4 });

// noop
fn noop() { // This function does nothing }
```


# Concurrency ......................................................................................
[rust_concurrency.md]($VIMWIKI_PATH/dev/rust_concurrency.md)


# Recipies .........................................................................................
## Init Once Threadsave
```rust
use std::sync::Once;
static INIT: Once = Once::new();
fn initialize() {
    // Initialize the value
}
fn main() {
    INIT.call_once(|| initialize());
    // Use the initialized value
}
```
## Add el to array in loop
- pushing t does not work, falls out of context outside for loop
```rust
    let tags = dal.get_related_tags("ccc").unwrap();
    let mut tags_str: Vec<&str> = Vec::new();
    println!("The bookmarks are: {:?}", tags);
    // assert_eq!(bms.unwrap()[0].id, 11);
    for (i, t) in tags.iter().enumerate() {
        tags_str.push(&tags[i].tags);
    }
    println!("The bookmarks are: {:?}", tags_str);
```
## Builder Pattern
[Builder - Rust Design Patterns](https://rust-unofficial.github.io/patterns/patterns/creational/builder.html)
seen more frequently in Rust because Rust lacks overloading


# Resources ........................................................................................
[rust_python.md]($VIMWIKI_PATH/dev/rust_python.md)

[Rust fact vs. fiction: 5 Insights from Google's Rust journey in 2022 | Google Open Source Blog](https://opensource.googleblog.com/2023/06/rust-fact-vs-fiction-5-insights-from-googles-rust-journey-2022.html)
[Prefer Rust to C/C++ for new code. - Cliffle](http://cliffle.com/blog/prefer-rust/)

[Rust Is Hard, Or: The Misery of Mainstream Programming](https://hirrolot.github.io/posts/rust-is-hard-or-the-misery-of-mainstream-programming.html)

[Why Rust in Production? | Corrode Rust Consulting](https://corrode.dev/why-rust/)

## Con
[Should I Rust or should I Go?](https://kerkour.com/should-i-rust-or-should-i-go)
