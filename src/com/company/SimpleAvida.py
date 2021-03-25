# TODO: This is a big and general one. DOCUMENT THE CODE BETTER.
# Write a full documentation. It will reveal itself once we have a functional system.
# %%
# Keeping track of all the imports we'll need
from queue import LifoQueue
from queue import Queue


# %%
class Program:

    # AVIDA Program class.
    
    # An instance of this class is nothing more than a list of instructions in AVIDA.
    # Each instruction is to be interpreted by the "Machine".
    # The instructions are symbols in an alphabet given by the instruction set.
    
    # Our instruction set has 26 instructions.
    # The only thing that needs to be checked at the construction of a new Program instance
    # is that all of the elements of the list of instructions are integers in range(0,26)


     # Will check whether the passed list is a valid list of instructions. TODO.
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
        
# %%
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
        
# %%

class InstructionPointer:
    
    def __init__(self):
        self.value = 0
    
    def get(self):
        return self.value
    
    def increment(self, a = 1):
        self.value += a
# %%
class ReadHead:
    def __init__(self):
        pass
# %% 
class WriteHead:
    def __init__(self):
        pass
# %% 
class flowcontrolHead:
    def __init__(self):
        pass
# %%
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
    
# %%

# Separate the hardware from the CPUEmulator
# TODO: Replace all of the elements of the CPUEmulator which rely on direct access to
# this virtual hardware

class CPU:
    
    # Should we define getters and setters for all of the components of the CPU
    # or just acces them directly? For now, it's direct access
    
    def __init__(self, a, b, c):
         # The three registers:

        self.reg_a = Register(a)
        self.reg_b = Register(b)
        self.reg_c = Register(c)

        # The instruction pointer. Initialize to 0.
        self.instr_pointer = InstructionPointer()
        
        # The two stacks. Only one is active at a time.
        # By default it is stack0 in the beginning.
        self.stack0 = LifoQueue()
        self.stack1 = LifoQueue()
        
        # active_stack is a pointer to the currently active stack, not a copy of it.
        # Exactly what we need.
        self.active_stack = self.stack0
        
        # The memory for the instructions. Initialize to empty list
        self.memory = Memory()
        
        # The input and output buffers. Implemented as FIFO Queues
        self.input_buffer = Queue()
        self.output_buffer = Queue()
        
        # Maximum memory size of the Machine. At the moment hard-coded to 10
        self.memory_size = 10

        # TODO: Add the three "read", "write" and "flow control" heads
        # TODO: Add input and output buffers which the organism (machine)
        # will use to interact with the environment
        
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
# %%
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
        self.machine = emulator
    
    def execute(self):
        if self.machine.reg_b.read() != self.machine.reg_c.read():
            pass # Do nothing, the next instruction will be executed
        else:
            self.machine.instr_pointer.increment(2) # To skip the next instruction, increase IP by 2
        

class InstructionIfLess:
    
    def __init__(self, emulator):
        self.machine = emulator.cpu
    
    def execute(self,machine):
        if self.machine.reg_b.get() < self.machine.reg_c.get():
            pass
        else:
            self.machine.instr_pointer.increment(2)
        

class InstructionPop:
    
    def __init__(self, emulator):
        self.machine = emulator.cpu
    
    def execute(self):
        
        # Making sure that if the stack is empty, pop returns a 0 and not an exception
        # as is defined in the implementation of the LifoQueue()
        # QUESTION: Should we define a class stack instead of using
        # a ready-made implementation?
        if self.machine.active_stack.empty():
            temp = 0
        else:
            temp = self.machine.active_stack.get()
            
        
        self.machine.reg_b.write(temp)
        
class InstructionSwap:
    
    def __init__(self, emulator):
        self.machine = emulator.cpu

    # TODO: Raise exception if machine not instance of CPUEmulator
    def execute(self):
        temp = self.machine.reg_b.read()
        self.machine.reg_b.write(self.machine.reg_c.read())
        self.machine.reg_c.write(temp)

