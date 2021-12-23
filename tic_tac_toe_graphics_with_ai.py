
# need to install piglet package first: pip install pyglet --user
import pyglet
from pyglet import shapes
from pyglet.gl import *
from pyglet.window import mouse

# creats window and background
width, height = 600, 600
window = pyglet.window.Window(width, height, "TicTacToe")
pyglet.gl.glClearColor(0.5,0.5,0.6,1)

batch = pyglet.graphics.Batch()
line1 = shapes.Line(200, 0, 200, 600, 10, color = (0,0,0), batch = batch)
line2 = shapes.Line(400, 0, 400, 600, 10, color = (0,0,0), batch = batch)
line3 = shapes.Line(0, 200, 600, 200, 10, color = (0,0,0), batch = batch)
line4 = shapes.Line(0, 400, 600, 400, 10, color = (0,0,0), batch = batch)

player_x = 0
player_y = 0

first_label = None
second_label = None
third_label = None
fourth_label = None
five_label = None
six_label = None
seven_label = None
eight_label = None
nine_label = None

# variable that represents the board
board = {1: " ", 2: " ", 3: " ",
         4: " ", 5: " ", 6: " ",
         7: " ", 8: " ", 9: " "}

clicking_count = 0
player_letter = "X"
computer_letter = "O"
isGameOver = False


# draw can happen only if all of the positions are full, so if any of the positions is empty, returning False
def isDraw():
    for pos in board.values():
        if pos == " ":
            return False
    return True

# check which player is winning through if statements (1=player, 2=computer)
def isWinning():
    # rows
    if board[1] == board[2] and board[2] == board[3] and board[3]==player_letter:
        return 1
    elif board[4] == board[5] and board[5] == board[6] and board[6]==player_letter:
        return 1
    elif board[7] == board[8] and board[8] == board[9] and board[9]==player_letter:
        return 1
    elif board[1] == board[2] and board[2] == board[3] and board[3]==computer_letter:
        return 2
    elif board[4] == board[5] and board[5] == board[6] and board[6]==computer_letter:
        return 2
    elif board[7] == board[8] and board[8] == board[9] and board[9]==computer_letter:
        return 2
    # collums 
    elif board[1] == board[4] and board[4] == board[7] and board[7]==player_letter:
        return 1
    elif board[2] == board[5] and board[5] == board[8] and board[8]==player_letter:
        return 1   
    elif board[3] == board[6] and board[6] == board[9] and board[9]==player_letter:
        return 1
    elif board[1] == board[4] and board[4] == board[7] and board[7]==computer_letter:
        return 2
    elif board[2] == board[5] and board[5] == board[8] and board[8]==computer_letter:
        return 2   
    elif board[3] == board[6] and board[6] == board[9] and board[9]==computer_letter:
        return 2
    # diagonal 
    elif board[1] == board[5] and board[5] == board[9] and board[9]==player_letter:
        return 1
    elif board[3] == board[5] and board[5] == board[7] and board[7]==player_letter:
        return 1   
    elif board[1] == board[5] and board[5] == board[9] and board[9]==computer_letter:
        return 2
    elif board[3] == board[5] and board[5] == board[7] and board[7]==computer_letter:
        return 2   
    else:
        return 0

# function that makes the computer move 
def computer_move():
    global clicking_count
    bestScore = -200
    bestMove = 0
    # goes through all possible positions
    for pos in board.keys():
        if board[pos] == " ":
            board[pos] = computer_letter
            score = minimax(False) # false becasue then it's the player turn
            board[pos] = " " # resetting the board
            if score > bestScore:
                bestScore = score
                bestMove = pos

    if board[bestMove] != " ":
        print("Can't place there, please choose a different place")
        # clicking_count -= 1
        computer_move()
    # place piece in the position if possible
    else:
        board[bestMove] = computer_letter
        return bestMove

