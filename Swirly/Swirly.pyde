class SwirlyWalker(object):
    """Class that represents a walker which can draw a circle on every step
    """

    def __init__(self, x, y, angle, speed, rotation_speed, rotation_acceleration, initial_thickness, thickness_multiplier, lifetime):
        """Create a SwirlyWalker object

           The object starts at location (x,y) in direction angle. On each
           update(), the object moves according to the current speed and
           direction, its direction is increased by the current rotation speed
           and the rotation speed is increased by rotation_acceleration. On each
           paint(), circle with diameter corresponding to the current thickness
           is drawn on the current location, and the current thickness is
           multiplied by thickness_multiplier.

        Arguments:
            x {float} -- initial x coordinate of the object
            y {float} -- initial y coordinate of the object
            angle {float} -- initial direction of the object
            speed {float} -- on update(), the object will move this many pixels
            rotation_speed {float} -- on update(), the object rotates by some angle. This is the initial
                                      rotation speed that will be changed by rotation_acceleration. The
                                      rotation can be negative.
            rotation_acceleration {float} -- on update(), rotation speed is increased by this value. Can be
                                             negative.
            initial_thickness {float} -- on paint(), a circle with some diameter is drawn on the current
                                         position. This is the initial diameter that will be changed by
                                         thickness_multiplier.
            thickness_multiplier {float} -- on update(), thickness is multiplied by this value.
            lifetime {int} -- number of update() calls during which this alive() will report true.
        """
        self._position = PVector(x, y)
        self._position_increment = PVector(speed)
        self._position_increment.rotate(angle)
        self._rotation_speed = rotation_speed
        self._rotation_acceleration = rotation_acceleration
        self._thickness = initial_thickness
        self._thickness_multiplier = thickness_multiplier
        self._lifetime = lifetime

    def alive(self):
        """Check whether the object is alive. Object lifetime is passed in __init__()

        Returns:
            [bool] -- True if alive, False otherwise
        """
        return self._lifetime > 0

    def paint(self):
        """Paint a circle at current position whose diameter is determined by current thickness.
           This function does not change fill or stroke color.
        """
        ellipse(self._position.x, self._position.y,
                self._thickness, self._thickness)

        self._thickness *= self._thickness_multiplier

    def update(self):
        """Update the position and movement parameters of the object
        """
        self._position.add(self._position_increment)

        self._position_increment.rotate(self._rotation_speed)
        self._rotation_speed += self._rotation_acceleration
        self._lifetime -= 1

###################
# Scene definitions
###################


class FlowerScene(object):
    def __init__(self):
        self._hues = [53, 19]
        self._walkers = self._create_walkers()
        self._hue_index = 0

    def _create_walkers(self):
        def create_walker(direction):
            return SwirlyWalker(width/2, height/2, direction, 3.3, 0.08, -0.001, 40, 0.991, 225)

        return [create_walker(map(i, 0, 10, 0, TWO_PI))
                for i in range(10)]

    def running(self):
        return self._hue_index < len(self._hues)

    def update(self):
        if not self.running():
            return

        if len(self._walkers) == 0:
            self._hue_index += 1
            if not self.running():
                return

            self._walkers = self._create_walkers()

        fill(self._hues[self._hue_index], 360, 288)
        for w in self._walkers:
            w.update()
            w.paint()

        self._walkers = [w for w in self._walkers if w.alive()]


class CircleScene(object):
    def __init__(self):
        self._circle_radius = 175
        self._creation_period = 5  # create a new walker every 5 steps
        self._until_creation = self._creation_period
        self._max_walkers = 72
        self._walkers_in_a_circle = 36
        self._initial_walker_thickness = 20

        self._progress_angle = 0
        self._progress_angle_increase = -2 * TWO_PI / 350  # measured experimentally

        self._walkers = [self._create_walker(0)]

    def _create_walker(self, circle_angle):
        pos_vector = PVector(self._circle_radius)
        pos_vector.rotate(circle_angle)
        pos_vector.add(PVector(width/2, height/2))

        # Note that these values are experimentally determined
        return SwirlyWalker(pos_vector.x, pos_vector.y, circle_angle - PI/2, 1.5, 0.000625, 0.0003125, self._initial_walker_thickness, 0.99, 195)

    def running(self):
        return any([w.alive() for w in self._walkers])

    def update(self):
        walker_count = len(self._walkers)

        # Create a new walker if creation period passed
        if self._until_creation == 0 and walker_count < self._max_walkers:
            self._walkers.append(self._create_walker(
                map(walker_count, 0, self._walkers_in_a_circle, TWO_PI, 0)))
            self._until_creation = self._creation_period

        for i in range(len(self._walkers)):
            w = self._walkers[i]
            if w.alive():
                w.update()
                fill(map(i, 0, self._max_walkers, 0, 360), 360, 288)
                w.paint()

        # If there are more walkers to be created, progress circle needs to advance too
        if len(self._walkers) < self._max_walkers:
            progress_circle = PVector(self._circle_radius)
            progress_circle.rotate(self._progress_angle)
            progress_circle.add(PVector(width/2, height/2))

            self._progress_angle += self._progress_angle_increase
            ellipse(progress_circle.x, progress_circle.y,
                    self._initial_walker_thickness, self._initial_walker_thickness)

        self._until_creation -= 1


