from . import digress as d

class file_digress(d.digress):
    
    def save(self, input, append=True):
        # save 
        f = open(self.artifact_path, "a")
        f.write(str(input)+"\n")
        f.close()