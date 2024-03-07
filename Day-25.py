import itertools


def load(day):
    contents = open(f"./inputs/{day}.txt", "r").read().strip().split("\n")
    return contents


def get_wire_structure():
    lines = load("25")
    components = {}
    total_connections = 0
    for line in lines:
        parts = line.split(": ")
        component = parts[0]
        connections = parts[1].split(" ")
        if component not in components:
            components[component] = set()
        for connection in connections:
            total_connections += 1
            if connection not in components:
                components[connection] = set()
            components[connection].add(component)
            components[component].add(connection)
    print(f"total connections: {total_connections}")
    return components


def get_group_count(component_map):
    groups = 0
    items_to_sort = list(component_map.keys())
    while items_to_sort:
        groups += 1
        exploring_from = [items_to_sort.pop(0)]
        while exploring_from:
            cur_point = exploring_from.pop(0)
            for neighbor in component_map[cur_point]:
                if neighbor in items_to_sort:
                    items_to_sort.remove(neighbor)
                    exploring_from.append(neighbor)
    return groups


def get_group_product(component_map):
    groups = []
    items_to_sort = list(component_map.keys())
    while items_to_sort:
        exploring_from = [items_to_sort.pop(0)]
        new_group = exploring_from.copy()
        while exploring_from:
            cur_point = exploring_from.pop(0)
            for neighbor in component_map[cur_point]:
                if neighbor in items_to_sort:
                    items_to_sort.remove(neighbor)
                    exploring_from.append(neighbor)
                    new_group.append(neighbor)
        groups.append(new_group)
    product = 1
    for group in groups:
        product *= len(group)
    return product


def main():
    components = get_wire_structure()

    count4 = 0
    for component in components:
        if len(components[component])==4:
            count4 += 1

main()

