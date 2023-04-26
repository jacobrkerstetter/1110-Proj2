from LevelCache import LevelCache
# cache class

class Cache:

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
    def read(self, address, arrivingTime):
        latency = 0
        for cache in self.cacheHierarchy:
            latency += cache.latency
            if cache.read(address, arrivingTime)[0]:
                break

        print('Finish Time:', arrivingTime)
        print('Total Read Latency:', latency)

        return latency
            
    # Function write
    def write(self, address, data, arrivingTime):
        # consider write-thru and write-back for each level
        latency = 0

        for cache in self.cacheHierarchy:
            latency += cache.latency

            # if this cache is write-back
            if cache.writePolicy == 0:
                # if level cache hits on write
                if cache.read(address, arrivingTime)[0] != False:
                    # write data into cache and mark as dirty
                    cache.write(address, 1, data, arrivingTime)
                    # break
                    break

                # if level cache misses on write
                else:
                    # if data read is dirty, read from memory into all levels
                    if cache.read(address, arrivingTime)[1].dirty == 1 and cache.lastLevel:
                        # missed and went to memory
                        latency += 100
                        for i in range(len(self.cacheHierarchy)):
                            self.cacheHierarchy[i].write(address, 0, 100, arrivingTime)
                    
                    # if data is not dirty, fill from L2 to L1
                    elif cache.read(address, arrivingTime)[1].dirty == 0:
                        for i in range(len(self.cacheHierarchy)):
                            if cache == self.cacheHierarchy[i]:
                                break
                            
                            self.cacheHierarchy[i].write(address, 0, cache.read(address, arrivingTime)[1].data, arrivingTime)

                    # check if set needed is full
                    isFull = cache.isFull(address)

                    # if set needed is full, must evict
                    if isFull:
                        # do LRU stuff ########### not done
                        LRU = cache.evict(address)
                        # write into the LRU block
                        cache.write(LRU, 1, data, arrivingTime)
                    
                    # put the item in a free block
                    cache.write(address, 1, data, arrivingTime)

            # if this cache is write-thru
            else:
                # if cache hits, write to next level as well
                if cache.read(address, arrivingTime)[0] != False:
                    # write as not dirty because it will write through
                    cache.write(address, 0, data, arrivingTime)

                # if cache misses
                else:
                    # if cache is last level, write default 100 memory data
                    if cache.lastLevel:
                        # add 100 if entered memory
                        latency += 100
                        cache.write(address, 0, 100, arrivingTime)

        return latency
        
    # Function print contents
    def printInfo(self):
        for i in range(len(self.cacheHierarchy)):
            print("Level", i+1, end=' ')     
            print("Hit rate: " + str(self.cacheHierarchy[i].hitRate()) + '%')
            print("Miss rate: " + str(self.cacheHierarchy[i].missRate()) + '%')

        for i in range(len(self.cacheHierarchy)):
            print('Cache L' + str(i + 1))
            self.cacheHierarchy[i].printContents()