import random
import pygame
# Imports a file, reads to list, and returns a random string in that list, split into a list.
def init_input(name):

    file_object = open(name)
    line = file_object.readline()
    temp_list = []
    while line:
        temp_list.append(line[0:-1])
        line = file_object.readline()
    file_object.close()
    temp_rand = random.randint(1, 900)
    temp_out = list(temp_list[temp_rand])
    temp_out.append(" ")
    temp_out[0].capitalize()
    print("You have to make the word: " + str("".join(temp_out)).capitalize())
    return temp_out, temp_out
class tile:
    def __init__(self, list, index, buffer, size):
        self.xgrid = index
        self.ygrid = list
        self.xPos = buffer + self.xgrid*size
        self.yPos = buffer + self.ygrid*size
        self.rectDraw = [self.xPos, self.yPos, size, size]
# Checks if the user has attempted to quit the game via the quit button or escape key
def check_running(key):
    tempRun = True
    for event in key:
        if event.type == pygame.QUIT:
            tempRun = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            tempRun = False
    return tempRun
# Checks if the user has clicked a key, and if so returns an assigned value to that specific key.
def movement(key):
    for item in key:
        if item.type == pygame.KEYDOWN:
            if item.key == pygame.K_w:
                return 1
            if item.key == pygame.K_a:
                return 2
            if item.key == pygame.K_s:
                return 3
            if item.key == pygame.K_d:
                return 4
    return -1
# Manages all the movement involved in thhe program when a user presses a key
def total_movement(total_list, key):
    while True:

        this_turn = movement(key)
        if this_turn != -1:
            blank_list, blank_index = find_blank(total_list)
            letter_list, letter_index = moved(blank_list, blank_index, this_turn)
            if check_possible(letter_list, letter_index):
                switch(total_list, blank_list, blank_index, letter_list, letter_index)
                return 1
            else:
                return 0

        else:
            return 0
# Makes the gameboard do a random shuffle by moving fifty peices indiviually and random,y
def shuffle_list(total_list):
    for i in range(50):
        random_temp = random.randrange(1,5)
        b_list_temp, b_index_temp = find_blank(total_list)

        l_list_temp, l_index_temp = moved(b_list_temp, b_index_temp, random_temp)

        if check_possible(l_list_temp, l_index_temp):
            switch(total_list, b_list_temp, b_index_temp, l_list_temp, l_index_temp)
# Writes the letters to the screen by utilising the length, fontsize, and buffer
def write_letters(screen, total_list, buffer, length, font):
    for list in range(len(total_list)):
        for item in range(len(total_list[list])):
            colour = (255, 255, 255)
            text_render = font.render(total_list[list][item], 1, colour)
            text_rect = text_render.get_rect()
            text_rect.centerx = buffer + item*length + length/2
            text_rect.centery = buffer + list*length + length/2
            screen.blit(text_render, text_rect)
# Writes the score to the screen
def write_score(screen, score, font, size):

    text = "Current Score: %s" % (str(score))
    score_render = font.render(text, 1, (0,0,0))
    score_rect = score_render.get_rect()
    score_rect.centery = size - 30
    score_rect.centerx = screen.get_rect().centerx
    screen.blit(score_render, score_rect)
# This checks if the position of the letters are in the correct position when refered to
# the position of the completed board.
def check_complete(total, complete):
    temp_total = []
    for list in total:
        for item in list:
            temp_total.append(item)
    if temp_total == complete:
        return True
    else:
        return False
# Draws all of the squares to theh screen
def draw(list, screen):
    for item in list:
        pygame.draw.rect(screen, (0,0,0), item.rectDraw)
# Finds the location of the blank square
def find_blank(total):
    for list in range(len(total)):
        for item in range(len(total[list])):
            if total[list][item] == " ":
                return list, item
# Finds which square has to be moved with the location of the blank square and the position the player made
def moved(blank_list, blank_index, movement):
    if movement == 1:
        return blank_list+1, blank_index
    if movement == 2:
        return blank_list, blank_index+1
    if movement == 3:
        return blank_list-1, blank_index
    if movement == 4:
        return blank_list, blank_index-1
# Switches two variables
def switch(total, blank_list, blank_index, letter_list, letter_index):
    total[blank_list][blank_index], total[letter_list][letter_index] = total[letter_list][letter_index], total[blank_list][blank_index]
# Checks if the move that the player wishes to make is possible
def check_possible(list, index):
    if list > 2 or index > 2:
        return False
    elif list < 0 or index < 0:
        return False
    else:
        return True
# Initialises the list for the game
def initialise_lists(file):
    random_list, complete_list = init_input(file)
    total_list = list_to_three(random_list)
    shuffle_list(total_list)
    return total_list, complete_list

class highscore:
    def __init__(self, score, name):
        self.score = score
        self.name = name
# Opens the file in which the high score is saved, then checks where and if the current score is in it
# If it fits in the list it will add it to the list at the correct position and remove any item
# from the list if the list length is > 10
def highscores(file, score):

    file_object = open(file)
    line = file_object.readline()
    temp_scores = []
    temp_names = []
    while line:
        score_temp, score_name = line[:-1].split()
        temp_scores.append(highscore(score_temp, score_name))
        line = file_object.readline()
    file_object.close()

    position = -1
    for item in range(len(temp_scores)):
        if int(temp_scores[item].score) > score:
            position = item
            break
    if position != -1:
        print("New score at position %s on the leaderboard!" % (position+1))
        users_name = input("What is your name? ")
        temp_scores.insert(position, highscore(score, users_name))
        if len(temp_scores) > 10:
            temp_scores.pop()
        temp_file = open(file, "w")
        for item in temp_scores:
            temp_file.write(str(item.score) + " " + item.name + "\n")
        temp_file.close()

    for item in range(len(temp_scores)):
        print("%s. %s by %s" % (str(item+1), str(temp_scores[item].score), str(temp_scores[item].name)))
# Converts the full list of letters to three seperate letters
def list_to_three(list):
    temp_list = [[],[],[]]
    for i in range(3):
        for j in range(3):
            temp_list[i].append(list[j+i*3])
    return temp_list
