use std::str::FromStr;

use regex::Captures;

pub trait ExtensionsTrait {
    fn get_as_str(&self, i: usize) -> Option<&str>;
    fn get_as_char(&self, i: usize) -> Option<char>;
    fn get_as_num<T: FromStr>(&self, i: usize) -> Option<T>;
}

impl ExtensionsTrait for Captures<'_> {
    
    fn get_as_str(&self, i: usize) -> Option<&str> {
        self.get(i).map(|m| m.as_str())
    }
    
    fn get_as_char(&self, i: usize) -> Option<char> {
        self.get_as_str(i).and_then(|m| m.chars().next())
    }

    fn get_as_num<T: FromStr>(&self, i: usize) -> Option<T> {
        self.get(i).and_then(|m| {
            m.as_str().parse().ok()
        })
    }
}