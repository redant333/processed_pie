mod generation_animator;
mod solution_animator;

mod maze_animator;
pub use maze_animator::*;

mod waiting_animator;
pub use waiting_animator::*;

use nannou::prelude::*;

pub trait Animator {
    fn update(&mut self);
    fn draw(&self, draw: &Draw, window: &Rect);
    fn done(&self) -> bool;
}