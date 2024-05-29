#![allow(unused_variables)]

#[derive(Debug, Clone)]
pub struct Span<I, V> {
    pub start: I,
    pub end: I,
    pub value: Option<V>,
}

impl<I, V> Span<I, V> {
    pub fn new(start: I, end: I) -> Span<I, V> {
        Span {
            start: start,
            end: end,
            value: None,
        }
    }
}
