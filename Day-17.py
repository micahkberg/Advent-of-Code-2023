def load(day):
    contents = open(f"./inputs/{day}.txt", "r").read().strip().split("\n")
    return contents


heat_loss_map = load("17")


def print_best_path_so_far(cost_map):
    for y in range(goal_y + 1):
        row = []
        for x in range(goal_x+1):
            if (x, y) in cost_map.keys():
                row.append(str(cost_map[(x,y)]).rjust(4, "-"))
            else:
                row.append("----")
        print(row)


goal_x = len(heat_loss_map[0])-1
goal_y = len(heat_loss_map)-1
max_cost = ((goal_x * 9) + (goal_y * 9))*2


class Node:
    def __init__(self, x, y, velocity):
        self.x = int(x)
        self.y = int(y)
        self.coords = (self.x, self.y)
        self.heat = int(heat_loss_map[self.y][self.x])
        self.velocity = velocity

    def get_closeness_to_end(self):
        return (goal_x-self.x)+(goal_y-self.y)

    def get_tile_evaluation(self, cost_guide):
        return max(self.velocity)*-1, cost_guide[self], self.heat, self.get_closeness_to_end()

    def __eq__(self, other_node):
        return self.x == other_node.x and self.y == other_node.y and self.velocity == other_node.velocity

    def __hash__(self):
        return hash((self.x, self.y, tuple(self.velocity)))

    def __repr__(self):
        return f"Node: ({self.x}, {self.y}), velocity: {self.velocity}"

    def get_connected_nodes(self):
        if self.x == goal_x and self.y == goal_y:
            return None
        potential_dirs = []
        u_vector = [self.velocity[0]/abs(sum(self.velocity)), self.velocity[1]/abs(sum(self.velocity))]
        if sum(self.velocity) < 3:
            potential_dirs.append(u_vector)
        potential_dirs.append([u_vector[1], u_vector[0]*-1])
        potential_dirs.append([u_vector[1]*-1, u_vector[0]])
        new_nodes = []
        for direction in potential_dirs:
            new_x = self.x + direction[0]
            new_y = self.y + direction[1]
            if new_x in range(goal_x+1) and new_y in range(goal_y+1):
                if direction == u_vector:
                    new_vector = [self.velocity[0]+u_vector[0], self.velocity[1]+u_vector[1]]
                else:
                    new_vector = direction

                new_node = Node(new_x, new_y, new_vector)
                new_nodes.append(new_node)
        return new_nodes


def find_path():
    nodes_to_test = [Node(0, 0, [1, 0]), Node(0, 0, [0, 1])]
    end_nodes = []
    for x_velocity in range(1,4):
        end_nodes.append(Node(goal_x, goal_y, [x_velocity, 0]))
    for y_velocity in range(1,4):
        end_nodes.append(Node(goal_x, goal_y, [0, y_velocity]))
    heat_from_start = {nodes_to_test[0]: 0, nodes_to_test[1]: 0}
    heat_to_end = {nodes_to_test[0]: max_cost, nodes_to_test[1]: max_cost}
    true_cost_guide = {nodes_to_test[0].coords: 0, nodes_to_test[1].coords: 0}
    best_answer = max_cost

    while len(nodes_to_test) > 0:
        nodes_to_test = sorted(nodes_to_test, key=lambda i: i.get_tile_evaluation(heat_from_start))
        current = nodes_to_test.pop(0)
        next_nodes = current.get_connected_nodes()
        for next_node in next_nodes:
            #if max_cost == best_answer:
            #    print(next_node.coords)
            heat_at_next_node = heat_from_start[current] + next_node.heat

            if heat_at_next_node + next_node.get_closeness_to_end() > best_answer:
                pass
            elif (next_node.x, next_node.y) == (goal_x, goal_y):
                if heat_at_next_node < best_answer:
                    best_answer = heat_at_next_node
                    print(f"current minimum heat: {best_answer}")
                print(f"current open node list length: {len(nodes_to_test)}")
            elif next_node not in heat_from_start.keys():
                heat_from_start[next_node] = heat_at_next_node
                if next_node.coords not in true_cost_guide.keys():
                    true_cost_guide[next_node.coords] = heat_at_next_node
                nodes_to_test.append(next_node)
            elif heat_from_start[next_node] > heat_at_next_node and true_cost_guide[next_node.coords] > heat_at_next_node:
                heat_from_start[next_node] = heat_at_next_node
                if true_cost_guide[next_node.coords] > heat_at_next_node:
                    true_cost_guide[next_node.coords] = heat_at_next_node
                nodes_to_test.append(next_node)

    print(best_answer)

find_path()

# part 1 1068 too high
#
