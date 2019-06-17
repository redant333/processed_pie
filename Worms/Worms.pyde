class Head(object):
    def __init__(self, x, y, speed):
        self.position = PVector(x, y, speed)
        self._position_increment = PVector(0, speed)
        self._angle_offset = 0
        self._noise_y = random(100)

    def update(self):
        self.position.add(self._position_increment)

        if not 0 <= self.position.x < width or not 0 <= self.position.y < height:
            self.position.sub(self._position_increment)
            self._angle_offset = (self._angle_offset + PI) % TWO_PI

        new_angle = map(noise(frameCount * 0.03, self._noise_y), 0, 1, 0 , TWO_PI)
        self._position_increment.rotate(new_angle - self._position_increment.heading() + self._angle_offset)

    def paint(self):
        strokeWeight(5)
        stroke(6,65,0)
        fill(7,102,0)
        ellipse(self.position.x, self.position.y, 35, 35)

class Body(object):
    def __init__(self, x, y, to_follow, distance):
        self.position = PVector(x, y)
        self._to_follow = to_follow
        self._distance = distance

    def update(self):
        distance_vector = PVector.sub(self._to_follow.position, self.position)
        distance_vector.setMag(self._distance)
        self.position = PVector.sub(self._to_follow.position, distance_vector)

    def paint(self):
        stroke(6,65,0)
        strokeWeight(5)
        fill(7,102,0)
        ellipse(self.position.x, self.position.y, 30, 30)

        strokeWeight(15)
        stroke(7,102,0)
        line(self.position.x, self.position.y, self._to_follow.position.x, self._to_follow.position.y)

        noStroke()
        fill(179,143,0)
        ellipse(self.position.x, self.position.y, 10, 10)
        ellipse(self._to_follow.position.x, self._to_follow.position.y, 10, 10)


class Catepillar(object):
    _BODY_SEGMENTS_DISTANCE = 20

    def __init__(self, x, y, body_length, speed):
        self._objects = [Head(x, y, speed)]

        last_segment = self._objects[0]
        for _ in range(body_length):
            body_segment = Body(x, y, last_segment,
                                Catepillar._BODY_SEGMENTS_DISTANCE)
            last_segment = body_segment
            self._objects.append(body_segment)

    def update(self):
        for obj in self._objects:
            obj.update()

    def paint(self):
        for obj in self._objects:
            obj.paint()

objects = []

def setup():
    size(1280,720)
    noStroke()

    global objects
    for _ in range(25):
        objects.append(Catepillar(width/2, height/2,int(random(4,8)),random(2,4)))


def draw():
    background(0)

    for obj in objects:
        obj.update()
        obj.paint()
