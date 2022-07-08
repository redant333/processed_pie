use maze::{animate::{AnimatorConfig, MazeGenerationAnimator, MazeSolutionAnimator}, generate::{recursive_division::RecursiveDivisionGenerator}};
use nannou::{prelude::*};

struct Model {
    animator: MazeGenerationAnimator<RecursiveDivisionGenerator>,
    solution_animator: Option<MazeSolutionAnimator>,
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
        .unwrap();

    let config = AnimatorConfig {
        back_color: rgb8(0x07, 0x10, 0x13),
        wall_color: rgb8(0x01, 0x97, 0xf6),
        wall_size: 32.0,
        y: 8.0,
    };
    let generator = RecursiveDivisionGenerator::new(38, 20);
    let animator = MazeGenerationAnimator::new(config, generator);

    Model {
        animator,
        solution_animator: None,
    }
}

fn update(_app: &App, model: &mut Model, _update: Update) {
    model.animator.update();
    if model.animator.maze_completed && model.solution_animator.is_none() {
        model.solution_animator = Some(MazeSolutionAnimator::new(
            model.animator.get_maze().unwrap(),
            32.0,
            model.animator.top_left_cell(),
            (0, 0),
            (37, 19)));
    }
}

fn view(app: &App, model: &Model, frame: Frame) {
    let draw = app.draw();
    draw.background().color(rgb8(0x07, 0x10, 0x13));

    model.animator.draw(&draw);
    if model.solution_animator.is_some() {
        model.solution_animator.as_ref().unwrap().draw(&draw);
    }

    draw.text(&(app.fps() as i32).to_string())
        .xy(app.window_rect().pad(15.0).top_right());

    draw.to_frame(app, &frame).unwrap();
}
