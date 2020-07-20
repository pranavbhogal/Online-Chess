"""
This is the main driver file. It will handle user input and display the current GameState.
"""

import pygame as p
from chess import ChessEngine

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
Main Driver, responsible for handling user input and updating grahics
"""

def main():
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    load_images()
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        drawGameState(screen, gs)
        clock.tick(max_fps)
        p.display.flip()
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


def drawPieces(scree, board):
    pass



if __name__ == "__main__":
    main()