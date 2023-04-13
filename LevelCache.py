# each level of the cache
# size (bytes), latency (cycles), block size (bytes), 
# set associativity, write policy

# storage array
# [ [valid (0/1), dirty (0/1), data] ], data, data, ...]
# store newest data at the end, LRU is the front element and we will pop off

class LevelCache:

    def __init__(self, size, latency, blockSize, setAssociativity, writePolicy):
        self.size = size # total capacity in bytes
        self.latency = latency # access latency in cycles
        self.blockSize = blockSize # block size in bytes
        self.setAssociativity = setAssociativity # set associativity in ways
        self.writePolicy = writePolicy # 0 = write-back, 1 = write-through

        self.contents = [] # [ set 1 , set 2 , set 3 , set 4 ]
                           # [ [ [block 1], [block 2], ... ] , [ [block 1], [block 2], ... ] ]
                           # block 1: [ valid , dirty , tag , data ]

    def fillEmptyContents(self):
        return

    def write(self, block):
        return

    def read(self, address):
        # which block in a set is accessed
        blockOffset = address % self.blockSize

        # block address
        setIndex = ( address // self.blockSize ) % self.setAssociativity
       
        print([blockOffset, setIndex])