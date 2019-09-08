from random import choice

BLOCK_SIZE = 10


class Labyrinth(object):
    START = 0
    WALL = 1
    PATH = 2
    END = 4

    def __init__(self, w, h):
        if w % 2 == 0 or h % 2 == 0:
            raise ValueError("Width and height must be odd numbers")

        self._width = w
        self._height = h
        self._cells = self._generate_labyrinth(w, h)

    @property
    def w(self):
        return self._width

    @property
    def h(self):
        return self._height

    def _generate_labyrinth(self, w, h):
        cells = [[Labyrinth.WALL] * w for _ in range(h)]

        cells[1][0] = Labyrinth.START
        cells[-2][-1] = Labyrinth.END

        def unvisited_neighbors(x, y):
            potential_neighbors = [(x-2, y), (x+2, y), (x, y+2), (x, y-2)]
            neighbors = [(neighbor_x, neighbor_y)
                         for (neighbor_x, neighbor_y) in potential_neighbors
                         if 1 <= neighbor_x < self._width - 1 and
                         1 <= neighbor_y < self._height - 1 and
                         cells[neighbor_y][neighbor_x] == Labyrinth.WALL]
            return neighbors

        (x, y) = (1, 1)
        cells[y][x] = Labyrinth.PATH
        stack = []
        while True:
            neighbors = unvisited_neighbors(x, y)

            if neighbors:
                (neighbor_x, neighbor_y) = choice(neighbors)
                cells[neighbor_y][neighbor_x] = Labyrinth.PATH

                if x == neighbor_x:
                    cells[x][(y+neighbor_y)/2] = Labyrinth.PATH
                elif y == neighbor_y:
                    cells[(x+neighbor_x)/2][y] = Labyrinth.PATH

                stack.append((x, y))
                (x, y) = (neighbor_x, neighbor_y)
            elif stack:
                (x, y) = stack.pop()
            else:
                break

        return cells

    def get(self, x, y):
        if 0 <= x < self._width and 0 <= y < self._height:
            return self._cells[y][x]
        else:
            return None

    def to_shape(self):
        ret = createShape(GROUP)
        for x in range(self._width):
            for y in range(self._height):
                val = self._cells[y][x]
                block_color = None
                block_height = BLOCK_SIZE

                if val == Labyrinth.START:
                    block_color = color(255, 0, 0)
                elif val == Labyrinth.END:
                    block_color = color(0, 255, 0)
                elif val == Labyrinth.WALL:
                    block_color = color(5, 99, 8)
                    block_height = 2 * BLOCK_SIZE
                elif val == Labyrinth.PATH:
                    block_color = color(200, 200, 0)

                new_box = createShape(
                    BOX, BLOCK_SIZE, BLOCK_SIZE, block_height)
                new_box.setFill(block_color)
                new_box.setStroke(color(0, 255, 0))
                new_box.setStrokeWeight(4)
                new_box.translate(x * BLOCK_SIZE, y *
                                  BLOCK_SIZE, block_height/2)
                ret.addChild(new_box)
        return ret

    def paint(self):
        noStroke()
        segment_size = 10
        for y in range(self._height):
            for x in range(self._width):
                fill_color = None
                if self._cells[y][x] == Labyrinth.START:
                    fill_color = color(255, 0, 0)
                elif self._cells[y][x] == Labyrinth.END:
                    fill_color = color(0, 255, 0)
                elif self._cells[y][x] == Labyrinth.WALL:
                    fill_color = color(100, 100, 100)
                elif self._cells[y][x] == Labyrinth.PATH:
                    fill_color = color(200, 200, 0)

                fill(fill_color)
                rect(x * segment_size, y * segment_size,
                     segment_size, segment_size)


