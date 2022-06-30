pub mod maze;
pub use crate::maze::maze::Maze;

pub mod wall;
pub use crate::maze::wall::Wall;

pub mod iterator;
pub use crate::maze::iterator::WallIterator;

#[cfg(test)]
mod tests {
    use crate::maze::wall::Direction::*;

    use super::*;

    #[test]
    fn maze_returns_appropriate_size_after_construction() {
        let maze = Maze::new(5, 6, false);
        assert_eq!(maze.width(), 5);
        assert_eq!(maze.height(), 6);
    }

    #[test]
    fn maze_get_wall_returns_false_when_maze_constructed_with_walls_off() {
        let maze = Maze::new(2, 2, false);
        assert_eq!(maze.get_wall(&Wall {x:0, y:0, dir: Right}), false);
    }

    #[test]
    fn maze_get_wall_returns_true_when_maze_constructed_with_walls_on() {
        let maze = Maze::new(2, 2, true);
        assert_eq!(maze.get_wall(&Wall {x:0, y:0, dir: Right}), true);
    }

    #[test]
    fn maze_set_wall_changes_wall_state() {
        let mut maze = Maze::new(2, 2, false);
        let wall = Wall{ x: 1, y: 0, dir: Left };

        maze.set_wall(&wall, true);
        let maze = maze;

        assert_eq!(maze.get_wall(&wall), true);
    }

    #[test]
    fn maze_returns_iterator_with_appropriate_count() {
        let maze = Maze::new(2, 2, false);
        let iter = maze.wall_iter();

        assert_eq!(iter.count(), 12);
    }

    #[test]
    fn maze_set_wall_sets_exactly_one_wall() {
        let mut maze = Maze::new(10, 10, false);
        let wall = Wall { x: 5, y: 5, dir: Left };

        maze.set_wall(&wall, true);
        let maze = maze;

        let on_count = maze.wall_iter()
            .filter(|wall| maze.get_wall(wall))
            .count();

        assert_eq!(on_count, 1);
    }

    #[test]
    fn maze_set_wall_can_set_all_walls() {
        let mut maze = Maze::new(3, 2, false);

        for (x, y) in itertools::iproduct!(0..3, 0..2) {
            maze.set_wall(&Wall {x, y, dir: Up}, true);
            maze.set_wall(&Wall {x, y, dir: Down}, true);
            maze.set_wall(&Wall {x, y, dir: Left}, true);
            maze.set_wall(&Wall {x, y, dir: Right}, true);
        }
        let maze = maze;

        let on_count = maze.wall_iter()
            .filter(|wall| maze.get_wall(wall))
            .count();

        assert_eq!(on_count, 17);
    }

    #[test]
    fn maze_can_be_constructed_with_edges() {
        let maze = Maze::new_with_edges(10, 10, false);

        let on_count = maze.wall_iter()
            .filter(|wall| maze.get_wall(wall))
            .count();

        assert_eq!(on_count, 40);
    }
}