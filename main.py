import argparse
import sys
from chessgamefrompgn import ChessGameFromPGN

def main():
    argumentParser= argparse.ArgumentParser()
    argumentParser.add_argument('-f', '--find-Mistakes', dest='mistakes', type=str,  help='Find mistakes in pgn File')
    argumentParser.add_argument('-u', '--userName', dest='userName', type=str,  help='Analyze as user <UserName>')
    args=argumentParser.parse_args()
    
    if args.mistakes:
        pgnFile=args.mistakes
        user='' if not args.userName else args.userName
        game=ChessGameFromPGN(pgnFile, user)
        game.buildGameFromFile()
        game.printMistakes()

if __name__ == "__main__":
    main()
