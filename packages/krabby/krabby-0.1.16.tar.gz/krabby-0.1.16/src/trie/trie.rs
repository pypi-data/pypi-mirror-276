#![allow(dead_code)]
#![allow(unused_variables)]

use std::collections::HashSet;
use std::fmt::Display;
use std::{collections::HashMap, hash::Hash};

use crate::trie::node::Node;
use crate::trie::span::Span;

#[derive(Debug, Clone)]
pub struct Trie<K: PartialEq + Eq + Copy + Hash + Display, V: Eq + Copy + Display> {
    pub root: Node<K, usize, V>,
    pub nodes: HashMap<usize, Node<K, usize, V>>,
    pub next: usize,
}

impl<K: PartialEq + Eq + Copy + Hash + Display, V: Eq + Copy + Display> Trie<K, V> {
    pub fn new() -> Trie<K, V> {
        Trie {
            next: 0,
            root: Node::default(),
            nodes: HashMap::new(),
        }
    }

    pub fn put(&mut self, key: &Vec<K>, last: V) {
        if key.len() == 0 {
            return;
        }

        if !self.root.next.contains_key(&key[0]) {
            let mut next = Node::default();
            if key.len() == 1 {
                next.value = Some(last);
            }

            self.nodes.insert(self.next, next);
            self.root.next.insert(key[0], self.next);
            self.next += 1;
        }

        let mut node_id = *self.root.next.get(&key[0]).unwrap();

        for i in 1..key.len() {
            let node = self.nodes.get_mut(&node_id).unwrap();
            if !node.next.contains_key(&key[i]) {
                let next = Node::default();

                node.next.insert(key[i], self.next);
                self.nodes.insert(self.next, next);
                self.next += 1;
            }
            let node = self.nodes.get(&node_id).unwrap();
            node_id = *node.next.get(&key[i]).unwrap();
        }
        let node = self.nodes.get_mut(&node_id).unwrap();
        node.value = Some(last);
    }

    pub fn pop(&mut self, key: &Vec<K>, last: V) {
        if key.len() == 0 {
            return;
        }

        if !self.root.next.contains_key(&key[0]) {
            return;
        }

        let mut node_id = *self.root.next.get(&key[0]).unwrap();

        let mut last_branch: Option<(usize, usize)> = None;
        let last_value: Option<V> = None;

        for i in 1..key.len() {
            let node = self.nodes.get_mut(&node_id).unwrap();
            if !node.next.contains_key(&key[i]) {
                return;
            }

            if node.equal(last) || node.next.len() > 1 {
                last_branch = Some((node_id, i));
            }

            node_id = *node.next.get(&key[i]).unwrap();
        }

        let node = self.nodes.get_mut(&node_id).unwrap();
        if !node.equal(last) {
            return;
        }
        node.value = None;
        if node.next.len() > 0 {
            return;
        }

        match last_branch {
            Some((node_id, i)) => {
                let node = self.nodes.get(&node_id).unwrap();
                if node.equal(last) {
                    return;
                }

                let mut curr_id = node_id;
                for j in i..key.len() {
                    let node = self.nodes.remove(&curr_id).unwrap();
                    curr_id = *node.next.get(&key[j]).unwrap();
                }

                if self.nodes.contains_key(&curr_id) {
                    self.nodes.remove(&curr_id);
                }
            }
            None => {
                self.root.next.remove(&key[0]);
            }
        }
    }

    pub fn extract(
        &self,
        key: &Vec<K>,
        target: V,
        boundary: Option<&HashSet<K>>,
    ) -> Vec<Span<usize, Vec<K>>> {
        if key.len() == 0 {
            return Vec::new();
        }

        let mut node = &self.root;
        let mut idx: usize = 0;
        let mut start: usize = 0;
        let mut end: usize = 0;
        let mut reset: bool = false;
        let size = key.len();

        let mut spans: Vec<Span<usize, Vec<K>>> = Vec::new();
        let (strict, boundary) = match boundary {
            Some(b) => (true, b.clone()),
            None => (false, HashSet::new()),
        };

        while idx < size {
            let curr = &key[idx];
            if !strict || boundary.contains(curr) {
                let valid = node.equal(target);

                if valid || node.next.contains_key(curr) {
                    let mut seq_start = 0;
                    let mut seq_end = 0;

                    if valid {
                        end = idx;
                        seq_start = start;
                        seq_end = end;
                    }

                    let mut longest_found = false;
                    if node.next.contains_key(curr) {
                        let child_id = node.next.get(curr).unwrap();
                        let mut child = self.nodes.get(child_id).unwrap();
                        let mut idy = idx + 1;

                        while idy < size {
                            let next = &key[idy];

                            if !strict || boundary.contains(next) {
                                if child.equal(target) {
                                    end = idy;
                                    longest_found = true;
                                    seq_start = start;
                                    seq_end = end;
                                }
                            }

                            if !child.next.contains_key(next) {
                                break;
                            }

                            let next_id = child.next.get(next).unwrap();
                            child = self.nodes.get(next_id).unwrap();
                            idy += 1;
                        }

                        if idy >= size {
                            if child.equal(target) {
                                end = idy + 1;
                                longest_found = true;
                                seq_start = start;
                                seq_end = end;
                            }
                        }

                        if longest_found {
                            idx = end;
                        }
                    }

                    if seq_start < seq_end {
                        if seq_end > size {
                            seq_end = size;
                        }

                        let span = Span::new(seq_start, seq_end);
                        spans.push(span);
                    }
                }
                node = &self.root;
                reset = true;
            } else {
                if node.next.contains_key(curr) {
                    node = self.nodes.get(node.next.get(curr).unwrap()).unwrap();
                } else {
                    node = &self.root;
                    reset = true;

                    let mut idy = idx + 1;

                    while !strict || idy < size {
                        let next = &key[idy];

                        if boundary.contains(next) {
                            break;
                        }

                        idy += 1;
                    }

                    idx = idy;
                }
            }

            if idx + 1 >= size {
                if node.equal(target) {
                    let span = Span::new(start, size);
                    spans.push(span);
                }
            }

            idx += 1;

            if reset {
                start = idx;
                reset = false;
            }
        }

        for span in spans.iter_mut() {
            span.value = Some(key[span.start..span.end].to_vec());
        }

        return spans;
    }

    pub fn has(&self, key: &Vec<K>, target: V) -> bool {
        if key.len() == 0 {
            return false;
        }

        let mut node = &self.root;
        for curr in key.iter() {
            if !node.next.contains_key(curr) {
                return false;
            }

            let child_id = node.next.get(curr).unwrap();
            let child = self.nodes.get(child_id).unwrap();
            node = child;
        }

        return node.equal(target);
    }
}
