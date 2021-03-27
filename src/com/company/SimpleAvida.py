# TODO: This is a big and general one. DOCUMENT THE CODE BETTER.
# Write a full documentation. It will reveal itself once we have a functional system.

# %%
# Keeping track of all the imports we'll need
from queue import LifoQueue
from queue import Queue

# Should we define separate classes for Stacks and Buffers too maybe?
# Probably.


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
                
            
        # We can surely do this with assertions. Is it the optimal way to do it though?
    
    # The constructor
    def __init__(self, instr_list):
        
        self.check_Validity(instr_list)

        self.instructions = instr_list
        
# %% The Registers

class Register:
    
    # Default initialization to 0
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

class FlowControlHead:
    
    def __init__(self):
        self.value = 0
        
    def increment(self, a = 1):
        self.value += a
        
    def set(self,a):
        self.value = a
        
    def get(self):
        return self.value

# %% The Memory

class Memory:
    
    def __init__(self):
        self.content = []
    
    # Write, as of now, just fully replaces the memory with the argument of this function.
    # A slower but maybe more reasonable implementation would iterate
    # over a list that we'd pass here as an argument and write the elements of it one by one
    def write(self,value):
        self.content = value
        
    # Wipe the memory completely
    def wipe(self):
        self.content = []
        
    def size(self):
        return len(self.content)
    
    def get(self,index):
        return self.content[index]
    
    def read(self):
        return self.content
    
    def append(self,value):
        self.content.append(value)
    
# %% The CPU

class CPU:
    
    # Should we define getters and setters for all of the components of the CPU
    # or just acces them directly? For now, it's direct access
    
    def __init__(self, a, b, c):
         
        # The three registers:
        self.reg_a = Register(a)
        self.reg_b = Register(b)
        self.reg_c = Register(c)
        
        # The two stacks. Only one is active at a time.
        # By default it is stack0 in the beginning.
        self.stack0 = LifoQueue()
        self.stack1 = LifoQueue()
        
        # active_stack is a pointer to the currently active stack.
        self.active_stack = self.stack0
        
        # The input and output buffers. Implemented as FIFO Queues
        self.input_buffer = Queue()
        self.output_buffer = Queue()
        
        # OPEN QUESTION: How to approach the task of the reward system?
        # We have no restrictions on the machines at the moment.
        
# %%

# TODO: Template matching and nop's as modifiers for all instructions
# TODO: Test the instructions

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
        
        if self.emulator.instr_pointer.get() >= self.emulator.memory.size() - 1:
            next = 0
        else:
            next = self.emulator.memory.get(self.emulator.instr_pointer.get() + 1)
        
        if isinstance(next, InstructionNopA):
            if self.machine.reg_a.read() != self.machine.reg_b.read():
                pass
            else:
                self.machine.instr_pointer.increment(2)
                
        elif isinstance(next, InstructionNopC):
            if self.machine.reg_c.read() != self.machine.reg_a.read():
                pass
            else:
                self.machine.instr_pointer.increment(2)
                
        else:
            if self.machine.reg_b.read() != self.machine.reg_c.read():
                pass
            else:
                self.emulator.instr_pointer.increment(2)
            

class InstructionIfLess:
    
    def __init__(self, emulator):
        
        self.machine = emulator.cpu

    
    def execute(self,machine):
        
        if self.emulator.instr_pointer.get() >= self.emulator.memory.size() - 1:
            next = 0
        else:
            next = self.emulator.memory.get(self.emulator.instr_pointer.get() + 1)
        
        if isinstance(next, InstructionNopA):
            if self.machine.reg_a.get() < self.machine.reg_b.get():
                pass
            else:
                self.machine.instr_pointer.increment(2)
                
        elif isinstance(next, InstructionNopC):
            if self.machine.reg_c.get() < self.machine.reg_a.get():
                pass
            else:
                self.machine.instr_pointer.increment(2)
                
        else:
            if self.machine.reg_b.get() < self.machine.reg_c.get():
                pass
            else:
                self.machine.instr_pointer.increment(2)
        
        
        
class InstructionSwap:
    
    def __init__(self, emulator):
        self.emulator = emulator

    def execute(self):
        
        # Getting the next instruction to check if it's a nop modifier
        # Just the else: part will be necessary once we have circular memory
        # The next = 0 part is there just to make the whole thing work
        if self.emulator.instr_pointer.get() >= self.emulator.memory.size() - 1:
            next = 0
        else:
            next = self.emulator.memory.get(self.emulator.instr_pointer.get() + 1)
            
        
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
        
        if self.emulator.instr_pointer.get() >= self.emulator.memory.size() - 1:
            next = 0
        else:
            next = self.emulator.memory.get(self.emulator.instr_pointer.get() + 1)
        
        # Making sure that if the stack is empty, pop returns a 0 and not an exception
        # as is defined in the implementation of the LifoQueue()
        # QUESTION: Should we define a class stack instead of using
        # a ready-made implementation?
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
            
        
        #self.machine.reg_b.write(temp)
        
