import re

class ChessGameFromPGN:
    info=[]
    moves=[]
    comments=[]
    playerUserName=''
    playerColor=''
    pgnFilePath=''

    def __init__(self, path, player):
        self.pgnFilePath=path
        self.playerUserName=player

    def buildGameFromFile(self):
        with open(self.pgnFilePath, 'r') as pgnFile:
            self.readGameInfo(pgnFile)
            self.findColorOfUser()
            pgnFile.seek(0)
            self.readGame(pgnFile)

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

    def readGame(self, pgnFile):
        for line in pgnFile:
            if self.isGameLine(line):
                self.seperateMovesFromComments(line)

    def isGameLine(self, line):
        return line[0] == '1'

    def seperateMovesFromComments(self, line):
            curMoveString=''
            curCommentString=''
            commentBracesStack=[]
            for c in line:
                if c == '{':
                    curMoveString=curMoveString.strip()
                    if curMoveString:
                        self.addMove(curMoveString)
                        curMoveString=''
                    else:
                        if not curCommentString:
                            curCommentString=self.removeLastCommentandReturn() + ' '
                    commentBracesStack.append('{')
                elif c == '}':
                    curCommentString+=c
                    commentBracesStack.pop()
                    if len(commentBracesStack) == 0:
                        self.addComment(curCommentString)
                        curCommentString=''
                    continue
                elif c == '(':
                    commentBracesStack.append('(')
                    if curMoveString.strip():
                        self.addMove(curMoveString)
                        curMoveString=''
                    else:
                        if not curCommentString:
                            curCommentString=self.removeLastCommentandReturn()+' '
                elif c == ')':
                    curCommentString+=c
                    commentBracesStack.pop()
                    if len(commentBracesStack) == 0:
                        self.addComment(curCommentString)
                        curCommentString=''
                    continue
                if not len(commentBracesStack) == 0:
                    curCommentString+=c
                else:
                    curMoveString+=c

    def returnGameWithAnalysisOnlyForPlayer(self):
        game=''.join(self.info)
        game+=self.getGameWithoutOpponentsAnalysis()
        return game

    def getGameWithoutOpponentsAnalysis(self):
        game=''
        for i, x in enumerate(self.comments):
            if (self.playerColor == 'White' and i%2==0) or (self.playerColor == 'Black' and i%2==1):
                game+=self.moves[i]+' '
            else:
                game+=self.moves[i]+' '+x+' '
        return game
