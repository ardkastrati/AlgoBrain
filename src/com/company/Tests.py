"""
These tests are an important sanity check

If any modification ruins the test functionality then we can be sure 
that the modification is detrimental
"""

from Environment import World

# clears all registers (under the assumption that the active stack is empty)
clear = [6, 0, 6, 1, 6, 2]

"""

Mapping integers - instructions:
    
0  <==> NopA
1  <==> NopB
2  <==> NopC
3  <==> IfNEq
4  <==> IfLess
5  <==> Swap
6  <==> Pop
7  <==> Push
8  <==> SwapStack
9  <==> RightShift
10 <==> LeftShift
11 <==> Inc
12 <==> Dec
13 <==> Add
14 <==> Sub
15 <==> Nand
16 <==> HAlloc
17 <==> HDivide
18 <==> IO
19 <==> HCopy
20 <==> HSearch
21 <==> MovHead
22 <==> JmpHead
23 <==> GetHead£
24 <==> SetFlow
25 <==> IfLabel

"""
#%%
"""
Parser to create instructions by reading input stream

All instructions to be written lowercase without dashes



"""

result = []
instr = []
number_of_empty_responses = 0
while True:
    data = input("Instructions: ")
    if data == "":
        number_of_empty_responses += 1
        if number_of_empty_responses == 2:
            break
    else:
        number_of_empty_responses = 0
        
        # Boring case checking
        if data == "nopa" or data == "a":
            result.append(0)
            instr.append("nopa")
        elif data == "nopb" or data == "b":
            result.append(1)
            instr.append("nopb")
        elif data == "nopc" or data == "c":
            result.append(2)
            instr.append("nopc")
        elif data == "ifneq":
            result.append(3)
        elif data == "ifless":
            result.append(4)
        elif data == "swap":
            result.append(5)
        elif data == "pop":
            result.append(6)
        elif data == "push":
            result.append(7)
        elif data == "swapstack":
            result.append(8)
        elif data == "rshift":
            result.append(9)
        elif data == "lshift":
            result.append(10)
        elif data == "inc":
            result.append(11)
        elif data == "dec":
            result.append(12)
        elif data == "add":
            result.append(13)
        elif data == "sub":
            result.append(14)
        elif data == "nand":
            result.append(15)
        elif data == "halloc":
            result.append(16)
        elif data == "hdivide":
            result.append(17)
        elif data == "io":
            result.append(18)
        elif data == "hcopy":
            result.append(19)
        elif data == "hsearch":
            result.append(20)
        elif data == "movhead":
            result.append(21)
        elif data == "jmphead":
            result.append(22)
        elif data == "gethead":
            result.append(23)
        elif data == "setflow":
            result.append(24)
        elif data == "iflabel":
            result.append(25)
        elif data == "consume":
            result.append(26)
        elif data == "back":
            result.pop(-1)
        elif data == "clear":
            result = []
        print(result)

#%%
"""
Test 1:
    
    An organism that computes NOT
    
    NOT(A) == -A - 1
    
    POP-B
    IO-C
    SUB-A
    DEC-A
    IO-A
    
"""

program_not = [6, 1, 18, 2, 14,0, 12, 0, 18, 0] + clear

instructions = program_not

world = World(1, replacement_strategy = "neighborhood", cm_prob = 0, ins_prob = 0, del_prob = 0)

world.place_custom(instructions)

world.schedule(13)

program_not = instructions

#%%
"""
Test 2:
    
    An organim that computes NAND
    
    IO-B
    IO-C
    NAND-A
    IO-A
    
"""

instructions = [18,1,18,2,15,0,18,0] + clear

world = World(1, replacement_strategy = "neighborhood", cm_prob = 0, ins_prob = 0, del_prob = 0)

world.place_custom(instructions)

world.schedule(10)

program_nand = instructions

#%%
"""
Test 3:
    
    An organism that computes AND
    
    Serial connection NAND => NOT
    
    AND(A,B) = NOT(NAND(A,B))
    
    IO-B
    IO-C
    NAND-C
    POP-B
    SUB-A
    INC-A
    IO-A
    
"""

instructions = [18,1,18,2,15,2,6,1,14,0,12,0,18,0] + clear
    
world = World(1, replacement_strategy = "neighborhood", cm_prob = 0, ins_prob = 0, del_prob = 0)

world.place_custom(instructions)

world.schedule(9)

program_and = instructions

