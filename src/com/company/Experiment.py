#%% Imports:
    
# Add Backend to path
import sys
sys.path.append('C:/Users/eeveetza/Documents/GitHub/AlgoBrain/src/com/company/Backend')

from Environment import World
from Mediator import Mediator

#%%
class Experiment(Mediator):
    
    def __init__(self, start_organism = "default", target_function = "nand", N=30,cm_prob = 0.05, ins_prob = 0.05, del_prob = 0.05, notify_ = False):
        
        # Define the organism that we start with
        self.start_organism = start_organism
        
        # Define the function that we want to evolve:
        self.target_function = target_function
        
        # Here we will save the first organism which really computes the target function
        self.first_specimen = None
        
        # The World in which everything happens
        self.world = World(N, cm_prob = cm_prob, ins_prob = ins_prob, del_prob = del_prob, notify_= notify_)
        
        # Set self as the world's linked experiment
        self.world.experiment = self
        
        # A helper attribute, to flag organisms which reported a function but can't actually solve it
        self.flagged = None
        
        # A helper attribute
        self.counter = 0
        
        if self.start_organism == "default":
            self.world.fill("default")
            
        elif self.start_organism == "nand":
            self.world.fill([23, 20, 2, 0, 21, 2, 6, 1, 19, 13, 18, 2, 25, 9, 2, 18, 16, 15, 15, 2, 2, 2, 18, 7, 2, 2, 2, 18, 2, 20, 10, 8, 18, 6, 4, 19, 8, 8, 17, 2, 6, 20, 19, 25, 2, 0, 17, 21, 0, 1])
        
        elif self.start_organism == "not":
            self.world.fill([16, 20, 2, 0, 21, 2, 25, 6, 2, 5, 18, 2, 14, 6, 14, 17, 7, 2, 12, 18, 10, 2, 17, 2, 2, 12, 2, 3, 15, 2, 2, 2, 17, 2, 2, 2, 11, 4, 24, 2, 11, 20, 19, 25, 2, 0, 17, 21, 0, 1])
        
        elif self.start_organism == "or_n":
            self.world.fill([23, 20, 2, 0, 21, 2, 6, 1, 19, 0, 18, 2, 16, 9, 24, 18, 16, 15, 15, 9, 2, 2, 18, 7, 2, 2, 2, 18, 2, 20, 10, 8, 18, 6, 12, 19, 8, 8, 17, 2, 6, 20, 19, 25, 2, 0, 17, 21, 0, 1])
        
        elif self.start_organism == "and":
            self.world.fill([1, 20, 2, 0, 21, 2, 11, 9, 13, 7, 20, 23, 11, 17, 7, 3, 7, 15, 20, 2, 20, 9, 18, 2, 0, 17, 2, 1, 18, 15, 15, 16, 13, 11, 7, 18, 8, 19, 17, 20, 19, 1, 19, 25, 2, 0, 17, 21, 0, 1])
            
        elif self.start_organism == "or":
            self.world.fill([10, 20, 2, 0, 21, 2, 13, 9, 13, 7, 13, 3, 10, 17, 7, 3, 7, 15, 20, 17, 22, 9, 18, 2, 0, 14, 2, 1, 18, 15, 15, 16, 0, 11, 7, 9, 2, 18, 17, 20, 3, 1, 19, 25, 2, 0, 17, 21, 0, 1])
            
        elif self.start_organism == "and_n":
            self.world.fill([10, 20, 2, 0, 21, 2, 13, 9, 13, 7, 13, 3, 23, 17, 7, 3, 7, 15, 20, 17, 22, 9, 18, 2, 0, 14, 2, 1, 18, 15, 15, 16, 0, 13, 7, 9, 2, 18, 17, 20, 3, 1, 19, 25, 2, 0, 17, 21, 0, 1])
            
        elif self.start_organism == "nor":
            self.world.fill([10, 20, 2, 0, 21, 2, 13, 9, 13, 7, 13, 3, 23, 17, 7, 3, 7, 15, 20, 17, 22, 9, 18, 2, 12, 14, 2, 1, 18, 15, 11, 16, 0, 13, 7, 9, 2, 18, 17, 20, 3, 19, 19, 25, 2, 0, 17, 21, 0, 1])
            
        elif type(self.start_organism) == list:
            self.world.fill(start_organism)
            
    # Experiment, just like World, implements the mediator interface
    # In this case, the mediator is used so that the world can notify the
    # current experiment of any important results
    def notify(self, sender, event, result):
        
        if event == self.target_function:
            self.react_on_function(sender, result)
            
        if event == "function_IO":
            self.react_on_function_io(sender,result)
            
    def react_on_function(self,sender,result):
        
        # Don't react on nand for flagged organisms
        if self.flagged == sender:
            pass
        
        else:
            print("Reacting on " + str(self.target_function))
        
            # Check whether the sender truly did compute NAND by letting it run for a certain (large) amount of cycles
            # and checking whether it outputs NAND
        
            # How we check this:
            # The organism needs to compute NAND once in the test world in 2000 cycles
        
            # The sender is the organism itself, the result is its memory content
        
            test_world = World(1,cm_prob = 0, ins_prob = 0, del_prob = 0)
        
            test_world.place_custom(result)
        
            test_world.experiment = self
            test_world.output = True
            
            print("Scheduled test world")
            test_world.schedule(5000)
            
            if self.flagged == sender.original_memory or self.counter < 5:
                self.first_specimen = None
            else:
                self.first_specimen = sender.original_memory
                
            self.counter = 0
        
    def react_on_function_io(self,sender,result):
        
        if self.flagged == sender.original_memory:
            print("Flagged ass bitch")
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
                    self.flagged = sender.original_memory
                    print("Test failed")
                    
            elif self.target_function == "not":
                
                print("Reacting on IO")
            
                i0 = result[0]
                i1 = result[1]
                out = result[2]
            
                print(i0,i1,out)
            
                if out == ~i0:
                    self.counter += 1
                    print("Test passed")
                
                else:
                    self.first_specimen = None
                    self.flagged = sender.original_memory
                    self.counter = 0
                    print("Test failed")
                    
            elif self.target_function == "and":
                
                print("Reacting on IO")
            
                i0 = result[0]
                i1 = result[1]
                out = result[2]
            
                print(i0,i1,out)
            
                if out == i0 & i1:
                    self.counter += 1
                    print("Test passed")
                
                else:
                    self.first_specimen = None
                    self.flagged = sender.original_memory
                    self.counter = 0
                    print("Test failed")
                    
            elif self.target_function == "or":
                
                print("Reacting on IO")
            
                i0 = result[0]
                i1 = result[1]
                out = result[2]
            
                print(i0,i1,out)
            
                if out == i0 | i1:
                    self.counter += 1
                    print("Test passed")
                
                else:
                    self.first_specimen = None
                    self.flagged = sender.original_memory
                    self.counter = 0
                    print("Test failed")
                    
            elif self.target_function == "and_n":
                
                print("Reacting on IO")
            
                i0 = result[0]
                i1 = result[1]
                out = result[2]
            
                print(i0,i1,out)
            
                if out == i0 & ~i1 or out == ~i0 & i1:
                    self.counter += 1
                    print("Test passed")
                
                else:
                    self.first_specimen = None
                    self.flagged = sender.original_memory
                    self.counter = 0
                    print("Test failed")
                    
            elif self.target_function == "nor":
                
                print("Reacting on IO")
            
                i0 = result[0]
                i1 = result[1]
                out = result[2]
            
                print(i0,i1,out)
            
                if out == ~i0 & ~i1:
                    self.counter += 1
                    print("Test passed")
                
                else:
                    self.first_specimen = None
                    self.flagged = sender.original_memory
                    self.counter = 0
                    print("Test failed")
                    
            elif self.target_function == "xor":
                
                print("Reacting on IO")
            
                i0 = result[0]
                i1 = result[1]
                out = result[2]
            
                print(i0,i1,out)
            
                if out == (~i0 & i1) | (i0 & ~i1):
                    self.counter += 1
                    print("Test passed")
                
                else:
                    self.first_specimen = None
                    self.flagged = sender.original_memory
                    self.counter = 0
                    print("Test failed")
                    
            elif self.target_function == "equ":
                
                print("Reacting on IO")
            
                i0 = result[0]
                i1 = result[1]
                out = result[2]
            
                print(i0,i1,out)
            
                if out == (i0 & i1) | (~i0 & ~i1):
                    self.counter += 1
                    print("Test passed")
                
                else:
                    self.first_specimen = None
                    self.flagged = sender.original_memory
                    self.counter = 0
                    print("Test failed")
                
                    
    def test(self, n = 3000):
        
        test_world = World(1,cm_prob = 0, ins_prob = 0, del_prob = 0, notify_ = True)
        
        test_world.place_custom(self.first_specimen)
        
        test_world.experiment = self
        test_world.output = True
        
        test_world.schedule(n)
        

    # We run the experiment until we have evolved the function that we wanted to evolve
    # If we have correctly evolved such a function, the first_specimen attribute will no longer be None
    def run(self):
        
        i = 0
        while self.first_specimen == None:
            self.world.schedule(1)
            i += 1
            
            if i == 1000:
                print("Min Length: " + str(self.min_len()))
                print("Max Length: " + str(self.max_len()))
                print("Mean Length: " + str(self.mean_len()))
                i = 0
                
            
    def min_len(self):
    
        len_ = 100000
        position = None
    
        for i in range(self.world.pool.shape[0]):
            for j in range(self.world.pool.shape[1]):
                if self.world.pool.get((i,j)) == 0:
                    pass
                else:
                    if len(self.world.pool.get((i,j)).original_memory) < len_:
                        len_ = len(self.world.pool.get((i,j)).original_memory)
                        position = (i,j)
                        
        return len_, position
    
    def max_len(self):
    
        len_ = -1
        position = None
    
        for i in range(self.world.pool.shape[0]):
            for j in range(self.world.pool.shape[1]):
                if self.world.pool.get((i,j)) == 0:
                    pass
                else:
                    if len(self.world.pool.get((i,j)).original_memory) > len_:
                        len_ = len(self.world.pool.get((i,j)).original_memory)
                        position = (i,j)
                        
        return len_, position
    
    def mean_len(self):
    
        sum_ = 0
        count = 0
    
        for i in range(self.world.pool.shape[0]):
            for j in range(self.world.pool.shape[1]):
                if self.world.pool.get((i,j)) == 0:
                    pass
                else:
                    sum_ += len(self.world.pool.get((i,j)).original_memory)
                    count += 1
                        
        return sum_/count