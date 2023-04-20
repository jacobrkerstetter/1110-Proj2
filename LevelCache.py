# each level of the cache
# size (bytes), latency (cycles), block size (bytes), 
# set associativity, write policy

# storage array
# [ [valid (0/1), dirty (0/1), data] ], data, data, ...]
# store newest data at the end, LRU is the front element and we will pop off

from Block import Block

class LevelCache:

    def __init__(self, size, latency, blockSize, setAssociativity, writePolicy):
        self.size = size # total capacity in bytes
        self.latency = latency # access latency in cycles
        self.blockSize = blockSize # block size in bytes
        self.setAssociativity = setAssociativity # set associativity in ways
        self.writePolicy = writePolicy # 0 = write-back, 1 = write-through
        self.lastLevel = True

        self.contents = [] # [ [ [block 1], [block 2], ... ] , [ [block 1], [block 2], ... ] ]
                           # block 1: [ valid , dirty , tag , data ]

        self.fillEmptyContents()

    def fillEmptyContents(self):
        layers = self.size // self.blockSize
        for i in range(layers):
            setArr = []
            for j in range(self.blockSize):
                block = Block(0, 0, 0, 0, j)
                setArr.append(block)

            self.contents.append(setArr)

    def write(self, address, dirty):
        # which block in a set is accessed
        blockOffset = address % self.blockSize

        # block address
        setIndex = ( address // self.blockSize ) % (self.size // self.blockSize)

        # 

    def read(self, address):
        # which block in a set is accessed
        blockOffset = address % self.blockSize

        # block address
        setIndex = ( address // self.blockSize ) % (self.size // self.blockSize)
       
        if not self.contents[setIndex][blockOffset].valid:
            block = Block(1, 0, tag, 1) # email about memory contents
            self.write(address, block)

    def printContents(self):
        for setObj in self.contents:
            for block in setObj:
                print('Block #' + str(block.blockNum) + ': ' + str(block.data))