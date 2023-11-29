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
MAX_FPS = 120 #for animation later on
IMAGES = {}
MAXIMUM_MOVES = 200 #maximum amount of moves for both of players, set 0 to disable
LOG_FILE_PATH = "log.txt" # SILNIK_BIALY SILNIK_CZARNY 0/1/2 -> 0-whiteWin 1-BlackWin 2-stalemate 
engineSelectedBlack = 'HUMAN'
engineSelectedWhite = 'HUMAN'
soundOn = True
resetGame = False
undoMove = False
engineParameters = [3, 3, 3, 3]


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
    p.mixer.init()
    p.mixer.music.load('sounds/move.mp3')
    global resetGame
    global undoMove
    global soundOn

    while running:

        drawMenu(screen, (0, 0), False)
        humanTurn = (gs.whiteToMove and engineSelectedWhite == 'HUMAN') or (not gs.whiteToMove and engineSelectedBlack == 'HUMAN')
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                print(engineParameters)
                location = p.mouse.get_pos() #(x, y) location of mouse
                drawMenu(screen, location, True) # draw menu from function
                if not gameOver and humanTurn:
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

            if undoMove:
                undoMove = False
                gs.undoMove()
                moveMade = True
                animate = False
            if resetGame:
                resetGame = False
                gs = ChessEngine.GameState()
                validMoves = gs.getValidMoves()
                sqSelected = ()
                playerClicks = []
                moveMade = False
                animate = False
                gameOver = False

        #AI move finder
        if not gameOver and not humanTurn:
            AIMove = SmartMoveFinder.useEngine(gs, validMoves, engineSelectedWhite, engineSelectedBlack)
            gs.makeMove(AIMove)
            moveMade = True
            animate = True

        if moveMade:
            if animate:
                if (soundOn):
                    p.mixer.music.play()
                animateMove(gs.moveLog[-1], screen, gs.board)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs, validMoves, sqSelected)

        if not gameOver:
            drawMoveLog(screen, gs, moveLogFont)

        if gs.checkmate:
            gameOver = True            
            if gs.whiteToMove:
                with open(LOG_FILE_PATH, "a") as log_file:
                    log_file.write(engineSelectedWhite + ' ' +  engineSelectedBlack + ' ' + '1' +'\n')
                drawEndGameText(screen, 'Black win by checkmate')
            else:
                with open(LOG_FILE_PATH, "a") as log_file:
                    log_file.write(engineSelectedWhite + ' ' +  engineSelectedBlack + ' ' + '0' +'\n')
                drawEndGameText(screen, 'White win by checkmate')

        elif gs.stalemate:
            with open(LOG_FILE_PATH, "a") as log_file:
                log_file.write(engineSelectedWhite + ' ' +  engineSelectedBlack + ' ' + '2' +'\n')
            gameOver = True

            drawEndGameText(screen, 'Stalemate')

        if gameOver and not engineSelectedWhite == 'HUMAN' and not engineSelectedBlack == 'HUMAN' or (timer > MAXIMUM_MOVES and MAXIMUM_MOVES != 0): #TEMPORARY TO PLAY ALWAYS AND SEARCH FOR BUGS
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
    global soundOn
    global engineParameters
    moveLogRect = p.Rect(BOARD_WIDTH, 0, MENU_PANEL_WIDTH, MENU_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color('gray'), moveLogRect)

    # Button dimensions and positions
    button_width = 50
    button_height = 50
    button_margin = 5

    # Calculate the starting X-coordinate to center the buttons
    button_x = BOARD_WIDTH + button_margin * 2
    button_y = button_margin

    # Load and resize button images
    reset_image = p.image.load("images/restart.png")
    reset_image = p.transform.scale(reset_image, (button_width, button_height))

    undo_image = p.image.load("images/undo.png")
    undo_image = p.transform.scale(undo_image, (button_width, button_height))

    if (soundOn):
        sound_image = p.image.load("images/unmute.png")
    else:
        sound_image = p.image.load("images/mute.png")
    sound_image = p.transform.scale(sound_image, (button_width, button_height))

    # Draw Reset button
    reset_button_rect = p.Rect(button_x, button_y, button_width, button_height)
    screen.blit(reset_image, (button_x, button_y))  # Draw image

    # Draw Undo button
    undo_button_rect = p.Rect(button_x + button_width + button_margin, button_y, button_width, button_height)
    screen.blit(undo_image, (button_x + button_width + button_margin, button_y))  # Draw image

    # Draw Mute button
    sound_button_rect = p.Rect(button_x + 2 * (button_width + button_margin), button_y, button_width, button_height)
    screen.blit(sound_image, (button_x + 2 * (button_width + button_margin), button_y))  # Draw image

    # Line spacer between buttons and sections
    line_rect = p.Rect(BOARD_WIDTH, button_y + button_height + button_margin, MENU_PANEL_WIDTH, 2)
    p.draw.rect(screen, p.Color('black'), line_rect)

    # Vertical line to create two sections
    vertical_line_rect = p.Rect(BOARD_WIDTH + MENU_PANEL_WIDTH // 2, button_y + button_height + button_margin, 2, MENU_PANEL_HEIGHT - (button_y + button_height + button_margin))
    p.draw.rect(screen, p.Color('black'), vertical_line_rect)

    # Headers for sections
    font = p.font.SysFont('calibri', 20)

    # Button names and functions for each section
    white_buttons = [{'name': 'human', 'function': handle_human_click_white}, {'name': 'minmax', 'function': handle_minmax_click_white},
                    {'name': 'negamax', 'function': handle_negamax_click_white}, {'name': 'lc0', 'function': handle_lc0_click_white},
                    {'name': 'fatFritz2', 'function': handle_fatFritz2_click_white}, {'name': 'stockfish', 'function': handle_stockfish_click_white}]

    black_buttons = [{'name': 'human', 'function': handle_human_click_black}, {'name': 'minmax', 'function': handle_minmax_click_black},
                    {'name': 'negamax', 'function': handle_negamax_click_black}, {'name': 'lc0', 'function': handle_lc0_click_black},
                    {'name': 'fatFritz2', 'function': handle_fatFritz2_click_black}, {'name': 'stockfish', 'function': handle_stockfish_click_black}]

    # Draw buttons below the WHITE section in two columns
    for i, button_info in enumerate(white_buttons):
        button_width = 100  # Set the desired width for the buttons
        button_height = 30  # Set the desired height for the buttons
        col = i % 2  # Determine the column (0 or 1)
        row = i // 2  # Determine the row
        button_rect = p.Rect(BOARD_WIDTH + 10 + col * (button_width + button_margin * 2),
                            button_y + button_height + button_margin * 3 + font.get_height() + row * (button_height + button_margin),
                            button_width, button_height)
        if (button_info['name'].upper() == engineSelectedWhite):
            p.draw.rect(screen, p.Color('#50C878'), button_rect)
        else:
            p.draw.rect(screen, p.Color('white'), button_rect)
        p.draw.rect(screen, p.Color('black'), button_rect, 2)  # Add border
        button_text = font.render(button_info['name'], True, p.Color('black'))
        screen.blit(button_text, (button_rect.x + button_width // 2 - button_text.get_width() // 2,
                                button_rect.y + button_height // 2 - button_text.get_height() // 2 + 4))

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
        if (button_info['name'].upper() == engineSelectedBlack):
            p.draw.rect(screen, p.Color('#50C878'), button_rect)
        else:
            p.draw.rect(screen, p.Color('black'), button_rect)
        p.draw.rect(screen, p.Color('white'), button_rect, 2)  # Add border
        button_text = font.render(button_info['name'], True, p.Color('white'))
        screen.blit(button_text, (button_rect.x + button_width // 2 - button_text.get_width() // 2,
                                button_rect.y + button_height // 2 - button_text.get_height() // 2 + 4))

        # Check for button clicks
        if button_rect.collidepoint(mouse_pos) and click:
            button_info['function']()

    # buttons to change engine properties
    button_x = BOARD_WIDTH + 5 * 2
    button_y = 170
    # Button dimensions and positions
    button_width = 50
    button_height = 50

    #  TODO make button ojects and normal sizes logic (more responsive)

    ### WHITE BUTTONS ENGINE
    # Load and resize button images
    minus_time_white_button_image = p.image.load("images/minus.png")
    # Draw Reset button
    minus_time_white_button_rect = p.Rect(button_x, button_y, button_width, button_height)
    screen.blit(minus_time_white_button_image, (button_x, button_y))  # Draw image

    button_x += 70
    # Load and resize button images
    plus_time_white_button_image = p.image.load("images/plus.png")
    # Draw Reset button
    plus_time_white_button_rect = p.Rect(button_x, button_y, button_width, button_height)
    screen.blit(plus_time_white_button_image, (button_x, button_y))  # Draw image

    button_x += 40
    minus_depth_white_button_image = p.image.load("images/minus.png")
    # Draw Reset button
    minus_depth_white_button_rect = p.Rect(button_x, button_y, button_width, button_height)
    screen.blit(minus_depth_white_button_image, (button_x, button_y))  # Draw image

    button_x += 70
    plus_depth_white_button_image = p.image.load("images/plus.png")
    # Draw Reset button
    plus_depth_white_button_rect = p.Rect(button_x, button_y, button_width, button_height)
    screen.blit(plus_depth_white_button_image, (button_x, button_y))  # Draw image


    ### BLACK BUTTONS ENGINE
    # Load and resize button images
    minus_time_black_button_image = p.image.load("images/minus.png")
    # Draw Reset button
    minus_time_black_button_rect = p.Rect(button_x, button_y, button_width, button_height)
    screen.blit(minus_time_black_button_image, (button_x, button_y))  # Draw image

    button_x += 70
    # Load and resize button images
    plus_time_black_button_image = p.image.load("images/plus.png")
    # Draw Reset button
    plus_time_black_button_rect = p.Rect(button_x, button_y, button_width, button_height)
    screen.blit(plus_time_black_button_image, (button_x, button_y))  # Draw image

    button_x += 40
    minus_depth_black_button_image = p.image.load("images/minus.png")
    # Draw Reset button
    minus_depth_black_button_rect = p.Rect(button_x, button_y, button_width, button_height)
    screen.blit(minus_depth_black_button_image, (button_x, button_y))  # Draw image

    button_x += 70
    plus_depth_black_button_image = p.image.load("images/plus.png")
    # Draw Reset button
    plus_depth_black_button_rect = p.Rect(button_x, button_y, button_width, button_height)
    screen.blit(plus_depth_black_button_image, (button_x, button_y))  # Draw image
    

    # Check for button clicks
    if click:
        if reset_button_rect.collidepoint(mouse_pos):
            global resetGame
            resetGame = True

        if undo_button_rect.collidepoint(mouse_pos):
            global undoMove
            undoMove = True

        if sound_button_rect.collidepoint(mouse_pos):
            # Button dimensions and positions
            soundOn = not soundOn

        if minus_time_white_button_rect.collidepoint(mouse_pos):
            engineParameters[0] -= 1

        if plus_time_white_button_rect.collidepoint(mouse_pos):
            engineParameters[0] += 1

        if minus_depth_white_button_rect.collidepoint(mouse_pos):
            engineParameters[1] -= 1

        if plus_depth_white_button_rect.collidepoint(mouse_pos):
            engineParameters[1] += 1

        
                

def updateEngineParameters(index, ):
    global engineParameters





# biale
def handle_human_click_white():
    global engineSelectedWhite
    engineSelectedWhite = 'HUMAN'
    global resetGame
    resetGame = True

def handle_minmax_click_white():
    global engineSelectedWhite
    engineSelectedWhite = 'MINMAX'
    global resetGame
    resetGame = True

def handle_negamax_click_white():
    global engineSelectedWhite
    engineSelectedWhite = 'NEGAMAX'
    global resetGame
    resetGame = True

def handle_lc0_click_white():
    global engineSelectedWhite
    engineSelectedWhite = 'LC0'
    global resetGame
    resetGame = True

def handle_fatFritz2_click_white():
    global engineSelectedWhite
    engineSelectedWhite = 'FATFRITZ2'
    global resetGame
    resetGame = True

def handle_stockfish_click_white():
    global engineSelectedWhite
    engineSelectedWhite = 'STOCKFISH'
    global resetGame
    resetGame = True

#czarne
def handle_human_click_black():
    global engineSelectedBlack
    engineSelectedBlack = 'HUMAN'
    global resetGame
    resetGame = True

def handle_minmax_click_black():
    global engineSelectedBlack
    engineSelectedBlack = 'MINMAX'
    global resetGame
    resetGame = True

def handle_negamax_click_black():
    global engineSelectedBlack
    engineSelectedBlack = 'NEGAMAX'
    global resetGame
    resetGame = True

def handle_lc0_click_black():
    global engineSelectedBlack
    engineSelectedBlack = 'LC0'
    global resetGame
    resetGame = True

def handle_fatFritz2_click_black():
    global engineSelectedBlack
    engineSelectedBlack = 'FATFRITZ2'
    global resetGame
    resetGame = True

def handle_stockfish_click_black():
    global engineSelectedBlack
    engineSelectedBlack = 'STOCKFISH'
    global resetGame
    resetGame = True







'''
Animating a move
'''
def animateMove(move, screen, board):
    clock = p.time.Clock()
    clock.tick(MAX_FPS)
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 6 #frames to move one square
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
