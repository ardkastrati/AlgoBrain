# A clean implementation of the Avida World simulator

# %%
# Necessary imports:

import numpy as np
import DigitalOrganism as DO
from Mediator import Mediator
import random

#%% Helper class for breaking nested loops
class BreakIt(Exception): pass

#%% Pool simulates an NxN Petri dish
# Avida organisms live in such a pool

class Pool:

    def __init__(self, N, dtype = None):
        
        if dtype == None:

            self.pool = np.zeros((N,N))
            
        else:
            
            self.pool = np.zeros((N,N), dtype = dtype)
    
    def shape(self):
        
        return self.pool.shape

    def get(self):
        
        return self.pool
    
    def put(self, obj, pos):
        
        self.pool[pos] = obj
    
#%% World is a powerful class which has full knowledge of all of its components

# World regulates everything
# It implements the Mediator abstract interface

class World(Mediator):

    # Pool of size NxN
    
    # Rates contains the metabolic rates of the emulators
    
    # Replacement strategy determines what happens if the pool is full and a
    # new organism is to be born. Per default, the oldest organism in the pool is killed
    
    # Ages keeps track of the ages of the organisms in the corresponding location
    
    
    # Default copy mutation probability is 0.0025
    
    def __init__(self, N, replacement_strategy = "neighborhood", cm_prob = 0.005, ins_prob = 0.05, del_prob = 0.05):

        # Pool() will contain the set of CPUEmulators.
        self.pool = Pool(N, dtype = DO.CPUEmulator)
        
        self.rates = np.zeros((N,N), dtype = int)
        
        self.ages = np.zeros((N,N), dtype = int)
        
        # Inputs is now an array of tuples of integers
        # The first integer is the most recent input
        # The second integer is the second most recent input
        # Initialize to 0. Assume that 0 means that there was no input yet
        # The probability of an input being exactly 0 is 2^-32
        
        self.inputs = np.zeros((N,N), dtype = (np.int64,2))
        
        self.replacement_strategy = replacement_strategy
        
        self.cm_prob = cm_prob
        
        self.ins_prob = ins_prob
        self.del_prob = del_prob

    # The following method instantiates a default self-replicating organism
    # as a random location in the pool, unless location specified otherwise
    # The location must be a valid tuple
    
    # Default as per Avida-ED website and Nature paper. Contains 35 nop-c in the middle
    # In total 50 instructions
    
    def place_default(self, position = None):
        
        self.place_custom([16, 20, 2, 0, 21] + [2]*36 + [20, 19, 25, 2, 0, 17, 21, 0, 1], position = position)
        
    # Default per avida paper, with only 15 instructions
    def place_default_15(self, position = None):
        
        self.place_custom([16, 20, 2, 0, 21, 2, 20, 19, 25, 2, 0, 17, 21, 0, 1], position = position)
        
    # Almost the same as the original default, only initialized with two IO operations
    # before the center nop-c cluster
    def place_def_io(self, position = None):
        
        self.place_custom([16, 20, 2, 0, 21] + [2]*18 + [18,1] + [2]*18 + [20, 19, 25, 2, 0, 17, 21, 0, 1], position = position)
        
    # The following method instantiates a custom self-replicating organism
    # as a random location in the pool, unless location specified otherwise
    # The location must be a valid tuple
        
    def place_custom(self, program, position = None, rate = 1):
        
        # Create program
        default_program = DO.Program(program)
        
        # Create a new emulator
        emulator = DO.CPUEmulator()
        
        # Load self as the emulator's mediator
        emulator.mediator = self
        
        # Set the copy mutation probability as defined in the world
        emulator.mutation_prob = self.cm_prob
        
        # Set the insertion and deletion mutation probabilities as defined in the world
        emulator.ins_prob = self.ins_prob
        emulator.del_prob = self.del_prob
        
        # Load program into emulator
        emulator.load_program(default_program)
        
        # Create random valid position or check if given position valid
        if position == None:
            
            position = (np.random.randint(0, self.pool.shape()[0]), np.random.randint(0, self.pool.shape()[1]))
            
        else:
            
            assert type(position) == tuple, "Given position is not a tuple"
            assert position[0] < self.pool.shape()[0] and position[1] < self.pool.shape()[1], "Positions out of bounds"
            
        # Put the emulator at the given position
        
        self.pool.put(emulator,position)
        
        # Put the emulator rate in the corresponding position
        # The world keeps track of the metabolic rates
        # Per default, upon any organism instantiation, the metabolic rate is 1
        
        self.rates[position] = rate
        
        # Pull out the age of the organism
        
        self.ages[position] = emulator.age
        

    # Here the scheduler loop, which runs forever unless told otherwise
    
    def schedule(self, n_loops = None):
        
        if n_loops == None:
            
            # I want to see how the population is doing every 10k cycles
            
            iterator = 0
            
            while True:
                
                 baseline_rate = self.baseline_rate()
                 iterator += 1
                 
                 if iterator == 5000:
                     # Shows that the whole thing is alive every 5k cycles
                     print("\nStill running")
                     # A sanity check, just making sure that the ages are behaving
                     # ok
                     print(self.ages[:10,:10])
                     iterator = 0
            
                 for i in range(self.pool.shape()[0]):
                     for j in range(self.pool.shape()[1]):
                    
                         if isinstance(self.pool.get()[i][j], DO.CPUEmulator):
                        
                             n_cycles = int(self.rates[i][j] / baseline_rate)
                        
                             for i_cycles in range(n_cycles):
                            
                                 current_emulator = self.pool.get()[i][j]
                            
                                 current_emulator.execute_instruction()
                            
                                 self.ages[i][j] = current_emulator.age
        else:
                                
            for i_loops in range(n_loops):
            
                baseline_rate = self.baseline_rate()
            
                for i in range(self.pool.shape()[0]):
                    for j in range(self.pool.shape()[1]):
                    
                        if isinstance(self.pool.get()[i][j], DO.CPUEmulator):
                        
                            n_cycles = int(self.rates[i][j] / baseline_rate)
                        
                            for i_cycles in range(n_cycles):
                            
                                current_emulator = self.pool.get()[i][j]
                            
                                current_emulator.execute_instruction()
                            
                                self.ages[i][j] = current_emulator.age
            
            print(self.ages)


    # The following method defines which functions are to be called when world is notified 
    # of various events
    
    def notify(self, sender, event, result):
        
        if event == "division":
            
            self.react_on_division(sender, result)

        elif event == "IO_operation":

            self.react_on_IO(sender, result)
            

    # The methods below define how the world reacts to different notifications
    
    # Here how the world reacts upon organism division
    
    def react_on_division(self, sender, result):
        
        idx0 = np.where(self.pool.get() == sender)[0][0]
        idx1 = np.where(self.pool.get() == sender)[1][0]
        
        # The organism, upon valid division, notifies the world of it using
        # self.mediator.notify(sender = self, event = "division", result = result)

        # Create a program from the result passed from the organism which underwent division
        program = DO.Program(result)
        
        # Create a new emulator and load the resulting program in it
        emulator = DO.CPUEmulator()
        emulator.load_program(program)
        
        # Link self as the new emulator's mediator
        emulator.mediator = self
        
        # Set the copy mutation probability as defined in the world
        emulator.mutation_prob = self.cm_prob
        
        # Default replacement strategy
        # Look for free spots in the 1-hop neighborhood of the parent
        # If there is a free spot, put the offspring into any such spot
        # If not, kill the oldest organism in the neighborhood and put offspring there
        # Note that the oldest organism in the neighborhood may be the parent itself
        if self.replacement_strategy == "neighborhood":
            
            # Find the position in the pool where the sender (parent) is at:

            idx0 = np.where(self.pool.get() == sender)[0][0]
            idx1 = np.where(self.pool.get() == sender)[1][0]
            
            width = self.pool.shape()[0]
            height = self.pool.shape()[1]
            
            # The neighborhood of the cell:
            # Iterate over rows max(idx0-1,0) idx0, min(idx0+1, pool height - 1)
            # Iterate over columns max(idx1-1,0), idx1, min(idx1 + 1, pool width - 1)
            
            # Breaking out of nested loops: 
            # https://stackoverflow.com/questions/653509/breaking-out-of-nested-loops
            
            position = None
            
            try:
                for i in range(max(idx0-1, 0), min(idx0+2, width)):
                    for j in range(max(idx1-1, 0), min(idx1+2, height)):  
                        if self.pool.get()[i][j] == 0:
                            position = (i,j)
                            raise BreakIt
                            
            except BreakIt:
                pass
            
            # If no free spot in the neighborhood was found, replace oldest cell in the neighborhood, excluding self
            if position == None:
                
                oldest = 0
                
                for i in range(max(idx0-1, 0), min(idx0+2, width)):
                        for j in range(max(idx1-1, 0), min(idx1+2, height)):  
                            if self.ages[i][j] >= oldest:
                                if i == idx0 and j == idx1:
                                    continue
                                else:
                                    oldest = self.ages[i][j]
                                    position = (i,j)

        # Define kill_oldest replacement strategy as:
        # If there is a free spot in the pool, put child there
        # Otherwise, kill oldest organism in the pool and put child there
        
        elif self.replacement_strategy == "kill_oldest":
            
            # If there is a free spot put the cell there
            if 0 in self.pool.get():
            
                idx0 = np.where(self.pool.get() == 0)[0][0]
                idx1 = np.where(self.pool.get() == 0)[1][0]
            
                position = (idx0, idx1)
        
            else:
            
                position = self.oldest_position()               
            
        # Put the created emulator in the found position
        
        self.pool.put(emulator, position)
        
        # Put age 0 in the correct position
        
        self.ages[position] = 0
        
        # Update rates
        
        self.rates[position] = sender.child_rate
        
        # Set input to none
        
        self.inputs[position] = (0,0)

    # Here how the world reacts upon an IO operation        

    def react_on_IO(self, sender, result):
        # Find the position in the pool where the sender is at:

        idx0 = np.where(self.pool.get() == sender)[0][0]
        idx1 = np.where(self.pool.get() == sender)[1][0]
        
        # If the most recent input is none, do nothing
        if self.inputs[idx0][idx1][0] == 0:
        
            pass
        
        # If the most recent input isn't none, but the second most recent is, check if not was computed
        elif self.inputs[idx0][idx1][0] != 0 and self.inputs[idx0][idx1][1] == 0:
            
            if self.inputs[idx0][idx1][0] == ~result:
                
                # Save input, result and the organism that computed it
                self.input = self.inputs[idx0][idx1][0]
                self.winner = self.get((idx0,idx1))
                self.result = result
                
                # Notify us about what happened
                print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED NOT\nINPUT:  " + str(bin(self.input & 0xffffffff)[2:]) + "\nOUTPUT: " + str(bin(self.result & 0xffffffff)[2:]))
                
                # Slow down with those mutations now
                # It takes a while to slow down to stable 0.005
                if self.cm_prob > 0.005:
                    self.cm_prob *= 0.999
                
                # Check whether the organism has computed not previously
                # If not, reward.
                if sender.fun_not == False:
                    sender.fun_not = True
                    sender.child_rate *= 2
                
                # If yes, ignore
                else:
                    pass
        
        # If the two most recent inputs aren't none, check whether a function of the two most recent inputs was computed
        elif self.inputs[idx0][idx1][0] != 0 and self.inputs[idx0][idx1][1] != 0:
            
            # If a NOT was computed
            
            if result == ~self.inputs[idx0][idx1][0]:
                
                # Save input, result and the organism that computed it
                input_ = self.inputs[idx0][idx1]
                
                # Notify us about what happened
                print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED NOT\nINPUT:  " + str(str(bin(input_[0] & 0xffffffff)[2:])) + "\nOUTPUT: " + str(bin(result & 0xffffffff)[2:]))
                
                # Slow down with those mutations now
                # It takes a while to slow down to stable 0.005
                if self.cm_prob > 0.005:
                    self.cm_prob *= 0.999
                
                # Check whether the organism has computed not previously
                # If not, reward.
                if sender.fun_not == False:
                    sender.fun_not = True
                    sender.child_rate *= 2
                
                # If yes, ignore
                else:
                    pass
            
            # If a NAND was computed
            elif result == ~(self.inputs[idx0][idx1][0] & self.inputs[idx0][idx1][1]):
                
                # Save input, result and the organism that computed it
                self.input = self.inputs[idx0][idx1]
                self.winner = self.get((idx0,idx1))
                self.result = result
                
                input_ = self.inputs[idx0][idx1]
                
                # Notify us about what happened
                print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED NAND\nINPUT 1: " + str(str(bin(input_[0] & 0xffffffff)[2:])) + "\nINPUT 2: " + str(str(bin(input_[1] & 0xffffffff)[2:])) + "\nOUTPUT:  " + str(bin(result & 0xffffffff)[2:]))
                
                # Slow down with those mutations now
                # It takes a while to slow down to stable 0.005
                if self.cm_prob > 0.005:
                    self.cm_prob *= 0.999
                
                # Check whether the organism has computed nand previously
                # If not, reward.
                if sender.fun_nand == False:
                    sender.fun_nand = True
                    sender.child_rate *= 2
                
                # If yes, ignore
                else:
                    pass
                
            # If an AND was computed
            elif result == self.inputs[idx0][idx1][0] & self.inputs[idx0][idx1][1]:
                
                # Save input, result and the organism that computed it
                self.input = self.inputs[idx0][idx1]
                self.winner = self.get((idx0,idx1))
                self.result = result
                
                # Notify us about what happened
                print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED AND\nINPUT: " + str(self.input) + "\nOUTPUT: " + str(self.result))
                
                # Slow down with those mutations now
                # It takes a while to slow down to stable 0.005
                if self.cm_prob > 0.005:
                    self.cm_prob *= 0.999
                
                # Check whether the organism has computed nand previously
                # If not, reward.
                if sender.fun_and == False:
                    sender.fun_and = True
                    sender.child_rate *= 4
                
                # If yes, ignore
                else:
                    pass
                
            # If an OR_N was computed
            elif result == self.inputs[idx0][idx1][0] | ~self.inputs[idx0][idx1][1] or result == ~self.inputs[idx0][idx1][0] | self.inputs[idx0][idx1][1]:
                
                # Save input, result and the organism that computed it
                self.input = self.inputs[idx0][idx1]
                self.winner = self.get((idx0,idx1))
                self.result = result
                
                # Notify us about what happened
                print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED OR_N\nINPUT: " + str(self.input) + "\nOUTPUT: " + str(self.result))
                
                # Slow down with those mutations now
                # It takes a while to slow down to stable 0.005
                if self.cm_prob > 0.005:
                    self.cm_prob *= 0.999
                
                # Check whether the organism has computed nand previously
                # If not, reward.
                if sender.fun_or_n == False:
                    sender.fun_or_n = True
                    sender.child_rate *= 4
                
                # If yes, ignore
                else:
                    pass
                
            # If an OR was computed
            elif result == self.inputs[idx0][idx1][0] | self.inputs[idx0][idx1][1]:
                
                # Save input, result and the organism that computed it
                self.input = self.inputs[idx0][idx1]
                self.winner = self.get((idx0,idx1))
                self.result = result
                
                # Notify us about what happened
                print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED OR\nINPUT: " + str(self.input) + "\nOUTPUT: " + str(self.result))
                
                # Slow down with those mutations now
                # It takes a while to slow down to stable 0.005
                if self.cm_prob > 0.005:
                    self.cm_prob *= 0.999
                
                # Check whether the organism has computed nand previously
                # If not, reward.
                if sender.fun_or == False:
                    sender.fun_or = True
                    sender.child_rate *= 8
                
                # If yes, ignore
                else:
                    pass
                
            # If an AND_N was computed
            elif result == self.inputs[idx0][idx1][0] & ~self.inputs[idx0][idx1][1] or result == ~self.inputs[idx0][idx1][0] & self.inputs[idx0][idx1][1]:
                
                # Save input, result and the organism that computed it
                self.input = self.inputs[idx0][idx1]
                self.winner = self.get((idx0,idx1))
                self.result = result
                
                # Notify us about what happened
                print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED AND_N\nINPUT: " + str(self.input) + "\nOUTPUT: " + str(self.result))
                
                # Slow down with those mutations now
                # It takes a while to slow down to stable 0.005
                if self.cm_prob > 0.005:
                    self.cm_prob *= 0.999
                
                # Check whether the organism has computed nand previously
                # If not, reward.
                if sender.fun_and_n == False:
                    sender.fun_and_n = True
                    sender.child_rate *= 8
                
                # If yes, ignore
                else:
                    pass
                
            # If a NOR was computed
            elif result == ~(self.inputs[idx0][idx1][0] | self.inputs[idx0][idx1][1]):
                
                # Save input, result and the organism that computed it
                self.input = self.inputs[idx0][idx1]
                self.winner = self.get((idx0,idx1))
                self.result = result
                
                # Notify us about what happened
                print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED NOR\nINPUT: " + str(self.input) + "\nOUTPUT: " + str(self.result))
                
                # Slow down with those mutations now
                # It takes a while to slow down to stable 0.005
                if self.cm_prob > 0.005:
                    self.cm_prob *= 0.999
                
                # Check whether the organism has computed nand previously
                # If not, reward.
                if sender.fun_nor == False:
                    sender.fun_nor = True
                    sender.child_rate *= 16
                
                # If yes, ignore
                else:
                    pass
                
            # If an XOR was computed:
            elif result == self.inputs[idx0][idx1][0] ^ self.inputs[idx0][idx1][1]:
                
                # Save input, result and the organism that computed it
                input = self.inputs[idx0][idx1]
                
                # Notify us about what happened
                print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED NOR\nINPUT: " + str(input) + "\nOUTPUT: " + str(result))
                
                # Slow down with those mutations now
                # It takes a while to slow down to stable 0.005
                if self.cm_prob > 0.005:
                    self.cm_prob *= 0.999
                
                # Check whether the organism has computed xor previously
                # If not, reward.
                if sender.fun_xor == False:
                    sender.fun_xor = True
                    sender.child_rate *= 16
                
                # If yes, ignore
                else:
                    pass
            
            
            """
            # If EQU was computed:
            # NOTE: I only want to reward the organisms
            elif result == (self.inputs[idx0][idx1][0] == self.inputs[idx0][idx1][1]) and result == 1:
                
                # Save input, result and the organism that computed it
                input = self.inputs[idx0][idx1]
                
                # Notify us about what happened
                print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED EQU\nINPUT: " + str(input) + "\nOUTPUT: " + str(result))
                
                # Slow down with those mutations now
                self.cm_prob = 0.005
                
                # Check whether the organism has computed equ previously
                # If not, reward.
                if sender.fun_equ == False:
                    sender.fun_equ = True
                    sender.child_rate *= 32
                
                # If yes, ignore
                else:
                    pass
                
            """
     
        # A random 32-bit number
        to_input = random.getrandbits(32)
        
        # Put the randomly generated number into the input buffer of the emulator
        sender.cpu.input_buffer.put(to_input)
        
        # Update inputs array
        # Old newest input gets placed into position 1
        # New input gets placed into position 0
        self.inputs[idx0][idx1][1] = self.inputs[idx0][idx1][0]
        self.inputs[idx0][idx1][0] = to_input

    # Helper methods here:
        
    def oldest_position(self):
        
        # Returns the position of the oldest emulator in the pool
        # If there are several such emulators with equal age, returns the first one
        # it encounters
        
        for i in range(0,self.pool.shape()[0]):
            for j in range(0,self.pool.shape()[1]):
                
                if isinstance(self.pool.get()[i][j], DO.CPUEmulator):
                    self.ages[i][j] = self.pool.get()[i][j].age
        
        idx0 = np.where(self.ages == np.max(self.ages))[0][0]
        idx1 = np.where(self.ages == np.max(self.ages))[1][0]
        
        return (idx0, idx1)
    
    def baseline_rate(self):
        
        # Returns the smallest metabolic rate value present
        
        baseline_rate = np.min(self.rates[self.rates > 0])
        
        return baseline_rate
    
    def get_pool(self):
        
        return self.pool.get()
    
    # Returns the emulator at the given position
    
    def get(self,position):
        
        return self.pool.get()[position]

    # A string representation of the world pool

    def __str__(self):
        
        emulators = self.pool.get()[self.pool.get() != 0]
         
        for i in range(emulators.size):

            print("Emulator " + str(i + 1) + ": ")
            print(emulators[i])

        return ""

