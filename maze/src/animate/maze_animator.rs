use crate::generate::MazeGenerator;
use nannou::prelude::*;

use super::{
    generation_animator::{AnimatorConfig, MazeGenerationAnimator},
    solution_animator::{MazeSolutionAnimator, SolutionAnimatorConfig},
    Animator,
};

pub struct MazeAnimator<T>
where
    T: MazeGenerator,
{
    generation_animator: MazeGenerationAnimator<T>,
    solution_animator: MazeSolutionAnimator,
    generator_name: String,
}

impl<T> MazeAnimator<T>
where
    T: MazeGenerator,
{
    pub fn new(generator: T, start: (usize, usize), end: (usize, usize)) -> Self
    where
        T: MazeGenerator,
    {
        let config = AnimatorConfig {
            back_color: rgb8(0x07, 0x10, 0x13),
            wall_color: rgb8(0x01, 0x97, 0xf6),
            wall_size: 32.0,
            y: 8.0,
        };
        let generator_name = generator.name();
        let generation_animator = MazeGenerationAnimator::new(config, generator);

        let config = SolutionAnimatorConfig {
            wall_size: 32.0,
            dot_size: 18.0,
            top_left: generation_animator.top_left_cell(),
            start,
            end,
            color: rgb(0xa5, 0x24, 0x22),
            line_weight: 5.0,
        };
        let solution_animator = MazeSolutionAnimator::new(config);

        Self {
            generation_animator,
            solution_animator,
            generator_name,
        }
    }
}

impl<T> Animator for MazeAnimator<T>
where
    T: MazeGenerator,
{
    fn update(&mut self) {
        if self.generation_animator.done() {
            self.solution_animator
                .set_maze(self.generation_animator.get_maze().unwrap());
        }

        if !self.generation_animator.done() {
            self.generation_animator.update();
        } else {
            self.solution_animator.update();
        }
    }

    fn draw(&self, draw: &Draw, window: &Rect) {
        self.generation_animator.draw(draw, window);
        self.solution_animator.draw(draw, window);

        draw.text(&self.generator_name)
            .xy(window.pad_bottom(30.0).mid_bottom())
            .w(window.w())
            .color(rgb8(0xcc, 0xc4, 0xbc))
            .font_size(30);
    }

    fn done(&self) -> bool {
        self.solution_animator.done()
    }
}
