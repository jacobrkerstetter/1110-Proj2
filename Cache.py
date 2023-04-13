from LevelCache import LevelCache
# cache class

# all layers
# static variable hits, misses, total accessses
global HITS, MISSES, ACCESSES

# Constructor #
class Cache:
    def __init__(self, op, address, ArrivingTime, size, latency, blockSize, setAssociativity, writePolicy):
        self.op = op
        self.addr = address
        self.ArrTime = ArrivingTime
        # self.size = size
        # self.latency = latency
        # self.blockSize = blockSize
        # self.setAssociativity = setAssociativity
        # self.writePolicy = writePolicy
        self.L1 = LevelCache(size, latency, blockSize, setAssociativity, writePolicy)

# Create Cache #
    def CreateLevelCache(self, level, size, latency, blockSize, setAssociativity, writePolicy):
        self.level = level # level number of the cache
        self.size = size # total capacity in bytes
        self.latency = latency # access latency in cycles
        self.blockSize = blockSize # block size in bytes
        self.setAssociativity = setAssociativity # set associativity in ways
        self.writePolicy = writePolicy # 0 = write-back, 1 = write-through

        self.contents = [] # [ set 1 , set 2 , set 3 , set 4 ]
                           # [ [ [block 1], [block 2], ... ] , [ [block 1], [block 2], ... ] ]
                           # block 1: [ valid , dirty , tag , data ]

# function read (return hit/miss, latency, finish time)
    def read(self):
        if(self.L1.read(self, self.addr)):
            HITS = HITS + 1
            Cache.printInfo(self, self.latency)


# function write
# function print contents
    def printInfo(self, latency):
        #output all cache information
        print("Finish Time: ")
        print("/nTotal Latency: " + latency)
        print("/nCache Status (Only dirty bits): ")
        print("/nFinish Time: ")
        print("/nHit rate: " + Cache.hitRate())
        print("/nMiss rate: " + Cache.missRate())


# function hit rate
    def hitRate():
        hitRate = HITS / (HITS + MISSES)
        print(hitRate)

# function miss rate
    def missRate():
        missRate = MISSES / (HITS + MISSES)
        print(missRate)