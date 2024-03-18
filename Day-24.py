import itertools


def load(day):
    contents = open(f"./inputs/{day}.txt", "r").read().strip().split("\n")
    return contents


class Hailstone:
    def __init__(self, pos, vel):
        self.x, self.y, self.z = pos
        self.dx, self.dy, self.dz = vel

    def slope2d(self):
        return self.dy/self.dx

    def y_intercept(self):
        return self.y - (self.slope2d() * self.x)

    def in_future(self, point):
        deltax = point[0] - self.x
        deltay = point[1] - self.y
        return deltax/abs(deltax) == self.dx/abs(self.dx) and deltay/abs(deltay) == self.dy/abs(self.dy)

    def intersect2d(self, other_hailstone):
        test_area = (200000000000000, 400000000000000)
        if self.slope2d() == other_hailstone.slope2d():
            return False
        x0 = (self.y_intercept() - other_hailstone.y_intercept()) / (other_hailstone.slope2d() - self.slope2d())
        y0 = self.slope2d() * x0 + self.y_intercept()
        intersection = (x0, y0)
        if not(test_area[0] <= x0 <= test_area[1] and test_area[0] <= y0 <= test_area[1]):
            return False
        if not(self.in_future(intersection) and other_hailstone.in_future(intersection)):
            return False
        return True

    def __repr__(self):
        coord = (self.x, self.y, self.z)
        vel = (self.dx, self.dy, self.z)
        return f"coord: {coord}, velocity: {vel}"


def read_hailstones():
    lines = load("24")
    hailstones = []
    for line in lines:
        stats = line.split(" ")
        stats.remove('@')
        stats = list(map(lambda i: i.strip(","), stats))
        stats = list(map(int, stats))
        new_stone = Hailstone(stats[0:3], stats[3:])
        hailstones.append(new_stone)
    return hailstones


def main():
    intersection_count = 0
    for pair in itertools.combinations(read_hailstones(), 2):
        if pair[0].intersect2d(pair[1]):
            intersection_count += 1
    print(intersection_count)
    print(read_hailstones())

main()

"""
part 2:
there are hailstones H
for each hailstone they have linear parametric equations H_nxyz_n = {x0_n + tdx_n}, {y0_n + tdy_n}, {z0_n + tdz_n}
we are given each of the coord_0 values and slopes
we need to find the line that intersects all of these worldlines
Rock = Hn(t)

i think i can start by just finding a line that intersects 2 lines and check it against a 3rd line
then keep going til it hits all lines?

line that passes through xn,yn,zn,tn

19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3

x1 = 19 - 2t       x2 = 18 - t
y1 = 13 + t         y2 = 19 - t
z1 = 30 - 2t        z2 = 22 - 2t

x = x0 + mt
y = y0 + nt
z = z0 + lt

x0 + mt_1 = 19 - 2t_1       18 - t_2 = x0 + mt_2
x0 = 19 - 2t_1 - mt_1       18 - x0  = t_2 + mt_2
x0 = 10 - t_1 (2+m)         x0  = t_2(1 + m) + 18

10 - t_1 (2+m) = t_2 (1 + m) +18
-t_1 * (2+m) = t_2(1+m) + 8


(x0 - x)/m = t_1



"""


def mainpt2():
    stones = read_hailstones()
    a = stones[0]
    b = stones[1]
    t = 0
    while True:



        t+=1