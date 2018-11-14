import random as py_random
####################
# Class definitions
####################


class World:
    """Class that manages a matrix of cell objecs. Each cell
       object must contain update() and get_color() methods.
    """

    def __init__(self, rows, columns, cell_size):
        """Creates a World object

        Arguments:
            rows {int} -- number of rows in the worlds matrix
            columns {int} -- number of columns in the worlds matrix
            cell_size {int} -- cell size in pixels(used in drawing)
        """

        self._rows = rows
        self._columns = columns
        self._cell_size = cell_size

        self._position_object_dict = {}
        self._object_position_dict = {}

    def get_object_count(self, object_class):
        """Returns number of objects of type object_class in the world

        Arguments:
            object_class {Class} -- class of objects to count

        Returns:
            [int] -- total number of objects of type object
        """

        return sum([1 for obj in self._object_position_dict if isinstance(obj, object_class)])

    def _is_valid_position(self, x, y):
        """Checks wheter given coordinates are inside of world's limits

        Arguments:
            x {integer} -- x coordinate
            y {integer} -- y coordiante

        Returns:
            boolean -- True if inside of this world's limits, False otherwise
        """

        if x < 0 or x >= self._columns:
            return False
        if y < 0 or y >= self._rows:
            return False
        return True

    def update(self):
        """Calls update on all managed objects
        """

        for obj in self._object_position_dict:
            # Object can be removed while this function is running
            # Do not call update on removed objects
            if obj in self._object_position_dict:
                obj.update()

    def draw(self, x, y):
        """Draws the world with top left corner on given coordinates

        Arguments:
            x {integer} -- x coordinate of the top left corner
            y {integer} -- y coordinate of the top left corner
        """

        for obj, position in self._object_position_dict.iteritems():
            rectX = x + position[0] * self._cell_size
            rectY = y + position[1] * self._cell_size
            noStroke()
            fill(obj.get_color())
            rect(rectX, rectY, self._cell_size, self._cell_size)

    def add_object(self, obj, x, y):
        """Adds an object into the world on the given coordiantes

        Arguments:
            obj {Object} -- the object to add
            x {int} -- x coordinate
            y {int} -- y coordinate

        Raises:
            Exception -- thrown when the coordinates are outside of the world
        """

        if not self._is_valid_position(x, y):
            raise Exception("({},{}) is not a valid position".format(x, y))

        self._position_object_dict[(x, y)] = obj
        self._object_position_dict[obj] = (x, y)

    def get_object_at_position(self, x, y):
        """Returns the object at given position

        Arguments:
            x {integer} -- x coordinate of the object
            y {integer} -- y coordiante of the object

        Returns:
            Object -- an object at position (x,y) if present, None otherwise
        """

        if (x, y) in self._position_object_dict:
            return self._position_object_dict[(x, y)]
        else:
            return None

    def get_object_position(self, obj):
        """Returns the position of given object

        Arguments:
            obj {Object} -- object whose position is needed

        Returns:
            (int, int) -- tuple with x and y coordinate if object is present,
                            None otherwise
        """

        if obj in self._object_position_dict:
            return self._object_position_dict[obj]
        else:
            return None

    def set_object_position(self, obj, x, y):
        """Sets the position of the given object inside the world

        Arguments:
            obj {Object} -- object whose position needs to be set
            x {integer} -- x coordinate
            y {integer} -- y coordinate

        Raises:
            Exception -- thrown when object is not in this world,
                         requested position is invalid or if there
                         is already an object at the requested position
        """

        if obj not in self._object_position_dict:
            raise Exception("Object not in this world")

        if not self._is_valid_position(x, y):
            raise Exception("({},{}) is not a valid position".format(x, y))

        new_position = (x, y)

        if new_position in self._position_object_dict:
            raise Exception("Position {} already taken".format(new_position))

        current_position = self._object_position_dict[obj]

        del self._position_object_dict[current_position]
        self._position_object_dict[new_position] = obj
        self._object_position_dict[obj] = new_position

    def remove_object(self, obj):
        """Removes the object from this world

        Arguments:
            obj {Object} -- object that should be removed

        Raises:
            Exception -- thrown when the object is not in this world
        """

        if obj not in self._object_position_dict:
            raise Exception("Object not in this world")

        current_position = self._object_position_dict[obj]
        del self._position_object_dict[current_position]
        del self._object_position_dict[obj]

    def get_size(self):
        """Returns the size of the world

        Returns:
            (int,int) -- tuple containing width and height of the world
        """

        return (self._columns, self._rows)


