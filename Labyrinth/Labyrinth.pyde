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
        return self._cells[y][x]

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
                    block_color = color(100, 100, 100)
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
    def __init__(self, x, y, geometry_x, geometry_y):
        self.x = x
        self.y = y
        self.geometry_x = geometry_x
        self.geometry_y = geometry_y

    def paint(self):
        pushMatrix()
        fill(200, 200, 200)
        translate(self.geometry_x, self.geometry_y, BLOCK_SIZE)
        sphere(0.4 * BLOCK_SIZE)
        popMatrix()


labyrinth = None
labyrinth_shape = None
player = None
rotation = 0

tweens = []


def setup():
    size(1280, 720, P3D)
    noStroke()
    background(0)

    global labyrinth
    labyrinth = Labyrinth(31, 31)

    global labyrinth_shape
    labyrinth_shape = labyrinth.to_shape()

    global player
    player = Player(0, 1, 0, BLOCK_SIZE)


def draw():
    camera(player.geometry_x - 50, player.geometry_y , 100, player.geometry_x + 50, player.geometry_y, 0, 0, 0, -1)
    background(0)
    lights()

    global tweens
    for tween in tweens:
        tween.update()
    tweens = filter(lambda tween: not tween.finished, tweens)

    rotateZ(rotation)

    player.paint()
    shape(labyrinth_shape)


def keyPressed():
    def set_rotation(new_rotation):
        global rotation
        rotation = new_rotation

    def set_player_position(new_position):
        global player
        player.geometry_x = new_position

    global tweens
    if tweens:
        return

    if keyCode == UP:
        tweens.append(Tween(player.geometry_x, player.geometry_x + BLOCK_SIZE, 25, set_player_position))
    elif keyCode == LEFT:
        tweens.append(Tween(rotation, rotation + PI/2, 50, set_rotation))
    elif keyCode == RIGHT:
        tweens.append(Tween(rotation, rotation - PI/2, 50, set_rotation))
