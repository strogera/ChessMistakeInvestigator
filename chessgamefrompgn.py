import re

class ChessGameFromPGN:
    info=[]
    moves=[]
    comments=[]
    mistakes=[]
    playerUserName=''
    playerColor=''
    pgnFilePath=''
    mistakeDefinitions=['Inaccuracy', 'Mistake', 'Blunder'] 

    def __init__(self, path, player):
        self.pgnFilePath=path
        self.playerUserName=player

    def buildGameFromFile(self):
        with open(self.pgnFilePath, 'r') as pgnFile:
            self.readGameInfo(pgnFile)
            self.findColorOfUser()
            pgnFile.seek(0)
            self.readGame(pgnFile)
            self.findMistakes()

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

    def findMistakes(self):
        for i, move in enumerate(self.moves):
            if self.playerToMove(i) and self.isMistake(self.comments[i]):
                self.mistakes.append((move, self.comments[i]))

    def playerToMove(self, index):
        return (self.playerColor == 'White' and index%2==1) or (self.playerColor == 'Black' and index%2==0)

    def isMistake(self, comment):
        for mistake in self.mistakeDefinitions:
            if mistake in comment:
                return True
        return False

    def printMistakes(self):
        for m in self.mistakes:
            print(m[0], m[1])

    def returnGameWithAnalysisOnlyForPlayer(self):
        game=''.join(self.info)
        game+=self.getGameWithoutOpponentsAnalysis()
        return game

    def getGameWithoutOpponentsAnalysis(self):
        game=''
        for i, x in enumerate(self.comments):
            if  self.playerToMove(i):
                game+=self.moves[i]+' '+x+' '
            else:
                game+=self.moves[i]+' '
        return game
