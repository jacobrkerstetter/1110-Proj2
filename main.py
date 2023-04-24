# this is where the main code will go
# input instructions, parse them into op - address - arrival time

# stall next instruction until returned from last

from Cache import Cache

c = Cache(2, 16, 5, 4, 4, 0) # 16 byte layer
c.CreateLevelCache(32, 5, 4, 4, 0)

# print empty contents
c.printInfo()

# write into cache
c.write(1, 100, 1) # write 100 into address: 0000
c.printInfo()