import re
import itertools
import copy
import collections
import sys
from logging import warning, info, debug
import asmsize

divergent_colors = ["FF6666", "66FF66", "6666FF", "FFFF66", "FF66FF", "66FFFF"]

class BasicBlock(object):
    def __init__(self, address):
        self.instructions = []
        self.address = address
        self.destinations = []
    def addInstruction(self, insn):
        self.instructions.append(insn)
    def isEmpty(self):
        return len(self.instructions) == 0
    def isConstantPool(self):
        cp = True
        hasDot = False

        for insn in self.instructions:
            if not (insn.isNop() or insn.isDotWord()):
                cp = False
            if insn.isDotWord():
                hasDot = True

        return cp and hasDot

    def isContained(self, addr):
        for insn in self.instructions:
            if insn.address == addr:
                return True
        return False

    def countCalls(self):
        cnt = collections.Counter()

        for insn in self.instructions:
            if insn.isCall() or insn.markedAsCall:
                cnt[insn.branchDestination()] += 1
        return cnt

    def codeSize(self):
        tot = 0

        for i in self.instructions:
            tot += i.insnSize()

        return tot

    def cycleCount(self):
        tot = 0

        for i in self.instructions:
            tot += i.cycleCount()

        return tot

    def isStart(self, addr):
        return self.address == addr

    def dumpDot(self, stream=sys.stdout, headcolor=[], snipafter=100):
        def escape(s):
            s = str(s)
            s = s.replace('&', '&amp;')
            s = s.replace('<', '&lt;')
            s = s.replace('>', '&gt;')
            return s
        # if len(self.instructions) <= 2:
        #     label = "<br align='left'/>".join(map(escape, self.instructions))
        # elif self.getTailInsn().doDelaySlot():
        #     label = "<br align='left'/>".join(map(escape, [self.instructions[0], "... ({} insns)".format(len(self.instructions)-3), self.instructions[-2], self.instructions[-1]]))
        # else:
        #     label = "<br align='left'/>".join(map(escape, [self.instructions[0], "... ({} insns)".format(len(self.instructions)-2), self.instructions[-1]]))

        if len(self.instructions) > snipafter:
            label = "<br align='left'/>".join(map(escape, self.instructions[:snipafter/2] + ["...", str(len(self.instructions)-snipafter)+" more instructions", "..."] + self.instructions[-snipafter/2:]))
        else:
            label = "<br align='left'/>".join(map(escape, self.instructions))

        if headcolor != []:
            cols = map(lambda x: "<td bgcolor='{}'> </td>".format(x), headcolor[1:])

            head = "<tr><td bgcolor='{}' align='left' port='f0'>{}</td>".format(headcolor[0], self.address) + "".join(cols) + "</tr>"
        else:
            headcolor = [None]
            head = "<tr><td align='left' port='f0'>{}</td></tr>".format(self.address)

        if hasattr(self.instructions[0],"lineno"):
            head += "<tr><td align='left' colspan='{}'>Line: {}</td></tr>".format(len(headcolor), self.instructions[0].lineno)

        if hasattr(self,"iterations"):
            head += "<tr><td align='left' colspan='{}'>Iterations: {}</td></tr>".format(len(headcolor), self.iterations)

        if hasattr(self,"inram"):
            head += "<tr><td align='left' bgcolor='blue' colspan='{}'>BB IN RAM</td></tr>".format(len(headcolor))
        else:
            head += "<tr><td align='left' colspan='{}'>BB NOT IN RAM</td></tr>".format(len(headcolor))

        if hasattr(self,"instrumented"):
            head += "<tr><td align='left' bgcolor='green' colspan='{}'>BB INSTRUMENTED</td></tr>".format(len(headcolor))
        else:
            head += "<tr><td align='left' colspan='{}'>BB NOT INSTRUMENTED</td></tr>".format(len(headcolor))


        label = "<<table cellborder='1' cellspacing='0' border='0'>{}<tr align='left'><td colspan='{}' align='left'>{}</td></tr></table>>".format(head, len(headcolor), label)
        stream.write("{} [shape=none, label={}];\n".format(self.address,label))
        for d in self.destinations:
            stream.write("{} -> {}:f0".format(self.address, d.address))
            if self.getTailInsn().branchDestination() == d.address:
                stream.write(" [color=blue]")
            stream.write(";\n")

    # Get the last branch instruction that defines the jump
    # of the basic block. This function copes with delay slots
    def getTailInsn(self):
        if self.instructions[-1].isBranch():
            return self.instructions[-1]
        if len(self.instructions) >= 2 and self.instructions[-2].isBranch() and self.instructions[-2].doDelaySlot():
            return self.instructions[-2]
        return self.instructions[-1]

    def getLoopHeaders(self):
        lh = self.cfg.getLoopHeaders(self)
        if self in self.cfg.loop_headers:
            lh = [self] + lh
        return lh

    def __hash__(self):
        return self.address
    def __str__(self):
        return hex(self.address) + "\n    " + "\n    ".join(map(str,self.instructions))
    def __repr__(self):
        return hex(self.address)

