# %%
# Necessary imports:
import numpy as np
from abc import ABC
import SimpleAvida as SA
"""Read_me:
    As we use the Mediator Scheme, so everything communicates with a Mediator and only with the Mediator,
    We implement everything as a component of said Mediator. 
    This means, we implement a our organism as a component"""


class Component1:
    pass


class Component2:
    pass


class Mediator(ABC):
    """
    The Mediator interface declares a method used by components to notify the
    mediator about various events. The Mediator may react to these events and
    pass the execution to other components.
    """

    def notify(self, sender: object, event: str, parameter: object) -> None:
        pass


class ConcreteMediator(Mediator):
    def __init__(self, component1: Component1, component2: Component2) -> None:
        self._component1 = component1
        self._component1.mediator = self
        self._component2 = component2
        self._component2.mediator = self
    """ Our notifying Operations are defined here. We implement a notify-Option for h_divide and for io-operation
    this means, organism does something with the two given values of the input_buffer, 
    then calls io, which calls notify(self,"output"). This will call operation defined below, that calls a check 
    function, and if working, puts new values into input_buffer for different operations.
    self.component1.do_mut() will change the mutation factor, self.component1.do_eff() will change the metabolism"""

    def notify(self, sender: object, event: str, result: object) -> None:
        if event == "A":
            print("Mediator reacts on A and triggers following operations:")
            self._component2.do_c()
        elif event == "D":
            print("Mediator reacts on D and triggers following operations:")
            self._component1.do_b()
            self._component2.do_c()
        elif event == "K":
            print("Notified, that H_Divide has been succesfull")
            #print(result)
            self._component2.do_d()
        elif event == "output":
            print("Notified, that something is in outputbuffer")
            if result == 1:
                print("result is correct")
                self._component2.do_input()
            else:
                print("result was wrong")
                pass

class BaseComponent:
    """
    The Base Component provides the basic functionality of storing a mediator's
    instance inside component objects.
    """

    def __init__(self, mediator: Mediator = None) -> None:
        self._mediator = mediator

    @property
    def mediator(self) -> Mediator:
        return self._mediator

    @mediator.setter
    def mediator(self, mediator: Mediator) -> None:
        self._mediator = mediator


"""
Concrete Components implement various functionality. They don't depend on other
components. They also don't depend on any concrete mediator classes.
"""


# %%

class Component1(BaseComponent):
    def do_a(self, emulator) -> None:
        world = World(12)
        world.place_cell(emulator)

        # Create a scheduler based on the world
        scheduler = Scheduler(world)
        scheduler.schedule()
        print("World places Organism.")
        print(world)
        self.mediator.notify(self, "K",None)

    def do_b(self) -> None:
        print("Component 1 does B.")
        self.mediator.notify(self, "B", None)


class Component2(BaseComponent):
    def do_c(self)->None:
        print("Component 2 does C.")
        self.mediator.notify(self, "C", None)
    def do_emulator(self, program):

        emulator = SA.CPUEmulator()
        emulator.cpu.input_buffer.put(1)
        emulator.cpu.input_buffer.put(2)
        # Loading the self-replicating program into the first emulator
        emulator.load_program(program)
        return emulator
    def do_d(self)->None:
        print("delete do_d")


    def do_input(self)->None:
        print("do_input has worked successfully")


10  # %% The Organism Pool Class


# The pool is a list of tuples. Each tuple contains in its first position
# the CPUEmulator itself and in its second position the CPUEmulator's metabolic rate

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


# %%
class World:

    # N stands for the number of cells, as per reference paper
    def __init__(self, N):

        # Pool() will contain the set of CPUEmulators.
        self.pool = Pool(N)

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


# %% The Scheduler Class

# The Scheduler should have access to the Pool of the World
# I think It's necessary to couple the Scheduler to the World
# The World should still be the one containing the CPUEmulator pool
# The Scheduler can access this Pool and run the CPUEmulators in it quasi-parallel

class Scheduler:

    def __init__(self, world):
        self.pool = world.pool

    def schedule(self):

        pool = self.pool.get()

        for i in range(0, 66):

            # The scheduler does indeed need to keep track of the baseline rate
            # But does it make sense to have it access it in every iteration?
            # It sure doesn't
            # Let's see how we're gonna change that later

            baseline_rate = self.pool.get_baseline()

            for (emulator, rate) in pool:

                if emulator == 0:
                    continue

                else:

                    temp = int(rate / baseline_rate)

                    while temp > 0:

                        # NOTE: This isn't good as it is.
                        # The scheduler should blindly run instructions,
                        # it shouldn't have to check every single time whether the instruction is HDivide

                        # If the next instruction to execute is HDivide:
                        if isinstance(emulator.memory.get(emulator.instr_pointer.get() % emulator.memory.size()),
                                      SA.InstructionHDivide):

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


if __name__ == "__main__":
    #the organism and everything needs to be defined here!
    # The client code.
    # Startorganism
    p = SA.Program([16, 20, 2, 0, 21, 2, 20, 19, 25, 2, 0, 17, 21, 0, 1])
    c1 = Component1()
    c2 = Component2()
    emulator = c2.do_emulator(p)
    mediator = ConcreteMediator(c1, c2)

    print("Client triggers operation A.")
    c1.do_a(emulator)

    print("\n", end="")

    #print("Client triggers operation D.")
    #c2.do_d()
    #c2.do_input()
    # The default self-replicating program
    """p = SA.Program([16, 20, 2, 0, 21, 2, 20, 19, 25, 2, 0, 17, 21, 0, 1])

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

    # Run this bad boy
    scheduler.schedule()

    # Showing the resulting World Emulator Pool
    print(world)
    """
# %%


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
