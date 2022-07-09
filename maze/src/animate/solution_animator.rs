use nannou::prelude::*;

use crate::{maze::Maze, solve::solve};

use super::Animator;

pub struct SolutionAnimatorConfig {
    pub wall_size: f32,
    pub dot_size: f32,
    pub top_left: Vec2,
    pub start: (usize, usize),
    pub end: (usize, usize),
    pub color: Rgb8,
    pub line_weight: f32,
}

pub struct MazeSolutionAnimator {
    config: SolutionAnimatorConfig,
    solution: Option<Vec<(usize, usize)>>,
    lines_to_draw: usize,
    lines_to_skip: usize,
    done: bool,
}

impl MazeSolutionAnimator {
    pub fn new(config: SolutionAnimatorConfig) -> Self {
        MazeSolutionAnimator {
            solution: None,
            config,
            lines_to_draw: 0,
            lines_to_skip: 0,
            done: false,
        }
    }

    fn maze_pos_to_xy_pos(&self, (x, y): (usize, usize)) -> Vec2 {
        self.config.top_left + pt2(x as f32, -(y as f32)) * self.config.wall_size
    }

    pub fn set_maze(&mut self, maze: &Maze) {
        self.solution = Some(solve(maze, self.config.start, self.config.end));
    }
}

impl Animator for MazeSolutionAnimator {
    fn update(&mut self) {
        if self.solution.is_none() || self.done() {
            return;
        }

        let solution_len = self.solution.as_ref().unwrap().len();

        if self.lines_to_skip > solution_len {
            self.done = true;
            return;
        }

        if self.lines_to_draw <= solution_len {
            self.lines_to_draw += 1;
        } else if self.lines_to_skip <= solution_len {
            self.lines_to_skip += 1;
        }
    }

    fn draw(&self, draw: &Draw, _window: &Rect) {
        if let Some(solution) = self.solution.as_ref() {
            let points = solution
                .iter()
                .map(|&(x, y)| self.maze_pos_to_xy_pos((x, y)))
                .skip(self.lines_to_skip)
                .take(self.lines_to_draw)
                .peekable();

            draw.polyline()
                .color(self.config.color)
                .weight(self.config.line_weight)
                .points(points);
        }

        let start = if self.solution.is_none() {
            self.maze_pos_to_xy_pos(self.config.start)
        } else {
            let cell = self
                .solution
                .as_ref()
                .unwrap()
                .get(self.lines_to_skip)
                .unwrap_or(&self.config.end);

            self.maze_pos_to_xy_pos(*cell)
        };

        draw.ellipse()
            .w_h(self.config.dot_size, self.config.dot_size)
            .color(self.config.color)
            .xy(start);
    }

    fn done(&self) -> bool {
        self.done
    }
}
