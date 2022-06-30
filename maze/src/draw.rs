use nannou::prelude::*;

use crate::maze::{Maze, Wall};
use crate::maze::wall::Direction::*;

pub struct Draw<'a> {
    draw: &'a nannou::Draw,
    maze: &'a Maze,
    color: Rgb8,
    wall_length: f32
}

impl<'a> Draw<'a> {
    pub fn new(
        draw: &'a nannou::Draw,
        maze: &'a Maze,
        color: Rgb8,
        wall_length: f32) -> Draw<'a>
    {
        Draw {
            draw,
            maze,
            color,
            wall_length
        }
    }

    pub fn wall(&self, wall: &Wall) {
        let maze_width = self.maze.width() as f32 * self.wall_length;
        let maze_height = self.maze.height() as f32 * self.wall_length;

        let maze_rect = Rect::from_w_h(maze_width, maze_height);

        let &Wall {x, y, ..} = wall;
        let cell = Rect::from_w_h(self.wall_length, self.wall_length)
            .top_left_of(maze_rect)
            .shift_x(x as f32 * self.wall_length)
            .shift_y(y as f32 * -self.wall_length);

        let (start, end) = match wall.dir {
            Up => (cell.top_left(), cell.top_right()),
            Down => (cell.bottom_left(), cell.bottom_right()),
            Left => (cell.top_left(), cell.bottom_left()),
            Right => (cell.top_right(), cell.bottom_right()),
        };

        self.draw.line()
            .start(start)
            .end(end)
            .color(self.color)
            .weight(3.0);
    }
}


