# %%
# Necessary imports:

from queue import LifoQueue
from queue import Queue
from Mediator import Mediator

# For the probability of random mutations
from scipy.stats import bernoulli
from random import randrange

# %% The Program

class Program:

    # AVIDA Program class.

    # An instance of this class is nothing more than a list of instructions in AVIDA.
    # Each instruction is to be interpreted by the "CPUEmulator".
    # The instructions are symbols in an alphabet given by the instruction set.

    # Our instruction set has 26 instructions.
    # The only thing that needs to be checked at the construction of a new Program instance
    # is that all of the elements of the list of instructions are integers in range(0,26)

    # Will check whether the passed list is a valid list of instructions.
    def check_Validity(self, instr_list):
        i = 0
        for instruction in instr_list:
            i += 1

            if instruction < 0 or instruction > 25 or int(instruction) != instruction:
                print("Invalid instruction at index " + str(i))
                raise NotImplementedError


    def __init__(self, instr_list):

        self.check_Validity(instr_list)

        self.instructions = instr_list

# %% The Register Class

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

    def get(self):
        return self.value

    def increment(self, a = 1):
        self.value += a

    def set(self,a):
        
        assert isinstance(a,int)
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

    def set(self,a):
        self.value = a

    def get(self):
        return self.value

# %% The Metabolic Rate

class MetabolicRate:

    def __init__(self):
        self.rate = 1

    def set(self,a):
        self.rate = a

    def get(self):
        return self.rate

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
        self.input_1 = 0
        self.input_2 = 0
        self.count = 0
        self.active_stack = self.stack0

        self.input_buffer = Queue()
        self.output_buffer = Queue()
        self.temp = self.reg_b

    def input_update(self, value):

        if self.count == 0:
            self.input_1 = value
            self.count = 1
        else:
            self.input_2 = value
            self.count = 0
    def get_input(self):

        if self.count == 0:
            self.count = 1
            return self.input_1
        else:
            self.count = 0
            return self.input_2

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

        next = self.emulator.memory.get((self.emulator.instr_pointer.get() + 1) % self.emulator.memory.size())

        if isinstance(next, InstructionNopA):
            if self.machine.reg_a.read() != self.machine.reg_b.read():
                pass
            else:
                self.emulator.instr_pointer.increment(2)

        elif isinstance(next, InstructionNopC):
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

        next = self.emulator.memory.get((self.emulator.instr_pointer.get() + 1) % self.emulator.memory.size())

        if isinstance(next, InstructionNopA):
            if self.machine.reg_a.read() < self.machine.reg_b.read():
                pass
            else:
                self.emulator.instr_pointer.increment(2)

        elif isinstance(next, InstructionNopC):
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

        next = self.emulator.memory.get((self.emulator.instr_pointer.get() + 1) % self.emulator.memory.size())

        if isinstance(next, InstructionNopA):
            temp = self.emulator.cpu.reg_a.read()
            self.emulator.cpu.reg_a.write(self.emulator.cpu.reg_b.read())
            self.emulator.cpu.reg_b.write(temp)

        elif isinstance(next, InstructionNopC):
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

        next = self.emulator.memory.get((self.emulator.instr_pointer.get() + 1) % self.emulator.memory.size())

        # Making sure that if the stack is empty, pop returns a 0 and not an exception
        # as is defined in the implementation of the LifoQueue()

        if self.machine.active_stack.empty():
            temp = 0
        else:
            temp = self.machine.active_stack.get()

        if isinstance(next, InstructionNopA):
            self.machine.reg_a.write(temp)

        elif isinstance(next, InstructionNopC):
            self.machine.reg_c.write(temp)

        else:
            self.machine.reg_b.write(temp)