class CFG(object):
    def __init__(self):
        self.startaddress = None
        self.loops = []
        self.loop_headers = []

    # def construct(self, instructions, extra_labels=[]):
    #     split_points = set()

    #     instructions = map(lambda x: x[1], sorted(instructions))

    #     for l in extra_labels:
    #         split_points.add((l, 0))

    #     # Find the points at which execution can jump from or to
    #     # We then split up the instructions based on this data
    #     # to form a list of basic blocks
    #     for insn in instructions:
    #         if insn.isBranch():
    #             if insn.doDelaySlot():
    #                 split_points.add((insn.address + insn.insnSize(), 1))
    #             split_points.add((insn.address, 1))
    #             d = insn.branchDestination()
    #             if d is not None:
    #                 split_points.add((d, 0))
    #         elif insn.isCall():
    #             d = insn.branchDestination()
    #             if d is not None:
    #                 split_points.add((d, 0))
    #         if insn.isDotWord():
    #             split_points.add((insn.address, 1))

    #     debug("Found split points:")
    #     s = ""
    #     for i, sp in enumerate(sorted(split_points)):
    #         s += "(" + hex(sp[0]) + ", " + str(sp[1]) + ") "
    #         if i % 5 == 4:
    #             debug("\t"+s)
    #             s = ""

    #     basicblocks = []
    #     bbmap = {}
    #     current_bb = None
    #     do_bds = False      # Branch delay slot

    #     for insn in instructions:
    #         if (insn.address, 0) in split_points and current_bb is not None and not do_bds:
    #             basicblocks.append(current_bb)
    #             current_bb = BasicBlock(insn.address)

    #         if current_bb == None:
    #             current_bb = BasicBlock(insn.address)
    #         current_bb.addInstruction(insn)

    #         if insn.doDelaySlot():
    #             do_bds = True
    #         else:
    #             do_bds = False

    #         if (insn.address, 1) in split_points and not do_bds:
    #             basicblocks.append(current_bb)
    #             current_bb = None

    #     if current_bb is not None:
    #         basicblocks.append(current_bb)

    #     # Remove basic blocks with only nops and .words in them (TODO better heuristic for constant pools)
    #     basicblocks = filter(lambda x: not x.isConstantPool(), basicblocks)

    #     for b in basicblocks:
    #         bbmap[b.address] = b

    #         debug(b)

    #     for i, b in enumerate(basicblocks):
    #         # TODO: rather than blindly pick the next basic block, we should pick the next address
    #         if not b.getTailInsn().isUnconditional() and i < len(basicblocks)-1:
    #             b.destinations.append(basicblocks[i+1])

    #         dest = b.getTailInsn().branchDestination()

    #         if dest is False or b.getTailInsn().isCall():
    #             continue
    #         if dest is None:
    #             # Indirect jump
    #             # b.destinations.append(None)
    #             pass
    #         else:
    #             if dest in bbmap:
    #                 b.destinations.append(bbmap[dest])

    #     self.basicblocks = basicblocks

    #     # Extra pass to cope with call instruction being abused as a local jump
    #     # Check in each partitioned cfg, whether the calls at the end of a BB are
    #     # in the same cfg or a different CFG. If the same CFG, assume it is being
    #     # used as a jump, not a call
    #     p_cfgs = self.partition()
    #     for cfg in p_cfgs:
    #         for bb in cfg.basicblocks:
    #             if bb.getTailInsn().isCall():
    #                 dest = bb.getTailInsn().branchDestination()
    #                 for bb2 in cfg.basicblocks:
    #                     if bb2.isContained(dest):
    #                         warning("Found contained call")
    #                         info("Contained call in BB: "+ hex(bb.address) + ", call to BB: "+ hex(bb2.address))
    #                         bb.destinations.remove(bb.destinations[0])
    #                         bb.destinations.append(bbmap[dest])
    #                         bb.getTailInsn().markNotCall()

    # This function creates basic blocks and links them together
    # from the instructions. The choice of entry point is important,
    # as the branches are found sequentially from this entry point
    def construct_new(self, instructions, fn_labels):
        label2insn = {}
        for i, insn in enumerate(instructions):
            if insn.label is not False:
                label2insn[insn.label] = i
            insn.address = i


        # Start constructing basic blocks by following branch targets.
        # Sequentially increment the instruction, and when we find a new
        # branch target, add it to the entry point list.

        # It is necessary to do this in two passes, so that we dont need
        # to split or merge basic blocks afterwards

        # Delay slots are handled by adding them to the list of processed
        # instructions, but not to the split points. When constructing
        # basic blocks later, the delay slot instruction is duplicated
        # and added to after the branch in the basic block. This is
        # Necessary because a basic block could start after the branch
        # but before the delay slot instruction.

        # Find entry point
        entry_points = set([])

        computed_functions = []
        for i in instructions:
            if i.isCall() and i.branchDestination() is not None:
                computed_functions.append(i.branchDestination())

        computed_functions += fn_labels

        for e in fn_labels + computed_functions:
            if e in label2insn:
                entry_points.add(label2insn[e])


        processed_entries = set()
        bb_starts = set()
        split_points = set()
        processed_insns = set()

        while len(entry_points) > 0:
            # current_address = entry_points.pop()
            current_address = min(entry_points)
            entry_points.remove(current_address)
            processed_entries.add(current_address)

            current_insns = []
            bb_start = current_address
            bb_starts.add(bb_start)
            split_points.add((bb_start, 0))

            if current_address is None:
                continue

            if current_address > len(instructions):
                warning("BB start@"+str(current_address)+" is not a valid instruction")
                continue

            debug("Starting BB@"+str(current_address))


            while True:
                insn = instructions[current_address]
                current_insns.append(insn)

                processed_insns.add(current_address)

                # Add call destination to entries, as a new basic block
                # should start from there
                if insn.isCall() and insn.branchDestination() not in label2insn:
                    info("Destination {} is not locatable (resolved at linktime?)".format(insn.branchDestination()))
                elif insn.isCall() and label2insn[insn.branchDestination()] not in processed_entries:
                    debug("\tFound call@{} to {} ()".format(current_address, insn.branchDestination(), label2insn[insn.branchDestination()]))
                    entry_points.add(label2insn[insn.branchDestination()])
                    if current_address+1 not in processed_entries:
                        entry_points.add(current_address + 1)

                if insn.isBranch():
                    # Add the current branch and destination as points to split on

                    if insn.branchDestination() is not None:
                        if insn.branchDestination() not in label2insn or insn.branchDestination() in fn_labels:
                            debug("\tCould not find branch destination@{}".format(current_address))
                        else:
                            e = (bb_start, label2insn[insn.branchDestination()])
                            split_points.add((label2insn[insn.branchDestination()], 0))

                            # Add branch destination as a new entry point for later processing
                            if label2insn[insn.branchDestination()] not in processed_entries:
                                entry_points.add(label2insn[insn.branchDestination()])
                                bd = label2insn[insn.branchDestination()]
                                debug("\tFound branch@{} to {}".format(current_address, bd))
                    else:
                        debug("\tFound indirect branch@{}".format(current_address))

                    if insn.isUnconditional():
                        debug("\tEnd BB@{}".format(current_address))
                        split_points.add((current_address, 1))
                        # If we are doing delay slots, add the insn after the branch
                        # to the list of processed instructions
                        if insn.doDelaySlot():
                            processed_insns.add(current_address+1)
                        break

                    # If the branch isnt unconditional, we add the following instruction as a
                    # start of a basic block
                    debug("\tFound fall through@{}".format(current_address))

                    # split_points.add((current_address + insn.insnSize(), 0))

                    # If we fall through, the next instruction is the beginning
                    # of the next basic block
                    if current_address+1 not in processed_entries:
                        entry_points.add(current_address + 1)

                    debug("\tEnd BB@{}".format(current_address))
                    split_points.add((current_address, 1))
                    if insn.doDelaySlot():
                        processed_insns.add(current_address+1)
                    break
                current_address += 1

        # Finish constructing BBs by considering target edges
        debug("Found split points:")
        s = ""
        for i, sp in enumerate(sorted(split_points)):
            if sp[0] is None:
                continue
            s += "(" + hex(sp[0]) + ", " + str(sp[1]) + ") "
            if i % 5 == 4:
                debug("\t"+s)
                s = ""

        basicblocks = []
        bbmap = {}
        current_bb = None
        do_bds = False      # Branch delay slot

        # From the 'split points' we have found, we can use this
        # to divide the instructions into basic blocks

        for insn_addr, insn in enumerate(instructions):
            if insn_addr not in processed_insns:
                continue
            debug("Insn:"+hex(insn_addr))
            if (insn.address, 0) in split_points and current_bb is not None and not do_bds:
                basicblocks.append(current_bb)
                current_bb = BasicBlock(insn.address)

            if current_bb == None:
                current_bb = BasicBlock(insn.address)
            current_bb.addInstruction(insn)

            if insn.doDelaySlot():
                do_bds = True
            else:
                do_bds = False

            if (insn.address, 1) in split_points and not do_bds:
                basicblocks.append(current_bb)
                current_bb = None

        if current_bb is not None:
            basicblocks.append(current_bb)

        # Create a map of start address to bb, so that we can
        # look up the relevant BB via a branch's destination
        for bb in basicblocks:
            bbmap[bb.address] = bb

        # This pass constructs all the links between the basic blocks, now that
        # every basic block should have been created
        for i, b in enumerate(basicblocks):
            # TODO: rather than blindly pick the next basic block, we should pick the next address
            debug("BB Start@"+hex(b.address))
            if not b.getTailInsn().isUnconditional() and i <= len(basicblocks)-1:
                b.destinations.append(basicblocks[i+1])
                debug("\tlink to "+hex(basicblocks[i+1].address))

            dest = b.getTailInsn().branchDestination()

            if dest is False or b.getTailInsn().isCall():
                debug("\tFall through")
                continue
            if dest is None:
                debug("\tindirect link")
                # Indirect jump
                # b.destinations.append(None)
                pass
            else:
                if dest in label2insn and dest not in fn_labels and label2insn[dest] in bbmap:
                    b.destinations.append(bbmap[label2insn[dest]])
                    debug("\tlink to "+hex(bbmap[label2insn[dest]].address))
                else:
                    print computed_functions
                    if dest in computed_functions:
                        warning("Standard branch \"{}\"@{} jumping to function:{}".format(str(b.getTailInsn()).strip(),b.address,dest))
                        b.getTailInsn().markAsCall()
                    else:
                        warning("BB@{} has link to unknown BB@{}".format(b.address, dest))

        self.basicblocks = basicblocks

        # Extra pass to cope with call instruction being abused as a local jump
        # Check in each partitioned cfg, whether the calls at the end of a BB are
        # in the same cfg or a different CFG. If the same CFG, assume it is being
        # used as a jump, not a call
        p_cfgs = self.partition()
        for cfg in p_cfgs:
            for bb in cfg.basicblocks:
                if bb.getTailInsn().isCall():
                    dest = bb.getTailInsn().branchDestination()
                    for bb2 in cfg.basicblocks:
                        if bb2.isContained(dest):
                            warning("Found contained call")
                            info("Contained call in BB: "+ hex(bb.address) + ", call to BB: "+ hex(bb2.address))
                            bb.destinations.remove(bb.destinations[0])
                            bb.destinations.append(bbmap[dest])
                            bb.getTailInsn().markNotCall()

    # Return a map of basic blocks to call destinations
    def findCalls(self):
        calls = set()
        for bb in self.basicblocks:
            for insn in bb.instructions:
                if insn.isCall() and insn.branchDestination() is not None:
                    calls.add(insn.branchDestination())
        return calls

    # Parition the CFG into non-connected CFGs
    def partition(self):
        cfgs = []
        bblist = copy.copy(self.basicblocks)

        entry_points = self.findCalls()

        while len(bblist) > 0:
            c = CFG()

            bbsublist = []


            bbsublist = [bblist[0]]

            # Go through the list
            #   If a destination isn't in the list, but the main block is, add it
            #   If the main block isnt in the list, but the destination is, add it
            #   Repeat until unchanged
            while True:
                changed = False
                for bb in bblist:
                    for d in bb.destinations:
                        if d in bbsublist:
                            if bb not in bbsublist:
                                bbsublist.append(bb)
                                changed = True
                        if bb in bbsublist:
                            if d not in bbsublist:
                                bbsublist.append(d)
                                changed = True
                if not changed:
                    break

            # Remove the selected blocks
            for bb in bbsublist:
                bblist.remove(bb)

            c.basicblocks = bbsublist
            starts = findStartingBlocks(c.basicblocks)

            # Add extra start blocks from the found destinations of function calls
            for bb in c.basicblocks:
                if bb.address in entry_points and bb not in starts:
                    starts.append(bb)

            if len(starts) > 1:
                debug("more than 1 possible starting block")
                debug(str(starts))

            if len(starts) == 0:
                warning("Warning: cannot find starting block")
                starts = c.basicblocks

            c.startaddress = map(lambda x: x.address, starts)
            cfgs.append(c)

        return cfgs

    # Return a list of unique paths through a loop. Each path is a list of
    # basic blocks and either escapes the loop or returns to the loop
    # header
    def loopPaths(self, loop_header):

        def createPath(cur_bb, p, first = False, n=0):
            if (loop_header not in self.getLoopHeaders(cur_bb) or cur_bb == loop_header) and not first:
                # print hex(cur_bb.address), self.getLoopHeaders(cur_bb)
                return [p]
            ps = []
            found_dest = False
            for d in cur_bb.destinations:
                if d not in p:
                    # print " |  "*n,hex(d.address)
                    ps += createPath(d, p + [cur_bb], n=n+1)
                    found_dest = True

            if not found_dest:
                ps += [p+[cur_bb]]

            if len(cur_bb.destinations) == 0:
                return [p + [cur_bb]]
            return ps

        paths = createPath(loop_header, [], True)
        for p in paths:
            print p
            # for bb in p:
            #     print hex(bb.address),
            # print ""

    def dumpDot(self, stream=sys.stdout):
        stream.write("digraph D {\n")

        for bb in self.basicblocks:
            drawn = False

            lh = self.getLoopHeaders(bb)

            if bb in self.loop_headers:
                lh = [bb] + lh

            if lh == []:
                bb.dumpDot(stream)
            else:
                cols = []

                for header in lh:
                    if header in self.loop_headers:
                        i = self.loop_headers.index(header)
                        cols.append('#'+divergent_colors[i%len(divergent_colors)])
                bb.dumpDot(stream, headcolor=cols)

        stream.write("}\n")

    def findLoops(self):
        start_bbs = filter(lambda x: x.address in self.startaddress, self.basicblocks)

        # Maybe this should be transformed into an iterative algorithm, so we dont have to
        # play around with the recursion depth
        rec_limit = max(1500,len(self.basicblocks)*2)
        debug("Set recursion limit to " + str(rec_limit))
        sys.setrecursionlimit(rec_limit)

        for sb in start_bbs:
            self.traverseLoops(sb)

        loop_headers = set()

        for bb in self.basicblocks:
            if bb.iloop_header is not None:
                loop_headers.add(bb.iloop_header)

        self.loop_headers = list(loop_headers)

        # print "Loop headers:"
        # for lh in self.loop_headers:
        #     print "\t", hex(lh.address)


    def getLoopHeaders(self, node):
        lh = []
        try:
            while node.iloop_header is not None:
                if node == node.iloop_header:
                    if hasattr(node, "iloop_header2"):
                        lh.append(node.iloop_header2)
                        node = node.iloop_header2
                        continue
                    else:
                        break
                lh.append(node.iloop_header)
                node = node.iloop_header
        except AttributeError:
            pass
        return lh

    # Implementation of Tao Wei et al. 2012, starts here ##########################
    def traverseLoops(self, root):
        for bb in self.basicblocks:
            bb.traversed = False
            bb.iloop_header = None
            bb.dfsp_pos = 0
        self.traverseLoopDFS(root,1)
        for bb in self.basicblocks:
            if bb in bb.destinations:
                if bb.iloop_header is not None:
                    bb.iloop_header2 = bb.iloop_header
                    bb.iloop_header = bb
                else:
                    bb.iloop_header = bb

    def tag_lhead(self, b, h):
        if h == b or h is None:
            return

        cur1 = b
        cur2 = h

        while cur1.iloop_header is not None:
            ih = cur1.iloop_header
            if ih == cur2:
                return
            if ih.dfsp_pos < cur2.dfsp_pos:
                cur1.iloop_header = cur2
                cur1 = cur2
                cur2 = ih
            else:
                cur1 = ih
        cur1.iloop_header = cur2

    def traverseLoopDFS(self, b0, dfsp_pos):
        b0.traversed = True
        b0.dfsp_pos = dfsp_pos
        for b in b0.destinations:
            if not b.traversed:
                nh = self.traverseLoopDFS(b, dfsp_pos + 1)
                self.tag_lhead(b0, nh)
            else:
                if b.dfsp_pos > 0:
                    self.tag_lhead(b0, b)
                elif b.iloop_header is None:
                    pass
                else:
                    h = b.iloop_header
                    if h.dfsp_pos > 0:
                        self.tag_lhead(b0, h)
                    else:
                        warning("Irreducible CFG")
                        pass
                        # print b, "is reentry"
                        # print "Irreducible CFG"
                        # print "TODO"
        b0.dfsp_pos = 0
        return b0.iloop_header

    # Implementation of Tao Wei et al. 2012, ends here ##########################

# Finds a block which is not jumped to by another block
def findStartingBlocks(basicblocks):
    bbmap = {b: True for b in basicblocks}

    for bb in basicblocks:
        for d in bb.destinations:
            bbmap[d] = False

    return list(itertools.compress(*zip(*bbmap.items())))
