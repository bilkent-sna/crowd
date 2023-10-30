import random
from crowd import node as n

class simple:

    def get_total_count(self):
        return 0

    def blue_red_ratio(network):
        all_blue_count = 0
        all_red_count = 0
        for node in network.G.nodes(data=True):
            if type(node[1]['node']).__name__ == 'Type2':
                all_blue_count += 1
            elif type(node[1]['node']).__name__ == 'Type1':
                all_red_count += 1

        return all_blue_count / all_red_count

    def calculate_fitness(network, node):
        neighbors = network.G.neighbors(node)
        n_red_count = 0
        n_blue_count = 0
        for neighbor in neighbors:
            neighbor_data = network.G.nodes[neighbor]
            if type(neighbor_data['node']).__name__ == "Type1":
                n_red_count = n_red_count + 1
            elif type(neighbor_data['node']).__name__ == "Type2":
                n_blue_count = n_blue_count + 1
        fitness = 0

        if type(network.G.nodes(data=True)[node]['node']).__name__ == "Type2":
            fitness = (1 - network.conf["info"]["w"]) + network.conf["info"]["w"] * (
                        n_blue_count * (network.conf["info"]["b"] - network.conf["info"]["c"]) + n_red_count * (
                    -network.conf["info"]["c"]))

        if type(network.G.nodes(data=True)[node]['node']).__name__ == "Type1":
            fitness = (1 - network.conf["info"]["w"]) + network.conf["info"]["w"] * (
                        n_blue_count * (network.conf["info"]["b"]))

        return fitness


    def get_neighbors_and_color_counts(network, node):
        neighbors = network.G.neighbors(node)

        red_count = 0
        blue_count = 0
        for neighbor in neighbors:
            neighbor_data = network.G.nodes[neighbor]
            if type(neighbor_data['node']).__name__ == "Type1":
                red_count = red_count + 1
            elif type(neighbor_data['node']).__name__ == "Type2":
                blue_count = blue_count + 1
        return neighbors, blue_count, red_count


    def randomly_choose_precise(network):
        nodes = network.G.nodes(data=True)

        choosen_node_id, choosen_node = random.choice(list(nodes))

        """if type(choosen_node['node']).__name__ != "Neutral":
            continue
        """
        #neighbors, blue_count, red_count = simple.get_neighbors_and_color_counts(network, choosen_node_id)


        return choosen_node_id


    def update(node, *argv):
        # node_fitness = calculate_fitness(G, choosen_node, red_nodes, blue_nodes)
        blue_fitness_sum = 0
        red_fitness_sum = 0
        # print neighbors
        (network,) = argv

        neighbors = network.G.neighbors(node)
        for neighbor in neighbors:
            neighbor_data = network.G.nodes[neighbor]
            if type(neighbor_data['node']).__name__ == "Type1":
                red_fitness_sum = red_fitness_sum + simple.calculate_fitness(network, neighbor)
            elif type(neighbor_data['node']).__name__ == "Type2":
                blue_fitness_sum = blue_fitness_sum + simple.calculate_fitness(network, neighbor)

        own_fitness = simple.calculate_fitness(network, node)

        if type(network.G.nodes()[node]['node']).__name__ == "Type1":
            red_fitness_sum += own_fitness
        if type(network.G.nodes()[node]['node']).__name__ == "Type2":
            blue_fitness_sum += own_fitness

        # print(blue_fitness_sum)
        # print(red_fitness_sum)
        nodeitself = network.G.nodes[node]

        if (red_fitness_sum > blue_fitness_sum):
            nodeitself['node'] = Type1()

        elif (red_fitness_sum < blue_fitness_sum):
            nodeitself['node'] = Type2()


    def changetype(node, *argv):
        # print("Changing type")
        if (type(node['node']).__name__ == "Type2"):
            node['node'] = Type1()
        else:
            node['node'] = Type2()

        return


    def select_nodes(network):
        nodes = []
        nodes.append(simple.randomly_choose_precise(network))
        return nodes


class Type1(n.Node):
        def select_actions(self, actions):
            n_actions = len(actions)
            n_selected_actions = random.randint(0, n_actions)
            selected_action_names = random.sample(actions, k=n_selected_actions)

            selected_actions = []
            for selected_action in selected_action_names:
                action_name = list(selected_action.keys())[0]
                argv = []
                selected_actions.extend({action_name: argv})
            return selected_actions

class Type2(n.Node):
    def select_actions(self, actions):
        n_actions = len(actions)
        n_selected_actions = random.randint(0, n_actions)
        selected_action_names = random.sample(actions, k=n_selected_actions)

        selected_actions = []
        for selected_action in selected_action_names:
            action_name = list(selected_action.keys())[0]
            argv = []
            selected_actions.extend({action_name: argv})
        return selected_actions

class Type3(n.Node):
    def select_actions(self, actions):
        n_actions = len(actions)
        n_selected_actions = random.randint(0, n_actions)
        selected_action_names = random.sample(actions, k=n_selected_actions)

        selected_actions = []
        for selected_action in selected_action_names:
            action_name = list(selected_action.keys())[0]
            argv = []
            selected_actions.extend({action_name: argv})
        return selected_actions

class moon:
    def get_parameters(self):
        return