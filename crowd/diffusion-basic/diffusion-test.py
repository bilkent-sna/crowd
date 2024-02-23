from crowd.models import diffusion as n
from crowd.visualization import basic as bv
import os

yaml_path = os.path.join(os.path.dirname(__file__), 'independent-cascade.yaml')
mysimplenetwork = n.DiffusionNetwork(yaml_path)
#visualizer = bv.Basic("artifacts")

trends = mysimplenetwork.run(5)

print(trends)
