
class AsmInstruction(object):
    def __init__(self, asm, lineno=None):
        self.operator = None
        self.operands = None
        self.markedNotCall = False
        self.markedAsCall = False
        self.lineno = lineno
        self.label = False
        self.processLine(asm)
    def processLine(self, l):
        pass
    def isBranch(self):
        return False
    def isUnconditional(self):
        return False
    def isCall(self):
        return False
    def isNop(self):
        return False
    def isDotWord(self):
        return False
    def branchDestination(self):
            return None
    def markNotCall(self):
        self.markedNotCall = True

    def __str__(self):
        if self.label is not False:
            return self.label + ":"
        if self.markedNotCall:
            s = "    * "
        else:
            s = "    "
        return str(s + self.operator + " " + self.operands)
    def __repr__(self):
        return str(self)

    @staticmethod
    def loadInstructions(fname):
        return []
