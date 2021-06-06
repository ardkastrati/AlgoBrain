# %%
# Necessary imports:

from queue import LifoQueue
from queue import Queue
from Mediator import Mediator
import sys
import numpy as np

# For the probability of random mutations
from scipy.stats import bernoulli
from random import randrange
from numpy import random

#%%

# We get overflow errors sometimes but for our purposes this is absolutely fine
# We care about the binary representation, not the actual int32 value
# Therefore, ignore overflow warnings
np.warnings.filterwarnings('ignore', 'overflow')


# %% The Program

class Program:

    # A class for AVIDA programs
    # A list of any size, the only restriction is that the elements must be integers in {0,1,...,25}

    def check_validity(self, instr_list):

        for instruction in instr_list:
            assert instruction in range(26)

    def __init__(self, instr_list):

        self.check_validity(instr_list)

        self.instructions = instr_list

# %% The Register Class

# Contains a single integer value

class Register:

    def __init__(self,value = 0):
        self.content = value

    def write(self,value):
        self.content = value

    def read(self):
        return self.content

    def increment(self, a = 1):
        self.content += a

    def decrement(self, b = 1):
        self.content -= b

# %% The Heads

class InstructionPointer:

    def __init__(self):
        self.value = 0

    def increment(self, a = 1):
        self.value += a

    def get(self):
        return self.value

    def next(self):
        return self.value + 1

    def set(self,a):
        self.value = a

class ReadHead:

    def __init__(self):
        self.value = 0

    def increment(self, a = 1):
        self.value += a

    def get(self):
        return self.value

    def set(self,a):
        self.value = a

class WriteHead:

    def __init__(self):
        self.value = 0

    def increment(self, a = 1):
        self.value += a

    def get(self):
        return self.value

    def set(self,a):
        self.value = a

class FlowControlHead:

    def __init__(self):
        self.value = 0

    def increment(self, a = 1):
        self.value += a

    def get(self):
        return self.value

    def set(self,a):
        self.value = a

# %% The Memory

class Memory:

    def __init__(self):
        self.content = []

    # Wipe the memory completely
    def wipe(self):
        self.content = []

    def size(self):
        return len(self.content)

    def get(self,index):
        if len(self.content) > index:
            return self.content[index]
        else:
            raise Exception("Index out of boundaries")

    def read(self):
        return self.content

    def append(self,value):
        self.content.append(value)

# %% The CPU (Virtual Hardware)

class CPU:

    def __init__(self, a, b, c):

        self.reg_a = Register(a)
        self.reg_b = Register(b)
        self.reg_c = Register(c)

        self.stack0 = LifoQueue()
        self.stack1 = LifoQueue()
        self.active_stack = self.stack0

        self.input_buffer = Queue()
        self.output_buffer = Queue()
        self.fitness = 100

    def clear(self):

        self.reg_a.write(0)
        self.reg_b.write(0)
        self.reg_c.write(0)

        while not self.stack0.empty():
            self.stack0.get()

        while not self.stack1.empty():
            self.stack1.get()

        while not self.input_buffer.empty():
            self.input_buffer.get()

        while not self.output_buffer.empty():
            self.output_buffer.get()

# %% The Instructions

# An implementation of the default AVIDA instruction set

# NOTATION: machine variable stands for the hardware,
# emulator variable stands for the emulator

class InstructionNopA:

    def __init__(self,emulator):
        pass

    def execute(self):
        pass

class InstructionNopB:

    def __init__(self,emulator):
        pass

    def execute(self):
        pass

class InstructionNopC:

    def __init__(self,emulator):
        pass

    def execute(self):
        pass

class InstructionIfNEq:

    def __init__(self,emulator):

        self.emulator = emulator
        self.machine = emulator.cpu

    def execute(self):

        next_ = self.emulator.instruction_memory.get((self.emulator.instr_pointer.get() + 1) % self.emulator.instruction_memory.size())

        if isinstance(next_, InstructionNopA):
            if self.machine.reg_a.read() != self.machine.reg_b.read():
                pass
            else:
                self.emulator.instr_pointer.increment(2)

        elif isinstance(next_, InstructionNopC):
            if self.machine.reg_c.read() != self.machine.reg_a.read():
                pass
            else:
                self.emulator.instr_pointer.increment(2)

        else:
            if self.machine.reg_b.read() != self.machine.reg_c.read():
                pass
            else:
                self.emulator.instr_pointer.increment(2)

