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

class TilableNoise2D:
    def __init__(self, seed, scale):
        self._seed = seed
        self._radius = scale

    def get_value(self, coord1, coord2, version):
        coord1 = constrain(coord1, 0.0, 1.0)
        coord2 = constrain(coord2, 0.0, 1.0)
        version = constrain(version, 0.0, 1.0)

        noise1 = TilableNoise(self._seed, self._radius)
        val1 = noise1.get_value(coord1, version)

        noise2 = TilableNoise(self._seed * 10, self._radius)
        val2 = noise2.get_value(coord2, version)

        return (val2 + val1) / 2.0

def setup():
    size(1050, 850)
    background(200)
    noiseSeed(0)

    tile_width = 200
    tile_height = 200
    tile_count_x = int(width/tile_width)
    tile_count_y = int(height/tile_height)
    tile_count = tile_count_x * tile_count_y

    scale = 0.25
    seed = 10.0
    tilableNoise = TilableNoise2D(seed, scale)

    for tile_index_x in range(tile_count_x):
        for tile_index_y in range(tile_count_y):
            x_start = tile_index_x * tile_width
            x_end = (tile_index_x+1) * tile_width
            y_start = tile_index_y * tile_height
            y_end = (tile_index_y+1) * tile_height

            tile_index = tile_index_x * tile_count_x + tile_index_y
            noise_version = map(tile_index, 0, tile_count, 0.0, 1.0)

            print(tile_index)

            for x in range(x_start, x_end):
                for y in range(y_start, y_end):
                    noise_coord1 = map(x, x_start, x_end, 0.0, 1.0)
                    noise_coord2 = map(y, y_start, y_end, 0.0, 1.0)

                    noise_value = tilableNoise.get_value(noise_coord1, noise_coord2, noise_version)
                    #noise_value = int(noise_value * 10) / 10.0

                    stroke( noise_value * 255)
                    point(x, y)

    stroke(255, 0, 0)
    for tile_index_x in range(1, tile_count_x+1):
        x = tile_index_x * tile_width
        line(x, 0, x, height)

    for tile_index_y in range(1, tile_count_y+1):
        y = tile_index_y * tile_height
        line(0, y, width, y)