import chess
import chess.pgn
from chessmove import ChessMove
from chessmove import Color

class ChessGameVisitor(chess.pgn.BaseVisitor):
    moves=[]
    isVariation=False
    variationMoves=[]
    moveCount=0
    whiteMoveFlag=False

    def visit_move(self, board, move):
        if not self.isVariation:
            self.whiteMoveFlag=not self.whiteMoveFlag
            moveColor=Color.Unknown
            if self.whiteMoveFlag:
                self.moveCount+=1
                moveColor=Color.White
            else:
                moveColor=Color.Black
            self.moves.append(ChessMove(board.san(move), board.fen(), self.moveCount, moveColor))
        else:
            self.variationMoves.append(board.san(move))

    def begin_variation(self):
        self.isVariation=True

    def end_variation(self):
        self.moves[-1].addComment(self.parseVariation())
        self.isVariation=False
        self.variationMoves=[]

    def parseVariation(self):
        variationComment='( '+ str(self.moveCount) + ('. ' if self.whiteMoveFlag else '... ') + self.variationMoves[0]
        variationMoveCounter=self.moveCount

        variationMovesToBeNumbered=self.variationMoves[1::2]
        variationMovesRest=self.variationMoves[2::2]

        variationMovesNumbered=self.addNumbersToMoves(variationMovesToBeNumbered, variationMoveCounter)

        return variationComment + ' '.join(self.joinMovesForVariation(variationMovesNumbered, variationMovesRest)) + ')' 

    def addNumbersToMoves(self, moves, startingNumber):
        #ex. (e4, 1) -> 1. e4
        counter=startingNumber
        numberedMoves=[]
        for move in moves:
            move= ' ' + str(counter) + '. ' + move
            numberedMoves.append(move)
            counter+=1
        return numberedMoves

    def joinMovesForVariation(self, numbered, rest):
        result=[None]*(len(numbered)+len(rest))
        result[::2]=numbered
        result[1::2]=rest
        return result

    def visit_comment(self, comment):
        self.moves[-1].addComment('{ ' + comment + '}')

    def visit_nag(self, nag):
        self.moves[-1].addNag(nag)

    def result(self):
        return self.moves

