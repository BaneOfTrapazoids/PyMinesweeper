import pygame
import sys
from time import sleep
from random import randint

pygame.init()

screen = pygame.display.set_mode((500,500))
Arial = pygame.font.Font("C:/Windows/Fonts/Arial.ttf", 30)

button_tile = pygame.image.load("minesweeper_pics/Button.png")
button_clicked = pygame.image.load("minesweeper_pics/Button_Clicked.png")
bomb_clicked = pygame.image.load("minesweeper_pics/Bomb.png")
flag = pygame.image.load("minesweeper_pics/Flag.png")

#sets the text and colours for each of the symbols that says how many adjacent bombs there are
one_text = Arial.render("1", True, (0,0,255))
two_text = Arial.render("2", True, (0,255,0))
three_text = Arial.render("3", True, (255,0,0))
four_text = Arial.render("4", True, (255,0,255))
five_text = Arial.render("5", True, (255,150,0))
six_text = Arial.render("6", True, (0,206,209))
seven_text = Arial.render("7", True, (0,0,0))
eight_text = Arial.render("8", True, (40,40,40))

game_over_text = Arial.render("GAME OVER", True, (0,0,0))

#the None value is a placeholder for the class and the first 0 is whether or not it's been revealed, and the second 0 is for whether or not there's a flag there
game_map = [[x, y, None, 0, 0] for y in range(10) for x in range(10)]


