def load(day):
    contents = open(f"./inputs/{day}.txt", "r").read().strip().split("\n")
    return contents


MAX_Y = len(load("21"))
MAX_X = len(load("21")[0])


def read_map():
    raw_data = load("21")
    garden_map = dict()
    for y in range(len(raw_data)):
        for x in range(len(raw_data[0])):
            char = raw_data[y][x]
            if char != "S":
                garden_map[(x,y)] = char
            else:
                start_pos = (x,y)
                garden_map[(x,y)] = "."
    return start_pos, garden_map


def mainpt1():
    start_pos, garden_map = read_map()
    current_positions = [start_pos]
    dirs = [[0, 1], [1, 0], [-1, 0], [0, -1]]
    for _ in range(64):
        new_positions = set()
        for pos in current_positions:
            for direction in dirs:
                new_position = (pos[0]+direction[0], pos[1]+direction[1])
                if new_position in garden_map.keys():
                    if garden_map[new_position] == ".":
                        new_positions.add(new_position)
        current_positions = new_positions.copy()
    print(len(current_positions))


def manhattan_distance(x1,y1,x2,y2):
    return abs(y1-y2) + abs(x1-x2)


def mainpt2():
    start_pos, garden_map = read_map()
    lines = load("21")
    manhattan_radius = 26501365
    tile_side_length = len(lines[0])  # 131 chars on each side of our small tile
    tiles_radius = (manhattan_radius-start_pos[0])/tile_side_length  # 2023.5 tiles in the radius of our 'circle'

    plots_on_tile = 1
    for line in lines:
        plots_on_tile += line.count(".")

    # alright imagine the big rhombus that has a "radius" of 2023.5
    # below is a rhombus of r=2.5 i guess, except that the line that represents
    # the limit of our motion cuts through some of these edges
    #
    #   .#.
    #   ###
    #  #####
    #   ###
    #    #

    # so we are going to imagine cutting the rhombus in quarters and then rearranging them to make a square

    quadrant_plots = {"NW": 0, "NE": 0, "SE": 0, "SW": 0}
    for tile in garden_map:
        x = tile[0]
        y = tile[1]
        if garden_map[tile] == "#":
            continue
        if manhattan_distance(x, y, 0, 0) <= 65:
            quadrant_plots["NW"] += 1
        elif manhattan_distance(x, y, 131, 0) <= 65:
            quadrant_plots["NE"] += 1
        elif manhattan_distance(x, y, 0, 131) <= 65:
            quadrant_plots["SW"] += 1
        elif manhattan_distance(x, y, 131, 131) <= 65:
            quadrant_plots["SE"] += 1
    central_area = plots_on_tile - sum(list(quadrant_plots.values()))
    print(quadrant_plots)
    # i can't really figure out how to make any assumptions about how to cut it up in a way
    # where i don't care about density of different areas
    total_garden_plots = 0
    edges = 0
    for x in range(-2023, 2024):
        for y in range(-2023, 2024):
            man_distance = abs(x)+abs(y)
            if man_distance > 2023:
                continue
            if man_distance < 2023:
                total_garden_plots += plots_on_tile
                continue
            if x==0 and y<x:
                total_garden_plots += central_area + quadrant_plots["NE"] + quadrant_plots["SE"]
            elif x==0 and x<y:
                total_garden_plots += central_area + quadrant_plots["NW"] + quadrant_plots["SW"]
            elif y==0 and x>y:
                total_garden_plots += central_area + quadrant_plots["SW"] + quadrant_plots["SE"]
            elif y==0 and x<y:
                total_garden_plots += central_area + quadrant_plots["NW"] + quadrant_plots["NE"]
            elif x<0 and y<0:
                edges += 1
    total_garden_plots += 4*edges*(plots_on_tile) - edges*sum(list(quadrant_plots.values()))
    total_garden_plots += (edges+1)*sum(list(quadrant_plots.values()))
    print(total_garden_plots)






mainpt2()

# pt 2, 123324038264 too low
# pt 2, 121993089736
# pt 2, 121993089750

