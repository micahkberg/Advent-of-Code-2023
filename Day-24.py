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




main()
