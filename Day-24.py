import itertools
import numpy


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

    def collide(self, other_hailstone):
        # t = (1_i - 2_i) / (2_v - 1_v)
        if self.dx==other_hailstone.dx or self.dy==other_hailstone.dy or self.dz==other_hailstone.dz:
            return False
        tx = (self.x - other_hailstone.x) / (other_hailstone.dx - self.dx)
        ty = (self.y - other_hailstone.y) / (other_hailstone.dy - self.dy)
        tz = (self.z - other_hailstone.z) / (other_hailstone.dz - self.dz)
        return tx==ty==tz #and tx%1==0

    def __repr__(self):
        coord = (self.x, self.y, self.z)
        vel = (self.dx, self.dy, self.dz)
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


def mainpt1():
    intersection_count = 0
    for pair in itertools.combinations(read_hailstones(), 2):
        if pair[0].intersect2d(pair[1]):
            intersection_count += 1
    print(intersection_count)
    #print(read_hailstones())

mainpt1()

"""
part 2: scratchpad thinking, probably going to find a hand solution somehow
there are hailstones H
for each hailstone they have linear parametric equations H_nxyz_n = {x0_n + tdx_n}, {y0_n + tdy_n}, {z0_n + tdz_n}
we are given each of the coord_0 values and slopes
we need to find the line that intersects all of these worldlines
Rock = Hn(t)

"""


