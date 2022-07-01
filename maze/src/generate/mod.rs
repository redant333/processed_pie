use crate::maze::{Wall, Maze};

pub mod simple;

pub trait MazeGenerator: Iterator<Item = (Wall, bool)> {
    fn width(&self) -> usize;
    fn height(&self) -> usize;
    fn initial_maze(&self) -> Maze;
}