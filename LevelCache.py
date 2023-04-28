# each level of the cache
# size (bytes), latency (cycles), block size (bytes), 
# set associativity, write policy

# storage array
# [ [valid (0/1), dirty (0/1), data] ], data, data, ...]
# store newest data at the end, LRU is the front element and we will pop off

from Block import Block
from math import log2
import random

class LevelCache:
    def __init__(self, size, latency, blockSize, setAssociativity, writePolicy, level):
        self.size = size # total capacity in bytes
        self.latency = latency # access latency in cycles
        self.blockSize = blockSize # block size in bytes
        self.setAssociativity = setAssociativity # set associativity in ways
        self.sets = (self.size // self.blockSize) // self.setAssociativity
        self.writePolicy = writePolicy # 0 = write-back, 1 = write-through
        self.level = level
        self.lastLevel = True
        self.tagBits = 32 - int(log2(self.blockSize)) - int(log2(self.sets))

        self.contents = [] # [ [ [block 1], [block 2], ... ] , [ [block 1], [block 2], ... ] ]
                           # block 1: [ valid , dirty , tag , data ]

        self.fillEmptyContents()

        self.hits = 0
        self.misses = 0

    def fillEmptyContents(self):
        layers = self.sets
        for i in range(layers):
            setArr = []
            for j in range(self.setAssociativity):
                block = Block(0, 0, 0, self.blockSize)
                block.data = [0 for i in range(self.blockSize)]
                setArr.append(block)

            self.contents.append(setArr)

    def write(self, address, dirty, data, arrivalTime):
        # set index and tag
        setIndex = (address // self.blockSize) % self.sets
        tag = address >> (32 - self.tagBits)

        # create new block to write
        newBlock = Block(1, dirty, tag, self.blockSize)
        newBlock.data = data
        newBlock.timeAccessed = arrivalTime

        for i, block in enumerate(self.contents[setIndex]):
            # the first empty block we come across, fill
            if not block.valid:
                self.contents[setIndex][i] = newBlock
                return
  
        # if none were empty, find the LRU and place there
        LRUIndex = self.LRU(setIndex)
        self.contents[setIndex][LRUIndex] = block

    def writeAccess(self, address):
        setIndex = (address // self.blockSize) % self.sets
        tag = address >> (32 - self.tagBits)

        for i, block in enumerate(self.contents[setIndex]):
            # if the block is valid and the tag matches, return true
            if block.valid and block.tag == tag:
                self.hits += 1
                print(self.level, 'hit write')
                return True

        # if the address cannot be found, miss, return false
        self.misses += 1
        return False

    def writeUp(self, address, dirty, newBlock, arrivalTime):
        # block address
        setIndex = (address // self.blockSize) % self.sets
        tag = address >> (32 - self.tagBits)

        newBlock.tag = tag

        for i, block in enumerate(self.contents[setIndex]):
            # the first empty block we come across, fill
            if block.timeAccessed == arrivalTime:
                self.contents[setIndex][i] = newBlock
                return

    def read(self, address, arrivalTime):
        # which block in a set is accessed
        blockOffset = address % self.blockSize

        # block address
        setIndex = (address // self.blockSize) % self.sets

        tag = address >> (32 - self.tagBits)

        # for each block in the set, search
        for block in self.contents[setIndex]:
            # if you find your tag and it's valid, hit
            if block.tag == tag and block.valid:
                self.hits += 1
                block.timeAccessed = arrivalTime
                return [True, block, self.level]
        
        
        # if miss, then write into first empty block
        # increment miss
        self.misses += 1

        # create new block from memory
        newBlock = Block(1, 0, tag, self.blockSize)
        newBlock.data = [random.randint(0, 255) for i in range(self.blockSize)]
        newBlock.timeAccessed = arrivalTime

        for i, block in enumerate(self.contents[setIndex]):
            # the first empty block we come across, fill
            if not block.valid:
                self.contents[setIndex][i] = newBlock
                return [False, newBlock, self.level]

        # if none were empty, find the LRU and place there
        LRUIndex = self.LRU(setIndex)
        self.contents[setIndex][LRUIndex] = newBlock

        return [False, newBlock, self.level]     

    # function to return the LRU block
    def LRU(self, setIndex):
        LRUTime, index = self.contents[setIndex][0].timeAccessed, 0
        for i in range(len(self.contents[setIndex])):
            if self.contents[setIndex][i].timeAccessed < LRUTime:
                LRUTime = self.contents[setIndex][i].timeAccessed
                index = i

        return index

    # function to calculate hit rate
    def hitRate(self):
        try:
            hitRate = self.hits / (self.hits + self.misses)
        except:
            hitRate = 0

        return int(hitRate*100)

    # function to calculate miss rate
    def missRate(self):
        try:
            missRate = self.misses / (self.hits + self.misses)
        except:
            missRate = 0

        return int(missRate*100)

    # function to print cache contents
    def printContents(self):
        setNum = 0
        for setObj in self.contents:
           print('Set #', setNum, end=': ')
           setNum += 1
           for i in range(len(setObj)):
               print('Block #' + str(i) + ': ' + str(setObj[i].data) + ' (' + str(setObj[i].tag), str(setObj[i].timeAccessed) + ')', end=' ')

           print('')