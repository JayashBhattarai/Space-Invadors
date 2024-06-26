import pygame
import random
import math
from pygame import mixer

# pygame initialising
pygame.init()  # IMPORTANT

# Creating the screen
screen = pygame.display.set_mode((800, 600))

# setting background
background = pygame.image.load('background.png')

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)                    # -1 to play for loop

# Title and Icon
pygame.display.set_caption("Space Invaders")  # title changed
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)  # setting the image to icon

# Player
playerImg = pygame.image.load('user.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
number_of_enemy = 6

for i in range(number_of_enemy):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 735))  # spawn in random x-axis
    enemyY.append(random.randint(50, 100))  # spawn in random y-axis
    enemyX_change.append(2)
    enemyY_change.append(40)

# Bullet
# when READY bullet doesn't appear on screen
# when FIRE bullet moves vertically
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480  # top of the spaceship
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 128)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (350, 200))


def player(x, y):
    screen.blit(playerImg, (x, y))  # drawing on the screen loading the image and the coordinates to appear on


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state  # to access from inside the function
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))  # 16 to be in middle and 10 to be a little above spaceship


# collision function
def isCollision(enemyX, enemyY, bulletX, bulletY, i):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# loop for the game
running = True
while running:

    # RGB up to 255
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # check for key presses right or left
        if event.type == pygame.KEYDOWN:  # KEYDOWN checks if key is pressed
            if event.key == pygame.K_LEFT:
                playerX_change = -3.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 3.5
            if event.key == pygame.K_SPACE:  # space to fire bullet
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:  # KEYUP checks if the key is released
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # to not go beyond the screen
    playerX += playerX_change  # changing the X coordinate accordingly
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # to not go beyond the screen
    for i in range(number_of_enemy):

        # Game Over
        if enemyY[i] > 440:
            for j in range(number_of_enemy):
                enemyY[j] = 1000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]  # changing the X coordinate accordingly
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY, i)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            # print(score_value)
            enemyY[i] = random.randint(50, 150)
            enemyX[i] = random.randint(0, 735)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement

    # multiple bullet
    if bulletY <= 0:  # beyond screen then reset
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()  # IMPORTANT to update every thing you do
