class Head(object):
    def __init__(self, x, y, speed):
        self.position = PVector(x, y, speed)
        self._position_increment = PVector(0, speed)
        self._noise_y = 0

    def update(self):
        self.position.add(self._position_increment)

        new_angle = map(noise(frameCount * 0.03, self._noise_y), 0.2, 0.8, 0, TWO_PI)

        if not 0 <= self.position.x < width or not 0 <= self.position.y < height:
            self.position.sub(self._position_increment)
            while not 0.9 * PI < abs((new_angle + TWO_PI) - (self._position_increment.heading() + TWO_PI)) < 1.1 * PI:
                self._noise_y += 0.05
                new_angle = map(noise(frameCount * 0.03, self._noise_y), 0.2, 0.8, 0, TWO_PI)
            print(new_angle - self._position_increment.heading())
            print("current angle {}, new angle {}".format(self._position_increment.heading(), new_angle))

        self._position_increment.rotate(new_angle - self._position_increment.heading())

    def paint(self):
        fill(0,255,0)
        ellipse(self.position.x, self.position.y, 30, 30)

    def alive(self):
        return True

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
        fill(255,255,0)
        ellipse(self.position.x, self.position.y, 30, 30)

    def alive(self):
        return True

objects = []

def setup():
    size(1280,720)
    head = Head(width/2,height/2,4)
    bodyPart = Body(0,0,head,20)
    noStroke()

    global objects
    objects = [head, bodyPart]
    for i in range(5):
        objects.append(Body(random(width),random(height),objects[len(objects) - 1],20))
    distribution_test()

def distribution_test():
    stats_array = [0] * 501

    noise_x = 0
    for i in range(100000):
        stats_array[int(noise(noise_x) * 501)] += 1
        noise_x += 0.03

    max_stat = max(stats_array)
    background(0)
    for i in range(len(stats_array)):
        rect(i*2, 200, 1, -map(stats_array[i], 0, max_stat, 0, 200))


def draw():
    return
    background(0)

    for obj in objects:
        if obj.alive():
            obj.update()
            obj.paint()