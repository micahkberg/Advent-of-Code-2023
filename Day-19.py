import re


def load(day):
    contents = open(f"./inputs/{day}.txt", "r").read().strip().split("\n")
    return contents


class ToolRange:
    def __init__(self):
        self.values = {"x": None, "m": None, "a": None, "s": None}

    def __str__(self):
        return str(self.values)

    def __repr__(self):
        return str(self.values)

    def combinations(self):
        return len(self.values["x"])*len(self.values["m"])*len(self.values["a"])*len(self.values["s"])


class Tool:
    def __init__(self, xmas):
        nums = []
        next_num = ""
        for char in xmas:
            if char in "1234567890":
                next_num += char
            elif next_num:
                nums.append(int(next_num))
                next_num = ""
        self.values = {"x": nums[0], "m": nums[1], "a": nums[2], "s": nums[3]}
        self.rating = sum(self.values.values())


class Rule:
    def __init__(self, rule_text):
        self.name = rule_text[:rule_text.find("{")]
        self.sub_rules = rule_text[rule_text.find("{")+1:-1].split(",")

    def __repr__(self):
        return f"{self.name}: {self.sub_rules}"

    def sort(self, tool, rules):
        for sub_rule in self.sub_rules:
            if ">" in sub_rule:
                quality, value, destination = re.split(">|:", sub_rule)
                if tool.values[quality] > int(value):
                    return rules[destination].sort(tool, rules)
            elif "<" in sub_rule:
                quality, value, destination = re.split("<|:", sub_rule)
                if tool.values[quality] < int(value):
                    return rules[destination].sort(tool, rules)
            else:
                return rules[sub_rule].sort(tool, rules)

    def get_subranges(self, tool_range, rules):
        subranges = []
        for sub_rule in self.sub_rules:
            if ">" in sub_rule:
                quality, value, destination = re.split(">|:", sub_rule)
                value = int(value)
                minval = min(tool_range.values[quality])
                maxval = max(tool_range.values[quality])
                if maxval > value:
                    match_range = ToolRange()
                    match_range.values = tool_range.values.copy()
                    match_range.values[quality] = range(max(value+1, minval), maxval + 1)
                    tool_range.values[quality] = range(minval, max(minval, value+1))
                    subranges.append(rules[destination].get_subranges(match_range, rules))
            elif "<" in sub_rule:
                quality, value, destination = re.split("<|:", sub_rule)
                value = int(value)
                minval = min(tool_range.values[quality])
                maxval = max(tool_range.values[quality])
                if minval < value:
                    match_range = ToolRange()
                    match_range.values = tool_range.values.copy()
                    tool_range.values[quality] = range(min(maxval, value), maxval + 1)
                    match_range.values[quality] = range(minval, min(value, maxval))
                    subranges.append(rules[destination].get_subranges(match_range, rules))
            else:
                subranges.append(rules[sub_rule].get_subranges(tool_range, rules))
        return subranges



class Reject:
    def __init__(self):
        self.name = "R"

    def sort(self, tool, rules):
        return 0

    def get_subranges(self, ranges, rules):
        return []


class Accept:
    def __init__(self):
        self.name = "A"

    def sort(self, tool, rules):
        return tool.rating

    def get_subranges(self, ranges, rules):
        return ranges


def read_tools_and_rules():
    raw = load("19")
    rules = {"A": Accept(), "R": Reject()}
    tools = []
    for line in raw:
        if line.startswith("{"):
            new_tool = Tool(line)
            tools.append(new_tool)
        elif line:
            new_rule = Rule(line)
            rules[new_rule.name] = new_rule
    return tools, rules


def main():
    tools, rules = read_tools_and_rules()
    total_accepted_rating = 0
    for tool in tools:
        total_accepted_rating += rules["in"].sort(tool, rules)
    print("initial pile of tools...")
    print(total_accepted_rating)

    # part 2

    initial_range = ToolRange()
    initial_range.values["x"] = range(1, 4001)
    initial_range.values["m"] = range(1, 4001)
    initial_range.values["a"] = range(1, 4001)
    initial_range.values["s"] = range(1, 4001)
    ranges = rules["in"].get_subranges(initial_range, rules)
    total_combos = 0

    def get_total(some_ranges):
        total = 0
        if type(some_ranges) == list:
            for i in some_ranges:
                total += get_total(i)
        else:
            total += some_ranges.combinations()
        return total


    print("total number of possible tools")
    print(get_total(ranges))


main()
