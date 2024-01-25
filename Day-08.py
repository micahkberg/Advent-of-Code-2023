def load(day):
    contents = open(f"./inputs/{day}.txt", "r").read().strip().split("\n")
    return contents

class Node:
    def __init__(self, name, l, r):
        self.L = l
        self.R = r
        self.name = name

    def get_next_node_name(self, direction):
        return {"L": self.L, "R": self.R}[direction]


def read_contents():
    contents = load("08")
    LR = contents[0]
    nodes = dict()
    for line in contents[2:]:
        name = line.split()[0]
        l = line.split()[2].strip('(,')
        r = line.split()[3].strip(')')
        nodes[name] = Node(name,l,r)
    return LR, nodes


def mainPart1():
    LR, nodes = read_contents()
    current_node = nodes["AAA"]
    steps_taken = 0
    while current_node.name != "ZZZ":
        next_direction = LR[steps_taken%len(LR)]
        current_node = nodes[{"L": current_node.L, "R": current_node.R}[next_direction]]
        steps_taken += 1
        if steps_taken%1000000==0:
            print(steps_taken)
    print(steps_taken)


def mainPart2():
    LR, all_nodes = read_contents()
    #looks like just need to take LCM of these path lengths

    def steps_to_11Z(node, ztest=False):
        steps_taken=0
        while True:
            next_direction = LR[steps_taken%len(LR)]
            node = all_nodes[{"L": node.L, "R": node.R}[next_direction]]
            steps_taken += 1
            if node.name[-1] == "Z":
                print(node.name)
                break
        print(steps_taken)
        #if not ztest:
        #    steps_to_11Z(node, True)
        return steps_taken

    def lcm(a,b):
        return a*b/gcd(a,b)

    def gcd(a,b):
        a,b = sorted([a,b])
        if a==0:
            return int(b)
        else:
            return gcd(a, b%a)

    steps = len(LR)
    for n in all_nodes.values():
        if n.name[-1] == "A":
            print(n.name)
            steps = lcm(steps, steps_to_11Z(n))

    print(steps)

#try 1 too low, 2010045535
#try 2 10668805667831

mainPart2()
