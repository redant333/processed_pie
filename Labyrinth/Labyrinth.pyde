from random import choice

########################
# Constants
########################
FRAMERATE = 60

BLOCK_SIZE = 10

LABYRINTH_WIDTH = 31
LABYRINTH_HEIGHT = 31

CAMERA_BACK_DISTANCE = 55
CAMERA_FRONT_DISTANCE = 50
CAMERA_Z = 89

PLAYER_MOVEMENT_FRAMES = FRAMERATE / 4
PLAYER_ROTATION_FRAMES = FRAMERATE / 2
PLAYER_Z = BLOCK_SIZE
PLAYER_SIZE = 0.4 * BLOCK_SIZE

LABEL_ROTATION_FRAMES = 3.5 * FRAMERATE
LABEL_RISE_FRAMES = 0.8 * FRAMERATE
LABEL_SCALE_FRAMES = LABEL_RISE_FRAMES

START_COLOR = color(255, 0, 0)
END_COLOR = color(0, 255, 0)
PATH_COLOR = color(200, 200, 0)
WALL_COLOR = color(5, 99, 8)
PLAYER_COLOR = color(200, 200, 200)
LABEL_FOREGROUND = color(0, 160, 0)
LABEL_BACKGROUND = color(255)


############################
# Class definitions
############################

class Labyrinth(object):
    """Class that represents a labyrinth made of cells in 2D grid.
       Each cell represents start, end, wall or path.
    """
    START = 0
    WALL = 1
    PATH = 2
    END = 4

    def __init__(self, w, h):
        """Creates a Labyrinth
        
        Arguments:
            w {[int]} -- Width of the labyrinth
            h {[int]} -- Height of the labyirinth
        
        Raises:
            ValueError: If w and h are not odd numbers(labyrinth cannot be created that way)
        """
        if w % 2 == 0 or h % 2 == 0:
            raise ValueError("Width and height must be odd numbers")

        self._width = w
        self._height = h
        self._cells = self._generate_labyrinth(w, h)

    @property
    def w(self):
        """Get the width of the Labyrinth
        
        Returns:
            [int] -- Width of the Labyirinth
        """
        return self._width

    @property
    def h(self):
        """Get the height of the Labyrinth
        
        Returns:
            [int] -- Height of the Labyirinth
        """
        return self._height

    def _generate_labyrinth(self, w, h):
        """Populates the labyrinth with walls, paths, start and end.
           Uses the recursive algorithm.
        
        Arguments:
            w {[int]} -- Width of the labyrinth
            h {[int]} -- Height of the labyrinth
        
        Returns:
            [int[][]] -- Integer matrix with dimensions w x h that contains
                         the values for walls, paths, start and end.
        """
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
                    cells[(y+neighbor_y)/2][x] = Labyrinth.PATH
                elif y == neighbor_y:
                    cells[y][(x+neighbor_x)/2] = Labyrinth.PATH

                stack.append((x, y))
                (x, y) = (neighbor_x, neighbor_y)
            elif stack:
                (x, y) = stack.pop()
            else:
                break

        return cells

    def get(self, x, y):
        """Get the cell value at position (x,y)
        
        Arguments:
            x {[int]} -- x coordinate of the cell
            y {[int]} -- y coordinate of the cell
        
        Returns:
            [int] -- One of the values START, END, WALL, PATH if (x,y) is
                     inside of the labyrinth, None otherwise
        """
        if 0 <= x < self._width and 0 <= y < self._height:
            return self._cells[y][x]
        else:
            return None

    def to_shape(self):
        """Create 3D PShape that represents the Labyrinth
        
        Returns:
            [PShape] -- 3D representation of the Labyrinth
        """
        ret = createShape(GROUP)
        for x in range(self._width):
            for y in range(self._height):
                val = self._cells[y][x]
                block_color = None
                block_height = BLOCK_SIZE

                if val == Labyrinth.START:
                    block_color = START_COLOR
                elif val == Labyrinth.END:
                    block_color = END_COLOR
                elif val == Labyrinth.WALL:
                    block_color = WALL_COLOR
                    block_height = 2 * BLOCK_SIZE
                elif val == Labyrinth.PATH:
                    block_color = PATH_COLOR

                new_box = createShape(
                    BOX, BLOCK_SIZE, BLOCK_SIZE, block_height)
                new_box.setFill(block_color)
                new_box.setStroke(False)
                new_box.translate(x * BLOCK_SIZE, y *
                                  BLOCK_SIZE, block_height/2)
                ret.addChild(new_box)
        return ret


