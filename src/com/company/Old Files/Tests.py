# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 17:22:05 2021

@author: Aleksandar
"""


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
"""print("Test 3 ")2
Emulator2 = CPUEmulator(0,0,0)
print(Emulator2)
program2 = Program([0,1,2,3,4,5,6,7,8,9,10])
Emulator2.load_program(program2)
Emulator2.execute_program()
print(Emulator2)"""
#%% 
program = Program([12])
emulator = CPUEmulator(0,0,0)
emulator.load_program(program)
emulator.execute_program()
print(emulator)
#%% 
print("TESTING TEMPLATE MATCHING FOR JUMPS:")
print("\nExample program: nop-a, h-search,, nop-a, mov-head, inc, inc, nop-b, dec")
print("\nWill test this on the machine with all registers initialized to 0")
print("\nExpected result: the inc's are skipped and only the dec was run")
print("\nWant to keep track of total number of executed instructions for debugging purposes")
#%% 
program = Program([20,0,1,21,11,11,1,2,12])
print("\n"+str(program.instructions)+"\n")
emulator = CPUEmulator(0,0,0)
emulator.load_program(program)
emulator.execute_program()
#%% 
print(emulator)
#%% 
print("\nTESTING H-COPY:")
print("First step: Allocate memory")
print("Second step: Run H-Copy")

program = Program([1,2,3,4,5,6,7,8,9,10,16,19,19,19,19,19,19,19,19,19,19,17])
emulator = CPUEmulator(0,0,0)
emulator.load_program(program)
print(emulator.program)
emulator.execute_program()
print(emulator.program)

print("\nWhat happens here is: We have an organism of size 21.")
print("\nFirst, it allocates memory for a child of size 10")
print("\nThen, it runs H-Copy 10 times and copies the first 10 instructions of the original organism into the child")

#%%
print("\nDEFAULT SELF-COPYING PROGRAM AS IN A.3 OF THE PAPER:")

# h-alloc
# h-search
# nop-c
# nop-a
# mov-head
# nop-c
# h-search
# h-copy
# if-label
# nop-c
# nop-a
# h-divide
# mov-head
# nop-a
# nop-b

program = Program([16,20,2,0,21,2,20,19,25,2,0,17,21,0,1])

#%% 


emulator = CPUEmulator(0,0,0)
emulator.load_program(program)

print("\nEmulator before execting the instructions: \n")
print(emulator)
print("\n")

emulator.execute_program()

print("\nEmulator after execting the instructions: \n")

#%%
print(emulator)


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