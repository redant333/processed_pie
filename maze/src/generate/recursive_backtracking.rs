use std::collections::HashSet;

use nannou::rand::prelude::IteratorRandom;
use nannou::rand::{random_range, thread_rng};

use crate::maze::wall::Direction;
use crate::maze::wall::Direction::*;
use crate::maze::{Maze, Wall};

use super::MazeGenerator;

pub struct RecursiveBacktrackingGenerator {
    width: usize,
    height: usize,
    visited_cells: HashSet<(usize, usize)>,
    backtrack_stack: Vec<(usize, usize)>,
    current_cell: (usize, usize),
}

impl RecursiveBacktrackingGenerator {
    pub fn new(width: usize, height: usize) -> Self {
        let current_cell = (random_range(0, width), random_range(0, height));

        let mut visited_cells = HashSet::new();
        visited_cells.insert(current_cell);

        Self {
            width,
            height,
            visited_cells,
            backtrack_stack: vec![current_cell],
            current_cell,
        }
    }

    fn next_unvisited(&self) -> Option<((usize, usize), Wall)> {
        [Up, Down, Left, Right]
            .into_iter()
            .filter_map(|dir| self.get_neighbor(self.current_cell, dir))
            .filter(|(cell, _)| !self.visited_cells.contains(cell))
            .choose(&mut thread_rng())
    }

    fn backtrack_and_next_unvisited(&mut self) -> Option<((usize, usize), Wall)> {
        loop {
            self.backtrack_stack.pop();
            self.current_cell = *self.backtrack_stack.last()?;

            if let next @ Some(_) = self.next_unvisited() {
                return next;
            }
        }
    }

    fn get_neighbor(&self, cell: (usize, usize), dir: Direction) -> Option<((usize, usize), Wall)> {
        let (x, y) = cell;

        let neighbor = match dir {
            Up if y == 0 => None,
            Up => Some((x, y - 1)),
            Down if y >= self.height - 1 => None,
            Down => Some((x, y + 1)),
            Left if x == 0 => None,
            Left => Some((x - 1, y)),
            Right if x >= self.width - 1 => None,
            Right => Some((x + 1, y)),
        }?;

        Some((neighbor, Wall { x, y, dir }))
    }
}

impl MazeGenerator for RecursiveBacktrackingGenerator {
    fn width(&self) -> usize {
        self.width
    }

    fn height(&self) -> usize {
        self.height
    }

    fn initial_maze(&self) -> crate::maze::Maze {
        Maze::new(self.width, self.height, true)
    }

    fn name(&self) -> String {
        "Recursive Backtracking".to_string()
    }
}

impl Iterator for RecursiveBacktrackingGenerator {
    type Item = (Wall, bool);

    fn next(&mut self) -> Option<Self::Item> {
        let (next_cell, carved_wall) = self
            .next_unvisited()
            .or_else(|| self.backtrack_and_next_unvisited())?;

        self.current_cell = next_cell;
        self.visited_cells.insert(next_cell);
        self.backtrack_stack.push(next_cell);

        Some((carved_wall, false))
    }
}
