import chess 
import enum

class Color(enum.Enum):
    Black = 1
    White = 2
    Unknown = 3

class ChessMove:
    boardStateBeforeMove=''
    move=''
    moveNumber=''
    moveColor=Color.Unknown
    comments=[]
    nag=''

    def __init__(self, move, boardStateBeforeMove='', moveNumber='', moveColor=Color.Unknown):
        self.move=move
        self.moveNumber=''
        self.moveColor=moveColor
        self.boardStateBeforeMove=boardStateBeforeMove
        self.comments=[]
        self.nag=''

    def addComment(self, comment):
        self.comments.append(comment)

    def addNag(self, nag):
        self.nag=self.parseNag(nag)

    def getNag(self):
        return self.nag

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

    def getMove(self, nag=True, time=False):
        return self.move+(self.nag if nag else '') + ((' ' + self.getTimeComment()) if time else '')

    def getBoard(self):
        return self.boardStateBeforeMove

    def getTimeComment(self):
        timeComment='{ '
        for comment in self.comments:
            if '[%clk' in comment:
                curString=comment
                while not curString.startswith('[%clk'):
                    curString=curString[1:]
                for c in curString:
                    if c != ']':
                        timeComment+=c
                    else:
                        timeComment+=c+' }'
                        break 
                break
        return timeComment

    def getComment(self):
        comments=self.joinCommandComments()
        return ' '.join(comments)

    def joinCommandComments(self):
        simComments=''
        restComments=[]
        for comment in self.comments:
            if '[%' in comment:
                simComments+=' ' + comment[1:-1]
            else:
                restComments.append(comment)
        return [('{ ' + simComments + '}' if simComments != '' else '')] + restComments

    def getMoveWithComment(self):
        return self.move+self.nag + ' ' + self.getComment()

    def printMove(self):
        print(self.getMoveWithComment())

