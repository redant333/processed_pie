use crate::maze::{Wall, Maze};

mod binary_tree;
pub use binary_tree::*;

mod recursive_division;
pub use recursive_division::*;

pub trait MazeGenerator: Iterator<Item = (Wall, bool)> {
    fn width(&self) -> usize;
    fn height(&self) -> usize;
    fn initial_maze(&self) -> Maze;
    fn name(&self) -> String;
}