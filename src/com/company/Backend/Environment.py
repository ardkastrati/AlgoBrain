# A clean implementation of the Avida World simulator

# %%
# Necessary imports:

import logging
import numpy as np
import DigitalOrganism as DO
from Mediator import Mediator

#divLog = logging.getLogger("Division Logger")
#divLog.setLevel(logging.DEBUG)
#divForm = logging.Formatter('%(message)s')
#divHandler = logging.FileHandler("divlog2.log")
#divHandler.setFormatter(divForm)
#divLog.addHandler(divHandler)

#%%

# We get overflow errors sometimes but for our purposes this is absolutely fine
# We care about the binary representation, not the actual int32 value
# Therefore, ignore overflow warnings
np.warnings.filterwarnings('ignore', 'overflow')

#%% Helper class for breaking nested loops
class BreakIt(Exception): pass

#%% Pool simulates an NxN Petri dish
# Avida organisms live in such a pool

class Pool:

    def __init__(self, N, dtype = None):
        
        if dtype == None:

            self.pool = np.zeros((N,N), dtype = DO.CPUEmulator)
            self.shape = (N,N)
            
        else:
            
            self.pool = np.zeros((N,N), dtype = dtype)
            self.shape = (N,N)

    def get(self,position = None):
        
        if position == None:
            return self.pool
        else:
            return self.pool[position]
    
    def put(self, obj, pos):
        self.pool[pos] = obj
    
    def kill(self,pos):
        self.pool[pos] = 0
        
#%% World is a powerful class which has full knowledge of all of its components

# World regulates everything
# It implements the Mediator abstract interface