class InstructionSwapStack:
    def __init__(self,emulator):
        self.machine = emulator.cpu
    def execute(self):
        if self.machine.active_stack == self.machine.stack0:
            self.machine.active_stack= self.machine.stack1
        else:
            self.machine.active_stack = self.machine.stack2
            
class RightShift:
     def __init__(self,emulator):
         self.machine = emulator.cpu
     def execute(self):
            self.machine.reg_b.write(self.machine.reg_b.read() >> 1)
            
class LeftShift:
    def __init__(self,emulator):
        self.machine = emulator.cpu
    def execute(self):
        self.machine.reg_b.write(self.machine.reg_b.read() << 1)
        
class inc:
    def __init__(self,emulator):
        self.machine = emulator.cpu
    def execute(self):
     # Checking whether the next instruction is a nop:
            if self.machine.instr_pointer.get() == self.machine.memory.size() - 1:
                a = 1
            else:
                a = self.machine.memory.get(self.machine.instr_pointer.get() + 1)

            if a == 0:
                    self.machine.reg_a.increment()
            elif a == 2:
                    self.machine.reg_c.increment()
            else:    
                self.machine.reg_b.increment()
                
class dec:
    def __init__(self,emulator):
        self.machine = emulator.cpu
    def execute(self):
        self.machine.reg_b.decrement()
        
class add:
    def __init__(self,emulator):
        self.machine = emulator.cpu
    def execute(self):
         self.machine.reg_b.write(self.machine.reg_b.read() + self.machine.reg_c.read())
         
class sub:
    def __init__(self,emulator):
        self.machine = emulator.cpu
    def execute(self):
        self.machine.reg_b.write(self.machine.reg_b.read() - self.machine.reg_c.read())
        
class nand:
    def __init__(self,emulator):
        self.machine = emulator.cpu
    def execute(self):
        self.machine.reg_b.write( ~(self.machine.reg_b.read() & self.machine.reg_c.read()))
        
class h_alloc:
    def __init__(self,emulator):
        self.machine = emulator.cpu
    def execute(self):
        self.machine.memory_size = self.machine.memory_size + self.machine.memory_size_child
        
class h_divide:
    def __init__(self,emulator):
        self.machine = emulator.cpu
    def execute(self):
        pass
    
# %%