class Tween(object):
    def __init__(self, from_val, to_val, frames, update_function=None):
        self._from_val = from_val
        self._to_val = to_val
        self._frames = frames
        self._frames_elapsed = 0
        self._update_function = update_function
        self._finished = False

    def update(self):
        self._frames_elapsed += 1

        if self._update_function:
            self._update_function(self.value)

        if self._frames == self._frames_elapsed:
            self._finished = True

    @property
    def value(self):
        return map(self._frames_elapsed, 0, self._frames, self._from_val, self._to_val)

    @property
    def finished(self):
        return self._finished


class Player(object):
    X_PLUS = 0
    Y_PLUS = 1
    X_MINUS = 2
    Y_MINUS = 3

    def __init__(self, labyrinth):
        self._labyrinth = labyrinth
        self._tweens = []

        self._x = 0
        self._y = 1
        self._direction = Player.X_PLUS

        self._geometry_x = self._x * BLOCK_SIZE
        self._geometry_y = self._y * BLOCK_SIZE
        self._geometry_direction = 0

    def move(self):
        if self._tweens:
            return

        def set_geometry_x(new_value):
            self._geometry_x = new_value

        def set_geometry_y(new_value):
            self._geometry_y = new_value

        offsets = {
            Player.X_PLUS: 1, Player.X_MINUS: -1, Player.Y_PLUS: 1, Player.Y_MINUS: -1
        }

        geometry = None
        set_geometry_function = None
        new_x = self._x
        new_y = self._y
        offset = offsets[self._direction] * BLOCK_SIZE

        if self._direction == Player.X_PLUS or self._direction == Player.X_MINUS:
            geometry = self._geometry_x
            set_geometry_function = set_geometry_x
            new_x = new_x + offsets[self._direction]
        else:
            geometry = self._geometry_y
            set_geometry_function = set_geometry_y
            new_y = new_y + offsets[self._direction]

        if self._labyrinth.get(new_x, new_y) in [Labyrinth.WALL, None]:
            return

        self._x = new_x
        self._y = new_y

        self._tweens.append(
            Tween(geometry, geometry + offset, 15, set_geometry_function))

    @property
    def geometry_direction(self):
        return self._geometry_direction

    @property
    def geometry_x(self):
        return self._geometry_x

    @property
    def geometry_y(self):
        return self._geometry_y

    def rotate_right(self):
        if self._tweens:
            return

        def set_direction(new_direction):
            self._geometry_direction = new_direction

        new_direction = (self._direction + 1) % 4
        self._tweens.append(Tween(self._geometry_direction,
                                  new_direction * PI/2, 30, set_direction))
        self._direction = new_direction

    def rotate_left(self):
        if self._tweens:
            return

        def set_direction(new_direction):
            self._geometry_direction = new_direction

        new_direction = (self._direction - 1) % 4

        self._tweens.append(Tween(self._geometry_direction,
                                  new_direction * PI/2, 30, set_direction))
        self._direction = new_direction

    def update(self):
        for tween in self._tweens:
            tween.update()

        self._tweens = filter(lambda tween: not tween.finished, self._tweens)

    def paint(self):
        pushMatrix()
        fill(200, 200, 200)
        translate(self._geometry_x, self._geometry_y, BLOCK_SIZE)
        sphere(0.4 * BLOCK_SIZE)
        popMatrix()


labyrinth = None
labyrinth_shape = None
player = None


def setup():
    size(1280, 720, P3D)
    noStroke()
    background(0)

    global labyrinth
    labyrinth = Labyrinth(31, 31)

    global labyrinth_shape
    labyrinth_shape = labyrinth.to_shape()

    global player
    player = Player(labyrinth)


def draw():
    background(0)
    lights()

    player.update()

    planar_camera_vector = PVector(-50, 0)
    planar_camera_vector.rotate(player.geometry_direction)
    camera(player.geometry_x + planar_camera_vector.x, player.geometry_y + planar_camera_vector.y, 100,
           player.geometry_x, player.geometry_y, 0, 0, 0, -1)

    player.paint()
    shape(labyrinth_shape)


def keyPressed():
    if keyCode == UP:
        player.move()
    elif keyCode == LEFT:
        player.rotate_left()
    elif keyCode == RIGHT:
        player.rotate_right()
