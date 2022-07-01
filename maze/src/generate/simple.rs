use crate::maze::{Wall, Maze};
use crate::maze::wall::Direction::*;

use super::MazeGenerator;

pub struct SimpleGenerator {
    width: usize,
    height: usize,
    x_index: usize,
    y_index: usize,
}

impl SimpleGenerator {
    pub fn new(width: usize, height: usize) -> SimpleGenerator {
        SimpleGenerator {
            width,
            height,
            x_index: 0,
            y_index: 0,
        }
    }
}

impl Iterator for SimpleGenerator {
    type Item = (Wall, bool);

    fn next(&mut self) -> Option<Self::Item> {
        if self.x_index >= self.width - 1 {
            return None;
        }

        let new_wall = Wall {x:self.x_index, y:self.y_index + self.x_index % 2, dir: Right};
        self.y_index += 1;

        if self.y_index >= self.height - 1 {
            self.y_index = 0;
            self.x_index += 1;
        }

        Some((new_wall, true))
    }
}

impl MazeGenerator for SimpleGenerator {
    fn width(&self) -> usize {
        self.width
    }

    fn height(&self) -> usize {
        self.height
    }

    fn initial_maze(&self) -> crate::maze::Maze {
        Maze::new_with_edges(self.width, self.height, false)
    }

    fn name(&self) -> String {
        "Simple Dummy Algorithm".to_string()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn simple_generator_should_output_one_value_for_two_by_two() {
        let generator = SimpleGenerator::new(2, 2);
        let walls = generator.count();

        assert_eq!(walls, 1);
    }

    #[test]
    fn simple_generator_should_output_four_values_for_three_by_three() {
        let generator = SimpleGenerator::new(3, 3);
        let walls = generator.count();

        assert_eq!(walls, 4);
    }

    #[test]
    fn simple_generator_should_not_return_too_large_values() {
        let generator = SimpleGenerator::new(20, 10);

        for (wall, _) in generator {
            assert!(wall.x < 20);
            assert!(wall.y < 10);
        }
    }
}