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
# %%

class InstructionSwap:
    def __init__(self):
        pass

    # TODO: Raise exception if machine not instance of CPUEmulator
    def execute(self, machine):
        temp = machine.reg_b.read()
        machine.reg_b.write(machine.reg_c.read())
        machine.reg_c.write(temp)
# %%

class CPUEmulator:

    # An Avida machine needs the following libraries to function:
    # from queue import LifoQueue

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

    # Do we need the separate methods "read_Program" and "execute_Program"?
    # Is there any advantage to this that we could see being useful to us in the future?
    # Is it better to maybe just wrap it all up in one method, "execute_Program(self,p)"
    # which saves a program and executes it at the same time

    # Read a Program type instance and save its instructions in the memory of the CPU
    def read_program(self, p):
        
        # Check if what we're trying to read is an instance od type "Program"
        if not isinstance(p, Program):
            raise NotImplementedError
            print("In Machine.read_program(p), p is not an instance of Program")
            
        
        # A way of putting a limit on the maximum size of memory.
        # At the moment hard-coded to 10
        if len(p.instructions) > self.memory_size:
            raise Exception('Memory exceeds the maximum allowed length')
        
        # What are we writing to memory again?
        # The instructions or just symbols? I'd say the instructions. Not implemented yet.
        self.memory.write(p.instructions)

    # The method which defines which function is to be executed after reading each instruction.
    # The functions to be executed aren't defined explicitly as functions, but as a set of statements after a case check

    # All of this is to be replaced with custom instruction classes
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

        while self.instr_pointer.get() < self.memory.size():
            
            # Save current instruction pointer value to later check if it was explicitly changed by an instruction
            temp = self.instr_pointer.get()

            self.execute_instruction(self.memory.get(self.instr_pointer.get()))

            # We have to allow for the possibility of the instruction changing the value of the IP
            # But we also have to ensure that if the instruction did nothing to explicitly change the IP,
            # that it's automatically increased by 1

            # Two options: Explicitly make each instruction change the IP as desired, or:

            # If it wasn't changed by an instruction, increase by 1, otherwise leave it
            if self.instr_pointer.get() == temp:
                self.instr_pointer.increment()

    # A string representation of the state of the machine
    def __str__(self):
        string_representation = "Register A: " + str(self.reg_a.read()) + "\nRegister B: " + str(
            self.reg_b.read()) + "\nRegister C: " + str(self.reg_c.read()) + "\nInstruction Pointer: " + str(self.instr_pointer.get()) + "\nMemory Content: " + str(self.memory.read()) + "\n"
        return string_representation

# %%

# TESTS:
    
# Three swaps on register B and its complement
program0 = Program([5,5,5])
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