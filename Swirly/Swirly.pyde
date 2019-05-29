class SwirlyWalker(object):
    def __init__(self, x, y, angle, speed, rotation_speed, color, lifetime):
        self._position = PVector(x, y)
        self._position_increment = PVector(speed)
        self._position_increment.rotate(angle)
        self._rotation_speed = rotation_speed
        self._color = color
        self._thickness = 40
        self._lifetime = lifetime

    def alive(self):
        return self._lifetime > 0

    def paint(self):
        noStroke()
        fill(self._color, 100, 100, 10)
        self._thickness *= 0.991
        ellipse(self._position.x, self._position.y,
                self._thickness, self._thickness)

    def update(self):
        self._position_increment.rotate(self._rotation_speed)
        self._rotation_speed -= 0.001
        self._position.add(self._position_increment)

        self._lifetime -= 1


walkers = []


def setup():
    size(1280, 720)
    background(0)
    colorMode(HSB, 100)


def draw():
    global walkers

    for walker in walkers:
        walker.update()
        walker.paint()

    walkers = [w for w in walkers if w.alive()]

    if len(walkers) == 0:
        clr = random(30)
        for i in range(10):
            walkers.append(
                SwirlyWalker(width/2, height/2, map(i, 0, 10, 0, TWO_PI), 3.3, 0.08, clr, 275))
