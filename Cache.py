from LevelCache import LevelCache
# cache class

# all layers
# static variable hits, misses, total accessses
global HITS, MISSES, ACCESSES

# Constructor #
class Cache:
    def __init__(self, layers, size, latency, blockSize, setAssociativity, writePolicy):
        # self.size = size
        # self.latency = latency
        # self.blockSize = blockSize
        # self.setAssociativity = setAssociativity
        # self.writePolicy = writePolicy
        self.layers = layers
        self.L1 = LevelCache(size, latency, blockSize, setAssociativity, writePolicy)

# Create Cache
    def CreateLevelCache(self, level):
        level = LevelCache(self.size, self.latency, self.blockSize, self.setAssociativity, self.writePolicy)

# function read (return hit/miss, latency, finish time)
    def read(self):
        if(self.L1.read(self, self.addr)):
            HITS = HITS + 1
            self.printInfo(self, self.latency)
        else:
            MISSES = MISSES + 1

# function write
    def write(self):
       self.L1 = LevelCache.write()
    

# function print contents
    def printInfo(self):
        # output all cache information
        print("Finish Time: ")
        print("/nTotal Latency: " + self.latency)
        print("/nCache Status (Only dirty bits): ")
        print("/nFinish Time: ")
        print("/nHit rate: " + self.hitRate())
        print("/nMiss rate: " + self.missRate())


# function hit rate
    def hitRate():
        hitRate = HITS / (HITS + MISSES)
        print(hitRate)

# function miss rate
    def missRate():
        missRate = MISSES / (HITS + MISSES)
        print(missRate)