def find_2d_speeds():
    print("\n\n\nDay 2:")
    stones = read_hailstones()
    for pair in itertools.combinations(stones,2):
        h1, h2 = pair
        if h1.dx == h2.dx and h1.dy == h2.dy:
            print(h1)
            print(h2)
    for trio in itertools.combinations(stones,3):
        h1, h2, h3 = trio
        if h1.dx == h2.dx == h3.dx:
            print(h1)
            print(h2)
            print(h3)
    print('z dimension')
    for pair in itertools.combinations(stones, 2):
        h1, h2 = pair
        if h1.dz == h2.dz:
            print(h1)
            print(h2)

    # ok if we match 2 things to have the same speeds,

    """
    resulting matches
    coord: (371401572831816, 109743759343214, 256669453937408), velocity: (-26, 120, 256669453937408)
    coord: (261914840973816, 241127837572814, 160786917788859), velocity: (-26, 120, 160786917788859)
    
    coord: (333356731903056, 357209684397110, 194072655195651), velocity: (32, -178, 194072655195651)
    coord: (298318963347266, 355284532278660, 501265513362196), velocity: (32, -178, 501265513362196)
    coord: (191772314964910, 331891699815218, 159959225249315), velocity: (32, -12, 159959225249315)
    
    scratchpad of better ideas:
    Rock = rock.x.i + rock.y.i + t*rock.dx + t*rock.dy
    h1 = h1.x.i + h1.y.i + t*(h1.dx + h1.dy)
    h2 = h2.x.i + h2.y.i + t*(h2.dx + h2.dy)
    but if we take the above found items where h1.dx=h2.dx etc.
    h1 = h1.x.i + h1.y.i + t*(dx + dy)
    h2 = h2.x.i + h2.y.i + t*(dx + dy)
    
    if we say at some times t1 and t2, the hailstones intersect the rock,
    h1(t1) = rock(t1)
    h2(t2) = rock(t2) 
    h1(t1) = h1.x.i + h1.y.i + t1*(dx + dy)
    h2(t2) = h2.x.i + h2.y.i + t2*(dx + dy)
    rock(t2)-rock(t1) = h2(t2) - h1(t1)
    (rock.dx + rock.dy) * (t2-t1)                       = (h2.x.i - h1.x.i) + (h2.y.i - h1.y.i) + (dx + dy)*(t2 - t1)
    (rock.dx + rock.dy) * (t2-t1) - (dx + dy)*(t2 - t1) = (h2.x.i - h1.x.i) + (h2.y.i - h1.y.i) 
    (rock.dx + rock.dy) - (dx + dy) * (t2 -t1)          = (h2.x.i - h1.x.i) + (h2.y.i - h1.y.i) 
    (rock.dx + rock.dy) - (dx + dy)                     = (h2.x.i - h1.x.i) + (h2.y.i - h1.y.i) / (t2 - t1)
    
    (rock.dx + rock.dy) = (dx + dy) + ((h2.x.i - h1.x.i) + (h2.y.i - h1.y.i)) / (t2 - t1)
    
    
    
    not really sure what to do with that, and i dont know 
    that the matched speeds matter, i could match 3 
    rocks with matching speeds in the 
    3rd dimension so that i know that dz doesnt matter

    or then i add in some 3rd rock.
    
    rock(t3)-rock(t1) = h3(t3) - h1(t1)
    rock(t3)-rock(t2) = h3(t3) - h1(t2)
    (rock.dx + rock.dy) * (t3-t1) = (h3.x.i - h1.x.i) + (h3.y.i - h1.y.i) + (dx + dy)*(t3 - t1) 
    (rock.dx + rock.dy) * (t3-t2) = (h3.x.i - h2.x.i) + (h3.y.i - h2.y.i) + (dx + dy)*(t3 - t2)
    t3-t1 = (t3-t2)+(t2-t1)
    t3-t2 = (t3-t1)-(t2-t1)
    
    ok new idea after staring at the above horseshit for a while:
    rock_x = rock_x_i + rock_dx*t
    
    
    hail_1_x = hail_1_x_i + hail_1_dx*t
    hail_2_x = hail_2_x_i + hail_2_dx*t
    
    but for each dimension there are stones where their velocity in x (or y or z) is the same
    hail_1_x(t) = hail_1_x_i + hail_dx*t
    hail_2_x(t) = hail_2_x_i + hail_dx*t
    
    subtract one equation from the other
    hail_2_x(t) - hail_1_x(t) = hail_2_x_i - hail_1_x_i
    
    since we are looking for rock_x(t2) = hail_2(t2), and rock_x(t1) = hail_1(t1)
    rock_x(t2)-rock_x(t1) = hail_2_x(t2)-hail_1_x(t1) = hail_2_x_i + hail_dx*t2 - hail_1_x_i + hail_dx*t1
    rock_x(t2)-rock_x(t1) = (hail_2_x_i - hail_1_x_i) + hail_dx*(t2-t1)
    rock_x(t2)-rock_x(t1) = rock_dx*(t2 -t1)
    rock_dx = (hail_2_x_i - hail_1_x_i)/(t2-t1) + hail_dx
    
    
    
    rock_x(t2) - rock_x(t1) = hail_2_x - hail_1_x = hail_2_x_i - hail_1_x_i
    = rock_x_i + rock_dx*(t2) - (rock_x_i - rock_dx*(t1))
    rock_dx*(t2-t1) = hail_2_x_i - hail_1_x_i
    
    since t2 and t1 have to be integers (i am pretty sure)
    rock_dx = (hail_2_x_i - hail_1_x_i) / (t2-t1)
    maybe i can iterate through integer divisors for integer speeds rock_dx,
    
    lets look at these two hailstones:
    coord: (371401572831816, 109743759343214, 256669453937408), velocity: (-26, 120, 256669453937408)
    coord: (261914840973816, 241127837572814, 160786917788859), velocity: (-26, 120, 160786917788859)
    
    the differences in x_i: 109486731858000
    
    """
