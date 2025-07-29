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
SNAKE_SIZE = 30
FOOD_SIZE = 30

# Load images
try:
    snake_head_img = pygame.image.load("./assets/images/snake_head.png").convert_alpha()
    snake_head_img = pygame.transform.scale(snake_head_img, (SNAKE_SIZE, SNAKE_SIZE))

    snake_body_img = pygame.image.load("./assets/images/snake_body.png").convert_alpha()
    snake_body_img = pygame.transform.scale(snake_body_img, (SNAKE_SIZE, SNAKE_SIZE))

    food_img = pygame.image.load("./assets/images/snake_food.png").convert_alpha()
    food_img = pygame.transform.scale(food_img, (FOOD_SIZE, FOOD_SIZE))
except:
    print("Warning: Image files not found. Using rectangles instead.")
    snake_head_img = None
    snake_body_img = None
    food_img = None

# Game settings
settings = {
    "bg_music_on": True,
    "sound_effects_on": True,
    "movement_sound_frequency": 3,
    "game_speed": 8,
}

# Sound setup
try:
    bg_music = pygame.mixer.Sound("./assets/sounds/bg_music.mp3")
    click_sound = pygame.mixer.Sound("./assets/sounds/click_music.wav")
    move_sound = pygame.mixer.Sound("./assets/sounds/snake_runing_music.mp3")
    eat_sound = pygame.mixer.Sound("./assets/sounds/snake_food_eating_music.wav")
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
    bg_music_played = False

    # Progress bar variables
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

        # Play bg music at 25% if not already played
        if percentage >= 25 and not bg_music_played and settings["bg_music_on"]:
            try:
                bg_music.play(-1)
                bg_music_played = True
            except:
                pass

        # Fill background
        gameWindow.fill(BLACK)

        # Draw loading text
        draw_text("LOADING...", font_large, GREEN, screen_width // 2, 200, True)

        # Draw progress bar
        pygame.draw.rect(
            gameWindow,
            GREEN,
            (progress_x - 2, progress_y - 2, progress_width + 4, progress_height + 4),
            2,
        )
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


def draw_background():
    """Draw the retro arcade background"""
    gameWindow.fill(BLACK)
    for x in range(0, screen_width, SNAKE_SIZE):
        pygame.draw.line(gameWindow, (20, 20, 20), (x, 0), (x, screen_height))
    for y in range(0, screen_height, SNAKE_SIZE):
        pygame.draw.line(gameWindow, (20, 20, 20), (0, y), (screen_width, y))
    pygame.draw.rect(gameWindow, GREEN, (0, 0, screen_width, screen_height), 2)


def draw_text(text, font, color, x, y, centered=False):
    """Helper function to draw text"""
    text_surface = font.render(text, True, color)
    if centered:
        text_rect = text_surface.get_rect(center=(screen_width // 2, y))
        gameWindow.blit(text_surface, text_rect)
    else:
        gameWindow.blit(text_surface, (x, y))


def play_sound(sound):
    """Play a sound effect if sound effects are enabled"""
    try:
        if settings["sound_effects_on"]:
            sound.play()
    except:
        pass


def toggle_bg_music():
    """Toggle background music on/off"""
    try:
        settings["bg_music_on"] = not settings["bg_music_on"]
        if settings["bg_music_on"]:
            bg_music.play(-1)
        else:
            bg_music.stop()
    except:
        pass


def settings_menu():
    """Display settings menu"""
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
                return True

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

    return False


def instructions_screen():
    """Display game instructions"""
    exit_instructions = False
    while not exit_instructions:
        draw_background()

        draw_text("HOW TO PLAY", font_large, GREEN, screen_width // 2, 50, True)

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

        draw_text(
            "BACK TO MENU (ESC)", font_medium, GREEN, screen_width // 2, 500, True
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    play_sound(click_sound)
                    exit_instructions = True
                elif event.key == pygame.K_q:
                    return True

        pygame.display.update()
        clock.tick(30)

    return False


def welcome():
    """Welcome screen with arrow key navigation"""
    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")
    with open("highscore.txt", "r") as f:
        highscore = int(f.read())

    menu_items = ["START PLAYING", "INSTRUCTIONS", "SETTINGS", "QUIT"]
    selected_item = 0
    exit_screen = False

    while not exit_screen:
        draw_background()

        draw_text(f"HIGH SCORE {highscore:06}", font_medium, GREEN, 50, 50)
        draw_text("SNAKE ARCADE", font_large, GREEN, screen_width // 2, 150, True)

        for i, item in enumerate(menu_items):
            color = WHITE if i == selected_item else GREEN
            if item == "QUIT":
                color = RED if i == selected_item else (200, 0, 0)
            draw_text(item, font_medium, color, screen_width // 2, 250 + i * 50, True)

        draw_text(
            "BUILD BY AUSAF UL ISLAM", font_small, GREEN, screen_width // 2, 500, True
        )
        draw_text(
            "CREDIT: 01", font_small, GREEN, screen_width - 150, screen_height - 30
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_item = (selected_item + 1) % len(menu_items)
                    play_sound(click_sound)
                elif event.key == pygame.K_UP:
                    selected_item = (selected_item - 1) % len(menu_items)
                    play_sound(click_sound)
                elif event.key == pygame.K_RETURN:
                    play_sound(click_sound)
                    if selected_item == 0:
                        exit_screen = True
                    elif selected_item == 1:
                        should_quit = instructions_screen()
                        if should_quit:
                            return True
                    elif selected_item == 2:
                        should_quit = settings_menu()
                        if should_quit:
                            return True
                    elif selected_item == 3:
                        return True
                elif event.key == pygame.K_SPACE and selected_item == 0:
                    play_sound(click_sound)
                    exit_screen = True
                elif event.key == pygame.K_q:
                    return True

        pygame.display.update()
        clock.tick(30)

    return False


def game_over_screen(score, highscore):
    """Display game over screen"""
    exit_screen = False
    play_sound(game_over_sound)

    while not exit_screen:
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
                return True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    play_sound(click_sound)
                    exit_screen = True
                elif event.key == pygame.K_q:
                    return True

        pygame.display.update()
        clock.tick(30)

    return False


def get_food_position():
    """Get random food position that's not too close to boundaries"""
    margin = 3 * SNAKE_SIZE  # Keep food at least 3 snake sizes from edges
    x = (
        random.randint(margin // SNAKE_SIZE, (screen_width - margin) // SNAKE_SIZE)
        * SNAKE_SIZE
    )
    y = (
        random.randint(margin // SNAKE_SIZE, (screen_height - margin) // SNAKE_SIZE)
        * SNAKE_SIZE
    )
    return x, y


def draw_snake_part(x, y, is_head=False, direction=None):
    """Draw a snake part (head or body)"""
    if is_head and snake_head_img:
        # Rotate head based on direction
        if direction == "RIGHT":
            img = snake_head_img
        elif direction == "LEFT":
            img = pygame.transform.rotate(snake_head_img, 180)
        elif direction == "UP":
            img = pygame.transform.rotate(snake_head_img, 90)
        elif direction == "DOWN":
            img = pygame.transform.rotate(snake_head_img, 270)
        else:
            img = snake_head_img
        gameWindow.blit(img, (x, y))
    elif snake_body_img:
        gameWindow.blit(snake_body_img, (x, y))
    else:
        # Fallback to rectangles if images not available
        color = GREEN if is_head else (0, 200, 0)
        pygame.draw.rect(gameWindow, color, [x, y, SNAKE_SIZE, SNAKE_SIZE])


def gameloop():
    """Main game loop"""
    # Initialize snake with head and 2 body parts
    snake_x = screen_width // 2
    snake_y = screen_height // 2
    snake_list = [[snake_x, snake_y]]  # Head
    # Add two initial body parts
    snake_list.append([snake_x - SNAKE_SIZE, snake_y])
    snake_list.append([snake_x - 2 * SNAKE_SIZE, snake_y])
    snake_length = 3  # Head + 2 body parts

    velocity_x = settings["game_speed"]
    velocity_y = 0
    score = 0
    move_counter = 0
    current_direction = "RIGHT"

    # Get initial food position
    food_x, food_y = get_food_position()

    # Load high score
    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")
    with open("highscore.txt", "r") as f:
        highscore = int(f.read())

    game_over = False

    while True:
        if game_over:
            new_highscore = max(score, highscore)
            with open("highscore.txt", "w") as f:
                f.write(str(new_highscore))

            should_quit = game_over_screen(score, new_highscore)
            return should_quit

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and velocity_x <= 0:
                    velocity_x = settings["game_speed"]
                    velocity_y = 0
                    move_counter = 0
                    current_direction = "RIGHT"
                    play_sound(move_sound)
                elif event.key == pygame.K_LEFT and velocity_x >= 0:
                    velocity_x = -settings["game_speed"]
                    velocity_y = 0
                    move_counter = 0
                    current_direction = "LEFT"
                    play_sound(move_sound)
                elif event.key == pygame.K_UP and velocity_y >= 0:
                    velocity_y = -settings["game_speed"]
                    velocity_x = 0
                    move_counter = 0
                    current_direction = "UP"
                    play_sound(move_sound)
                elif event.key == pygame.K_DOWN and velocity_y <= 0:
                    velocity_y = settings["game_speed"]
                    velocity_x = 0
                    move_counter = 0
                    current_direction = "DOWN"
                    play_sound(move_sound)
                elif event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_q:
                    return True

        # Update snake position
        snake_x += velocity_x
        snake_y += velocity_y

        # Add new head position
        new_head = [snake_x, snake_y]
        snake_list.insert(0, new_head)

        # Remove tail if we haven't eaten food
        if len(snake_list) > snake_length:
            snake_list.pop()

        # Play movement sound at specified frequency
        if velocity_x != 0 or velocity_y != 0:
            move_counter += 1
            if move_counter >= settings["movement_sound_frequency"]:
                play_sound(move_sound)
                move_counter = 0

        # Check wall collision (game over if snake touches boundary)
        if (
            snake_x < 0
            or snake_x >= screen_width
            or snake_y < 0
            or snake_y >= screen_height
        ):
            game_over = True

        # Check food collision
        if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10:
            score += 10
            snake_length += 2  # Grow snake by 5 segments
            food_x, food_y = get_food_position()
            play_sound(eat_sound)

        # Check self collision
        if new_head in snake_list[1:]:
            game_over = True

        # Drawing
        draw_background()

        # Draw food
        if food_img:
            gameWindow.blit(food_img, (food_x, food_y))
        else:
            pygame.draw.rect(gameWindow, RED, [food_x, food_y, FOOD_SIZE, FOOD_SIZE])

        # Draw snake body first
        for segment in snake_list[1:]:
            draw_snake_part(segment[0] , segment[1] , False, None)

        # Draw head last, centered and clean
        draw_snake_part(snake_list[0][0], snake_list[0][1], True, current_direction)

        # Draw score
        draw_text(f"SCORE {score:06}", font_medium, GREEN, 20, 20)
        draw_text(
            f"HIGH SCORE {highscore:06}", font_medium, GREEN, screen_width - 300, 20
        )

        pygame.display.update()
        clock.tick(30)


def main():
    """Main game function that manages the game loop"""
    loading_screen()

    while True:
        should_quit = welcome()
        if should_quit:
            break

        should_quit = gameloop()
        if should_quit:
            break

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
