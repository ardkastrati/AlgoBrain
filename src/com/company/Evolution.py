# -*- coding: utf-8 -*-
"""
Creating a World as was done in the "Nature" paper

Parameters:
    
    Size 60
    
"""

#%% 
# Necessary imports:
    
from Environment import World

world = World(60)

world.fill("default")

world.schedule(n_notify = 1000)