class InstructionPush:
    
    def __init__(self, emulator):
        
        self.emulator = emulator
        self.machine = emulator.cpu
        
    def execute(self):
        
        if self.emulator.instr_pointer.get() >= self.emulator.memory.size() - 1:
            next = 0
        else:
            next = self.emulator.memory.get(self.emulator.instr_pointer.get() + 1)
            
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
            self.machine.active_stack= self.machine.stack1
        else:
            self.machine.active_stack = self.machine.stack0
            

class InstructionRightShift:
    
     def __init__(self, emulator):
         
         self.emulator = emulator
         self.machine = emulator.cpu
     
     def execute(self):
         
        if self.emulator.instr_pointer.get() >= self.emulator.memory.size() - 1:
            next = 0
        else:
            next = self.emulator.memory.get(self.emulator.instr_pointer.get() + 1)
            
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
        
        if self.emulator.instr_pointer.get() >= self.emulator.memory.size() - 1:
            next = 0
        else:
            next = self.emulator.memory.get(self.emulator.instr_pointer.get() + 1)
            
            
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
        
        if self.emulator.instr_pointer.get() >= self.emulator.memory.size() - 1:
            next = 0
        else:
            next = self.emulator.memory.get(self.emulator.instr_pointer.get() + 1)
            
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
        
        if self.emulator.instr_pointer.get() >= self.emulator.memory.size() - 1:
            next = 0
        else:
            next = self.emulator.memory.get(self.emulator.instr_pointer.get() + 1)
        
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
        
        if self.emulator.instr_pointer.get() >= self.emulator.memory.size() - 1:
            next = 0
        else:
            next = self.emulator.memory.get(self.emulator.instr_pointer.get() + 1)
            
        if isinstance(next, InstructionNopA):
            self.machine.reg_a.write(self.machine.reg_b.read() + self.machine.reg_c.read())
                
        elif isinstance(next, InstructionNopC):
            self.machine.reg_c.write(self.machine.reg_b.read() + self.machine.reg_c.read())
                
        else:
            self.machine.reg_b.write(self.machine.reg_b.read() + self.machine.reg_c.read())
            
        
         
class InstructionSub:
    
    def __init__(self, emulator):
        self.emulator = emulator
        self.machine = emulator.cpu
    
    def execute(self):
        
        if self.emulator.instr_pointer.get() >= self.emulator.memory.size() - 1:
            next = 0
        else:
            next = self.emulator.memory.get(self.emulator.instr_pointer.get() + 1)
            
        if isinstance(next, InstructionNopA):
            self.machine.reg_a.write(self.machine.reg_b.read() - self.machine.reg_c.read())
                
        elif isinstance(next, InstructionNopC):
            self.machine.reg_c.write(self.machine.reg_b.read() - self.machine.reg_c.read())
                
        else:
            self.machine.reg_b.write(self.machine.reg_b.read() - self.machine.reg_c.read())
        
class InstructionNand:
    
    def __init__(self, emulator):
        self.emulator = emulator
        self.machine = emulator.cpu
    
    def execute(self):
        
        if self.emulator.instr_pointer.get() >= self.emulator.memory.size() - 1:
            next = 0
        else:
            next = self.emulator.memory.get(self.emulator.instr_pointer.get() + 1)
            
        if isinstance(next, InstructionNopA):
            self.machine.reg_a.write(self.machine.reg_b.read() - self.machine.reg_c.read())
                
        elif isinstance(next, InstructionNopC):
            self.machine.reg_c.write(self.machine.reg_b.read() - self.machine.reg_c.read())
                
        else:
            self.machine.reg_b.write(self.machine.reg_b.read() - self.machine.reg_c.read())
        
# Allocate the maximum number of instructions that a child organism may have on divide
# Hard code to 10 right now
class InstructionHAlloc:
    
    def __init__(self, emulator):
        self.emulator = emulator
    
    def execute(self):
        self.emulator.memory_size = self.emulator.memory_size + self.emulator.memory_size_child

# Split off the instructions between the Read-Head and the Write-Head
# and turn them into a new organism.

