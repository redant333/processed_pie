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


class FlowerScene(object):
    def __init__(self):
        def createWalker(direction):
            return SwirlyWalker(width/2, height/2, direction, 3.3, 0.08, -0.001, 40, 0.991, 275)

        self._walkers = [createWalker(map(i, 0, 10, 0, TWO_PI))
                         for i in range(10)]

    def running(self):
        return len(self._walkers) > 0

    def update(self):
        fill(20, 100, 80)
        for w in self._walkers:
            w.update()
            w.paint()

        self._walkers = [w for w in self._walkers if w.alive()]


scenes = None


def setup():
    size(1280, 720)
    background(0)
    colorMode(HSB, 100)
    smooth(8)
    noStroke()

    global scenes
    scenes = [FlowerScene()]


def draw():
    if len(scenes) == 0:
        return

    scene = scenes[0]
    if scene.running():
        scene.update()
    else:
        scenes.pop(0)
