"""
This is our main driver file. Responsible for handling user input and displaying current GameState
"""

import pygame as p
import ChessEngine, SmartMoveFinder

# Z to redo move, R to restart game
BOARD_HEIGHT = 512 #400 another option
BOARD_WIDTH = BOARD_HEIGHT #one half of game window responsible for board, second for menu
MOVE_LOG_PANEL_WIDTH = 450
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
MENU_PANEL_WIDTH = MOVE_LOG_PANEL_WIDTH
MENU_PANEL_HEIGHT = 200
DIMENSION = 8 #dimensions of chess board are 8x8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 60 #for animation later on
IMAGES = {}
IS_PLAYER_ONE_HUMAN = False #if a human playing white, this is true, if AI, this is False
IS_PLAYER_TWO_HUMAN = False #same as above but for black
MAXIMUM_MOVES = 0 #maximum amount of moves for both of players, set 0 to disable
engineSelectedBlack = 'STOCKFISH'
engineSelectedWhite = 'STOCKFISH'

'''
Initialize a global dictionary of images, called exacly once in the main
'''
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    #note: we can acces an image by saying IMAGES['wp']

'''
The main driver for our code, This will handle user input and update graphics
'''
def main():
    p.init()
    timer = 0 #TEMPORARY
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when the move is made
    animate = False #flag variable for when to animate
    moveLogFont = p.font.SysFont("Arial", 14, False, False)
    loadImages() #only once
    running = True
    sqSelected = () #no square is selected, keep track of the last click of user
    playerClicks = [] #keep track of player clicks (two tuples: [(6, 4), (4, 4)])
    gameOver = False
    playerOne = IS_PLAYER_ONE_HUMAN 
    playerTwo = IS_PLAYER_TWO_HUMAN 

    while running:

        mouse_pos = p.mouse.get_pos()
        click = False
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            elif event.type == p.MOUSEBUTTONDOWN:
                click = True
        drawMenu(screen, mouse_pos, click)

        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos() #(x, y) location of mouse
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if col < 8 and row < 8: #handling case when mouseclick is not on board
                        if sqSelected == (row, col): #the uset clicked same twice
                            sqSelected = () #deselect
                            playerClicks = [] #clear player clicks
                        else:
                            sqSelected = (row, col)
                            playerClicks.append(sqSelected) #append for both, first and second click
                        if len(playerClicks) == 2: #after senond click
                            move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    gs.makeMove(validMoves[i])
                                    moveMade = True
                                    animate = True
                                    sqSelected = () #reset user clicks
                                    playerClicks = []
                            if not moveMade:
                                playerClicks = [sqSelected]
            #key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when 'z' pressed
                    gs.undoMove()
                    moveMade = True
                    animate = False
                if e.key == p.K_r: #reset the board when 'r' is pressed
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False
                    print("Black engine: " + engineSelectedBlack)
                    print("White engine: " + engineSelectedWhite)

        #AI move finder
        if not gameOver and not humanTurn:
            AIMove = SmartMoveFinder.findBestMove(gs, validMoves)
            #AIMove = SmartMoveFinder.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            animate = True

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs, validMoves, sqSelected)

        if not gameOver:
            drawMoveLog(screen, gs, moveLogFont)

        if gs.checkmate:
            gameOver = True
            if gs.whiteToMove:
                drawEndGameText(screen, 'Black win by checkmate')
            else:
                drawEndGameText(screen, 'White win by checkmate')

        elif gs.stalemate:
            gameOver = True
            drawEndGameText(screen, 'Stalemate')

        if gameOver and not playerOne and not playerTwo or (timer > MAXIMUM_MOVES and MAXIMUM_MOVES != 0): #TEMPORARY TO PLAY ALWAYS AND SEARCH FOR BUGS
            gs = ChessEngine.GameState()
            validMoves = gs.getValidMoves()
            sqSelected = ()
            playerClicks = []
            moveMade = False
            animate = False
            gameOver = False
            timer = 0 #TEMPORARY

        if MAXIMUM_MOVES != 0:
            #print(timer)
            timer += 1 #TEMPORARY
        clock.tick(MAX_FPS)
        p.display.flip()

