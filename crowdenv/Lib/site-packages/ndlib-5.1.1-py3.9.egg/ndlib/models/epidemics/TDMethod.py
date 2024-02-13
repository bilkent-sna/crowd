from ..DiffusionModel import DiffusionModel
import numpy as np
import future.utils
import pandas as pd
import ndlib.models.ModelConfig as mc
from ndlib.utils import multi_runs

__author__ = "Giulio Rossetti, Florian Guggenmos, and Peter Hofmann"
__license__ = "BSD-2-Clause"
__paper__ = "Guggenmos, F., Hofmann, P., and Fridgen, G. (2019): " \
            "How ill is your IT Portfolio? – Measuring Criticality in IT Portfolios Using Epidemiology," \
            "40th International Conference on Information Systems (ICIS), Munich, Germany" \
            "https://www.researchgate.net/publication/336103578"
__email__ = "giulio.rossetti@gmail.com, florian.guggenmos@fim-rc.de, peter.hofmann@fim-rc.de"


class TDMethod(DiffusionModel):
    """
    Model Parameters to be specified via ModelConfig
    """

    def __init__(self, graph, seed=None):
        """
             Model Constructor

             :param graph: A networkx graph object
         """
        super(self.__class__, self).__init__(graph, seed)
        self.available_statuses = {
            "Susceptible": 0,
            "Infected": 1
        }

        self.parameters = {
            "model": {
                "beta": {
                    "descr": "Infection rate",
                    "range": "[0,1]",
                    "optional": False}
            },
            "nodes": {},
            "edges": {},
        }

        self.name = "TD"

    def iteration(self, node_status=True):
        """
        Execute a single model iteration

        :return: Iteration_id, Incremental node status (dictionary node->status)
        """
        self.clean_initial_status(list(self.available_statuses.values()))

        actual_status = {node: nstatus for node, nstatus in future.utils.iteritems(self.status)}

        if self.actual_iteration == 0:
            self.actual_iteration += 1
            delta, node_count, status_delta = self.status_delta(actual_status)
            if node_status:
                return {"iteration": 0, "status": actual_status.copy(),
                        "node_count": node_count.copy(), "status_delta": status_delta.copy()}
            else:
                return {"iteration": 0, "status": {},
                        "node_count": node_count.copy(), "status_delta": status_delta.copy()}

        for u in self.graph.nodes():
            u_status = self.status[u]
            eventp = np.random.random_sample()
            neighbors = []
            neighbors = self.graph.neighbors(u)
            if self.graph.directed:
                neighbors = self.graph.predecessors(u)

            if u_status == 0:
                infected_neighbors = [v for v in neighbors if self.status[v] == 1]
                for infn in infected_neighbors:
                    to_node = u
                    from_node = infn
                    print((from_node+" and "+to_node))

                    w = self.graph.get_edge_data(from_node, to_node)
                    wi = float(w[0]['weight'])
                    if eventp < len(infected_neighbors)*wi:
                        actual_status[u] = 1
                        break

        delta, node_count, status_delta = self.status_delta(actual_status)
        self.status = actual_status
        self.actual_iteration += 1

        if node_status:
            return {"iteration": self.actual_iteration - 1, "status": delta.copy(),
                    "node_count": node_count.copy(), "status_delta": status_delta.copy()}
        else:
            return {"iteration": self.actual_iteration - 1, "status": {},
                    "node_count": node_count.copy(), "status_delta": status_delta.copy()}

    @staticmethod
    def execute_model(G, number_of_iterations, number_of_executions):
        """
        Execute the TD model

        :return: df including model results)
        """
        nodes = []
        for node in G.nodes:
            nodes.append(node)
        df_mod_multi = pd.DataFrame(0, index=list(range(0, number_of_iterations)), columns=nodes)
        for infected_node in nodes:
            # print(infected_node)
            model = TDMethod(G)
            cfg_mod = mc.Configuration()
            cfg_mod.add_model_parameter('beta', 'individual betas')  # infection rate

            infection_sets = []
            infection_sets.append(infected_node)

            cfg_mod.add_model_initial_configuration("Infected", infection_sets)
            model.set_initial_status(cfg_mod)

            trends_multi = multi_runs(model, execution_number=number_of_executions,
                                      iteration_number=number_of_iterations, nprocesses=10)

            execution_list = list(range(0, number_of_executions))
            for ex_n in execution_list:
                list_of_infected_nodes = trends_multi[ex_n]['trends']['node_count'][1]
                iterator_ifn = 0
                for ifn in list_of_infected_nodes:
                    df_mod_multi.at[iterator_ifn, infected_node] = df_mod_multi.at[iterator_ifn, infected_node] + ifn
                    iterator_ifn = iterator_ifn + 1
        df_mod_multi = df_mod_multi / number_of_executions
        return df_mod_multi

    @staticmethod
    def execute_criticality_score(G, model_results, gamma):
        """
        Applies the criticality score

        :return: dict including criticality scores)
        """

        df_diff = model_results.diff().drop([0])
        nodes = G.nodes
        for node in nodes:
            for i in list(range(len(df_diff)))[1:]:
                df_diff[node][i] = df_diff[node][i] / (i ** gamma)
        df_sum_diff = df_diff.sum()
        df_results = df_sum_diff + 1
        crit = df_results.to_dict()
        return crit

    @staticmethod
    def execute_method(graph, number_of_iterations, number_of_executions, gamma):
        """
        Executes the whole method

        :return: dict including criticality scores)
        """

        model_results = TDMethod.execute_model(graph, number_of_iterations, number_of_executions)
        result_dict = TDMethod.execute_criticality_score(graph, model_results, gamma)
        return result_dict










