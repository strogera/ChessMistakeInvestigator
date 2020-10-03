import chess
import chess.pgn
from chessmove import ChessMove
from chessmovepair import MovePair

class ChessGameVisitor(chess.pgn.BaseVisitor):
    moves=[]
    variation=False
    variationMoves=[]
    moveCount=0
    whiteMoveFlag=False

    def visit_move(self, board, move):
        if not self.variation:
            self.whiteMoveFlag=not self.whiteMoveFlag
            self.moves.append(ChessMove(board.san(move), board.fen()))
            if self.whiteMoveFlag:
                self.moveCount+=1
        else:
            self.variationMoves.append(board.san(move))


    def begin_variation(self):
        self.variation=True

    def end_variation(self):
        variationComment='( '+ str(self.moveCount) + ('. ' if self.whiteMoveFlag else '... ') + self.variationMoves[0]
        variationMoveCounter=self.moveCount

        variationMovesToBeNumbered=self.variationMoves[1::2]
        variationMovesRest=self.variationMoves[2::2]

        variationMovesNumbered=[]
        for variationMove in variationMovesToBeNumbered:
            variationMove= ' ' + str(variationMoveCounter) + '. ' + variationMove
            variationMovesNumbered.append(variationMove)
            variationMoveCounter+=1

        result=[None]*(len(variationMovesNumbered)+len(variationMovesRest))
        result[::2]=variationMovesNumbered
        result[1::2]=variationMovesRest
        self.moves[-1].addComment(variationComment + ' '.join(result) + ' )')
        self.variation=False
        self.variationMoves=[]

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

