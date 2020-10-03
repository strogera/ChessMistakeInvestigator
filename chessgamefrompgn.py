import chess.pgn
from chessmove import ChessMove
from chessgamevisitor import ChessGameVisitor

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
            self.moves=chess.pgn.read_game(pgnFile, Visitor=ChessGameVisitor)
            self.findMistakesOfPlayer()

    def readGameInfo(self, pgnFile):
        for line in pgnFile:
            if not self.isGameLine(line):
                self.addInfoLine(line)

    def addInfoLine(self, line):
        self.info.append(line)

    def addMove(self, move):
        self.moves.append(move)

    def addComment(self, comment):
        self.comments.append(comment)

    def removeLastCommentandReturn(self):
        return self.comments.pop()

    def findColorOfUser(self):
        for line in self.info:
            if self.playerUserName in line:
                if "Black" in line:
                    self.playerColor = "Black"
                else:
                    self.playerColor = "White"
                if self.playerColor == '':
                    raise Exception('User: '+user+' is not part of the game')
                return

    def isGameLine(self, line):
        return line[0] == '1'

    def findMistakesOfPlayer(self):
        comments=''
        for i, move in enumerate(self.moves):
            commentsWhite=self.moves[i].getWhiteMoveComment()
            nagWhite=self.moves[i].getWhiteMoveNag()
            commentsBlack=self.moves[i].getBlackMoveComment()
            nagBlack=self.moves[i].getBlackMoveNag()

            if self.playerColor == 'White':
                if self.isMistake(commentsWhite, nagWhite):
                    self.mistakes.append(self.moves[i].getWhiteMove())
            elif self.playerColor == 'Black':
                if self.isMistake(commentsBlack, nagBlack):
                    self.mistakes.append(self.moves[i].getBlackMove())
            else:
                if self.isMistake(commentsWhite, nagWhite):
                    self.mistakes.append(self.moves[i].getWhiteMove())
                if self.isMistake(commentsBlack, nagBlack):
                    self.mistakes.append(self.moves[i].getBlackMove())

    def isMistake(self, comment, nag=''):
        for mistake in self.mistakeDefinitionsForComments:
            if mistake in comment:
                return True
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
            #game+=str(i+1) +  '. ' +self.moves[i].getWholeMove()
            if  self.playerColor == 'White':
                game+=str(i+1) + '. ' + self.moves[i].getWhiteMoveWithComment() + ' ' + self.moves[i].getBlackMoveToStr(time=True) + ' '
            elif self.playerColor == 'Black':
                game+=str(i+1) + '. ' + self.moves[i].getWhiteMoveToStr(time=True)+ ' ' + self.moves[i].getBlackMoveWithComment()  
            else:
                game+=str(i+1) + '. ' + self.moves[i].getWholeMove()
        game+='\n'
        return game
