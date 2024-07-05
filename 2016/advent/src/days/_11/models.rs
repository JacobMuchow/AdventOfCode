// use core::fmt;
// use serde::{Deserialize, Serialize};
#![allow(dead_code)]

use std::collections::{BTreeSet};

#[derive(Debug, Clone, Eq, PartialEq, Hash, PartialOrd, Ord)]
pub enum Element {
    Lithium,
    Hydrogen,
    Thulium,
    Plutonium,
    Strontium,
    Promethium,
    Ruthenium
}

#[derive(Debug, Clone, Eq, PartialEq, Hash, PartialOrd, Ord)]
pub enum Item {
    Generator(Element),
    Microchip(Element)
}

#[derive(Debug, Clone)]
pub struct GameState {
    pub floors: Vec<BTreeSet<Item>>,
    pub cur_floor: usize
}