#a class for tiles
class Tile():
    def __init__(self, x_coord, y_coord, bomb_num, has_bomb):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.bomb_num = bomb_num
        self.has_bomb = has_bomb
    
    #returns the attributes of all adjacent tiles
    def get_adjacent_values(self, pos):
        game_tile = game_map[pos]
        #checks if the tile is in the center pieces
        if game_tile[0] in range(1,9) and game_tile[1] in range(1,9):
            #a list of all adjacent tiles' values starting at the tile above the tile being focused on and moves clockwise
            adjacent_values = [
                (game_map[pos-10][2].x_coord, game_map[pos-10][2].y_coord, game_map[pos-10][2].bomb_num, game_map[pos-10][2].has_bomb, -10),
                (game_map[pos-9][2].x_coord, game_map[pos-9][2].y_coord, game_map[pos-9][2].bomb_num, game_map[pos-9][2].has_bomb, -9),
                (game_map[pos+1][2].x_coord, game_map[pos+1][2].y_coord, game_map[pos+1][2].bomb_num, game_map[pos+1][2].has_bomb, +1),
                (game_map[pos+11][2].x_coord, game_map[pos+11][2].y_coord, game_map[pos+11][2].bomb_num, game_map[pos+11][2].has_bomb, +11),
                (game_map[pos+10][2].x_coord, game_map[pos+10][2].y_coord, game_map[pos+10][2].bomb_num, game_map[pos+10][2].has_bomb, +10),
                (game_map[pos+9][2].x_coord, game_map[pos+9][2].y_coord, game_map[pos+9][2].bomb_num, game_map[pos+9][2].has_bomb, +9),
                (game_map[pos-1][2].x_coord, game_map[pos-1][2].y_coord, game_map[pos-1][2].bomb_num, game_map[pos-1][2].has_bomb, -1),
                (game_map[pos-11][2].x_coord, game_map[pos-11][2].y_coord, game_map[pos-11][2].bomb_num, game_map[pos-11][2].has_bomb, -11)]
        
        #checks if the tile is the top left corner
        elif game_tile[0] == 0 and game_tile[1] == 0:
            adjacent_values = [
                (game_map[pos+1][2].x_coord, game_map[pos+1][2].y_coord, game_map[pos+1][2].bomb_num, game_map[pos+1][2].has_bomb, +1),
                (game_map[pos+11][2].x_coord, game_map[pos+11][2].y_coord, game_map[pos+11][2].bomb_num, game_map[pos+11][2].has_bomb, +11),
                (game_map[pos+10][2].x_coord, game_map[pos+10][2].y_coord, game_map[pos+10][2].bomb_num, game_map[pos+10][2].has_bomb, +10)]

        #checks if the tile is on the top edge
        elif game_tile[0] in range(1,9) and game_tile[1] == 0:
            adjacent_values = [
                (game_map[pos+1][2].x_coord, game_map[pos+1][2].y_coord, game_map[pos+1][2].bomb_num, game_map[pos+1][2].has_bomb, +1),
                (game_map[pos+11][2].x_coord, game_map[pos+11][2].y_coord, game_map[pos+11][2].bomb_num, game_map[pos+11][2].has_bomb, +11),
                (game_map[pos+10][2].x_coord, game_map[pos+10][2].y_coord, game_map[pos+10][2].bomb_num, game_map[pos+10][2].has_bomb, +10),
                (game_map[pos+9][2].x_coord, game_map[pos+9][2].y_coord, game_map[pos+9][2].bomb_num, game_map[pos+9][2].has_bomb, +9),
                (game_map[pos-1][2].x_coord, game_map[pos-1][2].y_coord, game_map[pos-1][2].bomb_num, game_map[pos-1][2].has_bomb, -1)]

        #checks if the tile is the top right corner
        elif game_tile[0] == 9 and game_tile[1] == 0:
            adjacent_values = [
                (game_map[pos+10][2].x_coord, game_map[pos+10][2].y_coord, game_map[pos+10][2].bomb_num, game_map[pos+10][2].has_bomb, +10),
                (game_map[pos+9][2].x_coord, game_map[pos+9][2].y_coord, game_map[pos+9][2].bomb_num, game_map[pos+9][2].has_bomb, +9),
                (game_map[pos-1][2].x_coord, game_map[pos-1][2].y_coord, game_map[pos-1][2].bomb_num, game_map[pos-1][2].has_bomb, -1)]

        #checks if the tile is on the right edge
        elif game_tile[0] == 9 and game_tile[1] in range(1,9):
            adjacent_values = [
                (game_map[pos-10][2].x_coord, game_map[pos-10][2].y_coord, game_map[pos-10][2].bomb_num, game_map[pos-10][2].has_bomb, -10),
                (game_map[pos+10][2].x_coord, game_map[pos+10][2].y_coord, game_map[pos+10][2].bomb_num, game_map[pos+10][2].has_bomb, +10),
                (game_map[pos+9][2].x_coord, game_map[pos+9][2].y_coord, game_map[pos+9][2].bomb_num, game_map[pos+9][2].has_bomb, +9),
                (game_map[pos-1][2].x_coord, game_map[pos-1][2].y_coord, game_map[pos-1][2].bomb_num, game_map[pos-1][2].has_bomb, -1),
                (game_map[pos-11][2].x_coord, game_map[pos-11][2].y_coord, game_map[pos-11][2].bomb_num, game_map[pos-11][2].has_bomb, -11)]

        #checks if the tile is the bottom right corner
        elif game_tile[0] == 9 and game_tile[1] == 9:
            adjacent_values = [
                (game_map[pos-10][2].x_coord, game_map[pos-10][2].y_coord, game_map[pos-10][2].bomb_num, game_map[pos-10][2].has_bomb, -10),
                (game_map[pos-1][2].x_coord, game_map[pos-1][2].y_coord, game_map[pos-1][2].bomb_num, game_map[pos-1][2].has_bomb, -1),
                (game_map[pos-11][2].x_coord, game_map[pos-11][2].y_coord, game_map[pos-11][2].bomb_num, game_map[pos-11][2].has_bomb, -11)]
        #checks if the tile is on the bottome edge
        elif game_tile[0] in range(1,9) and game_tile[1] == 9:
            adjacent_values = [
                (game_map[pos-10][2].x_coord, game_map[pos-10][2].y_coord, game_map[pos-10][2].bomb_num, game_map[pos-10][2].has_bomb, -10),
                (game_map[pos-9][2].x_coord, game_map[pos-9][2].y_coord, game_map[pos-9][2].bomb_num, game_map[pos-9][2].has_bomb, -9),
                (game_map[pos+1][2].x_coord, game_map[pos+1][2].y_coord, game_map[pos+1][2].bomb_num, game_map[pos+1][2].has_bomb, +1),
                (game_map[pos-1][2].x_coord, game_map[pos-1][2].y_coord, game_map[pos-1][2].bomb_num, game_map[pos-1][2].has_bomb, -1),
                (game_map[pos-11][2].x_coord, game_map[pos-11][2].y_coord, game_map[pos-11][2].bomb_num, game_map[pos-11][2].has_bomb, -11)]
        #checks if the tile is the bottom left corner
        elif game_tile[0] == 0 and game_tile[1] == 9:
            adjacent_values = [
                (game_map[pos-10][2].x_coord, game_map[pos-10][2].y_coord, game_map[pos-10][2].bomb_num, game_map[pos-10][2].has_bomb, -10),
                (game_map[pos-9][2].x_coord, game_map[pos-9][2].y_coord, game_map[pos-9][2].bomb_num, game_map[pos-9][2].has_bomb, -9),
                (game_map[pos+1][2].x_coord, game_map[pos+1][2].y_coord, game_map[pos+1][2].bomb_num, game_map[pos+1][2].has_bomb, +1)]
        #checks if the tile is on the left edge
        elif game_tile[0] == 0 and game_tile[1] in range(1,9):
            adjacent_values = [
                (game_map[pos-10][2].x_coord, game_map[pos-10][2].y_coord, game_map[pos-10][2].bomb_num, game_map[pos-10][2].has_bomb, -10),
                (game_map[pos-9][2].x_coord, game_map[pos-9][2].y_coord, game_map[pos-9][2].bomb_num, game_map[pos-9][2].has_bomb, -9),
                (game_map[pos+1][2].x_coord, game_map[pos+1][2].y_coord, game_map[pos+1][2].bomb_num, game_map[pos+1][2].has_bomb, +1),
                (game_map[pos+11][2].x_coord, game_map[pos+11][2].y_coord, game_map[pos+11][2].bomb_num, game_map[pos+11][2].has_bomb, +11),
                (game_map[pos+10][2].x_coord, game_map[pos+10][2].y_coord, game_map[pos+10][2].bomb_num, game_map[pos+10][2].has_bomb, +10)]
        return adjacent_values

