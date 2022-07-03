#[derive(Copy, Clone)]
pub enum Direction { Up, Down, Left, Right }

pub struct Wall {
    pub x: usize,
    pub y: usize,
    pub dir: Direction,
}
