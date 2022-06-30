use crate::maze::Wall;

pub mod simple;

pub trait MazeGenerator: Iterator<Item = (Wall, bool)> {
    fn width(&self) -> usize;
    fn height(&self) -> usize;
}