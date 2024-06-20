from crowd import network as netw
import networkx as nx

class EdgeSimNetwork(netw.Network):
    def __init__(self, conf_dict):
        # create network by calling parent's constructor
        super().__init__(conf_dict)
        self.update_method = None

    def run(self, epochs, visualizers = None, snapshot_period = 1, agility = 1, digress = None):
        # Iteration data dictionary
        simulation_data = {}

        for epoch in range(0, epochs):
            if (epoch % snapshot_period) == 0 or (epoch == epochs-1):
                print("Epoch:", epoch)
                if visualizers is not None:
                    for visualizer in visualizers:
                        visualizer.draw(self, epoch)

                if digress is not None:
                    digress.save_graph(str(epoch), self.G, 'graph.json')

            self.update_method(self)
            