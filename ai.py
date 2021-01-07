import chess
import copy

pieceVal = { 'P': 100, 'N': 280, 'B': 320, 'R': 479, 'Q': 929, 'K': 60000 }

valMap = {'P' : [0,0,0,0,0,0,0,0,
               -31,8,-7,-37,-36,-14,3,-31,
               -22,9,5,-11,-10,-2,3,-19,
               -26,3,10,9,6,1,0,-23,
               -17,16,-2,15,14,0,15,-13,
               7,29,21,44,40,31,44,7,
               78,83,86,73,102,82,85,90,
               0,0,0,0,0,0,0,0],

        'N' : [-74,-23,-26,-24,-19,-35,-22,-69,
               -23,-15,2,0,2,0,-23,-20,
               -18,10,13,22,18,15,11,-14,
               -1,5,31,21,22,35,2,0,
               24,24,45,37,33,41,25,17,
               10,67,1,74,73,27,62,-2,
               -3,-6,100,-36,4,62,-4,-14,
               -66,-53,-75,-75,-10,-55,-58,-70],

        'B' : [-7,2,-15,-12,-14,-15,-10,-10,
               19,20,11,6,7,6,20,16,
               14,25,24,15,8,25,20,15,
               13,10,17,23,17,16,0,7,
               25,17,20,34,26,25,15,10,
               -9,39,-32,41,52,-10,28,-14,
               -11,20,35,-42,-39,31,2,-22,
               -59,-78,-82,-76,-23,-107,-37,-50],

        'R' : [-30,-24,-18,5,-2,-18,-31,-32,
               -53,-38,-31,-26,-29,-43,-44,-53,
               -42,-28,-42,-25,-25,-35,-26,-46,
               -28,-35,-16,-21, -13,-29,-46,-30,
               0,5,16,13,18,-4,-9,-6,19,35,28,33,
               45,27,25,15,55,29,56,67,55,62,34,
               60,35,29,33,4,37,33,56,50],

        'Q' : [-39,-30,-31,-13,-31,-36,-34,
               -42,-36,-18,0,-19,-15,-15,-21,
               -38,-30,-6,-13,-11,-16,-11,-16,
               -27,-14,-15,-2,-5,-1,-10,-20,-22,
               1,-16,22,17,25,20,-13,-6,-2,43,
               32,60,72,63,43,2,14,32,60,-10,20,
               76,57,24,6,1,-8,-104,69,24,88,26],

        'K' : [17,30,-3,-14,6,-1,40,18,
               -4,3,-14,-50,-57,-18,13,
               4,-47,-42,-43,-79,-64,-32,
               -29,-32,-55,-43,-52,-28,-51,
               -47,-8,-50,-55,50,11,-4,-19,
               13,0,-49,-62,12,-57,44,-67,28,
               37,-31,-32,10,55,56,56,55,10,
               3,4,54,47,-99,-99,60,83,-62]
}


class Node:
    def __init__(self,boardState):
        self.boardState = boardState
        self.children = []
        self.parent = None
        self.score = None
        self.move = None

class AI:

    def __init__(self,depth=4):
        self.depth = depth

    def minimax(self,boardState):
        self.root=Node(boardState)
        print('t')
        self.genTree()
        print('l')
        leafs = self.getLeafNodes()
        print('e')
        self.evalNodes(leafs)
        print('g')
        return(self.getmove())

    def genTree(self):
        curdepth = 0
        if(curdepth == self.depth):
            return
        else:
            return(self._genTree(self.root, curdepth))

    def _genTree(self, currentNode, curdepth):
        if(curdepth==self.depth):
            return
        else:
            for move in currentNode.boardState.legal_moves:
                newboard = copy.deepcopy(currentNode.boardState)
                newboard.push(move)
                newNode = Node(newboard)
                newNode.move = move
                newNode.parent = currentNode
                currentNode.children.append(newNode)
                self._genTree(newNode, curdepth+1)

    def printTree(self):
        if(self.currentNode==None):
            return
        else:
            self._printTree(self.currentNode)

    def _printTree(self, currentNode):
        print(currentNode.boardState)
        if(currentNode.children == []):
            return
        else:
            for child in currentNode.children:
                self._printTree(child)

    def getValState(self, color:bool, boardstate) -> int:
        #returns the value of pieces on board
        #True is white, False is Black
        val = 0
        for i in range(64):
            if(boardstate.color_at(i)==color):
                piece = str(boardstate.piece_at(i)).capitalize()
                piecevalue = pieceVal[piece]
                if(color==True):
                    val = (val + piecevalue) - valMap[piece][i]
                else:
                    #rotates valMap
                    val = (val + piecevalue) - valMap[piece][63-i]
        return(val)



    def getLeafNodes(self):
        leafs = []

        def _getLeafNodes(currentNode):
            if(len(currentNode.children)==0):
                leafs.append(currentNode)
            else:
                for child in currentNode.children:
                    _getLeafNodes(child)

        _getLeafNodes(self.root)
        return(leafs)


    def evalNodes(self, leafs):
        depth=1
        for leaf in leafs:
            leaf.score = self.evaluate(leaf.boardState)
        self._backprop(leafs, depth)

    def _backprop(self,nodes,depth):
        parents = []
        for node in nodes:
            if(node.parent==None):
                return
            else:
                if(node.parent.score==None):
                    node.parent.score = node.score
                    parents.append(node.parent)
                else:
                    #minimax
                    if(depth%2==0):
                        if(node.score>node.parent.score):
                            node.parent.score=node.score
                    else:
                        if(node.score<node.parent.score):
                            node.parent.score=node.score
        self._backprop(parents, depth+1)

    def getmove(self):
        bestPath = -100000
        for child in self.root.children:
            if(child.score>bestPath):
                bestmove = child.move
                bestPath = child.score
        return(bestmove)

    def evaluate(self, boardstate) -> int:
        #returns Blacks Evaluation for boardstate
        whitePieceVals = self.getValState(True, boardstate)
        blackPieceVals = self.getValState(False, boardstate)
        return(blackPieceVals-whitePieceVals)