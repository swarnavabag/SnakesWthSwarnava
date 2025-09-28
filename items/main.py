import pygame
import random

pygame.init()

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
button_color = (59, 83, 35)
hover_color = (80, 120, 70)
text_color = (250, 250, 210)
shadow_color = (220, 235, 180)

# Constants
WIDTH, HEIGHT = 600, 400
FPS = 60
snake_size = 40
apple_size = 30

# Font
score_font = pygame.font.SysFont("comicsansms", 25)
buttons_font = pygame.font.SysFont("Roboto", 25)
gameover_button_font = pygame.font.SysFont("Arial", 30)

# Load assets
intro_screen = pygame.image.load("intro_screen.jpg")
intro_screen = pygame.transform.scale(intro_screen, (WIDTH, HEIGHT))

settings_screen = pygame.image.load("settings_screen.jpg")
settings_screen = pygame.transform.scale(settings_screen, (WIDTH, HEIGHT))

background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

snake_head = pygame.image.load("snake_head.png")
snake_head = pygame.transform.scale(snake_head, (snake_size, snake_size))

snake_body = pygame.image.load("snake_body.png")
snake_body = pygame.transform.scale(snake_body, (snake_size, snake_size))

apple_img = pygame.image.load("apple.png")
apple_img = pygame.transform.scale(apple_img, (apple_size, apple_size))

gameover_screen = pygame.image.load("gameover_screen.png")
gameover_screen = pygame.transform.scale(gameover_screen, (500, 300))

# Game window
game_window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SnakesWthSwarnava")
clock = pygame.time.Clock()

# Function to create buttons


def create_button(text, x, y, width, height, inactive_color, active_color, action=None):
    shadow_offset = 3
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    pygame.draw.rect(game_window, shadow_color, (x + shadow_offset, y + shadow_offset, width, height), border_radius=8)

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(game_window, active_color, (x, y, width, height), border_radius=8)
        if click[0] == 1 and action:
            action()
    else:
        pygame.draw.rect(game_window, inactive_color, (x, y, width, height), border_radius=8)

    button_text = buttons_font.render(text, True, text_color)
    text_rect = button_text.get_rect(center=(x + width // 2, y + height // 2))
    game_window.blit(button_text, text_rect)


def gameover_button(text, x, y, width, height, inactive_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    pygame.draw.rect(game_window, white, (x, y, width, height))

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        if click[0] == 1 and action:
            action()

    button_text = gameover_button_font.render(text, True, text_color)
    text_rect = button_text.get_rect(center=(x + width // 2, y + height // 2))
    game_window.blit(button_text, text_rect)


def quit_game():
    pygame.quit()
    quit()


def create_label(text, x, y):
    label_text = buttons_font.render(text, True, text_color)
    text_rect = label_text.get_rect(center=(x, y))
    game_window.blit(label_text, text_rect)


def load_intro():
    intro_active = True
    while intro_active:
        game_window.blit(intro_screen, (0, 0))
        create_button("Play", 94, 250, 412, 30, button_color, hover_color, lambda: game_loop(2.5, 0.02))
        create_button("Settings", 94, 300, 412, 30, button_color, hover_color, load_settings)
        create_button("Quit", 94, 350, 412, 30, button_color, hover_color, quit_game)

        pygame.display.update()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()


def easy():
    game_loop(2.0, 0.01)


def medium():
    game_loop(2.5, 0.02)


def hard():
    game_loop(3.5, 0.03)


def load_settings():
    settings_active = True
    while settings_active:
        game_window.blit(settings_screen, (0, 0))
        create_label("Select Difficulty", WIDTH // 2, 100)
        create_button("Easy", 94, 150, 412, 30, button_color, hover_color, easy)
        create_button("Medium", 94, 200, 412, 30, button_color, hover_color, medium)
        create_button("Hard", 94, 250, 412, 30, button_color, hover_color, hard)
        create_button("Back", 10, 355, 60, 30, button_color, hover_color, load_intro)
        create_button("Quit", 525, 355, 60, 30, button_color, hover_color, quit_game)

        pygame.display.update()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()


def game_over(score):
    gameover_active = True
    while gameover_active:
        game_window.blit(gameover_screen, (50, 50))
        create_button("Play Again", 94, 150, 412, 30, button_color, hover_color, lambda: game_loop(2.5, 0.02))
        create_button("Main Menu", 94, 200, 412, 30, button_color, hover_color, load_intro)
        create_button("Quit", 94, 250, 412, 30, button_color, hover_color, quit_game)

        pygame.display.update()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()


def game_loop(snake_speed=2.5, speed_change=0.02):
    snake_x = 50
    snake_y = 50
    velocity_x = 0
    velocity_y = 0
    snake_list = []
    snake_len = 1
    score = 0

    apple_x = random.randint(0, WIDTH - apple_size)
    apple_y = random.randint(0, HEIGHT - apple_size)

    exit_game = False

    while not exit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    velocity_y = -snake_speed
                    velocity_x = 0
                elif event.key == pygame.K_DOWN:
                    velocity_y = snake_speed
                    velocity_x = 0
                elif event.key == pygame.K_LEFT:
                    velocity_x = -snake_speed
                    velocity_y = 0
                elif event.key == pygame.K_RIGHT:
                    velocity_x = snake_speed
                    velocity_y = 0
                elif event.key == pygame.K_ESCAPE:
                    exit_game = True

        snake_x += velocity_x
        snake_y += velocity_y

        head = [snake_x, snake_y]
        snake_list.append(head)
        if len(snake_list) > snake_len:
            del snake_list[0]

        if head in snake_list[:-1]:
            game_over(score)
            break

        if snake_x < 0 or snake_x > WIDTH - snake_size or snake_y < 0 or snake_y > HEIGHT - snake_size:
            game_over(score)
            break

        if abs(snake_x - apple_x) < 15 and abs(snake_y - apple_y) < 15:
            score += 5
            snake_len += 5
            snake_speed += speed_change
            apple_x = random.randint(0, WIDTH - apple_size)
            apple_y = random.randint(0, HEIGHT - apple_size)

        game_window.blit(background, (0, 0))
        game_window.blit(apple_img, (apple_x, apple_y))

        for i, (x, y) in enumerate(snake_list):
            if i == len(snake_list) - 1:
                game_window.blit(snake_head, (x, y))
            else:
                game_window.blit(snake_body, (x, y))

        text = score_font.render("Score: " + str(int(score)), True, black)
        game_window.blit(text, [5, 5])

        pygame.display.update()
        clock.tick(FPS)


load_intro()
quit_game()
