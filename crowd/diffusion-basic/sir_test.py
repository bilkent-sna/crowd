from crowd.models import DiffusionNetwork as n
from crowd.visualization import basic as bv
import os

yaml_path = os.path.join(os.path.dirname(__file__), 'SIR.yaml')
mysimplenetwork = n.DiffusionNetwork(yaml_path)
visualizer = bv.Basic(os.path.join(os.path.dirname(__file__), 'artifacts'))

mysimplenetwork.run(10, visualizers=[visualizer], snapshot_period=2)
