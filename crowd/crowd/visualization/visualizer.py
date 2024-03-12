from datetime import datetime
from crowd.digress import file_digress as fd

class Visualizer():

    def __init__(self, artifact_path="artifacts", digress=None):
        self.artifact_path = artifact_path
        self.layout = None
        self.fig = None
        self.imgs = []
        self.data = {}
        self.digress = digress

    def generate_artifact_path(self, file, epoch):
        # ':' not allowed in windows file names
        return self.artifact_path + "\\" +str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) +  "_"+file + "_" + str(epoch)