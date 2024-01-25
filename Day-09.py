def load(day):
    contents = open(f"./inputs/{day}.txt", "r").read().strip().split("\n")
    return contents


class Sequence:
    def __init__(self, l):
        self.numbers = l

    def get_next_num(self):
        if self.is_zeroes():
            return 0
        else:
            return self.numbers[-1]+self.get_subsequence().get_next_num()

    def get_prev_num(self):
        if self.is_zeroes():
            return 0
        else:
            return self.numbers[0]-self.get_subsequence().get_prev_num()

    def is_zeroes(self):
        return set(self.numbers) == {0}

    def get_subsequence(self):
        sub_sequence_numbers = []
        for i in range(len(self.numbers)-1):
            sub_sequence_numbers.append(self.numbers[i+1]-self.numbers[i])
        return Sequence(sub_sequence_numbers)


def main():
    sequences = []
    for content in load("09"):
        numbers = content.split()
        numbers = list(map(int, numbers))
        sequences.append(Sequence(numbers))

    next_nums_total = 0
    for sequence in sequences:
        next_nums_total += sequence.get_next_num()
    print(next_nums_total)

    prev_nums_total = 0
    for sequence in sequences:
        prev_nums_total += sequence.get_prev_num()
    print(prev_nums_total)
    # part2 try 1 19402 too high, whoops was supposed to be subtracting
    # 1140

main()

