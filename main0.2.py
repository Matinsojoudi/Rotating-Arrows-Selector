import pygame
import random
import time

# راه‌اندازی Pygame
pygame.init()
pygame.mixer.init()

# تنظیم اندازه صفحه
screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

# بارگذاری تصاویر و صداها
background_white = pygame.image.load("background_white.png")
roulette_image = pygame.image.load("roulette_circle.png")
arrow_image = pygame.image.load("arrow.png")
start_button_image = pygame.image.load("start_button.png")

roulette_sound = pygame.mixer.Sound("roulette_sound.wav")

# تغییر اندازه گردونه
smallest_side = min(screen_width, screen_height)
roulette_image = pygame.transform.scale(roulette_image, (smallest_side, smallest_side))

# محاسبه مرکز صفحه
def calculate_center():
    return screen.get_width() // 2, screen.get_height() // 2

# تابع برای رسم فلش
def draw_arrow(surface, image):
    rotated_image = pygame.transform.rotate(image, -90)  # چرخش 90 درجه به سمت راست
    center_x, center_y = calculate_center()
    rect = rotated_image.get_rect(center=(center_x, center_y))
    surface.blit(rotated_image, rect.topleft)

# متغیرها
running = True
rotation_angle = 0
speed = 10
deceleration = 0.05
arrow_selected_angle = None
game_started = False
background = background_white
fullscreen = False

# تابع برای انتخاب زاویه تصادفی
def choose_random_angle():
    return random.randint(0, 360)

# تابع برای نرمال‌سازی زاویه
def normalize_angle(angle):
    return angle % 360

# حلقه اصلی برنامه
while running:
    screen.blit(background, (0, 0))

    # رسم گردونه
    rotated_roulette_image = pygame.transform.rotate(roulette_image, rotation_angle)
    center_x, center_y = calculate_center()
    roulette_rect = rotated_roulette_image.get_rect(center=(center_x, center_y))
    screen.blit(rotated_roulette_image, roulette_rect)

    if not game_started:
        start_button_rect = start_button_image.get_rect(center=(center_x, center_y))
        screen.blit(start_button_image, start_button_rect)

        # بررسی کلیک روی دکمه استارت یا زدن Enter
        if pygame.mouse.get_pressed()[0] and start_button_rect.collidepoint(pygame.mouse.get_pos()):
            game_started = True
            arrow_selected_angle = None
            rotation_angle = 0
            speed = 10
            start_time = time.time()
            pygame.mixer.Sound.play(roulette_sound)
        elif pygame.key.get_pressed()[pygame.K_RETURN]:
            game_started = True
            arrow_selected_angle = None
            rotation_angle = 0
            speed = 10
            start_time = time.time()
            pygame.mixer.Sound.play(roulette_sound)

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
                rotation_angle = arrow_selected_angle
                game_started = False
                pygame.mixer.Sound.stop(roulette_sound)
                time.sleep(2)

        draw_arrow(screen, arrow_image)  # رسم فلش

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                background = background_white
            if event.key == pygame.K_e:
                running = False
            if event.key == pygame.K_RETURN and not game_started:
                game_started = True
            if event.key == pygame.K_F11:  # برای بزرگ‌نمایی و برگرداندن به حالت پنجره
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

    # محاسبه مرکز جدید
    center_x, center_y = calculate_center()

pygame.quit()
