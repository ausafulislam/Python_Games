import pygame
import random
import os
import time


# Initialize pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
screen_width = 800
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Colors
BLACK = (0, 0, 0)
GREEN = (57, 255, 20)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)

# Font setup
try:
    font_large = pygame.font.Font(
        "./assets/fonts/analog_whispers/analog_whispers.ttf", 50
    )
    font_medium = pygame.font.Font(
        "./assets/fonts/analog_whispers/analog_whispers.ttf", 30
    )
    font_small = pygame.font.Font(
        "./assets/fonts/analog_whispers/analog_whispers.ttf", 20
    )
    font_instructions = pygame.font.Font(
        "./assets/fonts/analog_whispers/analog_whispers.ttf", 18
    )
except:
    font_large = pygame.font.SysFont("courier", 50, bold=True)
    font_medium = pygame.font.SysFont("courier", 30, bold=True)
    font_small = pygame.font.SysFont("courier", 20, bold=True)
    font_instructions = pygame.font.SysFont("courier", 18, bold=True)

# Game title
pygame.display.set_caption("SNAKE ARCADE")
clock = pygame.time.Clock()

# Snake and food size
SNAKE_SIZE = 20
FOOD_SIZE = 20

# Game settings
settings = {
    "bg_music_on": True,
    "sound_effects_on": True,
    "movement_sound_frequency": 3,
    "game_speed": 9,
}

# Sound setup
try:
    bg_music = pygame.mixer.Sound("./assets/sounds/bg_music.mp3")
    click_sound = pygame.mixer.Sound("./assets/sounds/click_music.wav")
    move_sound = pygame.mixer.Sound("./assets/sounds/sanke_runing_music.wav")
    eat_sound = pygame.mixer.Sound("./assets/sounds/sanke_food_eating_music.wav")
    game_over_sound = pygame.mixer.Sound("./assets/sounds/game_over_music.wav")

    bg_music.set_volume(0.5)
    click_sound.set_volume(0.7)
    move_sound.set_volume(0.5)
    eat_sound.set_volume(0.7)
    game_over_sound.set_volume(0.7)

except:
    print("Warning: Sound files not found. Game will run without sound.")


