#%% Imports:
    
# Add Backend to path
import sys
sys.path.append('C:/Users/eeveetza/Documents/GitHub/AlgoBrain_local/Backend')

from Environment import World
from Mediator import Mediator

#%%
class Experiment(Mediator):
    
    def __init__(self, start_organism = "default", target_function = "nand", N=30):
        
        # Define the organism that we start with
        self.start_organism = start_organism
        
        # Define the function that we want to evolve:
        self.target_function = target_function
        
        # Here we will save the first organism which really computes the target function
        self.first_specimen = None
        
        # The World in which everything happens
        self.world = World(N, cm_prob = 0.05)
        
        # Set self as the world's linked experiment
        self.world.experiment = self
        
        # A helper attribute, to flag organisms which reported a function but can't actually solve it
        self.flagged = None
        
    # Experiment, just like World, implements the mediator interface
    # In this case, the mediator is used so that the world can notify the
    # current experiment of any important results
    def notify(self, sender, event, result):
        
        if event == "nand":
            self.react_on_nand(sender, result)
            
        if event == "function_IO":
            self.react_on_function_io(sender,result)
            
    def react_on_nand(self,sender,result):
        
        # Don't react on nand for flagged organisms
        if self.flagged == sender:
            pass
        
        else:
            print("REACTING ON NAND")
        
            # Check whether the sender truly did compute NAND by letting it run for a certain (large) amount of cycles
            # and checking whether it outputs NAND
        
            # How we check this:
            # The organism needs to compute NAND once in the test world in 2000 cycles
        
            # The sender is the organism itself, the result is its memory content
        
            test_world = World(1,cm_prob = 0, ins_prob = 0, del_prob = 0)
        
            test_world.place_custom(result)
        
            test_world.experiment = self
            test_world.output = True
        
            test_world.schedule(2000)
        
    def react_on_function_io(self,sender,result):
        
        if self.flagged == sender:
            pass
        
        else:
            
            if self.target_function == "nand":
            
                print("Reacting on IO")
            
                i0 = result[0]
                i1 = result[1]
                out = result[2]
            
                print(i0,i1,out)
            
            
                if out == ~(i0 & i1):
                    print("Test passed")
                    if self.first_specimen == None:
                        self.first_specimen = sender.original_memory
                    else:
                        pass
                
                # If an organism that reported NAND failed even a single one of these tests the sender gets flagged
                # and isn't allowed to be tested any longer
                else:
                    self.first_specimen = None
                    self.flagged = sender
                    print("Test failed")

    # We run the experiment until we have evolved the function that we wanted to evolve
    # If we have correctly evolved such a function, the first_specimen attribute will no longer be None
    def run(self):
        
        self.world.fill("default")
        
        while self.first_specimen == None:
            self.world.schedule(1)