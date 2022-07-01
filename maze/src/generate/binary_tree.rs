use nannou::rand::random_range;

use crate::maze::wall::Direction::*;
use crate::maze::{Maze, Wall};

use super::MazeGenerator;

pub struct BinaryTreeGenerator {
    maze: Maze,
    cell_index: usize,
}

impl BinaryTreeGenerator {
    pub fn new(width: usize, height: usize) -> BinaryTreeGenerator {
        BinaryTreeGenerator {
            maze: Maze::new_with_edges(width, height, true),
            cell_index: 0,
        }
    }

    fn get_candidate_walls(&self) -> Vec<Wall> {
        let x = self.cell_index % self.maze.width();
        let y = self.cell_index / self.maze.width();
        let mut candidates = Vec::new();

        let right_wall = Wall { x, y, dir: Right };
        if x <= self.maze.width() - 2 {
            candidates.push(right_wall);
        }

        let down_wall = Wall { x, y, dir: Down };
        if y <= self.maze.height() - 2 {
            candidates.push(down_wall)
        }

        candidates
    }
}

impl MazeGenerator for BinaryTreeGenerator {
    fn width(&self) -> usize {
        self.maze.width()
    }

    fn height(&self) -> usize {
        self.maze.height()
    }

    fn initial_maze(&self) -> crate::maze::Maze {
        Maze::new_with_edges(self.maze.width(), self.maze.height(), true)
    }

    fn name(&self) -> String {
        "Binary Tree Algorithm".to_string()
    }
}

impl Iterator for BinaryTreeGenerator {
    type Item = (Wall, bool);

    fn next(&mut self) -> Option<Self::Item> {
        if self.cell_index >= self.maze.width() * self.maze.height() {
            return None;
        }

        let mut candidates = self.get_candidate_walls();
        self.cell_index += 1;

        let candidate_count = candidates.len();
        if candidate_count > 0 {
            let wall_to_remove = candidates.remove(random_range(0, candidate_count));
            Some((wall_to_remove, false))
        } else {
            // This happens only on the last cell
            None
        }

    }
}
