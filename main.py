import pygame
import random
import time
import os

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroid Survival Game")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

# Шрифты
font = pygame.font.SysFont("monospace", 40)
small_font = pygame.font.SysFont("monospace", 25)

# Загрузка ресурсов
bg_image = pygame.image.load("image\\космос.jpg")
player_image = pygame.transform.scale(pygame.image.load("image\\корабль.png"), (50, 50))
asteroid_image = pygame.transform.scale(pygame.image.load("image\\астероид.png"), (50, 50))
explosion_image = pygame.transform.scale(pygame.image.load("image\\взрыв.png"), (100, 100))

# Загрузка и воспроизведение музыки
pygame.mixer.music.load("sound\\космос.mp3")
pygame.mixer.music.play(-1)

# Кнопки главного меню
def draw_button(text, x, y, w, h):
    pygame.draw.rect(screen, GRAY, (x, y, w, h))
    label = font.render(text, True, WHITE)
    screen.blit(label, (x + (w - label.get_width()) // 2, y + (h - label.get_height()) // 2))
    return pygame.Rect(x, y, w, h)

# Главное меню
def main_menu():
    while True:
        screen.blit(pygame.transform.scale(bg_image, (WIDTH, HEIGHT)), (0, 0))
        start_btn = draw_button("СТАРТ", WIDTH // 2 - 100, 200, 200, 60)
        help_btn = draw_button("ПОМОЩЬ", WIDTH // 2 - 100, 300, 200, 60)
        exit_btn = draw_button("ВЫХОД", WIDTH // 2 - 100, 400, 200, 60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.collidepoint(event.pos):
                    return
                elif help_btn.collidepoint(event.pos):
                    show_help()
                elif exit_btn.collidepoint(event.pos):
                    pygame.quit()
                    return

        pygame.display.flip()

# Окно помощи
def show_help():
    showing = True
    while showing:
        screen.fill(BLACK)
        lines = [
            "Вы управляете космическим кораблем.",
            "Уклоняйтесь от летящих метеоритов.",
            "При столкновении теряете жизнь (всего 3).",
            "Со временем скорость астероидов увеличивается.",
            "За каждую секунду начисляются очки.",
            "Нажмите любую клавишу для возврата."
        ]
        for i, line in enumerate(lines):
            label = small_font.render(line, True, WHITE)
            screen.blit(label, (WIDTH // 2 - label.get_width() // 2, 150 + i * 40))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                showing = False

# Сохраняем результат
def save_record(name, score, time_alive):
    with open("records.txt", "a", encoding="utf-8") as f:
        f.write(f"{name};{score};{time_alive}\n")

# Показываем таблицу рекордов
def show_records():
    screen.fill(BLACK)
    records = []
    if os.path.exists("records.txt"):
        with open("records.txt", "r", encoding="utf-8") as f:
            for line in f:
                name, score, time_alive = line.strip().split(";")
                records.append((name, int(score), int(time_alive)))
        records.sort(key=lambda x: x[1], reverse=True)
    header = font.render("Таблица рекордов", True, WHITE)
    screen.blit(header, (WIDTH // 2 - header.get_width() // 2, 50))
    for i, (name, score, t) in enumerate(records[:5]):
        record_text = small_font.render(f"{i+1}. {name} - Очки: {score}, Время: {t} сек", True, WHITE)
        screen.blit(record_text, (WIDTH // 2 - record_text.get_width() // 2, 120 + i * 40))
    pygame.display.flip()
    time.sleep(5)

# Основная игра
def game():
    player_pos = [WIDTH // 2, HEIGHT - 100]
    player_speed = 10
    lives = 3
    asteroid_speed = 5
    asteroids = []
    stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT)] for _ in range(100)]
    start_time = time.time()
    explosion_occurred = False
    explosion_pos = None
    explosion_time = 0

    clock = pygame.time.Clock()
    score = 0
    game_over = False

    while not game_over:
        elapsed_time = int(time.time() - start_time)
        score = elapsed_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - 50:
            player_pos[0] += player_speed

        # Движение звезд
        for star in stars:
            star[1] += 2
            if star[1] > HEIGHT:
                star[0] = random.randint(0, WIDTH)
                star[1] = 0

        # Генерация астероидов
        if random.randint(1, 20) == 1:
            asteroids.append([random.randint(0, WIDTH - 50), 0])

        # Движение астероидов
        for asteroid in asteroids[:]:
            asteroid[1] += int(asteroid_speed)
            if asteroid[1] > HEIGHT:
                asteroids.remove(asteroid)

        # Столкновения
        for asteroid in asteroids[:]:
            if (player_pos[0] < asteroid[0] + 50 and player_pos[0] + 50 > asteroid[0]) and \
               (player_pos[1] < asteroid[1] + 50 and player_pos[1] + 50 > asteroid[1]):
                lives -= 1
                explosion_occurred = True
                explosion_pos = asteroid[:]
                explosion_time = time.time()
                asteroids.remove(asteroid)
                if lives == 0:
                    game_over = True

        # Увеличение сложности
        if elapsed_time % 10 == 0:
            asteroid_speed += 0.02

        # Отрисовка
        screen.fill(BLACK)
        for star in stars:
            pygame.draw.circle(screen, WHITE, (star[0], star[1]), 2)
        screen.blit(player_image, tuple(player_pos))
        for asteroid in asteroids:
            screen.blit(asteroid_image, asteroid)
        if explosion_occurred:
            screen.blit(explosion_image, (explosion_pos[0] - 25, explosion_pos[1] - 25))
            if time.time() - explosion_time > 1:
                explosion_occurred = False
        screen.blit(font.render(f"Жизни: {lives}", True, WHITE), (10, 10))
        screen.blit(font.render(f"Очки: {score}", True, WHITE), (10, 50))
        pygame.display.flip()
        clock.tick(30)

    # Конец игры
    name = input_name(score, elapsed_time)
    save_record(name, score, elapsed_time)
    show_records()

# Ввод имени
def input_name(score, time_alive):
    name = ""
    active = True
    while active:
        screen.fill(BLACK)
        prompt = font.render("Введите имя:", True, WHITE)
        screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, 200))
        name_render = font.render(name + "|", True, WHITE)
        screen.blit(name_render, (WIDTH // 2 - name_render.get_width() // 2, 300))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "Игрок"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 10:
                        name += event.unicode
    return name or "Игрок"

# Запуск
main_menu()
game()
pygame.quit()
