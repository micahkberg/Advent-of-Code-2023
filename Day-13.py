def load(day):
    contents = open(f"./inputs/{day}.txt", "r").read().strip().split("\n")
    return contents


def read_grids():
    grids = []
    new_grid = []
    for line in load("13"):
        if line:
            new_grid.append(line)
        else:
            grids.append(new_grid)
            new_grid = []
    grids.append(new_grid)
    return grids


def horizontal_search(grid):
    for lines_above in range(1, len(grid)):
        mirrored = True
        for ln1 in range(lines_above):
            ln2 = lines_above*2-(ln1+1)
            if ln2 < len(grid):
                line1 = grid[ln1]
                line2 = grid[ln2]
                if not line1 == line2:
                    mirrored = False
                    break
        if mirrored:
            return lines_above
    return False


def get_col(grid, i):
    col = ""
    for row in grid:
        col += row[i]
    return col


def vertical_search(grid):
    for col_to_left in range(1, len(grid[0])):
        mirrored = True
        for ln1 in range(col_to_left):
            ln2 = col_to_left*2-(ln1+1)
            if ln2 < len(grid[0]):
                line1 = get_col(grid, ln1)
                line2 = get_col(grid, ln2)
                if not line1 == line2:
                    mirrored = False
                    break
        if mirrored:
            return col_to_left
    return False



def find_mirror(grid):
    horiz = horizontal_search(grid)
    if horiz:
        return 100*horiz
    vert = vertical_search(grid)
    if vert:
        return vert


def find_errors(l1, l2):
    count = 0
    for i in range(len(l1)):
        if l1[i] != l2[i]:
            count += 1
            if count>1:
                return count
    return count


def error_vertical_search(grid):
    for col_to_left in range(1, len(grid[0])):
        number_of_errors = 0
        for ln1 in range(col_to_left):
            ln2 = col_to_left*2-(ln1+1)
            if ln2 < len(grid[0]):
                line1 = get_col(grid, ln1)
                line2 = get_col(grid, ln2)
                number_of_errors += find_errors(line1,line2)
            if number_of_errors > 1:
                break
        if number_of_errors==1:
            return col_to_left
    return False


def error_horizontal_search(grid):
    for lines_above in range(1, len(grid)):
        number_of_errors = 0
        for ln1 in range(lines_above):
            ln2 = lines_above*2-(ln1+1)
            if ln2 < len(grid):
                line1 = grid[ln1]
                line2 = grid[ln2]
                number_of_errors += find_errors(line1, line2)
            if number_of_errors > 1:
                break
        if number_of_errors == 1:
            return lines_above
    return False


def find_mirror_with_error(grid):
    horiz = error_horizontal_search(grid)
    if horiz:
        return 100*horiz
    vert = error_vertical_search(grid)
    if vert:
        return vert


def main():
    grids = read_grids()
    summary = 0
    for grid in grids:
        summary += find_mirror(grid)
    print(f"perfect reflections: {summary}")
    summarypt2 = 0
    for grid in grids:
        summarypt2 += find_mirror_with_error(grid)
    print(f"number of smudged reflections: {summarypt2}")


main()
