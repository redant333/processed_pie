use maze::draw::Draw;
use nannou::prelude::*;

use maze::maze::{Maze};
use maze::generate::simple::SimpleGenerator;

struct Model {
    back_color: Rgb8,
    wall_color: Rgb8,
    maze: Maze,
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

    let mut maze = Maze::new_with_edges(38, 20, false);
    let generator = SimpleGenerator::new(38, 20);

    for (wall, state) in generator {
        maze.set_wall(&wall, state);
    }

    Model {
        back_color: rgb8(0x07, 0x10, 0x13),
        wall_color: rgb8(0x01, 0x97, 0xf6),
        maze,
    }
}

fn update(_app: &App, _model: &mut Model, _update: Update) {}

fn view(app: &App, model: &Model, frame: Frame) {
    let draw = app.draw();
    draw.background().color(model.back_color);

    let maze_draw = Draw::new(&draw, &model.maze, model.wall_color, 32.0);

    for wall in model.maze.wall_iter() {
        maze_draw.wall(&wall);
    }

    draw.to_frame(app, &frame).unwrap();
}
