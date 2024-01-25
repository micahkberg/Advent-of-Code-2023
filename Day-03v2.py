today = "03"
import itertools

def load(day):
    contents = open(f"./inputs/{day}.txt", "r").read().strip().split("\n")
    return contents

lines = load(today)

class Part:
    def __init__(self, symbol, x, y):
        self.symbol = symbol
        self.x = x
        self.y = y
        self.nums = []

    def is_gear(self):
        if self.symbol == "*" and len(self.nums)==2:
            return True

    def add_number(self, number):
        self.nums.append(int(number))

    def get_number(self):
        return sum(self.nums)

    def get_gear_number(self):
        if self.is_gear():
            return self.nums[0]*self.nums[1]
        else:
            return 0

def search_for_parts():
    parts = []
    part_num_sum = 0
    for y in range(len(lines)):
        line = lines[y]
        for x in range(len(line)):
            if line[x] not in ".1234567890":
                parts.append(Part(line[x], x, y))
    return parts

def find_neighbor_part(x,y):
    dirs = itertools.product([-1, 0, 1], repeat=2)
    for direction in dirs:
        x0 = x+direction[0]
        y0 = y+direction[1]
        for part in parts:
            if x0==part.x and y0==part.y:
                return part
    return False

def search_for_numbers():
    current_number = ""
    part = None
    for y in range(len(lines)):
        line = lines[y]
        for x in range(len(line)):
            char = line[x]
            if char in "1234567890":
                current_number+=char
                if not part:
                    part = find_neighbor_part(x,y)
            elif current_number and part:
                part.add_number(current_number)
                current_number = ""
                part = None
            elif current_number:
                current_number = ""



parts = search_for_parts()
search_for_numbers()
print("Part1")
print(sum(map(lambda i:i.get_number(), parts)))
print("Part2")
print(sum(map(lambda i:i.get_gear_number(), parts)))