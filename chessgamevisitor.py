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
            self.variationMoves.append(ChessMove(board.san(move), board.fen()))

    def begin_variation(self):
        self.isVariation=True

    def end_variation(self):
        self.isVariation=False
        self.moves[-1].addVariationMoves(self.variationMoves)
        self.variationMoves=[]

    def visit_comment(self, comment):
        self.moves[-1].addComment('{ ' + comment + '}')

    def visit_nag(self, nag):
        self.moves[-1].addNag(nag)

    def result(self):
        return self.moves

