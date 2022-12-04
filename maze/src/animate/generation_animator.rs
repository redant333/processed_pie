use nannou::prelude::*;

use crate::draw::Draw as MazeDraw;
use crate::{generate::MazeGenerator, maze::Maze};

use super::Animator;

pub struct AnimatorConfig {
    pub back_color: Rgb8,
    pub wall_color: Rgb8,
    pub wall_size: f32,
    pub y: f32,
}

pub struct MazeGenerationAnimator<T> {
    config: AnimatorConfig,
    generator: T,
    maze: Maze,
    first_frame: bool,
    pub maze_completed: bool,
}

impl<T> Animator for MazeGenerationAnimator<T>
where
    T: MazeGenerator,
{
    fn update(&mut self) -> () {
        if !self.first_frame {
            self.handle_new_wall();
        } else {
            self.first_frame = false;
        }
    }

    fn draw(&self, draw: &Draw, _window: &Rect) -> () {
        let draw = draw.x_y(0.0, self.config.y);

        draw.background().color(self.config.back_color);

        let maze_draw = MazeDraw::new(
            &draw,
            &self.maze,
            self.config.wall_color,
            self.config.wall_size,
        );

        for wall in self.maze.wall_iter() {
            maze_draw.wall(&wall);
        }
    }

    fn done(&self) -> bool {
        self.maze_completed
    }
}

impl<T> MazeGenerationAnimator<T>
where
    T: MazeGenerator,
{
    pub fn new(config: AnimatorConfig, generator: T) -> MazeGenerationAnimator<T> {
        let maze = generator.initial_maze();
        MazeGenerationAnimator {
            config,
            generator,
            maze,
            first_frame: true,
            maze_completed: false,
        }
    }

    pub fn top_left_cell(&self) -> Vec2 {
        let x =
            -(self.maze.width() as f32 * self.config.wall_size / 2.0) + self.config.wall_size / 2.0;
        let y = (self.maze.height() as f32 * self.config.wall_size / 2.0)
            - self.config.wall_size / 2.0
            + self.config.y;
        pt2(x, y)
    }

    pub fn get_maze(&self) -> Option<&Maze> {
        if self.maze_completed {
            Some(&self.maze)
        } else {
            None
        }
    }

    fn handle_new_wall(&mut self) {
        if let Some((wall, state)) = self.generator.next() {
            self.maze.set_wall(&wall, state);
        } else {
            self.maze_completed = true;
        }
    }
}
