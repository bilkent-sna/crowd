from datetime import datetime
from crowd.egress import file_egress as fd

class Visualizer():

    def __init__(self, artifact_path="artifacts", egress=None):
        self.artifact_path = artifact_path
        self.layout = None
        self.fig = None
        self.imgs = []
        self.data = {}
        self.egress = egress

    def generate_artifact_path(self, file, epoch):
        return self.artifact_path + "/" +str(datetime.now().strftime("%Y-%m-%d-%H:%M:%S")) +  "_"+file + "_" + str(epoch)