use bincode;
use serde::{Deserialize, Serialize};
use serde::de::DeserializeOwned;


#[derive(Clone, Debug, Serialize, Deserialize)]
struct Node {
    data: Option<Vec<u8>>
}

impl Node {
    pub fn new() -> Self {
        Node { data: None }
    }

    pub fn set<T>(&mut self, data: &T) where T: Serialize {
        let data: Vec<u8> = bincode::serialize(data).unwrap();
        self.data = Some(data);
    }

    pub fn get<'de, T>(&self, default: Option<T>) -> T where T: DeserializeOwned {
        let data = self.data.as_ref();
        match data {
            Some(value) => bincode::deserialize::<T>(&value[..]).unwrap(),
            None => match default {
                Some(default) => default,
                None => panic!("Data is not set"),
            }
        }
    }
}


#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Dict {
    data: std::collections::HashMap<String, Node>,
}

impl Dict {
    pub fn new() -> Self {
        Dict {
            data: std::collections::HashMap::new(),
        }
    }

    pub fn set<T>(&mut self, key: &str, data: &T) where T: Serialize {
        let mut node = Node::new();
        node.set(data);
        self.data.insert(key.to_string(), node);
    }

    pub fn get<T>(&self, key: &str, default: Option<T>) -> T where T: DeserializeOwned {
        let node = self.data.get(key);
        match node {
            Some(node) => node.get(default),
            None => match default {
                Some(default) => default,
                None => panic!("Key {} is not set", key),
            }
        }
    }
}
