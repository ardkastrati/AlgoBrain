# A clean implementation of the Avida World simulator

# %%
# Necessary imports:

import numpy as np
import DigitalOrganism as DO
from Mediator import Mediator
import logging
logger = logging.getLogger( __name__ )
logger2 = logging.getLogger(__name__)
logger3 = logging.getLogger(__name__)
logger4 = logging.getLogger(__name__)
formatter_1 = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
formatter_2 = logging.Formatter('%(asctime)s:%(message)s')
formatter_3 = logging.Formatter('%(relativeCreated)d')
formatter_4 = logging.Formatter('%(message)s')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('Function5.log')
file_handler.setFormatter(formatter_1)#,formatter_2,formatter_3
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter_2)
stream_handler_program = logging.StreamHandler()
stream_handler_program.setFormatter(formatter_4)
file_handler_2 = logging.FileHandler('Function_5.log')
file_handler_3 = logging.FileHandler('Organism_5.log')
file_handler_3.setFormatter(formatter_4)
file_handler_2.setFormatter(formatter_3)
#logger.addHandler(stream_handler)
logger.addHandler(file_handler)
#logger.addHandler(stream_handler_program)
logger2.addHandler(file_handler_2)
logger3.addHandler(stream_handler_program)
logger2.setLevel(logging.INFO)
logger3.setLevel(logging.INFO)
logger4.addHandler(file_handler_3)
logger4.setLevel(logging.DEBUG)

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

            self.pool = np.zeros((N,N))
            self.shape = (N,N)
            
        else:
            
            self.pool = np.zeros((N,N), dtype = dtype)
            self.shape = (N,N)

    def get(self):
        
        return self.pool
    
    def put(self, obj, pos):
        
        self.pool[pos] = obj
    
#%% World is a powerful class which has full knowledge of all of its components

# World regulates everything
# It implements the Mediator abstract interface

