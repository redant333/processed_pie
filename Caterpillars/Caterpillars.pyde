class Head(object):
    """Class that represents head of a caterpillar. Moves around choosing its
       direction by using Perlin noise. Bounces off the edges.
    """
    _STROKE_COLOR = color(6, 65, 0)
    _STROKE_WEIGHT = 5
    _FILL_COLOR = color(7, 102, 0)
    _DIAMETER = 35

    def __init__(self, x, y, speed, noise_increment):
        """Constructor.

        Arguments:
            x {float} -- initial x position.
            y {float} -- initial y position.
            speed {float} -- will move this much in current direction on every update()
            noise_increment {float} -- used to calculate current direction. Larger values mean
                                       sharper changes of direction.
        """
        self.position = PVector(x, y, speed)
        self._position_increment = PVector(0, speed)
        self._angle_offset = random(TWO_PI)
        self._noise_y = random(100)
        self._noise_x = 0
        self._noise_increment = noise_increment

    def update(self):
        self.position.add(self._position_increment)

        # Check if outside the screen
        if not 0 <= self.position.x < width or not 0 <= self.position.y < height:
            # Move back and reverse the angle
            self.position.sub(self._position_increment)
            self._angle_offset = (self._angle_offset + PI) % TWO_PI

        new_angle = map(noise(self._noise_x, self._noise_y), 0, 1, 0, TWO_PI)

        self._position_increment.rotate(
            new_angle - self._position_increment.heading() + self._angle_offset)
        self._noise_x += self._noise_increment

    def paint(self):
        strokeWeight(Head._STROKE_WEIGHT)
        stroke(Head._STROKE_COLOR)
        fill(Head._FILL_COLOR)
        ellipse(self.position.x, self.position.y,
                Head._DIAMETER, Head._DIAMETER)


class Body(object):
    """Class that represents body segment of a caterpillar. Follows another
       object at a fixed distance.
    """
    _STROKE_COLOR = color(6, 65, 0)
    _STROKE_WEIGHT = 5
    _FILL_COLOR = color(7, 102, 0)

    _DIAMETER = 30

    _MIDDLE_STROKE_WEIGHT = 15
    _DOT_FILL = color(179, 143, 0)
    _DOT_DIAMETER = 10

    def __init__(self, x, y, to_follow, distance):
        """Constructor.

        Arguments:
            x {float} -- initial x location.
            y {float} -- initial y location.
            to_follow {float} -- object to follow. The object must have
                                 attribute position of type PVector.
            distance {float} -- distance to maintain between this object and _to_follow.
        """
        self.position = PVector(x, y)
        self._to_follow = to_follow
        self._distance = distance

    def update(self):
        distance_vector = PVector.sub(self._to_follow.position, self.position)
        distance_vector.setMag(self._distance)
        self.position = PVector.sub(self._to_follow.position, distance_vector)

    def paint(self):
        # Draw a circle with stroke
        stroke(Body._STROKE_COLOR)
        strokeWeight(Body._STROKE_WEIGHT)
        fill(Body._FILL_COLOR)

        ellipse(self.position.x, self.position.y,
                Body._DIAMETER, Body._DIAMETER)

        # Draw a thick line connecting this and the next body segment
        # to create an illusion of connection between segments
        strokeWeight(Body._MIDDLE_STROKE_WEIGHT)
        stroke(Body._FILL_COLOR)
        line(self.position.x, self.position.y,
             self._to_follow.position.x, self._to_follow.position.y)

        # Place a dot on the current and the next body segment
        # Multiple dots needed because of overwriting
        noStroke()
        fill(Body._DOT_FILL)
        ellipse(self.position.x, self.position.y,
                Body._DOT_DIAMETER, Body._DOT_DIAMETER)
        ellipse(self._to_follow.position.x, self._to_follow.position.y,
                Body._DOT_DIAMETER, Body._DOT_DIAMETER)


class Caterpillar(object):
    """Class that represents a caterpillar. Composed of one head (see Head)
       and multiple body segments (see Body).
    """
    _BODY_SEGMENTS_DISTANCE = 20

    def __init__(self, x, y, body_length, speed, noise_increment):
        """Constructor.

        Arguments:
            x {float} -- initial x location.
            y {float} -- initial y location.
            body_length {int} -- number of body segments.
            speed {float} -- speed of the head.
            noise_increment {float} -- used to determine movement direction (see Head).
        """
        self._objects = [Head(x, y, speed, noise_increment)]

        last_segment = self._objects[0]
        for _ in range(body_length):
            body_segment = Body(x, y, last_segment,
                                Caterpillar._BODY_SEGMENTS_DISTANCE)
            last_segment = body_segment
            self._objects.append(body_segment)

    def update(self):
        for obj in self._objects:
            obj.update()

    def paint(self):
        for obj in self._objects:
            obj.paint()


##############################
# Processing loop and settings
##############################
SAVE_FRAMES = False
SAVE_FRAMES_PATH = "frames/frame_######.png"

FRAMERATE = 30
CATERPILLAR_COUNT = 10

caterpillars = []


def setup():
    size(1280, 720)
    frameRate(FRAMERATE)

    MIN_LENGTH = 4
    MAX_LENGTH = 8
    MIN_SPEED = 2
    MAX_SPEED = 4
    MIN_NOISE_INC = 0.02
    MAX_NOISE_INC = 0.04

    global caterpillars
    for _ in range(CATERPILLAR_COUNT):
        caterpillars.append(Caterpillar(width/2, height/2,
                                        int(random(MIN_LENGTH, MAX_LENGTH)),
                                        random(MIN_SPEED, MAX_SPEED),
                                        random(MIN_NOISE_INC, MAX_NOISE_INC)))


def draw():
    background(0)

    for caterpillar in caterpillars:
        caterpillar.update()
        caterpillar.paint()

    if SAVE_FRAMES:
        saveFrame(SAVE_FRAMES_PATH)