#calculates the amount of adjacent bombs for each tile and presets the starting tile to not have a bomb
def map_initializing(preset):
    preset[2].has_bomb = 0

    for i in range(100):

        #the current tile being worked on
        game_tile = game_map[i]

        adjacent_values = game_tile[2].get_adjacent_values(i)
        bomb_value = 0
        for attribute in adjacent_values:
            bomb_value += attribute[3]
        game_tile[2].bomb_num = bomb_value

def Game_Over():
    screen.blit(game_over_text, (200, 200))
    pygame.display.update()
    print("game over")
    sleep(3)
    pygame.quit()
    sys.exit()

#used to make sure you're only clicking one tile at a time
debounce = False

#all the code for buttons
def button_press():
    global debounce
    
    #pairs of bomb numbers and what text to render for that number
    bomb_num_dict = {
        0:button_clicked, 
        1:one_text,
        2:two_text,
        3:three_text,
        4:four_text,
        5:five_text,
        6:six_text,
        7:seven_text,
        8:eight_text
    }
    #detects what buttons are being pressed under certain conditions for each tile and executes code accordingly
    for i in range(100):
        game_tile = game_map[i]
        #detects if a tile is being left clicked to reveal it
        if game_tile[2].x_coord+50 > mouse_pos[0] > game_tile[2].x_coord and game_tile[2].y_coord+50 > mouse_pos[1] > game_tile[2].y_coord and mouse_buttons[0] == True and debounce == False:
            debounce = True
            #if it has a bomb, then end the game
            if game_tile[2].has_bomb == 1:
                screen.blit(bomb_clicked, (game_tile[2].x_coord, game_tile[2].y_coord))
                Game_Over()
            
            #if there's no bomb but it is adjacent to 1 or more bombs, then reveal it but put the right bomb number text
            elif game_tile[2].bomb_num > 0:
                screen.blit(button_clicked, (game_tile[2].x_coord, game_tile[2].y_coord))
                screen.blit(bomb_num_dict.get(game_tile[2].bomb_num), (game_tile[2].x_coord+15, game_tile[2].y_coord+10))

            #if there's no bomb and no adjacent bombs, then just reveal it
            elif game_tile[2].bomb_num == 0:
                screen.blit(button_clicked, (game_tile[2].x_coord, game_tile[2].y_coord))
        
        #detects if a tile is being right clicked to place a flag
        if game_tile[2].x_coord+50 > mouse_pos[0] > game_tile[2].x_coord and game_tile[2].y_coord+50 > mouse_pos[1] > game_tile[2].y_coord and mouse_buttons[2] == True and game_tile[3] == 0 and debounce == False:
            if game_tile[4] == 0:
                screen.blit(flag, (game_tile[2].x_coord, game_tile[2].y_coord))
                game_tile[4] = 1
                debounce = True
            elif game_tile[4] == 1:
                screen.blit(button_tile, (game_tile[2].x_coord, game_tile[2].y_coord))
                game_tile[4] = 0
                debounce = True
            
                
#draws all the tiles on the screen at the start of the game
def tile_drawing():
    for i in range(100):
        #makes a class for the tile in the third position of each tile
        game_map[i][2] = Tile(game_map[i][0]*50, game_map[i][1]*50, 0, 0)

        #puts the picture of each tile onto the screen before the game starts
        screen.blit(button_tile, (game_map[i][2].x_coord, game_map[i][2].y_coord))

    #places 20 bombs randomly around the map
    for i in range(20):
        game_map[randint(0,99)][2].has_bomb = 1
    
def start_detector():
    global times_run

    pairs_list = [[(range(x*50,x*50+50)), (range(y*50,y*50+50)), game_map[int(f"{y}{x}")]] for y in range(10) for x in range(10)]
    for i in range(100):
        if mouse_pos[0] in pairs_list[i][0] and mouse_pos[1] in pairs_list[i][1] and mouse_buttons[0]:
            times_run += 1
            return pairs_list[i][2]

times_run = 0

while True:
    global mouse_pos
    global mouse_buttons
    mouse_pos = pygame.mouse.get_pos()
    mouse_buttons = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if mouse_buttons[0] == False and mouse_buttons[2] == False:
        debounce = False

    if times_run == 0:
        tile_drawing()
        pygame.display.update()

    if times_run == 0 and mouse_buttons[0]:
        preset_tile = start_detector()
        map_initializing(preset_tile)
        
    if times_run > 0:
        button_press()
        pygame.display.update()