# -*- coding: utf-8 -*-.
"""
Created on Fri Mar 26 17:40:52 2021

@author: Tbuob
"""
import numpy as np
import Standardprogram as stp
import SimpleAvida as SA
"""Cell == Programm!"""
"""Thinking about how to implement the Avida-World"""
#%%
"""Class World is the AvidaWorld, how big it is, calls the cpuemulator, counts 
the time the cells are alive, gives them resources
"""


#%%

# We need to think about how to abstract away the programs and emulators
# The World doesn't need to know all of the implementation details
# Well, we already have the abstraction in a way. It offers methods
# load_program(Program) and execute_program()

# The replication process still doesn't fully make sense to me

# Also, we need to change the execute_program function to make the organisms
# run quasi-parallel. Therefore, execute_program should instead be 
# execute_instruction, and the scheduler will forever run execute_instruction()
# for each organism in its CPUEmulator pool

# The Scheduler needs access to each of the CPUEmulators in the World pool

# 



# A separate class for the Avida Scheduler

# "The Scheduler divides time up from the real CPU such that these virtual CPUs
# execute in a simulated parallel fashion"

# For the beginning, let's implement a scheduler that will have all virtual CPUs
# run at the same speed


class Scheduler:
    pass

#%% 

# Let's define a separate class for the organism pool.
# Who knows what advantages this may bring us in the future

# The Pool obviously has to have a predefined defined size. Call it N.

class Pool:
    
    def __init__(self, N):
        
        # Just a list of length N
        self.pool = [0 for element in range(0,N)]

    
class World:
    
    # N stands for the number of cells, as per reference paper
    def __init__(self,N):
        
        self.pool = Pool(N)
        
        self.scheduler = Scheduler()
        
    
    """How many cells can be alive at the same time"""
    def Worldsize(size):
        """Rather than having an nxn array, maybe it's easier to have a list"""
        world = np.zeros([size,size])
        
    #TODO
        pass
    def Place_Cell(self,size,world):
        self.world = world
        a = np.random.randint(0,size)
        b = np.random.randint(0,size)
        #Place Cell into our matrix from which we know, what places
        #are full and which places are not. Important for replication
        world[a,b]=1
        temp = stp.startprogram(a,b)
        SA.cpuemulator(temp)
        
        
        
        
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
    
        