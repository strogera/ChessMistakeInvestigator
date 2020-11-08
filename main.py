import argparse
import sys
from chessgamefrompgn import ChessGameFromPGN
from highlightsquares import highlightSquaresOfMoves

def main():
    argumentParser= argparse.ArgumentParser()
    argumentParser.add_argument('-f', '--find-Mistakes', dest='mistakes', type=str,  help='Find mistakes in pgn File')
    argumentParser.add_argument('-u', '--userName', dest='userName', type=str,  help='Analyze as user <UserName>')
    argumentParser.add_argument('-s', '--squares-highlight', dest='squares',  action='store_true', help='Highlight squares')
    argumentParser.add_argument('-a', '--analysis', dest='analysis',  action='store_true', help='Print game with analysis,\
     if used with -u only returns analysis for player')
    args=argumentParser.parse_args()
    
    pgnFile=args.mistakes
    playerUserName='' if not args.userName else args.userName
    game=ChessGameFromPGN(pgnFile)
    game.buildGameFromFile()
    if args.mistakes:
        mistakes=game.findMistakesOfPlayer(playerUserName)
        for m in mistakes:
            print(m.getMoveWithComment())
        if args.squares:
            print(highlightSquaresOfMoves(mistakes))


    if args.analysis:
        print(game.returnGameWithAnalysisOnlyForPlayer(playerUserName))

if __name__ == "__main__":
    main()