# We'll see how this should work exactly
class InstructionHDivide:
    
    def __init__(self,emulator):
        self.emulator = emulator
    
    def execute(self):        
        temp = []
        iterator = self.emulator.read_head.get()
        
        while iterator < self.emulator.write_head.get():
            temp.append(self.emulator.program[iterator])
            iterator += 1
            
        result = Program(temp)
        return result
            

# Don't care right now. When we have an Avida world we'll test it
class InstructionIO:
    
    def __init__(self,emulator):
        self.emulator = emulator
    
    def execute(self):
        pass
    
# Copy an instruction from the Read-Head to the Write-Head
class InstructionHCopy:
    
    def __init__(self,emulator):
        self.emulator = emulator
    
    def execute(self):
        temp = self.emulator.cpu.program[self.emulator.read_head]
        self.emulator.cpu.program[self.emulator.write_head] = temp
        self.emulator.read_head.increment()
        self.emulator.write_head.increment()
    
# This one will search in the forward direction for the complement label
# and set the flow control head to the end of the label.
# The distance to the end of the label is placed into BX
# The size of the label is put into CX
# If a complement label is not found or no label
# follows the instruction, set fchead to instruction-head
class InstructionHSearch:
    
    def __init__(self,emulator):
        self.emulator = emulator
    
    def execute(self):
        
        iterator = self.emulator.instr_pointer.get() + 1
        template = []
        
        while self.emulator.program[iterator] == 0 or self.emulator.program[iterator] == 1 or self.emulator.program[iterator] == 2:
            template.append(self.emulator.program[iterator])
            iterator += 1
            
        
        if len(template) == 0:
            self.emulator.fc_head.set(self.emulator.instr_pointer.get() )
            self.emulator.cpu.reg_b.write(0)
            self.emulator.cpu.reg_c.write(0)
            
            
        else:
            
        
        
            to_match = [(element + 1) % 3 for element in template]
        
            index0 = self.emulator.instr_pointer.get() + len(template)
            
            temp = self.emulator.program[index0:]
        
            # I want the index at which to_match can be found in the memory, starting from the end of the template,
            # to which iterator1 is initialized, until the end of the memory
            
            # In his example:
            # b is the smaller list (our to_match)
            # a is the larger list (our program from iterator1 to the end)
        
            index1 = [(i, i+len(to_match)) for i in range(len(temp)) if temp[i:i+len(to_match)] == to_match][0][1]
            
            self.emulator.fc_head.set(index1)
            
            distance = index1 - index0
            
            self.emulator.cpu.reg_b.write(distance)
            self.emulator.cpu.reg_c.write(len(to_match))
                  
# Move the ?Instruction-Head? to the position of the Flow-Control-Head
# A - instruction, default
# B - read
# C - write
class InstructionMovHead:
    
    def __init__(self,emulator):
        self.emulator = emulator
    
    def execute(self):
        if self.emulator.instr_pointer.get() >= self.emulator.memory.size() - 1:
            next = 0
        else:
            next = self.emulator.memory.get(self.emulator.instr_pointer.get() + 1)
            
        if isinstance(next, InstructionNopB):
            self.emulator.read_head.set(self.emulator.fc_head.get())
                
        elif isinstance(next, InstructionNopC):
            self.emulator.write_head.set(self.emulator.fc_head.get())
                
        else:
            self.emulator.instr_pointer.set(self.emulator.fc_head.get())
        
# Advance the ?Instruction-Head? by CX positions, and set the
# CX register to the initial position of the head.

class InstructionJmpHead:
    
    
    def __init__(self,emulator):
        self.emulator = emulator
    
    def execute(self):
        
        if self.emulator.instr_pointer.get() >= self.emulator.memory.size() - 1:
            next = 0
        else:
            next = self.emulator.memory.get(self.emulator.instr_pointer.get() + 1)
            
        temp = self.emulator.cpu.reg_c.read()
            
        if isinstance(next, InstructionNopB):
            temp1 = self.emulator.read_head.get()

            self.emulator.read_head.increment(temp)
                
        elif isinstance(next, InstructionNopC):
            temp1 = self.emulator.write_head.get()
            self.emulator.write_head.increment(temp)
                
        else:
            temp1 = self.machine.instr_pointer.get()
            self.emulator.instr_pointer.increment(temp)
            
        self.emulator.cpu.reg_c.write(temp1)