def loading_screen():
    """Show loading screen while initializing game"""
    start_time = time.time()
    loading = True
    bg_music_played = False  # Flag to track if we've played the music

    # Create progress bar variables
    progress = 0
    progress_width = 600
    progress_height = 20
    progress_x = (screen_width - progress_width) // 2
    progress_y = 400

    while loading:
        current_time = time.time()
        elapsed = current_time - start_time

        # Update progress (3 second loading screen)
        progress = min(elapsed / 3, 1) * progress_width
        percentage = int(progress / progress_width * 100)

        # Play bg music at 60% if not already played
        if percentage >= 40 and not bg_music_played and settings["bg_music_on"]:
            try:
                bg_music.play(-1)  # Loop indefinitely
                bg_music_played = True
            except:
                pass

        # Fill background
        gameWindow.fill(BLACK)

        # Draw loading text
        draw_text("LOADING...", font_large, GREEN, screen_width // 2, 200, True)

        # Draw progress bar outline
        pygame.draw.rect(
            gameWindow,
            GREEN,
            (progress_x - 2, progress_y - 2, progress_width + 4, progress_height + 4),
            2,
        )
        # Draw progress bar
        pygame.draw.rect(
            gameWindow, GREEN, (progress_x, progress_y, progress, progress_height)
        )

        # Draw loading percentage
        draw_text(
            f"{percentage}%",
            font_medium,
            GREEN,
            screen_width // 2,
            progress_y + 30,
            True,
        )

        # Draw developer info
        draw_text(
            "BUILD BY AUSAF UL ISLAM", font_small, GREEN, screen_width // 2, 500, True
        )

        pygame.display.update()

        # Check if loading is complete
        if elapsed >= 3:
            loading = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    # Transition to welcome screen
    welcome()


def draw_background():
    gameWindow.fill(BLACK)
    for x in range(0, screen_width, SNAKE_SIZE):
        pygame.draw.line(gameWindow, (20, 20, 20), (x, 0), (x, screen_height))
    for y in range(0, screen_height, SNAKE_SIZE):
        pygame.draw.line(gameWindow, (20, 20, 20), (0, y), (screen_width, y))
    pygame.draw.rect(gameWindow, GREEN, (0, 0, screen_width, screen_height), 2)


def draw_text(text, font, color, x, y, centered=False):
    text_surface = font.render(text, True, color)
    if centered:
        text_rect = text_surface.get_rect(center=(screen_width // 2, y))
        gameWindow.blit(text_surface, text_rect)
    else:
        gameWindow.blit(text_surface, (x, y))


def play_sound(sound):
    try:
        if settings["sound_effects_on"]:
            sound.play()
    except:
        pass


def toggle_bg_music():
    try:
        settings["bg_music_on"] = not settings["bg_music_on"]
        if settings["bg_music_on"]:
            bg_music.play(-1)
        else:
            bg_music.stop()
    except:
        pass


def settings_menu():
    menu_active = True
    selected_option = 0
    options = [
        f"Background Music: {'ON' if settings['bg_music_on'] else 'OFF'}",
        f"Sound Effects: {'ON' if settings['sound_effects_on'] else 'OFF'}",
        f"Move Sound Frequency: {settings['movement_sound_frequency']}",
        f"Game Speed: {settings['game_speed']}",
        "Back to Main Menu",
    ]

    while menu_active:
        draw_background()
        draw_text("SETTINGS", font_large, GREEN, screen_width // 2, 100, True)

        for i, option in enumerate(options):
            color = WHITE if i == selected_option else GRAY
            draw_text(option, font_medium, color, screen_width // 2, 200 + i * 50, True)

        draw_text(
            "Use ARROW KEYS to navigate, ENTER to toggle",
            font_small,
            GREEN,
            screen_width // 2,
            500,
            True,
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_active = False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                    play_sound(click_sound)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                    play_sound(click_sound)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        toggle_bg_music()
                        options[0] = (
                            f"Background Music: {'ON' if settings['bg_music_on'] else 'OFF'}"
                        )
                    elif selected_option == 1:
                        settings["sound_effects_on"] = not settings["sound_effects_on"]
                        options[1] = (
                            f"Sound Effects: {'ON' if settings['sound_effects_on'] else 'OFF'}"
                        )
                    elif selected_option == 4:
                        menu_active = False
                    play_sound(click_sound)
                elif event.key == pygame.K_LEFT:
                    if (
                        selected_option == 2
                        and settings["movement_sound_frequency"] > 1
                    ):
                        settings["movement_sound_frequency"] -= 1
                        options[2] = (
                            f"Move Sound Frequency: {settings['movement_sound_frequency']}"
                        )
                    elif selected_option == 3 and settings["game_speed"] > 5:
                        settings["game_speed"] -= 1
                        options[3] = f"Game Speed: {settings['game_speed']}"
                elif event.key == pygame.K_RIGHT:
                    if (
                        selected_option == 2
                        and settings["movement_sound_frequency"] < 5
                    ):
                        settings["movement_sound_frequency"] += 1
                        options[2] = (
                            f"Move Sound Frequency: {settings['movement_sound_frequency']}"
                        )
                    elif selected_option == 3 and settings["game_speed"] < 30:
                        settings["game_speed"] += 1
                        options[3] = f"Game Speed: {settings['game_speed']}"

        pygame.display.update()
        clock.tick(30)


def instructions_screen():
    """Display game instructions"""
    exit_instructions = False
    while not exit_instructions:
        draw_background()

        # Title
        draw_text("HOW TO PLAY", font_large, GREEN, screen_width // 2, 50, True)

        # Instructions text
        instructions = [
            "Control the snake using arrow keys:",
            "UP, DOWN, LEFT, RIGHT",
            "",
            "Game Rules:",
            "- Eat the red food to grow longer",
            "- Avoid hitting walls or yourself",
            "- Each food gives you 10 points",
            "",
            "Game Over Conditions:",
            "- Colliding with walls",
            "- Colliding with your own body",
            "",
            "Press ESC to return to main menu",
            "Press Q to quit during game",
        ]

        for i, line in enumerate(instructions):
            draw_text(
                line, font_instructions, WHITE, screen_width // 2, 120 + i * 25, True
            )

        # Back button
        draw_text(
            "BACK TO MENU (ESC)", font_medium, GREEN, screen_width // 2, 500, True
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_instructions = True
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    play_sound(click_sound)
                    exit_instructions = True

        pygame.display.update()
        clock.tick(30)


def welcome():
    """Welcome screen with arrow key navigation"""
    # Load high score
    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")
    with open("highscore.txt", "r") as f:
        highscore = int(f.read())

    menu_items = ["PRESS SPACE TO START", "INSTRUCTIONS", "SETTINGS", "QUIT"]
    selected_item = 0
    exit_game = False

    while not exit_game:
        draw_background()

        # Title - Shows actual high score
        draw_text(f"HIGH SCORE {highscore:06}", font_medium, GREEN, 50, 50)

        # Game title
        draw_text("SNAKE ARCADE", font_large, GREEN, screen_width // 2, 150, True)

        # Menu options with selection highlighting
        for i, item in enumerate(menu_items):
            color = WHITE if i == selected_item else GREEN
            if item == "QUIT":
                color = (
                    RED if i == selected_item else (200, 0, 0)
                )  # Darker red when not selected
            draw_text(item, font_medium, color, screen_width // 2, 250 + i * 50, True)

        # Footer
        draw_text(
            "BUILD BY AUSAF UL ISLAM", font_small, GREEN, screen_width // 2, 500, True
        )
        draw_text(
            "CREDIT: 01", font_small, GREEN, screen_width - 150, screen_height - 30
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_item = (selected_item + 1) % len(menu_items)
                    play_sound(click_sound)
                elif event.key == pygame.K_UP:
                    selected_item = (selected_item - 1) % len(menu_items)
                    play_sound(click_sound)
                elif event.key == pygame.K_RETURN:
                    play_sound(click_sound)
                    if selected_item == 0:  # START
                        gameloop()
                    elif selected_item == 1:  # INSTRUCTIONS
                        instructions_screen()
                    elif selected_item == 2:  # SETTINGS
                        settings_menu()
                    elif selected_item == 3:  # QUIT
                        exit_game = True
                elif event.key == pygame.K_SPACE:  # Space still works for start
                    if selected_item == 0:
                        play_sound(click_sound)
                        gameloop()

        pygame.display.update()
        clock.tick(30)


def game_over_screen(score, highscore):
    exit_game = False
    play_sound(game_over_sound)

    while not exit_game:
        draw_background()

        draw_text(f"HIGH SCORE {highscore:06}", font_medium, GREEN, 50, 50)
        draw_text("GAME OVER", font_large, RED, screen_width // 2, 150, True)
        draw_text(
            f"SCORE: {score:06}", font_medium, GREEN, screen_width // 2, 220, True
        )
        draw_text(
            "PRESS ENTER TO CONTINUE", font_medium, GREEN, screen_width // 2, 320, True
        )
        draw_text("PRESS Q TO QUIT", font_medium, RED, screen_width // 2, 370, True)
        draw_text(
            "BUILD BY AUSAF UL ISLAM", font_small, GREEN, screen_width // 2, 450, True
        )
        draw_text(
            "CREDIT: 01", font_small, GREEN, screen_width - 150, screen_height - 30
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    play_sound(click_sound)
                    welcome()
                elif event.key == pygame.K_q:
                    exit_game = True

        pygame.display.update()
        clock.tick(30)


def gameloop():
    snake_x = screen_width // 2
    snake_y = screen_height // 2
    snake_list = []
    snake_length = 1
    velocity_x = 0
    velocity_y = 0
    score = 0
    move_counter = 0

    food_x = random.randint(1, (screen_width - FOOD_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
    food_y = random.randint(1, (screen_height - FOOD_SIZE) // SNAKE_SIZE) * SNAKE_SIZE

    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")
    with open("highscore.txt", "r") as f:
        highscore = int(f.read())

    exit_game = False
    game_over = False

    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(max(score, highscore)))
            game_over_screen(score, max(score, highscore))
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and velocity_x <= 0:
                    velocity_x = settings["game_speed"]
                    velocity_y = 0
                    move_counter = 0
                    play_sound(move_sound)
                if event.key == pygame.K_LEFT and velocity_x >= 0:
                    velocity_x = -settings["game_speed"]
                    velocity_y = 0
                    move_counter = 0
                    play_sound(move_sound)
                if event.key == pygame.K_UP and velocity_y >= 0:
                    velocity_y = -settings["game_speed"]
                    velocity_x = 0
                    move_counter = 0
                    play_sound(move_sound)
                if event.key == pygame.K_DOWN and velocity_y <= 0:
                    velocity_y = settings["game_speed"]
                    velocity_x = 0
                    move_counter = 0
                    play_sound(move_sound)
                if event.key == pygame.K_ESCAPE:
                    welcome()
                    return
                if event.key == pygame.K_q:
                    exit_game = True

        snake_x += velocity_x
        snake_y += velocity_y

        if velocity_x != 0 or velocity_y != 0:
            move_counter += 1
            if move_counter >= settings["movement_sound_frequency"]:
                play_sound(move_sound)
                move_counter = 0

        if (
            snake_x < 0
            or snake_x >= screen_width
            or snake_y < 0
            or snake_y >= screen_height
        ):
            game_over = True

        if abs(snake_x - food_x) < SNAKE_SIZE and abs(snake_y - food_y) < SNAKE_SIZE:
            score += 10
            snake_length += 1
            food_x = (
                random.randint(1, (screen_width - FOOD_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
            )
            food_y = (
                random.randint(1, (screen_height - FOOD_SIZE) // SNAKE_SIZE)
                * SNAKE_SIZE
            )
            play_sound(eat_sound)

        snake_head = [snake_x, snake_y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        if snake_head in snake_list[:-1]:
            game_over = True

        draw_background()
        pygame.draw.rect(gameWindow, RED, [food_x, food_y, FOOD_SIZE, FOOD_SIZE])

        for i, segment in enumerate(snake_list):
            if i == len(snake_list) - 1:
                pygame.draw.rect(
                    gameWindow, GREEN, [segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE]
                )
            else:
                pygame.draw.rect(
                    gameWindow,
                    (0, 200, 0),
                    [segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE],
                )

        draw_text(f"SCORE {score:06}", font_medium, GREEN, 20, 20)
        draw_text(
            f"HIGH SCORE {highscore:06}", font_medium, GREEN, screen_width - 300, 20
        )

        pygame.display.update()
        clock.tick(30)


# Start the game
loading_screen()
welcome()
pygame.quit()
quit()
