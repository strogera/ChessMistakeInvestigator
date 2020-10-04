import chess
import chess.engine

class Investigator:
    engine=''
    movesToInvestigate=[]
    investigateAsColor=None

    def __init__(self, engine, moves, color: chess.Color):
        self.engine=str(engine)
        self.movesToInvestigate=moves
        self.investigateAsColor=color

    def investigate(self):
        for move in self.movesToInvestigate:
            board=chess.Board(fen=move.getBoard())
            board.push_san(move.getMove(nag=False))
            #print(self.analyzePosition(board))
            self.analyzePosition(board)

    def analyzePosition(self, board):
        engine=chess.engine.SimpleEngine.popen_uci(self.engine)
        info=engine.analyse(board, chess.engine.Limit(depth=3))
        engine.quit()
        squaresUnderAttack=[]
        for variationMove in info['pv']:
            board.push(variationMove)
            squaresUnderAttack.append(self.checkAttackedSquares(board))
        return info

    def checkAttackedSquares(self, board):
        whiteAttackersPerSquare={}
        blackAttackersPerSquare={}
        for square in chess.SQUARES:
            '''
            if not square in whiteAttackersPerSquare.keys():
                    whiteAttackersPerSquare[square]=[]
            whiteAttackersPerSquare[square].append(len(board.attackers(chess.WHITE, square)))
            '''
            whiteAttackersPerSquare[square]=(len(board.attackers(chess.WHITE, square)))
            '''
            if not square in blackAttackersPerSquare.keys():
                    blackAttackersPerSquare[square]=[]
            #blackAttackersPerSquare[square].append(len(board.attackers(chess.BLACK, square)))
            '''
            blackAttackersPerSquare[square]=(len(board.attackers(chess.BLACK, square)))
            #attackersPerSquare[square].append(board.attackers(self.investigateAsColor, square))
        print("######")
        print(board.fen())
        for square in chess.SQUARES:
            if whiteAttackersPerSquare[square] > blackAttackersPerSquare[square]:
                if blackAttackersPerSquare[square] != 0:
                    print(blackAttackersPerSquare[square])
                    print('w ' + chess.square_name(square) + ' ' +str(whiteAttackersPerSquare[square]))
            elif whiteAttackersPerSquare[square] < blackAttackersPerSquare[square]:
                if whiteAttackersPerSquare[square] != 0:
                    print('b ' + chess.square_name(square) +' ' + str(blackAttackersPerSquare[square]))
                    #print(chess.square_name(max(blackAttackersPerSquare, key=blackAttackersPerSquare.get)))
        print("######")
        return None



