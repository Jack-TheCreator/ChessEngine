import chess
import pandas as pd
import ai

#Removing the list

opening = True
prevMoves = []
board = chess.Board()
computer = ai.AI()

def initData(filepath):
    #reg exp to replace
    toClean = ['1\.','2\.','3\.','4\.','5\.','6\.','7\.','8\.','9\.','10\.','11\.','12\.','13\.',
               '14\.', '15\.']
    data = pd.read_csv(filepath)
    for s in toClean:
        data['moves'] = data.moves.str.replace(s, '')
    data['moves'] = data.moves.str.split()
    return(data['moves'].to_list())

def checkWin():
    return(board.is_game_over())

def playerMove():
    move = input("Enter Move: ")
    board.push_san(move)
    prevMoves.append(move)

def computerMove():
    global opening
    if(opening):
        for l in openingList:
            if(len(prevMoves) < len(l)):
                if(l[:len(prevMoves)]==prevMoves):
                    nextMove = l[len(prevMoves)]
                    board.push_san(nextMove)
                    prevMoves.append(nextMove)
                    return
        print('database exhausted')
        opening = False
    #do ai stuff here
    board.push(computer.minimax(board))



def main():
    endgame = False
    while(not endgame):
        print(board)
        endgame = checkWin()
        playerMove()
        print(board)
        endgame = checkWin()
        computerMove()

#list of openings for our AI
openingList = initData('chess_openings.csv')
main()