class World(Mediator):

    # Pool of size NxN
    
    # Rates contains the metabolic rates of the emulators
    
    # Replacement strategy determines what happens if the pool is full and a
    # new organism is to be born. Per default, the oldest organism in the pool is killed
    
    # Ages keeps track of the ages of the organisms in the corresponding location
    
    
    # Default copy mutation probability is 0.0100
    
    def __init__(self, N, replacement_strategy = "neighborhood", cm_prob = 0.25, ins_prob = 0.1, del_prob = 0.1):

        # Pool() will contain the set of CPUEmulators.
        self.pool = Pool(N, dtype = DO.CPUEmulator)
        
        self.rates = np.zeros((N,N), dtype = int)
        
        self.ages = np.zeros((N,N), dtype = int)
        
        # Inputs is now an array of tuples of integers
        # The first integer is the most recent input
        # The second integer is the second most recent input
        # Initialize to 0. Assume that 0 means that there was no input yet
        # The probability of an input being exactly 0 is 2^-32
        
        self.inputs = np.zeros((N,N), dtype = (np.intc,2))
        
        self.replacement_strategy = replacement_strategy
        
        self.cm_prob = cm_prob
        
        self.ins_prob = ins_prob
        self.del_prob = del_prob

    # The following method instantiates a default self-replicating organism
    # as a random location in the pool, unless location specified otherwise
    # The location must be a valid tuple
    
    # Default as per Avida-ED website and Nature paper. Contains 35 nop-c in the middle
    # In total 50 instructions
    
    def place_default(self, position = None):
        #self.place_custom([16,20,  2, 0, 21, 2, 2, 2, 2, 11, 2, 2, 2, 2, 2, 2, 2, 2, 18, 2, 2, 2, 2, 18, 1, 2, 12, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 20, 19, 25, 2, 0, 17, 21, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],position = position)

        #self.place_custom([16, 20, 2, 0, 21] + [2]*36 + [20, 19, 25, 2, 0, 17, 21, 0, 1], position = position)
        #not
        self.place_custom([16, 20, 2, 0, 21, 2, 2, 2, 2, 2, 2, 2, 2, 7, 2, 5, 2, 7, 2, 1, 10, 2, 2, 18, 1, 19, 2, 2, 15, 2, 2, 2, 2, 2, 2, 2, 2, 2, 15, 2, 17, 18, 2, 20, 19, 25, 2, 0, 17, 21, 0, 1],position = position)
    # Default per avida paper, with only 15 instructions
    def place_default_15(self, position = None):
        
        #self.place_custom([16, 20, 2, 0, 21, 2, 20, 19, 25, 2, 0, 17, 21, 0, 1], position = position)
        self.place_custom([16, 20, 2, 0, 21, 2, 2, 2, 2, 2, 2, 2, 2, 7, 2, 5, 2, 7, 2, 1, 10, 2, 2, 18, 1, 19, 2, 2, 15, 2, 2, 2, 2, 2, 2, 2, 2, 2, 15, 2, 17, 18, 2, 20, 19, 25, 2, 0, 17, 21, 0, 1],position = position)

    # Almost the same as the original default, only initialized with two IO operations
    # before the center nop-c cluster
    def place_def_io(self, position = None):
        """[16, 20, 2, 0, 1, 0, 8, 20, 1, 2, 16, 2, 19, 2, 10, 2, 24, 2, 4, 2, 14, 2, 11, 2, 11, 17, 8, 13, 13, 11, 1, 15,
         12, 0, 25, 24, 2, 2, 2, 9, 2, 18, 2, 3, 2, 3, 15, 19, 25, 2, 0, 17, 21, 0, 1, 16, 20, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0]"""
        self.place_custom([16, 20, 2, 0, 21, 2, 23, 2, 13, 13, 16, 2, 19, 2, 10, 1, 18, 2, 8, 9, 13, 5, 16, 15, 2, 18, 4, 2, 15, 4, 2, 24, 2, 2, 2, 11, 17, 8, 7, 13, 11, 2, 16, 12, 0, 18, 24,13, 18, 2, 18, 15, 2,23, 20, 19, 25, 2, 0, 17, 21, 0, 1],position = position)
        #self.place_custom([16, 20, 2, 0, 21, 2, 23, 2, 13, 13, 16, 2, 19, 2, 10, 1, 18, 2, 8, 9, 13, 5, 16, 15, 2, 18, 4, 2, 15, 4, 2, 24, 2, 2, 2, 11, 17, 8, 7, 13, 11, 2, 16, 12, 0, 18, 24, 2, 2, 2, 10, 2, 2, 2, 14, 2, 11, 15, 2, 1, 5, 18, 7, 13, 13, 2, 1, 3, 18, 21, 6, 2, 8, 7, 9, 20, 19, 25, 2, 0, 17, 11, 0, 1],position = position)
        #self.place_custom([16, 20, 2, 0, 21, 2, 23, 2, 13, 13, 16, 2, 19, 2, 10, 1, 18, 2, 8, 9, 13, 5, 16, 15, 2, 18, 4, 2, 15, 4, 2, 24, 2, 2, 2, 11, 17, 8, 7, 13, 11, 2, 16, 12, 0, 18, 24, 2, 2, 2, 15, 2, 2, 2, 14, 2, 3, 15, 2, 1, 5, 18, 7, 13, 18, 2, 1, 3, 18, 21, 6,2 ,8 ,7 ,9, 20, 19, 25, 2, 0, 17, 11, 0, 1, 21],position = position )
        #self.place_custom([16, 20, 2, 0, 21, 2, 23, 2, 2, 13, 16, 2, 19, 2, 10, 1, 18, 2, 18, 9, 13, 5, 16, 15, 2, 18, 2, 2, 15, 4, 2, 24, 2, 2, 2, 11, 17, 8, 7, 13, 11, 2, 1, 12, 0, 18, 24, 2, 2, 2, 2, 2, 2, 2, 18, 2, 3, 15 , 2, 1 ,5, 18, 7, 13, 20, 19, 25, 2, 0, 17, 21, 0, 1, 16, 20, 2, 0, 21, 2],position = position )
        #self.place_custom([16, 20, 2, 0, 21,2,  0, 8, 20, 1, 2, 16, 2, 19, 2, 10, 2, 24, 2, 4, 2, 14, 2, 11, 2, 11, 17, 8, 13, 13, 11, 1, 15, 12, 0, 25, 24, 2, 2, 2, 9, 2, 18, 2, 3, 2, 3, 15, 17,1,16, 18, 20, 19, 25, 2, 0, 17, 21, 0, 1],position=position)
        #self.place_custom([16, 2, 25, 2, 10, 2, 19, 15, 4, 2, 14, 2, 2, 2, 11, 17, 8, 7, 13, 4, 2, 1, 23, 0, 18, 24, 11, 2, 22, 2, 17, 12, 2, 18, 2, 3, 15, 19, 25, 2, 0, 17, 21, 0, 1, 14, 20, 0, 21, 2 ,23, 2 ,2 ,9], position = position)
        #self.place_custom([16,20,  2, 0, 21, 2, 2, 2, 2, 11, 2, 2, 2, 2, 2, 2, 2, 2, 18, 2, 2, 2, 2, 18, 1, 2, 12, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 20, 19, 25, 2, 0, 17, 21, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],position = position)
        #self.place_custom([16, 20, 2, 0, 21, 2, 0, 25, 20, 1, 18, 16, 2, 12, 2, 3, 22, 6, 3, 4, 9, 25, 2, 5, 18, 11, 17, 7, 13, 24, 11, 13, 4, 12, 0, 25, 13, 2, 19, 2, 9, 2, 18, 2, 17, 18, 15, 15, 17, 1, 16, 18, 20, 19, 25, 2, 0, 17, 21, 0, 1, 16,20, 19, 25, 2, 0, 17, 21, 0, 1] ,position = position)
        #self.place_custom([16, 20, 2, 0, 21] + [2]*18 +[2,11,13, 8, 7, 13,11,2,1,12,0]+ [18,1] + [2]*10 + [20, 19, 25, 2, 0, 17, 21, 0, 1], position = position)
        #self.place_custom([16, 20, 2, 0, 21, 2, 23, 2, 2, 2, 16, 2, 19, 2, 10,1,18,2,18,9,13,5,16,15,2,18, 2, 2, 15, 4, 2, 14, 2, 2, 2, 11, 17, 8, 7, 13, 11, 2, 1, 12, 0, 18, 24, 2, 2, 2, 2, 2, 2, 2, 18, 2, 3, 15, 19, 25, 2, 0, 17, 21, 0, 1],position = position)
        #self.place_custom([16, 20, 2, 0, 21, 2, 23, 2, 2, 13, 16, 2, 19, 2, 10, 1, 18, 2, 18, 9, 13, 5, 16, 15, 2, 18, 2, 2, 15, 4, 2, 24, 2, 2, 2, 11, 17, 8, 7, 13, 11, 2, 1, 12, 0, 18, 24, 2, 2, 2, 2, 2, 2, 2, 18, 2, 3, 15, 19, 25, 2, 0, 17, 21, 0, 1, 16, 20, 2, 0, 21, 2],position=position)
        #self.place_custom([16, 20, 2, 0, 21, 2, 2, 2,  18, 9, 24, 2, 2, 2, 18, 21, 20, 5, 10, 7, 2, 11, 10, 2, 25, 12, 3, 19, 1, 2, 15, 1, 2, 20, 3, 2, 7, 14, 17, 2, 18,1,2, 17, 18, 2, 2, 20, 19, 25, 2, 0, 17, 21, 0, 1],position = position)
        #self.place_custom([16, 20, 2, 0, 21, 2, 18, 2, 2, 2, 2, 2, 18, 7, 2, 5, 2, 7, 2, 1, 10, 2, 2, 18, 1, 19, 2, 2, 15, 2, 2, 2, 3, 2, 2, 2, 2, 2, 15, 2, 17, 18, 2, 2, 20, 19, 25, 2, 0, 17, 21, 0, 1],position = position)#, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],position = position)
        #self.place_custom([16, 20, 2, 0, 21, 2, 18, 2, 2, 2, 2, 2, 18, 2, 7, 2, 5, 2, 7, 2, 1, 10, 2, 2, 18, 1, 19, 2, 2, 15, 2, 2, 2, 2, 2, 2, 2, 2, 2, 15, 2, 17, 18, 2, 2, 20, 19, 25, 2, 0, 17, 21, 0, 1 ],position = position)
    # The following method instantiates a custom self-replicating organism
    # as a random location in the pool, unless location specified otherwise
    # The location must be a valid tuple
    
    # This function should always be used to place organisms in the pool
        
    def place_custom(self, program, position = None):
        
        # Create program
        default_program = DO.Program(program)
        logger2.critical(program)
        # Create a new emulator
        emulator = DO.CPUEmulator()
        
        # Load self as the emulator's mediator
        emulator.mediator = self
        
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
        
        self.rates[position] = emulator.instruction_memory.size()
        
        # Pull out the age of the organism
        
        self.ages[position] = emulator.age
        

    # Here the scheduler loop, which runs forever unless told otherwise
    
    def schedule(self, n_loops = None):
        
        if n_loops == None:
            
            # I want to see how the population is doing every 10k cycles
            
            iterator = 0
            
            while True:
                
                 baseline_rate = self.baseline_rate()
                 iterator += 1
                 
                 if iterator == 100:
                     # Shows that the whole thing is alive every 100 cycles
                     print("\nStill running")
                     # A sanity check, just making sure that the ages are behaving
                     # ok
                     print("AGES:")
                     print(self.ages)
                     iterator = 0
                     print("BASELINE RATE: " + str(self.baseline_rate()))
                     print("SHORTEST GENOME: " + str(self.shortest_genome()))
                     print("MAXIMAL RATE: " + str(self.max_rate()))
                     print("LONGEST GENOME: " + str(self.longest_genome()))
                     print("COPY MUTATION PROBABILITY: " + str(self.cm_prob))
            
                 for i in range(self.pool.shape[0]):
                     for j in range(self.pool.shape[1]):
                    
                         if isinstance(self.pool.get()[i][j], DO.CPUEmulator):
                        
                             n_cycles = round(self.rates[i][j] / baseline_rate)
                        
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
                            #TODO:
                            n_cycles = round(self.rates[i][j] / baseline_rate)
                        
                            for i_cycles in range(n_cycles):
                            
                                current_emulator = self.pool.get()[i][j]
                            
                                current_emulator.execute_instruction()
                            
                                self.ages[i][j] = current_emulator.age
            
            print(self.ages)


    # The following method defines which functions are to be called when world is notified 
    # of various events
    
    def notify(self, sender, event, result):
        
        if event == "division":
            
            self.react_on_division(sender, result)

        elif event == "IO_operation":

            self.react_on_IO(sender, result)
            

    # The methods below define how the world reacts to different notifications
    
    # Here how the world reacts upon organism division
    
    def react_on_division(self, sender, result):
        
        idx0 = np.where(self.pool.get() == sender)[0][0]
        idx1 = np.where(self.pool.get() == sender)[1][0]
        
        # The organism, upon valid division, notifies the world of it using
        # self.mediator.notify(sender = self, event = "division", result = result)

        # Create a program from the result passed from the organism which underwent division
        program = DO.Program(result)
        #logger4.debug('\n Father-organism : {} \n child-organism \n {}'.format(sender.memory, result))


        # Create a new emulator and load the resulting program in it
        emulator = DO.CPUEmulator()
        emulator.load_program(program)
        
        # Link self as the new emulator's mediator
        emulator.mediator = self
        
        # Set the copy mutation probability as defined in the world
        emulator.mutation_prob = self.cm_prob
        
        # Default replacement strategy
        # Look for free spots in the 1-hop neighborhood of the parent
        # If there is a free spot, put the offspring into any such spot
        # If not, kill the oldest organism in the neighborhood and put offspring there
        # Note that the oldest organism in the neighborhood may be the parent itself
        if self.replacement_strategy == "neighborhood":
            
            # Find the position in the pool where the sender (parent) is at:

            idx0 = np.where(self.pool.get() == sender)[0][0]
            idx1 = np.where(self.pool.get() == sender)[1][0]
            
            # Update the sender's rate according to its genome length
            
            width = self.pool.shape[0]
            height = self.pool.shape[1]
            
            # The neighborhood of the cell:
            # Iterate over rows max(idx0-1,0) idx0, min(idx0+1, pool height - 1)
            # Iterate over columns max(idx1-1,0), idx1, min(idx1 + 1, pool width - 1)
            
            # Breaking out of nested loops: 
            # https://stackoverflow.com/questions/653509/breaking-out-of-nested-loops
            
            position = None
            
            try:
                for i in range(max(idx0-1, 0), min(idx0+2, width)):
                    for j in range(max(idx1-1, 0), min(idx1+2, height)):  
                        if self.pool.get()[i][j] == 0:
                            position = (i,j)
                            raise BreakIt
                            
            except BreakIt:
                pass
            
            # If no free spot in the neighborhood was found, replace oldest cell in the neighborhood
            if position == None:
                
                oldest = 0
                
                for i in range(max(idx0-1, 0), min(idx0+2, width)):
                        for j in range(max(idx1-1, 0), min(idx1+2, height)):  
                            if self.ages[i][j] >= oldest:
                                    oldest = self.ages[i][j]
                                    position = (i,j)

        # Define kill_oldest replacement strategy as:
        # If there is a free spot in the pool, put child there
        # Otherwise, kill oldest organism in the pool and put child there
        
        elif self.replacement_strategy == "kill_oldest":
            
            # If there is a free spot put the cell there
            if 0 in self.pool.get():
            
                idx0 = np.where(self.pool.get() == 0)[0][0]
                idx1 = np.where(self.pool.get() == 0)[1][0]
            
                position = (idx0, idx1)
        
            else:
            
                position = self.oldest_position()               
            
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
                #logger.info('Not on input 1: ~{} = {}'.format(input_, result))
                #logger4.info("organism computed NOT : {} at {} \n".format(sender.memory, str((idx0, idx1))))
                #logger.info(sender.memory)
                # Notify us about what happened
                #"\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED NOT\nINPUT:  " + str(input_) + "\nOUTPUT: " + str(result))

                # Check whether the organism has computed not previously
                # If not, reward.
                if sender.fun_not == False:
                    sender.fun_not = True
                    sender.child_rate *= 2
                    
                    # Slow down with those mutations now
                    # It takes a while to slow down to stable 0.0100
                    if self.cm_prob > 0.002500:
                        self.cm_prob*= 0.99999999999999999
                
                # If yes, ignore
                else:
                    pass
        
        # If the two most recent inputs aren't none, check whether a function of the two most recent inputs was computed
        elif self.inputs[idx0][idx1][0] != 0 and self.inputs[idx0][idx1][1] != 0:
            
            # If a NOT was computed
            
            if result == ~self.inputs[idx0][idx1][0]:
                
                # Save input, result and the organism that computed it
                input_ = self.inputs[idx0][idx1]
                #logger.info('Not on input 2: ~{} = {}'.format(input_[1], result))
                #logger4.info("organism computed NOT : {} at {} \n {} \n".format(sender.memory, str((idx0, idx1)),self.baseline_rate()))
                #logger.info(sender.memory)
                # Notify us about what happened
                #print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED NOT\nINPUT:  " + str(input_[0]) + "\nOUTPUT: " + str(result))

                
                # Check whether the organism has computed not previously
                # If not, reward.
                if sender.fun_not == False:
                    sender.fun_not = True
                    sender.child_rate *= 2
                    
                    # Slow down with those mutations now
                    # It takes a while to slow down to stable 0.0100
                    if self.cm_prob > 0.025:
                        self.cm_prob*= 0.999999
                
                # If yes, ignore
                else:
                    pass
            
            # If a NAND was computed
            elif result == ~(self.inputs[idx0][idx1][0] & self.inputs[idx0][idx1][1]):
                
                # Save input, result and the organism that computed it
                input_ = self.inputs[idx0][idx1]
                #logger.info('NAND : ~({} & {}) = {}'.format(input_[0], input_[1], result))
                #logger4.info("organism computed NAND: {} at {} \n {} \n".format(sender.memory, str((idx0, idx1)), self.baseline_rate()))
                #logger.info(sender.memory)
                # Notify us about what happened
                #print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED NAND\nINPUT: " + str(input_) + "\nOUTPUT:  " + str(result))

                # Check whether the organism has computed nand previously
                # If not, reward.
                if sender.fun_nand == False:
                    sender.fun_nand = True
                    sender.child_rate *= 2
                    
                    # Slow down with those mutations now
                    # It takes a while to slow down to stable 0.002500
                    if self.cm_prob > 0.002500:
                        self.cm_prob*= 0.99
                
                # If yes, ignore
                else:
                    pass
                
            # If an AND was computed
            elif result == self.inputs[idx0][idx1][0] & self.inputs[idx0][idx1][1]:
                
                # Save input, result and the organism that computed it
                input_ = self.inputs[idx0][idx1]
                logger.info('AND : {} & {} = {}'.format(input_[0], input_[1], result))
                logger4.info("organism computed AND: {} at {} \n".format(sender.memory, str((idx0, idx1))))
                #logger.info(sender.memory)
                # Notify us about what happened
                #print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED AND\nINPUT: " + str(input_) + "\nOUTPUT:  " + str(result))

                # Check whether the organism has computed and previously
                # If not, reward.
                if sender.fun_and == False:
                    sender.fun_and = True
                    sender.child_rate *= 4
                    
                    # Slow down with those mutations now
                    # It takes a while to slow down to stable 0.002500
                    if self.cm_prob > 0.002500:
                        self.cm_prob*= 0.99
                
                # If yes, ignore
                else:
                    pass
                
            # If an OR_N was computed
            elif result == self.inputs[idx0][idx1][0] | ~self.inputs[idx0][idx1][1] or result == ~self.inputs[idx0][idx1][0] | self.inputs[idx0][idx1][1]:

                input_ = self.inputs[idx0][idx1]
                if (result == self.inputs[idx0][idx1][0] | ~self.inputs[idx0][idx1][1]):
                    logger.info('OR_N : {} | ~{} = {}'.format(input_[0], input_[1], result))
                    logger4.info('organism computed OR_n: {} at {} \n'.format(sender.memory, str((idx0, idx1))))
                    #logger.info(sender.memory)
                else:
                    logger.info('OR_N : ~{} | {} = {}'.format(input_[0], input_[1], result))
                    logger4.info('organism computed OR_N : {} at {} \n'.format(sender.memory, str((idx0, idx1))))
                    #logger.info(sender.memory)
                # Notify us about what happened
                #print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED OR_N\nINPUT: " + str(input_) + "\nOUTPUT:  " + str(result))
                
                
                # Check whether the organism has computed or_n previously
                # If not, reward.
                if sender.fun_or_n == False:
                    sender.fun_or_n = True
                    sender.child_rate *= 4
                    
                    # Slow down with those mutations now
                    # It takes a while to slow down to stable 0.002500
                    if self.cm_prob > 0.002500:
                        self.cm_prob*= 0.99
                
                # If yes, ignore
                else:
                    pass
                
            # If an OR was computed
            elif result == self.inputs[idx0][idx1][0] | self.inputs[idx0][idx1][1]:
                
                input_ = self.inputs[idx0][idx1]

                logger.info('OR : {} | {} = {}'.format(input_[0], input_[1], result))
                logger4.info("organism computed OR: {} at {} \n".format(sender.memory, str((idx0, idx1))))
                #logger.info(sender.memory)
                # Notify us about what happened
                #print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED OR\nINPUT: " + str(input_) + "\nOUTPUT:  " + str(result))

                # Check whether the organism has computed or previously
                # If not, reward.
                if sender.fun_or == False:
                    sender.fun_or = True
                    sender.child_rate *= 8

                    
                    # Slow down with those mutations now
                    # It takes a while to slow down to stable 0.002500
                    if self.cm_prob > 0.002500:
                        self.cm_prob*= 0.99
                
                # If yes, ignore
                else:
                    pass
                
            # If an AND_N was computed
            elif result == self.inputs[idx0][idx1][0] & ~self.inputs[idx0][idx1][1] or result == ~self.inputs[idx0][idx1][0] & self.inputs[idx0][idx1][1]:
                
                input_ = self.inputs[idx0][idx1]

                if result == self.inputs[idx0][idx1][0] & ~self.inputs[idx0][idx1][1]:
                    logger.info('AND_N : {} & ~{} = {}'.format(input_[0], input_[1], result))
                    logger4.info("organism computed AND_N: {} at {} \n {} \n".format(sender.memory, str((idx0, idx1)),self.max_rate()))
                    #logger.info(sender.memory)
                else:
                    logger.info('AND_N : ~{} & {} = {}'.format(input_[0], input_[1], result))
                    logger4.info("organism computed AND_N: {} at {} \n {} \n".format(sender.memory, str((idx0, idx1)), self.max_rate()))
                    #logger.info(sender.memory)
                # Notify us about what happened
                #print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED AND_N\nINPUT: " + str(input_) + "\nOUTPUT:  " + str(result))
                
                # Check whether the organism has computed and_n previously
                # If not, reward.
                if sender.fun_and_n == False:
                    sender.fun_and_n = True
                    sender.child_rate *= 8

                    # Slow down with those mutations now
                    # It takes a while to slow down to stable 0.002500
                    if self.cm_prob > 0.002500:
                        self.cm_prob*= 0.99
                
                # If yes, ignore
                else:
                    pass
                
            # If a NOR was computed
            elif result == ~(self.inputs[idx0][idx1][0] | self.inputs[idx0][idx1][1]):
                
                input_ = self.inputs[idx0][idx1]

                logger.info('NOR : ~{} & ~{} = {}'.format(input_[0], input_[1], result))
                logger4.info("organism computed NOR: {} at {} \n".format(sender.memory, str((idx0, idx1))))
                #logger.info(sender.memory)
                # Notify us about what happened
                #print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED NOR\nINPUT: " + str(input_) + "\nOUTPUT:  " + str(result))

                # Check whether the organism has computed nand previously
                # If not, reward.
                if sender.fun_nor == False:
                    sender.fun_nor = True
                    sender.child_rate *= 16
                    
                    # Slow down with those mutations now
                    # It takes a while to slow down to stable 0.002500
                    if self.cm_prob > 0.002500:
                        self.cm_prob*= 0.99
                
                # If yes, ignore
                else:
                    pass
                
            # If an XOR was computed:
            elif result == self.inputs[idx0][idx1][0] ^ self.inputs[idx0][idx1][1]:
                
                # Save input, result and the organism that computed it
                input_ = self.inputs[idx0][idx1]
                logger.info('XOR : {} & ~{} or ~{} & {} = {}'.format(input_[0], input_[1], (input_[0]), input_[1], result))
                logger4.info("organism computed XOR: {} at {} \n".format(sender.memory, str((idx0, idx1))))
                #logger.info(sender.memory)
                # Notify us about what happened
                #print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED XOR\nINPUT: " + str(input_) + "\nOUTPUT: " + str(result))
                
                # Check whether the organism has computed xor previously
                # If not, reward.
                if sender.fun_xor == False:
                    sender.fun_xor = True
                    sender.child_rate *= 16
                    
                    # Slow down with those mutations now
                    # It takes a while to slow down to stable 0.002500
                    if self.cm_prob > 0.002500:
                        self.cm_prob*= 0.99
                
                # If yes, ignore
                else:
                    pass
                
            # If EQU was computed:
            elif result == equ(self.inputs[idx0][idx1][0], self.inputs[idx0][idx1][1]):
                
                # Save input, result and the organism that computed it
                input_ = self.inputs[idx0][idx1]
                logger.critical('EQU : {} & {} or ~{} & ~{} = {}'.format(input_[0], input_[1], input_[0], input_[1], result))
                logger4.info("organism computed EQU: {} at {} \n".format(sender.memory, str((idx0,idx1))))
                logger2.critical(sender.memory)
                # Notify us about what happened
                #print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED EQU\nINPUT: " + str(input_) + "\nOUTPUT: " + str(result))
                
                # Check whether the organism has computed xor previously
                # If not, reward.
                if sender.fun_equ == False:
                    sender.fun_equ = True
                    sender.child_rate *= 32
                    
                    # Slow down with those mutations now
                    # It takes a while to slow down to stable 0.002500
                    if self.cm_prob > 0.002500:
                        self.cm_prob*= 0.99
                
                # If yes, ignore
                else:
                    pass
            
            
            """
            # If EQU was computed:
            # NOTE: I only want to reward the organisms
            elif result == (self.inputs[idx0][idx1][0] == self.inputs[idx0][idx1][1]) and result == 1:
                
                # Save input, result and the organism that computed it
                input = self.inputs[idx0][idx1]
                
                # Notify us about what happened
                print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED EQU\nINPUT: " + str(input) + "\nOUTPUT: " + str(result))
                
                # Slow down with those mutations now
                self.cm_prob = 0.005
                
                # Check whether the organism has computed equ previously
                # If not, reward.
                if sender.fun_equ == False:
                    sender.fun_equ = True
                    sender.child_rate *= 32
                
                # If yes, ignore
                else:
                    pass
                
            """
     
        # A random 32-bit number
        to_input = np.random.randint(low = -2147483648, high = 2147483648, dtype = np.intc)
        
        # Put the randomly generated number into the input buffer of the emulator
        sender.cpu.input_buffer.put(to_input)
        
        # Update inputs array
        # Old newest input gets placed into position 1
        # New input gets placed into position 0
        self.inputs[idx0][idx1][1] = self.inputs[idx0][idx1][0]
        self.inputs[idx0][idx1][0] = to_input

    # Helper methods here:
        
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
    
# Returns EQU of two numbers
def equ(a,b):
    return (a & b) | (~a & ~b)
#%% Testing some stuff


# First argument is world size
# cm_prob is copy mutation probability
# ins_prob and del_prob are insertion and deletion probabilities
world = World(60,replacement_strategy="neighborhood",cm_prob = 0.05, ins_prob = 0.01, del_prob = 0.01)

# Filling the world with the default organisms instantiated with two IOs
world.fill()

print("World full")

#%%
world.schedule()