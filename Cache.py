from LevelCache import LevelCache
# cache class

class Cache:
    # static variable hits, misses, total accessses
    HITS, MISSES, ACCESSES = 0, 0, 0

    # Constructor
    def __init__(self, layers, size, latency, blockSize, setAssociativity, writePolicy):
        self.layers = layers
        L1 = LevelCache(size, latency, blockSize, setAssociativity, writePolicy)

        self.cacheHierarchy = [L1]

        # self.latency = latency
        # self.blockSize = blockSize
        # self.setAssociativity = setAssociativity
        # self.writePolicy = writePolicy

    # Create New Level
    def CreateLevelCache(self, size, latency, blockSize, setAssociativity, writePolicy):
        # create new level in the cache
        level = LevelCache(size, latency, blockSize, setAssociativity, writePolicy)

        # set the last level flag to false in the previously LLC
        self.cacheHierarchy[len(self.cacheHierarchy) - 1].lastLevel = False

        # append new cache to the hierarchy
        self.cacheHierarchy.append(level)

    # Function read (return hit/miss, latency, finish time)
    def read(self):
        if(self.L1.read(self, self.addr)):
            HITS = HITS + 1
            self.printInfo(self, self.latency)
        else:
            MISSES = MISSES + 1

    # Function write
    def write(self, address, data, arrivingTime):
        # consider write-thru and write-back for each level

        for cache in self.cacheHierarchy:
            # if this cache is write-back
            if cache.writePolicy == 0:
                # if level cache hits on write
                if cache.read(address) == 1:
                    # increment cache hits
                    Cache.HITS += 1

                    # write data into cache and mark as dirty
                    cache.write(address, 1)

                    # if there are lower level caches, continue loop and write there as well

                # if level cache misses on write
                else:
                    # increment misses
                    Cache.MISSES += 1

                    # check if set needed is full
                    isFull = cache.isFull(address)

                    # if set needed is full, must evict
                    if isFull:
                        # do LRU stuff ########### not done
                        cache.evict(address)
                    
                    # put the item in a free block
                    cache.write(address, data)

            # if this cache is write-thru
            else:
                # if cache hits, write to next level as well
                if cache.read(address) == 1:
                    cache.write(address, 0)

                # if cache misses
        


    # Function print contents
    def printInfo(self):
        # output all cache information
        print("Finish Time: ")
        print("Cache Status (Only dirty bits): ")
        print("Finish Time: ")
        print("Hit rate: " + str(self.hitRate()))
        print("Miss rate: " + str(self.missRate()))

        for cache in self.cacheHierarchy:
            cache.printContents()


    # Function hit rate
    def hitRate(self):
        try:
            hitRate = Cache.HITS / (Cache.HITS + Cache.MISSES)
        except:
            hitRate = 0

        print(hitRate)

    # Function miss rate
    def missRate(self):
        try:
            missRate = Cache.MISSES / (Cache.HITS + Cache.MISSES)
        except:
            missRate = 0

        print(missRate)