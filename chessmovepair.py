import chess.pgn
from chessmove import ChessMove

class MovePair:
    whiteMove=None
    blackMove=None


    def __init__(self, whiteMove, blackMove):
        self.whiteMove=whiteMove
        self.blackMove=blackMove

    def getWhiteMove(self, time=False):
        if self.whiteMove:
            return self.whiteMove.getMove(time)
        else:
            return ''

    def getWhiteMoveComment(self):
        if self.whiteMove:
            return self.whiteMove.getComment()
        else:
            return ''

    def getWhiteMoveWithComment(self):
        if self.whiteMove:
            return self.whiteMove.getMoveWithComment()
        else:
            return ''

    def getBlackMove(self, time=False):
        if self.blackMove:
            return self.blackMove.getMove(time)
        else:
            return ''

    def getBlackMoveComment(self):
        if self.blackMove:
            return self.blackMove.getComment()
        else:
            return ''

    def getBlackMoveWithComment(self):
        if self.blackMove:
            return self.blackMove.getMoveWithComment()
        else:
            return ''

    def getWholeMove(self):
        return self.getWhiteMoveWithComment()+' '+self.getBlackMoveWithComment()

    def printMovePair(self):
        print(self.getWholeMove())

