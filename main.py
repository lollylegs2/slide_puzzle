import pygame
from functions import *

pygame.init()
pygame.font.init()


turns = 0
screenColor = (255, 255, 255)
tile_size = 75
tile_buffer = tile_size * 2
running = True
complete = False
font = pygame.font.Font(None, tile_size)
screenSize = tile_buffer * 2 + 3*tile_size


clock = pygame.time.Clock()
screen = pygame.display.set_mode((screenSize, screenSize))

total_list, complete_list = initialise_lists("8words.txt")

rect_list = []
for i in range(3):
    for j in range(3):
        rect_list.append(tile(i, j, tile_buffer, tile_size))


while running == True:
    clock.tick(30)
    key = pygame.event.get()
    running = check_running(key)
    screen.fill(screenColor)
    turns += total_movement(total_list, key)
    draw(rect_list, screen)
    write_letters(screen, total_list, tile_buffer, tile_size, font)
    write_score(screen, turns, font, screenSize)
    pygame.display.flip()
    if check_complete(total_list, complete_list):
        print("Congratulations! You won after only %s turns!" % (str(turns)))
        complete = True
        break

pygame.display.quit()
pygame.quit()
if complete == True:
    highscores("highscore.txt", turns)
