use std::{
    cell::RefCell,
    collections::{HashMap, HashSet}, rc::Rc,
};

use nannou::rand::prelude::{SliceRandom, ThreadRng};

use crate::maze::wall::Direction::*;
use crate::maze::{Maze, Wall};

use super::MazeGenerator;

pub struct KruskalsGenerator {
    width: usize,
    height: usize,
    sets: HashMap<(usize, usize), Rc<RefCell<HashSet<(usize, usize)>>>>,
    walls: Vec<Wall>,
}

impl KruskalsGenerator {
    pub fn new(width: usize, height: usize) -> KruskalsGenerator {
        let sets = create_sets(width, height);
        let walls = create_walls(width, height);

        KruskalsGenerator {
            width,
            height,
            sets,
            walls,
        }
    }

    fn get_cells(&self, wall: &Wall) -> ((usize, usize), (usize, usize)) {
        match wall {
            &Wall { x, y, dir: Down } => ((x, y), (x, y + 1)),
            &Wall { x, y, dir: Right } => ((x, y), (x + 1, y)),
            _ => panic!("Walls should be generated with only Down and Right dir."),
        }
    }

    fn try_remove(&mut self, wall: &Wall) -> bool {
        let (cell1, cell2) = self.get_cells(wall);

        let cell1_set = self.sets.get(&cell1).unwrap();
        if cell1_set.borrow().contains(&cell2) {
            return false
        }

        let cell1_set = self.sets.remove(&cell1).unwrap();
        let cell2_set = Rc::clone(self.sets.get(&cell2).unwrap());

        cell2_set.borrow_mut().extend(cell1_set.borrow().iter());
        for cell in cell1_set.borrow().iter() {
            self.sets.insert(*cell, Rc::clone(&cell2_set));
        }

        true
    }
}

fn create_walls(width: usize, height: usize) -> Vec<Wall> {
    let mut walls = vec![];

    for (x, y) in itertools::iproduct!(0..width, 0..height - 1) {
        walls.push(Wall { x, y, dir: Down });
    }

    for (x, y) in itertools::iproduct!(0..width - 1, 0..height) {
        walls.push(Wall { x, y, dir: Right });
    }

    walls.shuffle(&mut ThreadRng::default());

    walls
}

fn create_sets(
    width: usize,
    height: usize,
) -> HashMap<(usize, usize), Rc<RefCell<HashSet<(usize, usize)>>>> {
    itertools::iproduct!(0..width, 0..height)
        .map(|position| {
            let set = Rc::new(RefCell::new(HashSet::new()));
            set.borrow_mut().insert(position);

            (position, set)
        })
        .collect()
}

impl MazeGenerator for KruskalsGenerator {
    fn width(&self) -> usize {
        self.width
    }

    fn height(&self) -> usize {
        self.height
    }

    fn initial_maze(&self) -> crate::maze::Maze {
        Maze::new_with_edges(self.width, self.height, true)
    }

    fn name(&self) -> String {
        "Kruskal's Algorithm".to_string()
    }
}

impl Iterator for KruskalsGenerator {
    type Item = (Wall, bool);

    fn next(&mut self) -> Option<Self::Item> {
        loop {
            let wall = self.walls.pop()?;

            if self.try_remove(&wall) {
                return Some((wall, false));
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn create_walls_should_return_appropriate_number_of_walls() {
        let walls = create_walls(3, 3);
        assert_eq!(walls.len(), 12);
    }

    #[test]
    fn create_sets_should_return_appropriate_number_of_sets() {
        let sets = create_sets(3, 3);
        assert_eq!(sets.len(), 9);
    }

    #[test]
    fn create_sets_should_return_sets_with_size_one() {
        let sets = create_sets(3, 3);

        for (_, set) in sets.into_iter() {
            assert_eq!(set.borrow().len(), 1);
        }
    }
}