class InstructionIfLess:

    def __init__(self, emulator):

        self.emulator = emulator
        self.machine = emulator.cpu

    def execute(self):

        next_ = self.emulator.instruction_memory.get((self.emulator.instr_pointer.get() + 1) % self.emulator.instruction_memory.size())

        if isinstance(next_, InstructionNopA):
            if self.machine.reg_a.read() < self.machine.reg_b.read():
                pass
            else:
                self.emulator.instr_pointer.increment(2)

        elif isinstance(next_, InstructionNopC):
            if self.machine.reg_c.read() < self.machine.reg_a.read():
                pass
            else:
                self.emulator.instr_pointer.increment(2)

        else:
            if self.machine.reg_b.read() < self.machine.reg_c.read():
                pass
            else:
                self.emulator.instr_pointer.increment(2)

class InstructionSwap:

    def __init__(self, emulator):
        self.emulator = emulator

    def execute(self):

        next_ = self.emulator.instruction_memory.get((self.emulator.instr_pointer.get() + 1) % self.emulator.instruction_memory.size())

        if isinstance(next_, InstructionNopA):
            temp = self.emulator.cpu.reg_a.read()
            self.emulator.cpu.reg_a.write(self.emulator.cpu.reg_b.read())
            self.emulator.cpu.reg_b.write(temp)

        elif isinstance(next_, InstructionNopC):
            temp = self.emulator.cpu.reg_c.read()
            self.emulator.cpu.reg_c.write(self.emulator.cpu.reg_a.read())
            self.emulator.cpu.reg_a.write(temp)

        else:
            temp = self.emulator.cpu.reg_b.read()
            self.emulator.cpu.reg_b.write(self.emulator.cpu.reg_c.read())
            self.emulator.cpu.reg_c.write(temp)

class InstructionPop:

    def __init__(self, emulator):

        self.machine = emulator.cpu
        self.emulator = emulator


    def execute(self):

        next_ = self.emulator.instruction_memory.get((self.emulator.instr_pointer.get() + 1) % self.emulator.instruction_memory.size())

        # Making sure that if the stack is empty, pop returns a 0 and not an exception
        # as is defined in the implementation of the LifoQueue()

        if self.machine.active_stack.empty():
            temp = 0
        else:
            temp = self.machine.active_stack.get()

        if isinstance(next_, InstructionNopA):
            self.machine.reg_a.write(temp)

        elif isinstance(next_, InstructionNopC):
            self.machine.reg_c.write(temp)

        else:
            self.machine.reg_b.write(temp)

class InstructionPush:

    def __init__(self, emulator):

        self.emulator = emulator
        self.machine = emulator.cpu

    def execute(self):

        next_ = self.emulator.instruction_memory.get((self.emulator.instr_pointer.get() + 1) % self.emulator.instruction_memory.size())

        if isinstance(next_, InstructionNopA):
            self.machine.active_stack.put(self.machine.reg_a.read())

        elif isinstance(next_, InstructionNopC):
            self.machine.active_stack.put(self.machine.reg_c.read())

        else:
            self.machine.active_stack.put(self.machine.reg_b.read())

class InstructionSwapStack:

    def __init__(self,emulator):

        self.emulator = emulator
        self.machine = emulator.cpu

    def execute(self):

        if self.machine.active_stack == self.machine.stack0:
            self.machine.active_stack = self.machine.stack1

        else:
            self.machine.active_stack = self.machine.stack0

