import chess 

class ChessMove:
    boardStateBeforeMove=''
    move=''
    comments=[]
    nag=''

    def __init__(self, move, boardStateBeforeMove=''):
        self.move=move
        self.boardStateBeforeMove=boardStateBeforeMove
        self.comments=[]
        self.nag=''

    def addComment(self, comment):
        self.comments.append(comment)

    def addNag(self, nag):
        self.nag=self.parseNag(nag)

    def parseNag(self, nag):
        if nag == chess.pgn.NAG_GOOD_MOVE:
            return '!'
        elif nag == chess.pgn.NAG_MISTAKE:
            return '?'
        elif nag == chess.pgn.NAG_BRILLIANT_MOVE:
            return '!!'
        elif nag == chess.pgn.NAG_BLUNDER:
            return '??'
        elif nag == chess.pgn.NAG_SPECULATIVE_MOVE:
            return '!?'
        elif nag == chess.pgn.NAG_DUBIOUS_MOVE:
            return '?!'
        else:
            return ''

    def getMove(self):
        return self.move+self.nag

    def getComment(self):
        return ''.join(self.comments)

    def getMoveWithComment(self):
        return self.getMove() + ' ' + ' '.join(self.comments) 

    def printMove(self):
        print(self.getMoveWithComment())

