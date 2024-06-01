use std::time::{Duration, Instant};

fn main() {
    let text: &str = "J‘3";
    // let text: &str = "Instead of creating a new string remaining_text in each iteration, we convert text into a vector of characters text_chars once at the start. This conversion allows us to slice the character vector directly, avoiding repeated allocations.";
    let mut index = 0;
    let text_chars: Vec<char> = text.chars().collect();
    let text_len = text_chars.len();

    let start = Instant::now();
    while index < text_len {
        let remaining_text: String = text_chars[index..].iter().collect();
    }
    let duration = start.elapsed();
    println!("Time elapsed in expensive_function() is: {:?}", duration);
}