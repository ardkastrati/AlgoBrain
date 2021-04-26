"""
Mediator pseudocode

interface Mediator:
    
    method notify(sender, event)
    
class World implements Mediator:
    
    method notify(sender, event):
        
        if sender is an emulator and event is Hdivide:
            
            create a new emulator
            
            pack in the result program in it
            
            put the result program in the pool
            
CPUEMulator should implement Mediator

In execute_instruction(), if the instruction to execute is HDivide,
the CPUEmulator should notify()
"""

#%%

from abc import ABC


#%% The Mediator Interface

# A core part of the Mediator Design Pattern for reducing coupling between
# various components in our system.

# As of now, its purpose is to reduce coupling between the scheduler, pool
# and CPUEmulator upon executing the HDivide instruction

# It will grow a lot over time.
# We have to be careful not to have it evolve into a god-object

class Mediator(ABC):
    
    # Used by different concrete classes to notify the world of any relevant events
    def notify(self,sender,event,result = 0):
        pass    