import chess.pgn
from chessmove import ChessMove
from chessmove import Color
from chessgamevisitor import ChessGameVisitor

class ChessGameFromPGN:
    info=[]
    moves=[]
    pgnFilePath=''
    mistakeDefinitionsForComments=['Inaccuracy', 'Mistake', 'Blunder']
    mistakeDefinitionsForNags=['??', '!?', '?!', '?'] 

    def __init__(self, path):
        self.pgnFilePath=path

    def buildGameFromFile(self):
        with open(self.pgnFilePath, 'r') as pgnFile:
            self.readGameInfo(pgnFile)
            pgnFile.seek(0)
            self.moves=chess.pgn.read_game(pgnFile, Visitor=ChessGameVisitor)

    def readGameInfo(self, pgnFile):
        for line in pgnFile:
            if not self.isGameLine(line):
                self.addInfoLine(line)

    def addInfoLine(self, line):
        self.info.append(line)

    def findColorOfPlayer(self, playerUserName=''):
        for line in self.info:
            if playerUserName in line:
                if 'black' in line.lower():
                    return Color.Black
                elif 'white' in line.lower():
                    return Color.White
                else:
                    return Color.Unknown

    def isGameLine(self, line):
        return line[0] == '1'

    def findMistakesOfPlayer(self, playerUserName):
        playerMoves=self.getMovesOfColor(self.findColorOfPlayer(playerUserName))
        mistakes=[]
        for move in playerMoves:
            if self.isMistake(move.getComment(), move.getNag()):
                mistakes.append(move)
        return mistakes

    def getMovesOfColor(self, color):
        if color == Color.White:
            return self.moves[::2]
        elif color == Color.Black:
            return  self.moves[1::2]
        else:
            return self.moves

            
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

    def returnGameWithAnalysisOnlyForPlayer(self, playerUserName=''):
        game=''.join(self.info)
        game+=self.getGameWithoutOpponentsAnalysis(playerUserName)
        return game

    def getGameWithoutOpponentsAnalysis(self, playerUserName=''):
        game=''
        for i in range(len(self.moves)):
            if i%2 == 0:
                game+=str(i+1) + ' '
            game+=self.parseMoveForPlayer(playerUserName, self.moves[i], i)
            game+=' '
        game+='\n'
        return game

    def isPlayerToMove(self, playerUserName, index):
        playerColor=self.findColorOfPlayer(playerUserName)
        if playerColor == Color.White:
            return index%2 == 0
        elif playerColor == Color.Black:
            return index%2 == 1
        else:
            return True

    def parseMoveForPlayer(self, playerUserName, move, index):
        if self.isPlayerToMove(playerUserName, index):
            return move.getMoveWithComment()
        else:
            return move.getMove(time=True)

    def getMoves(self):
        return self.moves

    def highlightAllSquares(self):
        for move in self.moves:
            move.addComment(self.highlightSquaresOfPosition(move.getBoard()))

    def highlightSquaresOfPosition(self, board):
        board=chess.Board(fen=board)
        whiteAttackersPerSquare={}
        blackAttackersPerSquare={}
        for square in chess.SQUARES:
            whiteAttackersPerSquare[square]=(len(board.attackers(chess.WHITE, square)))
            blackAttackersPerSquare[square]=(len(board.attackers(chess.BLACK, square)))

        highlightSquareComment=[]
        squareColorWhiteWinning='G'
        squareColorBlackWinning='R'

        for square in chess.SQUARES:
            if whiteAttackersPerSquare[square] > blackAttackersPerSquare[square]:
                highlightSquareComment.append(squareColorWhiteWinning+chess.square_name(square))
            elif whiteAttackersPerSquare[square] < blackAttackersPerSquare[square]:
                highlightSquareComment.append(squareColorBlackWinning+chess.square_name(square))
            else:
                if whiteAttackersPerSquare[square] != 0:
                    highlightSquareComment.append('Y' + chess.square_name(square))
        return '{ ' + '[%csl ' + ','.join(highlightSquareComment) + ']}'
