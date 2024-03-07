def load(day):
    contents = open(f"./inputs/{day}.txt", "r").read().strip().split("\n")
    return contents


GLOBAL_LOW_PULSES = 0
GLOBAL_HIGH_PULSES = 0


class Module:
    def __init__(self, name, destinations):
        self.destinations = destinations
        self.inputs = dict()
        self.name = name

    def send_low_pulse(self, modules):
        global GLOBAL_LOW_PULSES
        next_pulses = []
        for destination in self.destinations:
            GLOBAL_LOW_PULSES += 1
            next_pulses += [modules[destination].pulse(False, self.name)]
        return next_pulses

    def send_high_pulse(self, modules):
        global GLOBAL_HIGH_PULSES
        next_pulses = []
        for destination in self.destinations:
            GLOBAL_HIGH_PULSES += 1
            next_pulses.append(modules[destination].pulse(True, self.name))
        return next_pulses

    def pulse(self, pulse, name):
        if not len(self.destinations):
            return None
        else:
            return AssertionError


class FlipFlop(Module):
    def __init__(self, name, destinations):
        Module.__init__(self, name, destinations)
        self.state = False

    def pulse(self, pulse, name):
        if pulse:
            return None
        elif self.state:
            self.state = False
            return self.send_low_pulse
        elif not self.state:
            self.state = True
            return self.send_high_pulse


class Conjunction(Module):
    def __init__(self, name, destinations):
        Module.__init__(self, name, destinations)
        self.last_pulse = dict()

    def pulse(self, pulse, name):
        self.last_pulse[name] = pulse
        if False in self.last_pulse.values():
            return self.send_high_pulse
        else:
            return self.send_low_pulse


class Broadcast(Module):
    def __init__(self, name, destinations):
        Module.__init__(self, name, destinations)

    def pulse(self, pulse, name):
        if pulse:
            return self.send_high_pulse
        else:
            return self.send_low_pulse


class Button(Module):
    def __init__(self, name, destinations):
        Module.__init__(self, name, destinations)
        self.destinations = ["broadcast"]

    def press(self):
        return self.send_low_pulse


def generate_modules():
    raw_data = load("20")
    modules = dict()
    modules["button"] = Button("button", None)
    for line in raw_data:
        module_info = line.split()[0]
        submodules = line.split(" -> ")[1].split(", ")
        if "%" in module_info:
            name = module_info.strip("%")
            modules[name] = FlipFlop(name, submodules)
        elif "&" in module_info:
            name = module_info.strip("&")
            modules[name] = Conjunction(name, submodules)
        else:
            name = "broadcast"
            modules[name] = Broadcast(name, submodules)
    initial_modules = list(modules.values())
    for module in initial_modules:
        for destination in module.destinations:
            if destination not in modules.keys():
                modules[destination] = Module(destination, [])
            modules[destination].inputs[module.name] = False
    return modules


def main():
    modules = generate_modules()
    for _ in range(1000):
        pulses = [modules["button"].press()]
        while len(pulses) > 0:
            #print(pulses)
            next_pulse = pulses.pop(0)
            if next_pulse:
                pulses += next_pulse(modules)
    print(GLOBAL_LOW_PULSES)
    print(GLOBAL_HIGH_PULSES)
    print(GLOBAL_LOW_PULSES*GLOBAL_HIGH_PULSES)


main()
