"""
written before realizing that parts could have multiple numbers, abandoning
"""


today = "03test"
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
        self.part_number = self.find_part_number()

    def find_part_number(self):
        dirs = itertools.product([-1,0,1],repeat=2)
        num_found = False
        for dir in dirs:
            x = dir[0] + self.x
            y = dir[1] + self.y
            if x in range(len(lines[0])) and y in range(len(lines)):
                if lines[y][x] in "1234567890":
                    num_found = True
                    part_number = lines[y][x]
                    break
        if num_found:
            i=1
            while True:
                try:
                    if lines[y][x-i] in "1234567890":
                        part_number = lines[y][x-i] + part_number
                        i+=1
                    else:
                        break

                except:
                    break
            i=1
            while True:
                try:
                    if lines[y][x+i] in "1234567890":
                        part_number += lines[y][x+i]
                        i+=1
                    else:
                        break
                except:
                    break
            return int(part_number)
        else:
            return Exception("no part number found")


def search_for_parts():
    parts = []
    part_num_sum = 0
    for y in range(len(lines)):
        line = lines[y]
        for x in range(len(line)):
            if line[x] not in ".1234567890":
                parts.append(Part(line[x], x, y))
    for part in parts:
        part_num_sum += part.part_number
    print(part_num_sum)

search_for_parts()