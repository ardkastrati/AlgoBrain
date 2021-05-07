# A clean implementation of the Avida World simulator

# %%
# Necessary imports:

import numpy as np
import DigitalOrganism as DO
from Mediator import Mediator
import random
import sys


# %% Helper class for breaking nested loops
class BreakIt(Exception): pass


# %% Pool simulates an NxN Petri dish
# Avida organisms live in such a pool

class Pool:

    def __init__(self, N, dtype=None):

        if dtype == None:

            self.pool = np.zeros((N, N))

        else:

            self.pool = np.zeros((N, N), dtype=dtype)

    def shape(self):

        return self.pool.shape

    def get(self):

        return self.pool

    def put(self, obj, pos):

        self.pool[pos] = obj



# %% World is a powerful class which has full knowledge of all of its components

# World regulates everything
# It implements the Mediator abstract interface

class World(Mediator):

    # Pool of size NxN

    # Rates contains the metabolic rates of the emulators

    # Replacement strategy determines what happens if the pool is full and a
    # new organism is to be born. Per default, the oldest organism in the pool is killed

    # Ages keeps track of the ages of the organisms in the corresponding location

    # Default copy mutation probability is 0.0025

    def __init__(self, N, replacement_strategy="neighborhood", cm_prob=0.0225, ins_prob=0.05, del_prob=0.05):

        # Pool() will contain the set of CPUEmulators.
        self.pool = Pool(N, dtype=DO.CPUEmulator)

        self.rates = np.zeros((N, N), dtype=int)

        self.ages = np.zeros((N, N), dtype=int)

        self.inputs = np.empty((2, N, N))
        self.inputs[:] = np.nan
        self.inputcount = 0
        self.replacement_strategy = replacement_strategy
        self.fitness_factor = np.zeros(9)
        self.cm_prob = cm_prob
        self.fitness = 1
        self.ins_prob = ins_prob
        self.del_prob = del_prob

        self.winner = None

        self.result = None

    # The following method instantiates a default self-replicating organism
    # as a random location in the pool, unless location specified otherwise
    # The location must be a valid tuple

    # Default as per Avida-ED website and Nature paper. Contains 35 nop-c in the middle
    # In total 50 instructions

    #def place_default(self, position = None):

    #    self.place_custom([16, 20, 2, 0, 21] + [2]*36 + [20, 19, 25, 2, 0, 17, 21, 0, 1], position = position)
    def place_default(self, position=None):
    #
       self.place_custom(
           [16, 20, 2, 0, 21, 2, 16, 13, 25, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 10, 2, 7, 2, 2, 2, 23, 4, 2, 6, 18, 15,
            2, 2, 15, 2, 2, 18, 2, 2, 20, 19, 25, 2, 0, 17, 21, 0, 1], position=position)
        # self.place_custom([18, 16, 20, 2, 0, 21, 2, 16, 13, 0, 2, 0, 2, 2, 13, 12, 13, 1, 2, 2, 10, 2, 7, 0, 2, 2, 23, 4, 2, 6, 18, 15, 2, 13, 15, 2, 2, 18, 2, 2, 20, 19, 25, 2, 0, 17, 21, 0, 1],position = position)

    # Default per avida paper, with only 15 instructions
    def place_default_15(self, position=None):

        self.place_custom([16, 20, 18, 2, 0, 21, 2, 20, 20, 19, 25, 2, 0, 17, 21, 0, 1], position=position)

    # The following method instantiates a custom self-replicating organism
    # as a random location in the pool, unless location specified otherwise
    # The location must be a valid tuple

    def place_custom(self, program, position=None):

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
        self.pool.set_fitness(1)
        # Create random valid position or check if given position valid
        if position == None:

            position = (np.random.randint(0, self.pool.shape()[0]), np.random.randint(0, self.pool.shape()[1]))

        else:

            assert type(position) == tuple, "Given position is not a tuple"
            assert position[0] < self.pool.shape()[0] and position[1] < self.pool.shape()[1], "Positions out of bounds"

        # Put the emulator at the given position

        self.pool.put(emulator, position)

        # Put the emulator rate in the corresponding position
        # The world keeps track of the metabolic rates
        # Per default, upon any organism instantiation, the metabolic rate is 1

        self.rates[position] = 1

        # Pull out the age of the organism

        self.ages[position] = emulator.age

    # Here the scheduler loop, which runs forever unless told otherwise

    def schedule(self, n_loops=None):

        if n_loops == None:

            # I want to see how the population is doing every 10k cycles

            iterator = 0
            while True:

                baseline_rate = self.baseline_rate()
                iterator += 1

                if iterator == 5000:
                    # Shows that the whole thing is alive every 10k cycles
                    print("\nStill running")

                    # Show a random organism from the pool

                    position = (np.random.randint(0, self.pool.shape()[0]), np.random.randint(0, self.pool.shape()[1]))
                    print(self.get(position))

                    iterator = 0

                for i in range(self.pool.shape()[0]):
                    for j in range(self.pool.shape()[1]):

                        if isinstance(self.pool.get()[i][j], DO.CPUEmulator):

                            n_cycles = int(self.rates[i][j] / baseline_rate)

                            for i_cycles in range(n_cycles):
                                current_emulator = self.pool.get()[i][j]

                                current_emulator.execute_instruction()

                                self.ages[i][j] = current_emulator.age

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
                for i in range(max(idx0 - 1, 0), min(idx0 + 2, width)):
                    for j in range(max(idx1 - 1, 0), min(idx1 + 2, height)):
                        if self.pool.get()[i][j] == 0:
                            position = (i, j)
                            raise BreakIt

            except BreakIt:
                pass

            # If no free spot in the neighborhood was found, replace oldest cell in the neighborhood
            if position == None:

                oldest = 0

                for i in range(max(idx0 - 1, 0), min(idx0 + 2, width)):
                    for j in range(max(idx1 - 1, 0), min(idx1 + 2, height)):
                        if self.ages[i][j] >= oldest:
                            oldest = self.ages[i][j]
                            position = (i, j)

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

        self.rates[position] = 1

        # Set input to none

        self.inputs[0][position] = np.nan
        self.inputs[1][position] = np.nan

    # Here how the world reacts upon an IO operation        

    def react_on_IO(self, sender, result):

        # Find the position in the pool where the sender is at:

        idx0 = np.where(self.pool.get() == sender)[0][0]
        idx1 = np.where(self.pool.get() == sender)[1][0]

        #
        if np.isnan(self.inputs[0][idx0][idx1]):

            pass

        else:

            if self.inputs[0][idx0][idx1] == ~result:

                self.input = self.inputs[0][idx0][idx1]

                self.winner = self.get((idx0, idx1))

                self.result = result
                print("\nEMULATOR AT POSITION " + str((idx0, idx1)) + " COMPUTED NOT\nINPUT: " + str(
                    self.input) + "\nOUTPUT: " + str(self.result))
                if self.fitness_factor[0] == 0:
                    self.rates[idx0][idx1] = 2 * self.rates[idx0][idx1]
                    self.fitness_factor[0] = 1
                else:
                    pass
            if self.inputs[1][idx0][idx1] == ~result:
                self.input = self.inputs[1][idx0][idx1]

                self.winner = self.get((idx0, idx1))

                self.result = result
                print("\nEMULATOR AT POSITION " + str((idx0, idx1)) + " COMPUTED NOT\nINPUT_2: " + str(
                    self.input) + "\nOUTPUT: " + str(self.result))
                if self.fitness_factor[0] == 0:
                    self.rates[idx0][idx1] = 2 * self.rates[idx0][idx1]
                    self.fitness_factor[0] = 1
                else:
                    pass
            # All operations that need two inputs:
            if np.isnan(self.inputs[1][idx0][idx1]):
                pass
            else:
                # Nand:
                if ~(self.inputs[0][idx0][idx1].astype(np.int64) & self.inputs[1][idx0][idx1].astype(np.int64)) == result:
                    input_1 = self.inputs[0][idx0][idx1]
                    input_2 = self.inputs[1][idx0][idx1]
                    self.winner = self.get((idx0, idx1))
                    self.result = result
                    print("\nEMULATOR AT POSITION " + str((idx0, idx1)) + " COMPUTED NAND\nINPUT_1: " + str(
                        input_1) + "\nInput_2: " + str(input_2) + "\nOUTPUT: " + str(self.result))
                    if self.fitness_factor[1] == 0:
                        self.rates[idx0][idx1] = 2 * self.rates[idx0][idx1]
                        self.fitness_factor[1] = 1
                # And:
                if (self.inputs[0][idx0][idx1].astype(np.int64) & self.inputs[1][idx0][idx1].astype(np.int64)) == result:
                    input_1 = self.inputs[0][idx0][idx1]
                    input_2 = self.inputs[1][idx0][idx1]
                    self.winner = self.get((idx0, idx1))
                    self.result = result
                    print("\nEMULATOR AT POSITION " + str((idx0, idx1)) + " COMPUTED AND\nINPUT_1: " + str(
                        input_1) + "\nInput_2: " + str(input_2) + "\nOUTPUT: " + str(self.result))
                    if self.fitness_factor[2] == 0:
                        self.rates[idx0][idx1] = 4 * self.rates[idx0][idx1]
                        self.fitness_factor[2] = 1
                # OR_N:
                if (self.inputs[0][idx0][idx1].astype(np.int64) & ~self.inputs[1][idx0][idx1].astype(np.int64)) == result:
                    input_1 = self.inputs[0][idx0][idx1]
                    input_2 = self.inputs[1][idx0][idx1]
                    self.winner = self.get((idx0, idx1))
                    self.result = result
                    print("\nEMULATOR AT POSITION " + str((idx0, idx1)) + " COMPUTED OR_n\nINPUT_1: " + str(
                        input_1) + "\nInput_2: " + str(input_2) + "\nOUTPUT: " + str(self.result))
                    if self.fitness_factor[3] == 0:
                        self.rates[idx0][idx1] = 4 * self.rates[idx0][idx1]
                        self.fitness_factor[3] = 1
                if (~self.inputs[0][idx0][idx1].astype(np.int64) & self.inputs[1][idx0][idx1].astype(np.int64)) == result:
                    input_1 = self.inputs[0][idx0][idx1]
                    input_2 = self.inputs[1][idx0][idx1]
                    self.winner = self.get((idx0, idx1))
                    self.result = result
                    print("\nEMULATOR AT POSITION " + str((idx0, idx1)) + " COMPUTED OR_n\nINPUT_1: " + str(
                        input_1) + "\nInput_2: " + str(input_2) + "\nOUTPUT: " + str(self.result))
                    if self.fitness_factor[3] == 0:
                        self.rates[idx0][idx1] = 4 * self.rates[idx0][idx1]
                        self.fitness_factor[3] = 1
                # OR
                if (self.inputs[0][idx0][idx1].astype(np.int64) | self.inputs[1][idx0][idx1].astype(np.int64)) == result:
                    input_1 = self.inputs[0][idx0][idx1]
                    input_2 = self.inputs[1][idx0][idx1]
                    self.winner = self.get((idx0, idx1))
                    self.result = result
                    print("\nEMULATOR AT POSITION " + str((idx0, idx1)) + " COMPUTED OR\nINPUT_1: " + str(
                        input_1) + "\nInput_2: " + str(input_2) + "\nOUTPUT: " + str(self.result))
                    if self.fitness_factor[4] == 0:
                        self.rates[idx0][idx1] = 8 * self.rates[idx0][idx1]
                        self.fitness_factor[4] = 1
                # And_N
                if (self.inputs[0][idx0][idx1].astype(np.int64) & ~self.inputs[1][idx0][idx1].astype(np.int64)) == result:
                    input_1 = self.inputs[0][idx0][idx1]
                    input_2 = self.inputs[1][idx0][idx1]
                    self.winner = self.get((idx0, idx1))
                    self.result = result
                    print("\nEMULATOR AT POSITION " + str((idx0, idx1)) + " COMPUTED And_n\nINPUT_1: " + str(
                        input_1) + "\nInput_2: " + str(input_2) + "\nOUTPUT: " + str(self.result))
                    if self.fitness_factor[5] == 0:
                        self.rates[idx0][idx1] = 8 * self.rates[idx0][idx1]
                        self.fitness_factor[5] = 1
                if (~self.inputs[0][idx0][idx1].astype(np.int64) & self.inputs[1][idx0][idx1].astype(np.int64)) == result:
                    input_1 = self.inputs[0][idx0][idx1]
                    input_2 = self.inputs[1][idx0][idx1]
                    self.winner = self.get((idx0, idx1))
                    self.result = result
                    print("\nEMULATOR AT POSITION " + str((idx0, idx1)) + " COMPUTED And_n\nINPUT_1: " + str(
                        input_1) + "\nInput_2: " + str(input_2) + "\nOUTPUT: " + str(self.result))
                    if self.fitness_factor[5] == 0:
                        self.rates[idx0][idx1] = 8 * self.rates[idx0][idx1]
                        self.fitness_factor[5] = 1
                # NOR
                if (~self.inputs[0][idx0][idx1].astype(np.int64) & ~self.inputs[1][idx0][idx1].astype(np.int64)) == result:
                    input_1 = self.inputs[0][idx0][idx1]
                    input_2 = self.inputs[1][idx0][idx1]
                    self.winner = self.get((idx0, idx1))
                    self.result = result
                    print("\nEMULATOR AT POSITION " + str((idx0, idx1)) + " COMPUTED NOR\nINPUT_1: " + str(
                        input_1) + "\nInput_2: " + str(input_2) + "\nOUTPUT: " + str(self.result))
                    if self.fitness_factor[6] == 0:
                        self.rates[idx0][idx1] = 16 * self.rates[idx0][idx1]
                        self.fitness_factor[6] = 1

                # XOR
                if ((self.inputs[0][idx0][idx1].astype(np.int64) & ~self.inputs[1][idx0][idx1].astype(np.int64)) | (
                        ~self.inputs[0][idx0][idx1].astype(np.int64) & self.inputs[1][idx0][idx1].astype(np.int64))) == result:
                    input_1 = self.inputs[0][idx0][idx1]
                    input_2 = self.inputs[1][idx0][idx1]
                    self.winner = self.get((idx0, idx1))
                    self.result = result
                    print("\nEMULATOR AT POSITION " + str((idx0, idx1)) + " COMPUTED XOR\nINPUT_1: " + str(
                        input_1) + "\nInput_2: " + str(input_2) + "\nOUTPUT: " + str(self.result))
                    if self.fitness_factor[7] == 0:
                        self.rates[idx0][idx1] = 16 * self.rates[idx0][idx1]
                        self.fitness_factor[7] = 1
                # EQU
                if ((self.inputs[0][idx0][idx1].astype(np.int64) & self.inputs[1][idx0][idx1].astype(np.int64)) | (~self.inputs[0][idx0][idx1].astype(np.int64) & ~self.inputs[1][idx0][idx1].astype(np.int64))) == result:
                    input_1 = self.inputs[0][idx0][idx1]
                    input_2 = self.inputs[1][idx0][idx1]
                    self.winner = self.get((idx0, idx1))
                    self.result = result
                    print("\nEMULATOR AT POSITION " + str((idx0, idx1)) + " COMPUTED EQU\nINPUT_1: " + str(
                        input_1) + "\nInput_2: " + str(input_2) + "\nOUTPUT: " + str(self.result))
                    if self.fitness_factor[8] == 0:
                        self.rates[idx0][idx1] = 32 * self.rates[idx0][idx1]
                        self.fitness_factor[8] = 1

        # A random 32-bit number
        to_input = random.getrandbits(31)

        # Put the randomly generated number into the input buffer of the emulator
        sender.cpu.input_buffer.put(to_input)

        # Update inputs array
        if self.inputcount == 0:
            self.inputs[0][idx0][idx1] = to_input
            self.inputcount = 1
        else:
            self.inputs[1][idx0][idx1] = to_input
            self.inputcount = 0

    # Helper methods here:

    def oldest_position(self):

        # Returns the position of the oldest emulator in the pool
        # If there are several such emulators with equal age, returns the first one
        # it encounters

        for i in range(0, self.pool.shape()[0]):
            for j in range(0, self.pool.shape()[1]):

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

    def get(self, position):

        return self.pool.get()[position]

    # A string representation of the world pool

    def __str__(self):

        emulators = self.pool.get()[self.pool.get() != 0]

        for i in range(emulators.size):
            print("Emulator " + str(i + 1) + ": ")
            print(emulators[i])

        return ""


