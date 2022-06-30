use super::{Wall, Maze};

pub struct WallIterator<'a> {
    iter: Box<dyn Iterator<Item=Wall> + 'a>
}

impl<'a> WallIterator<'a> {
    pub fn new(maze: &'a Maze) -> WallIterator {
        let left_edge_iter = (0..maze.height()).map(|y| Wall::Left { x: 0, y: y });
        let top_edge_iter = (0..maze.width()).map(|x| Wall::Up { x, y: 0 });
        let right_iter = itertools::iproduct!(0..maze.width(), 0..maze.height())
            .map(|(x, y)| Wall::Right { x, y });
        let down_iter = itertools::iproduct!(0..maze.width(), 0..maze.height())
            .map(|(x, y)| Wall::Down { x, y });

        let iter = left_edge_iter
            .chain(top_edge_iter)
            .chain(right_iter)
            .chain(down_iter);

        WallIterator {
            iter: Box::new(iter),
        }
    }
}

impl<'a> Iterator for WallIterator<'a> {
    type Item = Wall;

    fn next(&mut self) -> Option<Self::Item> {
        self.iter.next()
    }
}