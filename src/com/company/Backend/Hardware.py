from queue import LifoQueue
from queue import Queue

import numpy as np

# %% The Register Class

# Contains a single integer value

class Register:

    def __init__(self,value = 0):
        value = np.uintc(value)
        self.content = value

    def write(self,value):
        value = np.uintc(value)
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

    def increment(self, a = 1):
        self.value += a

    def get(self):
        return self.value
    
    def next(self):
        return self.value + 1

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

    def set(self,a):
        self.value = a

class FlowControlHead:

    def __init__(self):
        self.value = 0

    def increment(self, a = 1):
        self.value += a

    def get(self):
        return self.value

    def set(self,a):
        self.value = a

# %% The Memory

class Memory:

    def __init__(self):
        self.content = []

    # Wipe the memory completely
    def wipe(self):
        self.content = []

    def size(self):
        return len(self.content)

    def get(self,index):
        if len(self.content) > index:
            return self.content[index]
        else:
            raise Exception("Index out of boundaries")

    def read(self):
        return self.content

    def append(self,value):
        self.content.append(value)

# %% The CPU (Virtual Hardware)

class CPU:

    def __init__(self, a, b, c):

        self.reg_a = Register(a)
        self.reg_b = Register(b)
        self.reg_c = Register(c)

        self.stack0 = LifoQueue()
        self.stack1 = LifoQueue()
        self.active_stack = self.stack0

        self.input_buffer = Queue()
        self.output_buffer = Queue()

    def clear(self):

        self.reg_a.write(0)
        self.reg_b.write(0)
        self.reg_c.write(0)

        while not self.stack0.empty():
            self.stack0.get()

        while not self.stack1.empty():
            self.stack1.get()

        while not self.input_buffer.empty():
            self.input_buffer.get()

        while not self.output_buffer.empty():
            self.output_buffer.get()