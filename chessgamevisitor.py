import chess
import chess.pgn
from chessmove import ChessMove
from chessmovepair import MovePair

class ChessGameVisitor(chess.pgn.BaseVisitor):
    moves=[]
    variation=False
    variationMoves=[]

    def visit_move(self, board, move):
        if not self.variation:
            self.moves.append(ChessMove(board.san(move), board.fen()))
        else:
            self.variationMoves.append(board.san(move))


    def begin_variation(self):
        self.variation=True

    def end_variation(self):
        self.moves[-1].addComment('(' + ' '.join(self.variationMoves) + ')')
        self.moves[-1].printMove()
        self.variation=False

    def visit_comment(self, comment):
        self.moves[-1].addComment('{ ' + comment + '}')

    def visit_nag(self, nag):
        self.moves[-1].addNag(nag)

    def result(self):
        whiteMove=None
        movePairs=[]
        for i, move in enumerate(self.moves):
            if i%2 == 0:
                whiteMove=move
            else:
                blackMove=move
                movePairs.append(MovePair(whiteMove, blackMove))
                whiteMove=None
        if whiteMove:
            movePairs.append(MovePair(whiteMove, None))
        return movePairs