class InstructionPush:

    def __init__(self, emulator):

        self.emulator = emulator
        self.machine = emulator.cpu

    def execute(self):

        next = self.emulator.memory.get((self.emulator.instr_pointer.get() + 1) % self.emulator.memory.size())

        if isinstance(next, InstructionNopA):
            self.machine.active_stack.put(self.machine.reg_a.read())

        elif isinstance(next, InstructionNopC):
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

        next = self.emulator.memory.get((self.emulator.instr_pointer.get() + 1) % self.emulator.memory.size())

        if isinstance(next, InstructionNopA):
            self.machine.reg_a.write(self.machine.reg_a.read() >> 1)

        elif isinstance(next, InstructionNopC):
            self.machine.reg_c.write(self.machine.reg_c.read() >> 1)

        else:
            self.machine.reg_b.write(self.machine.reg_b.read() >> 1)

class InstructionLeftShift:

    def __init__(self, emulator):

        self.emulator = emulator
        self.machine = emulator.cpu

    def execute(self):

        next = self.emulator.memory.get((self.emulator.instr_pointer.get() + 1) % self.emulator.memory.size())

        if isinstance(next, InstructionNopA):
            self.machine.reg_a.write(self.machine.reg_a.read() << 1)

        elif isinstance(next, InstructionNopC):
            self.machine.reg_c.write(self.machine.reg_c.read() << 1)

        else:
            self.machine.reg_b.write(self.machine.reg_b.read() << 1)

class InstructionInc:

    def __init__(self, emulator):
        self.emulator = emulator

    def execute(self):

        next = self.emulator.memory.get((self.emulator.instr_pointer.get() + 1) % self.emulator.memory.size())

        if isinstance(next, InstructionNopA):
            self.emulator.cpu.reg_a.increment()

        elif isinstance(next, InstructionNopC):
            self.emulator.cpu.reg_c.increment()

        else:
            self.emulator.cpu.reg_b.increment()

class InstructionDec:

    def __init__(self, emulator):
        self.emulator = emulator
        self.machine = emulator.cpu

    def execute(self):

        next = self.emulator.memory.get((self.emulator.instr_pointer.get() + 1) % self.emulator.memory.size())

        if isinstance(next, InstructionNopA):
            self.machine.reg_a.decrement()

        elif isinstance(next, InstructionNopC):
            self.emulator.cpu.reg_c.decrement()

        else:
            self.emulator.cpu.reg_b.decrement()

class InstructionAdd:

    def __init__(self, emulator):
        self.emulator = emulator
        self.machine = emulator.cpu

    def execute(self):

        next = self.emulator.memory.get((self.emulator.instr_pointer.get() + 1) % self.emulator.memory.size())

        sum = self.machine.reg_b.read() + self.machine.reg_c.read()

        if isinstance(next, InstructionNopA):
            self.machine.reg_a.write(sum)

        elif isinstance(next, InstructionNopC):
            self.machine.reg_c.write(sum)

        else:
            self.machine.reg_b.write(sum)

class InstructionSub:

    def __init__(self, emulator):
        self.emulator = emulator
        self.machine = emulator.cpu

    def execute(self):

        next = self.emulator.memory.get((self.emulator.instr_pointer.get() + 1) % self.emulator.memory.size())

        diff = self.machine.reg_b.read() - self.machine.reg_c.read()

        if isinstance(next, InstructionNopA):
            self.machine.reg_a.write(diff)

        elif isinstance(next, InstructionNopC):
            self.machine.reg_c.write(diff)

        else:
            self.machine.reg_b.write(diff)

class InstructionNand:

    def __init__(self, emulator):
        self.emulator = emulator
        self.machine = emulator.cpu

    def execute(self):

        next = self.emulator.memory.get((self.emulator.instr_pointer.get() + 1) % self.emulator.memory.size())

        nand = ~(self.machine.reg_b.read() & self.machine.reg_c.read())

        if isinstance(next, InstructionNopA):
            self.machine.reg_a.write(nand)

        elif isinstance(next, InstructionNopC):
            self.machine.reg_c.write(nand)

        else:
            self.machine.reg_b.write(nand)