class InstructionRightShift:

     def __init__(self, emulator):

         self.emulator = emulator
         self.machine = emulator.cpu

     def execute(self):

        next_ = self.emulator.instruction_memory.get((self.emulator.instr_pointer.get() + 1) % self.emulator.instruction_memory.size())

        if isinstance(next_, InstructionNopA):
            self.machine.reg_a.write(int(self.machine.reg_a.read()) >> 1)

        elif isinstance(next_, InstructionNopC):
            self.machine.reg_c.write(int(self.machine.reg_c.read()) >> 1)

        else:
            self.machine.reg_b.write(int(self.machine.reg_b.read()) >> 1)

class InstructionLeftShift:

    def __init__(self, emulator):

        self.emulator = emulator
        self.machine = emulator.cpu

    def execute(self):

        next_ = self.emulator.instruction_memory.get((self.emulator.instr_pointer.get() + 1) % self.emulator.instruction_memory.size())

        if isinstance(next_, InstructionNopA):
            self.machine.reg_a.write(int(self.machine.reg_a.read()) << 1)

        elif isinstance(next_, InstructionNopC):
            self.machine.reg_c.write(int(self.machine.reg_c.read()) << 1)

        else:
            self.machine.reg_b.write(int(self.machine.reg_b.read()) << 1)

class InstructionInc:

    def __init__(self, emulator):
        self.emulator = emulator

    def execute(self):

        next_ = self.emulator.instruction_memory.get((self.emulator.instr_pointer.get() + 1) % self.emulator.instruction_memory.size())

        if isinstance(next_, InstructionNopA):
            self.emulator.cpu.reg_a.increment()

        elif isinstance(next_, InstructionNopC):
            self.emulator.cpu.reg_c.increment()

        else:
            self.emulator.cpu.reg_b.increment()

class InstructionDec:

    def __init__(self, emulator):
        self.emulator = emulator

    def execute(self):

        next_ = self.emulator.instruction_memory.get((self.emulator.instr_pointer.get() + 1) % self.emulator.instruction_memory.size())

        if isinstance(next_, InstructionNopA):
            self.emulator.cpu.reg_a.decrement()

        elif isinstance(next_, InstructionNopC):
            self.emulator.cpu.reg_c.decrement()

        else:
            self.emulator.cpu.reg_b.decrement()

class InstructionAdd:

    def __init__(self, emulator):
        self.emulator = emulator
        self.machine = emulator.cpu

    def execute(self):

        next_ = self.emulator.instruction_memory.get((self.emulator.instr_pointer.get() + 1) % self.emulator.instruction_memory.size())

        sum_ = self.machine.reg_b.read() + self.machine.reg_c.read()

        if isinstance(next_, InstructionNopA):
            self.machine.reg_a.write(sum_)

        elif isinstance(next_, InstructionNopC):
            self.machine.reg_c.write(sum_)

        else:
            self.machine.reg_b.write(sum_)

class InstructionSub:

    def __init__(self, emulator):
        self.emulator = emulator
        self.machine = emulator.cpu

    def execute(self):

        next_ = self.emulator.instruction_memory.get((self.emulator.instr_pointer.get() + 1) % self.emulator.instruction_memory.size())

        diff = self.machine.reg_b.read() - self.machine.reg_c.read()

        if isinstance(next_, InstructionNopA):
            self.machine.reg_a.write(diff)

        elif isinstance(next_, InstructionNopC):
            self.machine.reg_c.write(diff)

        else:
            self.machine.reg_b.write(diff)

class InstructionNand:

    def __init__(self, emulator):
        self.emulator = emulator
        self.machine = emulator.cpu

    def execute(self):

        next_ = self.emulator.instruction_memory.get((self.emulator.instr_pointer.get() + 1) % self.emulator.instruction_memory.size())

        nand = ~(np.int(self.machine.reg_b.read()) & np.int(self.machine.reg_c.read()))

        if isinstance(next_, InstructionNopA):
            self.machine.reg_a.write(nand)

        elif isinstance(next_, InstructionNopC):
            self.machine.reg_c.write(nand)

        else:
            self.machine.reg_b.write(nand)

class InstructionHAlloc:

    def __init__(self, emulator):
        self.emulator = emulator

    def execute(self):

        # An organism can only allocate memory once

        if self.emulator.allocated == False:
            
            for i in range(0, self.emulator.instruction_memory.size()):
                self.emulator.memory.append(0)

            self.emulator.allocated = True
        else:

            pass

