from LevelCache import LevelCache
import random
from copy import deepcopy
# cache class

class Cache:
    LEVELS_ACTIVE = 1

    # Constructor
    def __init__(self, layers, size, latency, blockSize, setAssociativity, writePolicy):
        self.layers = layers
        L1 = LevelCache(size, latency, blockSize, setAssociativity, writePolicy, 1)

        self.cacheHierarchy = [L1]

        # self.latency = latency
        # self.blockSize = blockSize
        # self.setAssociativity = setAssociativity
        # self.writePolicy = writePolicy

    # Create New Level
    def CreateLevelCache(self, size, latency, blockSize, setAssociativity, writePolicy):
        # create new level in the cache
        Cache.LEVELS_ACTIVE += 1
        level = LevelCache(size, latency, blockSize, setAssociativity, writePolicy, Cache.LEVELS_ACTIVE)

        # set the last level flag to false in the previously LLC
        self.cacheHierarchy[len(self.cacheHierarchy) - 1].lastLevel = False

        # append new cache to the hierarchy
        self.cacheHierarchy.append(level)

    # Function read (return hit/miss, latency, finish time)
    def read(self, address, arrivingTime):
        latency = 0
        readResults = []
        for cache in self.cacheHierarchy:
            latency += cache.latency
            readResults = cache.read(address, arrivingTime)
            # hit in whatever level we are searching
            if readResults[0]:
                break
            # if we miss in the level, search the next level

        #print('Finish Time:', arrivingTime)
        #print('Total Read Latency:', latency)

        # after searching all levels, if we missed, add 100 cycles for going to memory
        latency += 100
        
        # after all searches, if we have a hit, figure out what level it is
        hitLevel = readResults[2]
        newBlock = readResults[1]

        # if there are levels above the hit level, write the data up
        i = 1 # start at L1
        while i < hitLevel:
            self.cacheHierarchy[i - 1].writeUp(address, 0, deepcopy(newBlock), arrivingTime)

            # increment the level writing to
            i += 1

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
                if cache.writeAccess(address):
                    # write data into cache and mark as dirty
                    cache.write(address, 1, data, arrivingTime)

                    # copy into lower level caches
                    for c in range(cache.level, self.layers):
                        c.write(address, 1, data, arrivingTime)

                    # break, writing is done, no need to go to memory
                    break

                # if level cache misses on write
                else:
                    # write, may cause eviction based on LRU policy
                    cache.write(address, 0, data, arrivingTime)

            # if this cache is write-thru
            else:
                # if cache hits, write to next level as well
                if cache.writeAccess(address):
                    # write as not dirty because it will write through
                    cache.write(address, 0, data, arrivingTime)

                # if cache misses do nothing, essentially would continue all the way to memory (not represented in our code)

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