# %% Testing some stuff

# First argument is world size
# cm_prob is copy mutation probability
# ins_prob and del_prob are insertion and deletion probabilities
world = World(30, cm_prob=0.01, ins_prob=0.05, del_prob=0.05)

world.place_default((0, 0))
world.place_default((0, 15))
world.place_default((0, 29))
world.place_default((15, 0))
world.place_default((15, 15))
world.place_default((15, 29))
world.place_default((29, 0))
world.place_default((29, 15))
world.place_default((29, 29))

world.schedule()

# %%

# World claims this organisms computed NOT:

not0 = [16, 20, 2, 0, 21, 2, 2, 12, 14, 18, 13, 16, 2, 5, 24, 25, 13, 2, 7, 19, 2, 21, 23, 2, 23, 2, 2, 17, 2, 17, 2, 8,
        2, 2, 16, 2, 6, 2, 6, 7, 5, 25, 19, 25, 2, 0, 17, 21, 0, 1]

not1 = [16, 20, 2, 0, 21, 2, 3, 15, 2, 2, 2, 2, 21, 2, 2, 2, 2, 2, 2, 18, 15, 2, 2, 24, 25, 2, 22, 2, 2, 2, 18, 2, 2, 2,
        2, 2, 2, 2, 2, 23, 2, 20, 19, 23, 2, 0, 17, 21, 0, 1]

not2 = [16, 20, 2, 0, 21, 2, 16, 13, 25, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 10, 2, 7, 2, 2, 2, 23, 4, 2, 6, 18, 15, 2, 2,
        15, 2, 2, 18, 2, 2, 20, 19, 25, 2, 0, 17, 21, 0, 1]

# %%