# Split off the instructions between the Read-Head and the Write-Head
# and turn them into a new organism.
class InstructionHDivide:

    def __init__(self,emulator):
        self.emulator = emulator

    def execute(self):

        # If the parent has allocated memory division can happen
        if self.emulator.allocated:

            # Division may only happen if the write head is strictly larger than the read head
            # and they are both at valid positions

            rh = self.emulator.read_head.get()
            wh = self.emulator.write_head.get()

            if rh < wh:

                """
                result = []
                
                iterator = self.emulator.read_head.get()

                
                while iterator < min(len(self.emulator.program),self.emulator.write_head.get()):
                    result.append(self.emulator.program[iterator])
                    iterator += 1
                """

                result = self.emulator.memory[rh:wh]

                original = self.emulator.memory[:rh]

                # Conditions under which H-Divide fails:
                # Parent or offspring remain with fewer than 10 instructions
                # <70% of the parent was executed
                # <70% of the memory allocated for the child was copied into
                if len(original) < 10 or len(result) < 10 or (self.emulator.instr_pointer.get() % self.emulator.instruction_memory.size())/self.emulator.instruction_memory.size() < 0.7 or len(result) < 0.7 * self.emulator.instruction_memory.size():
                    
                    pass

                else:

                    # Fully reset the state of the emulator (except age)
                    self.emulator.load_program(Program(original))

                    # Insertion mutations
                    chance = bernoulli.rvs(self.emulator.ins_prob, size=1)

                    if chance == 1:

                        result.insert(random.randint(0, len(result)), randrange(26))
                    else:
                        pass
                    # TODO : -> change this
                    # TODO COME UP WITH A BETTER WAY FOR MUTATING!
                    # Deletion mutations
                    chance = bernoulli.rvs(self.emulator.del_prob, size=1)

                    if chance == 1:
                        del result[random.randint(0, len(result))]
                    else:
                        pass
                    
                    # Save old child rate to reset to after division
                    old_rate = self.emulator.child_rate
                    
                    # Update the child rate s.t. it's proportional to its genome length
                    #self.emulator.child_rate *= len(result)

                    # Notify the world about the division
                    self.emulator.mediator.notify(sender = self.emulator, event = "division", result = result)
                    
                    # Restore child_rate to old_rate
                    self.emulator.child_rate = old_rate

                    # Memory is no longer allocated
                    self.emulator.allocated = False

            # Otherwise, division is ignored

            else:
                pass

        else:
            pass

# Do a put and get immediately after each other.
# Working register is ?BX?
class InstructionIO:

    def __init__(self, emulator):
        self.emulator = emulator

    def execute(self):

        next_ = self.emulator.instruction_memory.get((self.emulator.instr_pointer.get() + 1) % self.emulator.instruction_memory.size())

        # put: place ?BX? instance in the output buffer and set register used to 0
        if isinstance(next_, InstructionNopA):
            self.emulator.cpu.output_buffer.put(self.emulator.cpu.reg_a.read())
            self.emulator.cpu.reg_a.write(0)

        elif isinstance(next_, InstructionNopC):
            self.emulator.cpu.output_buffer.put(self.emulator.cpu.reg_c.read())
            self.emulator.cpu.reg_c.write(0)

        else:
            self.emulator.cpu.output_buffer.put(self.emulator.cpu.reg_b.read())
            self.emulator.cpu.reg_b.write(0)

        to_output = self.emulator.cpu.output_buffer.get()

        # Notify the world about IO
        self.emulator.mediator.notify(sender = self.emulator, event = "IO_operation", result = to_output)

        # get: return value from input buffer into ?BX?
        if isinstance(next_, InstructionNopA):
            to_input = self.emulator.cpu.input_buffer.get()
            self.emulator.cpu.reg_a.write(to_input)

        elif isinstance(next_, InstructionNopC):
            to_input = self.emulator.cpu.input_buffer.get()
            self.emulator.cpu.reg_c.write(to_input)

        else:
            to_input = self.emulator.cpu.input_buffer.get()
            self.emulator.cpu.reg_b.write(to_input)

