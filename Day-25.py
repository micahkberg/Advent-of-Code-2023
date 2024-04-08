import itertools
from pyvis.network import Network

def load(day):
    contents = open(f"./inputs/{day}.txt", "r").read().strip().split("\n")
    return contents

def get_wire_structure():
    lines = load("25")
    components = {}
    all_connections = []
    total_connections = 0
    for line in lines:
        parts = line.split(": ")
        component = parts[0]
        connections = parts[1].split(" ")
        if component not in components:
            components[component] = set()
        for connection in connections:
            all_connections.append([component, connection])
            total_connections += 1
            if connection not in components:
                components[connection] = set()
            components[connection].add(component)
            components[component].add(connection)
    print(f"total connections: {total_connections}")
    return components, all_connections


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


def extra_paths_between(a, b, component_map):
    count = 0
    a_neighbors = list(component_map[a])
    a_neighbors.remove(b)
    for n in a_neighbors:
        seen = [a]
        to_do = [n]
        while to_do:
            next_neighbors = component_map[to_do.pop(-1)]
            for next_neighbor in next_neighbors:
                if next_neighbor not in seen:
                    seen.append(next_neighbor)
                    to_do.append(next_neighbor)
            if b in to_do:
                count+=1
                break
    return count


def main():
    components_map, connections = get_wire_structure()
    test_net = Network('500px', '500px')
    for node in components_map.keys():
        test_net.add_node(node,title=node)
    for connection in connections:
        test_net.add_edge(connection[0], connection[1])
    test_net.show('components.html', notebook=False)

    # visual inspection results;
    # 'crg'-'krf'
    # 'fmr'-zhg'
    # 'rgv'-'jct'

    # manual solution:
    components_map['crg'].remove('krf')
    components_map['krf'].remove('crg')
    components_map['fmr'].remove('zhg')
    components_map['zhg'].remove('fmr')
    components_map['rgv'].remove('jct')
    components_map['jct'].remove('rgv')

    print(get_group_product(components_map))

    components = set(components_map.keys())
    # lets try to find the edge by slowly adding points to a group
    starting_point = components.pop()
    group_a = {starting_point}
    seen = set()
    to_do = {starting_point}
    while to_do:
        m = to_do.pop()
        seen.add(m)
        for n in components_map[m]:
            if n not in seen:
                if extra_paths_between(m, n, components_map) >= 3:
                    group_a.add(n)
                    to_do.add(n)
        break
    print(group_a)

main()