class Tween(object):
    """Class that does linear interpolation between two values over the specified
       number of steps.
    """

    def __init__(self, from_val, to_val, frames, update_function=None, finish_function=None):
        """Creates a Tween object
        
        Arguments:
            from_val {[number]} -- starting value of the tween
            to_val {[number]} -- ending value of the tween
            frames {[int]} -- number of steps to get from the starting to the ending value
        
        Keyword Arguments:
            update_function {[function]} -- function to be called on every tween update (default: {None})
            finish_function {[function]} -- function to be called when tween reaches the
                                            ending value (default: {None})
        """
        self._from_val = from_val
        self._to_val = to_val
        self._frames = frames
        self._frames_elapsed = 0
        self._update_function = update_function
        self._finish_function = finish_function
        self._finished = False

    def update(self):
        """Advances the tween to the next value. It takes frames calls to this
           function for the tween to reach to_val. After that, this method has
           no effect. Calls update_function if the value has changed.
        """
        if self._finished:
            return

        self._frames_elapsed += 1

        if self._update_function:
            self._update_function(self.value)

        if self._frames <= self._frames_elapsed:
            self._finished = True
            if self._finish_function:
                self._finish_function()

    @property
    def value(self):
        """Get the value of this tween.
        
        Returns:
            [number] -- Current value of this tween.
        """
        return map(self._frames_elapsed, 0, self._frames, self._from_val, self._to_val)

    @property
    def finished(self):
        """Checks whether the tween has reached to_val. If this method returns true
           value will return to_val.
        
        Returns:
            [boolean] -- True if finished, False otherwise
        """
        return self._finished


class Player(object):
    """Class that represents the player.
    """
    X_PLUS = 0
    Y_PLUS = 1
    X_MINUS = 2
    Y_MINUS = 3

    def __init__(self, labyrinth):
        """Creates a Player object which can move through the specified labyirinth
        
        Arguments:
            labyrinth {[Labyrinth]} -- A labyrinth through which this Player can move
        """
        self._labyrinth = labyrinth
        self._tween = None

        self._x = 0
        self._y = 1
        self._direction = Player.X_PLUS

        self._geometry_x = self._x * BLOCK_SIZE
        self._geometry_y = self._y * BLOCK_SIZE
        self._geometry_direction = 0

    def move(self):
        """Start the movement of the Player one step in the direction it is facing if the cell is not a wall.
        """
        if self._tween:
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

        self._tween = Tween(geometry, geometry + offset,
                            PLAYER_MOVEMENT_FRAMES, set_geometry_function)

    @property
    def geometry_direction(self):
        """Gets the direction Player is currently facing. This direction does not need
           to be a multiple of 90 degrees due to animation.
        
        Returns:
            [float] -- The direction Player is currently facing
        """
        return self._geometry_direction

    @property
    def geometry_x(self):
        return self._geometry_x

    @property
    def geometry_y(self):
        """Current y coordinate of the Player in the world coordinates (not the labyrinth
           cell coordinates)
        
        Returns:
            [float] -- The current y coordinate of the Player
        """
        return self._geometry_y

    @property
    def won(self):
        """Checks whether the Player is at the end of the labyrinth
        
        Returns:
            [bool] -- True if the Player is currently at the end of the labyrint, False otherwise
        """
        return self._labyrinth.get(self._x, self._y) == Labyrinth.END

    @property
    def animating(self):
        """Checks whether the Player is currently animating (rotating or moving)
        
        Returns:
            [bool] -- [description]
        """
        return self._tween is not None

    def rotate_right(self):
        """Starts the rotation of the Player by 90 degrees in clockwise direction
        """
        if self._tween:
            return

        def set_direction(new_direction):
            self._geometry_direction = new_direction % TWO_PI

        next = {
            Player.X_PLUS: Player.Y_PLUS,
            Player.Y_PLUS: Player.X_MINUS,
            Player.X_MINUS: Player.Y_MINUS,
            Player.Y_MINUS: Player.X_PLUS
        }

        self._direction = next[self._direction]

        self._tween = Tween(self._geometry_direction,
                            self._geometry_direction + PI/2, PLAYER_ROTATION_FRAMES, set_direction)

    def rotate_left(self):
        """Starts the rotation of the Player by 90 degrees in anticlockwise direction
        """
        if self._tween:
            return

        def set_direction(new_direction):
            self._geometry_direction = new_direction % TWO_PI

        next = {
            Player.X_PLUS: Player.Y_MINUS,
            Player.Y_PLUS: Player.X_PLUS,
            Player.X_MINUS: Player.Y_PLUS,
            Player.Y_MINUS: Player.X_MINUS
        }

        self._direction = next[self._direction]

        self._tween = Tween(self._geometry_direction,
                            self._geometry_direction - PI/2, PLAYER_ROTATION_FRAMES, set_direction)

    def update(self):
        """Update the internal state of the Player. This method should be called once for every frame
        """
        if not self._tween:
            return

        self._tween.update()

        if self._tween.finished:
            self._tween = None

    def paint(self):
        """Draw the 3D representation of the Player in the world.
        """
        pushMatrix()
        noStroke()
        fill(PLAYER_COLOR)
        translate(self._geometry_x, self._geometry_y, PLAYER_Z)
        sphere(PLAYER_SIZE)
        popMatrix()