class InstructionHCopy:

    def __init__(self,emulator):
        self.emulator = emulator

    def execute(self):
        # To even start copying, we need to make sure that memory was allocated
        # and that the read and write heads aren't pointing to some random invalid positions
        if not self.emulator.allocated:

            pass

        else:

            # First we check if the read head and write head are even in their
            # valid ranges.

            # If they are not, HCopy will be ignored.

            wh = self.emulator.write_head.get()
            rh = self.emulator.read_head.get()

            if rh < len(self.emulator.original_memory) and wh < len(self.emulator.memory) and wh >= 0 and rh >= 0:

                chance = bernoulli.rvs(self.emulator.mutation_prob, size=1)

                if chance == 1:
                    temp = randrange(26)
                else:
                    temp = self.emulator.original_memory[self.emulator.read_head.get()]

                self.emulator.memory[wh] = temp
                self.emulator.read_head.increment()
                self.emulator.write_head.increment()
                self.emulator.copied.append(temp)

            else:

                pass

# Search in the forward direction for the complement label and set the flow-control-head
# to the end of the label

# The distance to the end of the label is placed into BX
# The size of the label is put into CX

# If no complement label is found, the flow-control-head is set
# to the current position of the instruction-head
class InstructionHSearch:

    def __init__(self,emulator):
        self.emulator = emulator

    def execute(self):
        
        # We will search in the circular memory until the position where the instruction is at.
        end_search_index = self.emulator.instr_pointer.get() % self.emulator.instruction_memory.size()

        # We will start reading in the label at the very next instruction
        iterator = (self.emulator.instr_pointer.get() + 1) % self.emulator.instruction_memory.size()

        # This is where the template will be saved
        template = []

        # Here we read in the template
        while self.emulator.original_memory[iterator] == 0 or self.emulator.original_memory[iterator] == 1 or self.emulator.original_memory[iterator] == 2:
            template.append(self.emulator.original_memory[iterator])
            iterator += 1
            iterator = iterator % self.emulator.instruction_memory.size()
            
        # If there was no template:
        # The flow control head is set to the current value of the instruction-head,
        # which also turns out to be our end search index
        
        # The distance to the end of the label is 0, and the label length is also 0
        if len(template) == 0:

            self.emulator.fc_head.set(end_search_index)
            self.emulator.cpu.reg_b.write(0)
            self.emulator.cpu.reg_c.write(0)

        # If a label was found:
        else:

            # The complement label that we're searching for
            to_match = [(element + 1) % 3 for element in template]
            
            # Write length of the label to reg_c
            self.emulator.cpu.reg_c.write(len(to_match))

            # Start the search at the following index
            # This index corresponds to the index where the read in template ends
            start_index = (self.emulator.instr_pointer.get() + len(template) + 1) % self.emulator.instruction_memory.size()

            # A helper variable
            iterator_index = start_index

            # Initialize the distance to the end of the complement label
            # It is equal to at least 2 * length (template), if a complement template is found
            distance = 2 * len(to_match)
            
            # If no complement template was found, the distance to the end of the label is not defined
            # Write 0 to register b
            # This will be updated with the true distance to the end of the label, if one is found
            self.emulator.cpu.reg_b.write(0)
            
            # If no label is found, set fc_head to the current instruction pointer
            # This will be updated if a complement label is found
            self.emulator.fc_head.set(end_search_index)

            while(iterator_index != end_search_index):
                
                # The possible index where the complement label ends
                candidate_index = iterator_index + len(to_match) % self.emulator.instruction_memory.size()
                # The possible template
                candidate_template = [self.emulator.original_memory[k % self.emulator.instruction_memory.size()] for k in range(iterator_index, iterator_index + len(to_match))]

                # If template was found
                if candidate_template == to_match:

                    self.emulator.fc_head.set(candidate_index)
                    self.emulator.cpu.reg_b.write(distance)
                    break
                # Otherwise, go on
                iterator_index += 1
                iterator_index = iterator_index % self.emulator.instruction_memory.size()
                distance += 1

