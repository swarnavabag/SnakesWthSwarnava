import random
import pygame

pygame.init()
pygame.font.init()

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (200, 200, 200)
red = (255, 0, 0)
button_color = (59, 83, 35)
hover_color = (80, 120, 70)
text_color = (250, 250, 210)
shadow_color = (220, 235, 180)

# Constants
WIDTH, HEIGHT = 600, 400
FPS = 60
snake_size = 40
apple_size = 30
snake_speed = 2.5
speed_change = 0.02
current_difficulty = "medium"

# Fonts
score_font = pygame.font.SysFont("comicsansms", 25)
buttons_font = pygame.font.SysFont("Roboto", 25)
gameover_button_font = pygame.font.Font(r"font/PressStart2P-Regular.ttf", 14)

# Load images
intro_screen = pygame.image.load(r"images/intro_screen.jpg")
intro_screen = pygame.transform.scale(intro_screen, (WIDTH, HEIGHT))

settings_screen = pygame.image.load(r"images/settings_screen.jpg")
settings_screen = pygame.transform.scale(settings_screen, (WIDTH, HEIGHT))

background = pygame.image.load(r"images/background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

snake_img = pygame.image.load(r"images/snake.png")
snake_img = pygame.transform.scale(snake_img, (snake_size, snake_size))

apple_img = pygame.image.load(r"images/apple.png")
apple_img = pygame.transform.scale(apple_img, (apple_size, apple_size))

gameover_screen = pygame.image.load(r"images/gameover_screen.png")
gameover_screen = pygame.transform.scale(gameover_screen, (500, 300))

hiscore_screen = pygame.image.load(r"images/hiscore_screen.webp")
hiscore_screen = pygame.transform.scale(hiscore_screen, (500, 300))

# Game window
game_window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SnakesWthSwarnava")
clock = pygame.time.Clock()


# Load sound
gamestart_sound = pygame.mixer.Sound(r"soundeffects/gamestart.mp3")
gameover_sound = pygame.mixer.Sound(r"soundeffects/gameover.mp3")
intro_sound = pygame.mixer.Sound(r"soundeffects/backgroundsound.mp3")
hiscore_sound = pygame.mixer.Sound(r"soundeffects/hiscore.mp3")
apple_eating_sound = pygame.mixer.Sound(r"soundeffects/apple_eating_sound.wav")
joy_sound = pygame.mixer.Sound(r"soundeffects/joy.mp3")


def create_button(text, x, y, width, height, inactive_color, active_color, action=None):
    shadow_offset = 3
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    pygame.draw.rect(game_window, shadow_color, (x + shadow_offset, y + shadow_offset, width, height), border_radius=8)

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(game_window, active_color, (x, y, width, height), border_radius=8)
        if click[0] == 1 and action:
            pygame.time.delay(150)  # to prevent multiple calls
            action()
    else:
        pygame.draw.rect(game_window, inactive_color, (x, y, width, height), border_radius=8)

    button_text = buttons_font.render(text, True, text_color)
    text_rect = button_text.get_rect(center=(x + width // 2, y + height // 2))
    game_window.blit(button_text, text_rect)


def gameover_button(text, x, y, width, height, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Check if the mouse is hovering over the button
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        if click[0] == 1 and action:
            pygame.time.delay(150)  # Prevent multiple calls on single click
            action()

    # Draw the text with red font color (no background color)
    button_text = gameover_button_font.render(
        text, True, red)  # Red font color
    text_rect = button_text.get_rect(center=(x + width // 2, y + height // 2))
    game_window.blit(button_text, text_rect)


def draw_slider(x, y, width, min_val, max_val, current_val, label=""):
    # Draw slider track
    pygame.draw.rect(game_window, gray, (x, y, width, 8), border_radius=5)

    # Calculate position of the knob
    knob_x = x + int((current_val - min_val) / (max_val - min_val) * width)
    pygame.draw.circle(game_window, red, (knob_x, y + 4), 10)

    # Draw label and value
    label_text = buttons_font.render(
        f"{label}: {int(current_val)}", True, text_color)
    game_window.blit(label_text, (x, y - 30))

    return knob_x


def quit_game():
    pygame.quit()
    quit()


def create_label(text, x, y):
    label_text = buttons_font.render(text, True, text_color)
    text_rect = label_text.get_rect(center=(x, y))
    game_window.blit(label_text, text_rect)


def easy():
    global snake_speed, speed_change, current_difficulty
    snake_speed = 2
    speed_change = 0.01
    current_difficulty = "easy"  # Set current difficulty to easy


def medium():
    global snake_speed, speed_change, current_difficulty
    snake_speed = 2.5
    speed_change = 0.03
    current_difficulty = "medium"  # Set current difficulty to medium


def hard():
    global snake_speed, speed_change, current_difficulty
    snake_speed = 3
    speed_change = 0.05
    current_difficulty = "hard"  # Set current difficulty to hard


def load_intro():
    global intro_sound

    if not intro_sound.get_num_channels():  # Play only if not already playing
        intro_sound.play(-1)  # Loop indefinitely

    intro_active = True
    while intro_active:
        game_window.blit(intro_screen, (0, 0))

        create_button("Play", 94, 250, 412, 30, button_color, hover_color, lambda: game_loop(snake_speed, speed_change))
        create_button("Settings", 94, 300, 412, 30, button_color, hover_color, load_settings)
        create_button("Quit", 94, 350, 412, 30, button_color, hover_color, quit_game)

        pygame.display.update()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()


def load_settings():
    settings_active = True
    global intro_sound, apple_eating_sound, gamestart_sound, gameover_sound

    master_volume = 50  # Default volume
    previous_volume = -1  # To force first update

    while settings_active:
        game_window.blit(settings_screen, (0, 0))

        # Labels
        create_label(
            f"Current Difficulty: {current_difficulty.capitalize()}", WIDTH // 2, 50)
        create_label("Select Difficulty", WIDTH // 2, 100)

        # Difficulty Buttons
        create_button("Easy", 94, 150, 412, 30, button_color, hover_color, easy)
        create_button("Medium", 94, 200, 412, 30, button_color, hover_color, medium)
        create_button("Hard", 94, 250, 412, 30, button_color, hover_color, hard)

        # Volume Slider (at y = 350)
        knob_x = draw_slider(150, 350, 300, 0, 100, master_volume, label="Volume")

        # Update volume only if it changed
        if master_volume != previous_volume:
            volume_value = master_volume / 100.0
            intro_sound.set_volume(volume_value)
            apple_eating_sound.set_volume(volume_value)
            gamestart_sound.set_volume(volume_value)
            gameover_sound.set_volume(volume_value)
            previous_volume = master_volume

        # Navigation Buttons
        create_button("Back", 10, 355, 60, 30, button_color, hover_color, load_intro)
        create_button("Quit", 525, 355, 60, 30, button_color, hover_color, quit_game)

        pygame.display.update()
        clock.tick(FPS)

        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                # Difficulty
                if 94 <= mx <= 506:
                    if 150 <= my <= 180:
                        easy()
                    elif 200 <= my <= 230:
                        medium()
                    elif 250 <= my <= 280:
                        hard()

                # Back and Quit
                if 10 <= mx <= 70 and 355 <= my <= 385:
                    load_intro()
                elif 525 <= mx <= 585 and 355 <= my <= 385:
                    quit_game()

                # Volume Slider
                if 150 <= mx <= 450 and 350 <= my <= 368:
                    master_volume = max(0, min(100, ((mx - 150) / 300) * 100))

            if event.type == pygame.MOUSEMOTION:
                mx, my = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0]:
                    if 150 <= mx <= 450 and 350 <= my <= 368:
                        master_volume = max(
                            0, min(100, ((mx - 150) / 300) * 100))


            pygame.display.update()


def game_over():
    gameover_sound.set_volume(0.3)
    gameover_sound.play()
    over = True
    next_action = None

    while over:
        game_window.blit(gameover_screen, (50, 50))

        def play_again():
            nonlocal over, next_action
            over = False
            next_action = "play"

        def open_settings():
            nonlocal over, next_action
            over = False
            next_action = "settings"

        def quit_game_action():
            nonlocal over, next_action
            over = False
            next_action = "quit"

        gameover_button("Play Again", 70, 315, 130, 30, play_again)
        gameover_button("Settings", 270, 315, 140, 30, open_settings)
        gameover_button("Quit", 460, 315, 100, 30, quit_game_action)

        pygame.display.update()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover_sound.stop()
                quit_game()

    gameover_sound.stop()

    # Now handle the selected action
    if next_action == "play":
        game_loop(snake_speed, speed_change)
    elif next_action == "settings":
        load_settings()
    elif next_action == "quit":
        quit_game()


def hiscore_load():
    gameover_sound.set_volume(0.5)
    hiscore_sound.play()
    over = True
    next_action = None

    while over:
        game_window.blit(hiscore_screen, (50, 50))

        def play_again():
            nonlocal over, next_action
            over = False
            next_action = "play"

        def open_settings():
            nonlocal over, next_action
            over = False
            next_action = "settings"

        def quit_game_action():
            nonlocal over, next_action
            over = False
            next_action = "quit"

        gameover_button("Play Again", 70, 315, 130, 30, play_again)
        gameover_button("Settings", 270, 315, 140, 30, open_settings)
        gameover_button("Quit", 460, 315, 100, 30, quit_game_action)

        pygame.display.update()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                hiscore_sound.stop()
                quit_game()

    hiscore_sound.stop()

    # Now handle the selected action
    if next_action == "play":
        game_loop(snake_speed, speed_change)
    elif next_action == "settings":
        load_settings()
    elif next_action == "quit":
        quit_game()


def check_self_collision(snake_list):
    head = snake_list[-1]
    body = snake_list[:-1]
    if head in body:
        return True
    return False


def game_loop(snake_speed, speed_change):
    gamestart_sound.play()

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
                elif event.key == pygame.K_d:
                    apple_eating_sound.play()
                    score += 5
                    snake_len += 5


        snake_x += velocity_x
        snake_y += velocity_y

        head = [snake_x, snake_y]
        snake_list.append(head)
        if len(snake_list) > snake_len:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == head:
                game_over()
                return

        border_buffer = 10
        if (
            snake_x < -border_buffer or
            snake_x > WIDTH - snake_size + border_buffer or
            snake_y < -border_buffer or
            snake_y > HEIGHT - snake_size + border_buffer
        ):
            game_over()
            return
        
        if abs(snake_x - apple_x) < 17 and abs(snake_y - apple_y) < 17:
            apple_eating_sound.play()
            score += 5
            snake_len += 5
            snake_speed += speed_change  # Increase speed after eating an apple
            apple_x = random.randint(0, WIDTH - apple_size)
            apple_y = random.randint(0, HEIGHT - apple_size)


        game_window.blit(background, (0, 0))
        game_window.blit(apple_img, (apple_x, apple_y))

        for x, y in snake_list:
            game_window.blit(snake_img, (x, y))

        with open("hiscore.txt", "r") as f:
            hiscore = f.read()

        if hiscore == "":
            hiscore = 0
        if int(score) > int(hiscore):
            joy_sound.play()
            hiscore = score
            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))

        text2 = score_font.render("High Score: " + str(int(hiscore)), True, black)
        game_window.blit(text2, [200, 5])

        text1 = score_font.render("Score: " + str(int(score)), True, black)
        game_window.blit(text1, [5, 5])

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    load_intro()
