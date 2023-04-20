# this is where the main code will go
# input instructions, parse them into op - address - arrival time

# stall next instruction until returned from last

from Cache import Cache

c = Cache(2, 8, 5, 4, 4, 0)
c.CreateLevelCache(16, 5, 4, 4, 0)

c.printInfo()