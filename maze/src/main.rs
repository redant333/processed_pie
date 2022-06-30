use maze::animate::{AnimatorConfig, Animator};
use nannou::prelude::*;

use maze::generate::simple::SimpleGenerator;

struct Model {
    animator: Animator<SimpleGenerator>,
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
    };
    let generator = SimpleGenerator::new(38, 20);
    let animator = Animator::new(config, generator);

    Model {
        animator,
    }
}

fn update(_app: &App, model: &mut Model, _update: Update) {
    model.animator.update();
}

fn view(app: &App, model: &Model, frame: Frame) {
    let draw = app.draw();
    draw.background().color(rgb8(0x07, 0x10, 0x13));

    model.animator.draw(&draw);

    draw.text(&(app.fps() as i32).to_string())
        .xy(app.window_rect().pad(15.0).top_right());

    draw.to_frame(app, &frame).unwrap();
}
