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
    mistakeDefinitionsForComments=['Inaccuracy', 'Mistake', 'Blunder']
    mistakeDefinitionsForNags=['??', '!?', '?!', '?'] 

    def __init__(self, path, player):
        self.pgnFilePath=path
        self.playerUserName=player

    def buildGameFromFile(self):
        with open(self.pgnFilePath, 'r') as pgnFile:
            self.readGameInfo(pgnFile)
            self.findColorOfUser()
            pgnFile.seek(0)
            self.moves=chess.pgn.read_game(pgnFile, Visitor=ChessGameVisitor)
            self.findMistakesOfPlayer()

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
                if 'black' in line.lower():
                    self.playerColor = 'Black'
                elif 'white' in line.lower():
                    self.playerColor = 'White'

    def isGameLine(self, line):
        return line[0] == '1'

    def findMistakesOfPlayer(self):
        comments=''
        playerMoves=self.getMovesOfColor(self.playerColor)
        for move in playerMoves:
            if self.isMistake(move.getComment(), move.getNag()):
                self.mistakes.append(move)

    def getMovesOfColor(self, color):
        moves=[]
        for movePair in self.moves:
            if color == 'White':
                moves.append(movePair.getWhiteMove())
            elif color == 'Black':
                moves.append(movePair.getBlackMove())
            else:
                moves.append(movePair.getWhiteMove())
                moves.append(movePair.getBlackMove())
        return moves
            
    def isMistake(self, comment, nag=''):
        return (self.isMistakeFromComments(comment) or self.isMistakeFromNag(nag))

    def isMistakeFromComments(self, comment):
        for mistake in self.mistakeDefinitionsForComments:
            if mistake in comment:
                return True
        return False

    def isMistakeFromNag(self, nag):
        for mistake in self.mistakeDefinitionsForNags:
            if mistake == nag:
                return True
        return False

    def printMistakes(self):
        for m in self.mistakes:
            m.printMove()

    def returnGameWithAnalysisOnlyForPlayer(self):
        game=''.join(self.info)
        game+=self.getGameWithoutOpponentsAnalysis()
        return game

    def getGameWithoutOpponentsAnalysis(self):
        game=''
        for i in range(len(self.moves)):
            game+=self.parseMoveForPlayer(self.playerColor, self.moves[i], i+1)
        game+='\n'
        return game

    def parseMoveForPlayer(self, color, move, moveNumber):
        moveStr=str(moveNumber) + '. '
        if color == 'White':
            moveStr+=move.getWhiteMoveWithComment() + ' ' + move.getBlackMoveToStr(time=True) + ' '
        elif color == 'Black':
            moveStr+=move.getWhiteMoveToStr(time=True) + ' ' + move.getBlackMoveWithComment() + ' '
        else:
            moveStr=move.getWholeMove() + ' '
        return moveStr
