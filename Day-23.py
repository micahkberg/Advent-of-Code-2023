def load(day):
    contents = open(f"./inputs/{day}.txt", "r").read().strip().split("\n")
    return contents


def make_map(lines):
    trail_map = dict()
    dirs = [(0, 1), (1, 0), (-1, 0), (0, -1)]
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            char = lines[y][x]
            if char in ".<>v^":
                trail_map[(x, y)] = []
                for d in dirs:
                    neighbor = (x+d[0], y+d[1])
                    if neighbor[0] in range(len(lines[0])) and neighbor[1] in range(len(lines)):
                        if lines[neighbor[1]][neighbor[0]] in ".<>v^":
                            trail_map[(x, y)].append(neighbor)
    return trail_map


def print_path(full_paths, path):
    for y in range(len(full_paths)):
        line = ""
        for x in range(len(full_paths[0])):
            if (x,y) in path:
                line += "0"
            else:
                line += full_paths[y][x]
        print(line)


def possible_to_finish(trail_map, path):
    sub_paths = [path]
    while len(sub_paths)>0:
        sub_paths.sort(key=lambda x: sum(x[-1]), reverse=True)
        cur_path = sub_paths.pop(0)
        cur_tile_coord = cur_path[-1]
        new_sub_path = cur_path.copy()
        for neighbor in trail_map[cur_tile_coord]:
            if neighbor == (139, 140):
                return True
            if neighbor not in new_sub_path:
                new_sub_path.append(neighbor)
        sub_paths.append(new_sub_path)
    return False


def find_paths(full_paths, trail_map, slippery=True):
    dir_map = {"<": (-1,0), ">": (1,0), "v": (0,1), "^": (0,-1)}
    start_coord = (1, 0)
    end_coord = (139, 140)
    paths = [[start_coord]]
    complete_paths = []
    while len(paths) > 0:
        cur_path = paths.pop(0)
        if complete_paths:
            if not possible_to_finish(trail_map, cur_path):
                continue
        cur_tile_coord = cur_path[-1]
        if cur_tile_coord == end_coord:
            complete_paths.append(cur_path)
            print('complete paths:')
            print(len(complete_paths))
            print('paths to test:')
            print(len(paths))
            #print_path(full_paths, cur_path)
            continue
        for neighbor in trail_map[cur_tile_coord]:
            new_path = cur_path.copy()
            if neighbor not in new_path:
                new_path.append(neighbor)
                if full_paths[neighbor[1]][neighbor[0]] in "<>v^" and slippery:
                    slide_dir = dir_map[full_paths[neighbor[1]][neighbor[0]]]
                    slide_to = (slide_dir[0]+neighbor[0], slide_dir[1]+neighbor[1])
                    if slide_to not in new_path:
                        new_path.append(slide_to)
                        paths.append(new_path)
                else:
                    paths.append(new_path)
    return complete_paths


def main_pt1():
    full_paths = load("23")
    trail_map = make_map(full_paths)

    # part 1
    paths = find_paths(full_paths, trail_map)
    print(len(paths))
    print(max(list(map(lambda i: len(i), paths)))-1)


def main_pt2():
    full_paths = load('23')
    trail_map = make_map(full_paths)

    # Classes for algorithm
    class Vertex:
        def __init__(self, coord):
            self.coord = coord
            self.edges = []

        def neighbors(self):
            ns = []
            for edge in self.edges:
                for v in edge.vs:
                    if v.coord != self.coord:
                        ns.append(v)
            return ns

        def is_done(self, coord):
            for edge in self.edges:
                if coord in edge.path:
                    return True
            return False

        def __str__(self):
            output = f"coord: {self.coord}:\n"
            for edge in self.edges:
                output += str(edge) + "\n"
            return output

    class Edge:
        def __init__(self, path, v1, v2):
            self.path = path
            self.vs = [v1, v2]

        def length(self):
            return len(self.path)-1

        def __str__(self):
            output = f"{self.vs[0].coord}<--{self.length()}-->{self.vs[1].coord}"
            return output

    # Generate our shortened edge concept
    start_vertex = Vertex((1,0))
    end_vertex = Vertex((139, 140))

    vertices = {start_vertex.coord: start_vertex,
                end_vertex.coord: end_vertex}
    vertices_to_do = [start_vertex]
    while vertices_to_do:
        cur_vertex = vertices_to_do.pop(0)
        edge_stems = [[cur_vertex.coord, x] for x in trail_map[cur_vertex.coord]]
        for stem in edge_stems:
            if not cur_vertex.is_done(stem[-1]):
                while True:
                    if len(trail_map[stem[-1]]) != 2:
                        break
                    for neighbor in trail_map[stem[-1]]:
                        if neighbor not in stem:
                            stem.append(neighbor)
                if stem[-1] not in vertices:
                    connected_v = Vertex(stem[-1])
                    vertices[connected_v.coord] = connected_v
                    vertices_to_do.append(connected_v)
                else:
                    connected_v = vertices[stem[-1]]
                new_edge = Edge(stem, cur_vertex, connected_v)
                cur_vertex.edges.append(new_edge)
                connected_v.edges.append(new_edge)
    combos_naive = 1
    for v in vertices:
        combos_naive *= len(vertices[v].edges)
        print(vertices[v])
    print(f"number of vertices = {len(vertices)}")
    print(f"max number of paths: {combos_naive}")

    paths_to_do = [[start_vertex]]
    max_len = 0
    count = 0

    def path_length(path):
        l = 0
        for i in range(len(path)-1):
            v1 = path[i]
            v2 = path[i+1]
            for edge in v1.edges:
                if v1.coord in edge.path and v2.coord in edge.path:
                    l += edge.length()
                    break
        return l

    while paths_to_do:
        current_path = paths_to_do.pop(-1)
        count += 1
        if count % 100000==0:
            print(f"try: {count}, cur_max {max_len}")
        if current_path[-1].coord == end_vertex.coord:
            new_len = path_length(current_path)
            if path_length(current_path) > max_len:
                max_len = new_len
            continue
        for neighbor in current_path[-1].neighbors():
            if neighbor not in current_path:
                new_path = current_path + [neighbor]
                paths_to_do.append(new_path)
    print('going to find max len')

    print(max_len)

main_pt2()
