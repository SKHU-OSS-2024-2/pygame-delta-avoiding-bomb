import pygame  # 1. pygame 선언
import random
import os

pygame.init()  # 2. pygame 초기화

# 3. pygame에 사용되는 전역변수 선언

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
size = [600, 800]
screen = pygame.display.set_mode(size)

# 화면에 글자를 띄우기 위한 폰트
game_font = pygame.font.Font(None, 200)

done = False
clock = pygame.time.Clock()

start_ticks = pygame.time.get_ticks()

game_over = False  # 게임 오버 상태를 나타내는 변수
lives = 3  # 목숨 변수 추가

def runGame():
    bomb_image = pygame.image.load('bomb_game/img/bomb.png')
    bomb_image = pygame.transform.scale(bomb_image, (50, 50))
    bombs = []

    for i in range(5):
        rect = pygame.Rect(bomb_image.get_rect())
        rect.left = random.randint(0, size[0])
        rect.top = -100
        dy = random.randint(3, 9)
        bombs.append({'rect': rect, 'dy': dy})

    person_image = pygame.image.load('bomb_game/img/person.png')
    person_image = pygame.transform.scale(person_image, (100, 100))
    person = pygame.Rect(person_image.get_rect())
    person.left = size[0] // 2 - person.width // 2
    person.top = size[1] - person.height
    person_dx = 0

    global done, game_over, lives
    font = pygame.font.SysFont(None, 75)  # 게임오버 텍스트를 위한 폰트 설정
    life_font = pygame.font.SysFont(None, 50)  # 목숨 표시를 위한 폰트 설정

    while not done:
        clock.tick(30)
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                break
            elif event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_LEFT:
                    person_dx = -5
                elif event.key == pygame.K_RIGHT:
                    person_dx = 5
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    person_dx = 0
                elif event.key == pygame.K_RIGHT:
                    person_dx = 0

        if not game_over:
            for bomb in bombs:
                bomb['rect'].top += bomb['dy']
                if bomb['rect'].top > size[1]:
                    bombs.remove(bomb)
                    rect = pygame.Rect(bomb_image.get_rect())
                    rect.left = random.randint(0, size[0])
                    rect.top = -100
                    dy = random.randint(3, 9)
                    bombs.append({'rect': rect, 'dy': dy})

            person.left = person.left + person_dx

            if person.left < 0:
                person.left = 0
            elif person.left > size[0] - person.width:
                person.left = size[0] - person.width

            screen.blit(person_image, person)

            for bomb in bombs:
                if bomb['rect'].colliderect(person):
                    bombs.remove(bomb)  # 충돌한 폭탄을 없앰
                    rect = pygame.Rect(bomb_image.get_rect())
                    rect.left = random.randint(0, size[0])
                    rect.top = -100
                    dy = random.randint(3, 9)
                    bombs.append({'rect': rect, 'dy': dy})

                    lives -= 1  # 목숨을 1 감소시킴
                    if lives <= 0:
                        game_over = True  # 목숨이 0이면 게임 오버
                screen.blit(bomb_image, bomb['rect'])

            # 목숨 표시
            lives_text = life_font.render(f"Lives: {lives}", True, WHITE)
            screen.blit(lives_text, (10, 10))

            # 경과시간 계산
            elapsed_time = (pygame.time.get_ticks() - start_ticks)

            # 타이머 화면 출력
            timer = game_font.render(str(int(elapsed_time // 1000)) + ' : ' + str(int(elapsed_time % 1000)), True, (255,255,255))

            # 시간 화면에 뜨게
            screen.blit(timer, (size[0]//2 - (timer.get_width() //2), size[1]//2 - (timer.get_height()//2)))


        if game_over:
            game_over_text = font.render("Game Over", True, WHITE)
            screen.blit(game_over_text, (size[0] // 2 - game_over_text.get_width() // 2, size[1] // 2 - game_over_text.get_height() // 2))
            pygame.display.update()

        pygame.display.update()

runGame()
pygame.quit()