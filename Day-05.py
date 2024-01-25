

def load(day):
    contents = open(f"./inputs/{day}.txt", "r").read().strip().split("\n")
    return contents


contents = load("05")


class TransformMap:
    def __init__(self, from_type, to_type):
        self.mappers = []
        self.from_type = from_type
        self.to_type = to_type

    def check_value(self, value):
        return_value = False
        for mapper in self.mappers:
            new_value = mapper.check_value(value)
            if new_value != value:
                if return_value and new_value<return_value:
                    return_value = new_value
                elif not return_value:
                    return_value = new_value
        if return_value:
            return return_value
        else:
            return value

    def try_transform(self, value):
        if self.to_type == "location":
            return self.check_value(value)
        else:
            return maps[self.to_type].try_transform(self.check_value(value))


class Mapper:
    def __init__(self, di, si, r):
        self.di = int(di)
        self.si = int(si)
        self.r = int(r)

    def check_value(self, value):
        if value in range(self.si, self.si + self.r):
            return self.di+value-self.si
        else:
            return value


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


def find_lowest_location_for_all_seeds():
    location_low = None
    for seed in seed_numbers:
        location = maps["seed"].try_transform(seed)
        if (location_low and location < location_low) or not location_low:
            location_low = location
    print(location_low)

find_lowest_location_for_all_seeds()
