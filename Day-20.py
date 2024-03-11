import numpy as np

def load(day):
    contents = open(f"./inputs/{day}.txt", "r").read().strip().split("\n")
    return contents


GLOBAL_LOW_PULSES = 0
GLOBAL_HIGH_PULSES = 0
GLOBAL_LCM_DICT = {'bm': None, 'cl': None, 'tn': None, 'dr': None}
GLOBAL_BUTTON_PRESSES = 0


class Module:
    def __init__(self, name, destinations):
        self.destinations = destinations
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
        if self.name == 'rx' and not pulse:
            return "reached_rx_low_pulse"
        elif self.name == 'rx':
            return None
        elif not len(self.destinations):
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
        else:
            self.state = not self.state
            if self.state:
                return self.send_high_pulse
            else:
                return self.send_low_pulse


class Conjunction(Module):
    def __init__(self, name, destinations):
        Module.__init__(self, name, destinations)
        self.last_pulse = dict()

    def pulse(self, pulse, name):
        global GLOBAL_BUTTON_PRESSES
        self.last_pulse[name] = pulse
        if self.name == "vr":
            pass
        if False in self.last_pulse.values():
            if self.name in ["bm", "cl", "tn", "dr"]:
                if not GLOBAL_LCM_DICT[self.name]:
                    GLOBAL_LCM_DICT[self.name] = GLOBAL_BUTTON_PRESSES
                print(f"{self.name}: press {GLOBAL_BUTTON_PRESSES}")
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
            elif type(modules[destination]) == Conjunction:
                modules[destination].last_pulse[module.name] = False
    return modules


def main():
    global GLOBAL_BUTTON_PRESSES
    modules = generate_modules()
    while True:
        GLOBAL_BUTTON_PRESSES += 1
        pulses = [modules["button"].press()]
        while len(pulses) > 0:
            next_pulse = pulses.pop(0)
            if next_pulse == "reached_rx_low_pulse":
                print(f"rx low pulse reached with {GLOBAL_BUTTON_PRESSES} presses")
                break
            if next_pulse:
                pulses += next_pulse(modules)
        if next_pulse == "reached_rx_low_pulse" or None not in GLOBAL_LCM_DICT.values():
            #print(lcm(list(GLOBAL_LCM_DICT.values())))
            values = list(GLOBAL_LCM_DICT.values())
            print('pt 2 product of primes')
            print(values[0]*values[1]*values[2]*values[3])
            break

        if GLOBAL_BUTTON_PRESSES == 1000:
            print(f"low pulses: {GLOBAL_LOW_PULSES}")
            print(f"high pulses: {GLOBAL_HIGH_PULSES}")
            print(f"product: {GLOBAL_LOW_PULSES*GLOBAL_HIGH_PULSES}")



main()

# pt2 73076219, too low
