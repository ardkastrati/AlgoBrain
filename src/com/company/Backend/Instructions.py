#%% Necessary Imports

# For the probability of random mutations
from scipy.stats import bernoulli
from random import randrange
from numpy import random

# %% The Program Class

class Program:

    # A class for AVIDA programs
    # A list of any size, the only restriction is that the elements must be integers in {0,1,...,25}

    def check_validity(self, instr_list):

        for instruction in instr_list:
            assert instruction in range(31)

    def __init__(self, instr_list):

        self.check_validity(instr_list)

        self.instructions = instr_list
# %% The Vanilla Instructions

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
            self.machine.reg_a.write(self.machine.reg_a.read() >> 1)

        elif isinstance(next_, InstructionNopC):
            self.machine.reg_c.write(self.machine.reg_c.read() >> 1)

        else:
            self.machine.reg_b.write(self.machine.reg_b.read() >> 1)

class InstructionLeftShift:

    def __init__(self, emulator):

        self.emulator = emulator
        self.machine = emulator.cpu

    def execute(self):

        next_ = self.emulator.instruction_memory.get((self.emulator.instr_pointer.get() + 1) % self.emulator.instruction_memory.size())

        if isinstance(next_, InstructionNopA):
            self.machine.reg_a.write(self.machine.reg_a.read() << 1)

        elif isinstance(next_, InstructionNopC):
            self.machine.reg_c.write(self.machine.reg_c.read() << 1)

        else:
            self.machine.reg_b.write(self.machine.reg_b.read() << 1)

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

        nand = ~(self.machine.reg_b.read() & self.machine.reg_c.read())

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
            
                #result = self.emulator.memory[rh:wh]
                result = self.emulator.copied

                #original = self.emulator.memory[:rh]
                original = self.emulator.original_memory

                # Conditions under which H-Divide fails:
                # Parent or offspring remain with fewer than 10 instructions
                # <70% of the parent was executed
                # <70% of the memory allocated for the child was copied into
                # The resulting organism wouldn't be able to divide
                if len(original) < 10 or len(result) < 10 or\
                    (self.emulator.instr_pointer.get() % self.emulator.instruction_memory.size())/self.emulator.instruction_memory.size() < 0.7 or\
                    len(result) < 0.95 * len(original):
                        # or not 17 in result or 17 not in original:
                    
                    pass

                else:
                    
                    # Fully reset the state of the emulator (except age)
                    self.emulator.load_program(Program(original))
                    
                    mutated = False

                    # Insertion mutations
                    chance = bernoulli.rvs(self.emulator.ins_prob, size=1)
                    
                    # Check which instruction set is being used
                    
                    if self.emulator.mediator.instruction_set == "default":
                        max_instr = 26
                    else:
                        max_instr = 28

                    if chance == 1:
                        location = random.randint(0, len(result))
                        insertion =  randrange(max_instr)
                        result.insert(location, insertion)
                        self.emulator.child_mutations.append(["I",location,insertion, self.emulator.generation])
                        mutated = True
                    else:
                        pass

                    # Deletion mutations
                    chance = bernoulli.rvs(self.emulator.del_prob, size=1)

                    if chance == 1 and not mutated:
                        location = random.randint(0, len(result))
                        self.emulator.child_mutations.append(["D", location, self.emulator.generation])
                        del result[location]
                    else:
                        pass
                    
                    ## Save old child rate to reset to after division
                    #old_rate = self.emulator.child_rate
                    
                    # Update the child rate s.t. it's proportional to its genome length
                    #self.emulator.child_rate *= len(result)
                    #self.emulator.child_rate *= len(result)

                    # Notify the world about the division
                    self.emulator.mediator.notify(sender = self.emulator, event = "division", result = result)
                    
                    # Restore child_rate to old_rate
                    #self.emulator.child_rate = old_rate

                    # Memory is no longer allocated
                    self.emulator.allocated = False
                    
                    # Reset child_mutations to an empty list
                    self.emulator.child_mutations = []
                    
                    # Note: rewarding the sender if necessary is fully delegated 
                    # to the mediator

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

        # get: return value from input buffer into ?BX? IFF input buffer not empty
        if not self.emulator.cpu.input_buffer.empty():
            
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
                
                # Mutations
                chance = bernoulli.rvs(self.emulator.mutation_prob, size=1)
                
                if self.emulator.mediator.instruction_set == "default":
                    max_instr = 26
                else:
                    max_instr = 28

                if chance == 1:
                    location = self.emulator.read_head.get()
                    temp = randrange(max_instr)
                    self.emulator.child_mutations.append(["C", location, temp, self.emulator.generation])
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

            most_recent = self.emulator.copied[len(self.emulator.copied)-len(to_match):]

            temp = self.emulator.instr_pointer.get()

            if to_match == most_recent:
                self.emulator.instr_pointer.set((temp + len(to_match) + 1) % self.emulator.instruction_memory.size())

            else:
                self.emulator.instr_pointer.set((temp + len(to_match) + 2) % self.emulator.instruction_memory.size())
  
#%% New Instructions:
    
class InstructionConsume:
    
    def __init__(self,emulator):
        self.emulator = emulator
        
    def execute(self):
        
        """
        The emulator fully consumes a less fit emulator from the neighborhood.
        Fitness here defined as rate * length
        The instructions of the smaller emulator are appended to after the consume instruction
        """
        self.emulator.mediator.notify(sender = self.emulator, event = "consume", result = None)

class InstructionMove:
    
    def __init__(self,emulator):
        self.emulator = emulator
        
    def execute(self):
        
        dice = randrange(4)
        
        if dice == 0:
            self.emulator.mediator.notify(sender = self.emulator, event = "mov_up", result = None)
        elif dice == 1:
            self.emulator.mediator.notify(sender = self.emulator, event = "mov_down", result = None)
        elif dice == 2:
            self.emulator.mediator.notify(sender = self.emulator, event = "mov_left", result = None)
        elif dice == 3:
            self.emulator.mediator.notify(sender = self.emulator, event = "mov_right", result = None)

class InstructionSexualReproduction:
    
    def __init__(self,emulator):
        self.emulator = emulator
        
    def execute(self):
        
        # Every reproduction has a certain chance of being successful
        if randrange(64) == 0:
            self.emulator.mediator.notify(sender = self.emulator, event = "feeling_frisky", result = None)