class Predator:
    """Predator(shark) class for Wa-Tor cellular automaton
    """

    def __init__(self, world, reproduction_time, energy):
        """Creates a Predator object

        Arguments:
            world {World} -- world this object will be placed in.
                             Note that constructor does not place the object.
            reproduction_time {int} -- this object will reproduce after 
                                       reproduction_time update() calls
            energy {int} -- amount of energy the object will start with. Every
                            update() call reduces the energy by 1, eating prey
                            increases the energy. If energy reaches 0, the object
                            dies.
        """

        self._world = world
        self._reproduction_time = reproduction_time
        self._reproduction_counter = reproduction_time

        self._energy = energy
        self._energy_counter = energy

    def _get_next_position(self, currentX, currentY):
        """Chooses and returns the next position

        Arguments:
            currentX {integer} -- current x position
            currentY {integer} -- current y position

        Returns:
            (int,int) -- tuple with x and y coordinates of the next position
        """

        world_width, world_height = self._world.get_size()
        emptyPositions = []
        preyPositions = []

        for x_diff, y_diff in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            potentialX = (currentX + x_diff) % world_width
            potentialY = (currentY + y_diff) % world_height
            obj = self._world.get_object_at_position(potentialX, potentialY)
            if obj is None:
                emptyPositions.append((potentialX, potentialY))
            elif isinstance(obj, Prey):
                preyPositions.append((potentialX, potentialY))

        if len(preyPositions) > 0:
            return py_random.choice(preyPositions)
        elif len(emptyPositions) > 0:
            return py_random.choice(emptyPositions)
        else:
            return None

    def update(self):
        """Updates the internal state of the object
        """

        x, y = self._world.get_object_position(self)
        next_position = self._get_next_position(x, y)
        self._energy_counter -= 1
        self._reproduction_counter -= 1

        if self._energy_counter == 0:
            self._world.remove_object(self)
            return

        if next_position is not None:
            obj_at_next_position = self._world.get_object_at_position(
                *next_position)
            if obj_at_next_position is None:
                self._world.set_object_position(self, *next_position)
            elif isinstance(obj_at_next_position, Prey):
                self._energy_counter += obj_at_next_position.get_energy_value()
                self._world.remove_object(obj_at_next_position)
                self._world.set_object_position(self, *next_position)

            if self._reproduction_counter <= 0:
                offspring = Predator(
                    self._world, self._reproduction_time, self._energy)
                self._world.add_object(offspring, x, y)

    def get_color(self):
        """Gets the color that should be used to draw this object

        Returns:
            Processing color -- color that should be used to draw this object
        """

        return color(255, 0, 0)


class Prey:
    """Prey(fish) class for Wa-Tor cellular automaton
    """

    def __init__(self, world, reproduction_time, energy):
        """Creates a Prey object

        Arguments:
            world {World} -- world this object will be placed in.
                             Note that constructor does not place the object.
            reproduction_time {int} -- this object will reproduce after 
                                       reproduction_time update() calls
            energy {int} -- energy value that Predator will earn by eating this
                            object.
        """

        self._world = world
        self._reproduction_time = reproduction_time
        self._reproduction_counter = reproduction_time
        self._energy_value = energy

    def get_energy_value(self):
        """Returns the energy that the predator earns after eating this prey

        Returns:
            int -- the energy value of this prey
        """

        return self._energy_value

    def update(self):
        """Updates the internal state of the object
        """
        x, y = self._world.get_object_position(self)
        world_width, world_height = self._world.get_size()

        # Find empty positions to move to
        emptyPositions = []
        for x_diff, y_diff in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            potentialX = (x + x_diff) % world_width
            potentialY = (y + y_diff) % world_height
            if self._world.get_object_at_position(potentialX, potentialY) is None:
                emptyPositions.append((potentialX, potentialY))

        # Decrement the reproduction counter
        self._reproduction_counter -= 1

        if len(emptyPositions) > 0:
            # Move to a random empty position
            new_position = py_random.choice(emptyPositions)
            self._world.set_object_position(self, *new_position)

            # Reproduce counter ran out
            if self._reproduction_counter <= 0:
                offspring = Prey(
                    self._world, self._reproduction_time, self._energy_value)
                self._world.add_object(offspring, x, y)
                self._reproduction_counter = self._reproduction_time

    def get_color(self):
        """Gets the color that should be used to draw this object

        Returns:
            Processing color -- color that should be used to draw this object
        """
        return color(0, 255, 0)


