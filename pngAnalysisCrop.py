import pathlib
import re

def findColorOfUser(pngFile, user):
    color = None
    for line in pngFile:
        if user in line:
            if "Black" in line:
                color = "Black"
                break
            else:
                color = "White"
                break
    if not color:
        raise Exception('User: '+user+' is not part of the game')
    return color 

def cropMistakesOfOpponent(pngFile, colorOfUser):
    moves=[]
    comments=[]
    for line in pngFile:
        curMoveString=''
        curCommentString=''
        if line[0] == '1':
            commentBraces=[]
            for c in line:
                if c == '{':
                    curMoveString=curMoveString.strip()
                    if curMoveString:
                        moves.append(curMoveString)
                        curMoveString=''
                    else:
                        if not curCommentString:
                            curCommentString=comments.pop()+' '
                    commentBraces.append('{')
                elif c == '}':
                    curCommentString+=c
                    commentBraces.pop()
                    if len(commentBraces) == 0:
                        comments.append(curCommentString)
                        curCommentString=''
                    continue
                elif c == '(':
                    commentBraces.append('(')
                    if curMoveString.strip():
                        moves.append(curMoveString)
                        curMoveString=''
                    else:
                        if not curCommentString:
                            curCommentString=comments.pop()+' '
                elif c == ')':
                    curCommentString+=c
                    commentBraces.pop()
                    if len(commentBraces) == 0:
                        comments.append(curCommentString)
                        curCommentString=''
                    continue

                if not len(commentBraces) == 0:
                    curCommentString+=c
                else:
                    curMoveString+=c
            comments.append(comments.pop()+' '+curMoveString)
            curMoveString=''
            curCommentString=''


    game=''
    for i, x in enumerate(comments):
        regResult=re.match(r'\s*\{\s*(.*?)\}\s*\{\s*(.*?)\}\s*\(\s*(.*?)\)\s*', x) 
        if regResult:
            if (colorOfUser == 'White' and i%2==0) or (colorOfUser == 'Black' and i%2==1):
                x='{'+regResult.group(2)+'}'
        game+=moves[i]+' '+x+' '

    return game




