import chess.pgn
from chessmove import ChessMove
from chessgamevisitor import ChessGameVisitor
from chessmovepair import MovePair

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
            self.moves=self.makePairsFromMoves(chess.pgn.read_game(pgnFile, Visitor=ChessGameVisitor))
            self.findMistakesOfPlayer()

    def readGameInfo(self, pgnFile):
        for line in pgnFile:
            if not self.isGameLine(line):
                self.addInfoLine(line)

    def addInfoLine(self, line):
        self.info.append(line)

    def makePairsFromMoves(self, moves):
        whiteMove=None
        movePairs=[]
        for i, move in enumerate(moves):
            if i%2 == 0:
                whiteMove=move
            else:
                blackMove=move
                movePairs.append(MovePair(whiteMove, blackMove))
                whiteMove=None
        if whiteMove:
            movePairs.append(MovePair(whiteMove, None))
        return movePairs

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
            moveStr+=move.getWholeMove() + ' '
        return moveStr

    def getMistakes(self):
        return self.mistakes

    def getAllMoves(self):
        moves=[]
        for movePair in self.moves:
            moves.append(movePair.getWhiteMove())
            moves.append(movePair.getBlackMove())
        return moves

    def highlightSquaresOfPosition(self, board):
        whiteAttackersPerSquare={}
        blackAttackersPerSquare={}
        for square in chess.SQUARES:
            whiteAttackersPerSquare[square]=(len(board.attackers(chess.WHITE, square)))
            blackAttackersPerSquare[square]=(len(board.attackers(chess.BLACK, square)))

        highlightSquareComment=[]
        if self.playerColor == 'White':
            squareColorWhiteWinning='G'
            squareColorBlackWinning='R'
        else:
            squareColorWhiteWinning='R'
            squareColorBlackWinning='G'

        for square in chess.SQUARES:
            if whiteAttackersPerSquare[square] > blackAttackersPerSquare[square]:
                highlightSquareComment.append(squareColorWhiteWinning+chess.square_name(square))
            elif whiteAttackersPerSquare[square] < blackAttackersPerSquare[square]:
                highlightSquareComment.append(squareColorBlackWinning+chess.square_name(square))
            else:
                if whiteAttackersPerSquare[square] != 0:
                    highlightSquareComment.append('Y' + chess.square_name(square))
        return '{ ' + '[%csl ' + ','.join(highlightSquareComment) + ']}'
