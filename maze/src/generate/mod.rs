use crate::maze::{Wall, Maze};

pub mod simple;
pub mod binary_tree;
pub mod recursive_division;

pub trait MazeGenerator: Iterator<Item = (Wall, bool)> {
    fn width(&self) -> usize;
    fn height(&self) -> usize;
    fn initial_maze(&self) -> Maze;
    fn name(&self) -> String;
}