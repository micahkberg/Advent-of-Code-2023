import re


def get_input():
    day = "15"
    initialization_sequence = open(f"./inputs/{day}.txt", "r").read().strip().split("\n")[0]
    initialization_sequence = initialization_sequence.split(",")
    return initialization_sequence


def ascii_hash(inp):
    value = 0
    for char in inp:
        value += ord(char)
        value *= 17
        value = value % 256
    return value


def focusing_power(boxes):
    power = 0
    for box, lenses in boxes.items():
        box_power = 1 + box
        for lens_num in range(len(lenses)):
            f = lenses[lens_num][1]
            power += box_power * (lens_num+1) * f
    return power


def remove_lens(box_list, label):
    new_box_list = []
    for lens in box_list:
        if lens[0] == label:
            pass
        else:
            new_box_list.append(lens)
    return new_box_list


def add_lens(box_list, label, f):
    new_box_list = []
    lens_placed = False
    for lens in box_list:
        if lens[0] == label:
            new_box_list.append([label, f])
            lens_placed = True
        else:
            new_box_list.append(lens)
    if not lens_placed:
        new_box_list.append([label, f])
    return new_box_list


def main():
    hashes = []
    commands = get_input()
    for command in commands:
        hashes.append(ascii_hash(command))
    print(f"part 1: verifying sequence: {sum(hashes)}")

    boxes = dict()
    for i in range(256):
        boxes[i] = []

    for command in commands:
        # print(command)
        re_tst = re.match("\w+", command)
        label = re_tst.group()
        operation = command[re_tst.span()[1]]
        box = ascii_hash(label)
        if operation == "-":
            boxes[box] = remove_lens(boxes[box], label)
        elif operation == "=":
            f = int(command[re_tst.span()[1]+1:])
            boxes[box] = add_lens(boxes[box], label, f)
        else:
            print("operation failed to be identified")
    print(boxes)
    print(f"part 2: focusing power: {focusing_power(boxes)}")


main()
# part 2, 106988 too low
