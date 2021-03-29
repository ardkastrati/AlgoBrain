# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 18:44:45 2021

@author: Tbuob
"""

"""Here we define our starting programm!
"""
import SimpleAvida as SA
#%%
class Start:
    list = [1,1,1,1,1,1,1,1,1,1,1,16,17,18]
    def __init__(self,list):
        self.list = list
    def startprogram(self,a,b):
        self.a = a
        self.b = b
        return self.list
#%%
class run:
    def __init__(self,emulator):
        self.emulator = emulator
    def runcell(self):
        Emulator0 = SA.CPUEmulator(1,2,5)
        print(Emulator0)
        program0 = SA.Program(list)
        Emulator0.load_program(program0)
        Emulator0.execute_program()
        print(Emulator0)
        
#%%
run(1)

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

program = SA.Program([16,20,2,0,21,2,20,19,25,2,0,17,21,0,1])

