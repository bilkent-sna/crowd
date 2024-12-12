import matplotlib.pyplot as plt
import imageio
import networkx as nx
import os
import importlib
import math
from . import visualizer as v
from .. import node as n

class StatsVisualizer(v.Visualizer):

 # def __init__(self):

  def animate(self):
    images = []
    
    # Using the png images create a gif image
    for filename in self.imgs:
      images.append(imageio.imread(filename))
    imageio.mimsave(super().generate_artifact_path("stats", "final")+".gif", images)

  """
      # Removing unused .pngs to save up space
    for filename in self.imgs:
      os.remove(filename)
"""

  def draw(self, network, epoch):
    self.fig = plt.figure()

    new_module = importlib.import_module(network.conf["definitions"]["source"], package=None)   
    cls = getattr(new_module, network.conf["definitions"]["source"])
    # // need to update this, as there may be many emit functions
    stat_function = getattr(cls, network.conf["definitions"]["statfunctions"][0])
    result = stat_function(network)
    if "X" not in self.data:
      self.data["X"] = []
    if "Y" not in self.data:
      self.data["Y"] = []

    self.data["X"].append(epoch)
    self.data["Y"].append(result)
    plt.axis([0, epoch+100, 0, math.ceil(result)+1])
    plt.plot(self.data["X"], self.data["Y"])

    imagename = super().generate_artifact_path("stats", epoch)
    self.imgs.append(imagename+".png")
    plt.xlabel('Epoch')
    plt.ylabel('Blue/Red ratio')
    plt.title('Change of Blue/Red Ratio over Epochs')
    plt.savefig(imagename)
    plt.close()

    if self.egress is not None:
      self.egress.save(self.data)