class InstructionHAlloc:

    def __init__(self, emulator):
        self.emulator = emulator

    def execute(self):
        
        # An organism can only allocate memory once

        if self.emulator.allocated == False:
            
            for i in range(0, self.emulator.memory.size()):
                self.emulator.program.append(0)

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

                result = []
                iterator = self.emulator.read_head.get()

                while iterator < self.emulator.write_head.get():
                    result.append(self.emulator.program[iterator])
                    iterator += 1

                original = Program(self.emulator.original_program)
                # Fully reset the state of the emulator (except age)
                self.emulator.load_program(original)
                
                if len(result) > 10 :
                
                    self.emulator.mediator.notify(sender = self.emulator, event = "division", result = result)
                
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

        next = self.emulator.memory.get((self.emulator.instr_pointer.get() + 1) % self.emulator.memory.size())
        
        # put: place ?BX? instance in the output buffer and set register used to 0
        if isinstance(next, InstructionNopA):
            self.emulator.cpu.output_buffer.put(self.emulator.cpu.reg_a.read())
            self.emulator.cpu.reg_a.write(0)

        elif isinstance(next, InstructionNopC):
            self.emulator.cpu.output_buffer.put(self.emulator.cpu.reg_c.read())
            self.emulator.cpu.reg_c.write(0)

        else:
            self.emulator.cpu.output_buffer.put(self.emulator.cpu.reg_b.read())
            self.emulator.cpu.reg_b.write(0)
            
        to_output = self.emulator.cpu.output_buffer.get()

        self.emulator.mediator.notify(sender = self.emulator, event = "IO_operation", result = to_output)

        if isinstance(next, InstructionNopA):
            self.emulator.cpu.input_update(self.emulator.cpu.input_buffer.get())
            self.emulator.cpu.reg_a.write(self.emulator.cpu.get_input())
            #self.emulator.cpu.reg_a.write(self.emulator.cpu.input_buffer.get())

        elif isinstance(next, InstructionNopC):
            self.emulator.cpu.input_update(self.emulator.cpu.input_buffer.get())
            self.emulator.cpu.reg_c.write(self.emulator.cpu.get_input())
            #self.emulator.cpu.reg_c.write(self.emulator.cpu.input_buffer.get())

        else:
            self.emulator.cpu.input_update(self.emulator.cpu.input_buffer.get())
            self.emulator.cpu.reg_b.write(self.emulator.cpu.get_input())
            #self.emulator.cpu.reg_b.write(self.emulator.cpu.input_buffer.get())

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
            
            if self.emulator.read_head.get() < len(self.emulator.original_program) and self.emulator.write_head.get() < len(self.emulator.program):
                
                chance = bernoulli.rvs(self.emulator.mutation_prob, size=1)
                
                if chance == 1:
                    temp = randrange(26)
                else:
                    temp = self.emulator.original_program[self.emulator.read_head.get()]
            
                self.emulator.program[self.emulator.write_head.get()] = temp
                self.emulator.read_head.increment()
                self.emulator.write_head.increment()
                self.emulator.copied.append(temp)
            
            else:
                
                pass

class InstructionHSearch:

    def __init__(self,emulator):
        self.emulator = emulator

    def execute(self):

        end_search_index = self.emulator.instr_pointer.get() % self.emulator.memory.size()

        iterator = (self.emulator.instr_pointer.get() + 1) % self.emulator.memory.size()

        template = []

        while self.emulator.original_program[iterator] == 0 or self.emulator.original_program[iterator] == 1 or self.emulator.original_program[iterator] == 2:
            template.append(self.emulator.original_program[iterator])
            iterator += 1
            iterator = iterator % self.emulator.memory.size()

        if len(template) == 0:

            self.emulator.fc_head.set(end_search_index)
            self.emulator.cpu.reg_b.write(0)
            self.emulator.cpu.reg_c.write(0)

        else:

            to_match = [(element + 1) % 3 for element in template]

            self.emulator.cpu.reg_c.write(len(to_match))

            start_index = (self.emulator.instr_pointer.get() + len(template) + 1) % self.emulator.memory.size()

            iterator_index = start_index

            distance = 2 * len(to_match)

            self.emulator.fc_head.set(end_search_index)

            while(iterator_index != end_search_index):

                candidate_index = iterator_index + len(to_match) % self.emulator.memory.size()
                candidate_template = [self.emulator.original_program[k % self.emulator.memory.size()] for k in range(iterator_index, iterator_index + len(to_match))]

                if candidate_template == to_match:

                    self.emulator.fc_head.set(candidate_index)
                    self.emulator.cpu.reg_b.write(distance)
                    break

                iterator_index += 1
                iterator_index = iterator_index % self.emulator.memory.size()

                distance += 1

