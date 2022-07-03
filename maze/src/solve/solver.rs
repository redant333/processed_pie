use crate::maze::{wall::Direction::*, Wall};
use std::collections::{HashMap, HashSet};

use crate::maze::Maze;

fn get_reachable_cells(maze: &Maze, cell: (usize, usize)) -> Vec<(usize, usize)> {
    let (x, y) = cell;

    vec![
        (x + 1, y, Right),
        (x.wrapping_sub(1), y, Left),
        (x, y + 1, Down),
        (x, y.wrapping_sub(1), Up),
    ]
    .into_iter()
    .filter(|(x, y, _)| (0..maze.width()).contains(x) && (0..maze.height()).contains(y))
    .filter(|&(_, _, dir)| maze.get_wall(&Wall { x, y, dir }) != true)
    .map(|(x, y, _)| (x, y))
    .collect()
}

pub fn solve(maze: &Maze, start: (usize, usize), end: (usize, usize)) -> Vec<(usize, usize)> {
    let mut came_from = HashMap::new();
    let mut checked_cells = HashSet::new();
    // Solve the maze backwards to make the path creation easier
    let mut cells_to_check = vec![end];

    while !came_from.contains_key(&start) {
        let cell = cells_to_check.pop().unwrap();
        checked_cells.insert(cell);

        let unchecked_reachable_cells = get_reachable_cells(maze, cell)
            .into_iter()
            .filter(|cell| !checked_cells.contains(cell));

        for cell_to_check in unchecked_reachable_cells {
            cells_to_check.push(cell_to_check);
            came_from.insert(cell_to_check, cell);
        }
    }

    let mut travel_path = vec![start];
    while *travel_path.last().unwrap() != end {
        let next_cell = came_from.get(travel_path.last().unwrap()).unwrap();
        travel_path.push(*next_cell);
    }
    travel_path
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn get_reachable_cells_should_return_all_neighbors_when_there_are_no_walls() {
        let maze = Maze::new(3, 3, false);
        let expected = vec![(0, 1), (1, 0), (1, 2), (2, 1)];

        let mut reachable = get_reachable_cells(&maze, (1, 1));
        reachable.sort();

        assert_eq!(reachable, expected);
    }

    #[test]
    fn get_reachable_cells_works_for_edge_cells() {
        let maze = Maze::new(2, 2, false);
        let expected = vec![(0, 1), (1, 0)];

        let mut reachable = get_reachable_cells(&maze, (1, 1));
        reachable.sort();

        assert_eq!(reachable, expected);
    }

    #[test]
    fn get_reachable_cells_returns_correct_neighbors_when_there_are_walls() {
        let mut maze = Maze::new(2, 2, false);
        maze.set_wall(
            &Wall {
                x: 0,
                y: 0,
                dir: Right,
            },
            true,
        );

        let expected = vec![(0, 1)];

        assert_eq!(get_reachable_cells(&maze, (0, 0)), expected);
    }

    #[test]
    fn solve_works_for_two_by_two_maze() {
        let mut maze = Maze::new(2, 2, false);
        maze.set_wall(&Wall {x: 0, y: 0, dir: Right}, true);

        let start = (0, 0);
        let end = (1, 0);
        let expected = vec![(0, 0), (0, 1), (1, 1), (1, 0)];

        assert_eq!(solve(&maze, start, end), expected);
    }

    #[test]
    fn solve_works_for_three_by_three_maze() {
        let mut maze = Maze::new(3, 3, false);
        maze.set_wall(&Wall {x: 1, y: 0, dir: Left}, true);
        maze.set_wall(&Wall {x: 1, y: 0, dir: Right}, true);
        maze.set_wall(&Wall {x: 1, y: 2, dir: Left}, true);
        maze.set_wall(&Wall {x: 1, y: 2, dir: Right}, true);

        let start = (0, 0);
        let end = (2, 2);
        let expected = vec![(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)];

        assert_eq!(solve(&maze, start, end), expected);
    }
}
