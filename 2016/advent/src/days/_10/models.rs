#[derive(Debug)]
pub enum Target {
    Bot(u32),
    OutputBin(u32)
}

#[derive(Debug)]
pub struct Bot {
    pub id: u32,
    pub chips: Vec<u32>,
    pub gives: Option<(Target, Target)>
}

impl Bot {
    pub fn new(id: u32) -> Bot {
        return Bot {
            id,
            chips: Vec::new(),
            gives: None
        };
    }
}

#[derive(Debug)]
pub struct OutputBin {
    pub id: u32,
    pub chips: Vec<u32>
}

impl OutputBin {
    pub fn new(id: u32) -> OutputBin {
        return OutputBin {
            id,
            chips: Vec::new()
        }
    }
}