# algorithm to calculate which move is the best for the computer
def minimax(isMaximizing):
    # the function returns a score that represents if the move is good or bad
    # high score represents a good move
    if isWinning() == 1:
        return -100 # player won aka bad move
    elif isWinning() == 2:
        return 100 # computer won aka great move
    elif isDraw():
        return 0 # there is a draw, okay move
    
    # isMaximaizng means that the computer is playing and we want the move with the highest score 
    if isMaximizing:
        bestScore = -200
        # goes through all the positions
        for pos in board.keys():
            if board[pos] == " ":
                board[pos] = computer_letter
                # repeats through recursion until someone is winning / there is a draw
                score = minimax(False) # false becasue then it's the player turn
                board[pos] = " " # resetting the board
                if score > bestScore:
                    bestScore = score
        return bestScore
    # now plays as the player, so it will do the best move for the player
    # used so the computer will know the counter attack that the player is likely to do
    else:
        bestScore = 200
        for pos in board.keys():
            # goes through all the positions
            if board[pos] == " ":
                board[pos] = player_letter
                score = minimax(True) # false becasue then it's the player turn
                board[pos] = " " # resetting the board
                if score < bestScore:
                    bestScore = score
        return bestScore

# changes the move that was calculated in computer_move() into x and y coordinates on the screen
def computer_position():
    pos = computer_move()
    if pos == 1:
        x = 50
        y = 450
    elif pos == 2:
        x = 250
        y = 450
    elif pos == 3:
        x = 450
        y = 450  
    elif pos == 4:
        x = 50
        y = 250
    elif pos == 5:
        x = 250
        y = 250
    elif pos == 6:
        x = 450
        y = 250
    elif pos == 7:
        x = 50
        y = 50
    elif pos == 8:
        x = 250
        y = 50
    elif pos == 9:
        x = 450
        y = 50
    return (x,y)

# returns the the centered x,y coordinates of the player move, arguments are x,y that are given when player clicks the board
def player_move(x,y):
    global clicking_count, isGameOver, player_x, player_y
    # plays based on position of clik
    if x>=0 and x<=200 and y>=400 and y<=600:
        # while the game is not over
        if isGameOver == False:
            # checks if there is already a piece in the position
            if board[1] != " ":
                print("Can't place there, please choose a different place")
                clicking_count -= 1
                player_move(x,y)
            else:
                if clicking_count % 2 != 0:
                    board[1] = player_letter
                    return 50, 450
    elif x>=200 and x<=400 and y>=400 and y<=600:
        if isGameOver == False:
            if board[2] != " ":
                print("Can't place there, please choose a different place")
                clicking_count -= 1
                player_move(x,y)
            else:
                if clicking_count % 2 != 0:
                    board[2] = player_letter
                    return 250,450
    elif x>=400 and x<=600 and y>=400 and y<=600:
        if isGameOver == False:
            if board[3] != " ":
                print("Can't place there, please choose a different place")
                clicking_count -= 1
                player_move(x,y)
            else:
                if clicking_count % 2 != 0:
                    board[3] = player_letter
                    return 450,450
    elif x>=0 and x<=200 and y>=200 and y<=400:
        if isGameOver == False:
            if board[4] != " ":
                print("Can't place there, please choose a different place")
                clicking_count -= 1
                player_move(x,y)
            else:
                if clicking_count % 2 != 0:
                    board[4] = player_letter
                    return 50,250
    elif x>=200 and x<=400 and y>=200 and y<=400:
        if isGameOver == False:
            if board[5] != " ":
                print("Can't place there, please choose a different place")
                clicking_count -= 1
                player_move(x,y)
            else:
                if clicking_count % 2 != 0:
                    board[5] = player_letter
                    return 250,250
    elif x>=400 and x<=600 and y>=200 and y<=400:
        if isGameOver == False:
            if board[6] != " ":
                print("Can't place there, please choose a different place")
                clicking_count -= 1
                player_move(x,y)
            else:
                if clicking_count % 2 != 0:
                    board[6] = player_letter
                    return 450,250
    elif x>=0 and x<=200 and y>=0 and y<=200:
        if isGameOver == False:
            if board[7] != " ":
                print("Can't place there, please choose a different place")
                clicking_count -= 1
                player_move(x,y)
            else:
                if clicking_count % 2 != 0:
                    board[7] = player_letter
                    return 50,50
    elif x>=200 and x<=400 and y>=0 and y<=200:
        if isGameOver == False:
            if board[8] != " ":
                print("Can't place there, please choose a different place")
                clicking_count -= 1
                player_move(x,y)
            else:
                if clicking_count % 2 != 0:
                    board[8] = player_letter
                    return 250,50
    elif x>=400 and x<=600 and y>=0 and y<=200:
        if isGameOver == False:
            if board[9] != " ":
                print("Can't place there, please choose a different place")
                clicking_count -= 1
                player_move(x,y)
            else:
                if clicking_count % 2 != 0:
                    board[9] = player_letter
                    return 450,50

