# %%
# Necessary imports:
    
from Mediator import Mediator

import numpy as np

from Instructions import *
from Hardware import *
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
            
            self.instruction_memory.append(self.instruction_list[instruction])
            """
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
                
            elif instruction == 26:
                self.instruction_memory.append(InstructionConsume(self))
                
            elif instruction == 27:
                self.instruction_memory.append(InstructionMoveUp(self))    
                
            elif instruction == 28:
                self.instruction_memory.append(InstructionMoveDown(self))    
            """
                
    def execute_instruction(self):
        
        memsize =  len(self.memory)

        self.instr_pointer.set(self.instr_pointer.get() % self.instruction_memory.size())

        ip = self.instr_pointer.get()

        self.instruction_memory.get(ip).execute()

        self.age += 1
        
        """
        if self.instr_pointer.get() == ip:
                self.instr_pointer.increment()
            
        """
        
        if self.instr_pointer.get() == ip:
            
            memsize =  len(self.memory)
            
            start = (ip + 1) % memsize
            for i in range(len(self.memory)):
                
                instr = self.memory[(start + i) % memsize]
                
                if instr > 2:
                    self.instr_pointer.set((start + i) % memsize)
                    break


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