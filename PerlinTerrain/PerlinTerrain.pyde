###################################################
# Seeds for random generation and noise
# Change these variables if you want specific seeds
RANDOM_SEED = floor(random(99999999))
PERLIN_SEED = floor(random(99999999))
randomSeed(RANDOM_SEED)
noiseSeed(PERLIN_SEED)
###################################################

###################################################
# Colors used for different terrain features
###################################################
WATER_COLOR = color(112, 193, 255, 240)
STONE_COLOR = color(128)
PLANT_COLOR = color(23, 96, 0)
SAND_COLOR = color(244, 226, 65)

###################################################
# Camera position and model rotation
###################################################
CAMERA_X = 0
CAMERA_Y = -500
CAMERA_Z = 500
ROTATION_SPEED = 0.01

###################################################
# Generated terrain size and precision
###################################################
# Terrain size in pixels
TERRAIN_SIZE = 400.0
# Number of generated points per terrain size
# Larger number means smoother terrain
PRECISION = 80

###################################################
# Generation parameters
###################################################
HORIZONTAL_POINTS = PRECISION
# Vertical size of generated terrain (in precision points)
VERTICAL_POINTS = floor(random(HORIZONTAL_POINTS * 0.5, HORIZONTAL_POINTS * 0.8))
# Water height (in precision points)
WATER_LEVEL_POINTS = floor(random(VERTICAL_POINTS * 0.3, VERTICAL_POINTS * 0.6))
# Height at which stone color is used instead of plant (in precision points)
STONE_LEVEL_POINTS = floor(random(VERTICAL_POINTS * 0.65, VERTICAL_POINTS * 0.8))

# Precision at which random(0.02, 0.05) gives reasonably good results
REFERENCE_PRECISION = 80
# Step used in random generation of terrain. 
# Corrected for potential change of precision
PERLIN_STEP = random(0.02, 0.05) * REFERENCE_PRECISION / PRECISION

# Distance in pixels between two randomly generated points
POINT_DISTANCE = TERRAIN_SIZE / (PRECISION - 1)
# STONE_LEVEL_POINTS converted to pixels
STONE_LEVEL = STONE_LEVEL_POINTS * POINT_DISTANCE
# WATER_LEVEL_POINTS converted to pixels and lowered by half of
# point distance. This is done to prevent having parallel water 
# and land which causes visual glitches
WATER_LEVEL = WATER_LEVEL_POINTS * POINT_DISTANCE - POINT_DISTANCE/2

# Height until which sand color is used
SAND_LEVEL = WATER_LEVEL + POINT_DISTANCE


def create_terrain(perlin_points):
    terrain = createShape()
    terrain.translate(-TERRAIN_SIZE/2, 0, -TERRAIN_SIZE/2)
    vertices = []

    # This is an emulation of triangle strip in order to enable
    # more flexible coloring (P3D renderer creates gradients if
    # neighboring vertices are of different color)
    def add_vertex(x, y, z):
        vertices.append((x, y, z))

        if len(vertices) > 3:
            vertices.pop(0)
        elif len(vertices) < 3:
            return

        all_sand = all([abs(y) < SAND_LEVEL for x, y, z in vertices])

        if all_sand:
            terrain.fill(SAND_COLOR)
            for x, y, z in vertices:
                terrain.vertex(x, y, z)
        else:
            for x, y, z in vertices:
                terrain.fill(PLANT_COLOR
                             if abs(y) < STONE_LEVEL
                             else STONE_COLOR)
                terrain.vertex(x, y, z)

    terrain.beginShape(TRIANGLES)
    terrain.noStroke()
    for x_index in range(HORIZONTAL_POINTS - 1):
        vertices = []
        for z_index in range(HORIZONTAL_POINTS):
            x = x_index * POINT_DISTANCE
            z = z_index * POINT_DISTANCE
            y = -perlin_points[x_index][z_index]
            add_vertex(x, y, z)
            x = (x_index + 1) * POINT_DISTANCE
            z = z_index * POINT_DISTANCE
            y = -perlin_points[x_index + 1][z_index]
            add_vertex(x, y, z)
    terrain.endShape()

    return terrain


def create_terrain_sides(perlin_points):
    terrain_sides = createShape(GROUP)
    terrain_sides.translate(-TERRAIN_SIZE/2, 0, -TERRAIN_SIZE/2)

    # Create sides at min and max z
    for z_index in (0, HORIZONTAL_POINTS - 1):
        side = createShape()
        terrain_sides.addChild(side)

        side.beginShape(TRIANGLE_STRIP)
        side.fill(STONE_COLOR)
        side.noStroke()
        z = z_index * POINT_DISTANCE
        for x_index in range(HORIZONTAL_POINTS):
            x = x_index * POINT_DISTANCE
            y = -perlin_points[x_index][z_index]
            side.vertex(x, 0, z)
            side.vertex(x, y, z)
        side.endShape()

    # Create sides at min and max x
    for x_index in (0, HORIZONTAL_POINTS - 1):
        side = createShape()
        terrain_sides.addChild(side)

        side.beginShape(TRIANGLE_STRIP)
        side.fill(STONE_COLOR)
        side.noStroke()

        x = x_index * POINT_DISTANCE
        for z_index in range(HORIZONTAL_POINTS):
            z = z_index * POINT_DISTANCE
            y = -perlin_points[x_index][z_index]
            side.vertex(x, 0, z)
            side.vertex(x, y, z)
        side.endShape()

    return terrain_sides


def create_water():
    WATER_OFFSET = POINT_DISTANCE / 4

    # Distance between end of water and end of terrain is
    # 1/4 of point distance, so that terrain can be seen from the side
    water = createShape(BOX, TERRAIN_SIZE - WATER_OFFSET * 2,
                        WATER_LEVEL, TERRAIN_SIZE - WATER_OFFSET * 2)
    water.setFill(WATER_COLOR)
    water.setStroke(False)
    water.translate(0, -WATER_LEVEL/2, 0)

    return water


rot_y = 0
terrain = None
terrain_sides = None
water = None

def setup():
    size(1280, 720, P3D)
    print("Using RANDOM_SEED {}, PERLIN_SEED {}".format(RANDOM_SEED, PERLIN_SEED))
    camera(CAMERA_X, CAMERA_Y, CAMERA_Z, 0, 0, 0, 0, 1, 0)

    # Create HORIZONTAL_PONTS x HORIZONTAL_POINTS matrix of numbers
    # that will be uses for terrain height
    perlin_points = [[0] * HORIZONTAL_POINTS for i in range(HORIZONTAL_POINTS)]
    for i in range(HORIZONTAL_POINTS):
        for j in range(HORIZONTAL_POINTS):
            point_height = noise(i*PERLIN_STEP, j*PERLIN_STEP)
            point_height *= VERTICAL_POINTS * POINT_DISTANCE
            # Round it to multiple of POINT_DISTANCE, so that
            # horizontal and vertical distance between points is same
            point_height -= point_height % POINT_DISTANCE
            perlin_points[i][j] = point_height

    global terrain, terrain_sides, water
    terrain = create_terrain(perlin_points)
    terrain_sides = create_terrain_sides(perlin_points)
    water = create_water()


def draw():
    global rot_y

    background(0)
    lights()

    rotateY(rot_y)
    # Model will be stopped if left mouse is pressed
    # Useful for inspection of details
    if mouseButton != LEFT:
        rot_y += ROTATION_SPEED

    # Draw terrain
    shape(terrain)

    # Draw sides
    shape(terrain_sides)

    # Draw water
    shape(water)
