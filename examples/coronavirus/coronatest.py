from crowd import network as n
from crowd.visualization import basic as bv
from crowd.visualization import statsvisualizer as sv
from crowd.visualization import bubblemapvisualizer as bmv
import pandas as pd
import matplotlib.pyplot as plt
import time

def test():
  
    mynetwork = n.Network("coronavirus.yaml")
    visualizer = bmv.BubbleMapVisualizer("artifacts")
    mynetwork.run_states("states.tsv", [visualizer])
  
   # visualizer = bv.Basic("artifacts")
    #visualizer2 = sv.StatsVisualizer("artifacts")
    #visualizer.draw(mynetwork)
    #mynetwork.run(30000, [visualizer,visualizer2], agility=0)

test()