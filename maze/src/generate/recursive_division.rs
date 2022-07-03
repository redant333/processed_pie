use nannou::rand::random_range;

use crate::maze::wall::Direction::*;
use crate::maze::{Maze, Wall};

use super::MazeGenerator;

#[derive(Debug)]
struct Field {
    x: usize,
    y: usize,
    width: usize,
    height: usize,
}

impl Field {
    fn split_vertically(self) -> (Field, Field) {
        let left_width = random_range(1, self.width);
        let left = Field {
            x: self.x,
            y: self.y,
            width: left_width,
            height: self.height,
        };
        let right = Field {
            x: self.x + left_width,
            y: self.y,
            width: self.width - left_width,
            height: self.height,
        };

        (left, right)
    }

    fn split_horizontally(self) -> (Field, Field) {
        let top_height = random_range(1, self.height);
        let top = Field {
            x: self.x,
            y: self.y,
            width: self.width,
            height: top_height,
        };
        let bottom = Field {
            x: self.x,
            y: self.y + top_height,
            width: self.width,
            height: self.height - top_height,
        };

        (top, bottom)
    }

    fn is_splittable(&self) -> bool {
        self.width > 1 || self.height > 1
    }
}

pub struct RecursiveDivisionGenerator {
    width: usize,
    height: usize,
    pending_stack: Vec<(Wall, bool)>,
    field_stack: Vec<Field>,
}

impl RecursiveDivisionGenerator {
    pub fn new(width: usize, height: usize) -> Self {
        let field_stack = vec![Field {
            x: 0,
            y: 0,
            width,
            height,
        }];

        Self {
            width,
            height,
            pending_stack: Vec::new(),
            field_stack,
        }
    }

    fn split_vertically(&mut self, field: Field) {
        let (left, right) = field.split_vertically();
        let split_x = left.x + left.width - 1;

        if left.height > 1 {
            let gap_y = random_range(left.y, left.y + left.height);
            let gap_wall = Wall {
                x: split_x,
                y: gap_y,
                dir: Right,
            };

            // Since this is a stack, push the wall gap first
            self.pending_stack.push((gap_wall, false));

            // Add the split walls
            self.pending_stack
                .extend((left.y..(left.y + left.height)).rev().map(|y| {
                    (
                        Wall {
                            x: split_x,
                            y,
                            dir: Right,
                        },
                        true,
                    )
                }));
        }

        // Add the split fields to stack
        if left.is_splittable() {
            self.field_stack.push(left);
        }
        if right.is_splittable() {
            self.field_stack.push(right);
        }
    }

    fn split_horizontally(&mut self, field: Field) {
        let (top, bottom) = field.split_horizontally();
        let split_y = top.y + top.height - 1;

        if top.width > 1 {
            let gap_x = random_range(top.x, top.x + top.width);
            let gap_wall = Wall {
                x: gap_x,
                y: split_y,
                dir: Down,
            };

            // Since this is a stack, push the wall gap first
            self.pending_stack.push((gap_wall, false));

            // Add the split walls
            self.pending_stack
                .extend((top.x..(top.x + top.width)).rev().map(|x| {
                    (
                        Wall {
                            x,
                            y: split_y,
                            dir: Down,
                        },
                        true,
                    )
                }));
        }

        // Add the split fields to stack
        if top.is_splittable() {
            self.field_stack.push(top);
        }
        if bottom.is_splittable() {
            self.field_stack.push(bottom);
        }
    }
}

impl MazeGenerator for RecursiveDivisionGenerator {
    fn width(&self) -> usize {
        self.width
    }

    fn height(&self) -> usize {
        self.width
    }

    fn initial_maze(&self) -> crate::maze::Maze {
        Maze::new_with_edges(self.width, self.height, false)
    }

    fn name(&self) -> String {
        "Recursive Division Algorithm".to_string()
    }
}

impl Iterator for RecursiveDivisionGenerator {
    type Item = (Wall, bool);

    fn next(&mut self) -> Option<Self::Item> {
        if self.pending_stack.is_empty() {
            let field = self.field_stack.pop()?;

            if field.width > field.height {
                self.split_vertically(field);
            } else {
                self.split_horizontally(field);
            }
        }

        self.pending_stack.pop()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn field_vertical_split_should_split_the_width() {
        let field = Field {
            x: 0,
            y: 0,
            width: 5,
            height: 5,
        };
        let (left, right) = field.split_vertically();

        assert_eq!(left.width + right.width, 5);
    }

    #[test]
    fn field_vertical_split_should_work_with_width_two() {
        let field = Field {
            x: 0,
            y: 0,
            width: 2,
            height: 5,
        };
        let (left, right) = field.split_vertically();

        assert_eq!(left.width, 1);
        assert_eq!(left.x, 0);

        assert_eq!(right.width, 1);
        assert_eq!(right.x, 1);
    }

    #[test]
    fn field_horizontal_split_should_split_the_height() {
        let field = Field {
            x: 0,
            y: 0,
            width: 5,
            height: 5,
        };
        let (top, bottom) = field.split_horizontally();

        assert_eq!(top.height + bottom.height, 5);
    }

    #[test]
    fn field_horizontal_split_should_work_with_height_two() {
        let field = Field {
            x: 0,
            y: 0,
            width: 5,
            height: 2,
        };
        let (top, bottom) = field.split_horizontally();

        assert_eq!(top.height, 1);
        assert_eq!(top.y, 0);

        assert_eq!(bottom.height, 1);
        assert_eq!(bottom.y, 1);
    }
}
