pub enum Wall {
    Up {x: usize, y: usize},
    Down {x: usize, y: usize},
    Left {x: usize, y: usize},
    Right {x: usize, y: usize}
}

impl Wall {
    pub fn xy(&self) -> (usize, usize) {
        match self {
            &Wall::Up { x, y } | &Wall::Down { x, y } | &Wall::Left { x, y } | &Wall::Right { x, y } => (x, y)
        }
    }
}