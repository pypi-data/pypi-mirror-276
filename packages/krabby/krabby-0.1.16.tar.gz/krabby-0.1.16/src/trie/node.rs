#![allow(dead_code)]

use std::collections::HashMap;
use std::fmt::Display;
use std::hash::Hash;

// use crate::span::Span;

#[derive(Debug, Clone)]
pub struct Node<
    K: PartialEq + Eq + Hash + Copy + Display,
    T: PartialEq + Eq + Hash + Copy,
    V: Eq + Copy + Display,
> {
    pub value: Option<V>,
    pub next: HashMap<K, T>,
}

impl<
        K: PartialEq + Eq + Hash + Copy + Display,
        T: PartialEq + Eq + Hash + Copy,
        V: Eq + Copy + Display,
    > Node<K, T, V>
{
    pub fn new(value: V) -> Node<K, T, V> {
        Node {
            value: Some(value),
            next: HashMap::new(),
        }
    }

    pub fn default() -> Node<K, T, V> {
        Node {
            value: None,
            next: HashMap::new(),
        }
    }

    pub fn equal(&self, value: V) -> bool {
        match self.value {
            Some(v) => v == value,
            None => false,
        }
    }
}
