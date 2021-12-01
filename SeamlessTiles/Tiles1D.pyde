class TilableNoise:
    def __init__(self, seed, scale):
        self._seed = seed
        self._radius = scale

    def get_value(self, coord, version):
        coord = constrain(coord, 0.0, 1.0)
        version = constrain(version, 0.0, 1.0)

        center = PVector(-self._radius, 0)
        center.rotate(TWO_PI * version)

        value_vector = PVector(self._radius, 0)
        value_vector.rotate(TWO_PI * version)
        value_vector.rotate(TWO_PI * coord)

        value_point = center + value_vector

        return noise(value_point.x, value_point.y + self._seed)

def setup():
    size(1000, 250)

def draw():
    background(200)

    tile_width = 200
    tile_height = 200
    tile_count = int(width/tile_width)

    scale = float(mouseX) / width * 5.0
    seed = float(mouseY) / height * 10
    tilableNoise = TilableNoise(seed, scale)

    for tile_index in range(tile_count):
        x_start = tile_index * tile_width
        x_end = (tile_index+1) * tile_width

        for x in range(x_start, x_end):
            noise_coord = map(x, x_start, x_end, 0.0, 1.0)
            noise_version = map(tile_index, 0, tile_count, 0.0, 1.0)

            stroke(tilableNoise.get_value(noise_coord, noise_version) * 255)
            line(x, 0, x, tile_height)

        stroke(255, 0, 0)
        line(x_end, tile_height, x_end, height)

