from crowd.project_management.new_project import NewProject


project_name = "nodeparamstest"

my_project = NewProject()
my_project.load_project(project_name)

my_project.lib_run_simulation(3, 1, 1, [], [], [], [])

#   File "c:\users\serif\desktop\nese\dyn and soc netw\simulation tool\netsim\crowd\crowd\models\DiffusionNetwork.py", line 97, in run
#     for method in self.after_iteration_methods:
# TypeError: 'NoneType' object is not iterable