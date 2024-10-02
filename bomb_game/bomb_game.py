import pygame  # 1. pygame 선언
import random
import os

pygame.init()  # 2. pygame 초기화

# 3. pygame에 사용되는 전역변수 선언

BLACK = (0, 0, 0)
size = [600, 800]
screen = pygame.display.set_mode(size)

#화면에 글자를 띄우기 위한 폰트
game_font = pygame.font.Font(None, 200)

done = False
clock = pygame.time.Clock()

#시간 정보
start_ticks = pygame.time.get_ticks()

def runGame():
    bomb_image = pygame.image.load('/Users/cho/2024/오픈소스 SW개발/delta/pygame-delta-avoiding-filth/bomb_game/bomb.png')
    bomb_image = pygame.transform.scale(bomb_image, (50, 50))
    bombs = []

    for i in range(5):
        rect = pygame.Rect(bomb_image.get_rect())
        rect.left = random.randint(0, size[0])
        rect.top = -100
        dy = random.randint(3, 9)
        bombs.append({'rect': rect, 'dy': dy})

    person_image = pygame.image.load('/Users/cho/2024/오픈소스 SW개발/delta/pygame-delta-avoiding-filth/bomb_game/person.png')
    person_image = pygame.transform.scale(person_image, (100, 100))
    person = pygame.Rect(person_image.get_rect())
    person.left = size[0] // 2 - person.width // 2
    person.top = size[1] - person.height
    person_dx = 0
    person_dy = 0

    global done
    while not done:
        clock.tick(30)
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    person_dx = -5
                elif event.key == pygame.K_RIGHT:
                    person_dx = 5
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    person_dx = 0
                elif event.key == pygame.K_RIGHT:
                    person_dx = 0

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
                done = True
            screen.blit(bomb_image, bomb['rect'])

        #경과시간 계산
        elapsed_time = (pygame.time.get_ticks() - start_ticks)

        #타이머 화면 출력
        timer = game_font.render(str(int(elapsed_time // 1000)) + ' : ' + str(int(elapsed_time % 1000)), True, (255,255,255))

        #시간 화면에 뜨게
        screen.blit(timer, (size[0]//2 - (timer.get_width() //2), size[1]//2 - (timer.get_height()//2)))

        pygame.display.update()

runGame()
pygame.quit()