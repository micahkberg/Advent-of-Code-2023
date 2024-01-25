

def load(day):
    contents = open(f"./inputs/{day}.txt", "r").read().strip().split("\n")
    return contents


contents = load("05")


class TransformMap:
    def __init__(self, from_type, to_type):
        self.mappers = []
        self.from_type = from_type
        self.to_type = to_type

    def check_value(self, range_to_transform):
        rtt = range(range_to_transform[0], range_to_transform[0] + range_to_transform[1])
        rtt_init = rtt[0]
        rtt_last = rtt[-1]
        all_ranges = 0
        for mapper in self.mappers:
            new_ranges = mapper.check_value(rtt)
            for r in new_ranges:
                if len(r)>0:
                    all_ranges.append(r)

        return all_ranges

    def try_transform(self, list_of_ranges):
        next_list_of_ranges = []
        for r in list_of_ranges:
            next_list_of_ranges += self.check_value(r)
        if self.to_type == "location":
            return next_list_of_ranges
        else:
            return maps[self.to_type].try_transform(next_list_of_ranges)


class Mapper:
    def __init__(self, di, si, r):
        self.di = int(di)
        self.si = int(si)
        self.r = int(r)
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
    for i in range(len(seed_numbers[0::2])):
        seed_ranges.append([seed_numbers[i], seed_numbers[i+1]])

    location_ranges = maps["seed"].try_transform(seed_ranges)
    location_low = None
    for r in location_ranges:
        if not location_low or r[0] < location_low:
            location_low = r[0]
    print(location_low)


find_lowest_location_from_seed_ranges()
