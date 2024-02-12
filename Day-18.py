def load(day):
    contents = open(f"./inputs/{day}.txt", "r").read().strip().split("\n")
    return contents


class Instruction:
    def __init__(self, line):
        self.direction, self.length, self.color = line.split(" ")
        self.color = self.color.strip("()")
        self.length = int(self.length)

def get_dig_instructions():
    raw_instructions = load("18")
    instructions = []
    for line in raw_instructions:
        instructions.append(Instruction(line))
    return instructions


def create_trenches():
    instructions = get_dig_instructions()
    holes = set([(0, 0)])
    pos = (0,0)
    dirs = {"L": [-1, 0], "R": [1, 0], "D": [0, 1], "U": [0, -1]}
    for instruction in instructions:
        head = dirs[instruction.direction]
        for _ in range(instruction.length):
            pos = (pos[0]+head[0], pos[1]+head[1])
            holes.add(pos)
    return holes


def print_holes(holes):
    hmin = min(list(map(lambda i: i[0], holes)))
    hmax = max(list(map(lambda i: i[0], holes)))
    vmin = min(list(map(lambda i: i[1], holes)))
    vmax = max(list(map(lambda i: i[1], holes)))
    out = ""
    for x in range(hmin, hmax + 1):
        for y in range(vmin, vmax + 1):
            if (x, y) in holes:
                out += "#"
            else:
                out += "."
        out += "\n"
    print("before fill")
    print(out)


def fill_holes(holes):
    hmin = min(list(map(lambda i: i[0], holes)))
    hmax = max(list(map(lambda i: i[0], holes)))
    vmin = min(list(map(lambda i: i[1], holes)))
    vmax = max(list(map(lambda i: i[1], holes)))
    candidates = set()
    dirs = {"L": [-1, 0], "R": [1, 0], "D": [0, 1], "U": [0, -1]}
    for x in range(hmin, hmax +1):
        if (x, vmin) in holes:
            if (x, vmin+1) not in holes:
                candidates.add((x, vmin+1))
    while len(candidates)>0:
        next_candidate = candidates.pop()
        for char in "LRUD":
            head = dirs[char]
            check = (next_candidate[0]+head[0], next_candidate[1]+head[1])
            if check not in holes:
                holes.add(check)
                candidates.add(check)
    return holes


def main():
    holes = create_trenches()
    print_holes(holes)
    holes = fill_holes(holes)
    print_holes(holes)
    print(len(holes))








main()