# Write the position of the ?Instruction-Head? into the CX register
# A - instruction, default
# B - read
# C - write
class InstructionGetHead:
    
    def __init__(self,emulator):
        self.emulator = emulator
    
    def execute(self):
        if self.emulator.instr_pointer.get() >= self.emulator.memory.size() - 1:
            next = 0
        else:
            next = self.emulator.memory.get(self.emulator.instr_pointer.get() + 1)
            
        if isinstance(next, InstructionNopB):
            self.emulator.cpu.reg_c.write(self.emulator.read_head.get())
                
        elif isinstance(next, InstructionNopC):
            self.emulator.cpu.reg_c.write(self.emulator.write_head.get())
        else:
            self.emulator.cpu.reg_c.write(self.emulator.instr_pointer.get())

# Set the ?Flow-Control-Head? to the address pointed to by the
# ?CX? register.

# A - instruction, default
# B - read
# C - write
class InstructionSetFlow:
    
    def __init__(self,emulator):
        self.emulator = emulator
    
    def execute(self):
        
        if self.emulator.instr_pointer.get() >= self.emulator.memory.size() - 1:
            next = 0
        else:
            next = self.emulator.memory.get(self.emulator.instr_pointer.get() + 1)
            
        if isinstance(next, InstructionNopA):
            self.emulator.fc_head.set(self.emulator.cpu.reg_a)
        elif isinstance(next, InstructionNopB):
            self.emulator.fc_head.set(self.emulator.cpu.reg_b)
        else:
            self.emulator.fc_head.set(self.emulator.cpu.reg_c)

class InstructionIfLabel:
    
    def __init__(self,emulator):
        pass
    
    def execute(self):
        pass
    
# %%

class CPUEmulator:

    def __init__(self, a, b, c):
        
        self.cpu = CPU(a,b,c)
        
        self.memory = Memory()
        
        self.program = []
        
        self.instr_pointer = InstructionPointer()
        self.read_head = ReadHead()
        self.write_head = WriteHead()
        self.fc_head = FlowControlHead()
        
        # Restricting memory size to 10. Hard coded at the moment,
        # will be changed later
        self.memory_size = 10
        
        # Restricting memory size of child organism to 10. Hard coded at the moment
        # Will be changed later
        self.memory_size_child = 10
        
        
    # Parse a Program type instance, load it into the memory of the CPUEmulator
    # as a list of Instruction type objects
    def load_program(self, p):
        
        # Check if what we're trying to read is an instance od type "Program"
        if not isinstance(p, Program):
            raise NotImplementedError
            print("In Machine.read_program(p), p is not an instance of Program")
            
        #Check if the program we're trying to read doesn't exceed the memory size of the CPUEmulator
        if len(p.instructions) > self.memory_size:
            raise Exception("Program length exceeds Emulator memory size")
            
        # Parsing
        
        self.program = p
        
        for instruction in p.instructions:
            self.read_head.increment()
            # For now just swap
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
            
    def execute_program(self):

        # For now it just executes each instruction in the list one by one.
        # When the last instruction is executed we stop.
        # TODO: Make the Instruction Pointer loop back to the beginning of the memory
        # This is easy to do, let's just leave it for when we have replicating organisms,
        # otherwise we'd just have one program that repeats itself infinitely many times

        while self.instr_pointer.get() < self.memory.size():
            self.write_head.increment()
            # Save current instruction pointer value to later check if it was explicitly changed by an instruction
            temp = self.instr_pointer.get()

            self.memory.get(self.instr_pointer.get()).execute()
            # If the IP wasn't changed by an instruction, increase by 1, otherwise leave it
            if self.instr_pointer.get() == temp:
                self.instr_pointer.increment()

    # A string representation of the state of the machine
    def __str__(self):
        string_representation = "Register A: " + str(self.cpu.reg_a.read()) + "\nRegister B: " + str(
            self.cpu.reg_b.read()) + "\nRegister C: " + str(self.cpu.reg_c.read()) + "\nInstruction Pointer: " + str(self.instr_pointer.get()) + "\n"
        return string_representation

# %% TESTS:

# Three swaps on register B and its complement, then a swap on A and its compelement
# Start : 0, 1, 5
# Expected result: 5, 0, 1

Emulator0 = CPUEmulator(0,1,5)
print(Emulator0)
program0 = Program([5,5,5,5,0])
Emulator0.load_program(program0)
Emulator0.execute_program()
print(Emulator0)


# Two increments on default register B, one increment on modified register A,
# three increments on modified register C
print("Test 2 -> 3times inc reg_B, one time reg_A, three times reg_C")
Emulator1 = CPUEmulator(0,0,0)
print(Emulator1)
program1 = Program([11, 11, 11, 0, 11, 2, 11, 2, 11, 2])
Emulator1.load_program(program1)
Emulator1.execute_program()
print(Emulator1)