#%% Testing some stuff


# First argument is world size
# cm_prob is copy mutation probability
# ins_prob and del_prob are insertion and deletion probabilities
world = World(66,replacement_strategy="neighborhood",cm_prob = 0.01, ins_prob = 0.005, del_prob = 0.005)

# Placing several default organisms at different positions in the pool

world.place_def_io((0,0))
world.place_def_io((0,32))
world.place_def_io((0,65))
world.place_def_io((32,0))
world.place_def_io((32,32))
world.place_def_io((32,65))
world.place_def_io((65,0))
world.place_def_io((65,32))
world.place_def_io((65,65))


world.schedule()

#%%

# World claims these organisms computed NOT:
    
not0 = [16, 20, 2, 0, 21, 2, 2, 12, 14, 18, 13, 16, 2, 5, 24, 25, 13, 2, 7, 19, 2, 21, 23, 2, 23, 2, 2, 17, 2, 17, 2, 8, 2, 2, 16, 2, 6, 2, 6, 7, 5, 25, 19, 25, 2, 0, 17, 21, 0, 1]

not1 = [16, 20, 2, 0, 21, 2, 3, 15, 2, 2, 2, 2, 21, 2, 2, 2, 2, 2, 2, 18, 15, 2, 2, 24, 25, 2, 22, 2, 2, 2, 18, 2, 2, 2, 2, 2, 2, 2, 2, 23, 2, 20, 19, 23, 2, 0, 17, 21, 0, 1]

not2 = [16, 20, 2, 0, 21, 2, 16, 13, 25, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 10, 2, 7, 2, 2, 2, 23, 4, 2, 6, 18, 15, 2, 2, 15, 2, 2, 18, 2, 2, 20, 19, 25, 2, 0, 17, 21, 0, 1]

#%%