def find_divisors_for_x_i():
    x_i = 109486731858000
    dt = 1
    divisors = []
    while True:
        if x_i % dt == 0:
            divisors.append(dt)
            divisors.append(x_i//dt)
        dt += 1
        if dt > numpy.sqrt(x_i):
            break

    print(divisors)

"""
so the above method yields a lot of possible values (and slowly), 
but luckily, these two hailstones have 2 matching speeds and so
differences in y_i = -131384078229600
and i just have to find the values where they are divisible into both of these:
"""

def find_divisors_for_x_i_and_y_i():
    x_i = 109486731858000
    y_i = 131384078229600
    dt = 1
    possible_speed_pairs = []
    while True:
        if x_i % dt == 0 and y_i % dt == 0:
            rock_dx = x_i / dt
            rock_dy = y_i / dt
            possible_speed_pairs.append([rock_dx, rock_dy])
        dt += 1
        if dt > numpy.sqrt(x_i):
            break
    print(possible_speed_pairs)
    return possible_speed_pairs


#find_divisors_for_x_i_and_y_i()

"""
so these list of divisors give us vaules for rock_dx = (hail_2_x_i - hail_1_x_i) / (t2-t1)
                                             rock_dy = (hail_2_y_i - hail_1_y_i) / (t2-t1)
by asserting some integer difference in the time, i get a list of speeds from position_difference/time_difference
to find a starting point, what if I iterate through all matching speeds and such to reduce the possible list of velocities?

then once i have identified Vxyz for the rock, i can find its initial position by 




"""

def get_possible_velocities(i1, i2, vx):
    di = abs(i2 - i1)
    dt = 1
    vs = []
    while dt <=1000: #<= numpy.sqrt(di):
        if di % dt == 0:
            v1 = di // dt
            v2 = di // v1
            vs.append(v1 + vx)
            vs.append(v2 + vx)
            vs.append(-v1 + vx)
            vs.append(-v2 + vx)
        dt+=1
    return vs

def reduce_vector_list(true_v, new_vs):
    if not true_v:
        return set(new_vs)
    else:
        return true_v.intersection(set(new_vs))

def main_pt_2():
    stones = read_hailstones()
    true_dx = None
    true_dy = None
    true_dz = None
    dx_done = False
    dy_done = False
    dz_done = False
    for pair in itertools.combinations(stones, 2):
        h1, h2 = pair
        if h1.dx == h2.dx and not dx_done:
            dxs = get_possible_velocities(h1.x, h2.x, h1.dx)
            true_dx = reduce_vector_list(true_dx, dxs)
        if h1.dy == h2.dy and not dy_done:
            dys = get_possible_velocities(h1.y, h2.y, h1.dy)
            true_dy = reduce_vector_list(true_dy, dys)
        if h1.dz == h2.dz and not dz_done:
            dzs = get_possible_velocities(h1.z, h2.z, h1.dz)
            true_dz = reduce_vector_list(true_dz, dzs)

        if type(true_dx) == set:
            dx_done = len(true_dx) == 1
        if type(true_dy) == set:
            dy_done = len(true_dy) == 1
        if type(true_dz) == set:
            dz_done = len(true_dz) == 1
    print(true_dx) # 214
    print(true_dy) # -168
    print(true_dz) # 249

    hailstone_1 = stones[0]
    hailstone_2 = stones[1]
    hailstone_3 = stones[2]
    rock_dx = true_dx.pop()
    rock_dy = true_dy.pop()
    rock_dz = true_dz.pop()

    for h in stones:
        if rock_dx == h.dx:
            print('x')
            print(h.x)
        if rock_dy == h.dy:
            print('y')
            print(h.y)
        if rock_dz == h.dz:
            print('z')
            print(h.z)

    t = 1
    mult = 1
    # just going to iterate up through time until we find the right values
    while True:
        rock_x = (hailstone_1.dx - rock_dx)*t + hailstone_1.x
        rock_y = (hailstone_1.dy - rock_dy)*t + hailstone_1.y
        rock_z = (hailstone_1.dz - rock_dz)*t + hailstone_1.z
        test_rock = Hailstone([rock_x,rock_y,rock_z],[rock_dx,rock_dy,rock_dz])
        if test_rock.collide(hailstone_2) and test_rock.collide(hailstone_3):
            print(sum([rock_z,rock_x,rock_y]))
            print("please have worked")
            break
        t+=1
        if t%10000==0:
            #print(t)
            pass

# bailing and starting over