class CloverScene(object):
    def __init__(self):
        self._leaf_walkers = []
        self._spike_walkers = self._create_spikes()
        self._until_leaf_creation = 50

    def _create_spikes(self):
        return [SwirlyWalker(width/2, height/2, PI/2 * i, 2, 0, 0, 30, 0.991, 150) for i in range(4)]

    def _create_leaves(self):
        def create_leaf(angle, facing):
            return SwirlyWalker(width/2, height/2, angle, 3.3,
                                0.04 * facing, -0.001 * facing, 40, 0.991, 150)

        leaves = [create_leaf(i * PI/2, 1) for i in range(4)]
        leaves += [create_leaf(i * PI/2, -1) for i in range(4)]
        return leaves

    def running(self):
        return any([w.alive() for w in self._spike_walkers]) or any([w.alive() for w in self._leaf_walkers])

    def update(self):
        fill(55, 360, 250)
        for w in self._spike_walkers:
            if w.alive():
                w.update()
                w.paint()

        fill(119, 360, 200)
        for w in self._leaf_walkers:
            if w.alive():
                w.update()
                w.paint()

        if self._until_leaf_creation > 0:
            self._until_leaf_creation -= 1

            if self._until_leaf_creation == 0:
                self._leaf_walkers = self._create_leaves()


class RoseScene(object):
    def __init__(self):
        self._vertical_center = height * 0.6  # move the center of the flower a bit down
        self._leaf_walkers = self._create_leaves()
        self._petal_walkers = []
        self._details_walkers = []
        self._until_petal_creation = 134
        self._until_details_creation = 234
        self._details_created = False

    def _create_leaves(self):
        def create_leaf(angle, facing):
            rotation_offset = -1
            return SwirlyWalker(width/2, self._vertical_center, angle + rotation_offset * facing, 3.3, facing * 0.015, 0, 20, 0.998, 134)

        leaves = [create_leaf(-PI/2 + map(i, 0, 3, 0, TWO_PI), 1)
                  for i in range(3)]
        leaves += [create_leaf(-PI/2 + map(i, 0, 3, 0, TWO_PI), -1)
                   for i in range(3)]
        return leaves

    def _create_petals(self):
        petals = [SwirlyWalker(
            width/2, self._vertical_center, map(i, 0, 6, 0, TWO_PI), 3.3, -0.01, -0.001, 20, 1.02, 100) for i in range(6)]
        petals += [SwirlyWalker(
            width/2, self._vertical_center, map(i, 0, 6, 0, TWO_PI), 3.3, 0.01, 0.001, 20, 1.02, 100) for i in range(6)]
        return petals

    def _create_details(self):
        rotation_offset = -0.2
        details = [SwirlyWalker(
            width/2, self._vertical_center, map(i, 0, 6, 0, TWO_PI) + rotation_offset, 3.3, -0.01, -0.001, 10, 0.998, 110) for i in range(6)]
        return details

    def running(self):
        return not self._details_created or any([w.alive() for w in self._details_walkers])

    def update(self):
        fill(119, 360, 200)
        for w in self._leaf_walkers:
            if w.alive():
                w.update()
                w.paint()

        fill(0, 360, 200)
        for w in self._petal_walkers:
            if w.alive():
                w.update()
                w.paint()

        fill(0, 360, 0)
        for w in self._details_walkers:
            if w.alive():
                w.update()
                w.paint()

        if self._until_petal_creation > 0:
            self._until_petal_creation -= 1

            if self._until_petal_creation == 0:
                self._petal_walkers = self._create_petals()

        if self._until_details_creation > 0:
            self._until_details_creation -= 1

            if self._until_details_creation == 0:
                self._details_walkers = self._create_details()
                self._details_created = True

##############################
# Processing loop and settings
##############################


SAVE_FRAMES = False
SAVE_FRAMES_PATH = "frames/frame_######.png"

FRAMERATE = 60
PAUSE_BETWEEN_SCENES = 2 * FRAMERATE

until_scene_pause_end = PAUSE_BETWEEN_SCENES
scenes = None


def setup():
    size(1280, 720)
    background(0)
    colorMode(HSB, 360)
    smooth(8)
    noStroke()
    frameRate(FRAMERATE)

    global scenes
    scenes = [
        FlowerScene(),
        CloverScene(),
        RoseScene(),
        CircleScene(),
    ]


def draw():
    if len(scenes) == 0:
        return

    scene = scenes[0]

    if scene.running():
        scene.update()
    else:
        global until_scene_pause_end
        if until_scene_pause_end == 0:
            until_scene_pause_end = PAUSE_BETWEEN_SCENES
            background(0)
            scenes.pop(0)
        else:
            until_scene_pause_end -= 1

    if SAVE_FRAMES:
        saveFrame(SAVE_FRAMES_PATH)