#%%
"""
Test 4:
    
    An organism that computes OR
    
    OR(A,B) == NOT(NOT(A) AND NOT(B))
    
    NOT(A) AND NOT(B) = NOT(NAND(NOT(A),NOT(B)))
    
    All together:
    
        OR(A,B) = NAND(NOT(A),NOT(B))
        
    
    #1: 
        Save NOT(A) in regA
        
        POP-B
        IO-C
        SUB-A
        DEC-A
        
    #2:
        Save NOT(B) in regC
        
        POP-B
        IO-C
        SUB-C
        DEC-C
        
    #3:
        Move regA to regB
        
        PUSH-A
        POP-B
    
    #4:
        NAND to regA, IO-A
        
        NAND-A
        IO-A
"""

l1 = [6,1,18,2,14,0,12,0]

l2 = [6,1,18,2,14,2,12,2]

l3 = [7,0,6,1]

l4 = [15,0,18,0]

instructions = l1 + l2 + l3 + l4 + clear
        
world = World(1, replacement_strategy = "neighborhood", cm_prob = 0, ins_prob = 0, del_prob = 0)

world.place_custom(instructions)

world.schedule(15)

program_or = instructions

#%%

"""
Test 5:
    
    An organism that computes OR_N
    
    Take A OR NOT(B)
    
    A OR NOT(B) = NOT(A) NAND B
    
    # Save NOT(A) to C
    # Input B
    # NAND to A
    # IO-A
    
    
"""

l1 = [6,1,18,2,14,2,12,2]
l2 = [18,1]
l3 = [15,0]
l4 = [18,0]

instructions = l1 + l2 + l3 + l4 + clear
        
world = World(1, replacement_strategy = "neighborhood", cm_prob = 0, ins_prob = 0, del_prob = 0)

world.place_custom(instructions)

world.schedule(10)

program_or_n = instructions
    
#%%

"""
Test 6:
    
    An organism that computes AND_N
    
    Take A AND NOT(B)
    
    a and not(b) = not(a nand not(b))
    
    # Save NOT(B) to regC
    # Load A to regB
    # NAND-C
    # POP-B
    # SUB-A
    # DEC-A
    # IO-A
    
"""

program_and_n = [6, 1, 18, 2, 14, 2, 12, 2, 18, 1, 15, 2, 6, 1, 14, 0, 12, 0, 18, 0] + clear
instructions = program_and_n 

world = World(1, replacement_strategy = "neighborhood", cm_prob = 0, ins_prob = 0, del_prob = 0)

world.place_custom(instructions)

world.schedule(12)

#%%

"""
Test 7:
    
    An organism that computes NOR
    
    NOT(A OR B)
    
    A OR B = NAND(NOT(A),NOT(B))
    
    How to do it:
        
    #1: 
        Save NOT(A) in regA
        
        IO-C
        SUB-A
        DEC-A
        
    #2:
        Save NOT(B) in regC
        
        POP-B
        IO-C
        SUB-C
        DEC-C
        
    #3:
        Move regA to regB
        
        PUSH-A
        POP-B
    
    #4:
        NAND to regC
        
        NAND-C
        
    #5: Clear B
        POP-B
        
    #6: Sub to A, Dec A, IO A
    
"""
program_nor = [18, 2, 14, 0, 12, 0, 6, 1, 18, 2, 14, 2, 12, 2, 7, 0, 6, 1, 15, 2, 6, 1, 14, 0, 12, 0, 18, 0] + clear
instructions = program_nor

world = World(1, replacement_strategy = "neighborhood", cm_prob = 0, ins_prob = 0, del_prob = 0)

world.place_custom(instructions)

world.schedule(20)

#%%

"""
Test 8:
    
    An organism that computes XOR
    
    (A and ~B) or (~A and B)
    
    NOT(NAND(A,NOT(B))) OR NOT(NAND(NOT(A),B))
    
    This ends up being equivalent to
    
    nand(nand(a,not(b)),nand(not(a),b))
    
    #1:
        input one to a
        input other to c
        push both to stack for later use. push 2nd input first and then the first one
        switch stack for popping
        calculate not(other) as:
            sub-c
            dec-c
        move first one from a to b by doing:
            push-a
            pop-b
            pop-a
        
        now we have:
            reg_a = 0
            reg_b = Input0
            reg_c = not(Input1)
            stack = (b,a)
        we just nand this to c
        pop-b
        push-c
        
        repeat first part
        
        swap stack
        pop a
        pop c
        
        Detailed Guide:
            
            # Inputing and saving to stack:
                IO-A
                IO-C
                PUSH-A
                PUSH-C
                
            Stack0 now is [i1,i0]
            
            Registers are:
                A = i0
                B = 0
                C = i1
                
            swapstack
            
            # Calculating not(i1):
                sub-c
                dec-c
                
            # Move one from A to B:
                push-a
                pop-b
                pop-a
                
                
            Registers are:
                
                regA = 0
                regB = A
                regC = NOT(B)
                
            # Nand them to C:
                
                nand-c
                
            # pop b to clear it:
                pop-b
            
            push-c
            
            now the second stack has nand(a,not(b)) in it.
            Switching to first stack with [b,a] in it
            
            swapstack
            pop-a
            pop-c
            
            # do not of register C which contains A
            
            sub-c
            dec-c
            
            # move B from A to regB
            
            push-a
            pop-b
            pop-a
            
            # Registers now:
                
                regA = 0
                regB = B
                regC = not(A)
            
            # nand them to c
            nand-c
            
            # swap to other stack
            
            swapstack
            
            # retrieve first result to regb
            
            pop-b
            
            # nand
            nand-a
            
            io-a
        
"""


