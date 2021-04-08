# -*- coding: utf-8 -*-.
"""
Created on Fri Mar 26 17:40:52 2021

@author: Tbuob
"""

import numpy as np
import SimpleAvida as SA

"""Cell == Programm!"""
"""Thinking about how to implement the Avida-World"""
#%%
"""Class World is the AvidaWorld, how big it is, calls the cpuemulator, counts 
the time the cells are alive, gives them resources
"""

#%% 

# Let's define a separate class for the organism pool.
# Who knows what advantages this may bring us in the future

# The Pool obviously has to have a predefined defined size. Call it N.

class Pool:
    
    def __init__(self, N):
        
        # Just a list of length N
        self.pool = [0 for element in range(0,N)]
        
    def put(self, emulator, position = "none"):
        
        # If no position specified, put emulator at random position in the pool
        if position == "none":
            idx = np.random.randint(0,len(self.pool))
        else:
            idx = position
        self.pool[idx] = emulator
        
    def size(self):
        return len(self.pool)
    
    def get(self):
        return self.pool
    
    


#%%


# The class World

# Has to have a pool of CPUEmulators. In the beginning only one,
# the default self-replicating organism as per the Avida paper

# Has to have a scheduler. The scheduler runs the instructions of the organisms
# in the pool in a quasi-parallel fashion

# For the beginning, implement the following:
# A scheduler that will run one single predefined program once

class World:
    
    # N stands for the number of cells, as per reference paper
    def __init__(self,N):
        
        # Pool() will contain the set of CPUEmulators.
        self.pool = Pool(N)
    
    """How many cells can be alive at the same time"""
    def Worldsize(size):
        """Rather than having an nxn array, maybe it's easier to have a list"""
        world = np.zeros([size,size])
        

    
    # Let metabolic rate in the emulator stand for how many cycles it has
    # available for it in one scheduler iteration
    
    # Scheduler structure:
    # An infinite loop:
        # A loop over all the emulators:
            # In each iteration in the loop over emulators, execute
            # emulator.metabolic_rate.get() many instructions
            
    # Let's make that infinite loop just, say, 52 iterations for now.
    # Exactly the number of cycles needed for self-replication

    
    def schedule(self):
        
        emulators = self.pool.get()
        
        for i in range(0,104):
        
            for emulator in emulators:
                
                if not isinstance(emulator, SA.CPUEmulator):
                    continue
                
                else:
                    
                    # Each emulator executes its metabolic_rate many instructions.
                    
                    rate = emulator.metabolic_rate.get()
                    
                    while rate > 0:
                    
                        # If the next instruction to execute is HDivide:
                            if isinstance(emulator.memory.get(emulator.instr_pointer.get()), SA.InstructionHDivide):
                        
                                # Grab the returned program,
                                # pack it into a CPUEmulator
                                
                                program = SA.Program(emulator.execute_instruction())
                                emulator = SA.CPUEmulator()
                                emulator.load_program(program)
                                
                                # Put the new emulator in the first free cell
                                # If no free cells, kill the oldest organism and put it there
                                
                                # Can also implement this functionality in the pool.put() function
                                
                                if 0 in self.pool.get():
                                    self.place_cell(emulator,self.pool.get().index(0))
                                    
                                else:
                                    
                                    # Find the oldest emulator
                                    
                                    oldest = 0
                                    for emulator in self.pool.get():
                                        age = emulator.age
                                        if age > oldest:
                                            oldest = emulator
                                            
                                    # Replace the oldest emulator with the newly constructed one
                                    
                                    self.place_cell(emulator,self.pool.get().index(oldest))
                                
                            
                            # Otherwise, just execute as usual
                            else: 
                                
                                emulator.execute_instruction()
                                
                            rate -= 1

        
        
    def __str__(self):
        
        emulators = self.pool.get()
        
        for i in range(0,len(emulators)):
            
            if emulators[i] == 0:
                continue
            else:
                print("Emulator " + str(i) + ": ")
                print(emulators[i])
        
        return ""
            
        
    def place_cell(self,emulator,position = "none"):
        self.pool.put(emulator,position)
    
    """def Place_Cell(self,size,world):
        self.world = world
        a = np.random.randint(0,size)
        b = np.random.randint(0,size)
        #Place Cell into our matrix from which we know, what places
        #are full and which places are not. Important for replication
        world[a,b]=1
        temp = stp.startprogram(a,b)
        SA.cpuemulator(temp)
        
    """
        
        
        
        
    """Call the function"""
    def Functioncall(instructionlist):
    #TODO    
        pass 
    """kill the cell after a certain amount of time"""
    def Killswitch(time,cell):
    #TODO
        pass
    """call the h-divide and h-allocate function and let the parent cell give
    birth to a new programm"""
    def Replication(cell):
    #TODO
        pass
  #%%
"""Class mutation is responsible for every mutation factor of our programms 
when they are replicating.
"""  
class Mutation:
    def __init__(self,time,emulator,factor):
        self.emulator = emulator
        self.time = time
        self.mutationfactor = factor
        
    def mutation(cell):
        #TODO
        pass
    
 #%% 
"""Efficiency is for the amount of instructions a programm gets during a clockcylce
Therefore, a more fit organism can do more in the same time"""  
class Efficiency:
    def __init__(self,value=0):
        self.value = value
    def raise_factor(self,rfactor):
        self.value += rfactor
    def lower_factor(self,lfactor):
        self.value += lfactor
        
#%%
"""Class for the input that we send to the world, ie. what we want our programms
to do """
class Input:
    
    def init__(self,emulator):
        self.emulator = emulator
        

#%%

"""A DEMONSTRATION OF SELF-REPLICATION:"""

# The default self-replicating program
p = SA.Program([16,20,2,0,21,2,20,19,25,2,0,17,21,0,1])

# A world with a 4-slot pool
world = World(4)

# Manually creating the first CPUEmulator
emulator = SA.CPUEmulator()

# Loading the self-replicating program into the first emulator
emulator.load_program(p)

# Placing the emulator into a random position in the world
world.place_cell(emulator)

# Running it for 104 cycles (hard coded atm, for testing purposes)
world.schedule()

# Showing the resulting World Emulator Pool
print(world)