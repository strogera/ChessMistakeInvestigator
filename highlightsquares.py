import chess

def highlightSquaresOfMoves(moves, gameInfo=''):
    game=gameInfo
    for move in moves:
        game+='[FEN \"'+ move.getBoard()+'\"]\n[SetUp "1"]\n\n'
        board=chess.Board(fen=move.getBoard())
        game+=highlightSquaresOfPosition(board) + ' '
        board.push_san(move.getMove(nag=False))
        move.addComment(highlightSquaresOfPosition(board))
        game+=move.getMoveWithComment()
        board=chess.Board(fen=move.getBoard())
        varMove=move.getVariationMoves()[0]
        print(varMove.getMove())
        board.push_san(varMove.getMove())
        varMove.addComment(highlightSquaresOfPosition(board))
        game+=' ('+ varMove.getMoveWithComment() + ' ' + ' '.join([x.getMove() for x in move.getVariationMoves()[1:]])+ ')'
        game+='\n\n'
    return game



def highlightSquaresOfPosition(board):
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
            highlightSquareComment.append(squareColorWhiteWinning+chess.square_name(square))
        elif whiteAttackersPerSquare[square] < blackAttackersPerSquare[square]:
            highlightSquareComment.append(squareColorBlackWinning+chess.square_name(square))
        else:
            if whiteAttackersPerSquare[square] != 0:
                highlightSquareComment.append('Y' + chess.square_name(square))
    return '{ ' + '[%csl ' + ','.join(highlightSquareComment) + ']}'