class InstructionMovHead:

    def __init__(self,emulator):
        self.emulator = emulator

    def execute(self):

        next_ = self.emulator.instruction_memory.get((self.emulator.instr_pointer.get() + 1) % self.emulator.instruction_memory.size())

        temp = self.emulator.fc_head.get()

        if isinstance(next_, InstructionNopB):
            self.emulator.read_head.set(temp)

        elif isinstance(next_, InstructionNopC):
            self.emulator.write_head.set(temp)

        else:
            self.emulator.instr_pointer.set(temp)

class InstructionJmpHead:

    def __init__(self,emulator):
        self.emulator = emulator

    def execute(self):

        next_ = self.emulator.instruction_memory.get((self.emulator.instr_pointer.get() + 1) % self.emulator.instruction_memory.size())

        temp = self.emulator.cpu.reg_c.read()

        if isinstance(next_, InstructionNopB):
            temp1 = self.emulator.read_head.get()

            self.emulator.read_head.increment(temp)

        elif isinstance(next_, InstructionNopC):
            temp1 = self.emulator.write_head.get()

            self.emulator.write_head.increment(temp)

        else:
            temp1 = self.emulator.instr_pointer.get()

            self.emulator.instr_pointer.increment(temp)

        self.emulator.cpu.reg_c.write(temp1)

class InstructionGetHead:

    def __init__(self,emulator):
        self.emulator = emulator

    def execute(self):

        next_ = self.emulator.instruction_memory.get((self.emulator.instr_pointer.get() + 1) % self.emulator.instruction_memory.size())

        if isinstance(next_, InstructionNopB):
            self.emulator.cpu.reg_c.write(self.emulator.read_head.get())

        elif isinstance(next_, InstructionNopC):
            self.emulator.cpu.reg_c.write(self.emulator.write_head.get())

        else:
            self.emulator.cpu.reg_c.write(self.emulator.instr_pointer.get())

class InstructionSetFlow:

    def __init__(self,emulator):
        self.emulator = emulator

    def execute(self):

        next_ = self.emulator.instruction_memory.get((self.emulator.instr_pointer.get() + 1) % self.emulator.instruction_memory.size())

        if isinstance(next_, InstructionNopA):
            self.emulator.fc_head.set(self.emulator.cpu.reg_a.read())
        elif isinstance(next_, InstructionNopB):
            self.emulator.fc_head.set(self.emulator.cpu.reg_b.read())
        else:
            self.emulator.fc_head.set(self.emulator.cpu.reg_c.read())

class InstructionIfLabel:

    def __init__(self,emulator):
        self.emulator = emulator

    def execute(self):

        # 1: Read in the template

        iterator = (self.emulator.instr_pointer.get() + 1) % self.emulator.instruction_memory.size()

        template = []

        while self.emulator.original_memory[iterator] == 0 or self.emulator.original_memory[iterator] == 1 or self.emulator.original_memory[iterator] == 2:
            template.append(self.emulator.original_memory[iterator])
            iterator += 1
            iterator = iterator % self.emulator.instruction_memory.size()

        # If template is empty, there is nothing to compare here.
        # Skip next instruction

        if len(template) == 0:

            self.emulator.instr_pointer.increment(2)

            self.emulator.instr_pointer.set(self.emulator.instr_pointer.get() % self.emulator.instruction_memory.size())


        # Otherwise:
        # Check if the most recent series of copied instructions is the
        # complement of this template.

        else:

            to_match = [(element + 1) % 3 for element in template]

            """

            start = self.emulator.write_head.get() - len(to_match)

            end = self.emulator.write_head.get()

            most_recent = self.emulator.program[start:end]
            
            """

            most_recent = self.emulator.copied[len(self.emulator.copied)-len(to_match):]

            temp = self.emulator.instr_pointer.get()

            if to_match == most_recent:

                self.emulator.instr_pointer.set((temp + len(to_match) + 1) % self.emulator.instruction_memory.size())

            else:

                self.emulator.instr_pointer.set((temp + len(to_match) + 2) % self.emulator.instruction_memory.size())

