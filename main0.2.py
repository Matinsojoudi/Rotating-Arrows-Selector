import pygame
import random
import time

pygame.init()

info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("گردونه شانس")

white = (255, 255, 255)

try:
    background_image = pygame.image.load("background.png")
    bg_width, bg_height = background_image.get_size()

    min_screen_dim = min(screen_width, screen_height)
    min_bg_dim = min(bg_width, bg_height)

    scale_factor = min_screen_dim / min_bg_dim

    new_bg_width = int(bg_width * scale_factor)
    new_bg_height = int(bg_height * scale_factor)
    
    background_image = pygame.transform.scale(background_image, (new_bg_width, new_bg_height))

    bg_x = (screen_width - new_bg_width) // 2
    bg_y = (screen_height - new_bg_height) // 2
except pygame.error as e:
    print(f"Error loading background image: {e}")
    pygame.quit()
    exit()

try:
    start_button_image = pygame.image.load("start_button.png")
except pygame.error as e:
    print(f"Error loading start button image: {e}")
    pygame.quit()
    exit()

try:
    arrow_image = pygame.image.load("arrow.png")
except pygame.error as e:
    print(f"Error loading image: {e}")
    pygame.quit()
    exit()

center_x, center_y = screen_width // 2, screen_height // 2

def draw_arrow(surface, image, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    rect = rotated_image.get_rect(center=(center_x, center_y))
    surface.blit(rotated_image, rect.topleft)

running = True
rotation_angle = 0
speed = 10
deceleration = 0.05
arrow_selected_angle = None
game_started = False
fullscreen = False

# تعداد بخش‌ها و زاویه هر بخش
num_sections = 30
section_angle = 360 / num_sections

# خطای مجاز
angle_correction_threshold = 2  # درجه مجاز برای تنظیم خطا

def choose_random_angle():
    section = random.randint(0, num_sections - 1)
    return section * section_angle

def normalize_angle(angle):
    return angle % 360

def correct_angle(angle):
    mod_angle = angle % section_angle
    if mod_angle < angle_correction_threshold:
        return angle - mod_angle
    elif mod_angle > section_angle - angle_correction_threshold:
        return angle + (section_angle - mod_angle)
    return angle

while running:
    screen.blit(background_image, (bg_x, bg_y))

    if not game_started:
        start_button_rect = start_button_image.get_rect(center=(center_x, center_y))
        screen.blit(start_button_image, start_button_rect)

        if pygame.mouse.get_pressed()[0] and start_button_rect.collidepoint(pygame.mouse.get_pos()):
            game_started = True
            arrow_selected_angle = None
            rotation_angle = 0
            speed = 10
            start_time = time.time()
    
    else:
        current_time = time.time()
        if arrow_selected_angle is None:
            if current_time - start_time < 5:
                rotation_angle += speed
                speed = max(speed - deceleration, 0.1)
            else:
                arrow_selected_angle = choose_random_angle()

        if arrow_selected_angle is not None:
            target_angle = normalize_angle(arrow_selected_angle)
            current_angle = normalize_angle(rotation_angle)

            angle_difference = (target_angle - current_angle + 360) % 360

            if angle_difference < 180:
                rotation_angle += speed
            else:
                rotation_angle -= speed

            if abs(angle_difference) < speed:
                rotation_angle = correct_angle(arrow_selected_angle)
                game_started = False
                time.sleep(2)

        draw_arrow(screen, arrow_image, rotation_angle)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                running = False

            if event.key == pygame.K_RETURN:  # دکمه اینتر برای شروع بازی
                game_started = True
                arrow_selected_angle = None
                rotation_angle = 0
                speed = 10
                start_time = time.time()

            if event.key == pygame.K_SPACE:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((screen_width, screen_height))
                pygame.display.set_caption("گردونه شانس")

pygame.quit()
