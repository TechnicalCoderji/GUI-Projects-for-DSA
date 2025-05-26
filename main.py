# For Main Sudoku Logic and Game
import pygame
import saver_loader as SL
# Import Classes from Tools
from tools import ToolButton, FileBrowserBox, InputBox, RemainingButton, GameBoard, Block
# Import Functions from Tools
from tools import blit_text

pygame.init()

# For Screen/Window Basic
WIDTH = 800
HEIGHT = 600
RES = WIDTH,HEIGHT
win = pygame.display.set_mode(RES)
pygame.display.set_caption("SUDOKU - Dip Parmar")
clock = pygame.Clock()
FPS = 30

# Global Variables
font_small = pygame.font.Font(None, 45)
font_small_mini = pygame.font.Font(None, 25)

# Define a color with an alpha value (RGBA)
transparent_color = (0, 0, 0, 150)  # RGB Color with 50% transparency

# Create a surface with transparency
transparent_surface = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
transparent_surface.fill(transparent_color)

# Funtions and Classes

# For Drawing Screen
def draw_win(win:pygame.surface.Surface):

    win.fill((97, 136, 199))

    # For Side-1 Box
    pygame.draw.rect(win, (0,0,0), (30,30,70,510))
    pygame.draw.rect(win, (200,200,200), (30,30,70,510), 5)
    blit_text(win,"Tools",(25,545),font_small,(255,255,255))

    # For Game Board Drawing
    GameBoard.draw(win)

    # For Side-2 Box
    pygame.draw.rect(win, (0,0,0), (700,30,70,510))
    pygame.draw.rect(win, (200,200,200), (700,30,70,510), 5)
    blit_text(win,"Remaining\n  Numbers",(690,545),font_small_mini,(255,255,255))

    # For 1 to 9 buttons
    for i in GameBoard.remaining_numbers:
        if GameBoard.remaining_numbers[i]<9:
            button = buttons[int(i)-1]
            button.draw(win)

    # For Tools Button
    for button in tool_buttons:
        button.draw(win)

    if save_load_screen:
        # For Transparent Background
        win.blit(transparent_surface,(0,0))

        if save_load_screen == "save":
            # For Background Box
            pygame.draw.rect(win,(50,50,50),(250,200,300,200),0,20)
            pygame.draw.rect(win,(200,200,200),(250,200,300,200),5,20)
            pygame.draw.rect(win,(100,100,100),(250,200,300,50),0,border_top_left_radius=20,border_top_right_radius=20)

            blit_text(win,"Save Menu",(265,215),font_small,(255,255,255))
            blit_text(win,"Enter File Name:",(275,260),font_small_mini,(220,220,220))
            # For Input Box Draw
            input_box.draw(win)
            close_button.draw(win) # For Close Button Draw on Screen
            save_button.draw(win) # For Save Button Draw

        else:
            # For Background Box
            pygame.draw.rect(win,(50,50,50),(250,100,300,400),0,20)
            pygame.draw.rect(win,(200,200,200),(250,100,300,400),5,20)
            pygame.draw.rect(win,(100,100,100),(250,100,300,50),0,border_top_left_radius=20,border_top_right_radius=20)
            
            blit_text(win,"Open Menu",(265,115),font_small,(255,255,255))
            blit_text(win,"Select File To Open:",(275,160),font_small_mini,(220,220,220))

            close_button_1.draw(win) # For Close Button Draw on Screen
            filelist_box.draw(win)
            open_button.draw(win)

# For Handling Game events
def handle_event(event):
    if save_load_screen:
        if save_load_screen == "save":
            close_button.handle_event(event)
            save_button.handle_event(event)
            input_box.handle_event(event)

        else:
            close_button_1.handle_event(event)
            open_button.handle_event(event)
            filelist_box.handle_event(event)

    else:

        if event.type == pygame.MOUSEBUTTONDOWN:
            GameBoard.handle_event(event)

        for i in GameBoard.remaining_numbers:
            if GameBoard.remaining_numbers[i]<9:
                button = buttons[int(i)-1]
                button.handle_event(event)

        for button in tool_buttons:
            button.handle_event(event)

        if event.type == pygame.KEYDOWN:
            # For Print Something -- Only for Test
            if event.key == pygame.K_p:
                print(len(GameBoard.undo_stack))

# Functions For Tools
# For Save File
def save_menu_fun():
    global save_load_screen
    save_load_screen = "save"