class CPUEmulator:

    def __init__(self, a, b, c):
        
        self.cpu = CPU(a,b,c)
        self.memory = []

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
            if instruction == 5:
                self.memory.append(InstructionSwap(self))

    
    # All of this is to be replaced with custom instruction classes
    # OBSOLETE
    def execute_instruction(self, i):
        
        # This here will set the active stack to stack0 every time we execute an instruction.
        # Do we want that?
        #self.active_stack = self.stack0
        
        
        # This will be a lookup table where we'll see what each instruction is supposed to do
        
        # The instruction set as given on page 49 of reference paper
        
        # nop-a
        if i == 0:
            pass
        
        # nop-b
        elif i == 1:
            pass
        
        # nop-c
        elif i == 2:
            pass
        
        # if-n-equ
        # We need to be careful how we manipulate the instruction pointer
        # If it wasn't explicitly changed, it will increase by 1, otherwise it will follow the explicit change
        elif i == 3:
            
            # Checking whether the next instruction is a nop:
                
            # At the moment we don't have circular memory
            # If we're at the last instruction we won't do any checking
            # for what the next instruction is because it produces an error,
            # instead we execute in on the defaul register.
            # This is to be changed once we introduce circular memory
            if self.instr_pointer.get() == self.memory.size() - 1:
                a = 1
            else:
                a = self.memory.get(self.instr_pointer.get() + 1)

            if a == 0:
                    if self.reg_a.read() != self.reg_b.read():
                        pass # Do nothing, the next instruction will be executed
                    else:
                        self.instr_pointer.increment(2) # To skip the next instruction, increase IP by 2
            elif a == 2:
                    if self.reg_c.read() != self.reg_a.read():
                        pass # Do nothing, the next instruction will be executed
                    else:
                        self.instr_pointer.increment(2) # To skip the next instruction, increase IP by 2
            else:    
                if self.reg_b.read() != self.reg_c.read():
                    pass # Do nothing, the next instruction will be executed
                else:
                    self.instr_pointer.increment(2) # To skip the next instruction, increase IP by 2
                
        # if-less
        elif i == 4:
            # Checking whether the next instruction is a nop:
            if self.instr_pointer.get() == self.memory.size() - 1:
                a = 1
            else:
                a = self.memory.get(self.instr_pointer.get() + 1)
            
            if a == 0:
                if self.reg_a.get() < self.reg_b.get():
                    pass
                else:
                    self.instr_pointer.increment(2)
            if a == 2:
                if self.reg_c.get() < self.reg_a.get():
                    pass
                else:
                    self.instr_pointer.increment(2)
            else:
                if self.reg_b.get() < self.reg_c.get():
                    pass
                else:
                    self.instr_pointer.increment(2)
            
        # swap
        elif i == 5:
            # Checking whether the next instruction is a nop:
            if self.instr_pointer.get() == self.memory.size() - 1:
                a = 1
            else:
                a = self.memory.get(self.instr_pointer.get() + 1)
            
            if a == 0:
                temp = self.reg_a.read()
                self.reg_a.write(self.reg_b.read())
                self.reg_b.write(temp)
            elif a == 2:
                temp = self.reg_c.read()
                self.reg_c.write(self.reg_a.read())
                self.reg_a.write(temp)
            else:
                temp = self.reg_b.read()
                self.reg_b.write(self.reg_c.read())
                self.reg_c.write(temp)
                
        # pop. TODO: Template matching
        elif i == 6:
            # NOTE: If stack is empty, pop should return 0 (see page 11 of original Avida paper)
            
            # Checking whether the next instruction is a nop:
            if self.instr_pointer.get() == self.memory.size() - 1:
                a = 1
            else:
                a = self.memory.get(self.instr_pointer.get() + 1)
                
            if self.active_stack.empty():
                temp = 0
            else:
                temp = self.active_stack.get()
                
            if a == 0:
                self.reg_a.write(temp)
            elif a == 2:
                self.reg_c.write(temp)
            else:
                self.reg_b.write(temp)
            
        # push. TODO: Template matching
        elif i == 7:
            self.active_stack.put(self.reg_b.read())
            
        # swap-stk
        elif i == 8:
            if self.active_stack == self.stack0:
                self.active_stack = self.stack1
            else:
                self.active_stack = self.stack0
            
        # shift-r. TODO: Template matching
        elif i == 9:
            self.reg_b.write(self.reg_b.read() >> 1) # Bitwise 1 right shift
            
        # shift-l. TODO: Template matching
        elif i == 10:
            self.reg_b.write(self.reg_b.read() << 1) # Bitwise 1 left shift
        
        # inc. TODO: Template matching
        elif i == 11:
            # Checking whether the next instruction is a nop:
            if self.instr_pointer.get() == self.memory.size() - 1:
                a = 1
            else:
                a = self.memory.get(self.instr_pointer.get() + 1)

            if a == 0:
                    self.reg_a.increment()
            elif a == 2:
                    self.reg_c.increment()
            else:    
                self.reg_b.increment()
            
        # dec. TODO: Template matching
        elif i == 12:
            self.reg_b.decrement()
            
        # add. TODO: Template matching
        elif i == 13:
            self.reg_b.write(self.reg_b.read() + self.reg_c.read())
        
        # sub. TODO: Template matching
        elif i == 14:
            self.reg_b.write(self.reg_b.read() - self.reg_c.read())
            
        # nand. TODO: Template matching
        elif i == 15:
            self.reg_b.write( ~(self.reg_b.read() & self.reg_c.read())) # Bitwise NAND
        
        # h-alloc. TODO: All
        # The instruction allocates new memory, necessary for self-replication
        # Extends the memory by the maximal size the offspring is allowed to have
        # For now let's hard-code that size to 10 instructions
        # The newly inserted memory is initilized either to a default instruction
        # (typically nop-A) or to random code
        elif i == 16:
            pass
        
        # h-divide. TODO: All
        # After self-replication has been completed, h-divide splits off the instructions
        # between the read head and the write head and uses them as the genome for the
        # offspring organism
        
        # After splitting off, the state of both the parent and the offspring is cleared
        # (registers and queues reset, all pointers reset to position 0)
        
        # There are conditions under which h-divide fails
        elif i == 17:
            pass
            
        # IO. TODO: All
        elif i == 18:
            pass
        
        # h-copy. TODO: All
        # Copies the instruction at the position of the read head to the 
        # position of the write head and advances both heads by 1
        
        # First let's implement a standard copy algorithm, but afterwards we'll need
        # to think of mutations
        elif i == 19:
            pass
        
        # h-search. TODO: All
        elif i == 20:
            pass
        
        # mov-head. TODO: All
        elif i == 21:
            pass
        
        # jmp-head. TODO: All
        elif i == 22:
            pass
        
        # get-head. TODO: All
        elif i == 23:
            pass
        
        # set-flow. TODO: All
        elif i == 24:
            pass
        
        # if-label. TODO: All
        elif i == 25:
            pass
                
        
        # i is how we index the different instructions.
        # Here it's the instruction pointer that we should manipulate, not i
        
        # compare if register a == register b
        #if i == 1:
        #    if(self.reg_b != self.reg_c):
        #        i+=1
        #    else:
        #        i+=2
        #    #print("instruction here")

        # Which instructions are these exactly?
        #if i == 9:
        #    if self.reg_b == self.reg_c:
        #        self.reg_b = False
        #    else:
        #        self.reg_b = True
        
        #if i == 10:
        #    if self.reg_b < self.reg_c:
        #        self.reg_b = self.reg_b+1
        #    else:
        #        self.reg_b = self.reg_b+2
        
    # Execute the list of instruction that's stored in the CPU's memory
    def execute_program(self):

        # For now it just executes each instruction in the list one by one.
        # When the last instruction is executed we stop.
        # TODO: Make the Instruction Pointer loop back to the beginning of the memory
        # This is easy to do, let's just leave it for when we have replicating organisms,
        # otherwise we'd just have one program that repeats itself infinitely many times

        while self.cpu.instr_pointer.get() < len(self.memory):
            
            # Save current instruction pointer value to later check if it was explicitly changed by an instruction
            temp = self.cpu.instr_pointer.get()

            self.memory[self.cpu.instr_pointer.get()].execute()

            # We have to allow for the possibility of the instruction changing the value of the IP
            # But we also have to ensure that if the instruction did nothing to explicitly change the IP,
            # that it's automatically increased by 1

            # Two options: Explicitly make each instruction change the IP as desired, or:

            # If it wasn't changed by an instruction, increase by 1, otherwise leave it
            if self.cpu.instr_pointer.get() == temp:
                self.cpu.instr_pointer.increment()

    # A string representation of the state of the machine
    def __str__(self):
        string_representation = "Register A: " + str(self.cpu.reg_a.read()) + "\nRegister B: " + str(
            self.cpu.reg_b.read()) + "\nRegister C: " + str(self.cpu.reg_c.read()) + "\nInstruction Pointer: " + str(self.cpu.instr_pointer.get()) + "\n"
        return string_representation

# %%

# Three swaps on register B and its complement
Machine = CPUEmulator(0,1,5)
print(Machine)
program0 = Program([5,5,5])
Machine.load_program(program0)
Machine.execute_program()
print(Machine)

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