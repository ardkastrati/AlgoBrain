class Program:

    # A class that will need to hold anything that could count as a program

    # As a start, for the Avida-type implementation, all we need to consider as a program is a list of instructions

    # We also need to consider what data type the instructions will be. I'd say integers.

    # How many instructions do we have? Only around 32. short will do, int is a waste of space

    # Short is not defined in Python. Int will have to do.

    # For now just one instruction, indexed with 0

    # How about this:

    # A class attribute as a list. The list can be as long as possible. Each instruction is defined by an int
    # and the list only permits integers up to the value of (number of instructions) - 1

    # Initializing an empty program.

    # How about we only start with a couple of random instructions. Let's see what those could be.

    # For now I'll just work on a cpu with three registers and only one instruction
    # This instruction (Instruction 0) exchanges the values inside the first two registers

    def __init__(self, instr_list):
        # Again, we need a way of checking whether what has been passed here is a valid list of instructions.
        # Would make sense to define a separate method which does that (overkill maybe?)

        self.instructions = instr_list

    # Will check whether the passed list is a valid list of instructions. TODO.
    def check_Validity(instr_list):
        # What will our instructions look like?
        #
        # try:
        #
        # except AttributeError:
        #   raise NotImplementedError('Instruction_List isn't valid')

        pass

    def get_Instructions(self):
        return self.instructions


# %%

class Machine:

    # An Avida machine needs the following libraries to function:
    # from queue import LifoQueue

    # The state of the machine is defined by the values in its three registers
    # Instruction pointer? Yeah probably. I'd want it to loop around to the beginning once it has reached the end of the program
    # Or no, rather just stop (for now, we'll need to make it loop later)

    # The constructor. To be expanded with an additional instruction pointer (And also those headers we saw in the paper).
    # All of the arguments passed here should FULLY determine the state of the Machine.

    # Need to add the stack too. Will have to take a closer look at the details of the implementation.
    # Should we just copy the Avida Instruction set? (Give credits if necessary, but I mean who owns an instruction set)
    # Should we make something simpler? But we need to then make sure that every possible permutation of any number of instructions
    # constitutes a valid program. That's a hefty task. Rather copy.

    # What's a good datatype to store stacks in Python?

    # Answer: LIFO Queue, already implemented as a library

    def __init__(self, a, b, c):

        # The libraries our machine will need will be imported
        # whenever the first constructor is called
        # TO CHECK: Does it work like this?
        # It seems to but I don't know the details
        from queue import LifoQueue

        self.reg_a = a
        self.reg_b = b
        self.reg_c = c

        # Adding the instruction pointer. Don't need it yet but will later.
        # Initialize it to 0

        # Increase it by 1 after each executed instruction
        self.instr_pointer = 0

        self.stack0 = LifoQueue()
        self.stack1 = LifoQueue()
        self.active_stack = 0
    # Oh, this will be strictly an Avida machine. It has to keep track of what differently indexed instructions do

    # How can I ensure that p is of class "Program"

    # Idea for now: First read program and then execute it. This way we have the list of instructions saved here.
    # We'll need that in order to be able to copy it later.

    # Do I need the separate methods "read_Program" and "execute_Program"?
    # Is there any advantage to this that we could see being useful to us in the future?
    # Is it better to maybe just wrap it all up in one method, "execute_Program(self,p)"
    # which saves a program and executes it at the same time

    # Let's keep it like this for now but it could be unoptimal

    # This will just read a Program type instance and save its instructions in the memory of the CPU
    def read_Program(self, p):

        # A very basic way of checking whether the argument is of class Program

        if not isinstance(p, Program):
            raise NotImplementedError
            # Here I want an error statement, not just a print
            print("In Machine_read_Program(p), p is not an instance of Program")

        self.instruction_list = p.get_Instructions()

    # The method which defines which function is to be executed after reading each instruction.
    # The functions to be executed aren't defined explicitly as functions, but as a set of statements after a case check

    # When we get a couple more of them we can see whether it makes sense to also define seperate functions for each instr.
    def execute_Instruction(self, i):
        self.active_stack = self.stack0
        # This will be a lookup table where we'll see what each instruction is supposed to do
        #swap instruction!
        if i == 0:
            # Might need to worry about deleting variables so the memory doesn't get blocked up
            # Does temp need to be deleted explicitly?
            # Well, let's do it just to be safe

            temp = self.reg_a
            self.reg_a = self.reg_b
            self.reg_b = temp

            del temp
        # compare if register a == register b
        if i == 1:
            if(self.reg_b != self.reg_c):
                i+=1
            else:
                i+=2
            #print("instruction here")
        if i == 2:
            temp = self.active_stack.get()
            self.reg_b = temp
            del temp

        if i == 3:
            self.active_stack.put(self.reg_b)
        #swap_Stacks
        if i == 4:
            if self.active_stack == self.stack0:
                self.active_stack = self.stack1
            else:
                self.active_stack = self.stack0
        if i == 5:
            self.reg_b = self.reg_b+1
        if i == 6:
            self.reg_b = self.reg_b-1
        if i == 7:
            self.reg_b = self.reg_b + self.reg_c
        if i == 8:
            self.reg_b = self.reg_b - self.reg_c
        if i == 9:
            if self.reg_b == self.reg_c:
                self.reg_b = False
            else:
                self.reg_b = True
        if i == 10:
            if self.reg_b < self.reg_c:
                self.reg_b = self.reg_b+1
            else:
                self.reg_b = self.reg_b+2


    # This function takes no arguments, it just executes the program that's saved in the CPU's memory
    def execute_Program(self):

        # For now it just executes each instruction in the list one by one
        # When the last instruction is executed we stop

        while self.instr_pointer < len(self.instruction_list):

            temp = self.instr_pointer

            self.execute_Instruction(self.instruction_list[self.instr_pointer])

            # We have to allow for the possibility of the instruction changing the value of the IP
            # But we also have to ensure that if the instruction did nothing to explicitly change the IP,
            # that it's automatically increased by 1

            # Two options: Explicitly make each instruction change the IP as desired, or:

            # If it wasn't changed by an instruction, increase by 1, otherwise leave it
            if self.instr_pointer == temp:
                self.instr_pointer += 1

    # Just to have a nice string representation.
    # This should print out all of the important variables that define the state of the machine.
    # For now it's only the three registers + IP
    def __str__(self):
        string_representation = "Register A: " + str(self.reg_a) + "\nRegister B: " + str(
            self.reg_b) + "\nRegister C: " + str(self.reg_c) + "\nInstruction Pointer: " + str(self.instr_pointer)
        return string_representation
test_program = Program([3,2,0])
test_program.instructions
test_machine = Machine(4, 7, 8)
print(test_machine)
test_machine.read_Program(test_program)
test_machine.execute_Program()
print(test_machine)