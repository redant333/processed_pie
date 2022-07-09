use crate::generate::MazeGenerator;
use nannou::prelude::*;

use super::{
    generation_animator::{AnimatorConfig, MazeGenerationAnimator},
    solution_animator::MazeSolutionAnimator,
    Animator,
};

pub struct MazeAnimator<T>
where
    T: MazeGenerator,
{
    generation_animator: MazeGenerationAnimator<T>,
    solution_animator: Option<MazeSolutionAnimator>,
}

impl<T> MazeAnimator<T>
where
    T: MazeGenerator,
{
    pub fn new(generator: T) -> Self
    where
        T: MazeGenerator,
    {
        let config = AnimatorConfig {
            back_color: rgb8(0x07, 0x10, 0x13),
            wall_color: rgb8(0x01, 0x97, 0xf6),
            wall_size: 32.0,
            y: 8.0,
        };

        let generation_animator = MazeGenerationAnimator::new(config, generator);
        Self {
            generation_animator,
            solution_animator: None,
        }
    }
}

impl<T> Animator for MazeAnimator<T>
where
    T: MazeGenerator,
{
    fn update(&mut self) {
        if self.generation_animator.done() && self.solution_animator.is_none() {
            self.solution_animator = Some(MazeSolutionAnimator::new(
                self.generation_animator.get_maze().unwrap(),
                32.0,
                self.generation_animator.top_left_cell(),
                (0, 0),
                (37, 19),
            ));
        }

        if !self.generation_animator.done() {
            self.generation_animator.update();
        } else {
            self.solution_animator.as_mut().unwrap().update();
        }
    }

    fn draw(&self, draw: &Draw, window: &Rect) {
        self.generation_animator.draw(draw, window);

        if let Some(solution_animator) = self.solution_animator.as_ref() {
            solution_animator.draw(draw, window);
        }
    }

    fn done(&self) -> bool {
        if let Some(solution) = self.solution_animator.as_ref() {
            solution.done()
        } else {
            false
        }
    }
}