# %%

class CPUEmulator:

    def __init__(self, a = 0, b = 0, c = 0, mutation_prob = 0, ins_prob = 0, del_prob = 0):
        self.kill = False
        self.deathloop = []
        self.deathcounter = 0
        self.death = [0,0,0]
        self.cpu = CPU(a,b,c)
        #multiprocessing.Process(target=CPUEmulator)
        # self.instruction_memory contains the instructions as objects
        self.instruction_memory = Memory()

        # Current state of memory. Instructions are letters in an alphabet. Can be modified by h-alloc and h-copy.
        self.memory = []

        # Helper list. Contains the copied instructions. Used in If-label
        self.copied = []

        # Equivalent to memory, only the instructions aren't objects, but letters in an alphabet
        self.original_memory = []

        self.instr_pointer = InstructionPointer()
        self.read_head = ReadHead()
        self.write_head = WriteHead()
        self.fc_head = FlowControlHead()

        self.age = 0

        # The emulator needs to store a reference to the mediator object
        # or rather, an abstract mediator object (the interface)

        self.mediator = Mediator()

        # Divide needs to fail if the parent has not allocated memory

        self.allocated = False

        # Probability of random mutation upon h_copy
        self.mutation_prob = mutation_prob

        # Probabilities of random insertion/deletion upon division
        self.ins_prob = ins_prob
        self.del_prob = del_prob

        self.child_rate = 1

        self.fun_not = False
        self.fun_nand = False
        self.fun_and = False
        self.fun_or_n = False
        self.fun_or = False
        self.fun_and_n = False
        self.fun_nor = False
        self.fun_xor = False
        self.fun_equ = False
        self.fun_not_2 = False
        self.fun_nand_2 = False
        self.fun_and_2 = False
        self.fun_or_n_2 = False
        self.fun_or_2 = False
        self.fun_and_n_2 = False
        self.fun_nor_2 = False
        self.fun_xor_2 = False
        self.fun_equ_2 = False

    def clear(self):

        self.cpu.clear()
        self.instruction_memory.wipe()
        self.instr_pointer.set(0)
        self.read_head.set(0)
        self.write_head.set(0)
        self.fc_head.set(0)
        self.memory = []
        self.original_memory = []
        self.copied = []
        self.allocated = False

    def load_program(self, p):

        self.clear()

        # Check if what we're trying to read is an instance od type "Program"
        if not isinstance(p, Program):
            raise NotImplementedError
            print("In Machine.read_program(p), p is not an instance of Program")
        
        # Instantiate memory, original_memory and instruction_memory
        self.memory = p.instructions.copy()
        self.original_memory = p.instructions.copy()

        for instruction in self.original_memory:

            if instruction == 0:
                self.instruction_memory.append(InstructionNopA(self))

            elif instruction == 1:
                self.instruction_memory.append(InstructionNopB(self))

            elif instruction == 2:
                self.instruction_memory.append(InstructionNopC(self))

            elif instruction == 3:
                self.instruction_memory.append(InstructionIfNEq(self))

            elif instruction == 4:
                self.instruction_memory.append(InstructionIfLess(self))

            elif instruction == 5:
                self.instruction_memory.append(InstructionSwap(self))

            elif instruction == 6:
                self.instruction_memory.append(InstructionPop(self))

            elif instruction == 7:
                self.instruction_memory.append(InstructionPush(self))

            elif instruction == 8:
                self.instruction_memory.append(InstructionSwapStack(self))

            elif instruction == 9:
                self.instruction_memory.append(InstructionRightShift(self))

            elif instruction == 10:
                self.instruction_memory.append(InstructionLeftShift(self))

            elif instruction == 11:
                self.instruction_memory.append(InstructionInc(self))

            elif instruction == 12:
                self.instruction_memory.append(InstructionDec(self))

            elif instruction == 13:
                self.instruction_memory.append(InstructionAdd(self))

            elif instruction == 14:
                self.instruction_memory.append(InstructionSub(self))

            elif instruction == 15:
                self.instruction_memory.append(InstructionNand(self))

            elif instruction == 16:
                self.instruction_memory.append(InstructionHAlloc(self))

            elif instruction == 17:
                self.instruction_memory.append(InstructionHDivide(self))

            elif instruction == 18:
                self.instruction_memory.append(InstructionIO(self))

            elif instruction == 19:
                self.instruction_memory.append(InstructionHCopy(self))

            elif instruction == 20:
                self.instruction_memory.append(InstructionHSearch(self))

            elif instruction == 21:
                self.instruction_memory.append(InstructionMovHead(self))

            elif instruction == 22:
                self.instruction_memory.append(InstructionJmpHead(self))

            elif instruction == 23:
                self.instruction_memory.append(InstructionGetHead(self))

            elif instruction == 24:
                self.instruction_memory.append(InstructionSetFlow(self))

            elif instruction == 25:
                self.instruction_memory.append(InstructionIfLabel(self))

    def execute_instruction(self):

        self.instr_pointer.set(self.instr_pointer.get() % self.instruction_memory.size())
        #print("instr_pointer",self.instr_pointer.get())
        #print("size",self.instruction_memory.size())
        ip = self.instr_pointer.get()

        self.instruction_memory.get(ip).execute()

        self.age += 1
        if self.age > 40000:
            self.mediator.notify(sender=self, event="death", result=None)

        #    self.kill = True
        if(self.age >= 14*self.instruction_memory.size()):
            if(self.age<=self.instruction_memory.size()+5):
                self.deathloop.append(self.instr_pointer.get())
            if(len(self.deathloop)>0):
                if(self.instr_pointer.get()==0):
                    pass
                elif (self.instr_pointer.get() == 1):
                    pass
                elif (self.instr_pointer.get() == 2):
                    pass
                else:
                    if(self.age > self.instruction_memory.size()+6):
                        if(self.deathloop[0]==self.instr_pointer.get()) and self.death[1]==0 & self.death[2]==0:
                            self.death[0]=1
                        else:
                            self.death[0]=0
                        if(self.death[0]==1):
                            if (self.deathloop[1] == self.instr_pointer.get()):
                                self.death[1]=1
                            else:
                                self.death[0]=0
                                self.death[1]=0
                        if (self.death[1] == 1):
                            if (self.deathloop[2] == self.instr_pointer.get()):
                                self.death[2] = 1
                                self.deathcounter+=1
                            else:
                                self.death[0] = 0
                                self.death[1] = 0
                                self.death[2] = 0
                        if self.deathcounter >5:
                            self.kill = True
                            #print('killed cell that was in death_loop with age',self.age)
                            #print("killed endless loop organism")
                            self.mediator.notify(sender=self, event="death",result = None)
                #if (self.deathloop[2] == self.instr_pointer.get()):
                #if (self.deathloop[3] == self.instr_pointer.get()):

        if self.instr_pointer.get() == ip:
            self.instr_pointer.increment()

        #print('instr.pointer', self.instr_pointer.get())
        #print("cpu_position",self.cpu.position)

    # Obsolete
    def execute_program(self):

        while self.instr_pointer.get() < self.instruction_memory.size():

            # Save current instruction pointer value to later check if it was explicitly changed by an instruction
            temp = self.instr_pointer.get()

            print("Executing instruction " + str(temp))

            self.instruction_memory.get(self.instr_pointer.get()).execute()

            # If the IP wasn't changed by an instruction, increase by 1, otherwise leave it
            if self.instr_pointer.get() == temp:
                self.instr_pointer.increment()


    # A string representation of the state of the machine
    def __str__(self):
        string_representation = "\nRegister A: " + str(self.cpu.reg_a.read()) + "\nRegister B: " + str(
            self.cpu.reg_b.read()) + "\nRegister C: " + str(
            self.cpu.reg_c.read()) + "\nInstruction Pointer: " + str(
            self.instr_pointer.get()) + "\n" + "Memory: " + str(
            self.original_memory) + "\n" + "Age: " + str(
            self.age) + "\n"

        return string_representation