  * Installation
  
  This project manages the python dependencies using
  [pipenv](https://pipenv.pypa.io/)
  
  `pipenv install`
  
  * Usage
  
  Please refer to the documentation of [SNAKES CPN](https://snakes.ibisc.univ-evry.fr/)
  
    * To Simulate the petri net and generate Simulation State PNG images:
    
    ```
    from lib import simulator
    
    # Define your petri net
    net = PetriNet("MyPetriNet")
    
    # Add Places and Transitions
    
    # Store Transitions in a list
    
    transitions = [Transition("A"), Transition("B")]
    
    simulator.run_simulation(net, transitions, limit=20)  # Limit the maximum number of transition firings to avoid infinite loops


    ```
    If the simulation has no errors, png images of the petri net "MyPetriNet-*.png" images will appear in the root directory ordered by the simulation state index:
    
    ![RaceCondition-0](RaceCondition-0.png)
