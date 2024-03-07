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
                    self.cubes.add((x,y,z))

    def go_down(self):
        new_cubes = set()
        for cube in self.cubes:
            new_cube = (cube[0],cube[1],cube[2]-1)
            self.min_z = min(self.min_z, new_cube[2])
            self.max_z = max(self.min_z, new_cube[2])
            new_cubes.add(new_cube)
        self.cubes = new_cubes

    def is_on_ground(self):
        for cube in self.cubes:
            if cube[2]==1:
                return True
        return False

    def is_on_other_brick(self, other_brick):
        if other_brick in self.supported_by:
            return True
        if self.min_z != other_brick.max_z + 1:
            return False
        for cube in self.cubes:
            cube_below = (cube[0],cube[1],cube[2]-1)
            if cube_below in other_brick.cubes:
                self.supported_by.append(other_brick)
                other_brick.supporting.append(self)
                return True
        return False

    def try_disintegrating(self, bricks):
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


def sort_bricks_into_grounded_and_falling(grounded_bricks, falling_bricks):
    newly_grounded_count = 1
    while newly_grounded_count > 0:
        newly_grounded_count = 0
        to_fall = []
        for brick in falling_bricks:
            brick_falling = True
            if brick.is_on_ground():
                grounded_bricks.append(brick)
                newly_grounded_count += 1
                brick_falling = False
            else:
                for ground_brick in grounded_bricks:
                    if brick.is_on_other_brick(ground_brick):
                        if brick_falling:
                            newly_grounded_count += 1
                            grounded_bricks.append(brick)
                            brick_falling = False
            if brick_falling:
                to_fall.append(brick)
        falling_bricks = to_fall
    return grounded_bricks, falling_bricks


def lower_bricks(bricks):
    # figure out starting condition of bricks
    grounded_bricks = []
    grounded_bricks, bricks_to_fall = sort_bricks_into_grounded_and_falling(grounded_bricks, bricks)
    while len(bricks_to_fall) > 0:
        print(str(100*len(bricks_to_fall)/len(bricks))[:5]+"%")
        for brick in bricks_to_fall:
            brick.go_down()
        grounded_bricks, bricks_to_fall = sort_bricks_into_grounded_and_falling(grounded_bricks, bricks_to_fall)
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
                    if cube[1]==y and cube[2]==z:
                        empty = False
                        break
            if empty:
                row += "."
            else:
                row += "#"
        output += row + "\n"
    print(output)


def main():
    bricks = read_bricks()
    draw_yz_grid(bricks)
    print(len(bricks))
    print("lowering bricks... slowly")
    bricks = lower_bricks(bricks)
    draw_yz_grid(bricks)
    disintegrate_count = 0
    print("testing disintegration")
    count = 0
    for brick in bricks:
        print(f"{count} / {len(bricks)}")
        disintegrate_count += brick.try_disintegrating(bricks)
        count+=1
    print(disintegrate_count)

main()

# pt 1 1456 too high
# pt 2 427 too low
# 468 someone elses lol
