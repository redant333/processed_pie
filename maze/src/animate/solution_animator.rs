use nannou::prelude::*;

use crate::{maze::Maze, solve::solve};

use super::Animator;

pub struct MazeSolutionAnimator {
    solution: Vec<(usize, usize)>,
    top_left: Vec2,
    wall_size: f32,
    lines_counter: usize,
    done: bool,
}

impl MazeSolutionAnimator {
    pub fn new(
        maze: &Maze,
        wall_size: f32,
        top_left: (f32, f32),
        start: (usize, usize),
        end: (usize, usize),
    ) -> Self {
        let solution = solve(maze, start, end);

        MazeSolutionAnimator {
            solution,
            top_left: pt2(top_left.0, top_left.1),
            wall_size,
            lines_counter: 0,
            done: false,
        }
    }
}

impl Animator for MazeSolutionAnimator {
    fn update(&mut self) {
        self.lines_counter += 1;

        if self.lines_counter > self.solution.len() {
            self.done = true;
        }
    }

    fn draw(&self, draw: &Draw, _window: &Rect) {
        let points = self
            .solution
            .iter()
            .map(|&(x, y)| self.top_left + pt2(x as f32, -(y as f32)) * self.wall_size)
            .take(self.lines_counter);

        draw.polyline().points(points).color(RED);
    }

    fn done(&self) -> bool {
        self.done
    }
}
