def load(day):
    contents = open(f"./inputs/{day}.txt", "r").read().strip().split("\n")
    return contents


class Instruction:
    def __init__(self, line):
        fake_direction, fake_length, self.hash_info = line.split(" ")
        self.hash_info = self.hash_info.strip("()#")
        self.length = int(self.hash_info[:5], 16)
        self.direction = "RDLU"[int(self.hash_info[-1])]


class Edge:
    def __init__(self, pos1, pos2):
        self.x1 = pos1[0]
        self.x2 = pos2[0]
        self.y1 = pos1[1]
        self.y2 = pos2[1]

    def determinant(self):
        a = self.x1
        b = self.x2
        c = self.y1
        d = self.y2
        return a*d - b*c


def get_dig_instructions():
    raw_instructions = load("18")
    instructions = []
    for line in raw_instructions:
        instructions.append(Instruction(line))
    return instructions


def create_trenches():
    instructions = get_dig_instructions()
    edges = []
    pos = (0, 0)
    dirs = {"L": [-1, 0], "R": [1, 0], "D": [0, 1], "U": [0, -1]}
    for instruction in instructions:
        head = dirs[instruction.direction]
        next_pos = (pos[0]+head[0]*instruction.length, pos[1]+head[1]*instruction.length)
        new_edge = Edge(pos, next_pos)
        pos = next_pos
        edges.append(new_edge)
    return edges


def shoelace_with_picks_formula(edges):
    interior_area = 0
    perimeter = 0
    for edge in edges:
        interior_area += edge.determinant()/2
        perimeter += abs(edge.x1-edge.x2) + abs(edge.y1-edge.y2)
    return interior_area + perimeter/2 + 1


def main():
    edges = create_trenches()
    area = shoelace_with_picks_formula(edges)
    print(area)

main()


def test_formula():
    L = 2
    M = 2
    edge1 = Edge((0, 0), (L, 0))
    edge2 = Edge((L, 0), (L, M))
    edge3 = Edge((L, M), (0, M))
    edge4 = Edge((0, M), (0, 0))
    edges = [edge1,edge2,edge3,edge4]
    print(shoelace_with_picks_formula(edges))

test_formula()


# 68548216873199 too low


