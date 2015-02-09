import re, string
from asminstruction import AsmInstruction
from logging import warning, info, debug
import asmsize

label_regex     = r'^([a-f0-9]{8})\s<([^>]+)>:'
instr_regex     = r'^\s*(?P<address>[a-f0-9]+):\s+(?P<size>([a-f0-9]+[ ]?)+)\s+(?P<insn>.+)'

disassembler    = "arm-none-eabi-objdump"

class ArmAsmInstruction(AsmInstruction):
    def __init__(self, asm, lineno):
        super(ArmAsmInstruction, self).__init__(asm, lineno)
    def processLine(self, l):
        parts = l.split(':')
        parts[0] = parts[0].strip()
        # If len == 3, then we often have :lower16: type directives
        if len(parts) == 2 and " " not in parts[0] and '\t' not in parts[0]:
            if parts[1].strip() != "":
                print parts[0]
                print "Stuff after label? '{}'".format(parts[1])
            self.label = parts[0].strip()
            self.operator=""
            self.operands=""
        else:
            if l.strip()[0] in ['.', '@']: # Dont care about directives
                return
            sregex = r'([a-zA-Z0-9.]+)\s*([^;]*)'

            m = re.match(sregex, l.strip())
            if m is None:
                print "Unmatched: "+l.strip()
                return

            self.operator = m.group(1).lower()
            # self.operator = self.operator.split('.')[0]
            self.operands = m.group(2).strip()
    def isLabel(self):
        return self.label is False
    def isBranch(self):
        if self.operator in ["b", "bx", "beq", "bne", "bcs", "bcc", "bhs", "blo", "bmi", "bpl", "bvs", "bvc", "bhi", "bls", "bge", "blt", "bgt", "ble", "cbnz", "cbz"]:
            return True
        if self.operator[:3] == "pop" or self.operator[:5] == "ldmia":
            if "pc" in self.operands:
                return True
        if self.operator == "mov" or self.operator == "ldr":
            if self.operands[:2] == "pc":
                return True
        if self.operator == "tbh" and self.operands[1:3] == "pc":
            return True
        return False
    def isLoad(self):
        if self.operator in ["ldr", "pop", "ldm", "ldmia"]:
            return True
        return False
    def isStore(self):
        if self.operator in ["str", "push", "stm", "stmia"]:
            return True
        return False
    def isUnconditional(self):
        if not self.isBranch():
            return False
        if self.operator in ["b", "bx"]:
            return True
        if self.operator == "pop" or self.operator[:5] == "ldmia":
            if "pc" in self.operands:
                return True
        if self.operator == "mov" or self.operator == "ldr":
            if self.operands[:2] == "pc":
                return True
        if self.operator == "tbh" and self.operands[1:3] == "pc":
            return True
        return False
    def isCall(self):
        if self.operator in ["bl", "blx"] and not self.markedNotCall:
            return True
        return False
    def isNop(self):
        if self.operator in ["nop"]:
            return True
        return False
    def isDotWord(self):
        return self.operator in [".word"]
    def branchDestination(self):
        if not self.isBranch() and not self.isCall():
            return False

        if self.operator in ["cbnz", "cbz"]:
            d = self.operands.split(',')
            return d[1].strip()


        d = self.operands.strip()
        if d == "":
            return None
        if self.operator[:3] == "pop" or self.operator[:5] == "ldmia":
            return None
        if self.operator == "mov" or self.operator == "ldr" or self.operator == "bx":
            return None
        # if self.operator == "tbh" and self.operands[1:3] == "pc":
            # return None

        return d
    def markNotCall(self):
        self.markedNotCall = True
    def markAsCall(self):
        self.markedAsCall = True
    def doDelaySlot(self):
        return False
    def stripConditional(self):
        op = self.operator
        for suffix in ["gt", "le", "lt", "ne", "ge", "eq", "ls", "hi", "cc", "cs", "mi", "pl"]: # TODO MORE
            if suffix == self.operator[-2:] and len(self.operator)>4:
                op = self.operator[:-2]
        return op
    def insnSize(self):
        dest = None
        if self.isBranch():
            dest = self.branchDestination()

        op = self.stripConditional()
        insn = op + " " + self.operands

        if (op == "ldr" or op == "adr") and '[' not in self.operands and '=' not in self.operands:
            parts = self.operands.split(',')
            dest = parts[1]
            if "+" in dest:
                dest = dest[:dest.index('+')]
            if "-" in dest:
                dest = dest[:dest.index('-')]

        self.insnsize = asmsize.findSize(insn, b_dest=dest)

        return self.insnsize

    def cycleCount(self):
        two_bytes_one_cycle =  ["adc", "add", "and", "asr", "bic", "cmn", "cmp", "cpy",
                                "eor", "lsl", "lsr", "mov", "mul", "mvn", "neg", "orr",
                                "ror", "sbc", "sub", "tst", "rev", "revh", "revsh",
                                "sxtb", "sxth", "uxtb", "uxth", "mul", "nop",

                                "adds", "movs", "subs", "lsls", "asrs", "orrs", "lsrs",
                                "eors", "mvns", "muls", "ands", "negs",

                                "it", "ite", "itt", "ittt", "itttt",
                                ]
        two_bytes_one_flush =   [
                                "b", "bl", "bx", "blx",

                                "beq", "bne", "ble", "bgt", "bge", "blt", "bcc", "bcs", "bmi",
                                "bpl", "bvs", "bhi", "bls",

                                "cbz", "cbnz"
                                ]

        two_bytes_two_cycles =  ["ldr", "ldrb", "ldrh", "ldrsb", "ldrsh", "str", "strb",
                                "strh",

                                "adr"]

        four_bytes_one_cycle =  ["adcs", "adds", "cmn", "rsbs", "sbcs", "subs", "cmp",
                                "ands", "tst", "bics", "eors", "teq", "orrs", "movs",
                                "orns", "mvns", "adc", "add", "cmn", "rsb", "sbc",
                                "sub", "and", "bic", "eor", "orr", "mov", "orn", "mvn", "nop",
                                "negs",

                                "movw", "movt", "addw", "subw", "movw", "mov",

                                "bfi", "bfc", "ubfx", "sbfx",

                                "asrs", "lsls", "lsrs", "rors", "rrxs",
                                "asr", "lsl", "lsr", "ror", "rrx",

                                "rev", "revh", "revsh", "rbit", "clz", "sxtb", "sxth", "uxtb", "uxth",

                                "mul", "mla", "mls", "mul",
                                ]

        four_bytes_one_flush  = [
                                "bl", "b",

                                "beq", "bne"
                                ]

        four_bytes_two_cycles=   ["mla", "mls",

                                "ldr", "ldrb", "ldrsb", "ldrh", "ldrsh", "str", "strb", "strh",

                                "ldrd", "strd",

                                "adr",
                                ]

        four_bytes_three_cycles = ["umull", "smull", "umlal", "smlal"]


        # TODO if pc is dest, add pipeline flush
        pflush = 2
        do_flush = False
        cyc = 0

        if self.insnSize() == 2:
            if self.stripConditional() in two_bytes_one_cycle:
                cyc = 1
            elif self.stripConditional() in two_bytes_one_flush:
                cyc = 1
                do_flush = True
            elif self.stripConditional() in two_bytes_two_cycles:
                cyc =  2
            elif self.stripConditional() in ["ldmia", "stmia"]:
                cyc =  1 + self.operands.count(',')
            elif self.stripConditional() in ["push", "pop"]:
                cyc =  1 + self.operands.count(',')+1
            else:
                raise RuntimeError("Unknown cycle count for "+ str(self.operator))
            # ldm stm push pop
        elif self.insnSize() == 4:
            if self.stripConditional() in four_bytes_one_cycle:
                cyc = 1
            elif self.stripConditional() in four_bytes_one_flush:
                cyc = 1
                do_flush = True
            elif self.stripConditional() in four_bytes_two_cycles:
                cyc = 2
            elif self.stripConditional() in four_bytes_three_cycles:
                cyc = 3
            elif self.stripConditional() in ["ldm", "stm", "stmia", "ldmia"]:
                cyc =  1 + self.operands.count(',')
            elif self.stripConditional() in ["push", "pop"]:
                cyc =  1 + self.operands.count(',')+1
            elif self.stripConditional() in ["sdiv", "udiv"]:
                cyc = 6
            else:
                print self
                raise RuntimeError("Unknown cycle count for "+ str(self.operator))
        else:
            return 0

        if do_flush:
            cyc += pflush

        return cyc


def loadInstructions(fname):
    lines = open(fname).readlines()

    instructions = []
    functions = []

    for lineno, l in enumerate(lines):
        insn = ArmAsmInstruction(l, lineno)

        if (insn.operator != "" and insn.operator is not None) or insn.label is not False:
            instructions.append(insn)
            debug("Instruction:"+str(insn))

        if "%function" in l:
            m = re.match(r"\s*\.type\s+([^,]+),\s*%function", l)
            functions.append(m.group(1))

        if ".cfi" in l or ".size" in l or ".loc" in l:
            lines[lineno] = ""

    return instructions, lines, functions

