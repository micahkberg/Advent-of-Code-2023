def load(day):
    contents = open(f"./inputs/{day}.txt", "r").read().strip().split("\n")
    return contents


MAX_Y = len(load("21"))
MAX_X = len(load("21")[0])


def read_map(extra_tile=False):
    raw_data = load("21")
    garden_squares = set()
    if extra_tile:
        for i in range(len(raw_data)):
            raw_data[i] += raw_data[i]

    for y in range(len(raw_data)):
        for x in range(len(raw_data[0])):
            char = raw_data[y][x]
            if char == ".":
                garden_squares.add((x, y))
            elif char == "S":
                start_pos = (x, y)
                garden_squares.add((x, y))
    return start_pos, garden_squares


def mainpt1():
    start_pos, garden_squares = read_map()
    current_positions = [start_pos]
    dirs = [[0, 1], [1, 0], [-1, 0], [0, -1]]
    even_cells = set()
    visited = set()
    for step in range(64):
        new_positions = set()
        for pos in current_positions:
            for direction in dirs:
                new_position = (pos[0]+direction[0], pos[1]+direction[1])
                if new_position in garden_squares and new_position not in visited:
                    new_positions.add(new_position)
                    visited.add(new_position)
                    if step % 2 == 1: # lol not that even i guess
                        even_cells.add(new_position)
        current_positions = new_positions.copy()
    print("part 1: reachable in 64 steps")
    print(len(even_cells))


mainpt1()


def manhattan_distance(x1,y1,x2,y2):
    return abs(y1-y2) + abs(x1-x2)


def count_tiles_from(start_coord, tiles, steps):
    current_positions = [start_coord]
    dirs = [[0, 1], [1, 0], [-1, 0], [0, -1]]
    for step in range(steps):
        new_positions = set()
        for pos in current_positions:
            for direction in dirs:
                new_position = (pos[0] + direction[0], pos[1] + direction[1])
                if new_position in tiles:
                    new_positions.add(new_position)
        current_positions = new_positions.copy()
    return len(current_positions)


def mainpt2():
    start_pos, garden_squares = read_map()
    tile0_mass = count_tiles_from((65, 65), garden_squares, 139)
    tile1_mass = count_tiles_from((65, 65), garden_squares, 140)
    lines = load("21")
    manhattan_radius = 26501365
    tile_side_length = len(lines[0])  # 131 chars on each side of our small tile
    tiles_radius = int((manhattan_radius-start_pos[0])/tile_side_length)  # 202300.5 tiles in the radius of our 'circle'

    # alright imagine the big rhombus that has a "radius" of 2023.5
    # below is a rhombus of r=2.5 i guess, except that the line that represents
    # the limit of our motion cuts through some of these edges
    #
    #   .#.
    #   ###
    #  #####
    #   ###
    #    #

    # i can't really figure out how to make any assumptions about how to cut it up in a way
    # where i don't care about density of different areas

    # so lets look at the mass of the different segments and then count
    # up how many of those segments there are

    LR_triangle = count_tiles_from((130, 130), garden_squares, 64)
    LL_triangle = count_tiles_from((0, 130), garden_squares, 64)
    UR_triangle = count_tiles_from((130, 0), garden_squares, 64)
    UL_triangle = count_tiles_from((0,0), garden_squares, 64)

    NW_pentagon = count_tiles_from((130, 130), garden_squares, 131 + 64)
    NE_pentagon = count_tiles_from((0, 130), garden_squares, 131 + 64)
    SW_pentagon = count_tiles_from((130, 0), garden_squares, 131 + 64)
    SE_pentagon = count_tiles_from((0, 0), garden_squares, 131 + 64)

    S_corner = count_tiles_from((65, 0), garden_squares, 130)
    N_corner = count_tiles_from((65, 130), garden_squares, 130)
    E_corner = count_tiles_from((0, 65), garden_squares, 130)
    W_corner = count_tiles_from((130, 65), garden_squares, 130)

    # my quadrant solution assumed that everything was reachable by manhattan distance which was not the case
    # above solution actually walks the different kinds of partial tiles

    #quadrant_plots_0 = {"NW": set(), "NE": set(), "SE": set(), "SW": set()}
    #quadrant_plots_1 = {"NW": set(), "NE": set(), "SE": set(), "SW": set()}
    #center_area_0 = set()
    #center_area_1 = set()
    #for tile in garden_squares:
    #    x = tile[0]
    #    y = tile[1]
    #    if manhattan_distance(x, y, 0, 0) < 65:
    #        if (x, y) in start_tile_set:
    #            quadrant_plots_0["NW"].add((x, y))
    #        else:
    #            quadrant_plots_1["NW"].add((x, y))
    #    elif manhattan_distance(x, y, 131, 0) < 65:
    #        if (x, y) in start_tile_set:
    #            quadrant_plots_0["NE"].add((x, y))
    #        else:
    #            quadrant_plots_1["NE"].add((x, y))
    #    elif manhattan_distance(x, y, 0, 131) < 65:
    #        if (x, y) in start_tile_set:
    #            quadrant_plots_0["SW"].add((x, y))
    #        else:
    #            quadrant_plots_1["SW"].add((x, y))
    #    elif manhattan_distance(x, y, 131, 131) < 65:
    #        if (x, y) in start_tile_set:
    #            quadrant_plots_0["SE"].add((x, y))
    #        else:
    #            quadrant_plots_1["SE"].add((x, y))
    #    elif manhattan_distance(x, y, start_pos[0], start_pos[1]) < 65:
    #        if (x, y) in start_tile_set:
    #            center_area_0.add((x, y))
    #        else:
    #            center_area_1.add((x, y))

    tile0_count = 1
    tile1_count = 0
    ring_size = 4
    #ok instead of growing out, i can just count out in rhombus circles alternatingly
    for i in range(1, tiles_radius):
        if i % 2 == 0:
            tile0_count += ring_size
        else:
            tile1_count += ring_size
        ring_size += 4

    whole_tile_total = tile0_count*tile0_mass + tile1_count*tile1_mass
    small_triangle_total = (LR_triangle + LL_triangle + UL_triangle + UR_triangle) * tiles_radius
    big_pentagon_total = (NW_pentagon + NE_pentagon + SE_pentagon + SW_pentagon) * (tiles_radius-1)
    corners = N_corner + E_corner + S_corner + W_corner

    total_garden_plots = whole_tile_total + small_triangle_total + big_pentagon_total + corners
    print("part 2: mega grid reachable")
    print(total_garden_plots)






mainpt2()

# pt 2, 123324038264 too low
# pt 2, 121993089736
# pt 2, 121993089750
# pt 2, 42595196809
# pt 2, 42668421306
# pt 2, 442702020632 too low (guess)
# pt 2, 426529402562035 close, finally got the size of the problem correct
# pt 2, 426528480467240
# pt 2, 426528352193175
# pt 2, 609586735877925
# pt 2, 609585229256075
# pt 2, 609585229256084.... finally