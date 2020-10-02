import chess.pgn
from chessmove import ChessMove
from chessgamevisitor import ChessGameVisitor

class ChessGameFromPGN:
    info=[]
    moves=[]
    mistakes=[]
    playerUserName=''
    playerColor=''
    pgnFilePath=''
    mistakeDefinitions=['Inaccuracy', 'Mistake', 'Blunder'] 

    def __init__(self, path, player):
        self.pgnFilePath=path
        self.playerUserName=player

    def buildGameFromFile(self):
        with open(self.pgnFilePath, 'r') as pgnFile:
            self.readGameInfo(pgnFile)
            self.findColorOfUser()
            pgnFile.seek(0)
            self.moves=chess.pgn.read_game(pgnFile, Visitor=ChessGameVisitor)
            #self.findMistakes()

    def readGameInfo(self, pgnFile):
        for line in pgnFile:
            if not self.isGameLine(line):
                self.addInfoLine(line)

    def addInfoLine(self, line):
        self.info.append(line)

    def addMove(self, move):
        self.moves.append(move)

    def addComment(self, comment):
        self.comments.append(comment)

    def removeLastCommentandReturn(self):
        return self.comments.pop()

    def findColorOfUser(self):
        for line in self.info:
            if self.playerUserName in line:
                if "Black" in line:
                    self.playerColor = "Black"
                else:
                    self.playerColor = "White"
                if self.playerColor == '':
                    raise Exception('User: '+user+' is not part of the game')
                return

    def isGameLine(self, line):
        return line[0] == '1'

    def findMistakes(self):
        for i, move in enumerate(self.moves):
            if self.playerToMove(i) and self.isMistake(self.comments[i]):
                self.mistakes.append((move, self.comments[i]))

    def playerToMove(self, index):
        return (self.playerColor == 'White' and index%2==1) or (self.playerColor == 'Black' and index%2==0)

    def isMistake(self, comment):
        for mistake in self.mistakeDefinitions:
            if mistake in comment:
                return True
        return False

    def printMistakes(self):
        for m in self.mistakes:
            print(m[0], m[1])

    def returnGameWithAnalysisOnlyForPlayer(self):
        game=''.join(self.info)
        game+=self.getGameWithoutOpponentsAnalysis()
        return game

    def getGameWithoutOpponentsAnalysis(self):
        game=''
        for i in range(len(self.moves)):
            game+=str(i+1) +  '. ' +self.moves[i].getWholeMove()
            """
            if  self.playerColor == 'White':
                game+=str(i+1) + '. ' + self.moves[i].getWhiteMoveWithComment() + ' ' + self.moves[i].getBlackMove() + ' '
            elif self.playerColor == 'Black':
                game+=str(i+1) + '. ' + self.moves[i].getWhiteMove()+ ' ' + self.moves[i].getBlackMoveWithComment()  
            else:
                game+=str(i+1) + '. ' + self.moves[i].getWholeMove()
                """
        game+='\n'
        return game