class InstructionMovHead:

    def __init__(self,emulator):
        self.emulator = emulator

    def execute(self):

        next = self.emulator.memory.get((self.emulator.instr_pointer.get() + 1) % self.emulator.memory.size())

        temp = self.emulator.fc_head.get()

        if isinstance(next, InstructionNopB):
            self.emulator.read_head.set(temp)

        elif isinstance(next, InstructionNopC):
            self.emulator.write_head.set(temp)

        else:
            self.emulator.instr_pointer.set(temp)

class InstructionJmpHead:

    def __init__(self,emulator):
        self.emulator = emulator

    def execute(self):

        next = self.emulator.memory.get((self.emulator.instr_pointer.get() + 1) % self.emulator.memory.size())

        temp = self.emulator.cpu.reg_c.read()

        if isinstance(next, InstructionNopB):
            temp1 = self.emulator.read_head.get()

            self.emulator.read_head.increment(temp)

        elif isinstance(next, InstructionNopC):
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

        next = self.emulator.memory.get((self.emulator.instr_pointer.get() + 1) % self.emulator.memory.size())

        if isinstance(next, InstructionNopB):
            self.emulator.cpu.reg_c.write(self.emulator.read_head.get())

        elif isinstance(next, InstructionNopC):
            self.emulator.cpu.reg_c.write(self.emulator.write_head.get())

        else:
            self.emulator.cpu.reg_c.write(self.emulator.instr_pointer.get())

class InstructionSetFlow:

    def __init__(self,emulator):
        self.emulator = emulator

    def execute(self):

        next = self.emulator.memory.get((self.emulator.instr_pointer.get() + 1) % self.emulator.memory.size())

        if isinstance(next, InstructionNopA):
            self.emulator.fc_head.set(self.emulator.cpu.reg_a.read())
        elif isinstance(next, InstructionNopB):
            self.emulator.fc_head.set(self.emulator.cpu.reg_b.read())
        else:
            self.emulator.fc_head.set(self.emulator.cpu.reg_c.read())

class InstructionIfLabel:

    def __init__(self,emulator):
        self.emulator = emulator

    def execute(self):

        # 1: Read in the template

        iterator = (self.emulator.instr_pointer.get() + 1) % self.emulator.memory.size()

        template = []

        while self.emulator.original_program[iterator] == 0 or self.emulator.original_program[iterator] == 1 or self.emulator.original_program[iterator] == 2:
            template.append(self.emulator.original_program[iterator])
            iterator += 1
            iterator = iterator % self.emulator.memory.size()

        # If template is empty, there is nothing to compare here.
        # Skip next instruction

        if len(template) == 0:

            self.emulator.instr_pointer.increment(2)

            self.emulator.instr_pointer.set(self.emulator.instr_pointer.get() % self.emulator.memory.size())


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

                self.emulator.instr_pointer.set((temp + len(to_match) + 1) % self.emulator.memory.size())

            else:
                self.emulator.instr_pointer.set((temp + len(to_match) + 2) % self.emulator.memory.size())

# %%

