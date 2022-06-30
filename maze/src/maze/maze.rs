use super::{WallIterator, Wall};

pub struct Maze {
    width: usize,
    height: usize,
    vertical_walls: Vec<Vec<bool>>,
    horizontal_walls: Vec<Vec<bool>>,
}

impl Maze {
    pub fn new(width: usize, height: usize, walls_on: bool) -> Maze {
        let vertical_walls = vec![vec![walls_on; height]; width + 1];
        let horizontal_walls = vec![vec![walls_on; height + 1]; width];

        Maze {
            width,
            height,
            vertical_walls,
            horizontal_walls,
        }
    }

    pub fn width(&self) -> usize { self.width }

    pub fn height(&self) -> usize { self.height }

    pub fn wall_iter(&self) -> WallIterator {
        WallIterator::new(self)
    }

    pub fn set_wall(&mut self, wall: &Wall, on: bool) {
        match wall {
            &Wall::Up { x, y }    => self.horizontal_walls[x][y] = on,
            &Wall::Down { x, y }  => self.horizontal_walls[x][y+1] = on,
            &Wall::Left { x, y }  => self.vertical_walls[x+1][y] = on,
            &Wall::Right { x, y } => self.vertical_walls[x][y] = on,
        }
    }

    pub fn get_wall(&self, wall: &Wall) -> bool {
        match wall {
            &Wall::Up { x, y }    => self.horizontal_walls[x][y],
            &Wall::Down { x, y }  => self.horizontal_walls[x][y+1],
            &Wall::Left { x, y }  => self.vertical_walls[x+1][y],
            &Wall::Right { x, y } => self.vertical_walls[x][y],
        }
    }
}