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

class Machine:

    # An Avida machine needs the following libraries to function:
    # from queue import LifoQueue

    def __init__(self, a, b, c):
        
        # The three registers:

        self.reg_a = a
        self.reg_b = b
        self.reg_c = c

        # The instruction pointer. Initialize to 0.
        self.instr_pointer = 0
        
        # The two stacks. Only one is active at a time.
        # By default it is stack0 in the beginning.
        self.stack0 = LifoQueue()
        self.stack1 = LifoQueue()
        
        # active_stack is a pointer to the currently active stack, not a copy of it.
        # Exactly what we need.
        self.active_stack = self.stack0
        
        # The memory for the instructions. Initialize to empty list
        self.memory = []
        
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

        self.memory = p.instructions

    # The method which defines which function is to be executed after reading each instruction.
    # The functions to be executed aren't defined explicitly as functions, but as a set of statements after a case check

    # When we get a couple more of them we can see whether it makes sense to also define seperate functions for each instr.
    def execute_instruction(self, i):
        
        # This here will set the active stack to stack0 every time we execute an instruction.
        # Do we want that?
        #self.active_stack = self.stack0
        
        
        # This will be a lookup table where we'll see what each instruction is supposed to do
        
        # The instruction set as given on page 49 of reference paper
        
            
        
        # nop-a. TODO: Use as template
        if i == 0:
            pass
        
        # nop-b. TODO: Use as template
        elif i == 1:
            pass
        
        # nop-c. TODO: Use as template
        elif i == 2:
            pass
        
        # if-n-equ. TODO: Expand beyond default register b with the use of templates
        # We need to be careful how we manipulate the instruction pointer
        # If it wasn't explicitly changed, it will increase by 1, otherwise it will follow the explicit change
        elif i == 3:
            if self.reg_b != self.reg_c:
                pass # Do nothing, the next instruction will be executed
            else:
                self.instr_pointer += 2 # To skip the next instruction, increase IP by 2
                
        # if-less. TODO: Expand beyond default register b with the use of templates (Template matching)
        elif i == 4:
            if self.reg_b < self.reg_c:
                pass
            else:
                self.instr_pointer += 2
            
        # swap. TODO: Template matching   
        elif i == 5:
            temp = self.reg_b
            self.reg_b = self.reg_c
            self.reg_c = temp
        
        # pop. TODO: Template matching
        elif i == 6:
            # NOTE: If stack is empty, pop should return 0 (see page 11 of original Avida paper)
            if self.active_stack.empty():
                temp = 0
            else:
                temp = self.active_stack.get()
            self.reg_b = temp
            
        # push. TODO: Template matching
        elif i == 7:
            self.active_stack.put(self.reg_b)
            
        # swap-stk
        elif i == 8:
            if self.active_stack == self.stack0:
                self.active_stack = self.stack1
            else:
                self.active_stack = self.stack0
            
        # shift-r. TODO: Template matching
        elif i == 9:
            self.reg_b = self.reg_b >> 1 # Bitwise 1 right shift
            
        # shift-l. TODO: Template matching
        elif i == 10:
            self.reg_b = self.reg_b << 1 # Bitwise 1 left shift
        
        # inc. TODO: Template matching
        elif i == 11:
            # Checking whether the next instruction is a nop:
            a = self.memory[self.instr_pointer + 1]

            if a == 0:
                    self.reg_a += 1
            elif a == 1:
                    self.reg_b += 1
            elif a == 2:
                    self.reg_c += 1
            else:    
                self.reg_b = self.reg_b + 1
            
        # dec. TODO: Template matching
        elif i == 12:
            self.reg_b = self.reg_b - 1
            
        # add. TODO: Template matching
        elif i == 13:
            self.reg_b = self.reg_b + self.reg_c
        
        # sub. TODO: Template matching
        elif i == 14:
            self.reg_b = self.reg_b - self.reg_c
            
        # nand. TODO: Template matching
        elif i == 15:
            self.reg_b = ~(self.reg_b & self.reg_c) # Bitwise NAND
        
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

        while self.instr_pointer < len(self.memory):
            
            # Save current instruction pointer value to later check if it was explicitly changed by an instruction
            temp = self.instr_pointer

            self.execute_instruction(self.memory[self.instr_pointer])

            # We have to allow for the possibility of the instruction changing the value of the IP
            # But we also have to ensure that if the instruction did nothing to explicitly change the IP,
            # that it's automatically increased by 1

            # Two options: Explicitly make each instruction change the IP as desired, or:

            # If it wasn't changed by an instruction, increase by 1, otherwise leave it
            if self.instr_pointer == temp:
                self.instr_pointer += 1

    # A string representation of the state of the machine
    def __str__(self):
        string_representation = "Register A: " + str(self.reg_a) + "\nRegister B: " + str(
            self.reg_b) + "\nRegister C: " + str(self.reg_c) + "\nInstruction Pointer: " + str(self.instr_pointer)
        return string_representation
# %%

# TESTS:
    
# Three swaps on register B and its complement
program0 = Program([5,5,5])
program0.instructions
machine0 = Machine(4, 7, 8)
print(machine0)
machine0.read_program(program0)
machine0.execute_program()
print(machine0)

# Two increments on default register B, one increment on modified register A,
# three increments on modified register C

program1 = Program([11, 11, 11, 0, 11, 2, 11, 2, 11, 2])
machine1 = Machine(0,0,0)
print(machine1)
machine1.read_program(program1)
machine1.execute_program()
print(machine1)

# Trying to read a program of larger length than the hard-coded Machine memory 10
program2 = Program([0,1,2,3,4,5,6,7,8,9,10])
machine2 = Machine(0,0,0)
machine2.read_program(program2)