# For Open File
def open_menu_fun():
    global save_load_screen
    save_load_screen = "open"

# For Undo last move
def undo_fun():
    if GameBoard.undo_stack:
        for pos,i in zip(GameBoard.board,GameBoard.undo_stack.pop()):
            GameBoard.board[pos].text = i

        GameBoard.check_error()

    else:
        print("Not Undo")

# For Erase cell
def eraser_fun():
    box = GameBoard.current_selected_block
    if box and not box.permanent:
        GameBoard.undo_stack.append([GameBoard.board[pos].text for pos in GameBoard.board])
        box.text = None
        GameBoard.check_error()
        RemainingButton.selected_text = None

# For Delete Board(Reset)
def reset_fun():
    GameBoard.undo_stack.append([GameBoard.board[pos].text for pos in GameBoard.board])
    for pos in GameBoard.board:
        box = GameBoard.board[pos]
        if not box.permanent:
            box.text = None

# For Change Pencil Color To White
def whitepen_fun():
    Block.pen_color = (255,255,255)

# For Change Pencil Color To Yellow
def yellowpen_fun():
    Block.pen_color = (255,255,0)

# For Change Pencil Color To Orange
def orangepen_fun():
    Block.pen_color = (255, 165, 0)

# For Delete Entire Board
def delete_fun():
    for pos in GameBoard.board:
        GameBoard.board[pos].text = None
        GameBoard.board[pos].permanent = False
    GameBoard.undo_stack.clear()

# For Close Mini-Window of Save-Load Screen
def close_fun():
    global save_load_screen
    save_load_screen = None

# For Finally Save The File
def save_fun():
    global save_load_screen
    SL.save_sudoku(input_box.text,GameBoard.board)
    save_load_screen = None
    filelist_box.update()

# For Finally Open The File
def open_fun():
    global save_load_screen
    SL.load_sudoku(filelist_box.selected_file,GameBoard.board)
    save_load_screen = None

# Objects
GameBoard.set_board(130,30,540)
buttons = [RemainingButton(710,(55*i)-15,50,50,str(i)) for i in range(1,10)]

# Close Load
close_button_1 = ToolButton(500,105,40,40,"img\close.png","Close",close_fun)
open_button = ToolButton(370,430,60,60,"img\\folder.png","Open",open_fun)
filelist_box = FileBrowserBox(270,180,260,240,"game boards")

# For Save
close_button = ToolButton(500,205,40,40,"img\close.png","Close",close_fun)
input_box = InputBox(270,280,260,40,"mygame")
save_button = ToolButton(370,330,60,60,"img\diskette.png","Save",save_fun)

tool_buttons = [] # For Tool Button List
# Save Tool Button
tool_buttons.append(ToolButton(40,40,50,50,"img\diskette.png","Save",save_menu_fun))
# Open Tool Button
tool_buttons.append(ToolButton(40,95,50,50,"img\\folder.png","Open",open_menu_fun))
# Undo Tool Button
tool_buttons.append(ToolButton(40,150,50,50,"img\\undo.png","Undo",undo_fun))
# Eraser Tool Button
tool_buttons.append(ToolButton(40,205,50,50,"img\eraser.png","Eraser",eraser_fun))
# Reset Tool Button
tool_buttons.append(ToolButton(40,260,50,50,"img\\reset.png","Reset",reset_fun))
# White Pen Button
tool_buttons.append(ToolButton(40,315,50,50,"img\white_pen.png","White",whitepen_fun))
# Yellow Pen Button
tool_buttons.append(ToolButton(40,370,50,50,"img\yellow_pen.png","Yellow",yellowpen_fun))
# Orange Pen Button
tool_buttons.append(ToolButton(40,425,50,50,"img\orange_pen.png","Orange",orangepen_fun))
# Delete Tool Buttom
tool_buttons.append(ToolButton(40,480,50,50,"img\delete.png","Delete",delete_fun))

# Main Function That Start Execution Of Program
def main():
    global save_load_screen
    
    save_load_screen = None

    # For Gameloop
    while True:

        # For Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            # For handle Sudoku Events
            handle_event(event)
            
        # For Drawing Sudoku On Screen
        draw_win(win)

        pygame.display.flip()
        clock.tick(FPS)

if __name__=="__main__":
    main()
    pygame.quit()
    exit()