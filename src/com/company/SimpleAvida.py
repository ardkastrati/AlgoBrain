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

class ReadHead:
    
    def __init__(self):
        self.value = 0

class WriteHead:
    
    def __init__(self):
        self.value = 0

class FlowControlHead:
    
    def __init__(self):
        self.value = 0
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

# TODO: Implement a separate class for each instruction
# There are some technicalities here, like, how to have the instructions be able to access
# the underlying hardware
# Ard's idea: Pass the Hardware as an argument to the execute() function of the instruction instance

# TODO: Template matching and nop's as modifiers for all instructions
# TODO: Test the instructions
# TODO: Change the implementation to follow the Command design pattern. Right now it doesn't
# Big difference: The execute function of the Command pattern takes no arguments.
# All arguments it could need are passed into the construction of the Command object

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
                self.machine.instr_pointer.increment(2)
            

class InstructionIfLess:
    
    def __init__(self, emulator):
        
        self.machine = emulator.cpu

    
    def execute(self,machine):
        
        if self.emulator.instr_pointer.get() >= self.emulator.memory.size() - 1:
            next = 0
        else:
            next = self.emulator.memory.get(self.emulator.instr_pointer.get() + 1)
        
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
        
        if emulator.instr_pointer.get() == emulator.memory.size() - 1:
            pass
        else:
            self.next = emulator.memory.get(emulator.instr_pointer.get() + 1)
    
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
            
        
        self.machine.reg_b.write(temp)
        
class InstructionPush:
    
    def __init__(self, emulator):
        
        self.machine = emulator.cpu
        
    def execute(self):
        
        if self.emulator.instr_pointer.get() >= self.emulator.memory.size() - 1:
            next = 0
        else:
            next = self.emulator.memory.get(self.emulator.instr_pointer.get() + 1)
            
        self.machine.active_stack.put(self.machine.reg_b.read())
        

class InstructionSwapStack:

    def __init__(self,emulator):
        
        self.machine = emulator.cpu
        
    def execute(self):
        
        if self.machine.active_stack == self.machine.stack0:
            self.machine.active_stack= self.machine.stack1
        else:
            self.machine.active_stack = self.machine.stack0
            

class InstructionRightShift:
    
     def __init__(self, emulator):
         self.emulator = emulator
     
     def execute(self):
         
        if self.emulator.instr_pointer.get() >= self.emulator.memory.size() - 1:
            next = 0
        else:
            next = self.emulator.memory.get(self.emulator.instr_pointer.get() + 1)
            
        self.machine.reg_b.write(self.machine.reg_b.read() >> 1)
            
class InstructionLeftShift:
    
    def __init__(self):
        pass
    
    def execute(self,machine):
        machine.reg_b.write(machine.reg_b.read() << 1)
        
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
        self.machine = emulator.cpu
    
    def execute(self):
        self.machine.reg_b.decrement()
        
class InstructionAdd:
    
    def __init__(self, emulator):
        self.machine = emulator.cpu
    
    def execute(self):
         self.machine.reg_b.write(self.machine.reg_b.read() + self.machine.reg_c.read())
         
class InstructionSub:
    
    def __init__(self, emulator):
        self.machine = emulator.cpu
    
    def execute(self):
        self.machine.reg_b.write(self.machine.reg_b.read() - self.machine.reg_c.read())
        
class InstructionNand:
    
    def __init__(self, emulator):
        self.machine = emulator.cpu
    
    def execute(self):
        self.machine.reg_b.write( ~(self.machine.reg_b.read() & self.machine.reg_c.read()))
        
class InstructionHAlloc:
    
    def __init__(self, emulator):
        self.emulator = emulator
    
    def execute(self):
        self.emulator.memory_size = self.emulator.memory_size + self.emulator.memory_size_child
        
class InstructionHDivide:
    
    def __init__(self,emulator):
        pass
    
    def execute(self):
        pass

    
class InstructionIO:
    
    def __init__(self,emulator):
        pass
    
    def execute(self):
        pass
    
class InstructionHCopy:
    
    def __init__(self,emulator):
        pass
    
    def execute(self):
        pass
    
class InstructionHSearch:
    
    def __init__(self,emulator):
        pass
    
    def execute(self):
        pass
    
    
class InstructionMovHead:
    
    def __init__(self,emulator):
        pass
    
    def execute(self):
        pass
    
class InstructionJmpHead:
    
    def __init__(self,emulator):
        pass
    
    def execute(self):
        pass
    
class InstructionGetHead:
    
    def __init__(self,emulator):
        pass
    
    def execute(self):
        pass

class InstructionSetFlow:
    
    def __init__(self,emulator):
        pass
    
    def execute(self):
        pass

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
            
        # Parsing
        for instruction in p.instructions:
            
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
            
            # Save current instruction pointer value to later check if it was explicitly changed by an instruction
            temp = self.instr_pointer.get()

            self.memory.get(self.instr_pointer.get()).execute()

            # We have to allow for the possibility of the instruction changing the value of the IP
            # But we also have to ensure that if the instruction did nothing to explicitly change the IP,
            # that it's automatically increased by 1

            # Two options: Explicitly make each instruction change the IP as desired, or:

            # If it wasn't changed by an instruction, increase by 1, otherwise leave it
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

Emulator1 = CPUEmulator(0,0,0)
print(Emulator1)
program1 = Program([11, 11, 11, 0, 11, 2, 11, 2, 11, 2])
Emulator1.load_program(program1)
Emulator1.execute_program()
print(Emulator1)


# %%


# TESTS (NO LONGER VALID. SEE ABOVE):
    
# Three swaps on register B and its complement
"""program0 = Program([5,5,5])
program0.instructions
machine0 = CPUEmulator(4, 7, 8)
print(machine0)
machine0.read_program(program0)
machine0.execute_program()
print(machine0)

# Two increments on default register B, one increment on modified register A,
# three increments on modified register C

program1 = Program([11, 11, 11, 0, 11, 2, 11, 2, 11, 2])
machine1 = CPUEmulator(0,0,0)
print(machine1)
machine1.read_program(program1)
machine1.execute_program()
print(machine1)

# Trying to read a program of larger length than the hard-coded Machine memory 10
program2 = Program([0,1,2,3,4,5,6,7,8,9,10])
machine2 = CPUEmulator(0,0,0)
machine2.read_program(program2)
"""