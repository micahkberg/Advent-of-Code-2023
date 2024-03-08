def load(day):
    contents = open(f"./inputs/{day}.txt", "r").read().strip().split("\n")
    return contents


class Tile:
    def __init__(self, symbol):
        self.connections = []
        self.symbol = symbol

    def connects_to(self, coord):
        return True if coord in self.connections else False


def walk_pipes_from_S(tile_info):
    # step 0: types of pipes:
    pipe_types = {"|": "NS",
                  "-": "EW",
                  "L": "NE",
                  "J": "NW",
                  "7": "SW",
                  "F": "SE"}

    dirs = {"N": [0, -1], "S": [0, 1],
            "E": [1, 0], "W": [-1,0]}

    opposites = {"N": "S", "E": "W",
                 "W": "E", "S": "N"}

    # step 1 find the animal
    y = 0
    for content in tile_info:
        if "S" in content:
            x = content.find("S")
            break
        y += 1

    # step 2 determine pipe length
    going = "N"
    steps = 0
    current_pipe = "s"
    loop_tiles_for_part2 = dict()
    loop_list = []
    while current_pipe != "S":
        loop_list.append((x, y))
        xv, yv = dirs[going]

        new_tile = Tile(current_pipe)
        new_tile.connections.append((x+xv,y+yv))
        try:
            new_tile.connections.append(loop_list[-2])
        except:
            pass
        loop_tiles_for_part2[(x, y)] = new_tile

        x, y = x+xv, y+yv
        steps += 1
        current_pipe = tile_info[y][x]
        if current_pipe == "S":
            break

        going = pipe_types[current_pipe].replace(opposites[going], "")
    print('half circumfrence of loop')
    print(steps/2)
    return loop_list, loop_tiles_for_part2


def main():
    tile_info = load("10")
    test_print = ""
    loop_coords, loop_tiles = walk_pipes_from_S(tile_info)
    tiles_enclosed = 0

    for y in range(len(tile_info)):
        directions_of_vertical_pipes = ""
        inside_of_loop = False
        last_tile_coords = None
        row = tile_info[y]
        for x in range(len(row)):
            current_tile_coords = (x, y)

            on_pipe = current_tile_coords in loop_coords
            last_tile_was_pipe = last_tile_coords in loop_coords

            if on_pipe and last_tile_was_pipe:
                new_pipe = current_tile_coords not in loop_tiles[last_tile_coords].connections
            elif on_pipe:
                new_pipe = True
            else:
                new_pipe = False

            if new_pipe or (not on_pipe and last_tile_was_pipe):
                if directions_of_vertical_pipes in ["NS", "SN"]:
                    inside_of_loop = not inside_of_loop
                directions_of_vertical_pipes = ""

            if on_pipe:
                current_tile = loop_tiles[current_tile_coords]
                if current_tile.symbol in "F7":
                    directions_of_vertical_pipes += "S"
                elif current_tile.symbol in "LJ":
                    directions_of_vertical_pipes += "N"
                elif current_tile.symbol in "s|":
                    directions_of_vertical_pipes += "NS"

            if current_tile_coords in loop_coords:
                test_print += loop_tiles[(x, y)].symbol
            elif inside_of_loop:
                tiles_enclosed += 1
                test_print += "I"
            else:
                test_print += "O"
            last_tile_coords = (x, y)
        test_print += "\n"
    print("number of tiles enclosed or area")
    print(tiles_enclosed)
    print(test_print)

main()

#part2 try1 3046 too high
