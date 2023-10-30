from crowd import network as n
from crowd.visualization import basic as bv



mysimplenetwork = n.Network("simple.yaml")
visualizer = bv.Basic("artifacts")
mysimplenetwork.run(1000, visualizers=[visualizer], snapshot_period=10, agility=0)
