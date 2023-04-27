# each level of the cache
# size (bytes), latency (cycles), block size (bytes), 
# set associativity, write policy

# storage array
# [ [valid (0/1), dirty (0/1), data] ], data, data, ...]
# store newest data at the end, LRU is the front element and we will pop off

from Block import Block
from math import log2

class LevelCache:
    # static variable hits, misses, total accessses

    def __init__(self, size, latency, blockSize, setAssociativity, writePolicy):
        self.size = size # total capacity in bytes
        self.latency = latency # access latency in cycles
        self.blockSize = blockSize # block size in bytes
        self.setAssociativity = setAssociativity # set associativity in ways
        self.writePolicy = writePolicy # 0 = write-back, 1 = write-through
        self.lastLevel = True
        self.tagBits = 32 - int(log2(self.blockSize)) - int(log2(self.setAssociativity))

        self.contents = [] # [ [ [block 1], [block 2], ... ] , [ [block 1], [block 2], ... ] ]
                           # block 1: [ valid , dirty , tag , data ]

        self.fillEmptyContents()

        self.hits = 0
        self.misses = 0

    def fillEmptyContents(self):
        layers = self.size // self.blockSize
        for i in range(layers):
            setArr = []
            for j in range(self.blockSize):
                block = Block(0, 0, 0, 0)
                setArr.append(block)

            self.contents.append(setArr)

    def write(self, address, dirty, data, arrivalTime):
        # which block in a set is accessed
        blockOffset = address % self.blockSize

        # block address
        setIndex = (address // self.blockSize) % (self.size // self.setAssociativity)

        tag = address >> (32 - self.tagBits)

        block = Block(1, dirty, tag, data)
        block.timeAccessed = arrivalTime
        self.contents[setIndex][blockOffset] = block

    def read(self, address, arrivalTime):
        # which block in a set is accessed
        blockOffset = address % self.blockSize

        # block address
        setIndex = (address // self.blockSize) % (self.size // self.setAssociativity)

        tag = address >> (32 - self.tagBits)
       
        if not self.contents[setIndex][blockOffset].valid:
            # increment miss
            self.misses += 1

            self.contents[setIndex][blockOffset] = Block(1, 0, tag, 100)
            self.contents[setIndex][blockOffset].timeAccessed = arrivalTime
            return [False, self.contents[setIndex][blockOffset]]
        
        # if tag doesnt match, increment miss
        if self.contents[setIndex][blockOffset].tag != tag:
            self.misses += 1
            return [False, self.contents[setIndex][blockOffset]]

        # if tag matches, increment hit
        else:
            self.hits += 1

        # update time accessed and return data
        self.contents[setIndex][blockOffset].timeAccessed = arrivalTime
        return [True, self.contents[setIndex][blockOffset]]

    # function to find out if the set needed is full
    def isFull(self, address):
        # calculate set
        setLoc = (address // self.blockSize) % (self.size // self.blockSize)

        # iterate over set to see if it is full
        for block in self.contents[setLoc]:
            if block.valid == 0:
                return False

        return True

    # function to evict LRU content from set
    def evict(self, address):
        # get set location
        setLoc = (address // self.blockSize) % (self.size // self.setAssociativity)

        # set base minimum
        LRUTime = self.contents[setLoc][0].timeAccessed
        LRUBlock = 0

        # search each block in the set for minimum
        for i in range(len(self.contents[setLoc])):
            if self.contents[setLoc][i].timeAccessed < LRUTime:
                LRUTime = self.contents[setLoc][i].timeAccessed
                LRUBlock = i
        
        return LRUBlock

    # Function hit rate
    def hitRate(self):
        try:
            hitRate = self.hits / (self.hits + self.misses)
        except:
            hitRate = 0

        return int(hitRate*100)

    # Function miss rate
    def missRate(self):
        try:
            missRate = self.misses / (self.hits + self.misses)
        except:
            missRate = 0

        return int(missRate*100)

    def printContents(self):
        setNum = 0
        for setObj in self.contents:
            print('Set #', setNum, end=': ')
            setNum += 1
            for i in range(len(setObj)):
                print('Block #' + str(i) + ': ' + str(setObj[i].data) + ' (' + str(setObj[i].tag), str(setObj[i].timeAccessed) + ')', end=' ')

            print('')