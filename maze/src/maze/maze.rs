use super::{WallIterator, Wall};
use super::{wall::Direction::*};

pub struct Maze {
    width: usize,
    height: usize,
    vertical_walls: Vec<Vec<bool>>,
    horizontal_walls: Vec<Vec<bool>>,
}

impl Maze {
    pub fn new(width: usize, height: usize, walls_on: bool) -> Maze {
        assert!(width > 1);
        assert!(height > 1);

        let vertical_walls = vec![vec![walls_on; height]; width + 1];
        let horizontal_walls = vec![vec![walls_on; height + 1]; width];

        Maze {
            width,
            height,
            vertical_walls,
            horizontal_walls,
        }
    }

    pub fn new_with_edges(width: usize, height: usize, walls_on: bool) -> Maze {
        let mut maze = Maze::new(width, height, walls_on);

        for i in maze.vertical_walls.first_mut().unwrap() {
            *i = true;
        }

        for i in maze.vertical_walls.last_mut().unwrap() {
            *i = true;
        }

        for row in &mut maze.horizontal_walls {
            *row.first_mut().unwrap() = true;
            *row.last_mut().unwrap() = true;
        }

        maze
    }

    pub fn width(&self) -> usize { self.width }

    pub fn height(&self) -> usize { self.height }

    pub fn wall_iter(&self) -> WallIterator {
        WallIterator::new(self)
    }

    pub fn set_wall(&mut self, wall: &Wall, on: bool) {
        match wall {
            &Wall { x, y, dir: Up } => self.horizontal_walls[x][y] = on,
            &Wall { x, y, dir: Down } => self.horizontal_walls[x][y+1] = on,
            &Wall { x, y, dir: Left } => self.vertical_walls[x][y] = on,
            &Wall { x, y, dir: Right } => self.vertical_walls[x+1][y] = on,
        }
    }

    pub fn get_wall(&self, wall: &Wall) -> bool {
        match wall {
            &Wall { x, y, dir: Up } => self.horizontal_walls[x][y],
            &Wall { x, y, dir: Down } => self.horizontal_walls[x][y+1],
            &Wall { x, y, dir: Left } => self.vertical_walls[x][y],
            &Wall { x, y, dir: Right } => self.vertical_walls[x+1][y],
        }
    }
}