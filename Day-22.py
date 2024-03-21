import itertools


def load(day):
    contents = open(f"./inputs/{day}.txt", "r").read().strip().split("\n")
    return contents


class Brick:
    def __init__(self, coords):
        xrange = range(coords[0][0], coords[1][0]+1)
        yrange = range(coords[0][1], coords[1][1]+1)
        zrange = range(coords[0][2], coords[1][2]+1)
        self.cubes = set()
        self.min_z = min(zrange)
        self.max_z = max(zrange)
        self.supporting = []
        self.supported_by = []
        for x in xrange:
            for y in yrange:
                for z in zrange:
                    self.cubes.add((x, y, z))

    def fall_by(self, fall_by):
        new_cubes = set()
        for cube in self.cubes:
            new_cube = (cube[0], cube[1], cube[2]-fall_by)
            self.min_z = min(self.min_z, new_cube[2])
            self.max_z = max(self.max_z, new_cube[2])
            new_cubes.add(new_cube)
        self.cubes = new_cubes

    def is_on_ground(self):
        for cube in self.cubes:
            if cube[2] == 1:
                return True
        return False

    def is_on_other_brick(self, other_brick):
        if other_brick in self.supported_by:
            return True
        if self.min_z != other_brick.max_z + 1:
            return False
        for cube in self.cubes:
            cube_below = (cube[0], cube[1], cube[2]-1)
            if cube_below in other_brick.cubes:
                return True
        return False

    def try_disintegrating(self):
        for brick in self.supporting:
            if len(brick.supported_by) == 1:
                return 0
        return 1


def read_bricks():
    raw_cube_data = load("22")
    bricks = []
    for line in raw_cube_data:
        halves = line.split("~")
        c1 = tuple(map(int, halves[0].split(",")))
        c2 = tuple(map(int, halves[1].split(",")))
        bricks.append(Brick([c1, c2]))
    return bricks


def lower_bricks(bricks):
    # figure out starting condition of bricks
    bricks = sorted(bricks, key=lambda k: k.min_z)
    highest = dict()
    for x in range(10):
        for y in range(10):
            highest[(x, y)] = 0

    for brick in bricks:
        distance_to_fall = brick.min_z - 1
        for cube in brick.cubes:
            x, y, z = cube
            distance_to_fall = min(distance_to_fall, z-highest[(x, y)]-1)
        brick.fall_by(distance_to_fall)
        for cube in brick.cubes:
            highest[(cube[0], cube[1])] = max(highest[(cube[0], cube[1])], cube[2])
    return bricks


def draw_yz_grid(bricks):
    max_y = 0
    max_z = 0
    output = ""
    for brick in bricks:
        for cube in brick.cubes:
            if cube[1] > max_y:
                max_y = cube[1]
            if cube[2] > max_z:
                max_z = cube[2]
    for z in reversed(range(max_z+1)):
        row = ""
        for y in range(max_y+1):
            empty = True
            for brick in bricks:
                if not empty:
                    break
                for cube in brick.cubes:
                    if cube[1] == y and cube[2] == z:
                        empty = False
                        break
            if empty:
                row += "."
            else:
                row += "#"
        output += row + "\n"
    print(output)


def find_all_supports(bricks):
    for pair in itertools.permutations(bricks, 2):
        brick1, brick2 = pair
        if brick1.is_on_other_brick(brick2):
            brick1.supported_by.append(brick2)
            brick2.supporting.append(brick1)
    return bricks


def main():
    bricks = read_bricks()
    draw_yz_grid(bricks)
    print(f"number of bricks: {len(bricks)}")
    print("lowering bricks... quicker?")
    bricks = lower_bricks(bricks)
    bricks = find_all_supports(bricks)
    draw_yz_grid(bricks)
    disintegrate_count = 0
    print("testing disintegration")
    count = 0
    for brick in bricks:
        #print(f"{count} / {len(bricks)}")
        disintegrate_count += brick.try_disintegrating()
        count += 1
    print(disintegrate_count)


main()

# pt 1 1456 too high
# pt 1 427 too low
# 468, 475, 491, 487, 1446

