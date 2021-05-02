# A clean implementation of the Avida World simulator

# %%
# Necessary imports:

import numpy as np
import SimpleAvida as SA
from Mediator import Mediator
import random

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
    
    # mask is a helper variable which helps us quickly pull out a 1D list of all
    # the valid populated positions in the world pool
    
    # Default copy mutation probability is 0.0025
    
    def __init__(self, N, replacement_strategy = "kill_oldest", cm_prob = 0.0025, ins_prob = ):

        # Pool() will contain the set of CPUEmulators.
        self.pool = Pool(N, dtype = SA.CPUEmulator)
        
        self.rates = np.zeros((N,N), dtype = int)
        
        self.replacement_strategy = replacement_strategy
        
        self.ages = np.zeros((N,N), dtype = int)
        
        self.mask = np.zeros((N,N), dtype = bool)
        
        self.cm_prob = cm_prob
        
        self.inputs = np.empty((N,N))
        self.inputs[:] = np.nan
        
    # The following method instantiates a default self-replicating organism
    # as a random location in the pool, unless location specified otherwise
    # The location must be a valid tuple
    
    def instantiate_default(self, position = None):
        
        self.instantiate_custom([16, 20, 2, 0, 21, 2, 20, 19, 25, 2, 0, 17, 21, 0, 1], position = position)
        
    # The following method instantiates a custom self-replicating organism
    # as a random location in the pool, unless location specified otherwise
    # The location must be a valid tuple
        
    def instantiate_custom(self, program, position = None):
        
        # Create default program
        default_program = SA.Program(program)
        
        # Create a new emulator
        emulator = SA.CPUEmulator()
        
        # Load self as the emulator's mediator
        emulator.mediator = self
        
        # Set the copy mutation probability as defined in the world
        emulator.mutation_prob = self.cm_prob
        
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
        
        self.rates[position] = 1
        
        # Pull out the age of the organism
        
        self.ages[position] = emulator.age
        
        # Update mask
        
        self.mask[position] = True
        

    # Here the scheduler loop, which runs forever unless told otherwise
    
    def schedule(self, n_loops = None):
        
        if n_loops == None:

            while True:
                
                baseline_rate = self.baseline_rate()
            
                mask = self.mask
            
                emulators = self.pool.get()[mask]
            
                rates = self.rates

                for i in range(emulators.size):
                    
                    n_cycles = int(rates[mask][i] / baseline_rate)

                    for i_cycles in range(n_cycles):
                        
                        emulators[i].execute_instruction()
            
        for i_loops in range(n_loops):

            baseline_rate = self.baseline_rate()
            
            mask = self.mask
            
            emulators = self.pool.get()[mask]
            
            rates = self.rates

            for i in range(emulators.size):
                    
                    n_cycles = int(rates[mask][i] / baseline_rate)

                    for i_cycles in range(n_cycles):
                        
                        emulators[i].execute_instruction()

    # The following method defines which functions are to be called when world is notified 
    # of various events
    
    def notify(self, sender, event, result):
        
        if event == "division":
            
            self.react_on_division(result)

        elif event == "IO_operation":

            self.react_on_IO(sender, result)
            

    # The methods below define how the world reacts to different notifications
    
    # Here how the world reacts upon organism division
    
    def react_on_division(self, result):
        
        # The organism, upon valid division, notifies the world of it using
        # self.mediator.notify(sender = self, event = "division", result = result)

        # Create a program from the result passed from the organism which underwent division
        program = SA.Program(result)
        
        # Create a new emulator and load the resulting program in it
        emulator = SA.CPUEmulator()
        emulator.load_program(program)
        
        # Link self as the new emulator's mediator
        emulator.mediator = self
        
        # Set the copy mutation probability as defined in the world
        emulator.mutation_prob = self.cm_prob
        
        # If there is a free spot put the cell there
        if 0 in self.pool.get():
            
            idx0 = np.where(self.pool.get() == 0)[0][0]
            idx1 = np.where(self.pool.get() == 0)[1][0]
            
            position = (idx0, idx1)
        
        # Otherwise find the oldest emulator and replace it with the newly created one
        
        elif self.replacement_strategy == "kill_oldest":
            
            position = self.oldest_position()
            
        # Put the created emulator in the found position
        
        self.pool.put(emulator, position)
        
        # Put age 0 in the correct position
        
        self.ages[position] = 0
        
        # Update mask
        
        self.mask[position] = True
        
        # Update rates
        
        self.rates[position] = 1
            
    # Here how the world reacts upon an IO operation        

    def react_on_IO(self, sender, result):
        
        # Find the position in the pool where the sender is at:
        
        idx0 = np.where(world.pool.get() == sender)[0][0]
        idx1 = np.where(world.pool.get() == sender)[1][0]
        
        if np.isnan(self.inputs[idx0][idx1]):
            
            pass
        
        else:
            
            if self.inputs[idx0][idx1] == ~result:
                
                print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED NOT\n")
                
                # Doble the organism's metabolic rate
                self.rates[(idx0,idx1)] *= 2

        # A random 32-bit number
        to_input = random.getrandbits(32)
        
        # Put the randomly generated number into the input buffer of the emulator
        sender.cpu.input_buffer.put(to_input)
        
        # Update inputs array
        self.inputs[idx0][idx1] = to_input

    # Helper methods here:
        
    def oldest_position(self):
        
        # Returns the position of the oldest emulator in the pool
        # If there are several such emulators with equal age, returns the first one
        # it encounters
        
        # The ages matrix is only updated when we need it
        
        for i in range(0,self.pool.shape()[0]):
            for j in range(0,self.pool.shape()[1]):
                
                if isinstance(self.pool.get()[i][j], SA.CPUEmulator):
                    self.ages[i][j] = self.pool.get()[i][j].age
        
        idx0 = np.where(self.ages == np.max(self.ages))[0][0]
        idx1 = np.where(self.ages == np.max(self.ages))[1][0]
        
        return (idx0, idx1)
    
    def baseline_rate(self):
        
        # Returns the smallest metabolic rate value present
        
        baseline_rate = np.min(self.rates[self.mask])
        
        return baseline_rate
    
    def get_pool(self):
        
        return self.pool.get()
    
    # A string representation of the world pool

    def __str__(self):
        
        emulators = self.pool.get()[self.mask]
        
        for i in range(emulators.size):

            print("Emulator " + str(i + 1) + ": ")
            print(emulators[i])

        return ""

#%% Testing some stuff

world = World(10)

world.instantiate_default((0,0))
world.instantiate_default((1,0))
world.instantiate_default((9,9))

world.schedule(10000)