class Label(object):
    """3D animated label that rises and rotates.
    """
    def __init__(self, x, y, z, final_z, string):
        """Creates a Label with text string that starts at (x,y,z) and moves
           towards (x,y,final_z) while rotating.
        
        Arguments:
            x {float} -- Initial x coordinate
            y {float} -- Initial y coordinate
            z {float} -- Initial z coordinate
            final_z {float} -- Final z coordinate
            string {[type]} -- Text written on the Label
        """
        self._x = x
        self._y = y
        self._z = z

        self._final_z = final_z
        self._string = string

        self._tweens = []
        self._text_height = BLOCK_SIZE / 2
        textSize(self._text_height)
        self._text_width = textWidth(string)

        self._rotation = 0
        self._scale = 0

        def set_rotation(new_rotation):
            self._rotation = new_rotation % TWO_PI

        def set_z(new_z):
            self._z = new_z

        def set_scale(new_scale):
            self._scale = new_scale

        def rotate_again():
            self._tweens.append(
                Tween(self._rotation, self._rotation + TWO_PI, LABEL_ROTATION_FRAMES, set_rotation, rotate_again))

        self._tweens.append(
            Tween(0, TWO_PI, LABEL_ROTATION_FRAMES, set_rotation, rotate_again))
        self._tweens.append(Tween(z, final_z, LABEL_RISE_FRAMES, set_z))
        self._tweens.append(Tween(0, 1, LABEL_SCALE_FRAMES, set_scale))

    def update(self):
        """Update the internal state of the Label. This method should be called once for every frame
        """
        for tween in self._tweens:
            tween.update()

        self._tweens = filter(lambda tween: not tween.finished, self._tweens)

    def paint(self):
        """Draw the 3D representation of the Label in the world.
           Contains drawing commands of questionable readability.
        """
        offset = self._text_height / 4
        a_little = 0.01

        textAlign(CENTER, CENTER)
        rectMode(CENTER)
        textSize(self._text_height)

        pushMatrix()
        translate(self._x, self._y, self._z)
        scale(self._scale)
        rotateZ(PI/2)
        rotateX(-PI/2)
        rotateY(self._rotation)

        noStroke()
        fill(0, 160, 0)

        translate(0, 0, a_little)
        text(self._string, 0, 0)

        translate(0, 0, -a_little)
        translate(0, textDescent() / 2, 0)
        fill(255)
        strokeWeight(10)
        stroke(0, 160, 0)
        rect(0, 0, self._text_width + offset,
             self._text_height + textDescent() + offset)
        translate(0, -textDescent() / 2, 0)

        rotateY(PI)

        fill(0, 160, 0)
        translate(0, 0, a_little)
        text(self._string, 0, 0)

        popMatrix()

##########################
# Main loop and globals
##########################

labyrinth_shape = None
player = None
label = None


def set_camera():
    """Sets the camera position and direction
    """
    camera_pos = PVector(-CAMERA_BACK_DISTANCE, 0)
    camera_pos.rotate(player.geometry_direction)
    camera_target = PVector(CAMERA_FRONT_DISTANCE, 0)
    camera_target.rotate(player.geometry_direction)

    camera(player.geometry_x + camera_pos.x, player.geometry_y + camera_pos.y, CAMERA_Z,
           player.geometry_x + camera_target.x, player.geometry_y + camera_target.y, 0,
           0, 0, -1)


def handle_keys():
    """Check for the pressed keys and trigger player movement accordingly
    """
    if keyCode == UP:
        player.move()
    elif keyCode == LEFT:
        player.rotate_left()
    elif keyCode == RIGHT:
        player.rotate_right()


def setup():
    size(1280, 720, P3D)
    frameRate(FRAMERATE)
    textMode(SHAPE)
    background(0)

    labyrinth = Labyrinth(LABYRINTH_WIDTH, LABYRINTH_HEIGHT)

    global labyrinth_shape
    labyrinth_shape = labyrinth.to_shape()

    global player
    player = Player(labyrinth)


def draw():
    global label
    background(0)
    lights()

    if not player.won and keyPressed:
        handle_keys()

    if player.won and not player.animating and not label:
        label = Label(player.geometry_x, player.geometry_y,
                      PLAYER_Z, PLAYER_Z + 2 * BLOCK_SIZE, "Yay, you won!")

    player.update()
    set_camera()
    player.paint()

    if label:
        label.update()
        label.paint()

    shape(labyrinth_shape)
