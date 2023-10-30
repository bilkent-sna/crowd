import community
import importlib
import networkx as nx
import random
from . import preprocessor as p

class CommunityDetection(p.Preprocessor):
    
    def __init__(self):
        self.threshold = 10

    def get_equi_count_partitions(self, parts):
        partition_keys= set(parts.values())
        partition_counts = {}
        for partition in partition_keys:
            partition_counts[partition] = sum(x == partition for x in parts.values())
        
        sorted_partition_counts = sorted(partition_counts.items(), key=lambda item: item[1])
        #partition_counts = {k: v for k, v in sorted(partition_counts.items(), key=lambda item: item[1])}

        minimum = len(parts)
        best_partitions = None
        keys = list([i[0] for i in sorted_partition_counts])
        for i in range(0,len(partition_counts)-1):
            
            partition_count = partition_counts[keys[i]]
            partition_count2 = partition_counts[keys[i+1]]
            diff = partition_count2 - partition_count
            if diff < minimum and diff <= self.threshold:
                minimum = diff
                best_partitions = [keys[i], keys[i+1]]
        print(partition_counts)
        print(best_partitions)
        return best_partitions
    

    def process(self, network, args):
        # Args are partitions
        mandatory_nodetypes = args

        # Partition until you are sure that the two partition sides are equally weighted
        
        parts = community.best_partition(network.G)
        best_partitions = self.get_equi_count_partitions(parts)
        if (best_partitions == None):
            return False

        new_module = importlib.import_module(network.conf["definitions"], package=None)
        nodetypes = list(network.conf["nodetypes"].keys())
        nodetypes_counts = {}
        for nodetype in nodetypes:
            nodetypes_counts[nodetype] = 0
            
        for mandatory_nodetype in mandatory_nodetypes:
            nodetypes.remove(mandatory_nodetype)
        
        count  = 0
        

        for node in network.G:        
            if parts.get(node) == best_partitions[0]:
                selected_nodetype = mandatory_nodetypes[0]
            elif parts.get(node) == best_partitions[1]:
                selected_nodetype = mandatory_nodetypes[1]
            else:
                selected_nodetype  = random.choice(nodetypes)

            nodetypes_counts[selected_nodetype] +=1
            nodetype = getattr(new_module, selected_nodetype)
            nodeobject = nodetype()
            #print(nodeobject)
            nx.set_node_attributes(network.G, {count:{"node": nodetype()}})
            count = count + 1
        print(nodetypes_counts)    
        return True

    