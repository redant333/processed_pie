###################################################
# Seeds for random generation and noise
# Change these variables if you want specific seeds
RANDOM_SEED = floor(random(99999999))
PERLIN_SEED = floor(random(99999999))
randomSeed(RANDOM_SEED)
noiseSeed(PERLIN_SEED)
###################################################

WATER_COLOR = color(112, 193, 255, 240)
STONE_COLOR = color(128)
PLANT_COLOR = color(23, 96, 0)
SAND_COLOR = color(244, 226, 65)

CAMERA_X = 0
CAMERA_Y = -500
CAMERA_Z = 500
ROTATION_SPEED = 0.02

TERRAIN_SIZE = 400.0
HORIZONTAL_POINTS = 80

VERTICAL_POINTS = 60
WATER_LEVEL_POINTS = 28
STONE_LEVEL_POINTS = 45
PERLIN_STEP = 0.035


POINT_DISTANCE = TERRAIN_SIZE / (HORIZONTAL_POINTS - 1)
WATER_OFFSET = POINT_DISTANCE / 4
STONE_LEVEL = STONE_LEVEL_POINTS * POINT_DISTANCE
WATER_LEVEL = WATER_LEVEL_POINTS * POINT_DISTANCE - WATER_OFFSET
SAND_LEVEL = WATER_LEVEL

rot_y = 0
perlin_points = [[0] * HORIZONTAL_POINTS for i in range(HORIZONTAL_POINTS)]


def setup():
    size(1280, 720, P3D)
    print("Using RANDOM_SEED {}, PERLIN_SEED {}".format(RANDOM_SEED, PERLIN_SEED))
    camera(CAMERA_X, CAMERA_Y, CAMERA_Z, 0, 0, 0, 0, 1, 0)

    for i in range(HORIZONTAL_POINTS):
        for j in range(HORIZONTAL_POINTS):
            point_height = noise(i*PERLIN_STEP, j*PERLIN_STEP)
            point_height *= VERTICAL_POINTS * POINT_DISTANCE
            point_height -= point_height % POINT_DISTANCE
            perlin_points[i][j] = point_height


def get_color_from_y(y):
    if y > STONE_LEVEL:
        return STONE_COLOR
    elif y < SAND_LEVEL:
        return SAND_COLOR
    else:
        return PLANT_COLOR


def draw():
    global rot_y

    background(0)
    lights()

    rotateY(rot_y)
    if mouseButton != LEFT:
        rot_y += ROTATION_SPEED

    translate(-TERRAIN_SIZE/2, 0, -TERRAIN_SIZE/2)

    # Draw terrain
    fill(PLANT_COLOR)
    noStroke()
    for x_index in range(HORIZONTAL_POINTS - 1):
        beginShape(TRIANGLE_STRIP)
        for z_index in range(HORIZONTAL_POINTS):
            x = x_index * POINT_DISTANCE
            z = z_index * POINT_DISTANCE
            y = -perlin_points[x_index][z_index]
            fill(get_color_from_y(-y))
            vertex(x, y, z)
            x = (x_index + 1) * POINT_DISTANCE
            z = z_index * POINT_DISTANCE
            y = -perlin_points[x_index + 1][z_index]
            fill(get_color_from_y(-y))
            vertex(x, y, z)

        endShape()

    # Draw sides
    fill(STONE_COLOR)
    for z_index in (0, HORIZONTAL_POINTS - 1):
        beginShape(TRIANGLE_STRIP)
        z = z_index * POINT_DISTANCE
        for x_index in range(HORIZONTAL_POINTS):
            x = x_index * POINT_DISTANCE
            y = -perlin_points[x_index][z_index]
            vertex(x, 0, z)
            vertex(x, y, z)
        endShape()

    for x_index in (0, HORIZONTAL_POINTS - 1):
        beginShape(TRIANGLE_STRIP)
        x = x_index * POINT_DISTANCE
        for z_index in range(HORIZONTAL_POINTS):
            z = z_index * POINT_DISTANCE
            y = -perlin_points[x_index][z_index]
            vertex(x, 0, z)
            vertex(x, y, z)
        endShape()

    # Draw water
    fill(WATER_COLOR)
    water_height = WATER_LEVEL_POINTS * POINT_DISTANCE - WATER_OFFSET
    translate(TERRAIN_SIZE/2, -water_height/2, TERRAIN_SIZE/2)
    box(TERRAIN_SIZE - WATER_OFFSET * 2,
        water_height, TERRAIN_SIZE - WATER_OFFSET * 2)
