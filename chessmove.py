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
    variationMoves=[]
    nag=''

    def __init__(self, move, boardStateBeforeMove='', moveNumber='', moveColor=Color.Unknown):
        self.move=move
        self.moveNumber=''
        self.moveColor=moveColor
        self.boardStateBeforeMove=boardStateBeforeMove
        self.comments=[]
        self.nag=''
        self.variationMoves=[]

    def addComment(self, comment):
        self.comments.append(comment)

    def addNag(self, nag):
        self.nag=self.parseNag(nag)

    def addVariationMoves(self, variationMoves):
        self.variationMoves=variationMoves

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
        if len(self.comments) == 0:
            return ''
        timeComment='{ '
        for comment in self.comments:
            if '[%clk' in comment:
                curString=comment
                while not curString.startswith('[%clk'):
                    curString=curString[1:]
                for c in curString:
                    timeComment+=c
                    if c == ']':
                        break 
                break
        return timeComment +'}'

    def getVariationMoves(self):
        return self.variationMoves

    def parseVariationMoves(self):
        if len(self.variationMoves) > 0:
            return '(' + ' '.join([varMove.getMove() for varMove in self.variationMoves])+')'
        else:
            return ''
        #TODO variation with numbers // deleted from chessgamevisitor.py
        '''
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
        '''

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

    def getMoveWithComment(self, var=True):
        return self.move+self.nag + ' ' + self.getComment() + ' ' + (self.parseVariationMoves() if var else '')

    def printMove(self):
        print(self.getMoveWithComment())

