def load(day):
    contents = open(f"./inputs/{day}.txt", "r").read().strip().split("\n")
    return contents


def roll_tile_at_position(grid, x, y, direction):
    if grid[y][x] != "O":
        return grid
    dir_range = {"N": reversed(range(y)),
                 "S": range(y+1, len(grid)),
                 "E": range(x+1, len(grid[0])),
                 "W": reversed(range(x))}
    locked_dim = y if direction in "EW" else x
    last_x = x
    last_y = y
    for tile_pos in dir_range[direction]:
        new_x = tile_pos if direction in "EW" else locked_dim
        new_y = tile_pos if direction in "NS" else locked_dim
        if grid[new_y][new_x] == ".":
            grid[last_y][last_x] = "."
            grid[new_y][new_x] = "O"
            last_x = new_x
            last_y = new_y
        else:
            break
    return grid


def get_rock_count(rock_grid):
    return str(rock_grid).count("O")


def read_initial_rock_position():
    rock_grid = load("14")
    rock_grid = list(map(list, rock_grid))
    return rock_grid


rock_grid_change_map = dict()
rock_grid_repeats = dict()
rock_grid_repeat_cycle_counts = dict()



def roll_all_rocks(rock_grid, direction):
    #if (str(rock_grid), direction) in rock_grid_change_map.keys():
    #    return rock_grid_change_map[(str(rock_grid), direction)]
    init_grid = str(rock_grid)
    if direction in "NS":
        for col in range(len(rock_grid[0])):
            if direction == "N":
                vert_range = range(len(rock_grid))
            else:
                vert_range = reversed(range(len(rock_grid)))
            for row in vert_range:
                rock_grid = roll_tile_at_position(rock_grid, col, row, direction)
    if direction in "EW":
        for row in range(len(rock_grid)):
            if direction == "W":
                horiz_range = range(len(rock_grid[0]))
            else:
                horiz_range = reversed(range(len(rock_grid[0])))
            for col in horiz_range:
                rock_grid = roll_tile_at_position(rock_grid, col, row, direction)
    rock_grid_change_map[(init_grid, direction)] = rock_grid

    rock_test = 0
    for row in rock_grid:
        for char in row:
            if char=="O":
                rock_test += 1
    return rock_grid


def weight_on_north_beams(rock_grid):
    weight = 0
    for col in range(len(rock_grid[0])):
        for row in range(len(rock_grid)):
            tile = rock_grid[row][col]
            if tile == "O":
                weight += len(rock_grid) - row
    return weight


def gridprint(grid):
    output = "\n"
    for line in grid:
        output += "".join(line) + "\n"
    print(output)

def main():
    rock_grid = read_initial_rock_position()
    rock_grid = roll_all_rocks(rock_grid, "N")
    print(f"part 1: {weight_on_north_beams(rock_grid)}")

    cycles = 1000000000
    for i in range(cycles):
        for direction in "NWSE":
            rock_grid = roll_all_rocks(rock_grid, direction)
            #print(direction)
            #gridprint(rock_grid)
        if str(rock_grid) in rock_grid_repeats.keys():
            rock_grid_repeats[str(rock_grid)].append(i)
            rock_grid_repeat_cycle_counts[(str(rock_grid))] += 1
            step_size = rock_grid_repeats[str(rock_grid)][-1] - rock_grid_repeats[str(rock_grid)][-2]
            if (cycles - i -1) % step_size == 0:
                print(f"{weight_on_north_beams(rock_grid)}, {rock_grid_repeat_cycle_counts[(str(rock_grid))]} times")
                break
        else:
            rock_grid_repeats[str(rock_grid)] = [i]
            rock_grid_repeat_cycle_counts[(str(rock_grid))] = 1
        if i % 50000 == 0:
            print(f"{100*i/cycles}%")
    print(f"part 2: {weight_on_north_beams(rock_grid)}")


main()

# part1 23033 low
# part2 146593 too high
# part2 89119
