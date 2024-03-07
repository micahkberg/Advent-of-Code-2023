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


class Tile:
    def __init__(self, coord, garden_map):
        self.coords = coord
        self.x = coord[0]
        self.y = coord[1]
        self.char = garden_map[self.y % MAX_Y][self.x % MAX_X]


def mainpt2():
    start_pos, garden_map = read_map()
    even_distance_positions = set(start_pos)
    odd_distance_positions = set()
    seen = set(start_pos)
    current_positions = [start_pos]
    dirs = [[0, 1], [1, 0], [-1, 0], [0, -1]]
    for step in range(1, 26501365 + 1):
        if step % 1000 == 0:
            print(f"{str(100*step/(26501365 + 1))[:4]}%, {len(current_positions)}")
        new_positions = set()
        for pos in current_positions:
            for direction in dirs:
                new_position = (pos[0]+direction[0], pos[1]+direction[1])
                if new_position not in seen:
                    seen.add(new_position)
                    if garden_map[(new_position[0] % MAX_X, new_position[1] % MAX_Y)] == ".":
                        new_positions.add(new_position)
                        if step % 2 == 0:
                            even_distance_positions.add(new_position)
                        else:
                            odd_distance_positions.add(new_position)
        current_positions = new_positions.copy()
    print(len(even_distance_positions))


mainpt2()
