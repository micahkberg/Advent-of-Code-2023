# Day 1 of Advent of Code 2023!
def load(day):
    contents = open(f"./inputs/{day}.txt", "r").read().strip().split("\n")

    return contents

import re


day = "01"


def get_cal_value(line):
    digits = ""
    for char in line:
        try:
            a = int(char)
            digits += char
        except:
            pass
    return int(digits[0]+digits[-1])


def get_cal_value_advanced(line):
    digits = 0
    spelling_dict = {"one": 1,
                     "two": 2,
                     "three": 3,
                     "four": 4,
                     "five": 5,
                     "six": 6,
                     "seven": 7,
                     "eight": 8,
                     "nine": 9}
    spelled_nums = "|".join(spelling_dict.keys())
    all_digits = re.findall(f"(?=([1-9]|{spelled_nums}))", line)
    first_digit = all_digits[0]
    last_digit = all_digits[-1]
    if first_digit in spelling_dict.keys():
        digits += spelling_dict[first_digit]*10
    else:
        digits += int(first_digit)*10
    if last_digit in spelling_dict.keys():
        digits += spelling_dict[last_digit]
    else:
        digits += int(last_digit)
    print(f"{line},{first_digit},{last_digit}, {digits}")
    return digits


def part1():
    total = 0
    for line in load(day):
        total += get_cal_value(line)
    print(total)


def part2():
    total = 0
    for line in load("01"):
        total += get_cal_value_advanced(line)
    print(total)


def part2_test():
    total = 0
    for line in "two1nine\neightwothree\nabcone2threexyz\nxtwone3four\n4nineeightseven2\nzoneight234\n7pqrstsixteen".split("\n"):
        total += get_cal_value_advanced(line)
    print(total)

part1()
part2()
