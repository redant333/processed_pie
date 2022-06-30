pub mod maze;
pub use crate::maze::maze::Maze;

pub mod wall;
pub use crate::maze::wall::Wall;

pub mod iterator;
pub use crate::maze::iterator::WallIterator;

#[cfg(test)]
mod tests {
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
        assert_eq!(maze.get_wall(&Wall::Right{x:0, y:0}), false);
    }

    #[test]
    fn maze_get_wall_returns_true_when_maze_constructed_with_walls_on() {
        let maze = Maze::new(2, 2, true);
        assert_eq!(maze.get_wall(&Wall::Right{x:0, y:0}), true);
    }

    #[test]
    fn maze_set_wall_changes_wall_state() {
        let mut maze = Maze::new(2, 2, false);
        let wall = Wall::Left { x: 1, y: 0 };

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
    fn mase_set_wall_sets_exactly_one_wall() {
        let mut maze = Maze::new(10, 10, false);
        let wall = Wall::Left { x: 5, y: 5 };

        maze.set_wall(&wall, true);
        let maze = maze;

        let on_count = maze.wall_iter()
            .filter(|wall| maze.get_wall(wall))
            .count();

        assert_eq!(on_count, 1);
    }
}