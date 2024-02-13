import yaml
import os
import importlib
import logging 

class ConfChecker:
    
    FIELDS = {
        'name': {'required' : True},
        'nodetypes' : {'required' : True},
        'definitions': {'required' : False},
        'structure': {'required' : True},
        'node_actions': {'required' : False},
        'info': {'required' : False},
        'functions': {'required' : False},
        'preprocessing': {'required': False},
        'statfunctions': {'required': False}
    }

    #CONF_FILE = os.path.join(os.path.dirname(__file__), 'conf3.yaml')
    #CONF_FILE = os.path.join(os.path.dirname(__file__), 'conf4.yaml')
    CONF_FILE = 'conf4.yaml'

    def __init__(self, network_file):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.nconf = self.parse(network_file)
        #self.nconf = self.parse_input_file(network_file)
        self.logger.info("Initialized confchecker object")
        

    def get_conf(self):
        return self.nconf 


    def check_conf(self, mconf, nconf):
        # Check if unrecognized fields present
        print("Checking for unrecognized fields")
        print(mconf)
        print(nconf)
        for elem in nconf:
            if "fields" in mconf:
                # Check if unrecognized fields present
                if elem not in mconf["fields"]:
                    raise Exception("Unrecognized field:", elem)
            
            if "select_fields" in mconf:
                if elem not in mconf["select_fields"]:
                    raise Exception("Unrecognized field:", elem) 
        print("Check 2")
        # Check if required fields present
        if "fields" in mconf:
            for melem in mconf["fields"]:
                if mconf["fields"][melem]["required"] == True and melem not in nconf:
                    raise Exception("Required field " + melem + " is not defined in the input file")

        # Check if only one selected field present
        if "select_fields" in mconf:
            count = 0
            for melem in mconf["select_fields"]:
                if melem in nconf:
                    count+=1
            if count > 1:        
                raise Exception("Only one field can be present in " + melem)
            if count == 0:
                raise Exception("One of the fields must be present in " + melem)
        
        print("Recurse")
        for elem in nconf:
            if type(nconf[elem]) is dict:
                if "fields" in mconf:
                    if elem in mconf["fields"] :
                        print("Recursing for field " + elem)
                        self.check_conf(mconf["fields"][elem], nconf[elem])
                if "select_fields" in mconf:
                    if elem in mconf["select_fields"]:
                        print("Recursing for selected_field " + elem)
                        self.check_conf(mconf["select_fields"][elem], nconf[elem])
        
        return True

    def parse(self, network_file):
        print("HELLO INSIDE PARSE METHOD")
        print(ConfChecker.CONF_FILE)
        #with open(ConfChecker.CONF_FILE) as f:
         #   module_conf = yaml.load(f, Loader=yaml.FullLoader)
        #self.logger.info("module_conf:" + str(module_conf))
        
        with open(network_file) as f:
            nconf = yaml.load(f, Loader=yaml.FullLoader)
        #self.logger.info("module_conf:" + str(nconf))

        try: 
            if self.check_conf(module_conf, nconf):
                return nconf
        except Exception as ex:
            print(str(ex))
     
        """
        for field in module_conf["fields"]:
            print(field)
        """

    def parse_input_file(self, network_file):
        with open(network_file) as f:
            nconf = yaml.load(f, Loader=yaml.FullLoader)
        if self.check_input_network(nconf) == True:
            return nconf
        else:
            return None

    def check_input_network(self, nconf):
        
        try:
            if (nconf is None):
                return False
            self.check_fields(nconf)    
            if("definitions" in nconf):
                self.check_source_files(nconf)
            return True
        except Exception as ex:
            print("Got exception " + str(ex))
            return False

    def check_fields(self, nconf):
        # Check whether only possible network fields are written in the input
        for elem in nconf:
            if elem not in ConfChecker.FIELDS:
                raise Exception("Undefined field:", elem)

        # Check whether compulsory fields are present
        for elem in ConfChecker.FIELDS:
            if ConfChecker.FIELDS[elem]["required"] == True and elem not in nconf:
                raise Exception("Required field " + elem + " is not defined in the input file")

        return True


    def check_source_files(self, nconf):
        self.logger.info("Checking source files")
        
        # Check for the existence of definition file
        definitions = nconf["definitions"] 
        definitions_file = definitions+ ".py"
        if not os.path.isfile(definitions_file):
            raise Exception("Definition file "+definitions_file+" does not exist")

        # Check for network functions    
        new_module = importlib.import_module(definitions, package=None)
        cls = getattr(new_module, definitions)
        for funct in nconf["functions"]:
            if not (hasattr(cls, funct)):
                raise Exception("Function "+funct+" does not exist in "+ definitions)
        
        # Check for the existence of nodetypes
        for nodetype in nconf["nodetypes"]:
            
            if not nodetype in dir(new_module):
                raise Exception("NodeType definition class:" + nodetype + " does not exist in "+ definitions)
        
        # Check for the existence of actions
        for node_action in nconf["node_actions"]:
            action_name = list(node_action.keys())[0]
            if not (hasattr(cls, action_name)):
                raise Exception("Action function "+ action_name +" does not exist in "+ definitions)
        
        return True      