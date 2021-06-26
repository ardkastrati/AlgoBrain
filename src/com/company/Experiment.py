#%% Imports:
    
import numpy as np
    
# Add Backend to path
import sys
#sys.path.append('C:/Users/eeveetza/Documents/GitHub/AlgoBrain/src/com/company/Backend')
sys.path.append('C:/Users/eeveetza/Documents/GitHub/AlgoBrain_local/Backend')
#sys.path.append('C:/Users/Tbuob/OneDrive/Dokumente/GitHub/AlgoBrain/src/com/company/Backend')

from Environment import World
from Mediator import Mediator

import matplotlib.pyplot as plt

#%%
class Experiment(Mediator):
    
    def __init__(self, start_organism = "default", target_function = "equ", N=30,cm_prob = 0.05, ins_prob = 0.05, del_prob = 0.05, notify_ = False, stat_cycles = 200,\
                 instruction_set = "default"):
        
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
        
        # Set the world's instruction set. This information is to propagate further to the organisms.
        # Defines the range of instructions which an organism may acquire upon a mutation
        self.world.instruction_set = instruction_set
        
        # A helper attribute, to flag organisms which reported a function but can't actually solve it
        self.flagged = None
        
        # Helper attributes
        self.counter = 0
        self.stat_cycles = stat_cycles
        self.update = 0
        self.N = N
        
        if self.start_organism == "default":
            self.world.fill("default")
            
        elif self.start_organism == "default_long":
            self.world.fill([16, 20, 2, 0, 21] + [2]*76 + [20, 19, 25, 2, 0, 17, 21, 0, 1])
            
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
            
        elif self.start_organism == "xor":
            self.world.fill([16, 20, 2, 0, 21] + [2] + [18, 0, 18, 2, 7, 0, 7, 2, 8, 14, 2, 12, 2, 7, 0, 6, 1, 6, 0, 15,2, 6, 1, 7, 2, 8, 6, 0, 6, 2, 14, 2, 12, 2, 7, 0, 6, 1, 6, 0, 15, 2, 8, 6, 1, 15, 0, 18, 0]\
                            + [6, 0, 6, 1, 6, 2] + [20, 19, 25, 2, 0, 17, 21, 0, 1])
            
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
            
            for i in range(10):
                test_world = World(1,cm_prob = 0, ins_prob = 0, del_prob = 0)
        
                test_world.place_custom(result)
        
                test_world.experiment = self
                test_world.output = True
            
                test_world.schedule(1000)
            
            # If the target function was output less than 5 times in 5000 cycles,
            # ignore the organism
            if self.counter < 5:
                self.first_specimen = None
            else:
                self.first_specimen = sender.original_memory
                
            self.counter = 0
        
    def react_on_function_io(self,sender,result):
        
        i0 = result[0]
        i1 = result[1]
        out = result[2]
        
        # Filtering outputs
        if -7 < out < 7:
            pass
        elif i0 == ~i1:
            pass
        elif ~i0 == i1:
            pass
        elif i0 & ~i1 == i0:
            pass
        elif i0 & i1 == i1:
            pass
        elif i0 & ~i1 == i1:
            pass
        elif ~i0 & i1 == i0:
            pass
        elif i0 | i1 == i0:
            pass
        elif i0 | i1 == i1:
            pass
        elif i0 | ~i1 == i0:
            pass
        elif i0 | ~i1 == i1:
            pass
        elif ~i0 | i1 == i0:
            pass
        elif ~i0 | i1 == i1:
            pass
        
        else:
            if self.target_function == "nand":
            
                print("Reacting on IO")
            
                i0 = result[0]
                i1 = result[1]
                out = result[2]
            
                print(i0,i1,out)

                if out == ~(i0 & i1):
                    self.counter += 1
                    print("Test passed")
                
                """
                # If an organism that reported NAND failed even a single one of these tests the sender gets flagged
                # and isn't allowed to be tested any longer
                else:
                    self.first_specimen = None
                    self.flagged = sender.original_memory
                    self.counter = 0
                    print("Test failed")
                """
                    
            elif self.target_function == "not":
                
                print("Reacting on IO")
            
                i0 = result[0]
                i1 = result[1]
                out = result[2]
            
                print(i0,i1,out)
            
                if out == ~i0:
                    self.counter += 1
                    print("Test passed")
                
                """
                else:
                    self.first_specimen = None
                    self.flagged = sender.original_memory
                    self.counter = 0
                    print("Test failed")
                """
                    
            elif self.target_function == "and":
                
                print("Reacting on IO")
            
                i0 = result[0]
                i1 = result[1]
                out = result[2]
            
                print(i0,i1,out)
            
                if out == i0 & i1:
                    self.counter += 1
                    print("Test passed")
                    
                """
                else:
                    self.first_specimen = None
                    self.flagged = sender.original_memory
                    self.counter = 0
                    print("Test failed")
                """
                    
            elif self.target_function == "or":
                
                print("Reacting on IO")
            
                i0 = result[0]
                i1 = result[1]
                out = result[2]
            
                print(i0,i1,out)
            
                if out == i0 | i1:
                    self.counter += 1
                    print("Test passed")
                
                """
                else:
                    self.first_specimen = None
                    self.flagged = sender.original_memory
                    self.counter = 0
                    print("Test failed")
                """
                
            elif self.target_function == "and_n":
                
                print("Reacting on IO")
            
                i0 = result[0]
                i1 = result[1]
                out = result[2]
            
                print(i0,i1,out)
            
                if out == i0 & ~i1 or out == ~i0 & i1:
                    self.counter += 1
                    print("Test passed")
                
                """
                else:
                    self.first_specimen = None
                    self.flagged = sender.original_memory
                    self.counter = 0
                    print("Test failed")
                """
                
            elif self.target_function == "nor":
                
                print("Reacting on IO")
            
                i0 = result[0]
                i1 = result[1]
                out = result[2]
            
                print(i0,i1,out)
            
                if out == ~i0 & ~i1:
                    self.counter += 1
                    print("Test passed")
                
                """
                else:
                    self.first_specimen = None
                    self.flagged = sender.original_memory
                    self.counter = 0
                    print("Test failed")
                """
                
            elif self.target_function == "xor":
                
                print("Reacting on IO")
            
                i0 = result[0]
                i1 = result[1]
                out = result[2]
            
                print(i0,i1,out)
            
                if out == (~i0 & i1) | (i0 & ~i1):
                    self.counter += 1
                    print("Test passed")
                
                """
                else:
                    self.first_specimen = None
                    self.flagged = sender.original_memory
                    self.counter = 0
                    print("Test failed")
                """
                    
            elif self.target_function == "equ":
                
                print("Reacting on IO")
            
                i0 = result[0]
                i1 = result[1]
                out = result[2]
            
                print(i0,i1,out)
            
                if out == (i0 & i1) | (~i0 & ~i1):
                    self.counter += 1
                    print("Test passed")
                
                """
                else:
                    self.first_specimen = None
                    self.flagged = sender.original_memory
                    self.counter = 0
                    print("Test failed")
                """
                    
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
            
            # When on average each emulator has executed 30 instructions, increase the number of updates
            if self.world.executions >= 30 * (self.N ** 2):
                self.update += 1
                self.world.executions = 0
            
            i += 1
            
            if i == self.stat_cycles:
                
                print("\n")
                print("UPDATE: " + str(self.update))
                self.display_statistics()
                
                #print(self.world.rates)
                
                #plt.imshow(self.world.rates)
                #plt.colorbar()
                #plt.show()
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
    
    def count_functions(self):
        
        # Returns the number of organisms reported to be able to compute different
        # boolean functions
        
        count_not = 0
        count_nand = 0
        count_and = 0
        count_or_n = 0
        count_or = 0
        count_and_n = 0
        count_nor = 0
        count_xor = 0
        count_equ = 0
        
        for i in range(self.world.pool.shape[0]):
            for j in range(self.world.pool.shape[1]):
                if self.world.pool.get((i,j)).fun_not:
                    count_not += 1
                if self.world.pool.get((i,j)).fun_nand:
                    count_nand += 1
                if self.world.pool.get((i,j)).fun_and:
                    count_and += 1
                if self.world.pool.get((i,j)).fun_or_n:
                    count_or_n += 1
                if self.world.pool.get((i,j)).fun_or:
                    count_or += 1
                if self.world.pool.get((i,j)).fun_and_n:
                    count_and_n += 1
                if self.world.pool.get((i,j)).fun_nor:
                    count_nor += 1
                if self.world.pool.get((i,j)).fun_xor:
                    count_xor += 1
                if self.world.pool.get((i,j)).fun_equ:
                    count_equ += 1
        
        print("NOT: " + str(count_not))
        print("NAND: " + str(count_nand))
        print("AND: " + str(count_and))
        print("OR_N: " + str(count_or_n))
        print("OR: " + str(count_or))
        print("AND_N: " + str(count_and_n))
        print("NOR: " + str(count_nor))
        print("XOR: " + str(count_xor))
        print("EQU: " + str(count_equ))
        
    def display_statistics(self):
        
        """
        Merges all of the above pool statistics functions into one
        
        Efficiency
        """
        
        min_len = 100000
        position_min = None
        
        max_len = -1
        position_max = None
        
        sum_ = 0
        count = 0
        
        count_not = 0
        count_nand = 0
        count_and = 0
        count_or_n = 0
        count_or = 0
        count_and_n = 0
        count_nor = 0
        count_xor = 0
        count_equ = 0
    
        for i in range(self.world.pool.shape[0]):
            for j in range(self.world.pool.shape[1]):
                if self.world.pool.get((i,j)) == 0:
                    pass
                else:
                    
                    # Computed functions
                    if self.world.pool.get((i,j)).fun_not:
                        count_not += 1
                    if self.world.pool.get((i,j)).fun_nand:
                        count_nand += 1
                    if self.world.pool.get((i,j)).fun_and:
                        count_and += 1
                    if self.world.pool.get((i,j)).fun_or_n:
                        count_or_n += 1
                    if self.world.pool.get((i,j)).fun_or:
                        count_or += 1
                    if self.world.pool.get((i,j)).fun_and_n:
                        count_and_n += 1
                    if self.world.pool.get((i,j)).fun_nor:
                        count_nor += 1
                    if self.world.pool.get((i,j)).fun_xor:
                        count_xor += 1
                    if self.world.pool.get((i,j)).fun_equ:
                        count_equ += 1
                        
                    # Minimum length and its position
                    if len(self.world.pool.get((i,j)).original_memory) < min_len:
                        min_len = len(self.world.pool.get((i,j)).original_memory)
                        position_min = (i,j)
                        
                    # Max length and its position
                    if len(self.world.pool.get((i,j)).original_memory) > max_len:
                        max_len = len(self.world.pool.get((i,j)).original_memory)
                        position_max = (i,j)
                        
                    # Mean length calculation
                    sum_ += len(self.world.pool.get((i,j)).original_memory)
                    count += 1
                
        mean_len = sum_/count

        print("Min Length: " + str((min_len,position_min)))
        print("Max Length: " + str((max_len,position_max)))
        print("Mean Length: " + str(mean_len))
        print("Min Rate: " + str(np.min(self.world.rates)))
        print("Max Rate: " + str(np.max(self.world.rates)))
        print("Mean Rate: " + str(np.mean(self.world.rates)))
        print("Max Age: " + str(np.max(self.world.ages)))
        print("Mean Age: " + str(np.mean(self.world.ages)))
        print("NOT: " + str(count_not))
        print("NAND: " + str(count_nand))
        print("AND: " + str(count_and))
        print("OR_N: " + str(count_or_n))
        print("OR: " + str(count_or))
        print("AND_N: " + str(count_and_n))
        print("NOR: " + str(count_nor))
        print("XOR: " + str(count_xor))
        print("EQU: " + str(count_equ))
