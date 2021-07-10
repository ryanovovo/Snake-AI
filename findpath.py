from SnakeEnv import SnakeEnv

class Node:
    def __init__(self, parent, pos):
        self.parent = parent
        self.pos = pos
        self.level = int
        self.childs = []


class Search:
    def __init__(self, start):
        self.end = False
        self.start = start
        start = [start[0]-1, start[1]-1]
        rightNear = self.findNeighbors(start)
        root = Node(None, start)
        root.level = 1
        self.treeGrow(rightNear, root)
        self.go(finalPath)

    def findNeighbors(self, ori):
        neighborlist = []
        x = ori[0];
        y = ori[1];
        if ((x - 1) >= 0 and (x - 1) < size):
            neighborlist.append([x - 1,y])
        if ((y - 1) >= 0 and (y - 1) < size):
            neighborlist.append([x, y - 1])
        if ((x + 1) < size):
            neighborlist.append([x + 1, y])
        if ((y + 1) < size):
            neighborlist.append([x, y + 1])

        return neighborlist

    def treeGrow(self, rightNear, node):
        if self.end:
            return 0
        childPos = self.findNextMove(node)
        if len(childPos) > 0:
            childNodes = []
            for i in range(0,len(childPos)):
                child = childPos[i]
                childNode = Node(node, child)
                childNode.level = node.level + 1
                childNodes.append(childNode)
                self.treeGrow(rightNear, childNode)
            node.childs = childNodes
        else:
            if node.level == size*size:
                lastPos = node.pos
                lastPosString = str(lastPos[0])+","+str(lastPos[1])
                for j in range(0, len(rightNear)):
                    near = rightNear[j]
                    nearPos = str(near[0])+","+str(near[1])
                    if lastPosString == nearPos:
                        global finalPath
                        finalPath = self.dumpTree(node)
                        self.end = True
                        return 0


    def dumpTree(self, node):
        pathList = []
        self.checkTreePathPos(pathList, node)
        return pathList


    def findNextMove(self, node):
        neighbors = []
        pathList = []
        self.checkTreePathPos(pathList, node)
        neighborList = self.findNeighbors(node.pos)
        for i in range(0, len(neighborList)):
            near = neighborList[i]
            pos = str(near[0])+","+str(near[1])
            noteExist = False
            for j in range(0, len(pathList)):
                path = pathList[j]
                pathString = str(path[0])+","+str(path[1])
                if pathString == pos:
                    noteExist = True
                    break
            if noteExist == False:
                neighbors.append(near)
        return neighbors


    def checkTreePathPos(self, pathList, node):

        pathList.append(node.pos)
        if node.parent != None:
            self.checkTreePathPos(pathList, node.parent)

    def go(self,pathList):
        temp = pathList[len(pathList) - 1]
        for j in range(0, len(pathList)-1):
            j = len(pathList) - 1 - j
            pathList[j] = pathList[j-1]
        pathList[0] = temp
        print(pathList)
        while True:
            for i in range(0, len(pathList)):
                env.render()
                if i == len(pathList)-1:
                    this = pathList[i]
                    next = pathList[0]
                else:
                    this = pathList[i]
                    next = pathList[i + 1]
                if (this[0] > next[0]):
                    env.change_snake_dir([0, 0, 1, 0])
                if (this[0] < next[0]):
                    env.change_snake_dir([0, 0, 0, 1])
                if (this[1] > next[1]):
                    env.change_snake_dir([1, 0, 0, 0])
                if (this[1] < next[1]):
                    env.change_snake_dir([0, 1, 0, 0])
                if env.step() == -1:
                    env.reset()


# main
size = 4
path = []
env = SnakeEnv(game_board_size=size+2, gui=True)
print(env.snake_pos[0])
Search(env.snake_pos[0])


