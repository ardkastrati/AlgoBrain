# A clean implementation of the Avida World simulator

# %%
# Necessary imports:
#TODO:  line 308
import numpy as np
import DigitalOrganism as DO
from Mediator import Mediator
import logging
import multiprocessing
logger = logging.getLogger( __name__ )
logger2 = logging.getLogger(__name__)
logger3 = logging.getLogger(__name__)
logger4 = logging.getLogger(__name__)
formatter_1 = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
formatter_2 = logging.Formatter('%(asctime)s:%(message)s')
formatter_3 = logging.Formatter('%(relativeCreated)d')
formatter_4 = logging.Formatter('%(message)s')
logger.setLevel(logging.INFO)
#file_handler = logging.FileHandler('Function7.log')
#file_handler.setFormatter(formatter_1)#,formatter_2,formatter_3
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter_2)
stream_handler_program = logging.StreamHandler()
stream_handler_program.setFormatter(formatter_4)
#file_handler_2 = logging.FileHandler('Function_7.log')
file_handler_3 = logging.FileHandler('Organism_log3.log')
file_handler_3.setFormatter(formatter_4)
#file_handler_2.setFormatter(formatter_3)
logger.addHandler(stream_handler)
#logger.addHandler(file_handler)
#logger.addHandler(stream_handler_program)
#logger2.addHandler(file_handler_2)
#logger3.addHandler(stream_handler_program)
#logger2.setLevel(logging.INFO)
#logger3.setLevel(logging.INFO)
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
        #self.place_custom([16, 20, 2, 0, 21] + [2] * 60 + [18,1,13,11,15,18,2,1,3,18,0]+[2]*15+ [20, 19, 25, 2, 0, 17, 21, 0, 1], position=position)
        #self.place_custom([0,0,24,2,6,18,24,5,13,7,3,24,15,8,2,0,0,18,15,3,11,13,10,18,25,24,12,11,15,14,13,16,18,7,8,13,20,2,0,12,21,2,23,2,10,23,18,15,8,15,25,22,15,15,12,4,6,11,1,0,15,12,4,25,18,15,1,9,0,14,5,15,18,2,7,3,15,5,2,7,2,18,2,4,7,17,16,7,15,2,2,25,17,24,6,3,17,19,7,18,2,2,2,24,15,2,25,25,1,7,24,2,0,19,15,2,6,15,24,18,2,12,14,16,11,24,18,5,20,19,24,2,0,17,21,0,1], position = position)

        #THIS = GODPROGRAM
        #self.place_custom([16, 20, 2, 0, 21, 2, 3, 16, 23, 12, 2, 1, 11, 13, 3, 2, 20, 12, 19, 5, 7, 5, 12, 0, 6, 18, 3, 19, 25, 4, 2, 8, 6, 2, 17, 14, 7, 3, 14, 5, 4, 12, 24, 16, 17, 15, 7, 5, 18, 2, 6, 15, 2, 3, 25, 16, 4, 19, 15, 1, 7, 7, 8, 5, 25, 2, 24, 18, 18, 2, 15, 18, 8, 2, 15, 2, 6, 5, 13, 11, 15, 18, 23, 20, 19, 16, 19, 25, 2, 0, 17, 21, 0, 1],position= position)

        #self.place_custom([16, 2, 25, 2, 10, 2, 19, 15, 4, 2, 14, 2, 2, 2, 11, 17, 8, 7, 13, 4, 2, 1, 23, 0, 18, 24, 11, 2, 22, 2, 17, 12, 2, 18, 2, 3, 15, 19, 25, 2, 0, 17, 21, 0, 1, 14, 20, 0, 21, 2 ,23, 2 ,2 ,9], position = position)

        #self.place_custom([16, 20, 2, 0, 21] +[2]+[18,1]+ [2]*25 +  [2]+[18,2,4,1,11,13,18,1,8,0]+[20, 19, 25, 2, 0, 17, 21, 0, 1], position = position)
        #not
        #self.place_custom([16, 20, 2, 0, 21, 2, 3, 16, 23, 12, 2, 1, 11, 13, 3, 2, 20, 12, 19, 5, 7, 5, 12, 0, 6, 18, 3, 19, 25, 4, 2, 8, 6, 2, 17, 14, 7, 3, 14, 5, 4, 12, 24, 16, 17, 15, 7, 5, 18, 2, 6, 15, 2, 3, 25, 16, 4, 19, 15, 1, 7, 7, 8, 5, 25, 2, 24, 18, 18, 2, 15, 18, 8, 2, 15, 2, 6, 5, 13, 11, 15, 18, 23, 20, 19, 16, 19, 25, 2, 0, 17, 21, 0, 1],position= position)

        #self.place_custom([0, 0, 0, 12, 25, 16, 20, 2, 0, 21, 2, 8, 3, 12, 11, 2, 2, 6, 15, 7, 12, 12, 9, 8, 8, 12, 15, 25, 6, 19, 3, 18, 3, 25, 18, 12, 2, 6, 2, 14, 3, 8, 2, 16, 14, 2, 14, 12, 24, 2, 15, 7, 5, 18, 2, 6, 15, 2, 25, 1, 18, 2, 19, 7, 15, 7, 25, 25, 2, 6, 7, 18, 4, 16, 3, 18, 2, 15, 18, 1, 5, 15, 2, 16, 6, 15, 18, 11, 5, 16, 5, 5, 23, 20, 19, 25, 2, 0, 17, 21, 0, 1],position = position)
        #self.place_custom([24, 16, 20, 2, 0, 21, 2, 1, 3, 12, 5, 19, 10, 10, 17, 20, 18, 0, 5, 6, 1, 16, 3, 2, 9, 2, 6, 4, 18, 19, 14, 1, 23, 20, 5, 15, 18, 2, 25, 14, 2, 19, 3, 2, 5, 0, 18, 15, 7, 18, 15, 15, 13, 2, 4, 8, 2, 7, 18, 11, 2, 18, 17, 5, 2, 16, 6, 19, 15, 18, 4, 6, 2, 1, 14, 18, 15, 3, 3, 3, 18, 1, 17, 16, 16, 14, 16, 8, 13, 25, 20, 19, 25, 2, 0, 17, 21, 23, 0, 1],position = position)
        #self.place_custom([16, 20, 2, 0, 21] + [2]*18 + [18,1] + [11,2]+ [24,2]+ [2]*70+[20, 19, 25, 2, 0, 17, 21, 0, 1], position = position)
        #3self.place_custom([24, 16, 20, 2, 0, 21, 2, 1, 3, 12, 5, 19, 10, 10, 17, 20, 18, 0, 5, 6, 1, 16, 3, 2, 9, 2, 6, 4, 18, 19, 14, 1, 23, 20, 5, 15, 18, 2, 25, 14, 2, 19, 3, 2, 5, 0, 18, 15, 7, 18, 15, 15, 13, 2, 4, 8, 2, 7, 18, 11, 2, 18, 17, 5, 2, 16, 6, 19, 15, 18, 4, 6, 2, 1, 14, 18, 15, 3, 3, 3, 18, 1, 17, 16, 16, 14, 16, 8, 13, 25, 20, 19, 25, 2, 0, 17, 21, 23, 0, 1, 24, 16, 20, 2, 0, 21, 0, 1],position=position)
        #self.place_custom([10, 16, 20, 2, 0, 21, 2, 1, 9, 8, 9, 19, 3, 11, 20, 20, 6, 17, 11, 17, 2, 2, 13, 3, 12, 11, 5, 17, 19, 20, 1, 8, 17, 5, 20, 7, 15, 18, 2, 3, 16, 19, 3, 5, 0, 18, 15, 11, 18, 15, 15, 13, 2, 3, 7, 1, 16, 7, 18, 11, 2, 14, 5, 2, 6, 19, 15, 18, 6, 13, 25, 16, 11, 18, 15, 17, 8, 2, 18, 18, 4, 8, 16, 14, 1, 17, 13, 25, 20, 19, 25, 2, 0, 17, 21, 0, 1],position =position)
        #self.place_custom([10, 16, 20, 2, 0, 21, 2, 1, 9, 8, 9, 19, 3, 11, 20, 20, 6, 17, 11, 17, 2, 2, 13, 3, 12, 11, 5, 17, 19, 20, 1, 8, 17, 5, 20, 7, 15, 18, 2, 3, 16, 19, 3, 5, 0, 18, 15, 11, 18, 15, 15, 13, 2, 3, 7, 1, 16, 7, 18, 11, 2, 14, 5, 2, 6, 19, 15, 18, 6, 13, 25, 16, 11, 18, 15, 17, 8, 2, 18, 18, 4, 8, 16, 14, 1, 17, 13, 25, 20, 19, 25, 2, 0, 17, 21, 0, 1],position =position)
        #self.place_custom([16, 20, 2, 0, 21, 2, 23, 2, 13, 13, 16, 2, 19, 2, 10, 1, 18, 2, 8, 9, 13, 5, 16, 15, 2, 18, 4, 2, 15, 4, 2, 24, 2, 2, 2, 11, 17, 8, 7, 13, 11, 2, 16, 12, 0, 18, 24,13, 18, 2, 18, 15, 2,23, 20, 19, 25, 2, 0, 17, 21, 0, 1],position = position)
        #self.place_custom([16, 20, 2, 0, 21, 2, 23, 2, 13, 13, 16, 2, 19, 2, 10, 1, 18, 2, 8, 9, 13, 5, 16, 15, 2, 18, 4, 2, 15, 4, 2, 24, 2, 2, 2, 11, 17, 8, 7, 13, 11, 2, 16, 12, 0, 18, 24,13, 18, 2, 18, 15, 2,23, 20, 19, 25, 2, 0, 17, 21, 0, 1],position = position)
        self.place_custom([16, 20, 2, 0, 21, 2, 3, 16, 23, 12, 2, 1, 11, 13, 3, 2, 20, 12, 19, 5, 7, 5, 12, 0, 6, 18, 3, 19, 25, 4, 2, 8, 6, 2, 17, 14, 7, 3, 14, 5, 4, 12, 24, 16, 17, 15, 7, 5, 18, 2, 6, 15, 2, 3, 25, 16, 4, 19, 15, 1, 7, 7, 8, 5, 25, 2, 24, 18, 18, 2, 15, 18, 8, 2, 15, 2, 6, 5, 13, 11, 15, 18, 23, 20, 19, 16, 19, 25, 2, 0, 17, 21, 0, 1],position= position)

        #elf.place_custom([16, 20, 2, 0, 21, 2, 2, 2, 2, 2, 2, 2, 2, 7, 2, 5, 2, 7, 2, 1, 10, 2, 2, 18, 1, 19, 2, 2, 15, 2, 2, 2, 2, 2, 2, 2, 2, 2, 15, 2, 17, 18, 2, 20, 19, 25, 2, 0, 17, 21, 0, 1],position = position)
    # Default per avida paper, with only 15 instructions
    def place_zero(self,position = None):
        self.place_custom([0],position = position)
    def place_default_15(self, position = None):
        self.place_custom([16, 20, 2, 0, 21] + [2] * 50 + [20, 19, 25, 2, 0, 17, 21, 0, 1], position=position)
        #self.place_custom([16, 20, 2, 0, 21, 2, 20, 19, 25, 2, 0, 17, 21, 0, 1], position = position)
        #self.place_custom([16, 20, 2, 0, 21, 2, 2, 2, 2, 2, 2, 2, 2, 7, 2, 5, 2, 7, 2, 1, 10, 2, 2, 18, 1, 19, 2, 2, 15, 2, 2, 2, 2, 2, 2, 2, 2, 2, 15, 2, 17, 18, 2, 20, 19, 25, 2, 0, 17, 21, 0, 1],position = position)
        #self.place_custom([13, 24, 16, 20, 2, 0, 21, 2, 0, 25, 5, 21, 2, 19, 19, 2, 20, 24, 19, 24, 24, 4, 1, 9, 3, 24, 7, 19, 3, 19, 7, 14, 7, 8, 20, 17, 7, 15, 18, 2, 8, 7, 4, 19, 16, 17, 5, 0, 18, 15, 17, 18, 15, 15, 13, 2, 4, 7, 4, 16, 7, 18, 11, 2, 18, 16, 5, 2, 6, 19, 15, 18, 1, 17, 6, 13, 25, 7, 16, 11, 18, 13, 7, 9, 18, 17, 7, 2, 1, 14, 1, 3, 13, 25, 20, 19, 25, 2, 0, 17, 21, 0, 1],position=position)
        #self.place_custom([5, 16, 18, 20, 2, 0, 21, 2, 2, 23, 23, 14, 11, 11, 19, 3, 16, 11, 6, 6, 11, 25, 7, 10, 7, 23, 9, 23, 2, 16, 23, 24, 15, 17, 19, 20, 8, 15, 18, 2, 25, 14, 2, 19, 19, 8, 5, 0, 18, 15, 17, 18, 15, 15, 13, 2, 16, 7, 16, 7, 18, 11, 2, 18, 14, 5, 2, 17, 6, 25, 19, 15, 18, 6, 13, 25, 8, 11, 18, 8, 15, 7, 4, 3, 18, 8, 8, 3, 1, 0, 14, 1, 25, 14, 13, 25, 20, 19, 25, 2, 0, 17, 21, 0, 1],position = position)
    # Almost the same as the original default, only initialized with two IO operations
    # before the center nop-c cluster
    def place_def_io(self, position = None):
        """[16, 20, 2, 0, 1, 0, 8, 20, 1, 2, 16, 2, 19, 2, 10, 2, 24, 2, 4, 2, 14, 2, 11, 2, 11, 17, 8, 13, 13, 11, 1, 15,
         12, 0, 25, 24, 2, 2, 2, 9, 2, 18, 2, 3, 2, 3, 15, 19, 25, 2, 0, 17, 21, 0, 1, 16, 20, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0]"""
        #self.place_custom([5, 16, 20, 2, 0, 21, 2, 2, 8, 17, 25, 7, 19, 17, 4, 6, 2, 17, 18, 17, 19, 9, 7, 5, 0, 19, 1, 7, 25, 5, 20, 15, 18, 2, 25, 16, 19, 5, 0, 18, 15, 17, 18, 15, 15, 13, 2, 2, 7, 1, 7, 18, 11, 2, 5, 2, 6, 19, 15, 18, 6, 13, 16, 16, 11, 18, 3, 6, 3, 3, 18, 18, 4, 14, 17, 13, 25, 20, 19, 25, 2, 0, 17, 21, 4, 0, 1],position = position)
        #self.place_custom([13, 24, 16, 20, 2, 0, 21, 2, 0, 25, 5, 21, 2, 19, 19, 2, 20, 24, 19, 24, 24, 4, 1, 9, 3, 24, 7, 19, 3, 19, 7, 14, 7, 8, 20, 17, 7, 15, 18, 2, 8, 7, 4, 19, 16, 17, 5, 0, 18, 15, 17, 18, 15, 15, 13, 2, 4, 7, 4, 16, 7, 18, 11, 2, 18, 16, 5, 2, 6, 19, 15, 18, 1, 17, 6, 13, 25, 7, 16, 11, 18, 13, 7, 9, 18, 17, 7, 2, 1, 14, 1, 3, 13, 25, 20, 19, 25, 2, 0, 17, 21, 0, 1],position=position)
        #self.place_custom([10, 16, 20, 2, 0, 21, 2, 1, 9, 8, 9, 19, 3, 11, 20, 20, 6, 17, 11, 17, 2, 2, 13, 3, 12, 11, 5, 17, 19, 20, 1, 8, 17, 5, 20, 7, 15, 18, 2, 3, 16, 19, 3, 5, 0, 18, 15, 11, 18, 15, 15, 13, 2, 3, 7, 1, 16, 7, 18, 11, 2, 14, 5, 2, 6, 19, 15, 18, 6, 13, 25, 16, 11, 18, 15, 17, 8, 2, 18, 18, 4, 8, 16, 14, 1, 17, 13, 25, 20, 19, 25, 2, 0, 17, 21, 0, 1],position =position)
        #self.place_custom([16, 20, 2, 0, 21, 2, 23, 2, 13, 13, 16, 2, 19, 2, 10, 1, 18, 2, 8, 9, 13, 5, 16, 15, 2, 18, 4, 2, 15, 4, 2, 24, 2, 2, 2, 11, 17, 8, 7, 13, 11, 2, 16, 12, 0, 18, 24,13, 18, 2, 18, 15, 2,23, 20, 19, 25, 2, 0, 17, 21, 0, 1],position = position)
        #self.place_custom([16, 20, 2, 0, 21, 2, 23, 2, 13, 13, 16, 2, 19, 2, 10, 1, 18, 2, 8, 9, 13, 5, 16, 15, 2, 18, 4, 2, 15, 4, 2, 24, 2, 2, 2, 11, 17, 8, 7, 13, 11, 2, 16, 12, 0, 18, 24, 2, 2, 2, 10, 2, 2, 2, 14, 2, 11, 15, 2, 1, 5, 18, 7, 13, 13, 2, 1, 3, 18, 21, 6, 2, 8, 7, 9, 20, 19, 25, 2, 0, 17, 11, 0, 1],position = position)
        #self.place_custom([16, 20, 2, 0, 21, 2, 23, 2, 13, 13, 16, 2, 19, 2, 10, 1, 18, 2, 8, 9, 13, 5, 16, 15, 2, 18, 4, 2, 15, 4, 2, 24, 2, 2, 2, 11, 17, 8, 7, 13, 11, 2, 16, 12, 0, 18, 24, 2, 2, 2, 15, 2, 2, 2, 14, 2, 3, 15, 2, 1, 5, 18, 7, 13, 18, 2, 1, 3, 18, 21, 6,2 ,8 ,7 ,9, 20, 19, 25, 2, 0, 17, 11, 0, 1, 21],position = position )
        #self.place_custom([16, 20, 2, 0, 21, 2, 23, 2, 2, 13, 16, 2, 19, 2, 10, 1, 18, 2, 18, 9, 13, 5, 16, 15, 2, 18, 2, 2, 15, 4, 2, 24, 2, 2, 2, 11, 17, 8, 7, 13, 11, 2, 1, 12, 0, 18, 24, 2, 2, 2, 2, 2, 2, 2, 18, 2, 3, 15 , 2, 1 ,5, 18, 7, 13, 20, 19, 25, 2, 0, 17, 21, 0, 1, 16, 20, 2, 0, 21, 2],position = position )
        #self.place_custom([16, 20, 2, 0, 21,2,  0, 8, 20, 1, 2, 16, 2, 19, 2, 10, 2, 24, 2, 4, 2, 14, 2, 11, 2, 11, 17, 8, 13, 13, 11, 1, 15, 12, 0, 25, 24, 2, 2, 2, 9, 2, 18, 2, 3, 2, 3, 15, 17,1,16, 18, 20, 19, 25, 2, 0, 17, 21, 0, 1],position=position)
        #self.place_custom([16, 2, 25, 2, 10, 2, 19, 15, 4, 2, 14, 2, 2, 2, 11, 17, 8, 7, 13, 4, 2, 1, 23, 0, 18, 24, 11, 2, 22, 2, 17, 12, 2, 18, 2, 3, 15, 19, 25, 2, 0, 17, 21, 0, 1, 14, 20, 0, 21, 2 ,23, 2 ,2 ,9], position = position)
        #self.place_custom([16,20,  2, 0, 21, 2, 2, 2, 2, 11, 2, 2, 2, 2, 2, 2, 2, 2, 18, 2, 2, 2, 2, 18, 1, 2, 12, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 20, 19, 25, 2, 0, 17, 21, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],position = position)
        #self.place_custom([16, 20, 2, 0, 21, 2, 0, 25, 20, 1, 18, 16, 2, 12, 2, 3, 22, 6, 3, 4, 9, 25, 2, 5, 18, 11, 17, 7, 13, 24, 11, 13, 4, 12, 0, 25, 13, 2, 19, 2, 9, 2, 18, 2, 17, 18, 15, 15, 17, 1, 16, 18, 20, 19, 25, 2, 0, 17, 21, 0, 1, 16,20, 19, 25, 2, 0, 17, 21, 0, 1] ,position = position)
        #good for nothing
        #self.place_custom([5, 16, 18, 20, 2, 0, 21, 2, 2, 23, 23, 14, 11, 11, 19, 3, 16, 11, 6, 6, 11, 25, 7, 10, 7, 23, 9, 23, 2, 16, 23, 24, 15, 17, 19, 20, 8, 15, 18, 2, 25, 14, 2, 19, 19, 8, 5, 0, 18, 15, 17, 18, 15, 15, 13, 2, 16, 7, 16, 7, 18, 11, 2, 18, 14, 5, 2, 17, 6, 25, 19, 15, 18, 6, 13, 25, 8, 11, 18, 8, 15, 7, 4, 3, 18, 8, 8, 3, 1, 0, 14, 1, 25, 14, 13, 25, 20, 19, 25, 2, 0, 17, 21, 0, 1],position=position)
        #able to calculate xor
        self.place_custom(160 * [0], position=position)
        #self.place_custom([16, 20, 2, 0, 21] + [1] * 120 + [20, 19, 25, 2, 0, 17, 21, 0, 1], position=position)
        #self.place_custom([16, 20, 2, 0, 21, 2, 3, 16, 12, 12, 1, 23, 6, 19, 2, 24, 25, 20, 5, 7, 25, 6, 17, 24, 1, 4, 11, 18, 6, 18, 7, 5, 4, 12, 24, 16, 17, 15, 7, 5, 16, 18, 2, 6, 15, 2, 3, 25, 4, 3, 2, 15, 3, 7, 19, 8, 5, 25, 2, 7, 18, 18, 2, 15, 1, 18, 8, 2, 15, 2, 6, 5, 13, 11, 15, 18, 3, 20, 0, 5, 20, 19, 25, 2, 0, 17, 21, 0, 1],position = position)
        #this should be the godprogramm according to avida

        #self.place_custom([16, 20, 2, 0, 21, 2, 3, 16, 23, 12, 2, 1, 11, 13, 3, 2, 20, 12, 19, 5, 7, 5, 12, 0, 6, 18, 3, 19, 25, 4, 2, 8, 6, 2, 17, 14, 7, 3, 14, 5, 4, 12, 24, 16, 17, 15, 7, 5, 18, 2, 6, 15, 2, 3, 25, 16, 4, 19, 15, 1, 7, 7, 8, 5, 25, 2, 24, 18, 18, 2, 15, 18, 8, 2, 15, 2, 6, 5, 13, 11, 15, 18, 23, 20, 19, 16, 19, 25, 2, 0, 17, 21, 0, 1],position= position)
        #self.place_custom([24, 16, 20, 2, 0, 21, 2, 1, 3, 12, 5, 19, 10, 10, 17, 20, 18, 0, 5, 6, 1, 16, 3, 2, 9, 2, 6, 4, 18, 19, 14, 1, 23, 20, 5, 15, 18, 2, 25, 14, 2, 19, 3, 2, 5, 0, 18, 15, 7, 18, 15, 15, 13, 2, 4, 8, 2, 7, 18, 11, 2, 18, 17, 5, 2, 16, 6, 19, 15, 18, 4, 6, 2, 1, 14, 18, 15, 3, 3, 3, 18, 1, 17, 16, 16, 14, 16, 8, 13, 25, 20, 19, 25, 2, 0, 17, 21, 23, 0, 1],position=position)
        #self.place_custom([7, 16, 20, 2, 0, 21, 2, 0, 3, 9, 16, 5, 19, 10, 10, 9, 20, 18, 0, 20, 12, 1, 15, 3, 2, 9, 20, 10, 6, 19, 10, 5, 23, 20, 5, 15, 18, 2, 25, 14, 2, 19, 3, 0, 5, 0, 18, 15, 3, 18, 15, 15, 13, 2, 2, 4, 8, 16, 7, 18, 11, 2, 18, 13, 5, 2, 16, 6, 19, 15, 18, 4, 6, 2, 16, 18, 15, 3, 3, 18, 1, 17, 0, 14, 16, 8, 13, 25, 20, 19, 25, 2, 0, 17, 21, 23, 0, 1],position=position)
        #self.place_custom([16, 20, 2, 0, 21] + [2]*18 + [18,1] + [2]*18 + [20, 19, 25, 2, 0, 17, 21, 0, 1], position = position)
        #self.place_custom([16, 18, 5, 12, 14, 18, 24, 15, 4, 0, 5, 0, 25, 15, 0, 4, 11, 13, 18, 17, 15, 3, 25, 2, 9, 15, 15, 18, 3, 23, 7, 24, 7, 20, 2, 0, 5, 21, 2, 11, 9, 10, 16, 20, 20, 9, 25, 11, 20, 20, 5, 10, 11, 10, 8, 15, 20, 19, 10, 12, 11, 25, 24, 4, 10, 4, 7, 6, 16, 12, 18, 2, 7, 6, 14, 25, 25, 17, 7, 3, 23, 18, 2, 4, 7, 16, 15, 2, 0, 19, 0, 25, 0, 15, 24, 7, 8, 18, 2, 15, 2, 4, 14, 19, 8, 15, 25, 6, 15, 2, 1, 15, 18, 2, 1, 12, 14, 16, 11, 18, 6, 3, 20, 19, 25, 2, 0, 24, 21, 0, 1],position = position)
        #organism that can compute not,nand,or_not,or,and_not,nor
        #self.place_custom([0,0,24,2,6,18,24,5,13,7,3,24,15,8,2,0,0,18,15,3,11,13,10,18,25,24,12,11,15,14,13,16,18,7,8,13,20,2,0,12,21,2,23,2,10,23,18,15,8,15,25,22,15,15,12,4,6,11,1,0,15,12,4,25,18,15,1,9,0,14,5,15,18,2,7,3,15,5,2,7,2,18,2,4,7,17,16,7,15,2,2,25,17,24,6,3,17,19,7,18,2,2,2,24,15,2,25,25,1,7,24,2,0,19,15,2,6,15,24,18,2,12,14,16,11,24,18,5,20,19,24,2,0,17,21,0,1], position = position)
        #self.place_custom([16, 18, 5, 12, 14, 18, 24, 15, 4, 0, 5, 0, 25, 15, 0, 4, 11, 13, 18, 17, 15, 3, 25, 2, 9, 15, 15, 18, 3, 23, 7, 24, 7, 20, 2, 0, 5, 21, 2, 11, 9, 10, 16, 20, 20, 9, 25, 11, 20, 20, 5, 10, 11, 10, 8, 15, 20, 19, 10, 12, 11, 25, 24, 4, 10, 4, 7, 6, 16, 12, 18, 2, 7, 6, 14, 25, 25, 17, 7, 3, 23, 18, 2, 4, 7, 16, 15, 2, 0, 19, 0, 25, 0, 15, 24, 7, 8, 18, 2, 15, 2, 4, 14, 19, 8, 15, 25, 6, 15, 2, 1, 15, 18, 2, 1, 12, 14, 16, 11, 18, 6, 3, 20, 19, 25, 2, 0, 24, 21, 0, 1],position=position)
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
        
        #self.rates[position] = emulator.instruction_memory.size()
        self.rates[position] = 1#len(program)
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
                 
                 if iterator == 500:
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
                     #for i in range(0,self.pool.get().shape[0]):
                     #    for j in range(0,self.pool.get().shape[1]):
                     #        print(self.rates[i][j])
                     #print(self.rates)
                 for i in range(self.pool.shape[0]):
                     for j in range(self.pool.shape[1]):
                    
                         if isinstance(self.pool.get()[i][j], DO.CPUEmulator):
                        # TODO: rememember the change from round to int here
                             n_cycles = int(self.rates[i][j] / baseline_rate)
                        
                             for i_cycles in range(n_cycles):
                            
                                current_emulator = self.pool.get()[i][j]
                                if(self.pool.get()[i][j]!=0):
                                    current_emulator.execute_instruction()
                            
                                    self.ages[i][j] = current_emulator.age
                                else:
                                    pass
        else:
                                
            for i_loops in range(n_loops):
            
                baseline_rate = self.baseline_rate()
            
                for i in range(self.pool.shape[0]):
                    for j in range(self.pool.shape[1]):
                    
                        if isinstance(self.pool.get()[i][j], DO.CPUEmulator):
                            #TODO:
                            n_cycles = int(self.rates[i][j] / baseline_rate)
                        
                            for i_cycles in range(n_cycles):
                                #TODO:  Make this better!
                                if(self.ages[i][j]>(self.rates[i][j]/self.baseline_rate()*len(self.get((i,j)).memory))):
                                    print("Dogshit_organism killed")
                                    self.react_on_death(self.get((i,j)))
                                else:
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
            
        elif event == "death":
            self.react_on_death(sender)
    # The methods below define how the world reacts to different notifications
    
    # Here how the world reacts upon organism division

    def react_on_death(self, sender):
        #p = multiprocessing.Process(target=World.schedule(self))
        #p.terminate()
        sender.clear

        # Find the position in the pool where the sender is at:
        idx0 = np.where(self.pool.get() == sender)[0][0]
        idx1 = np.where(self.pool.get() == sender)[1][0]

        self.pool.put(0,(idx0,idx1))
        self.rates[idx0][idx1]=0
        self.ages[idx0][idx1]=0
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
        if self.replacement_strategy == "custom":
            idx0 = np.where(self.pool.get() == sender)[0][0]
            idx1 = np.where(self.pool.get() == sender)[1][0]
            cost = 1
            age = 0
            doessomething = False
            width = self.pool.shape[0]
            height = self.pool.shape[1]
            position = None

            try:
                for i in range(max(idx0 - 1, 0), min(idx0 + 2, width)):
                    for j in range(max(idx1 - 1, 0), min(idx1 + 2, height)):
                        if self.pool.get()[i][j] == 0:
                            position = (i, j)
                            raise BreakIt

            except BreakIt:
                pass

            # If no free spot in the neighborhood was found, replace oldest cell in the neighborhood
            if position == None:

                oldest = 0

                for i in range(max(idx0 - 1, 0), min(idx0 + 2, width)):
                    for j in range(max(idx1 - 1, 0), min(idx1 + 2, height)):
                        if self.ages[i][j] >= oldest:
                            oldest = self.ages[i][j]
                            position = (i, j)
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
            #print('replacement now')
            try:
                for i in range(max(idx0-1, 0), min(idx0+2, width)):
                    for j in range(max(idx1-1, 0), min(idx1+2, height)):
                        if self.pool.get()[i][j] == 0:
                            position = (i,j)
                            #print('free_spot taken')
                            raise BreakIt
                            
            except BreakIt:
                pass
            
            # If no free spot in the neighborhood was found, replace oldest cell in the neighborhood
            if position == None:

                oldest = 0
                #print('nofreespot')
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

        self.pool.get()[position].fun_not = sender.fun_not_2
        self.pool.get()[position].fun_nand = sender.fun_nand_2
        self.pool.get()[position].fun_and = sender.fun_and_2
        self.pool.get()[position].fun_nor = sender.fun_nor_2
        self.pool.get()[position].fun_xor = sender.fun_xor_2
        self.pool.get()[position].fun_equ = sender.fun_equ_2
        self.pool.get()[position].fun_and_n = sender.fun_and_n_2
        self.pool.get()[position].fun_or = sender.fun_or_2
        self.pool.get()[position].fun_or_n = sender.fun_or_n_2
        if sender.fun_not != sender.fun_not_2:
            sender.child_rate = sender.child_rate/2
        if sender.fun_nand != sender.fun_nand_2:
            sender.child_rate = sender.child_rate / 2
        if sender.fun_and != sender.fun_and_2:
            sender.child_rate = sender.child_rate / 4
        if sender.fun_nor != sender.fun_nor_2:
            sender.child_rate = sender.child_rate / 16
        if  sender.fun_xor != sender.fun_xor_2:
           sender.child_rate = sender.child_rate / 16
        if sender.fun_equ != sender.fun_equ_2:
            sender.child_rate = sender.child_rate / 32
        if sender.fun_and_n != sender.fun_and_n_2:
            sender.child_rate = sender.child_rate / 8
        if sender.fun_or != sender.fun_or_2:
            sender.child_rate = sender.child_rate / 8
        if sender.fun_or_n != sender.fun_or_n_2:
            sender.child_rate = sender.child_rate / 4
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
                sender.fun_not_2 = True
                if sender.fun_not == False:
                    sender.fun_not = True
                    sender.child_rate *= 2
                    self.rates[idx0][idx1] *= 2
                    # Save input, result and the organism that computed it
                    input_ = self.inputs[idx0][idx1][0]
                    #logger.info('Not on input 1: ~{} = {}'.format(input_, result))
                    logger4.info("organism computed NOT on input 1: ~{} = {} and {} at {} \n with rate {}".format(input_,result, sender.memory, str((idx0, idx1)), self.rates[idx0][idx1]))
                    #logger.info(sender.memory)
                    # Notify us about what happened
                    #"\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED NOT\nINPUT:  " + str(input_) + "\nOUTPUT: " + str(result))

                    # Check whether the organism has computed not previously
                    # If not, reward.


                    # Slow down with those mutations now
                    # It takes a while to slow down to stable 0.0100
                    if self.cm_prob > 0.002500:
                        self.cm_prob*=1.0
                
                # If yes, ignore
                else:
                    pass
        
        # If the two most recent inputs aren't none, check whether a function of the two most recent inputs was computed
        elif self.inputs[idx0][idx1][0] != 0 and self.inputs[idx0][idx1][1] != 0:
            
            # If a NOT was computed
            
            if result == ~self.inputs[idx0][idx1][0]:
                sender.fun_not_2 = True
                if sender.fun_not == False:
                    sender.fun_not = True
                    sender.child_rate *= 2
                    self.rates[idx0][idx1] *= 2
                    # Save input, result and the organism that computed it
                    input_ = self.inputs[idx0][idx1]
                    #logger.info('Not on input 2: ~{} = {}'.format(input_[1], result))
                    logger4.info("organism computed NOT : ~{} = {} and {} at Position {} \n with rate {} \n".format(input_[1], result,sender.memory, str((idx0, idx1)),self.rates[idx0][idx1]))
                    #logger.info(sender.memory)
                    # Notify us about what happened
                    #print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED NOT\nINPUT:  " + str(input_[0]) + "\nOUTPUT: " + str(result))


                    # Check whether the organism has computed not previously
                    # If not, reward.
                    #if sender.fun_not == False:

                    # Slow down with those mutations now
                    # It takes a while to slow down to stable 0.0100
                    if self.cm_prob > 0.025:
                        self.cm_prob*=1.0

                # If yes, ignore
                else:
                    pass
            
            # If a NAND was computed
            elif result == ~(self.inputs[idx0][idx1][0] & self.inputs[idx0][idx1][1]) :
                sender.fun_nand_2 = True
                if sender.fun_nand == False:
                    sender.fun_nand = True
                    sender.child_rate *= 2
                    self.rates[idx0][idx1] *= 2
                    # Save input, result and the organism that computed it
                    input_ = self.inputs[idx0][idx1]
                    #logger.info('NAND : ~({} & {}) = {}'.format(input_[0], input_[1], result))
                    logger4.info("organism computed NAND: ~({} & {}) = {}' and {} at Position {} \n with rate {}\n".format(input_[0], input_[1], result,sender.memory, str((idx0, idx1)), self.rates[idx0][idx1]))
                    #logger.info(sender.memory)
                    # Notify us about what happened
                    #print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED NAND\nINPUT: " + str(input_) + "\nOUTPUT:  " + str(result))

                    # Check whether the organism has computed nand previously
                    # If not, reward.
 #                   if sender.fun_nand == False:

                    # Slow down with those mutations now
                    # It takes a while to slow down to stable 0.002500
                    if self.cm_prob > 0.002500:
                        self.cm_prob*=1.
                
                # If yes, ignore
                else:
                    pass
                
            # If an AND was computed
            elif result == self.inputs[idx0][idx1][0] & self.inputs[idx0][idx1][1] and sender.fun_and == False:
                sender.fun_and_2 = True
                if sender.fun_and == False:
                    sender.fun_and = True
                    sender.child_rate *= 4
                    self.rates[idx0][idx1] *= 4
                    # Save input, result and the organism that computed it
                    input_ = self.inputs[idx0][idx1]
                    #logger.info('AND : {} & {} = {}'.format(input_[0], input_[1], result))
                    logger4.info("organism computed AND: {} & {} = {} and {} at Position {} \n with rate {}".format(input_[0], input_[1], result,sender.memory, str((idx0, idx1)),self.rates[idx0][idx1]))
                    #logger.info(sender.memory)
                    # Notify us about what happened
                    #print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED AND\nINPUT: " + str(input_) + "\nOUTPUT:  " + str(result))

                    # Check whether the organism has computed and previously
                    # If not, reward.

                        # Slow down with those mutations now
                        # It takes a while to slow down to stable 0.002500
                    if self.cm_prob > 0.002500:
                        self.cm_prob*=1.
                
                # If yes, ignore
                else:
                    pass
                
            # If an OR_N was computed
            elif result == self.inputs[idx0][idx1][0] | ~self.inputs[idx0][idx1][1] or result == ~self.inputs[idx0][idx1][0] | self.inputs[idx0][idx1][1] :
                sender.fun_or_n_2 = True
                if sender.fun_or_n == False:
                    sender.fun_or_n = True
                    sender.child_rate *= 4
                    self.rates[idx0][idx1] *= 4
                    input_ = self.inputs[idx0][idx1]
                    if (result == self.inputs[idx0][idx1][0] | ~self.inputs[idx0][idx1][1]):
                        #logger.info('OR_N : {} | ~{} = {}'.format(input_[0], input_[1], result))
                        logger4.info('organism computed OR_n: {} | ~{} = {} and {} at Position {} with rate {} \n'.format(input_[0], input_[1], result,sender.memory, str((idx0, idx1)), self.rates[idx0][idx1]))
                        #logger.info(sender.memory)
                    else:
                        #logger.info('OR_N : ~{} | {} = {}'.format(input_[0], input_[1], result))
                        logger4.info('organism computed OR_N : ~{} | {} = {} and {} Position at {} with rate {} \n'.format(input_[0], input_[1], result,sender.memory, str((idx0, idx1)), self.rates[idx0][idx1]))
                        #logger.info(sender.memory)
                    # Notify us about what happened
                    #print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED OR_N\nINPUT: " + str(input_) + "\nOUTPUT:  " + str(result))


                    # Check whether the organism has computed or_n previously
                # If not, reward.
