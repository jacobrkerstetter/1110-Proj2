import random

class Block:
    def __init__(self, valid, dirty, tag, blockSize):
        self.valid = valid
        self.dirty = dirty
        self.tag = tag

        self.data = []
        self.blockSize = blockSize
        self.timeAccessed = 0


    def writeValue(self, data):
        # actually fill it not random
        self.data = data