class ParameterWatch: #similar to datacollectors in soil and mesa
    def __init__(self) -> None:
        pass

    #parameter watcher by default just saves the value of parameter every iteration
    #or user can define what to do with it with python code
    #for example, save a+b

    #or user can ask to call a library's method on it
    #like calculate centralities every iteration through networkx
    
    #do we allow importing libraries that we do not use? for example can they call numpy to do matrix multiplier etc