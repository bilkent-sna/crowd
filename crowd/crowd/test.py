import json 
class test:
    def __init__(self, input1, input2):
        self.input1 = input1
        self.input2 = input2

    def get_crowd_version(self):
        return "1.0.0"
    
    def get_values(self):
        values = {}
        values["input1"] = self.input1
        values["input2"] = self.input2
        return json.dumps(values)
    

class test2:
    def get_values(self, input1, input2):
        values = {}
        values["input1"] = input1
        values["input2"] = input2
        return json.dumps(values)