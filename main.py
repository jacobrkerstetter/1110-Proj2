# this is where the main code will go
# input instructions, parse them into op - address - arrival time

# stall next instruction until returned from last

from Cache import Cache

c = Cache(2, 32, 5, 4, 4, 0) # 16 byte layer
c.CreateLevelCache(64, 5, 4, 4, 0)

# print empty contents
c.printInfo()

# write into cache
for i in range(32):
    c.write(i, 100, i)

c.printInfo()

# do some test case like:
# find a bunch of addr that addr the same set but have different tags, so they evict 
# read those addr in in order to push LRU to different elements 
c.write(0, 123, 0)
c.write(1, 321, 1)
c.write(2, 111, 2)
c.write(0, 123, 3) 
c.printInfo()