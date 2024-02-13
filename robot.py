#Hello to the game "Robot vs Monser"
#This game is played with 2 players, one controls the Robot with A and D keys and the other controls the Monster with the left and right arrow keys.
#The goal is to be the first to gain 10 points
#You can gain points by touching the coins
#However, if you touch the doors, you lose points
#I hope you have fun :)

import pygame
from random import randint

def initialize_game():
    pygame.init()
    width, height = 640, 480
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Robot vs Monster")
    return width, height, window

def load_images():
    monster = pygame.image.load("monster.png")
    robot = pygame.image.load("robot.png")
    coin = pygame.image.load("coin.png")
    door = pygame.image.load("door.png")
    return monster, robot, coin, door

def generate_positions(num, width, height):
    positions = []
    for i in range(num):
        positions.append([randint(0, width - coin.get_width()), -randint(100, 1000)])
    return positions

def generate_door_positions(num, width, height):
    door_positions = []
    for i in range(num):
        door_positions.append([randint(0, width - door.get_width()), -randint(100, 1000)])
    return door_positions

def handle_events(to_left, to_right, to_a, to_d):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_left = True
            if event.key == pygame.K_RIGHT:
                to_right = True
            if event.key == pygame.K_a:
                to_a = True
            if event.key == pygame.K_d:
                to_d = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                to_left = False
            if event.key == pygame.K_RIGHT:
                to_right = False
            if event.key == pygame.K_a:
                to_a = False
            if event.key == pygame.K_d:
                to_d = False

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    return to_left, to_right, to_a, to_d

def move_characters(x, y, a, b, to_left, to_right, to_a, to_d):
    if to_right and x < width - monster.get_width():
        x += 2
    if to_left and x > 0:
        x -= 2
    if to_a and a > 0:
        a -= 2
    if to_d and a < width - robot.get_width():
        a += 2

    return x, y, a, b

def update_coin_positions(positions, number, width, height, x, y, a, b, points, points2):
    for i in range(number):
        positions[i][1] += 5
        if positions[i][1] + coin.get_height() >= height:
            positions[i][0] = randint(0, width - coin.get_width())
            positions[i][1] = -randint(100, 1000)

        if positions[i][1] + coin.get_height() >= y:
            monster_middle = x + monster.get_width() / 2
            coin_middle = positions[i][0] + coin.get_width() / 2

            if abs(monster_middle - coin_middle) <= (monster.get_width() + coin.get_width()) / 2:
                positions[i][0] = randint(0, width - coin.get_width())
                positions[i][1] = -randint(100, 1000)
                points += 1

        if positions[i][1] + coin.get_height() >= b:
            robot_middle = a + robot.get_width() / 2
            coin_middle = positions[i][0] + coin.get_width() / 2

            if abs(robot_middle - coin_middle) <= (robot.get_width() + coin.get_width()) / 2:
                positions[i][0] = randint(0, width - coin.get_width())
                positions[i][1] = -randint(100, 1000)
                points2 += 1

    return positions, points, points2

def update_door_positions(door_p, door_num, width, height, x, y, a, b, points, points2):
    for i in range(door_num):
        door_p[i][1] += 5
        if door_p[i][1] + door.get_height() >= height:
            door_p[i][0] = randint(0, width - door.get_width())
            door_p[i][1] = -randint(100, 1000)

        if door_p[i][1] + door.get_height() >= y:
            monster_middle = x + monster.get_width() / 2
            door_middle = door_p[i][0] + door.get_width() / 2
            if abs(monster_middle - door_middle) <= (monster.get_width() + door.get_width()) / 2:
                door_p[i][0] = randint(0, width - door.get_width())
                door_p[i][1] = -randint(100, 1000)
                points -= 1

        if door_p[i][1] + door.get_height() >= b:
            robot_middle = a + robot.get_width() / 2
            door_middle = door_p[i][0] + door.get_width() / 2
            if abs(robot_middle - door_middle) <= (robot.get_width() + door.get_width()) / 2:
                door_p[i][0] = randint(0, width - door.get_width())
                door_p[i][1] = -randint(100, 1000)
                points2 -= 1

    return door_p, points, points2

def check_win_conditions(points, points2):
    if points >= 10:
        return "Monster wins!"
    elif points2 >= 10:
        return "Robot wins!"
    else:
        return None

def main():
    global width, height, monster, robot, coin, door

    width, height, window = initialize_game()
    monster, robot, coin, door = load_images()

    x = width - monster.get_width()
    y = height - monster.get_height()
    a = 0
    b = height - robot.get_height()

    number = 5
    positions = generate_positions(number, width, height)

    door_num = 5
    door_p = generate_door_positions(door_num, width, height)

    to_left, to_right, to_a, to_d = False, False, False, False
    points, points2 = 0, 0

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)

    while True:
        to_left, to_right, to_a, to_d = handle_events(to_left, to_right, to_a, to_d)
        x, y, a, b = move_characters(x, y, a, b, to_left, to_right, to_a, to_d)

        positions, points, points2 = update_coin_positions(positions, number, width, height, x, y, a, b, points, points2)
        door_p, points, points2 = update_door_positions(door_p, door_num, width, height, x, y, a, b, points, points2)

        window.fill((100, 100, 100))
        window.blit(monster, (x, y))
        window.blit(robot, (a, b))
        for i in range(number):
            window.blit(coin, (positions[i][0], positions[i][1]))
        for i in range(door_num):
            window.blit(door, (door_p[i][0], door_p[i][1]))

        text = font.render("Use <+>, Monster Points: " + str(points), True, (255, 0, 0))
        window.blit(text, (330, 10))

        text2 = font.render("Use A+D, Robot Points: " + str(points2), True, (0, 0, 255))
        window.blit(text2, (20, 10))

        text3 = font.render("coins=1 doors=-1 get 10 points to win <3", True, (255, 255, 0))
        window.blit(text3, (100, 40))

        win_message = check_win_conditions(points, points2)
        if win_message:
            win_text = font.render(win_message, True, (255, 255, 0))
            window.blit(win_text, (width / 2 - win_text.get_width() / 2, height / 2 - win_text.get_height() / 2))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()


    
