# attempting part 2 in a cleaner file

import itertools
import numpy


def load(day):
    contents = open(f"./inputs/{day}.txt", "r").read().strip().split("\n")
    return contents


class Hailstone:
    def __init__(self, pos, vel):
        self.x, self.y, self.z = pos
        self.dx, self.dy, self.dz = vel
        self.idnum = None

    def collide(self, other_hailstone):
        # t = (1_i - 2_i) / (2_v - 1_v)
        if self.dx == other_hailstone.dx or self.dy == other_hailstone.dy or self.dz == other_hailstone.dz:
            print("parallel issue")
            return False
        tx = (self.x - other_hailstone.x) / (other_hailstone.dx - self.dx)
        ty = (self.y - other_hailstone.y) / (other_hailstone.dy - self.dy)
        tz = (self.z - other_hailstone.z) / (other_hailstone.dz - self.dz)
        if tx == ty == tz:
            return tx > 0
        return tz

    def distance_from_start_dir(self):
        return self.x - self.y + self.z

    def __repr__(self):
        coord = (self.x, self.y, self.z)
        vel = (self.dx, self.dy, self.dz)
        return f"coord: {coord}, velocity: {vel}"


def read_hailstones():
    lines = load("24")
    hailstones = []
    idnum = 0
    for line in lines:
        stats = line.split(" ")
        stats.remove('@')
        stats = list(map(lambda i: i.strip(","), stats))
        stats = list(map(int, stats))
        new_stone = Hailstone(stats[0:3], stats[3:])
        new_stone.idnum = idnum
        hailstones.append(new_stone)
        idnum += 1
    return hailstones


def get_possible_velocities(i1, i2, vx):
    di = abs(i2 - i1)
    dt = 1
    vs = []
    while dt <= min([1000, numpy.sqrt(di)]):
        if di % dt == 0:
            v1 = di // dt
            v2 = di // v1
            vs.append(v1 + vx)
            vs.append(v2 + vx)
            vs.append(-v1 + vx)
            vs.append(-v2 + vx)
        dt += 1
    return vs


def reduce_vector_list(true_v, new_vs):
    if not true_v:
        return set(new_vs)
    else:
        return true_v.intersection(set(new_vs))


