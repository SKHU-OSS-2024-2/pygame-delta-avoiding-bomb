import pygame  # pygame 라이브러리 선언
import random
import os

pygame.init()  # pygame 초기화

# 게임 화면 크기 및 색상 설정
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
size = [600, 800]
screen = pygame.display.set_mode(size)

# 타이머에 사용할 폰트 설정
game_font = pygame.font.Font(None, 200)

# 게임 상태와 관련된 변수 초기화
done = False  # 게임 루프를 제어하는 변수
clock = pygame.time.Clock()  # 프레임 속도 제어를 위한 시계 객체
start_ticks = pygame.time.get_ticks()  # 시작 시간 기록
game_over = False  # 게임 오버 상태를 나타내는 변수
lives = 3  # 초기 목숨 개수 설정

def text_objects(text, font): # START버튼 
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()

# 게임 실행 함수 정의
def runGame():
    bomb_image = pygame.image.load('bomb_game/img/bomb.png')  # 폭탄 이미지 파일을 불러옴
    bomb_image = pygame.transform.scale(bomb_image, (50, 50))  # 폭탄 이미지 크기를 50x50으로 조절
    bombs = []  # 폭탄 정보를 담을 리스트 초기화
    elapsed_time = 0  # 초기화 추가

    # 초기 폭탄 5개 생성
    for i in range(5):
        rect = pygame.Rect(bomb_image.get_rect())  # 폭탄 이미지 크기와 위치 설정
        rect.left = random.randint(0, size[0])  # 폭탄의 x 좌표를 무작위로 설정
        rect.top = -100  # 폭탄의 초기 y 좌표 설정
        dy = random.randint(3 + elapsed_time // 2000, 9 + elapsed_time // 2000)  # 폭탄 낙하 속도를 무작위로 설정
        bombs.append({'rect': rect, 'dy': dy})  # 폭탄 정보를 리스트에 추가

    # 캐릭터 이미지 불러오기 및 초기 위치 설정
    person_image = pygame.image.load('bomb_game/img/person.png')
    person_image = pygame.transform.scale(person_image, (100, 100))
    person = pygame.Rect(person_image.get_rect())
    person.left = size[0] // 2 - person.width // 2  # 캐릭터를 화면 중앙에 배치
    person.top = size[1] - person.height  # 캐릭터를 화면 하단에 배치
    person_dx = 0  # 캐릭터의 초기 이동 속도 설정

    global done, game_over, lives
    font = pygame.font.SysFont(None, 75)  # 게임오버 텍스트를 위한 폰트 설정
    life_font = pygame.font.SysFont(None, 50)  # 목숨 표시를 위한 폰트 설정

    game_over_time = None #게임 오버 시간을 저장하기 위한 변수

    while not done:
        clock.tick(30)  # 초당 30프레임 설정
        screen.fill(BLACK)  # 화면을 검은색으로 채움

        # 키 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True  # 게임 종료
                break
            elif event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_LEFT:
                    person_dx = -5  # 왼쪽 키를 누르면 왼쪽으로 이동
                elif event.key == pygame.K_RIGHT:
                    person_dx = 5  # 오른쪽 키를 누르면 오른쪽으로 이동
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    person_dx = 0  # 키를 떼면 이동 정지

        # 게임 오버가 아닐 때 게임 로직 실행
        if not game_over:
            # 폭탄 이동 및 화면을 벗어난 폭탄 제거 후 새 폭탄 추가
            for bomb in bombs:
                bomb['rect'].top += bomb['dy']  # 폭탄의 y 좌표에 속도를 더하여 아래로 이동
                if bomb['rect'].top > size[1]:  # 폭탄이 화면 하단을 벗어났을 경우
                    bombs.remove(bomb)
                    rect = pygame.Rect(bomb_image.get_rect())
                    rect.left = random.randint(0, size[0])  # 새 폭탄의 x 좌표를 무작위로 설정
                    rect.top = -100  # 새 폭탄의 y 좌표 초기화
                    dy = random.randint(3 + elapsed_time // 2000, 9 + elapsed_time // 2000)  # 폭탄 낙하 속도를 무작위로 설정
                    bombs.append({'rect': rect, 'dy': dy})  # 새 폭탄 추가

            # 캐릭터 이동 처리
            person.left += person_dx  # 이동 속도를 현재 위치에 더함
            if person.left < 0:  # 화면 왼쪽을 넘어가지 않도록
                person.left = 0
            elif person.left > size[0] - person.width:  # 화면 오른쪽을 넘어가지 않도록
                person.left = size[0] - person.width

            screen.blit(person_image, person)  # 캐릭터를 화면에 그림

            # 폭탄 충돌 검사 및 목숨 감소
            for bomb in bombs:
                if bomb['rect'].colliderect(person):  # 캐릭터와 충돌 시
                    bombs.remove(bomb)
                    rect = pygame.Rect(bomb_image.get_rect())
                    rect.left = random.randint(0, size[0])  # 새 폭탄의 x 좌표 설정
                    rect.top = -100  # 새 폭탄의 y 좌표 초기화
                    dy = random.randint(3, 9)  # 낙하 속도 설정
                    bombs.append({'rect': rect, 'dy': dy})  # 새 폭탄 추가
                    lives -= 1  # 목숨 감소
                    if lives <= 0:
                        game_over = True  # 목숨이 0이면 게임 오버
                        game_over_time = (pygame.time.get_ticks() - start_ticks) / 1000 # 게임 오버 시 경과 시간 저장
                screen.blit(bomb_image, bomb['rect'])

            # 목숨 개수 표시
            lives_text = life_font.render(f"Lives: {lives}", True, WHITE)
            screen.blit(lives_text, (10, 10))


            # 경과 시간 계산 및 표시
            elapsed_time = pygame.time.get_ticks() - start_ticks
            timer = game_font.render(f"{elapsed_time // 1000} : {elapsed_time % 1000}", True, WHITE)
            screen.blit(timer, (size[0] // 2 - timer.get_width() // 2, size[1] // 2 - timer.get_height() // 2))

        # 게임 오버 시 메시지 출력
        if game_over:
            game_over_text = font.render("Game Over", True, WHITE)
            game_over_time_text = font.render(f"Time: {game_over_time:.2f} sec", True, WHITE)
            screen.blit(game_over_text, (size[0] // 2 - game_over_text.get_width() // 2, size[1] // 2 - game_over_text.get_height() // 2))
            screen.blit(game_over_time_text, (size[0] // 2 - game_over_time_text.get_width() // 2, size[1] // 2 + game_over_text.get_height()))
            pygame.display.update()

        pygame.display.update()  # 화면 업데이트

runGame()
pygame.quit()  # 게임 종료