class StatusPanel:
    """Class that renders text in a box and updates every update_interval calls
    """

    def __init__(self, x, y, panel_width, panel_height, font_size, update_interval, status_function):
        """Create a panel.

        Arguments:
            x {float} -- x coordinate of upper left corner of the status panel
            y {float} -- y coordinate of upper right corner of the status panel
            panel_width {float} -- width of the panel
            panel_height {float} -- height of the panel
            font_size {float} -- font size to use when writing text
            update_interval {int} -- the text will be updated every update_interval update() calls
            status_function {function} -- function that takes no parameters and returns a string.
                                          Will be called to refresh the text
        """

        self._x = x
        self._y = y
        self._width = panel_width
        self._height = panel_height
        self._font_size = font_size
        self._update_interval = update_interval
        # Set update counter to zero to force text update on first update call
        self._update_counter = 0

        self._status_function = status_function

        self._text = ""
        self._border_weight = 5

    def update(self):
        self._update_counter -= 1

        if self._update_counter <= 0:
            self._text = self._status_function()
            self._update_counter = self._update_interval

    def draw(self):
        stroke(255)
        strokeWeight(self._border_weight)
        fill(0)
        rect(self._x, self._y, self._width, self._height)

        fill(color(255))
        textSize(self._font_size)
        textAlign(LEFT, TOP)

        text(self._text, self._x + self._border_weight,
             self._y + self._border_weight)


##############################
# Processing loop and settings
##############################

# Set these constants to adjust the simulation behavior.
# These values seem to give a balanced simulation:
#    WORLD_ROWS = 90
#    WORLD_COLUMNS = 160
#
#    PREDATOR_ENERGY = 10
#    PREDATOR_COUNT = 50
#    PREDATOR_REPRODUCTION_TIME = 15
#
#    PREY_ENERGY_VALUE = 1
#    PREY_COUNT = 500
#    PREY_REPRODUCTION_TIME = 2
WORLD_ROWS = 90
WORLD_COLUMNS = 160
WORLD_CELL_SIZE = 8

PREDATOR_ENERGY = 10
PREDATOR_COUNT = 50
PREDATOR_REPRODUCTION_TIME = 15

PREY_ENERGY_VALUE = 1
PREY_COUNT = 500
PREY_REPRODUCTION_TIME = 2

SIMULATION_FRAMERATE = 20

STATUS_PANEL_HEIGHT = 50
STATUS_PANEL_WIDTH = 170
STATUS_PANEL_FONT_SIZE = 15
STATUS_PANEL_UPDATE_INTERVAL = 1

# Settings for saving the data
DRAW_STATUS_PANEL = True
SAVE_FRAMES = False
SAVE_FRAMES_PATH = "frames/frame_######.png"
PRINT_STATS = False


def add_predators(world, count):
    """Adds the specified number of predators into the specified world

    Arguments:
        world {World} -- world to add the predators in
        count {integer} -- number of predators to add
    """

    while count > 0:
        predator = Predator(world, PREDATOR_REPRODUCTION_TIME, PREDATOR_ENERGY)
        x = py_random.randint(0, WORLD_COLUMNS - 1)
        y = py_random.randint(0, WORLD_ROWS - 1)

        while world.get_object_at_position(x, y) is not None:
            x = py_random.randint(0, WORLD_COLUMNS - 1)
            y = py_random.randint(0, WORLD_ROWS - 1)

        world.add_object(predator, x, y)
        count -= 1


def add_prey(world, count):
    """Adds the specified number of prey into the specified world

    Arguments:
        world {World} -- world to add the prey in
        count {integer} -- number of prey to add
    """
    while count > 0:
        predator = Prey(world, PREY_REPRODUCTION_TIME, PREY_ENERGY_VALUE)
        x = py_random.randint(0, WORLD_COLUMNS - 1)
        y = py_random.randint(0, WORLD_ROWS - 1)

        while world.get_object_at_position(x, y) is not None:
            x = py_random.randint(0, WORLD_COLUMNS - 1)
            y = py_random.randint(0, WORLD_ROWS - 1)

        world.add_object(predator, x, y)
        count -= 1


def status_function(world):
    predator_count = world.get_object_count(Predator)
    prey_count = world.get_object_count(Prey)

    if PRINT_STATS:
        print("{}\t{}".format(predator_count, prey_count))

    return "Predators: {}\nPrey: {}".format(predator_count, prey_count)


world = World(WORLD_ROWS, WORLD_COLUMNS, WORLD_CELL_SIZE)
statusPanel = StatusPanel(0, 0, STATUS_PANEL_WIDTH, STATUS_PANEL_HEIGHT, STATUS_PANEL_FONT_SIZE,
                          STATUS_PANEL_UPDATE_INTERVAL, lambda: status_function(world))


def setup():
    size(1280, 720)
    frameRate(SIMULATION_FRAMERATE)

    add_predators(world, PREDATOR_COUNT)
    add_prey(world, PREY_COUNT)


def draw():
    background(0)

    world.draw(0, 0)

    if DRAW_STATUS_PANEL:
        statusPanel.update()
        statusPanel.draw()
    
    if SAVE_FRAMES:
        saveFrame(SAVE_FRAMES_PATH)

    world.update()

