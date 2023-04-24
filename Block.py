class Block:
    def __init__(self, valid, dirty, tag, data):
        self.valid = valid
        self.dirty = dirty
        self.tag = tag
        self.data = data
        self.timeAccessed = 0