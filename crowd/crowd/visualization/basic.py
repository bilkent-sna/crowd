import matplotlib.pyplot as plt
import imageio
import networkx as nx
import os
from . import visualizer as v
from .. import node as n

class Basic(v.Visualizer):

  def animate(self):
    images = []

    # Using the png images create a gif image
    for filename in self.imgs:
      images.append(imageio.imread(filename))
    imageio.mimsave(super().generate_artifact_path("basic","final")+".gif", images)
    """
    # Removing unused .pngs to save up space
    for filename in self.imgs:
      os.remove(filename)
    """

  def draw(self, network, epoch):
    if self.layout == None:
      #self.layout = nx.spring_layout(network.G, iterations=50, seed=10)
      #self.layout = nx.spectral_layout(network.G)
      self.layout = nx.random_layout(network.G)
    color_map = []
    
    for _,data in network.G.nodes(data=True):
      color_map.append(network.conf["definitions"]["nodetypes"][type(data["node"]).__name__]["color"])

    self.fig = plt.figure()
    img = nx.draw_networkx(network.G, pos = self.layout, node_color = color_map, edge_color = 'gray', with_labels = False, node_size = 20, width=0.5)
    imagename = super().generate_artifact_path("basic", epoch)
    self.imgs.append(imagename+".png")
    plt.axis('off')
    plt.savefig(imagename, transparent=True, bbox_inches='tight', pad_inches=0)
    plt.close()
    