# %%
# Necessary imports:
    
import numpy as np
import SimpleAvida as SA
# %% The Organism Pool Class

# The pool is a list of tuples. Each tuple contains in its first position
# the CPUEmulator itself and in its second position the CPUEmulator's metabolic rate

class Pool:

    def __init__(self, N):

        # A list of tuples of length N
        # The first element in the tuple is the CPUEmulator
        # The second element in the tuple is its associated metabolic rate
        self.pool = [(0,0) for element in range(0, N)]

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
        return [emulator for (emulator,rate) in self.pool]
    
    def get_rates(self):
        return [rate for (emulator,rate) in self.pool]
    
    def get_baseline(self):
        return min([rate for (emulator,rate) in self.pool if rate > 0])


#%% The Scheduler Class

# The Scheduler should have access to the Pool of the World
# I think It's necessary to couple the Scheduler to the World
# The World should still be the one containing the CPUEmulator pool
# The Scheduler can access this Pool and run the CPUEmulators in it quasi-parallel

class Scheduler:
    
    def __init__(self,world):
        self.pool = world.pool
        
    
    def schedule(self):

        pool = self.pool.get()

        for i in range(0, 132):
            
            # The scheduler does indeed need to keep track of the baseline rate
            # But does it make sense to have it access it in every iteration?
            # It sure doesn't
            # Let's see how we're gonna change that later
            
            baseline_rate = self.pool.get_baseline()

            for (emulator, rate) in pool:

                if emulator == 0:
                    continue

                else:
                    
                    temp = int(rate/baseline_rate)

                    while temp > 0:
                        
                        # NOTE: This isn't good as it is.
                        # The scheduler should blindly run instructions,
                        # it shouldn't have to check every single time whether the instruction is HDivide
                        
                        # If the next instruction to execute is HDivide:
                        if isinstance(emulator.memory.get(emulator.instr_pointer.get() % emulator.memory.size()), SA.InstructionHDivide):

                            # Grab the returned program,
                            # pack it into a CPUEmulator

                            program = SA.Program(emulator.execute_instruction())
                            emulator = SA.CPUEmulator()
                            emulator.load_program(program)

                            # Put the new emulator in the first free cell
                            # If no free cells, kill the oldest organism and put it there

                            # Can also implement this functionality in the pool.put() function

                            if 0 in self.pool.get_emulators():
                                
                                self.pool.put(emulator, self.pool.get_emulators().index(0))

                            else:

                                # Find the oldest emulator

                                oldest = 0
                                
                                for emulator in self.pool.get_emulators():
                                    
                                    age = emulator.age
                                    if age > oldest:
                                        oldest = emulator

                                # Replace the oldest emulator with the newly constructed one

                                self.pool.put(emulator, self.pool.get().index(oldest))

                        # Otherwise, just execute as usual
                        
                        # This is really all that the scheduler should do
                        else:

                            emulator.execute_instruction()

                        temp -= 1

# %% The World Class

# Contains a pool of CPUEmulators
# Should respond to CPUEmulator events (One such obvious event is division)

# Think, what should the World do?

# Maybe the world itself should be the mediator between the pool and the emulators

class World:

    # N stands for the number of cells, as per reference paper
    def __init__(self, N):

        # Pool() will contain the set of CPUEmulators.
        self.pool = Pool(N)
        self.mediator = 0
        

    def __str__(self):

        emulators = self.pool.get_emulators()

        for i in range(0, len(emulators)):

            if emulators[i] == 0:
                continue
            else:
                print("Emulator " + str(i) + ": ")
                print(emulators[i])

        return ""

    def place_cell(self, emulator, position="none"):
        self.pool.put(emulator, position)


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

class InOutput:

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


# %% Class Update()
""" Functions that's called from notify in SimpleAvida.py, so our World knows, when there
is an output avaible of a cell"""


class Observable:
    def __init__(self) -> None:
        self._observers = []

    def register_observer(self, observer) -> None:
        self._observers.append(observer)

    def notify_observers(self, *args, **kwargs) -> None:
        for observer in self._observers:
            observer.notify(self, *args, **kwargs)
# %%
""" In our Avida file we have a class IO. There we give the input arguments and it returns
an output. We then analyze that output and depending on what it is, we can change it's
fitness and other factors.
Class IO yet has to be implemented -> How do we implement it, how does it work?
"""


class Output:
    def __init__(self, emulator):
        self.emulator = emulator


# %%

"""A DEMONSTRATION OF SELF-REPLICATION:"""

# The default self-replicating program
p = SA.Program([16, 20, 2, 0, 21, 2, 20, 19, 25, 2, 0, 17, 21, 0, 1])

# A world with a 4-slot pool
world = World(4)

# Manually creating the first CPUEmulator
emulator = SA.CPUEmulator()

# Loading the self-replicating program into the first emulator
emulator.load_program(p)

# Placing the emulator into a random position in the world
world.place_cell(emulator)

# Create a scheduler based on the world
scheduler = Scheduler(world)

#%%

# Run this bad boy
scheduler.schedule()

#%%

# Showing the resulting World Emulator Pool
print(world)