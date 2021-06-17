# %%
# Necessary imports:
    
from Mediator import Mediator

import numpy as np

from Instructions import *
from Hardware import *

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
        
#%%

# We get overflow errors sometimes but for our purposes this is absolutely fine
# We care about the binary representation, not the actual int32 value
# Therefore, ignore overflow warnings

np.warnings.filterwarnings('ignore', 'overflow')

# %%

class CPUEmulator:

    def __init__(self, a = 0, b = 0, c = 0, mutation_prob = 0, ins_prob = 0, del_prob = 0):

        self.cpu = CPU(a,b,c)

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
        
        # Indicators for which boolean functions the organism can compute
        self.fun_not = False
        self.fun_nand = False
        self.fun_and = False
        self.fun_or_n = False
        self.fun_or = False
        self.fun_and_n = False
        self.fun_nor = False
        self.fun_xor = False
        self.fun_equ = False
        
        # Helper list to quickly load program
        self.instruction_list = [InstructionNopA(self),InstructionNopB(self),InstructionNopC(self),InstructionIfNEq(self),\
                                InstructionIfLess(self),InstructionSwap(self),InstructionPop(self),InstructionPush(self),\
                                InstructionSwapStack(self),InstructionRightShift(self),InstructionLeftShift(self),\
                                InstructionInc(self), InstructionDec(self),InstructionAdd(self),InstructionSub(self),\
                                InstructionNand(self),InstructionHAlloc(self),InstructionHDivide(self),InstructionIO(self),\
                                InstructionHCopy(self),InstructionHSearch(self),InstructionMovHead(self),InstructionJmpHead(self),\
                                InstructionGetHead(self),InstructionSetFlow(self),InstructionIfLabel(self),InstructionConsume(self),\
                                InstructionMoveUp(self),InstructionMoveDown(self),InstructionMoveLeft(self),InstructionMoveRight(self)]
            
        # Helper attributes for tracking the lineage of an organism
        self.ancestor = None
        
        # The cumulated mutations which resulted in the current organism, starting from the ancestor
        self.mutations = []
        
        # The mutations which, when applied on current program, result in the child
        self.child_mutations = []

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
        """
        if not isinstance(p, Program):
            raise NotImplementedError
            print("In Machine.read_program(p), p is not an instance of Program")
        """
        
        # Instantiate memory, original_memory and instruction_memory
        self.memory = p.instructions.copy()
        self.original_memory = p.instructions.copy()
        
        for instruction in self.original_memory:
            self.instruction_memory.append(self.instruction_list[instruction])
                            
    def execute_instruction(self):
        
        memsize =  len(self.memory)

        self.instr_pointer.set(self.instr_pointer.get() % self.instruction_memory.size())

        ip = self.instr_pointer.get()

        self.instruction_memory.get(ip).execute()

        self.age += 1
        

        if self.instr_pointer.get() == ip:
                self.instr_pointer.increment()

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