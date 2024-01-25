

def load(day):
    contents = open(f"./inputs/{day}.txt", "r").read().strip().split("\n")
    return contents


contents = load("05")


class TransformMap:
    def __init__(self, from_type, to_type):
        self.mappers = []
        self.from_type = from_type
        self.to_type = to_type

    def transform(self, range_to_transform):
        all_ranges = []
        for mapper in self.mappers:
            new_ranges = mapper.check_value(range_to_transform)
            for r in new_ranges:
                if len(r)>0:
                    all_ranges.append(r)

        return all_ranges


class Mapper:
    def __init__(self, di, si, r):
        self.di = di
        self.si = si
        self.r = r
        self.input_range = range(si, si+r)
        self.offset = self.di-self.si

    def check_value(self, rtt):
        nums_below = range(rtt[0], min(rtt[-1]+1, self.si))
        nums_above = range(max(self.si+self.r, rtt[0]+1), rtt[-1]+1)
        overlap = range(max(rtt[0], self.si)+self.offset,
                        min(rtt[-1]+1, self.si+self.r)+self.offset)
        unmoved = [nums_above, nums_below]
        return unmoved, overlap

# parts input file
maps = dict()
for content in contents:
    if content.startswith("seeds:"):
        seed_numbers = list(map(int, content.split(" ")[1:]))
    else:
        if content and "map" in content:
            k, v = content.split(" ")[0].split("-")[0::2]
            maps[k]  = TransformMap(k, v)
        elif content:
            d_start, s_start, range_len = content.split(" ")
            maps[k].mappers.append(Mapper(d_start, s_start, range_len))


def find_lowest_location_from_seed_ranges():
    seed_ranges = []
    for i in range(len(seed_numbers))[0::2]:
        seed_ranges.append(range(seed_numbers[i], seed_numbers[i]+seed_numbers[i+1]))
    current_category = "seed"
    while current_category != "location":
        new_ranges = []
        for r in seed_ranges:
            new_ranges += maps[current_category].transform(r)
        seed_ranges = new_ranges
        current_category = maps[current_category].to_type
    lowest_location = None
    for r in seed_ranges:
        if (lowest_location and lowest_location>r[0]) or not lowest_location:
            lowest_location = r[0]
    print(lowest_location)


find_lowest_location_from_seed_ranges()
