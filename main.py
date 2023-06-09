# this is where the main code will go
# input instructions, parse them into op - address - arrival time

# stall next instruction until returned from last

from Cache import Cache

# test case 1 (2 level write back):

programLatency = 0

c = Cache(2, 64, 1, 16, 4, 0)
c.CreateLevelCache(256, 50, 16, 8, 0)

# print empty contents

# warm up set 0 
programLatency += c.read(0, programLatency) # miss
programLatency += c.read(16, programLatency) # miss
programLatency += c.read(32, programLatency) # miss
programLatency += c.read(1, programLatency) # hit!
programLatency += c.read(48, programLatency) # miss - L1 full
programLatency += c.read(64, programLatency) # miss - overwrite 16
programLatency += c.read(16, programLatency) # miss L1, hit L2
programLatency += c.read(80, programLatency) # miss

data = [123 for i in range(16)]
programLatency += c.write(0, data, programLatency) # write hit in L2 for write through, miss L1 (do nothing)


'''
# test case 2 (2 level write thru):
programLatency = 0

c = Cache(2, 32, 5, 4, 4, 1)
c.CreateLevelCache(64, 5, 4, 4, 0)

# print empty contents
c.printInfo()

# warm up
for i in range(32):
    programLatency += c.read(i, i)

c.printInfo()

programLatency += c.write(0, 123, 32)
programLatency += c.write(1, 321, 33)
programLatency += c.write(2, 111, 34)
programLatency += c.write(0, 412, 35) 
print('Program Latency:', programLatency)
c.printInfo()
'''

'''
# test case 3 (read miss):
programLatency = 0

c = Cache(2, 32, 5, 4, 4, 1)
c.CreateLevelCache(64, 5, 4, 4, 0)

# warm up
for i in range(32):
    programLatency += c.read(i, i)

programLatency += c.read(33, 33)

print('Program Latency:', programLatency)
c.printInfo()
'''

'''
# test case 4 (read miss, then write, then read hit):
programLatency = 0

c = Cache(2, 32, 5, 4, 4, 0)
c.CreateLevelCache(64, 5, 4, 4, 0)

# warm up
for i in range(32):
    programLatency += c.read(i, i)

programLatency += c.read(33, 33)
programLatency += c.write(33, 123, 34)
programLatency += c.read(33, 35)

print('Program Latency:', programLatency)
c.printInfo()
'''

'''
# test case 5 (miss L1 hit L2):
programLatency = 0

c = Cache(2, 32, 5, 4, 4, 1)
c.CreateLevelCache(64, 5, 4, 4, 0)

# warm up
for i in range(64):
    programLatency += c.read(i, i)

# write to L2
c.write(45, 456, 33)

# read
c.read(45, 35)

print('Program Latency:', programLatency)
c.printInfo()
'''