# this is where the main code will go
# input instructions, parse them into op - address - arrival time

# stall next instruction until returned from last

from Cache import Cache

# test case 1 (2 level write back):
'''
programLatency = 0

c = Cache(2, 32, 5, 4, 4, 0)
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