program_xor = [18, 0, 18, 2, 7, 0, 7, 2, 8, 14, 2, 12, 2, 7, 0, 6, 1, 6, 0, 15,\
           2, 6, 1, 7, 2, 8, 6, 0, 6, 2, 14, 2, 12, 2, 7, 0, 6, 1, 6, 0, 15, 2, 8, 6, 1, 15, 0, 18, 0] + clear
    

instructions = program_xor

world = World(1, replacement_strategy = "neighborhood", cm_prob = 0, ins_prob = 0, del_prob = 0)

world.place_custom(instructions)

world.schedule(30)

#%%

"""
Test EQU:
    
    An organism that computes EQU
    
    EQU(A,B) = (A and B) or (~A and ~B)
    
    not(nand(a,b)) or not(nand(not(a),not(b)))
    
    nand(nand(a,b),nand(not(a),not(b)))
    
    #0: Input a,b; store in active stack
    #1: Switch stack
    #2: Compute nand(a,b)
    #3: Clear register b
    #4: Store nand(a,b) to stack
    #5: Switch stack
    #6: Put a to reg_a, b to reg_c
    #7 : Calculate not(b) in reg_c, store to stack
    #8: Move a to reg_c by doing push-a pop-c
    #9: Calculate not(a) in reg_c
    #10: pop not(b) to reg_b
    #11: nand them to c
    #12: swap stack
    #13: pop to b
    #14: nand to a
    #15: io-a
        
"""

program_equ = [18, 1, 18, 2, 7, 1, 7, 2, 8, 15, 2, 6, 1, 7, 2, 8, 6, 0, 6, 2, 14, 2, 12, 2, 7,\
               2, 7, 0, 6, 2, 14, 2, 12, 2, 6, 1, 15, 2, 8, 6, 1, 15, 0, 18, 0]
    
instructions = program_equ

world = World(1, replacement_strategy = "neighborhood", cm_prob = 0, ins_prob = 0, del_prob = 0)

world.place_custom(instructions)

world.schedule(30)
#%%

"""
Test 9:
    
    Move Up
    
"""

program = [27,0,0,1,2]

world = World(2, replacement_strategy = "neighborhood", cm_prob = 0, ins_prob = 0, del_prob = 0)

world.place_custom(program,(1,0))

print("Before Moving Up")
print(world.pool.get())


world.schedule(1)

print("\nAfter Moving Up")
print(world.pool.get())

#%%

"""
Test 10:
    
    Move Down
    
"""

program = [28,0,0,1,2]

world = World(2, replacement_strategy = "neighborhood", cm_prob = 0, ins_prob = 0, del_prob = 0)

world.place_custom(program,(0,0))

print("Before Moving Down")
print(world.pool.get())


world.schedule(1)

print("\nAfter Moving Down")
print(world.pool.get())

#%%

"""
Test 11:
    
    Move Left
    
"""

program = [29,0,0,1,2]

world = World(2, replacement_strategy = "neighborhood", cm_prob = 0, ins_prob = 0, del_prob = 0)

world.place_custom(program,(0,1))

print("Before Moving Left")
print(world.pool.get())


world.schedule(1)

print("\nAfter Moving Left")
print(world.pool.get())

#%%

"""
Test 12:
    
    Move Right
    
"""

program = [30,0,0,1,2]

world = World(2, replacement_strategy = "neighborhood", cm_prob = 0, ins_prob = 0, del_prob = 0)

world.place_custom(program,(0,0))

print("Before Moving Right")
print(world.pool.get())


world.schedule(1)

print("\nAfter Moving Right")
print(world.pool.get())


#%%
"""
Test 13:
    
    Consume
"""

print("A demonstration of the Consume instruction\n")

program_predator = [17,17,26] + (len(program_xor))*[0]
program_prey = program_xor

world = World(2, replacement_strategy = "neighborhood", cm_prob = 0, ins_prob = 0, del_prob = 0)

world.place_custom(program_predator, position = (0,0))
world.place_custom(program_prey, position = (0,1))

print(world)

#%%
world.schedule(1)
print(world)