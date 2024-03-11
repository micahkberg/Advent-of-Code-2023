def load(day):
    contents = open(f"./inputs/{day}.txt", "r").read().strip().split("\n")
    return contents


heat_loss_map = load("17")


def print_best_path_so_far(cost_map):
    # prints out a map of heat at different city blocks
    for y in range(goal_y + 1):
        row = "|"
        for x in range(goal_x+1):
            if (x, y) in cost_map.keys():
                row += str(cost_map[(x, y)]).rjust(4, "-") + "|"
            else:
                row += ("----|")
        print(row)

# coords for bottom right spot
goal_x = len(heat_loss_map[0])-1
goal_y = len(heat_loss_map)-1

# wild choice for a max cost
max_cost_estimate = ((goal_x * 9) + (goal_y * 9)) * 2
# instead i'll just put the max cost from getting a wrong answer :^)
small_max_cost = 1314
#max_cost_estimate = small_max_cost


class Node:
    def __init__(self, x, y, velocity):
        self.x = int(x)
        self.y = int(y)
        self.coords = (self.x, self.y)
        self.heat = int(heat_loss_map[self.y][self.x])
        self.velocity = velocity
        self.heat_to_end = self.get_max_heat_to_end()

    def get_closeness_to_end(self):
        # manhattan distance to goal
        return (goal_x-self.x)+(goal_y-self.y)

    def get_max_heat_to_end(self):
        # manhattan distance times max heat of each tile
        return self.get_closeness_to_end() * 9

    def get_tile_evaluation(self, cost_guide, dfs=True):
        #return self.get_closeness_to_end(), self.heat
        #return max(self.velocity)*-1, cost_guide[self], self.heat, self.get_closeness_to_end()

        # sorting criteria based on if we have reached the end or not
        # if end not reached, depth first search, else focus on seemingly """best""" points to search from

        if dfs:
            return self.get_closeness_to_end(), sum(self.velocity) * -1
            #return cost_guide[self], self.get_closeness_to_end() #, max(self.velocity)*-1, cost_guide[self]+self.get_closeness_to_end()
        else:
            return cost_guide[self] + self.get_closeness_to_end(), max(self.velocity)*-1

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
        # unit vector representing faced direction of lava car
        u_vector = [self.velocity[0]/abs(sum(self.velocity)), self.velocity[1]/abs(sum(self.velocity))]

        # if not going too fast can go straight
        if abs(sum(self.velocity)) < 10:
            potential_dirs.append(u_vector)

        # left and right turns
        if abs(sum(self.velocity)) >= 4:
            potential_dirs.append([u_vector[1], u_vector[0]*-1])
            potential_dirs.append([u_vector[1]*-1, u_vector[0]])

        # for each of those above possibilities, create a new node for those positions and return them
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
    nodes_to_test = [Node(1, 0, [1, 0]), Node(0, 1, [0, 1])]
    end_nodes = []
    heat_from_start = {nodes_to_test[0]: 3, nodes_to_test[1]: 4}

    for velocity in range(1, 11):
        heat_at_end = heat_loss_map[goal_y][goal_x]
        # in x direction
        new_end_node = Node(goal_x, goal_y, [velocity, 0])
        end_nodes.append(new_end_node)
        # in y direction
        new_end_node = Node(goal_x, goal_y, [0, velocity])
        end_nodes.append(new_end_node)

    true_cost_guide = {nodes_to_test[0].coords: 0, nodes_to_test[1].coords: 0}
    best_answer = max_cost_estimate
    iters = 0
    while len(nodes_to_test) > 0:
        if best_answer == max_cost_estimate:
            nodes_to_test = sorted(nodes_to_test, key=lambda i: i.get_tile_evaluation(heat_from_start))
            current = nodes_to_test.pop(0)
        else:
            current = nodes_to_test.pop(0)

        # print out stuff for debugging purposes
        if iters % 1000 == 0:
            nodes_to_test = sorted(nodes_to_test, key=lambda i: i.get_tile_evaluation(heat_from_start, dfs=False))
        if iters % 10000 == 0:
            print(f"loop# {iters}")
            print(f"nodes to test: {len(nodes_to_test)}")
            print(f"current: {current.coords}")
        if iters % 100000 == 0:
            print_best_path_so_far(true_cost_guide)
        iters += 1

        # if we are over best answer, skip to next one
        if heat_from_start[current] + current.get_closeness_to_end() > best_answer:
            #print("node trimmed")
            #print(current)
            #print(heat_from_start[current])
            continue

        # list of next possible nodes
        next_nodes = current.get_connected_nodes()

        for next_node in next_nodes:
            # heat we would be at for new node
            heat_at_next_node = heat_from_start[current] + next_node.heat

            if next_node in end_nodes:
                print("Found end point!")
                if heat_at_next_node < best_answer:
                    heat_from_start[next_node] = heat_at_next_node
                    true_cost_guide[next_node] = heat_at_next_node
                    best_answer = heat_at_next_node
                    print(f"potential part1 : {heat_at_next_node}")
                continue
            improvement = False
            if next_node not in heat_from_start.keys():
                heat_from_start[next_node] = heat_at_next_node
                improvement = True
            elif heat_from_start[next_node] > heat_at_next_node:
                heat_from_start[next_node] = heat_at_next_node
                improvement = True

            if next_node.coords not in true_cost_guide.keys():
                true_cost_guide[next_node.coords] = heat_at_next_node
                improvement = True
            elif true_cost_guide[next_node.coords] > heat_at_next_node:
                true_cost_guide[next_node.coords] = heat_at_next_node
                improvement = True

            if improvement and heat_at_next_node + next_node.get_closeness_to_end() < best_answer:
                nodes_to_test.append(next_node)
    print(best_answer)

find_path()

# part 1 1314 too high
#
