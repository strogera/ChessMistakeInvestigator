import chess

def highlightSquaresOfMoves(moves, gameInfo=''):
    game=gameInfo
    for move in moves:
        game+='[FEN \"'+ move.getBoard()+'\"]\n[SetUp "1"]\n\n'
        board=chess.Board(fen=move.getBoard())
        board.push_san(move.getMove(nag=False))
        move.addComment(highlightSquaresOfPosition(board))

        varMove=move.getVariationMoves()[0]
        board=chess.Board(fen=varMove.getBoard())
        board.push_san(varMove.getMove())
        varMove.addComment(highlightSquaresOfPosition(board))

        game+=highlightDifferentSquaresofPositions(move, varMove)
        game+=move.getMoveWithComment(var=False)
        game+=' ('+ varMove.getMoveWithComment(var=False) + ' ' + ' '.join([x.getMove() for x in move.getVariationMoves()[1:]])+ ')'
        game+='\n\n'
    return game



def highlightSquaresOfPosition(board):
    highlightSquareComment=findColorOfSquares(board)
    return makeHighlightComment(highlightSquareComment)

def makeHighlightComment(highlightSquareComment, arrows=None):
    return '{ ' + '[%csl ' + ','.join(highlightSquareComment) + ']' + makeArrowComment(arrows)+ '}'

def makeArrowComment(arrows):
    if arrows:
        return '[%cal '+ ','.join(arrows) +']'
    else:
        return ''

def findColorOfSquares(board):
    whiteAttackersPerSquare={}
    blackAttackersPerSquare={}
    for square in chess.SQUARES:
        whiteAttackersPerSquare[square]=(len(board.attackers(chess.WHITE, square)))
        blackAttackersPerSquare[square]=(len(board.attackers(chess.BLACK, square)))

    highlightSquareComment=[]
    squareColorWhiteWinning='G'
    squareColorBlackWinning='R'

    for square in chess.SQUARES:
        if whiteAttackersPerSquare[square] > blackAttackersPerSquare[square]:
            if blackAttackersPerSquare[square]!=0:
                highlightSquareComment.append(squareColorWhiteWinning+chess.square_name(square))
        elif whiteAttackersPerSquare[square] < blackAttackersPerSquare[square]:
            if whiteAttackersPerSquare[square] !=0:
                highlightSquareComment.append(squareColorBlackWinning+chess.square_name(square))
        else:
            if whiteAttackersPerSquare[square] != 0:
                highlightSquareComment.append('Y' + chess.square_name(square))
    return highlightSquareComment

def highlightDifferentSquaresOfMoves(moves, gameInfo=''):
    game=gameInfo
    for move in moves:
        game+='[FEN \"'+ move.getBoard()+'\"]\n[SetUp "1"]\n\n'
        varMove=move.getVariationMoves()[0]
        game+=highlightDifferentSquaresofPositions(move, varMove)
        game+=move.getMoveWithComment()
        game+=' ('+ varMove.getMoveWithComment() + ' ' + ' '.join([x.getMove() for x in move.getVariationMoves()[1:]])+ ')'
        game+='\n\n'
    return game

def highlightDifferentSquaresofPositions(move, altmove):
        board=chess.Board(fen=move.getBoard())
        move=board.parse_san(move.getMove(nag=False))
        board.push(move)
        position1=findColorOfSquares(board)
        arrow1='R'+move.uci()
        board=chess.Board(fen=altmove.getBoard())
        altmove=board.parse_san(altmove.getMove(nag=False))
        board.push(altmove)
        position2=findColorOfSquares(board)
        arrow2='G'+altmove.uci()
        return makeHighlightComment(listDiff(position1, position2), [arrow1, arrow2])

def listDiff(li1, li2):
    return (list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))