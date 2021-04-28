# %%
# Necessary imports:

import numpy as np
import SimpleAvida as SA
from Mediator import Mediator
from abc import ABC


# %% The Organism Pool Class

# The pool is a list of tuples. Each tuple contains in its first position
# the CPUEmulator itself and in its second position the CPUEmulator's metabolic rate

# Maybe the world should be the one managing the pool fully

# As in, the pool doesn't need to know that emulator has a metabolic_rate.get() method

# Let's have the world act as mediator between SimpleAvida, Pool and Scheduler
# Keep the implementations of SA,Pool and Scheduler separate

class Pool:

    def __init__(self, N):

        # A list of tuples of length N
        # The first element in the tuple is the CPUEmulator
        # The second element in the tuple is its associated metabolic rate
        self.pool = [(0, 0) for element in range(0, N)]

    def put(self, emulator, position="none"):

        # If no position specified, put emulator at random position in the pool
        if position == "none":
            idx = np.random.randint(0, len(self.pool))
        else:
            idx = position

        self.pool[idx] = (emulator, emulator.metabolic_rate.get())

    def size(self):
        return len(self.pool)

    def get(self):
        return self.pool

    def get_emulators(self):
        return [emulator for (emulator, rate) in self.pool]

    def get_rates(self):
        return [rate for (emulator, rate) in self.pool]

    def get_baseline(self):
        return min([rate for (emulator, rate) in self.pool if rate > 0])


# %% The Scheduler Class

# The Scheduler should have access to the Pool of the World
# I think It's necessary to couple the Scheduler to the World
# The World should still be the one containing the CPUEmulator pool
# The Scheduler can access this Pool and run the CPUEmulators in it quasi-parallel

class Scheduler:

    def __init__(self, world):
        self.pool = world.pool

    def schedule(self, N=201):

        pool = self.pool.get()

        for i in range(0, N):

            baseline_rate = self.pool.get_baseline()

            for (emulator, rate) in pool:

                if emulator == 0:
                    continue

                else:

                    temp = int(rate / baseline_rate)

                    while temp > 0:
                        emulator.execute_instruction()

                        temp -= 1


# %% The World Class

# It implements the Mediator interface, whose main and at the moment only part
# is the notify() method

# The World Class has knowledge of all of the other parts of the system and manages
# the way they communicate with each other

# Maybe world can act like a scheduler factory

# So, instead of creating a scheduler object and linking it to the world,
# we can do world = World(), world.create_scheduler(), world.run() or something of the form
class Input:
    def __init__ (self,x=0,y=0,i=0):
        self.input_1 = x
        self.input_2 = y
        self.count = i
    def update_input(self,input):
        if self.count == 0:
            self.input_1 = input
            self.count = 1
        else:
            self.input_2 = input
            self.count = 0
    def get_input(self):
        if self.count == 0:
            temp = self.input_1
            self.count = 1

            return self.input_1
        else:
            temp = self.input_2
            self.count = 0
            return self.input_2

class World(Mediator):

    # N stands for the number of cells, as per reference paper
    #
    def __init__(self, N):

        # Pool() will contain the set of CPUEmulators.
        self.pool = Pool(N)
    
    def react_on_division(self, result, replacement_strategy = "oldest"):
        
        program = SA.Program(result)
                
        
        emulator = SA.CPUEmulator()
        emulator.load_program(program)

        if 0 in self.pool.get_emulators():

            self.place_cell(emulator, self.pool.get_emulators().index(0))

        else:

            if replacement_strategy == "oldest":
                ages = [element.age for element in self.pool.get_emulators()]

                # Replace the oldest emulator with the newly constructed one

                self.place_cell(emulator, ages.index(max(ages)))
                
    
    def react_on_operation(self, cpu):
        # As we use lifo-queue, the world needs to know the input and not get it from the organism!
        input_1 = Input.get_input(self)
        input_2 = Input.get_input(self)

        result = cpu.output_buffer.get()

        #print(result)
        #calling result like this works, also passing the cpu works!
        #result = cpu.output_buffer.get()

        # TODO , implement IO operation checker
        # if result is correct, multiply effiency coefficient with the given coefficient for each factor!
        #addition
        #first call of IO is needed for loading in values! -> first result = 0;
        cpu.input_buffer.put(3)
        if result == 0:
            cpu.input_buffer.put(1)
            cpu.input_buffer.put(2)
        if (input_1+input_2) == result:
            print("addition")
            cpu.input_buffer.put(2)
            cpu.input_buffer.put(4)
            print("input_loaded")
        # xor
        if (input_1^input_2) == result:
            pass
        # multiplicatin
        if (input_1*input_2) == result:
            pass
        # subtraction
        if (input_1-input_2) == result:
            pass
        # and
        if (input_1 & input_2) == result:
            pass
        # or
        if (input_1 | input_2) == result:
            pass
        else:
            print("check_function else")
            print(result)
            pass
        
    def notify(self, sender, event, result):

        if event == "division":
            self.react_on_division(result)
            
        if event == "IO_operation":
            self.react_on_operation(result)
            
    #at this position, we need a function, that put's stuff into the input_buffer
    """def load_input(self,emulator):
        emulator.mediator = self
        #emulator.cpu.input_buffer.put(1)
        #emulator.cpu.input_buffer.put(2)"""
        
    def place_cell(self, emulator, position="none"):

        emulator.mediator = self
        self.pool.put(emulator, position)

    # A string representation of the world pool

    def __str__(self):

        emulators = self.pool.get_emulators()

        for i in range(0, len(emulators)):

            if emulators[i] == 0:
                continue
            else:
                print("Emulator " + str(i + 1) + ": ")
                print(emulators[i])

        return ""