# Trying to read a program of larger length than the hard-coded Machine memory 10
"""print("Test 3 ")
Emulator2 = CPUEmulator(0,0,0)
print(Emulator2)
program2 = Program([0,1,2,3,4,5,6,7,8,9,10])
Emulator2.load_program(program2)
Emulator2.execute_program()
print(Emulator2)"""
#Test 3
#%% 
#Those Functios called here need fixing!
# Fix when nop's are implemented!
#
#
print ("Test 4 -> subtraction  reg_B-reg_C,")
Emulator3 = CPUEmulator(1,3,6)
print(Emulator3)
program3 = Program([14,1])
program4 = Program([14,2])
Emulator3.load_program(program3)
Emulator3.execute_program()
print(Emulator3)
Emulator3.load_program(program4)
Emulator3.execute_program()
print(Emulator3)
print("Needs Correct implementation!" '\n' '\n')
print("Test 5 -> adding reg_b + reg_c, reg_a +reg_c")
Emulator4 = CPUEmulator(1,3,5)
print("Start")
print(Emulator4)
program4 = Program([13,1,13,0])
#program5 = Program([13,0])
Emulator4.load_program(program4)
Emulator4.execute_program()
print(Emulator4)
#Emulator4.load_program(program5)
#Emulator4.execute_program()
#print(Emulator4)
print("Needs correct implementation!" '\n' "-> Please Check if this is correct" '\n')
#%%
#   More Tests

print ("Test 6 -> subtraction  reg_B = reg_B-reg_C,reg_C = reg_B_new-reg_C")
Emulator5 = CPUEmulator(1,3,6)
print(Emulator5)
program5 = Program([15])
program6 = Program([15,2])
Emulator5.load_program(program5)
Emulator5.execute_program()
print(Emulator5)
Emulator5.load_program(program6)
Emulator5.execute_program()
print(Emulator5)

#%%
#Tests for more functions
    
print("Test 7 -> testing the swap and pop functions:" '\n' "swap AX-BX")
Emulator6 = CPUEmulator(1, 3, 6)
print(Emulator6)
program6 = Program([5, 0])
Emulator6.load_program(program6)
Emulator6.execute_program()
print(Emulator6)
print("swap BX-CX")
program6 = Program([5, 1])
Emulator6.load_program(program6)
Emulator6.execute_program()
print(Emulator6)
print("swap CX-AX")
program6 = Program([5, 2])
Emulator6.load_program(program6)
Emulator6.execute_program()
print(Emulator6)

print("Test 8 -> testing the pop functions:" '\n' "pop BX")
Emulator7 = CPUEmulator(1, 3, 6)
print(Emulator7)
program7 = Program([7, 2, 6, 1])
Emulator7.load_program(program7)
Emulator7.execute_program()
print(Emulator7)
print("pop AX")
print("""Needs work, for some reason it calls pop three times, once one AX, once on BX and once on CX""")
program8 = Program([7, 2, 6, 0, 6, 2])
Emulator8 = CPUEmulator(1, 3, 6)
Emulator8.load_program(program8)
Emulator8.execute_program()
print(Emulator8)
print("pop CX")
"""Error here, pops cx and bx like wtf?"""
program7 = Program([6, 2])
Emulator7.load_program(program7)
Emulator7.execute_program()
print(Emulator7)

print("Test 9 -> testing the shift-r and shift-l functions:" '\n' "shift-r AX")
Emulator9 = CPUEmulator(1, 3, 6)
print(Emulator9)
program9 = Program([9, 0])
Emulator9.load_program(program9)
Emulator9.execute_program()
print(Emulator9)
print("shift-l AX")
Emulator9 = CPUEmulator(7, 3, 6)
print(Emulator9)
program9 = Program([9, 1])
Emulator9.load_program(program9)
Emulator9.execute_program()
print(Emulator9)
print("shift-r AX")
Emulator9 = CPUEmulator(7, 3, 6)
print(Emulator9)
program9 = Program([10, 1])
Emulator9.load_program(program9)
Emulator9.execute_program()
print(Emulator9)

#%% H-functions:
print("h-alloc, h-divide")
Emulator9 = CPUEmulator(7, 3, 6)
print(Emulator9)
program9 = Program([3, 1, 9, 2, 16, 17, 10, 0, 10, 1])
Emulator9.load_program(program9)
Emulator9.execute_program()
print(Emulator9)
