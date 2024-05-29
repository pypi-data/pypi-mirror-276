use std::os;
use std::fs::read_dir;
use std::io::Read;
use std::path::Path;
use md5::{Md5, Digest};

pub fn md5sum(path: &str, batch_size: usize) -> String {
    let mut files: Vec<String> = Vec::new();
    let mut dirs: Vec<String> = Vec::new();

    // Check if path exists
    if Path::new(path).exists() {
        // Check if path is a file
        if Path::new(path).is_file() {
            files.push(path.to_string());
        } else {
            dirs.push(path.to_string());
        }
    }

    loop {
        if dirs.is_empty() {
            break;
        }

        let dir = dirs.pop().unwrap();
        let entries = match read_dir(&dir) {
            Ok(entries) => entries,
            Err(_) => continue,
        };

        for entry in entries {
            let entry = match entry {
                Ok(entry) => entry,
                Err(_) => continue,
            };

            let path = entry.path();
            if path.is_file() {
                files.push(path.to_string_lossy().to_string());
            } else {
                dirs.push(path.to_string_lossy().to_string());
            }
        }
    }

    let mut hashes: Vec<String> = Vec::new();
    for file in &files {
        //Get relative path if path is a directory
        let relative_path = if Path::new(path).is_dir() {
            let file_path = Path::new(file);
            let relative_path = file_path.strip_prefix(path).unwrap();
            let relative_path = relative_path.to_str().unwrap();
            // add ./ to relative path
            format!("./{}", relative_path)
        } else {
            Path::new(file).file_name().unwrap().to_str().unwrap().to_string()
        };
        let mut md5 = Md5::new();
        let mut fin = match std::fs::File::open(file) {
            Ok(fin) => fin,
            Err(_) => continue,
        };

        loop {
            let mut buf = vec![0; batch_size];
            let n = match fin.read(&mut buf) {
                Ok(n) => n,
                Err(_) => break,
            };

            if n == 0 {
                break;
            }

            md5.update(&buf[..n]);
        }

        let hash_value = format!("{:x} {}", md5.finalize(), relative_path);
        hashes.push(hash_value);
    }

    hashes.sort();

    // Concatenate all hashes with newline
    let mut hash_value = hashes.join("\n");

    // Add a newline at the end
    hash_value += "\n";

    // Hash the concatenated hashes
    let mut md5 = Md5::new();
    md5.update(hash_value.as_bytes());
    format!("{:x}", md5.finalize())
}