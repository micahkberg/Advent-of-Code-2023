def load(day):
    contents = open(f"./inputs/{day}.txt", "r").read().strip().split("\n")
    return contents


lines = load("05")


class TransformMap:
    def __init__(self, from_type, to_type):
        self.mappers = []
        self.from_type = from_type
        self.to_type = to_type

    def transform(self, ranges_to_transform):
        remaining = ranges_to_transform
        all_ranges = []
        print(f'maps to apply {len(self.mappers)}')
        step_num = 1
        for mapper in self.mappers:
            print(f"starting map {step_num} of {len(self.mappers)}, remaining ranges {len(remaining)}")
            transformed, remaining = mapper.check_value(remaining)
            print(transformed)
            print(remaining)
            all_ranges += transformed
            step_num += 1
        return all_ranges+remaining


class Mapper:
    def __init__(self, di, si, r):
        self.destination_initial = di
        self.source_initial = si
        self.range_length = r
        self.source_end = si + r - 1
        self.offset = di - si

    def check_value(self, rtt):
        if type(rtt) == list:
            transformed, untransformed = [], []
            for r in rtt:
                t, u = self.check_value(r)
                transformed += t
                untransformed += u
        else:
            if rtt.end < self.source_initial or rtt.start > self.source_end:
                return [], [rtt]
            nums_below = SeedRange(rtt.start, min(rtt.end, self.source_initial-1))
            nums_above = SeedRange(max(self.source_end+1, rtt.start), rtt.end)
            overlap = SeedRange(max(self.source_initial, rtt.start)+self.offset,
                                min(self.source_end, rtt.end)+self.offset)
            untransformed = []
            transformed = []
            if nums_above.is_valid():
                untransformed.append(nums_above)
            if nums_below.is_valid():
                untransformed.append(nums_below)
            if overlap.is_valid():
                transformed.append(overlap)
        return transformed, untransformed


class SeedRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __repr__(self):
        return str(f"{self.start} -> {self.end}")

    def is_valid(self):
        return self.end - self.start > 0

    def min(self):
        return self.start

    def length(self):
        return self.end - self.start


def read_seed_ranges():
    seed_data = list(map(int, lines[0].split(" ")[1:]))
    seed_ranges = []
    for i in range(0, len(seed_data), 2):
        seed_ranges.append(SeedRange(seed_data[i], seed_data[i]+seed_data[i+1]-1))
    return seed_ranges


def read_transformations():
    maps = dict()
    for line in lines:
        if line.startswith("seeds"):
            pass
        elif "map" in line:
            k, v = line.split(" ")[0].split("-")[0::2]
            maps[k] = TransformMap(k, v)
        elif line:
            d_start, s_start, range_len = list(map(int, line.split(" ")))
            maps[k].mappers.append(Mapper(d_start, s_start, range_len))
    return maps


def find_lowest_location_from_seed_ranges():
    seed_ranges = read_seed_ranges()
    print(f"Seeds initialized, number of ranges: {len(seed_ranges)}")
    maps = read_transformations()
    print(f"Transformations initialized, number of transformation steps: {len(maps)}")
    step_num = 1
    for transformation in maps.values():
        print(f"Starting step: {step_num} of {len(maps)}")
        seed_ranges = transformation.transform(seed_ranges)
        step_num += 1
        print(f"current number of ranges: {len(seed_ranges)}")
    print(f"lowest val")
    print(min(list(map(lambda i: i.min(), seed_ranges))))


find_lowest_location_from_seed_ranges()

#pt 2 77864447 too high
