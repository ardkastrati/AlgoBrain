# DO NOT IMPORT import World -> Avoid Circular import!
import SimpleAvida as SA
import Standardprogram as st
import World as wd
#%%
""" File Scheduler plans our World, what effiency do cells have, executions pro clock takt"""

p = SA.Program([16, 20, 3, 2, 0, 21, 2, 20, 19, 25, 2, 0, 6, 17, 21, 0, 1])
# A world with a 4-slot pool
world = wd.World(4)

# Manually creating the first CPUEmulator
emulator = SA.CPUEmulator()

# Loading the self-replicating program into the first emulator
emulator.load_program(p)

# Placing the emulator into a random position in the world
world.place_cell(emulator)

# Running it for 104 cycles (hard coded atm, for testing purposes)
world.schedule()

# Showing the resulting World Emulator Pool
print(world)