#                if sender.fun_or_n == False:

                    # Slow down with those mutations now
                    # It takes a while to slow down to stable 0.002500
                    if self.cm_prob > 0.002500:
                        self.cm_prob*=1.
                
                # If yes, ignore
                else:
                    pass
                
            # If an OR was computed
            elif result == self.inputs[idx0][idx1][0] | self.inputs[idx0][idx1][1] and sender.fun_or == False:
                sender.fun_or_2 = True
                if sender.fun_or == False:
                    sender.fun_or = True
                    sender.child_rate *= 8
                    self.rates[idx0][idx1] *= 8

                    input_ = self.inputs[idx0][idx1]

                    #logger.info('OR : {} | {} = {}'.format(input_[0], input_[1], result))
                    logger4.info("organism computed OR: {} | {} = {} and {} at Position {} with rate {}\n".format(input_[0], input_[1], result,sender.memory, str((idx0, idx1)),self.rates[idx0][idx1]))
                    #logger.info(sender.memory)
                    # Notify us about what happened
                    #print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED OR\nINPUT: " + str(input_) + "\nOUTPUT:  " + str(result))

                    # Check whether the organism has computed or previously
                    # If not, reward.

                        # Slow down with those mutations now
                        # It takes a while to slow down to stable 0.002500
                    if self.cm_prob > 0.002500:
                        self.cm_prob*=1.

                # If yes, ignore
                else:
                    pass
                
            # If an AND_N was computed
            elif result == self.inputs[idx0][idx1][0] & ~self.inputs[idx0][idx1][1] or result == ~self.inputs[idx0][idx1][0] & self.inputs[idx0][idx1][1]:
                sender.fun_and_n_2 = True
                if sender.fun_and_n == False:
                    sender.fun_and_n = True
                    sender.child_rate *= 8
                    self.rates[idx0][idx1] *= 8
                    input_ = self.inputs[idx0][idx1]
                    if result == self.inputs[idx0][idx1][0] & ~self.inputs[idx0][idx1][1]:
                        #logger.info('AND_N : {} & ~{} = {}'.format(input_[0], input_[1], result))
                        logger4.info("organism computed AND_N: {} & ~{} = {} and {} at Position {} \n  with rate {}\n".format(input_[0], input_[1], result,sender.memory, str((idx0, idx1)),self.rates[idx0][idx1]))
                        #logger.info(sender.memory)
                    else:
                        #logger.info('AND_N : ~{} & {} = {}'.format(input_[0], input_[1], result))
                        logger4.info("organism computed AND_N: ~{} & {} = {} and {} at Position {} \n with rate {} \n".format(input_[0], input_[1], result,sender.memory, str((idx0, idx1)), self.rates[idx0][idx1]))
                        #logger.info(sender.memory)
                    # Notify us about what happened
                    #print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED AND_N\nINPUT: " + str(input_) + "\nOUTPUT:  " + str(result))

                    # Check whether the organism has computed and_n previously
                    # If not, reward.
                    # Slow down with those mutations now
                    # It takes a while to slow down to stable 0.002500
                    if self.cm_prob > 0.002500:
                        self.cm_prob*=1.
                
                # If yes, ignore
                else:
                    pass
                
            # If a NOR was computed
            elif result == ~(self.inputs[idx0][idx1][0] | self.inputs[idx0][idx1][1]):
                sender.fun_nor_2 = True
                if sender.fun_nor == False:
                    sender.fun_nor = True
                    sender.child_rate *= 16
                    self.rates[idx0][idx1] *= 16
                    input_ = self.inputs[idx0][idx1]

                    #logger.info('NOR : ~{} & ~{} = {}'.format(input_[0], input_[1], result))
                    logger4.info("organism computed NOR: ~{} & ~{} = {} and {} at Position {} with rate {}\n".format(input_[0], input_[1], result,sender.memory, str((idx0, idx1)), self.rates[idx0][idx1]))
                    #logger.info(sender.memory)
                    # Notify us about what happened
                    #print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED NOR\nINPUT: " + str(input_) + "\nOUTPUT:  " + str(result))

                    # Check whether the organism has computed nand previously
                    # If not, reward.


                    # Slow down with those mutations now
                    # It takes a while to slow down to stable 0.002500
                    if self.cm_prob > 0.002500:
                        self.cm_prob*=1.
                
                # If yes, ignore
                else:
                    pass
                
            # If an XOR was computed:
            elif result == self.inputs[idx0][idx1][0] ^ self.inputs[idx0][idx1][1]:
                sender.fun_xor_2 = True
                if sender.fun_xor == False:
                    sender.fun_xor = True
                    sender.child_rate *= 16
                    self.rates[idx0][idx1] *= 16
                    # Save input, result and the organism that computed it
                input_ = self.inputs[idx0][idx1]
                #logger.info('XOR : {} & ~{} | ~{} & {} = {}'.format(input_[0], input_[1], (input_[0]), input_[1], result))
                logger4.info("organism computed XOR: {} & ~{} | ~{} & {} = {} and {} at Position {} with rate {}\n".format(input_[0], input_[1], (input_[0]), input_[1], result,sender.memory, str((idx0, idx1)), self.rates[idx0][idx1]))
                #logger.info(sender.memory)
                # Notify us about what happened
                #print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED XOR\nINPUT: " + str(input_) + "\nOUTPUT: " + str(result))
                
                # Check whether the organism has computed xor previously
                # If not, reward.

                    # Slow down with those mutations now
                    # It takes a while to slow down to stable 0.002500
                if self.cm_prob > 0.002500:
                    self.cm_prob*=1.
                
                # If yes, ignore
                else:
                    pass
                
            # If EQU was computed:
            elif result == equ(self.inputs[idx0][idx1][0], self.inputs[idx0][idx1][1]):
                sender.fun_equ_2 = True
                if sender.fun_equ == False:
                    sender.fun_equ = True
                    sender.child_rate *= 32
                    self.rates[idx0][idx1] *= 32
                # Save input, result and the organism that computed it
                input_ = self.inputs[idx0][idx1]
                #logger.critical('EQU : {} & {} | ~{} & ~{} = {}'.format(input_[0], input_[1], input_[0], input_[1], result))
                logger4.info("organism computed EQU: {} & {} | ~{} & ~{} = {} and {} at Position {} with rate {}\n".format(input_[0], input_[1], input_[0], input_[1], result,sender.memory, str((idx0,idx1)), self.rates[idx0][idx1]))
                logger2.critical(sender.memory)
                # Notify us about what happened
                #print("\nEMULATOR AT POSITION " + str((idx0,idx1)) + " COMPUTED EQU\nINPUT: " + str(input_) + "\nOUTPUT: " + str(result))
                
                # Check whether the organism has computed xor previously
                # If not, reward.

                    # Slow down with those mutations now
                    # It takes a while to slow down to stable 0.002500
                if self.cm_prob > 0.002500:
                    self.cm_prob*=1.
                
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

        #return np.min(self.rates[self.rates > 0])

        try:
            return np.min(self.rates[self.rates > 0])
        except:
            return 1
    def max_rate(self):
        
        # Returns the maximal metabolic rate value present
        try:
            return np.max(self.rates[self.rates > 0])
        except:
            return 1
    def get_pool(self):
        
        return self.pool.get()
    
    # Returns the emulator at the given position
    
    def get(self,position):
        
        return self.pool.get()[position]
    
    # A function that fills the world with the chosen organism type
    def fill(self, organism_type = "default_IO"):
        
        if organism_type == "default_IO":
            #self.place_def_io((15,15))
            for i in range(self.pool.shape[0]):
                for j in range(self.pool.shape[1]):
                    if i<25 or j <22:
                        #self.place_zero((i,j))
                        #self.place_def_io((i,j))
                    #elif( i==16 and j ==26):
                        pass
                    #    self.place_default_15((i,j))
                    else:

                        self.place_default((i,j))
                        self.rates[i][j]=1
            #self.place_def_io((17,13))
        elif organism_type == "default":
            
            for i in range(self.pool.shape[0]):
                for j in range(self.pool.shape[1]):
                    self.place_default((i,j))
        #for i in range(self.pool.shape[0]):
        #    for j in range(self.pool.shape[1]):
        #        self.rates[i][j]=1
    # Find the minimum genome length present in the pool
    def shortest_genome(self):
        
        shortest = 1000
        
        for i in range(self.pool.shape[0]):
            for j in range(self.pool.shape[1]):
                if (self.pool.get()[i][j] == 0):
                    pass
                else:
                    length = self.pool.get()[i][j].instruction_memory.size()
                    if length <= shortest:
                        shortest = length
                    
        return shortest
    
    # Find the maximum genome length present in the pool
    def longest_genome(self):
        
        longest = -1
        
        for i in range(self.pool.shape[0]):
            for j in range(self.pool.shape[1]):
                if (self.pool.get()[i][j] == 0):
                    pass
                else:
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
world = World(30,replacement_strategy="neighborhood",cm_prob = 0.0025, ins_prob = 0.05, del_prob = 0.05)

# Filling the world with the default organisms instantiated with two IOs
world.fill()

print("World full")

#%%
world.schedule()