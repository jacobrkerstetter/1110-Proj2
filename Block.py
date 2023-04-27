import random

class Block:
    def __init__(self, valid, dirty, tag, data, blockSize):
        self.valid = valid
        self.dirty = dirty
        self.tag = tag

        self.data = []
        for i in range(blockSize):
            self.data.append(random.randint(0, 255))
        self.blockSize = blockSize
        self.timeAccessed = 0