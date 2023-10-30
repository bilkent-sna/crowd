import os
from jinja2 import Template
from shutil import copyfile
from . import visualizer as v

class BubbleMapVisualizer(v.Visualizer):

    TEMPLATE_FILE = os.path.join(os.path.dirname(__file__), 'd3/template.html')
    TEMPLATE_JSON = os.path.join(os.path.dirname(__file__), 'd3/world.geojson')
    PLAYERTEMPLATE_FILE =  os.path.join(os.path.dirname(__file__), 'd3/playertemplate.html')

    def __init__(self, artifact_path="artifacts"):
        super().__init__(artifact_path)
        self.template = None
        self.playertemplate = None

    def animate(self):
        if self.playertemplate is None:
            with open(BubbleMapVisualizer.PLAYERTEMPLATE_FILE) as f:
                self.playertemplate = f.read()

        os.makedirs(self.artifact_path, exist_ok=True)
        
        tm = Template(self.playertemplate)

        html = ""
        for img in self.imgs:
            if html == "":
                html += "<div class='item first'><iframe src=\""+img.replace(self.artifact_path+"/","")+"\" style=\"height:700px;width:1260px;border:0;\" scrolling=\"no\"></iframe></div>\n"
            else:
                html += "<div class='item'><iframe src=\""+img.replace(self.artifact_path+"/","")+"\" style=\"height:700px;width:1260px;border:0;\" scrolling=\"no\">></iframe></div>\n"

        rendered_html = tm.render(frames=html)
        player = super().generate_artifact_path("bubblemap", "player") + ".html"
        f= open(player,"w+")
        f.write(rendered_html)
        f.close()

        return

    def draw(self, network, epoch):
        if self.template is None:
            with open(BubbleMapVisualizer.TEMPLATE_FILE) as f:
                self.template = f.read()

        os.makedirs(self.artifact_path, exist_ok=True)
        
        epoch = epoch.replace("/","-")
        tm = Template(self.template)
        datafile = epoch+".csv"
        rendered_html = tm.render(datafile=datafile, epoch=epoch)

        f = open(self.artifact_path+"/"+datafile,"w+")
        f.write("homelat,homelon,homecontinent,n\n")

        for node, data in network.G.nodes(data=True):
            line = str(data["Lat"]) + "," + str(data["Long"]) +"," +"Europe"+","+ str(data["state"]) +"\n"
            f.write(line)

        f.close()    

        imagename = super().generate_artifact_path("bubblemap", epoch) + ".html"
        f= open(imagename,"w+")
        f.write(rendered_html)
        f.close()
        self.imgs.append(imagename)
        copyfile(BubbleMapVisualizer.TEMPLATE_JSON, self.artifact_path+"/world.geojson")


        