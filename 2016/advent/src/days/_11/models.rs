#![allow(dead_code)]

use std::collections::BTreeSet;

#[derive(Debug, Clone, Eq, PartialEq, Hash, PartialOrd, Ord)]
pub enum Element {
    Lithium,
    Hydrogen,
    Thulium,
    Plutonium,
    Strontium,
    Promethium,
    Ruthenium,
    Elerium,
    Dilithium
}

impl Element {
    pub fn name(&self) -> &str {
        match self {
            Element::Lithium => "Li",
            Element::Hydrogen => "H",
            Element::Thulium => "Th",
            Element::Plutonium => "Pu",
            Element::Strontium => "Sr",
            Element::Promethium => "Pr",
            Element::Ruthenium => "Ru",
            Element::Elerium => "El",
            Element::Dilithium => "Di",
        }
    }
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