'''
Highlight square selected  and moves for piece selected
'''
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): #sqSelected is a piece that can be moved
            #highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) #transparency value -> 0 transparent; 255 opaque
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            #highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))

'''
Responsible for all graphics within a current game state
'''
def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen) #draw squares on the board
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board) #draw pieces on top of those squares

'''
Draw squares on the board, the top left is always light
'''
def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("dark gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Draw the pieces on the board using the current GameState.board
'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #not empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawMoveLog(screen, gameState, font):
    """
    Draws the move log.
    """
    moveLogRect = p.Rect(BOARD_WIDTH, MENU_PANEL_HEIGHT, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT - MENU_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color('black'), moveLogRect)
    moveLog = gameState.moveLog
    moveTexts = []
    for i in range(0, len(moveLog), 2):
        moveString = str(i // 2 + 1) + '.' + str(moveLog[i]) + " "
        if i + 1 < len(moveLog):
            moveString += str(moveLog[i + 1]) + "   "
        moveTexts.append(moveString)

    movesPerRow = 6
    padding = 5
    lineSpacing = 2
    textY = padding
    for i in range(0, len(moveTexts), movesPerRow):
        text = ""
        for j in range(movesPerRow):
            if i + j < len(moveTexts):
                text += moveTexts[i + j]

        textObject = font.render(text, True, p.Color('white'))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing










def drawMenu(screen, mouse_pos, click):
    """
    Draws game menu and handles button clicks.
    """
    speed_value = 1
    moveLogRect = p.Rect(BOARD_WIDTH, 0, MENU_PANEL_WIDTH, MENU_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color('gray'), moveLogRect)

    # Button dimensions and positions
    button_width = 30
    button_height = 30
    button_margin = 5
    total_buttons_width = 6 * button_width + 5 * button_margin

    # Calculate the starting X-coordinate to center the buttons
    button_x = BOARD_WIDTH + (MENU_PANEL_WIDTH - total_buttons_width) // 2
    button_y = button_margin

    # Load and resize button images
    reset_image = p.image.load("images/refresh_button.png")
    reset_image = p.transform.scale(reset_image, (button_width, button_height))

    undo_image = p.image.load("images/undo_button.png")
    undo_image = p.transform.scale(undo_image, (button_width, button_height))

    mute_image = p.image.load("images/mute_button.png")
    mute_image = p.transform.scale(mute_image, (button_width, button_height))

    plus_image = p.image.load("images/plus_button.png")
    plus_image = p.transform.scale(plus_image, (button_width, button_height))

    minus_image = p.image.load("images/minus_button.png")
    minus_image = p.transform.scale(minus_image, (button_width, button_height))

    # Draw Reset button
    reset_button_rect = p.Rect(button_x, button_y, button_width, button_height)
    # Draw the button without a hover effect
    p.draw.rect(screen, p.Color('white'), reset_button_rect)
    p.draw.rect(screen, p.Color('black'), reset_button_rect, 2)  # Add border
    screen.blit(reset_image, (button_x, button_y))  # Draw image

    # Draw Undo button
    undo_button_rect = p.Rect(button_x + button_width + button_margin, button_y, button_width, button_height)
    # Draw the button without a hover effect
    p.draw.rect(screen, p.Color('white'), undo_button_rect)
    p.draw.rect(screen, p.Color('black'), undo_button_rect, 2)  # Add border
    screen.blit(undo_image, (button_x + button_width + button_margin, button_y))  # Draw image

    # Draw Mute button
    mute_button_rect = p.Rect(button_x + 2 * (button_width + button_margin), button_y, button_width, button_height)
    # Draw the button without a hover effect
    p.draw.rect(screen, p.Color('white'), mute_button_rect)
    p.draw.rect(screen, p.Color('black'), mute_button_rect, 2)  # Add border
    screen.blit(mute_image, (button_x + 2 * (button_width + button_margin), button_y))  # Draw image

    # Draw Decrease Speed button
    decrease_speed_button_rect = p.Rect(button_x + 3 * (button_width + button_margin), button_y, button_width, button_height)
    # Draw the button without a hover effect
    p.draw.rect(screen, p.Color('white'), decrease_speed_button_rect)
    p.draw.rect(screen, p.Color('black'), decrease_speed_button_rect, 2)  # Add border
    screen.blit(minus_image, (button_x + 3 * (button_width + button_margin), button_y))  # Draw image

    # Draw Increase Speed button
    increase_speed_button_rect = p.Rect(button_x + 5 * (button_width + button_margin) + button_margin * 2, button_y, button_width, button_height)
    # Draw the button without a hover effect
    p.draw.rect(screen, p.Color('white'), increase_speed_button_rect)
    p.draw.rect(screen, p.Color('black'), increase_speed_button_rect, 2)  # Add border
    screen.blit(plus_image, (button_x + 5 * (button_width + button_margin) + button_margin * 2, button_y))  # Draw image

    # Line spacer between buttons and sections
    line_rect = p.Rect(BOARD_WIDTH, button_y + button_height + button_margin, MENU_PANEL_WIDTH, 2)
    p.draw.rect(screen, p.Color('black'), line_rect)

    # Vertical line to create two sections
    vertical_line_rect = p.Rect(BOARD_WIDTH + MENU_PANEL_WIDTH // 2, button_y + button_height + button_margin, 2, MENU_PANEL_HEIGHT - (button_y + button_height + button_margin))
    p.draw.rect(screen, p.Color('black'), vertical_line_rect)

    # Headers for sections
    font = p.font.Font(None, 24)
    white_text = font.render('WHITE', True, p.Color('white'))
    black_text = font.render('BLACK', True, p.Color('black'))
    screen.blit(white_text, (BOARD_WIDTH + 10, button_y + button_height + button_margin * 2))
    screen.blit(black_text, (BOARD_WIDTH + MENU_PANEL_WIDTH // 2 + 10, button_y + button_height + button_margin * 2))

    # Button names and functions for each section
    white_buttons = [{'name': 'human', 'function': handle_human_click_white}, {'name': 'random', 'function': handle_random_click_white},
                    {'name': 'negamax', 'function': handle_negamax_click_white}, {'name': 'lc0', 'function': handle_lc0_click_white},
                    {'name': 'allie', 'function': handle_allie_click_white}, {'name': 'stockfish', 'function': handle_stockfish_click_white}]

    black_buttons = [{'name': 'human', 'function': handle_human_click_black}, {'name': 'random', 'function': handle_random_click_black},
                    {'name': 'negamax', 'function': handle_negamax_click_black}, {'name': 'lc0', 'function': handle_lc0_click_black},
                    {'name': 'allie', 'function': handle_allie_click_black}, {'name': 'stockfish', 'function': handle_stockfish_click_black}]

    # Draw buttons below the WHITE section in two columns
    for i, button_info in enumerate(white_buttons):
        button_width = 100  # Set the desired width for the buttons
        button_height = 30  # Set the desired height for the buttons
        col = i % 2  # Determine the column (0 or 1)
        row = i // 2  # Determine the row
        button_rect = p.Rect(BOARD_WIDTH + 10 + col * (button_width + button_margin * 2),
                            button_y + button_height + button_margin * 3 + font.get_height() + row * (button_height + button_margin),
                            button_width, button_height)
        p.draw.rect(screen, p.Color('white'), button_rect)
        p.draw.rect(screen, p.Color('black'), button_rect, 2)  # Add border
        button_text = font.render(button_info['name'], True, p.Color('black'))
        screen.blit(button_text, (button_rect.x + button_width // 2 - button_text.get_width() // 2,
                                button_rect.y + button_height // 2 - button_text.get_height() // 2))

        # Check for button clicks
        if button_rect.collidepoint(mouse_pos) and click:
            button_info['function']()

    # Draw buttons below the BLACK section in two columns
    for i, button_info in enumerate(black_buttons):
        button_width = 100  # Set the desired width for the buttons
        button_height = 30  # Set the desired height for the buttons
        col = i % 2  # Determine the column (0 or 1)
        row = i // 2  # Determine the row
        button_rect = p.Rect(BOARD_WIDTH + MENU_PANEL_WIDTH // 2 + 10 + col * (button_width + button_margin * 2),
                            button_y + button_height + button_margin * 3 + font.get_height() + row * (button_height + button_margin),
                            button_width, button_height)
        p.draw.rect(screen, p.Color('black'), button_rect)
        p.draw.rect(screen, p.Color('white'), button_rect, 2)  # Add border
        button_text = font.render(button_info['name'], True, p.Color('white'))
        screen.blit(button_text, (button_rect.x + button_width // 2 - button_text.get_width() // 2,
                                button_rect.y + button_height // 2 - button_text.get_height() // 2))

    # Draw buttons below the BLACK section in two columns
    for i, button_info in enumerate(black_buttons):
        button_width = 100  # Set the desired width for the buttons
        button_height = 30  # Set the desired height for the buttons
        col = i % 2  # Determine the column (0 or 1)
        row = i // 2  # Determine the row
        button_rect = p.Rect(BOARD_WIDTH + MENU_PANEL_WIDTH // 2 + 10 + col * (button_width + button_margin * 2),
                            button_y + button_height + button_margin * 3 + font.get_height() + row * (button_height + button_margin),
                            button_width, button_height)
        p.draw.rect(screen, p.Color('black'), button_rect)
        p.draw.rect(screen, p.Color('white'), button_rect, 2)  # Add border
        button_text = font.render(button_info['name'], True, p.Color('white'))
        screen.blit(button_text, (button_rect.x + button_width // 2 - button_text.get_width() // 2,
                                button_rect.y + button_height // 2 - button_text.get_height() // 2))

        # Check for button clicks
        if button_rect.collidepoint(mouse_pos) and click:
            button_info['function']()

    # Check for button clicks
    if click:
        if reset_button_rect.collidepoint(mouse_pos):
            print("Reset button clicked!")
            # Add your reset button logic here

        if undo_button_rect.collidepoint(mouse_pos):
            print("Undo button clicked!")
            # Add your undo button logic here

        if mute_button_rect.collidepoint(mouse_pos):
            print("Mute button clicked!")
            # Add your mute button logic here

        if decrease_speed_button_rect.collidepoint(mouse_pos):
            print("Decrease Speed button clicked!")
            # Subtract 0.5 from the speed value
            speed_value -= 0.5
            # Make sure the speed doesn't go below 0.5
            speed_value = max(0.5, speed_value)

        if increase_speed_button_rect.collidepoint(mouse_pos):
            print("Increase Speed button clicked!")
            # Add 0.5 to the speed value
            speed_value += 0.5
            # Make sure the speed doesn't go above 3.0
            speed_value = min(3.0, speed_value)

    # Render and draw updated speed text
    speed_text = font.render(f'{int(speed_value)}.0x', True, p.Color('black'))
    screen.blit(speed_text, (button_x + 4 * (button_width + button_margin) + button_margin, button_y + button_margin))




# Button functions
def handle_human_click_white():
    global engineSelectedWhite
    engineSelectedWhite = 'HUMAN'

def handle_random_click_white():
    global engineSelectedWhite
    engineSelectedWhite = 'RANDOM'

def handle_negamax_click_white():
    print("Handling NEGAMAX click white")

def handle_lc0_click_white():
    print("Handling LC0 click white")

def handle_allie_click_white():
    print("Handling ALLIE click white")

def handle_stockfish_click_white():
    global engineSelectedWhite
    engineSelectedWhite = 'STOCKFISH'

def handle_human_click_black():
    global engineSelectedBlack
    engineSelectedBlack = 'HUMAN'

def handle_random_click_black():
    global engineSelectedBlack
    engineSelectedBlack = 'RANDOM'

def handle_negamax_click_black():
    print("Handling NEGAMAX click black")

def handle_lc0_click_black():
    print("Handling LC0 click black")

def handle_allie_click_black():
    print("Handling ALLIE click black")

def handle_stockfish_click_black():
    global engineSelectedBlack
    engineSelectedBlack = 'STOCKFISH'














'''
Animating a move
'''
def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 3 #frames to move one square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        #erase the piece moved from its ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        #draw captured piece onto rectangle
        if move.pieceCaptured != "--":
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        #draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(MAX_FPS)


def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    text_object = font.render(text, False, p.Color("gray"))
    text_location = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - text_object.get_width() / 2, BOARD_HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, False, p.Color('black'))
    screen.blit(text_object, text_location.move(2, 2))


if __name__ == "__main__":
    main()
