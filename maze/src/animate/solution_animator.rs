use nannou::prelude::*;

use crate::{maze::Maze, solve::solve};

pub struct MazeSolutionAnimator {
    solution: Vec<(usize, usize)>,
    top_left: Vec2,
    wall_size: f32,
}

impl MazeSolutionAnimator {
    pub fn new(maze: &Maze, wall_size: f32, top_left: (f32, f32), start: (usize, usize), end: (usize, usize)) -> Self {
        let solution = solve(maze, start, end);
        MazeSolutionAnimator {
            solution,
            top_left: pt2(top_left.0, top_left.1),
            wall_size,
        }
    }

    pub fn update(&mut self) {
    }

    pub fn draw(&self, draw: &Draw) {
        let points = self.solution.iter()
            .map(|&(x, y)| self.top_left + pt2(x as f32, -(y as f32)) * self.wall_size);
        draw.polyline().points(points).color(RED);
    }
}