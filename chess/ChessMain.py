"""
This is the main driver file. It will handle user input and display the current GameState.
"""

import pygame as p
import ChessEngine

# from chess.ChessEngine import GameState

p.init() #initialize pygame
width = height = 512
dimension = 8
sq_size = height//dimension
max_fps = 15
images = {}

"""
Initialize a global dictionary of images. Called exactly once in the main.
"""
def load_images():
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (sq_size, sq_size))
        #we can access an image by saying 'images["wP"]'

"""
Responsible for all graphics within the current game state
"""
def drawGameState(screen, gs):
    drawBoard(screen) #draw squares on the board
    drawPieces(screen, gs.board)

def drawBoard(screen):
    colors =  [p.Color("white"), p.Color("gray")]
    for i in range(dimension):
        for j in range(dimension):
            color = colors[(i+j)%2]
            p.draw.rect(screen, color, p.Rect(i*sq_size, j*sq_size, sq_size, sq_size))

def drawPieces(screen, board):
    for r in  range(dimension):
        for c in range(dimension):
            piece = board[c][r]
            if piece != "--":
                screen.blit(images[piece], p.Rect(r*sq_size, c*sq_size, sq_size, sq_size))

def main():
    """
    Main Driver, responsible for handling user input and updating grahics
    """
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = GameState()
    load_images()
    running = True
    sqSelected = () #no square selected at the, keeps track of the last click of the user (tuple: (row, col))
    playerClicks = [] #keeps track of player clicks (two tuples: [(6, 4), (4, 4)]
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #get (x, y) location of the mouse
                col = location[0]//sq_size
                row = location[1]//sq_size
                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) #append for both first and second click
                if len(playerClicks) == 2: #after 2nd click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    gs.makeMove(move)
                    sqSelected = ()
                    playerClicks = []


        drawGameState(screen, gs)
        clock.tick(max_fps)
        p.display.flip()

main()