def main_pt2():
    stones = read_hailstones()

    """
    Hailstones H
    Velocities V
    time t
    initial positions P

    H_n = V_n * t + P_n
    Rock = V_r * t + P_r

    Rock(t_n) = H_n(t_n) = V_n * t_n + P_n = V_r * t_n + P_r
    H_1 and H_2 where V_1.x == V_2.x, we will call them just V.x

    Rock(t_2) - Rock(t_1) = H_2(t_2) - H_1(t_1)
    V_r * (t_2 - t_1) = V.x * (t_2 - t_1) + P_2 - P_1
    (V_r - V.x)(t_2 - t_1) = P_2 - P_1
    V_r = ((P_2 - P_1)/(t_2 - t_1)) + V.x

    so we are looking for some integer time interval that divides the difference
    in start positions between two hailstones.
    if we iterate through stones to find the ones with matching velocities

    lets call t2-t1 "dt" (difference in time)
    lets call P_2-P_1 "di" (difference in initial positions)
    """

    true_dx = None
    true_dy = None
    true_dz = None
    dx_done = False
    dy_done = False
    dz_done = False
    for pair in itertools.combinations(stones, 2):
        h1, h2 = pair
        new_nums = False
        if h1.dx == h2.dx and not dx_done:
            dxs = get_possible_velocities(h1.x, h2.x, h1.dx)
            true_dx = reduce_vector_list(true_dx, dxs)
            new_nums = True
        if h1.dy == h2.dy and not dy_done:
            dys = get_possible_velocities(h1.y, h2.y, h1.dy)
            new_nums = True
            true_dy = reduce_vector_list(true_dy, dys)
        if h1.dz == h2.dz and not dz_done:
            dzs = get_possible_velocities(h1.z, h2.z, h1.dz)
            new_nums = True
            true_dz = reduce_vector_list(true_dz, dzs)

        if type(true_dx) == set:
            dx_done = len(true_dx) == 1
        if type(true_dy) == set:
            dy_done = len(true_dy) == 1
        if type(true_dz) == set:
            dz_done = len(true_dz) == 1
        #if new_nums:
        #    print(true_dx)  # 214
        #    print(true_dy)  # -168
        #    print(true_dz)  # 249
    print(true_dx)  # 214
    print(true_dy)  # -168
    print(true_dz)  # 249
    rock_dx = true_dx.pop()
    rock_dy = true_dy.pop()
    rock_dz = true_dz.pop()

    dts = list()
    for pair in itertools.combinations(stones, 2):
        h1, h2 = pair
        if h1.dx == h2.dx:
            dt = (h2.x - h1.x) / (rock_dx - h1.dx)
            dts.append([h1, h2, dt])
        if h1.dy == h2.dy:
            dt = (h2.y - h1.y) / (rock_dy - h1.dy)
            dts.append([h1, h2, dt])
        if h1.dz == h2.dz:
            dt = (h2.z - h1.z) / (rock_dz - h1.dz)
            dts.append([h1, h2, dt])
    for dt in dts:
        print(dt)
    """
    so now that we have the effective slopes of the rock, we have to figure out its actual initial start positions
    V_r is now known
    Rock = V_r*t + P_r
    H_n = V_n * t + P_n
    
    lets say we want to try and put this in matrix form:
    columns will be for t1, t2, t3, etc. and xi, yi, and zi,
    lets say we take the first 3 lines of dt:
    [coord: (176253337504656, 321166281702430, 134367602892386), velocity: (190, 8, 338), coord: (307032218923206, 220427490765998, 286976738475573), velocity: (29, 8, 58), 572379493957.0]
    [coord: (176253337504656, 321166281702430, 134367602892386), velocity: (190, 8, 338), coord: (192355441091208, 289762636514572, 280207383018611), velocity: (190, -97, 89), 670920982773.0]
    [coord: (176253337504656, 321166281702430, 134367602892386), velocity: (190, 8, 338), coord: (308344120080284, 193172753823598, 249535698501761), velocity: (60, 8, 134), 727235953857.0]
    i.e.
    h1,h2,t2-t1
    h1,h3,t3-t1
    h1,h4,t4-t1
    
    we can abbreviate our source equations as this:
    h1.dx*t1 + h1.x = rock_dx*t1 + rock.x
    (h1.dx-rock_dx)*t1 - rock.x = -h1.x
    (h1.dy-rock_dy)*t1 - rock.y = -h1.y
    (h1.dz-rock_dz)*t1 - rock.z = -h1.z
    (h2.dx-rock_dx)*t2 - rock.x = -h2.x
    (h2.dy-rock_dy)*t2 - rock.y = -h2.y
    (h2.dz-rock_dz)*t2 - rock.z = -h2.z
    etc, through h4,t4
    t2-t1=dt1
    t3-t1=dt2
    t4-t1=dt3
    
    thus my variables would be t1,t2,t3,t4,xi,yi,zi
    matrix constitution:
    t1          t2          t3          t4          xi          yi          zi      .xyz/dt
    h1.dx-r.dx  0           0           0           -1          0           0       -h1.x
    
    -1          1           0           0           0           0           0       dt1
    -1          0           1           0           0           0           0       dt2
    -1          0           0           1           0           0           0       dt3
    
    hmm, not working, what if i add more equations lol,
    adding h5 and h6 and h7:

    
    """
    h1, h2, dt1 = dts[0]
    h1, h3, dt2 = dts[1]
    h1, h4, dt3 = dts[2]

    test_matrix_A = numpy.array(
        [[h1.dx - rock_dx, 0, 0, 0, -1, 0, 0],
         [h1.dy - rock_dy, 0, 0, 0, 0, -1, 0],
         [h1.dz - rock_dz, 0, 0, 0, 0, 0, -1],
         [0, h2.dx - rock_dx, 0, 0, -1, 0, 0],
         [0, h2.dy - rock_dy, 0, 0, 0, -1, 0],
         [0, h2.dz - rock_dz, 0, 0, 0, 0, -1],
         [0, 0, h3.dx - rock_dx, 0, -1, 0, 0],
         [0, 0, h3.dy - rock_dy, 0, 0, -1, 0],
         [0, 0, h3.dz - rock_dz, 0, 0, 0, -1],
         [0, 0, 0, h4.dx - rock_dx, -1, 0, 0],
         [0, 0, 0, h4.dy - rock_dy, 0, -1, 0],
         [0, 0, 0, h4.dz - rock_dz, 0, 0, -1],
         [-1, 1, 0, 0, 0, 0, 0],
         [-1, 0, 1, 0, 0, 0, 0],
         [-1, 0, 0, 1, 0, 0, 0]
         ], dtype=numpy.int64)
    #test_matrix_A = numpy.pad(test_matrix_A,[(0,0),(0,8)],mode='constant')
    print(test_matrix_A.shape)
    test_matrix_B = numpy.array([-h1.x, -h1.y, -h1.z, -h2.x, -h2.y, -h2.z,
                                 -h3.x, -h3.y, -h3.z, -h4.x, -h4.y, -h4.z, dt1, dt2, dt3], dtype=numpy.int64)
    #print(test_matrix)
    res = numpy.linalg.lstsq(test_matrix_A, test_matrix_B)
    print(res)
    xs = res[0]
    rock_xi, rock_yi, rock_zi = xs[-3:]
    t1, t2, t3, t4 = xs[:4]
    print(sum(xs[-3:]))
    print([dt1, dt2, dt3])
    print([xs[1]-xs[0], xs[2]-xs[0], xs[3]-xs[0]])

    """
    what if i just look around this general area for an answer...
    """
    t1 = int(t1 // 1)
    off_set = 1
    while True:
        answer = None
        t1_above = t1+off_set
        t1_below = t1-off_set
        for t1_test in [t1_above, t1_below]:
            x = h1.dx * t1_test + h1.x
            y = h1.dy * t1_test + h1.y
            z = h1.dz * t1_test + h1.z

            xi = x - rock_dx * t1_test
            yi = y - rock_dy * t1_test
            zi = z - rock_dz * t1_test
            potential_rock = Hailstone([xi, yi, zi], [rock_dx, rock_dy, rock_dz])
            h10 = stones[10] # random other stone
            if potential_rock.collide(h10):
                answer = xi + yi + zi
                break
        if answer:
            break
    print(answer)

    # wild

    # print(rock_xi + rock_yi + rock_zi)


main_pt2()
# 661196463254978 too low
# 669042940632375 STILL LOW
# 669042940632377