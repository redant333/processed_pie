use nannou::{color::Rgb8, Draw};

use crate::{maze::Maze, generate::MazeGenerator};
use crate::draw::Draw as MazeDraw;

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
    pub maze_completed: bool,
}

impl<T> MazeGenerationAnimator<T> where T: MazeGenerator {
    pub fn new(config: AnimatorConfig, generator: T) -> MazeGenerationAnimator<T> {
        let maze = generator.initial_maze();
        MazeGenerationAnimator {
            config,
            generator,
            maze,
            maze_completed: false,
        }
    }

    pub fn top_left_cell(&self) -> (f32, f32) {
        let x = -(self.maze.width() as f32 * self.config.wall_size / 2.0) +
            self.config.wall_size / 2.0;
        let y = (self.maze.height() as f32 * self.config.wall_size / 2.0) -
            self.config.wall_size / 2.0 + self.config.y;
        (x, y)
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

    pub fn update(&mut self) {
        self.handle_new_wall();
    }

    pub fn draw(&self, draw: &Draw) {
        let draw = draw.x_y(0.0, self.config.y);

        let maze_draw = MazeDraw::new(
            &draw,
            &self.maze,
            self.config.wall_color,
            self.config.wall_size);

        for wall in self.maze.wall_iter() {
            maze_draw.wall(&wall);
        }
    }
}