class CPUEmulator:

    def __init__(self, a = 0, b = 0, c = 0, mutation_prob = 0, insertion_prob = 0, deletion_prob = 0):

        self.cpu = CPU(a,b,c)

        self.memory = Memory()

        # Current program. Can be modified by h-alloc and h-copy.
        self.program = []
        
        # Helper list. Contains the copied instructions. Used in If-label
        self.copied = []

        # Originally loaded program. Used to return to start state after h-divide
        self.original_program = []

        self.instr_pointer = InstructionPointer()
        self.read_head = ReadHead()
        self.write_head = WriteHead()
        self.fc_head = FlowControlHead()

        self.metabolic_rate = MetabolicRate()

        self.age = 0

        # The emulator needs to store a reference to the mediator object
        # or rather, an abstract mediator object (the interface)

        self.mediator = Mediator()

        # Divide needs to fail if the parent has not allocated memory

        self.allocated = False

        # Probability of random mutation upon h_copy
        self.mutation_prob = mutation_prob

        # Probabilities of random insertion/deletion upon division
        self.insertion_prob = insertion_prob
        self.deletion_prob = deletion_prob

    def clear(self):

        self.memory.wipe()
        self.instr_pointer.set(0)
        self.read_head.set(0)
        self.write_head.set(0)
        self.fc_head.set(0)
        self.program = []
        self.original_program = []
        self.cpu.clear()

    def load_program(self, p):

        self.clear()

        # Check if what we're trying to read is an instance od type "Program"
        if not isinstance(p, Program):
            raise NotImplementedError
            print("In Machine.read_program(p), p is not an instance of Program")

        self.program = p.instructions.copy()
        self.original_program = p.instructions.copy()

        for instruction in self.program:

            if instruction == 0:
                self.memory.append(InstructionNopA(self))

            elif instruction == 1:
                self.memory.append(InstructionNopB(self))

            elif instruction == 2:
                self.memory.append(InstructionNopC(self))

            elif instruction == 3:
                self.memory.append(InstructionIfNEq(self))

            elif instruction == 4:
                self.memory.append(InstructionIfLess(self))

            elif instruction == 5:
                self.memory.append(InstructionSwap(self))

            elif instruction == 6:
                self.memory.append(InstructionPop(self))

            elif instruction == 7:
                self.memory.append(InstructionPush(self))

            elif instruction == 8:
                self.memory.append(InstructionSwapStack(self))

            elif instruction == 9:
                self.memory.append(InstructionRightShift(self))

            elif instruction == 10:
                self.memory.append(InstructionLeftShift(self))

            elif instruction == 11:
                self.memory.append(InstructionInc(self))

            elif instruction == 12:
                self.memory.append(InstructionDec(self))

            elif instruction == 13:
                self.memory.append(InstructionAdd(self))

            elif instruction == 14:
                self.memory.append(InstructionSub(self))

            elif instruction == 15:
                self.memory.append(InstructionNand(self))

            elif instruction == 16:
                self.memory.append(InstructionHAlloc(self))

            elif instruction == 17:
                self.memory.append(InstructionHDivide(self))

            elif instruction == 18:
                self.memory.append(InstructionIO(self))

            elif instruction == 19:
                self.memory.append(InstructionHCopy(self))

            elif instruction == 20:
                self.memory.append(InstructionHSearch(self))

            elif instruction == 21:
                self.memory.append(InstructionMovHead(self))

            elif instruction == 22:
                self.memory.append(InstructionJmpHead(self))

            elif instruction == 23:
                self.memory.append(InstructionGetHead(self))

            elif instruction == 24:
                self.memory.append(InstructionSetFlow(self))

            elif instruction == 25:
                self.memory.append(InstructionIfLabel(self))

    def execute_instruction(self):

        self.instr_pointer.set(self.instr_pointer.get() % self.memory.size())

        ip = self.instr_pointer.get()

        self.memory.get(ip).execute()

        self.age += 1

        if self.instr_pointer.get() == ip:
            self.instr_pointer.increment()

    # Obsolete
    def execute_program(self):

        while self.instr_pointer.get() < self.memory.size():

            # Save current instruction pointer value to later check if it was explicitly changed by an instruction
            temp = self.instr_pointer.get()

            print("Executing instruction " + str(temp))

            self.memory.get(self.instr_pointer.get()).execute()

            # If the IP wasn't changed by an instruction, increase by 1, otherwise leave it
            if self.instr_pointer.get() == temp:
                self.instr_pointer.increment()


    # A string representation of the state of the machine
    def __str__(self):
        string_representation = "\nRegister A: " + str(self.cpu.reg_a.read()) + "\nRegister B: " + str(
            self.cpu.reg_b.read()) + "\nRegister C: " + str(
            self.cpu.reg_c.read()) + "\nInstruction Pointer: " + str(
            self.instr_pointer.get()) + "\n" + "Memory: " + str(
            self.program) + "\n" + "Age: " + str(
            self.age) + "\n"

        return string_representation
