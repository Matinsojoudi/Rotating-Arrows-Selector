import pygame
import random
import time

# تنظیمات اولیه Pygame
pygame.init()

# تنظیم اندازه صفحه به متغیر
screen_width = 850  # عرض دلخواه
screen_height = 850  # ارتفاع دلخواه
screen = pygame.display.set_mode((screen_width, screen_height))

# عنوان پنجره
pygame.display.set_caption("گردونه شانس")

# رنگ‌ها
white = (255, 255, 255)

# بارگذاری تصویر پس‌زمینه
try:
    background_image = pygame.image.load("background.png")  # آدرس تصویر پس‌زمینه را اینجا قرار دهید
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  # تغییر اندازه به کل صفحه
except pygame.error as e:
    print(f"Error loading background image: {e}")
    pygame.quit()
    exit()

# بارگذاری تصویر دکمه شروع
try:
    start_button_image = pygame.image.load("start_button.png")  # آدرس تصویر دکمه شروع را اینجا قرار دهید
except pygame.error as e:
    print(f"Error loading start button image: {e}")
    pygame.quit()
    exit()

# بارگذاری تصویر فلش با کیفیت بالا
try:
    arrow_image = pygame.image.load("arrow.png")  # آدرس تصویر فلش را اینجا قرار دهید
except pygame.error as e:
    print(f"Error loading image: {e}")
    pygame.quit()
    exit()

# موقعیت مرکز
center_x, center_y = screen_width // 2, screen_height // 2

# رسم فلش
def draw_arrow(surface, image, angle):
    rotated_image = pygame.transform.rotate(image, angle)  # چرخش تصویر بر اساس زاویه
    rect = rotated_image.get_rect(center=(center_x, center_y))  # مرکز تصویر
    surface.blit(rotated_image, rect.topleft)  # رسم تصویر چرخیده

# متغیرها
running = True
rotation_angle = 0
speed = 10  # سرعت اولیه چرخش
deceleration = 0.05  # کاهش سرعت به مرور زمان
arrow_selected_angle = None
game_started = False

# تابع تصادفی انتخاب زاویه برای توقف فلش
def choose_random_angle():
    return random.randint(0, 360)

# تابع برای نگه‌داشتن زاویه در محدوده 0 تا 360
def normalize_angle(angle):
    return angle % 360

# حلقه اصلی برنامه
while running:
    # رسم پس‌زمینه
    screen.blit(background_image, (0, 0))

    # اگر بازی شروع نشده باشد، دکمه‌ها را نشان می‌دهیم
    if not game_started:
        # رسم تصویر دکمه شروع
        start_button_rect = start_button_image.get_rect(center=(center_x, center_y))
        screen.blit(start_button_image, start_button_rect)

        # بررسی کلیک روی دکمه شروع
        if pygame.mouse.get_pressed()[0] and start_button_rect.collidepoint(pygame.mouse.get_pos()):
            game_started = True  # شروع بازی
            arrow_selected_angle = None  # بازنشانی زاویه انتخابی
            rotation_angle = 0  # بازنشانی زاویه چرخش
            speed = 10  # بازنشانی سرعت
            start_time = time.time()  # زمان شروع
    else:
        # چرخش گردونه
        current_time = time.time()
        if arrow_selected_angle is None:
            # به چرخش ادامه بده
            if current_time - start_time < 5:
                rotation_angle += speed
                speed = max(speed - deceleration, 0.1)  # کاهش سرعت
            else:
                # انتخاب زاویه تصادفی برای توقف
                arrow_selected_angle = choose_random_angle()

        if arrow_selected_angle is not None:
            # تنظیم جهت چرخش
            target_angle = normalize_angle(arrow_selected_angle)
            current_angle = normalize_angle(rotation_angle)

            # محاسبه اختلاف زاویه
            angle_difference = (target_angle - current_angle + 360) % 360

            # چرخش به سمت زاویه انتخاب شده
            if angle_difference < 180:
                rotation_angle += speed
            else:
                rotation_angle -= speed

            # اگر به زاویه انتخاب شده نزدیک شدیم، توقف کنیم
            if abs(angle_difference) < speed:
                rotation_angle = arrow_selected_angle  # توقف در زاویه انتخاب شده
                game_started = False  # پایان بازی
                time.sleep(2)  # توقف به مدت 2 ثانیه

        # رسم فلش با زاویه کنونی
        draw_arrow(screen, arrow_image, rotation_angle)

    # آپدیت صفحه
    pygame.display.flip()

    # بررسی رویدادهای خروج
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # بررسی کلید F11 برای ورود به حالت فول‌اسکرین
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f11:  # اگر F11 فشار داده شود
                # تغییر حالت به فول‌اسکرین یا پنجره‌ای
                if screen.get_flags() & pygame.NOFRAME:  # اگر در حالت فول‌اسکرین باشد
                    screen = pygame.display.set_mode((screen_width, screen_height))  # بازگشت به پنجره‌ای
                else:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # ورود به حالت فول‌اسکرین
                pygame.display.set_caption("گردونه شانس")  # عنوان پنجره

pygame.quit()
