use nannou::prelude::*;
use std::collections::VecDeque;
use std::path::PathBuf;
use std::process::exit;
use std::time::SystemTime;
use std::time::UNIX_EPOCH;

use maze::animate::*;
use maze::generate::*;

const MAZE_WIDTH: usize = 38;
const MAZE_HEIGHT: usize = 20;
const SCENE_TIMEOUT: u32 = 60;
const EXPORTING: bool = false;

struct Model {
    animators: VecDeque<Box<dyn Animator>>,
    current_animator: Box<dyn Animator>,
    frames_folder: PathBuf,
}

fn main() {
    nannou::app(model).update(update).run();
}

fn add_generator<T: 'static>(
    animators: &mut VecDeque<Box<dyn Animator>>,
    generator: T,
    start: (usize, usize),
    end: (usize, usize),
) where
    T: MazeGenerator,
{
    let animator: Box<dyn Animator> = Box::new(MazeAnimator::new(generator, start, end));
    animators.push_back(animator);
    animators.push_back(Box::new(WaitingAnimator::new(SCENE_TIMEOUT)));
}

fn get_frames_folder(app: &App) -> PathBuf {
    let timestamp = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .expect("Could not get timestamp")
        .as_millis();

    app.project_path()
        .expect("Could not get project_path")
        .join(format!("frames_{}", timestamp))
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

    add_generator(
        &mut animators,
        RecursiveBacktrackingGenerator::new(MAZE_WIDTH, MAZE_HEIGHT),
        (0, 0),
        (MAZE_WIDTH - 1, MAZE_HEIGHT - 1),
    );
    add_generator(
        &mut animators,
        KruskalsGenerator::new(MAZE_WIDTH, MAZE_HEIGHT),
        (MAZE_WIDTH - 1, MAZE_HEIGHT - 1),
        (0, 0),
    );
    add_generator(
        &mut animators,
        BinaryTreeGenerator::new(MAZE_WIDTH, MAZE_HEIGHT),
        (0, 0),
        (MAZE_WIDTH - 1, MAZE_HEIGHT - 1),
    );
    add_generator(
        &mut animators,
        RecursiveDivisionGenerator::new(MAZE_WIDTH, MAZE_HEIGHT),
        (MAZE_WIDTH - 1, MAZE_HEIGHT - 1),
        (0, 0),
    );

    let current_animator = animators.pop_front().unwrap();

    Model {
        animators,
        current_animator,
        frames_folder: get_frames_folder(app),
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

    draw.to_frame(app, &frame).unwrap();

    if EXPORTING {
        let file = format!("frame_{}.png", frame.nth());
        app.main_window()
            .capture_frame(model.frames_folder.join(file));
    }
}
