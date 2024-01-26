def load(day):
    contents = open(f"./inputs/{day}.txt", "r").read().strip().split("\n")
    #for row in contents:
    #    print(row)
    #print("=============================================================================================")
    return contents


def simple_expand(grid):
    rows_expanded = []
    for row in grid:
        rows_expanded.append(row)
        if "#" not in row:
            rows_expanded.append(row)
    cols_expanded = [""]*len(rows_expanded)
    for x in range(len(rows_expanded[0])):
        for y in range(len(rows_expanded)):
            cols_expanded[y] += rows_expanded[y][x]
        if "#" not in list(map(lambda i: i[x], rows_expanded)):
            for y in range(len(rows_expanded)):
                cols_expanded[y] += rows_expanded[y][x]
    return cols_expanded

def complex_expand(grid):
    big_rows = []
    big_cols = []
    for y in range(len(grid)):
        row = grid[y]
        if "#" not in row:
            big_rows.append(y)
    for x in range(len(grid[0])):
        if "#" not in list(map(lambda i: i[x], grid)):
            big_cols.append(x)
    return big_rows, big_cols


class Galaxy:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def galaxy_distance_manhattan(g1, g2):
    dist = abs(g1.x-g2.x) + abs(g1.y - g2.y)
    return dist


def expanded_distances(g1, g2, row_nums, col_nums):
    count = 0
    for row_num in row_nums:
        if (g1.y < row_num < g2.y) or (g2.y < row_num < g1.y):
            count+=1
    for col_num in col_nums:
        if (g1.x < col_num < g2.x) or (g2.x < col_num < g1.x):
            count+=1

    return count*(1000000-1)



def find_all_galaxies(grid):
    galaxies = []
    for y in range(len(grid)):
        row = grid[y]
        for x in range(len(row)):
            if grid[y][x] == "#":
                galaxies.append(Galaxy(x, y))
    return galaxies


def mainpt1():
    initial_space = load("11")
    expanded_space = simple_expand(initial_space)
    galaxy_list = find_all_galaxies(expanded_space)
    distance_sum = 0
    for i in range(len(galaxy_list)):
        for j in range(i+1, len(galaxy_list)):
            distance_sum += galaxy_distance_manhattan(galaxy_list[i],galaxy_list[j])
    print(distance_sum)


def mainpt2():
    initial_space = load("11")
    big_rows, big_cols = complex_expand(initial_space)
    galaxy_list = find_all_galaxies(initial_space)
    distance_sum = 0
    for i in range(len(galaxy_list)):
        for j in range(i+1, len(galaxy_list)):
            g1 = galaxy_list[i]
            g2 = galaxy_list[j]
            distance_sum += galaxy_distance_manhattan(g1, g2)
            distance_sum += expanded_distances(g1, g2 , big_rows, big_cols)
    print(distance_sum)

#part2 try 1 377319269864, too high
#part2 try 2 377318892554
mainpt2()