# event that happens when mouse is clicked
@window.event
def on_mouse_press(x, y, button, modifiers):
    global clicking_count, isGameOver, player_x, player_y
    global first_label, second_label, third_label, fourth_label, five_label, six_label, seven_label, eight_label, nine_label

    # showing pieces on board
    clicking_count += 1
    # use clicking count to check if it's computer or player turn 
    if button == mouse.LEFT:
        if isGameOver == False:
            if clicking_count == 1:
                x,y = player_move(x,y)
                first_label = pyglet.text.Label(player_letter,
                    font_name='Times New Roman',
                    font_size=100,
                    x=x, y=y)
                clicking_count += 1
            if clicking_count == 2:
                x,y = computer_position()
                second_label = pyglet.text.Label(computer_letter,
                    font_name='Times New Roman',
                    font_size=100,
                    x=x, y=y)
            if clicking_count == 3:
                x,y = player_move(x,y)
                third_label = pyglet.text.Label(player_letter,
                    font_name='Times New Roman',
                    font_size=100,
                    x=x, y=y)
                clicking_count += 1
            if clicking_count == 4:
                x,y = computer_position()
                fourth_label = pyglet.text.Label(computer_letter,
                    font_name='Times New Roman',
                    font_size=100,
                    x=x, y=y)
            if clicking_count == 5:
                x,y = player_move(x,y)
                five_label = pyglet.text.Label(player_letter,
                    font_name='Times New Roman',
                    font_size=100,
                    x=x, y=y)
                clicking_count += 1
            if clicking_count == 6:
                x,y = computer_position()
                six_label = pyglet.text.Label(computer_letter,
                    font_name='Times New Roman',
                    font_size=100,
                    x=x, y=y)
            if clicking_count == 7:
                x,y = player_move(x,y)
                seven_label = pyglet.text.Label(player_letter,
                    font_name='Times New Roman',
                    font_size=100,
                    x=x, y=y)
                clicking_count += 1
            if clicking_count == 8:
                x,y = computer_position()
                eight_label = pyglet.text.Label(computer_letter,
                    font_name='Times New Roman',
                    font_size=100,
                    x=x, y=y)
            if clicking_count == 9:
                x,y = player_move(x,y)
                nine_label = pyglet.text.Label(player_letter,
                    font_name='Times New Roman',
                    font_size=100,
                    x=x, y=y)
                # clicking_count += 1

# drawing the pieces on the board and checks if the game is over
@window.event
def on_draw():
    global clicking_count, isGameOver
    window.clear()
    batch.draw()
    if first_label != None:
        first_label.draw()
    if second_label != None:
        second_label.draw()
    if third_label != None:
        third_label.draw()
    if fourth_label != None:
        fourth_label.draw()
    if five_label != None:
        five_label.draw()
    if six_label != None:
        six_label.draw()
    if seven_label != None:
        seven_label.draw()
    if eight_label != None:
        eight_label.draw()
    if nine_label != None:
        nine_label.draw()

    if isWinning()!=0 or isDraw()==True:
        isGameOver = True
        if isWinning() == 1:
            text = "Player won!"
        elif isWinning() == 2:
            text = "Computer won!"
        else:
            text = "Draw!" 
        winning_label = pyglet.text.Label(text,
            font_name='Times New Roman',
            font_size=40,
            color=(150,150,150,255),
            x=150, y=250)
        winning_label.draw()

        

def main():
    pyglet.app.run()

if __name__ == "__main__":
    main()