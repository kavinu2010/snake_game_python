import pygame
import random

# Initialize Pygame
pygame.init()

# Screen Dimensions
width_of_screen = 900
height_of_screen = 600

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
pink = (255, 182, 193)

# Create Window
gameWindow = pygame.display.set_mode((width_of_screen, height_of_screen))
pygame.display.set_caption("Python Snake Game")
clock = pygame.time.Clock()

# Font Initialization
font = pygame.font.SysFont(None, 35)

# Function to Display Score on Screen
def score_on_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

# Function to Plot Snake
def plot_snake(gameWindow, color, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

# Welcome Screen
def welcome():
    game_exit = False
    while not game_exit:
        gameWindow.fill(pink)
        score_on_screen("Welcome to Snakes Game by PythonGeeks", black, 90, 250)
        score_on_screen("Press SPACEBAR to Play", black, 232, 290)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game()
        pygame.display.update()
        clock.tick(60)

# Game Loop
def game():
    game_exit = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    init_velocity = 5
    score = 0
    apple_x = random.randint(20, width_of_screen // 2)
    apple_y = random.randint(20, height_of_screen // 2)
    snake_size = 30
    snake_list = []
    snake_length = 1
    fps = 40

    # Load Highscore
    try:
      with open("highscore.txt", "r") as f:
        highscore = f.read()
    except FileNotFoundError:
    # If the file doesn't exist, create it with a highscore of 0
      with open("highscore.txt", "w") as f:
        f.write("0")
      highscore = "0"


    while not game_exit:
        if game_over:
            # Save Highscore
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))
            gameWindow.fill(white)
            score_on_screen("Game Over! Press ENTER to Continue", red, 100, 250)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

            snake_x += velocity_x
            snake_y += velocity_y

            # Detect Collision with Apple
            if abs(snake_x - apple_x) < 20 and abs(snake_y - apple_y) < 20:
                score += 10
                apple_x = random.randint(20, width_of_screen // 2)
                apple_y = random.randint(20, height_of_screen // 2)
                snake_length += 5
                if score > int(highscore):
                    highscore = score

            # Update the Game Window
            gameWindow.fill(white)
            score_on_screen("Score: " + str(score) + " Highscore: " + str(highscore), red, 5, 5)
            pygame.draw.rect(gameWindow, red, [apple_x, apple_y, snake_size, snake_size])

            # Snake Movement
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list) > snake_length:
                del snake_list[0]

            # Detect Snake Collision
            if head in snake_list[:-1]:
                game_over = True
            if snake_x < 0 or snake_x > width_of_screen or snake_y < 0 or snake_y > height_of_screen:
                game_over = True

            plot_snake(gameWindow, black, snake_list, snake_size)
            pygame.display.update()
            clock.tick(fps)

    pygame.quit()
    quit()

# Start the Game
welcome()
