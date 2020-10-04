import chess
import chess.engine

class Investigator:
    engine=''
    movesToInvestigate=[]

    def __init__(self, engine, moves):
        self.engine=str(engine)
        self.movesToInvestigate=moves

    def investigate(self):
        for move in self.movesToInvestigate:
            print(self.analyzePosition(move))

    def analyzePosition(self, move):
        engine=chess.engine.SimpleEngine.popen_uci(self.engine)
        board=chess.Board(fen=move.getBoard())
        board.push_san(move.getMove(nag=False))
        info=engine.analyse(board, chess.engine.Limit(depth=2))
        engine.quit()
        return info



