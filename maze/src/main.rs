use nannou::prelude::*;
use std::collections::VecDeque;
use std::process::exit;

use maze::animate::*;
use maze::generate::*;

struct Model {
    animators: VecDeque<Box<dyn Animator>>,
    current_animator: Box<dyn Animator>,
}

fn main() {
    nannou::app(model).update(update).run();
}

fn model(app: &App) -> Model {
    app.new_window()
        .size(1280, 720)
        .resizable(false)
        .decorations(false)
        .view(view)
        .build()
        .expect("Could not initialize window");

    let mut animators = VecDeque::new();

    let generator = KruskalsGenerator::new(38, 20);
    let animator: Box<dyn Animator> = Box::new(MazeAnimator::new(generator));
    animators.push_back(animator);

    let generator = BinaryTreeGenerator::new(38, 20);
    let animator: Box<dyn Animator> = Box::new(MazeAnimator::new(generator));
    animators.push_back(animator);

    let generator = RecursiveDivisionGenerator::new(38, 20);
    let animator: Box<dyn Animator> = Box::new(MazeAnimator::new(generator));
    animators.push_back(animator);

    let current_animator = animators.pop_front().unwrap();

    Model {
        animators,
        current_animator,
    }
}

fn update(app: &App, model: &mut Model, _update: Update) {
    if model.current_animator.done() {
        model.current_animator = model.animators.pop_front().unwrap_or_else(|| {
            app.quit();
            exit(0)
        });
    }

    model.current_animator.update();
}

fn view(app: &App, model: &Model, frame: Frame) {
    let draw = app.draw();
    let window = app.window_rect();

    model.current_animator.draw(&draw, &window);

    draw.text(&(app.fps() as i32).to_string())
        .xy(app.window_rect().pad(15.0).top_right());

    draw.to_frame(app, &frame).unwrap();
}
