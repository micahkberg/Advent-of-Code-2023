import itertools

def load(day):
    contents = open(f"./inputs/{day}.txt", "r").read().strip().split("\n")
    return contents


solutions = dict()


class Springs:
    def __init__(self, springs, log_tuple):
        self.springs = springs
        self.log_tuple = log_tuple

    def quintuplate(self):
        # lengthens the string per part 2
        s = self.springs
        self.springs = s + "?" + s + "?" + s + "?" + s + "?" + s
        self.log_tuple = self.log_tuple * 5
        self.springs = self.springs.strip(".")

    def finished(self):
        # checks if remaining segments actually add up to finish the tuple segments already
        return convert_to_tuple(self.springs) == self.log_tuple

    def possible(self):
        # check some basic arithmetic to determine if the tuple can still
        # work out onto the remaining real spring segment, other possible cases could be
        # evaluated for determining viability
        if self.springs.count("#") + self.springs.count("?") < sum(self.log_tuple):
            # the remaining hashes and q's aren't enough to complete the tuple log
            return False
        elif len(self.springs) < sum(self.log_tuple) - 1 + len(self.log_tuple):
            # length of the remaining spring string doesnt fit the minimum required size of the
            # log tuple
            return False
        elif not self.log_tuple and convert_to_tuple(self.springs):
            # if our log is empty, and our string isn't, then that doesnt work
            return False
        elif self.springs:
            # not checking the second fact unless first is true to avoid index issues
            if self.springs[0] == "#" and self.log_tuple[0] < convert_to_tuple(self.springs)[0]:
                # if we have a spring section that begins our string, and it is longer than our first number,
                # then no amount of adding springs fixes that situation
                return False
        return True

    def clean_up_end(self):
        if self.finished():
            return
        last_length = self.log_tuple[-1]
        self.springs = self.springs.strip(".")
        if self.springs.endswith("#"*last_length):
            self.springs = self.springs[:-last_length]
            self.log_tuple = self.log_tuple[:-1]
            self.clean_up_end()
        elif self.springs.endswith("#"*last_length + "?"):
            self.springs = self.springs[:-1-last_length]
            self.log_tuple = self.log_tuple[:-1]
            self.clean_up_end()

    def keyname(self):
        return self.springs + str(self.log_tuple)


def read_logs():
    contents = load("12")
    logs = []
    for line in contents:
        new_springs, log_tuple = line.split()
        log_tuple = tuple(map(int, log_tuple.split(",")))
        logs.append(Springs(new_springs, log_tuple))
    return logs


def convert_to_tuple(spring_list):
    output = []
    count = None
    for char in spring_list:
        if char == "#":
            if not count:
                count = 1
            else:
                count += 1
        elif char in ".?" and count:
            output.append(count)
            count = None
    if count:
        output.append(count)
    return tuple(output)


def remake_str(old_str, repl_tupl):
    # for part 1, places ther iter object into the spring string area
    new_str = ""
    j = 0
    for char in old_str:
        if char == "?":
            if repl_tupl[j]:
                new_str += "#"
            else:
                new_str += "."
            j += 1
        else:
            new_str += char
    return new_str


def brute_force_solve(springs):
    solutions = 0
    qs = springs.springs.count("?")
    arrs = itertools.product(range(2), repeat=qs)
    for arr in arrs:
        test_str = remake_str(springs.springs, arr)
        if convert_to_tuple(test_str) == springs.log_tuple:
            solutions += 1
    return solutions


def placement_compatible(original_spring, new_spring):
    if len(original_spring) != len(new_spring):
        Exception('spring lengths didnt match')
        return False
    else:
        for i in range(len(original_spring)):
            if original_spring[i] != new_spring[i] and original_spring[i] != "?":
                return False
    return True


def tuple_compatible(log_tuple, spring_string):
    new_tuple = convert_to_tuple(spring_string)
    return log_tuple[0] == new_tuple[0]


def find_placements(spr: Springs):
    if not spr.possible():
        return 0
    #spr.clean_up_end()
    if spr.finished():
        return 1
    if spr.keyname() in solutions.keys():
        return solutions[spr.keyname()]
    next_length = spr.log_tuple[0]
    number_of_subarrangements = 0
    if "#" in spr.springs:
        first_spring = spr.springs.find("#")
    else:
        first_spring = len(spr.springs)
    search_end = min(first_spring+1, len(spr.springs)-next_length+1)
    for i in range(search_end):
        remainder_str = spr.springs[i+next_length:]
        test_str = spr.springs[0:i] + "#"*next_length + remainder_str
        if placement_compatible(spr.springs, test_str):
            if tuple_compatible(spr.log_tuple, test_str):
                sub_springs = Springs(remainder_str[1:], spr.log_tuple[1:])
                number_of_subarrangements += find_placements(sub_springs)
    solutions[spr.keyname()] = number_of_subarrangements
    return number_of_subarrangements


def main():
    spring_logs = read_logs()
    solutions_total = 0
    for springs in spring_logs:
        print(f"{springs.springs}    {springs.log_tuple}")
        solutions_total += brute_force_solve(springs)
        print(solutions_total)


def mainpt2():
    spring_logs = read_logs()
    for spring in spring_logs:
        spring.quintuplate()

    solutions_total = 0
    j = 1
    for springs in spring_logs:
        print(f"{j} / {len(spring_logs)}    {springs.springs}    {springs.log_tuple}")
        number_of_new_solutions = find_placements(springs)
        solutions_total += number_of_new_solutions
        print(f"{number_of_new_solutions}/{solutions_total}")
        j += 1
    print(solutions_total)

mainpt2()


# part1 7409 too low