class World(Mediator):

    # Pool of size NxN
    
    # Rates contains the metabolic rates of the emulators
    
    # Replacement strategy determines what happens if the pool is full and a
    # new organism is to be born. Per default, the oldest organism in the pool is killed
    
    # Ages keeps track of the ages of the organisms in the corresponding location
    
    # Default copy mutation probability is 0.0025
    
    def __init__(self, N, replacement_strategy = "rates", cm_prob = 0.0025, ins_prob = 0.05, del_prob = 0.05, notify_ = False, log_division = False, log_functions = False):

        # Pool() will contain the set of CPUEmulators.
        self.pool = Pool(N)
        
        self.rates = np.zeros((N,N), dtype = int)
        
        self.ages = np.zeros((N,N), dtype = int)
        
        # Inputs is now an array of tuples of integers
        # The first integer is the most recent input
        # The second integer is the second most recent input
        # Initialize to 0. Assume that 0 means that there was no input yet
        # The probability of an input being exactly 0 is 2^-32
        self.inputs = np.zeros((N,N), dtype = (np.uintc,2))
        
        self.replacement_strategy = replacement_strategy
        
        self.cm_prob = cm_prob
        
        self.ins_prob = ins_prob
        self.del_prob = del_prob
        
        # The following attribute links a world to a concrete experiment
        self.experiment = None
        
        # The following attribute causes the organism to send its last two inputs and
        # the corresponding output to the experiment which has created the world
        # for the purpose of testing
        self.output = False
        
        # Helper, used in react_on_IO
        self.notify_ = notify_
        
        """
        # See whether we want to log divisions
        self.log_division = log_division
        if self.log_division:
            # Create a logger and set its level
            # The logger will be used purely to track organism divisions
            self.divisionLogger = logging.getLogger( __name__ )
            self.divisionLogger.setLevel(logging.DEBUG)
            # Create a file handler and set its level
            f_handler_div = logging.FileHandler('divisions.log')
            f_handler_div.setLevel(logging.DEBUG)
            # Create a formatter and add it to the handler
            f_format_div = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            f_handler_div.setFormatter(f_format_div)
            # Add handler to logger
            self.divisionLogger.addHandler(f_handler_div)
            
        # See whether we want to log functions
        self.log_functions = log_functions
        if self.log_functions:
            # Create a logger and set its level
            # The logger will be used purely to track organism divisions
            self.functionLogger = logging.getLogger( __name__ )
            self.functionLogger.setLevel(logging.DEBUG)
            # Create a file handler and set its level
            f_handler_fun = logging.FileHandler('divisions.log')
            f_handler_fun.setLevel(logging.DEBUG)
            # Create a formatter and add it to the handler
            f_format_fun = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            f_handler_fun.setFormatter(f_format_fun)
            # Add handler to logger
            self.functionLogger.addHandler(f_handler_fun)
        """
        
    """
    The following methods comprise the core functionality of World
    """
    
    # Here the scheduler loop, which runs forever unless told otherwise
    
    def schedule(self, n_loops = None, n_notify = None):
        
        if n_loops == None:
            
            # I want to see how the population is doing every 10k cycles
            
            iterator = 0
            
            while True:
                
                 baseline_rate = self.baseline_rate()
                 
                 # Sanity check notifications, only displayed if parameter n_notify specified
                 iterator += 1
                 
                 if n_notify == None:
                     iterator = 0
                 
                 elif iterator == n_notify:
                     # Shows that the whole thing is alive every 100 cycles
                     print("\nStill running")
                     # A sanity check, just making sure that the ages are behaving
                     # ok
                     print("AGES:")
                     print(self.ages[:10,:10])
                     iterator = 0
                     print("BASELINE RATE: " + str(self.baseline_rate()))
                     print("SHORTEST GENOME: " + str(self.shortest_genome()))
                     print("MAXIMAL RATE: " + str(self.max_rate()))
                     print("LONGEST GENOME: " + str(self.longest_genome()))
                     print("COPY MUTATION PROBABILITY: " + str(self.cm_prob))
            
                 for i in range(self.pool.shape[0]):
                     for j in range(self.pool.shape[1]):
                    
                         if isinstance(self.pool.get()[i][j], DO.CPUEmulator):
                             
                             # Each emulator gets a certain number of cycles assigned to it,
                             # depending on its rate
                             n_cycles = int(self.rates[i][j] / baseline_rate)
                        
                             for i_cycles in range(n_cycles):
                            
                                 current_emulator = self.pool.get()[i][j]
                                 current_emulator.execute_instruction()
                                 self.ages[i][j] = current_emulator.age
        else:
                                
            for i_loops in range(n_loops):
            
                baseline_rate = self.baseline_rate()
            
                for i in range(self.pool.shape[0]):
                    for j in range(self.pool.shape[1]):
                    
                        if isinstance(self.pool.get()[i][j], DO.CPUEmulator):
                        
                            n_cycles = int(self.rates[i][j] / baseline_rate)
                        
                            for i_cycles in range(n_cycles):
                            
                                current_emulator = self.pool.get()[i][j]
                                current_emulator.execute_instruction()
                                self.ages[i][j] = current_emulator.age

    # The following method defines which functions are to be called when world is notified 
    # of various events
    
    def notify(self, sender, event, result):
        
        if event == "division":
            self.react_on_division(sender, result)

        if event == "IO_operation":
            self.react_on_IO(sender, result)
            
        if event == "len_change":
            self.react_on_len_change(sender, result)
            
        if event == "consume":
            self.react_on_consume(sender,result)
            
        if event == "mov_up":
            self.react_on_mov_up(sender,result)
            
        if event == "mov_down":
            self.react_on_mov_down(sender,result)
            
        if event == "mov_left":
            self.react_on_mov_left(sender,result)
            
        if event == "mov_right":
            self.react_on_mov_right(sender,result)
    """
    The methods below define how the world reacts to different notifications
    """
    
    def react_on_mov_right(self,sender,result):
        
        # Find out where the sender is at
        idx0 = np.where(self.pool.get() == sender)[0][0]
        idx1 = np.where(self.pool.get() == sender)[1][0]
        
        sender_pos = (idx0,idx1)
        
        # If the sender is already all the way right it won't be able to move
        if idx1 == self.pool.shape[1]-1:
            pass
        
        else:
            
            # Swap places of sender and organism right of it
            target_pos = (idx0,idx1+1)
            
            # Save target which is to be moved left, along with all of its
            # important properties which the world keeps track of:
            t_org = self.pool.get(target_pos)
            t_inp = self.inputs[target_pos]
            t_rate = self.rates[target_pos]
            t_age = self.ages[target_pos]
            
            # Save sender which is to be moved right, along with all of its
            # important properties which the world keeps track of:
            org = self.pool.get(sender_pos)
            inp = self.inputs[sender_pos]
            rate = self.rates[sender_pos]
            age = self.ages[sender_pos]
            
            # Move the other organism left
            self.pool.put(t_org,sender_pos)
            self.inputs[sender_pos] = t_inp
            self.rates[sender_pos] = t_rate
            self.ages[sender_pos] = t_age
            
            # Move the original organism right
            self.pool.put(org,target_pos)
            self.inputs[target_pos] = inp
            self.rates[target_pos] = rate
            self.ages[target_pos] = age
    
    def react_on_mov_down(self,sender,result):
        
        # Find out where the sender is at
        idx0 = np.where(self.pool.get() == sender)[0][0]
        idx1 = np.where(self.pool.get() == sender)[1][0]
        
        sender_pos = (idx0,idx1)
        
        # If the sender is already all the way down it won't be able to move
        if idx0 == self.pool.shape[0]-1:
            pass
        
        else:
            
            # Swap places of sender and organism below it
            target_pos = (idx0+1,idx1)
            
            # Save target which is to be moved up, along with all of its
            # important properties which the world keeps track of:
            t_org = self.pool.get(target_pos)
            t_inp = self.inputs[target_pos]
            t_rate = self.rates[target_pos]
            t_age = self.ages[target_pos]
            
            # Save sender which is to be moved down, along with all of its
            # important properties which the world keeps track of:
            org = self.pool.get(sender_pos)
            inp = self.inputs[sender_pos]
            rate = self.rates[sender_pos]
            age = self.ages[sender_pos]
            
            # Move the other organism up
            self.pool.put(t_org,sender_pos)
            self.inputs[sender_pos] = t_inp
            self.rates[sender_pos] = t_rate
            self.ages[sender_pos] = t_age
            
            # Move the original organism down
            self.pool.put(org,target_pos)
            self.inputs[target_pos] = inp
            self.rates[target_pos] = rate
            self.ages[target_pos] = age

    def react_on_mov_up(self,sender,result):
        
        # Find out where the sender is at
        idx0 = np.where(self.pool.get() == sender)[0][0]
        idx1 = np.where(self.pool.get() == sender)[1][0]
        
        sender_pos = (idx0,idx1)
        
        # If the sender is already all the way at the top it won't be able to move
        if idx0 == 0:
            pass
        
        else:
            
            # Swap places of sender and organism above it
            target_pos = (idx0-1,idx1)
            
            # Save target which is to be moved down, along with all of its
            # important properties which the world keeps track of:
            t_org = self.pool.get(target_pos)
            t_inp = self.inputs[target_pos]
            t_rate = self.rates[target_pos]
            t_age = self.ages[target_pos]
            
            # Save sender which is to be moved up, along with all of its
            # important properties which the world keeps track of:
            org = self.pool.get(sender_pos)
            inp = self.inputs[sender_pos]
            rate = self.rates[sender_pos]
            age = self.ages[sender_pos]
            
            # Move the other organism down
            self.pool.put(t_org,sender_pos)
            self.inputs[sender_pos] = t_inp
            self.rates[sender_pos] = t_rate
            self.ages[sender_pos] = t_age
            
            # Move the original organism up
            self.pool.put(org,target_pos)
            self.inputs[target_pos] = inp
            self.rates[target_pos] = rate
            self.ages[target_pos] = age
            
    def react_on_mov_left(self,sender,result):
        
        # Find out where the sender is at
        idx0 = np.where(self.pool.get() == sender)[0][0]
        idx1 = np.where(self.pool.get() == sender)[1][0]
        
        sender_pos = (idx0,idx1)
        
        # If the sender is already all the way left it won't be able to move
        if idx1 == 0:
            pass
        
        else:
            
            # Swap places of sender and organism left of it
            target_pos = (idx0,idx1-1)
            
            # Save target which is to be moved right, along with all of its
            # important properties which the world keeps track of:
            t_org = self.pool.get(target_pos)
            t_inp = self.inputs[target_pos]
            t_rate = self.rates[target_pos]
            t_age = self.ages[target_pos]
            
            # Save sender which is to be moved left, along with all of its
            # important properties which the world keeps track of:
            org = self.pool.get(sender_pos)
            inp = self.inputs[sender_pos]
            rate = self.rates[sender_pos]
            age = self.ages[sender_pos]
            
            # Move the other organism right
            self.pool.put(t_org,sender_pos)
            self.inputs[sender_pos] = t_inp
            self.rates[sender_pos] = t_rate
            self.ages[sender_pos] = t_age
            
            # Move the original organism left
            self.pool.put(org,target_pos)
            self.inputs[target_pos] = inp
            self.rates[target_pos] = rate
            self.ages[target_pos] = age

    def react_on_consume(self,sender,result):
        
        # Find out where the sender is at
        idx0 = np.where(self.pool.get() == sender)[0][0]
        idx1 = np.where(self.pool.get() == sender)[1][0]
        
        # Look for a target for consumation.
        # Right now for testing purposes this is the only organism in the neighborhood
        
        width = self.pool.shape[0]
        height = self.pool.shape[1]
        
        position = None
        
        try:
            for i in range(max(idx0-1, 0), min(idx0+2, width)):
                for j in range(max(idx1-1, 0), min(idx1+2, height)):
                    if i == idx0 and j == idx1:
                        continue
                    if self.pool.get()[i][j] != 0:
                        position = (i,j)
                        raise BreakIt
        except BreakIt:
                pass
            
        if position == None:
            pass
        
        else:
        
            # The emulator at position "position" is to be consumed
            prey = self.pool.get(position)
        
            # Take its memory content
            prey_memory = prey.memory
            
        
            # Take the predator's memory content and its IP
            predator = self.pool.get((idx0,idx1))
        
            ip = predator.instr_pointer.get()
            predator_memory = predator.memory
            
            # Save its age and inputs to restore to later
            age = predator.age
            ins = self.inputs[(idx0,idx1)]
        
            # Initialize iterator which keeps track of where the instructions are
            # to be inserted
            iterator = ip + 1
        
           # Insert prey_memory into predator_memory starting at index ip+1
        
            for i in range(len(prey_memory)):
                predator_memory.insert(iterator+i,prey_memory[i])
            
            # Kill prey
        
            self.pool.kill(position)
            self.inputs[position] = (0,0)
            self.rates[position] = 0
            self.ages[position] = 0
        
            # Create new Organism with predator_memory at sender position
        
            self.place_custom(predator_memory,(idx0,idx1))
            
            # Modify IP such that execution continues right where we left off
            self.pool.get((idx0,idx1)).instr_pointer.set(ip+1)
            
            # Restore age and inputs
            self.pool.get((idx0,idx1)).age = age+1
            self.inputs[(idx0,idx1)] = ins
            
        
    # Here how the world reacts upon organism division
    
    def react_on_division(self, sender, result):
        
        # No division allowed in a 1x1 size pool
        if self.pool.shape == (1,1):
            pass
        
        else:
        
            # Find out where the sender is at
            idx0 = np.where(self.pool.get() == sender)[0][0]
            idx1 = np.where(self.pool.get() == sender)[1][0]
        
            # Log the division:
            """
                if self.log_division:
                self.divisionLogger.info('\n Parent: {} \n Child: \n {}'.format(sender.original_memory, result))
            """
        
            # divLog.info('{}\n{}\n'.format(sender.original_memory, result))
            # The organism, upon valid division, notifies the world of it using
            # self.mediator.notify(sender = self, event = "division", result = result)

            # Create a program from the result passed from the organism which underwent division
            program = DO.Program(result)
        
            # Create a new emulator and load the resulting program in it
            emulator = DO.CPUEmulator()
            emulator.load_program(program)
        
            # Link self as the new emulator's mediator
            emulator.mediator = self
        
            # Set the mutation probabilities as defined in the world
            emulator.mutation_prob = self.cm_prob
            emulator.ins_prob = self.ins_prob
            emulator.del_prob = self.del_prob
        
            # The child inherits the ancestor from its parent
            emulator.ancestor = sender.ancestor.copy()
        
            # The mutations which resulted in the child:
            emulator.mutations = sender.mutations + sender.child_mutations
            
            # Default replacement strategy
            # Look for free spots in the 1-hop neighborhood of the parent
            # If there is a free spot, put the offspring into any such spot
            # If not, kill the oldest organism in the neighborhood and put offspring there
            # Note that the oldest organism in the neighborhood may be the parent itself
            if self.replacement_strategy == "neighborhood":
            
                width = self.pool.shape[0]
                height = self.pool.shape[1]
            
                # The neighborhood of the cell:
                # Iterate over rows max(idx0-1,0) idx0, min(idx0+1, pool height - 1)
                # Iterate over columns max(idx1-1,0), idx1, min(idx1 + 1, pool width - 1)
            
                # Breaking out of nested loops: 
                # https://stackoverflow.com/questions/653509/breaking-out-of-nested-loops
            
                position = None
                oldest = 0
            
                # Looking for a free position and simultaneously checking which organism
                # in the neighborhood is the oldest one
                try:
                    for i in range(max(idx0-1, 0), min(idx0+2, width)):
                        for j in range(max(idx1-1, 0), min(idx1+2, height)):
                            # No suicides!
                            if i == idx0 and j == idx1:
                                pass
                            else:
                                if self.pool.get()[i][j] == 0:
                                    position = (i,j)
                                    raise BreakIt
                                elif self.ages[i][j] >= oldest:
                                    oldest = self.ages[i][j]
                                    position = (i,j)                          
                except BreakIt:
                    pass

            # Define kill_oldest replacement strategy as:
            # If there is a free spot in the pool, put child there
            # Otherwise, kill oldest organism in the pool and put child there
        
            elif self.replacement_strategy == "kill_oldest":
            
                # If there is a free spot put the cell there
                if 0 in self.pool.get():
            
                    i0 = np.where(self.pool.get() == 0)[0][0]
                    i1 = np.where(self.pool.get() == 0)[1][0]
                    position = (i0, i1)
        
                else:
            
                    position = self.oldest_position()      
                
            # This replacement strategy kills the neighboring organism with the lowest rate        
            elif self.replacement_strategy == "rates":
            
                width = self.pool.shape[0]
                height = self.pool.shape[1]
            
                # The neighborhood of the cell:
                # Iterate over rows max(idx0-1,0) idx0, min(idx0+1, pool height - 1)
                # Iterate over columns max(idx1-1,0), idx1, min(idx1 + 1, pool width - 1)
            
                # Breaking out of nested loops: 
                # https://stackoverflow.com/questions/653509/breaking-out-of-nested-loops
            
                position = None
                weakest = np.max(self.rates)
            
                # Looking for a free position and simultaneously checking which organism
                # in the neighborhood is the weakest one
                try:
                    for i in range(max(idx0-1, 0), min(idx0+2, width)):
                        for j in range(max(idx1-1, 0), min(idx1+2, height)):
                            # No suicides!
                            if i == idx0 and j == idx1:
                                pass
                            else:
                                if self.pool.get()[i][j] == 0:
                                    position = (i,j)
                                    raise BreakIt
                                elif self.rates[i][j] <= weakest:
                                    weakest = self.rates[i][j]
                                    position = (i,j)                          
                except BreakIt:
                    pass
                
            # This replacement strategy kills the neighboring organism with the
            # highest age/rate ratio
            elif self.replacement_strategy == "ratio":
            
                width = self.pool.shape[0]
                height = self.pool.shape[1]
            
                # The neighborhood of the cell:
                # Iterate over rows max(idx0-1,0) idx0, min(idx0+1, pool height - 1)
                # Iterate over columns max(idx1-1,0), idx1, min(idx1 + 1, pool width - 1)
            
                # Breaking out of nested loops: 
                # https://stackoverflow.com/questions/653509/breaking-out-of-nested-loops
            
                position = None
                weakest = 0
            
                # Looking for a free position and simultaneously checking which organism
                # in the neighborhood is the weakest one
                try:
                    for i in range(max(idx0-1, 0), min(idx0+2, width)):
                        for j in range(max(idx1-1, 0), min(idx1+2, height)):
                            # No suicides!
                            if i == idx0 and j == idx1:
                                pass
                            else:
                                if self.pool.get()[i][j] == 0:
                                    position = (i,j)
                                    raise BreakIt
                                elif self.ages[i][j]/self.rates[i][j] >= weakest:
                                    weakest = self.ages[i][j]/(2*self.rates[i][j])
                                    position = (i,j)                          
                except BreakIt:
                    pass
            
            # Put the created emulator in the found position
            self.pool.put(emulator, position)
        
            # Put age 0 in the correct position
            self.ages[position] = 0
        
            # Update rates
            self.rates[position] = sender.child_rate
        
            # Set input to none
            self.inputs[position] = (0,0)

    # Here how the world reacts upon an IO operation        

    def react_on_IO(self, sender, result):
        
        # Find the position in the pool where the sender is at:
        idx0 = np.where(self.pool.get() == sender)[0][0]
        idx1 = np.where(self.pool.get() == sender)[1][0]
        
        # If the most recent input is none, do nothing
        if self.inputs[idx0][idx1][0] == 0:
            pass
        
        # Filtering outputs
        elif -7 < result < 7:
            pass
        elif self.inputs[idx0][idx1][0] == ~self.inputs[idx0][idx1][1]:
            pass
        elif ~self.inputs[idx0][idx1][0] == self.inputs[idx0][idx1][1]:
            pass
        elif self.inputs[idx0][idx1][0] & ~self.inputs[idx0][idx1][1] == self.inputs[idx0][idx1][0]:
            pass
        elif (~self.inputs[idx0][idx1][0] & self.inputs[idx0][idx1][1]) == self.inputs[idx0][idx1][1]:
            pass
        elif self.inputs[idx0][idx1][0] & ~self.inputs[idx0][idx1][1] == self.inputs[idx0][idx1][1]:
            pass
        elif ~self.inputs[idx0][idx1][0] & self.inputs[idx0][idx1][1] ==self.inputs[idx0][idx1][0]:
            pass
        elif self.inputs[idx0][idx1][0] | self.inputs[idx0][idx1][1] == self.inputs[idx0][idx1][0]:
            pass
        elif self.inputs[idx0][idx1][0] | self.inputs[idx0][idx1][1] ==    self.inputs[idx0][idx1][1]:
            pass
        elif self.inputs[idx0][idx1][0] | ~self.inputs[idx0][idx1][1] == self.inputs[idx0][idx1][0]:
            pass
        elif self.inputs[idx0][idx1][0] | ~self.inputs[idx0][idx1][1] == self.inputs[idx0][idx1][1]:
            pass
        elif ~self.inputs[idx0][idx1][0] | self.inputs[idx0][idx1][1] == self.inputs[idx0][idx1][0]:
            pass
        elif ~self.inputs[idx0][idx1][0] | self.inputs[idx0][idx1][1] == self.inputs[idx0][idx1][1]:
            pass
        
        # If the most recent input isn't none, but the second most recent is, check if not was computed
        elif self.inputs[idx0][idx1][0] != 0 and self.inputs[idx0][idx1][1] == 0:
            
            if self.inputs[idx0][idx1][0] == ~result:
                
                # Save input, result and the organism that computed it
                input_ = self.inputs[idx0][idx1][0]
                
                # Notify us about what happened
                if self.notify_:
                    print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED NOT\nINPUT:  " + str(input_) + "\nOUTPUT: " + str(result))

                # Check whether the organism has computed not previously
                # If not, reward.
                if sender.fun_not == False:
                    sender.fun_not = True
                    sender.child_rate *= 2
                
                # If yes, ignore
                else:
                    pass
                
                # Notify the experiment about this event, if the current world is linked to one
                if self.experiment != None and not self.output:
                    #print("Notifying experiment of NOT")
                    self.experiment.notify(sender = sender, event = "not", result = sender.original_memory)
                    
                if self.output:
                    print("Notifying experiment of function_IO")
                    self.experiment.notify(sender = sender, event = "function_IO", result = ((self.inputs[idx0][idx1][0],self.inputs[idx0][idx1][1],result)))
        
        # If the two most recent inputs aren't none, check whether a function of the two most recent inputs was computed
        elif self.inputs[idx0][idx1][0] != 0 and self.inputs[idx0][idx1][1] != 0:
            
            # If a NOT was computed
            
            if result == ~self.inputs[idx0][idx1][0]:
                
                # Save input, result and the organism that computed it
                input_ = self.inputs[idx0][idx1]
                
                # Notify us about what happened
                if self.notify_:
                    print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED NOT\nINPUT:  " + str(input_[0]) + "\nOUTPUT: " + str(result))

                
                # Check whether the organism has computed not previously
                # If not, reward.
                if sender.fun_not == False:
                    sender.fun_not = True
                    sender.child_rate *= 2

                # If yes, ignore
                else:
                    pass
                
                # Notify the experiment about this event, if the current world is linked to one
                if self.experiment != None and not self.output:
                    #print("Notifying experiment of NOT")
                    self.experiment.notify(sender = sender, event = "not", result = sender.original_memory)
                    
                if self.output:
                    print("Notifying experiment of function_IO")
                    self.experiment.notify(sender = sender, event = "function_IO", result = ((self.inputs[idx0][idx1][0],self.inputs[idx0][idx1][1],result)))
            
            # If a NAND was computed
            elif result == ~(self.inputs[idx0][idx1][0] & self.inputs[idx0][idx1][1]):
                
                # Save input, result and the organism that computed it
                input_ = self.inputs[idx0][idx1]
                
                # Notify us about what happened
                if self.notify_:
                    print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED NAND\nINPUT: " + str(input_) + "\nOUTPUT:  " + str(result))

                # Check whether the organism has computed nand previously
                # If not, reward.
                if sender.fun_nand == False:
                    sender.fun_nand = True
                    sender.child_rate *= 2
                
                # If yes, ignore
                else:
                    pass
                
                # Notify the experiment about this event, if the current world is linked to one
                if self.experiment != None and not self.output:
                    #print("Notifying experiment of NAND")
                    self.experiment.notify(sender = sender, event = "nand", result = sender.original_memory)
                    
                if self.output:
                    print("Notifying experiment of function_IO")
                    self.experiment.notify(sender = sender, event = "function_IO", result = ((self.inputs[idx0][idx1][0],self.inputs[idx0][idx1][1],result)))
                
            # If an AND was computed
            elif result == self.inputs[idx0][idx1][0] & self.inputs[idx0][idx1][1]:
                
                # Save input, result and the organism that computed it
                input_ = self.inputs[idx0][idx1]
                
                # Notify us about what happened
                if self.notify_:
                    print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED AND\nINPUT: " + str(input_) + "\nOUTPUT:  " + str(result))

                # Check whether the organism has computed and previously
                # If not, reward.
                if sender.fun_and == False:
                    sender.fun_and = True
                    sender.child_rate *= 4
                
                # If yes, ignore
                else:
                    pass
                
                # Notify the experiment about this event, if the current world is linked to one
                if self.experiment != None and not self.output:
                    #print("Notifying experiment of AND")
                    self.experiment.notify(sender = sender, event = "and", result = sender.original_memory)
                    
                if self.output:
                    print("Notifying experiment of function_IO")
                    self.experiment.notify(sender = sender, event = "function_IO", result = ((self.inputs[idx0][idx1][0],self.inputs[idx0][idx1][1],result)))
                
            # If an OR_N was computed
            elif result == self.inputs[idx0][idx1][0] | ~self.inputs[idx0][idx1][1] or result == ~self.inputs[idx0][idx1][0] | self.inputs[idx0][idx1][1]:

                input_ = self.inputs[idx0][idx1]
                
                # Notify us about what happened
                if self.notify_:
                    print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED OR_N\nINPUT: " + str(input_) + "\nOUTPUT:  " + str(result))
                
                
                # Check whether the organism has computed or_n previously
                # If not, reward.
                if sender.fun_or_n == False:
                    sender.fun_or_n = True
                    sender.child_rate *= 4
                
                # If yes, ignore
                else:
                    pass
                
            # If an OR was computed
            elif result == self.inputs[idx0][idx1][0] | self.inputs[idx0][idx1][1]:
                
                input_ = self.inputs[idx0][idx1]
                
                # Notify us about what happened
                if self.notify_:
                    print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED OR\nINPUT: " + str(input_) + "\nOUTPUT:  " + str(result))

                # Check whether the organism has computed or previously
                # If not, reward.
                if sender.fun_or == False:
                    sender.fun_or = True
                    sender.child_rate *= 8
                
                # If yes, ignore
                else:
                    pass
                
                # Notify the experiment about this event, if the current world is linked to one
                if self.experiment != None and not self.output:
                    #print("Notifying experiment of OR")
                    self.experiment.notify(sender = sender, event = "or", result = sender.original_memory)
                    
                if self.output:
                    print("Notifying experiment of function_IO")
                    self.experiment.notify(sender = sender, event = "function_IO", result = ((self.inputs[idx0][idx1][0],self.inputs[idx0][idx1][1],result)))
                
            # If an AND_N was computed
            elif result == np.uintc(self.inputs[idx0][idx1][0] & ~self.inputs[idx0][idx1][1]) or result == np.uintc(~self.inputs[idx0][idx1][1] & self.inputs[idx0][idx1][0]):
                
                input_ = self.inputs[idx0][idx1]
                
                # Notify us about what happened
                if self.notify_:
                    print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED AND_N\nINPUT: " + str(input_) + "\nOUTPUT:  " + str(result))
                
                # Check whether the organism has computed and_n previously
                # If not, reward.
                if sender.fun_and_n == False:
                    sender.fun_and_n = True
                    sender.child_rate *= 8
                
                # If yes, ignore
                else:
                    pass
                
                # Notify the experiment about this event, if the current world is linked to one
                if self.experiment != None and not self.output:
                    #print("Notifying experiment of AND_N")
                    self.experiment.notify(sender = sender, event = "and_n", result = sender.original_memory)
                    
                if self.output:
                    print("Notifying experiment of function_IO")
                    self.experiment.notify(sender = sender, event = "function_IO", result = ((self.inputs[idx0][idx1][0],self.inputs[idx0][idx1][1],result)))
                
            # If a NOR was computed
            elif result == ~(self.inputs[idx0][idx1][0] | self.inputs[idx0][idx1][1]):
                
                input_ = self.inputs[idx0][idx1]
                
                # Notify us about what happened
                if self.notify_:
                    print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED NOR\nINPUT: " + str(input_) + "\nOUTPUT:  " + str(result))

                # Check whether the organism has computed nand previously
                # If not, reward.
                if sender.fun_nor == False:
                    sender.fun_nor = True
                    sender.child_rate *= 16
                
                # If yes, ignore
                else:
                    pass
                
                # Notify the experiment about this event, if the current world is linked to one
                if self.experiment != None and not self.output:
                    #print("Notifying experiment of NOR")
                    self.experiment.notify(sender = sender, event = "nor", result = sender.original_memory)
                    
                if self.output:
                    print("Notifying experiment of function_IO")
                    self.experiment.notify(sender = sender, event = "function_IO", result = ((self.inputs[idx0][idx1][0],self.inputs[idx0][idx1][1],result)))
                
            # If an XOR was computed:
            #elif result == self.inputs[idx0][idx1][0] ^ self.inputs[idx0][idx1][1]:
            elif result == ((self.inputs[idx0][idx1][0] & ~self.inputs[idx0][idx1][1]) | (~self.inputs[idx0][idx1][0] & self.inputs[idx0][idx1][1])):
                
                # Save input, result and the organism that computed it
                input_ = self.inputs[idx0][idx1]
                
                # Notify us about what happened
                if self.notify_:
                    print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED XOR\nINPUT: " + str(input_) + "\nOUTPUT: " + str(result))  
                
                # Check whether the organism has computed xor previously
                # If not, reward.
                if sender.fun_xor == False:
                    sender.fun_xor = True
                    sender.child_rate *= 16

                # If yes, ignore
                else:
                    pass
                
                # Notify the experiment about this event, if the current world is linked to one
                if self.experiment != None and not self.output:
                    print("Notifying experiment of XOR")
                    self.experiment.notify(sender = sender, event = "xor", result = sender.original_memory)
                    
                if self.output:
                    print("Notifying experiment of function_IO")
                    self.experiment.notify(sender = sender, event = "function_IO", result = ((self.inputs[idx0][idx1][0],self.inputs[idx0][idx1][1],result)))
                
            # If EQU was computed:
            elif result == equ(self.inputs[idx0][idx1][0], self.inputs[idx0][idx1][1]):
                
                # Save input, result and the organism that computed it
                input_ = self.inputs[idx0][idx1]
                
                # Notify us about what happened
                if self.notify_:
                    print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED EQU\nINPUT: " + str(input_) + "\nOUTPUT: " + str(result))  
                
                # Check whether the organism has computed xor previously
                # If not, reward.
                if sender.fun_equ == False:
                    sender.fun_equ = True
                    sender.child_rate *= 32
                
                # If yes, ignore
                else:
                    pass
     
        # A random 32-bit number
        #to_input = np.random.randint(low = 0, high = 4294967295, dtype = np.uintc)
        to_input = np.random.randint(low = 0, high = 4294967295, dtype = np.uintc)
        
        # Put the randomly generated number into the input buffer of the emulator
        sender.cpu.input_buffer.put(to_input)
        
        # Update inputs array
        # Old newest input gets placed into position 1
        # New input gets placed into position 0
        self.inputs[idx0][idx1][1] = self.inputs[idx0][idx1][0]
        self.inputs[idx0][idx1][0] = to_input
        
    """
    Everything that follows doesn't compose the core functionality of World.
    These are all helper methods whose purpose is cleaning up the above syntax
    """
    
    # The following method instantiates a default self-replicating organism
    # as a random location in the pool, unless location specified otherwise
    # The location must be a valid tuple
    
    # Default as per Avida-ED website and Nature paper. Contains 35 nop-c in the middle
    # In total 50 instructions
    
    def place_default(self, position = None):
        
        self.place_custom([16, 20, 2, 0, 21] + [2]*36 + [20, 19, 25, 2, 0, 17, 21, 0, 1], position = position)
        
    # Default per avida paper, with only 15 instructions
    def place_default_15(self, position = None):
        
        self.place_custom([16, 20, 2, 0, 21, 2, 20, 19, 25, 2, 0, 17, 21, 0, 1], position = position)
        
    # Almost the same as the original default, only initialized with a couple of IO operations
    def place_def_io(self, position = None):
        
        self.place_custom([16, 20, 2, 0, 21] + [2]*18 + [18,0,18,2] + [2]*18 + [20, 19, 25, 2, 0, 17, 21, 0, 1], position = position)
        
    # The following method instantiates a custom self-replicating organism
    # as a random location in the pool, unless location specified otherwise
    # The location must be a valid tuple
    
    # This function should always be used to place organisms in the pool
        
    def place_custom(self, program, position = None):
        
        # Create program
        default_program = DO.Program(program)
        
        # Create a new emulator
        emulator = DO.CPUEmulator()
        
        # Load self as the emulator's mediator
        emulator.mediator = self
        
        # Initialize the ancestor. It is the organism itself. All of its children
        # will inherit this attribute
        emulator.ancestor = program.copy()
        
        # Set the copy mutation probability as defined in the world
        emulator.mutation_prob = self.cm_prob
        
        # Set the insertion and deletion mutation probabilities as defined in the world
        emulator.ins_prob = self.ins_prob
        emulator.del_prob = self.del_prob
        
        # Load program into emulator
        emulator.load_program(default_program)
        
        # Create random valid position or check if given position valid
        if position == None:
            
            position = (np.random.randint(0, self.pool.shape[0]), np.random.randint(0, self.pool.shape[1]))
            
        else:
            
            assert type(position) == tuple, "Given position is not a tuple"
            assert position[0] < self.pool.shape[0] and position[1] < self.pool.shape[1], "Positions out of bounds"
            
        # Put the emulator at the given position
        
        self.pool.put(emulator,position)
        
        # Put the emulator rate in the corresponding position
        # The world keeps track of the metabolic rates
        # Per default, upon any organism instantiation, the metabolic rate is
        # equal to its memory length
        
        #self.rates[position] = len(emulator.original_memory)
        self.rates[position] = len(emulator.original_memory)
        
        # Pull out the age of the organism
        
        self.ages[position] = emulator.age

    def react_on_len_change(self,sender,result):
        
        # If an organism splits unevenly adjust its rate
        # such that it's proportional to its new length
        
        # Find the emulator
        idx0 = np.where(self.pool.get() == sender)[0][0]
        idx1 = np.where(self.pool.get() == sender)[1][0]
        
        # Update rate
        self.rates[idx0][idx1] = result
 
    def oldest_position(self):
        
        # Returns the position of the oldest emulator in the pool
        # If there are several such emulators with equal age, returns the first one
        # it encounters
        
        for i in range(0,self.pool.shape[0]):
            for j in range(0,self.pool.shape[1]):
                
                if isinstance(self.pool.get()[i][j], DO.CPUEmulator):
                    self.ages[i][j] = self.pool.get()[i][j].age
        
        idx0 = np.where(self.ages == np.max(self.ages))[0][0]
        idx1 = np.where(self.ages == np.max(self.ages))[1][0]
        
        return (idx0, idx1)
    
    def baseline_rate(self):
        
        # Returns the smallest metabolic rate value present
        return np.min(self.rates[self.rates > 0])
    
    def max_rate(self):
        
        # Returns the maximal metabolic rate value present
        return np.max(self.rates[self.rates > 0])
    
    def get_pool(self):
        
        return self.pool.get()
    
    # Returns the emulator at the given position
    
    def get(self,position):
        
        return self.pool.get()[position]
    
    # A function that fills the world with the chosen organism type
    def fill(self, organism_type = "default_IO"):
        
        if organism_type == "default_IO":
            
            for i in range(self.pool.shape[0]):
                for j in range(self.pool.shape[1]):
                    self.place_def_io((i,j))
                    
        elif organism_type == "default":
            
            for i in range(self.pool.shape[0]):
                for j in range(self.pool.shape[1]):
                    self.place_default((i,j))
                    
        elif type(organism_type) == list:
            for i in range(self.pool.shape[0]):
                for j in range(self.pool.shape[1]):
                    self.place_custom(organism_type,(i,j))
    
    # Find the minimum genome length present in the pool
    def shortest_genome(self):
        
        shortest = 1000
        
        for i in range(self.pool.shape[0]):
            for j in range(self.pool.shape[1]):
                length = self.pool.get()[i][j].instruction_memory.size()
                if length <= shortest:
                    shortest = length
                    
        return shortest
    
    # Find the maximum genome length present in the pool
    def longest_genome(self):
        
        longest = -1
        
        for i in range(self.pool.shape[0]):
            for j in range(self.pool.shape[1]):
                length = self.pool.get()[i][j].instruction_memory.size()
                if length >= longest:
                    longest = length
                    
        return longest
            
    # A string representation of the world pool

    def __str__(self):
        
        emulators = self.pool.get()[self.pool.get() != 0]
         
        for i in range(emulators.size):
            
            print("Emulator " + str(i + 1) + ": ")
            print(emulators[i])

        return ""

#%% General Helper Functions:
    
def not_(a):
    result = np.uintc(~a)
    return result

# Returns EQU of two numbers
def equ(a,b):
    return (a & b) | (~a & ~b)