# %%
"""Class mutation is responsible for every mutation factor of our programms 
when they are replicating.
"""


class Mutation:

    def __init__(self, time, emulator, factor):
        self.emulator = emulator
        self.time = time
        self.mutationfactor = factor

    def mutation(self):
        # TODO
        pass


# %%
"""Class for the input that we send to the world, ie. what we want our programms
to do 
When the IO operation in Avida is called, it takes an input from this class, does something and then 
calls the output class below.
IO operation has yet to be implemented!

IO has been implemented, now access to the input_buffer is needed.
"""


class Check_Values:

    def __init__(self, emulator):
        self.emulator = emulator

    def input(self):
        # load our input queue for cell here
        SA.CPUEmulator.input_buffer.put(0)

    # output Queue from the cell
    def output(self):
        output = SA.CPUEmulator.output_buffer
        while (output.empty == False):
            print(output.get())



# %%

"""A DEMONSTRATION OF SELF-REPLICATION:"""

# The default self-replicating program
p5 = SA.Program([ 16, 20, 2, 0, 21, 2, 20, 19, 25, 2, 0, 17, 21, 0, 1])
p = SA.Program([11,1,11,2,11,2,13,0,18,1, 16, 20, 2, 0, 21, 2, 20, 19, 25, 2, 0, 17, 21, 0, 1])

# Some random program, no idea what it does really.
# Just want to see if loading a completely random program is gonna break our system.
# It shouldn't, but it may

p1 = SA.Program([11,10,4,4,4,1,0,10,19,20,21,22,23,24,11,11,11])

# Testing a program with all the instructions we have lol
p2 = SA.Program(list(range(0,25)))

# They all work. Whether they do anything, I can't comment, but at least
# the system seems to be pretty stable

p3 = SA.Program([0,1,4,6,7,22,21,16,17,2,2,2,3,4,5,6,7,8,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,1,1,0,1,11,11,11,11])


# Why do the registers always end up being all 0?


# A world with a 10-slot pool
world = World(10)

# Manually creating the first CPUEmulator
emulator = SA.CPUEmulator()

# The first two inputs for our organism to work with
#emulator.cpu.input_buffer.put(1)
#emulator.cpu.input_buffer.put(2)

# Loading the self-replicating program into the first emulator
emulator.load_program(p)

# Placing the emulator into a random position in the world
#world.load_input(emulator)
world.place_cell(emulator, 0)
# Create a scheduler based on the world
scheduler = Scheduler(world)

# %%

# Checking execution times for a 4-slot pool.

# These execution times were recorded before defining world as mediator:

# 10k scheduler cycles takes around 0.7s
# 100k scheduler cycles takes around 7s
# 1 million scheduler cycles takes around 70s
# Ok, as expected, the time grows linearly with the number of cycles

# These execution times were recorded after defining world as mediator:

    
# 10k scheduler cycles take around 0.3s
# 100k scheduler cycles take around 3s
# 1 million scheduler cycles take around 30s


# %%time

# Run this bad boy
scheduler.schedule(250)

# %%

# Showing the resulting World Emulator Pool
print(world)
