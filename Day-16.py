def load(day):
    contents = open(f"./inputs/{day}.txt", "r").read().strip().split("\n")
    return contents


def get_cave_floor():
    return load("16")


def get_splitter_dirs(splitter_symbol):
    return "NS" if splitter_symbol in "|" else "EW"


def get_mirror_dirs(mirror_symbol):
    return ["NW", "SE"] if mirror_symbol =="\\" else ["NE", "SW"]


def parallel(beam_direction, splitter_symbol):
    splitter_dir = get_splitter_dirs(splitter_symbol)
    return beam_direction in splitter_dir


def move(cave, beam):
    x, y, direction = beam
    dirs = {"N": (0,-1), "S": (0,1), "E": (1,0), "W": (-1,0)}
    tile = cave[y][x]
    splitters = "-|"
    mirrors = "/\\"
    if tile == ".":
        return [(x+dirs[direction][0], y+dirs[direction][1], direction)]
    elif tile in splitters:
        if parallel(direction, tile):
            return [(x + dirs[direction][0], y + dirs[direction][1], direction)]
        else:
            splitter_dirs = get_splitter_dirs(tile)
            beam1 = (x + dirs[splitter_dirs[0]][0], y + dirs[splitter_dirs[0]][1], splitter_dirs[0])
            beam2 = (x + dirs[splitter_dirs[1]][0], y + dirs[splitter_dirs[1]][1], splitter_dirs[1])
            return [beam1, beam2]
    elif tile in mirrors:
        mirror_dirs = get_mirror_dirs(tile)
        for mirror_dir in mirror_dirs:
            if direction  in mirror_dir:
                new_direction = mirror_dir.replace(direction, "")
                return [(x + dirs[new_direction][0], y+dirs[new_direction][1], new_direction)]
    else:
        print("Failed to identify tile")
        return None


def energize(start_pos):
    cave = get_cave_floor()
    initial_beam = start_pos
    beams = {initial_beam}
    seen = set()
    energized = set()
    while len(beams)>0:
        new_beams = []
        beam = beams.pop()
        seen.add(beam)
        energized.add((beam[0], beam[1]))
        new_beams += move(cave, beam)
        for new_beam in new_beams:
            if new_beam in seen:
                pass
            elif new_beam[0] in range(len(cave[0])) and new_beam[1] in range(len(cave)):
                beams.add(new_beam)
    return len(energized)


def main():
    print('Part 1')
    print(energize((0, 0, "E")))

    max_energize = 0
    xs = range(len(get_cave_floor()[0]))
    ys = range(len(get_cave_floor()))
    for x in xs:
        top_energy = energize((x, 0, "S"))
        bot_energy = energize((x, ys[-1], "N"))
        max_energize = max([top_energy, bot_energy, max_energize])
    for y in ys:
        left_energy = energize((0, y, "E"))
        right_energy = energize((0, xs[-1], "W"))
        max_energize = max([left_energy, right_energy, max_energize])

    print("Part 2")
    print(max_energize)

main()
