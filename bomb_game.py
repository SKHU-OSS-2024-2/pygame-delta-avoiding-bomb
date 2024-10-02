import pygame  # 1. pygame 선언
import random
import os

pygame.init()  # 2. pygame 초기화

# 3. pygame에 사용되는 전역변수 선언

# 게임 화면 크기 및 배경 색 지정
BLACK = (0, 0, 0)
size = [600, 800]
screen = pygame.display.set_mode(size)

done = False
clock = pygame.time.Clock()

def runGame():
    bomb_image = pygame.image.load('bomb.png')  # pygame.image.load() 함수를 이용하여 폭탄 이미지 파일을 불러오는 코드
    bomb_image = pygame.transform.scale(bomb_image, (50, 50))   # pygmae.transform.scale() 함수를 통해서 bomb_image의 크기를 50X50으로 조절
    bombs = []  # 이후 Rect()로 생성할 폭탄들을 담을 리스트를 선언해주는 코드

    # 총 5개의 폭탄을 생성하기 위한 for 반복문 코드
    for i in range(5):
        rect = pygame.Rect(bomb_image.get_rect())   # Rect() 함수를 통해서 폭탄 이미지의 사각형 크기를 가져와 네모난 사격형 안에 폭탄 이미지를 넣어주는 코드

        # 앞서 가져온 사각형의 좌표를 설정해주는데 먼저, left라는 변수를 random 값을 넣어 스크린의 width(size[0]) 안에 속하는 랜덤 x 좌표를 설정해주고, 
        # top이라는 변수에는 폭탄의 시작점을 설정
        rect.left = random.randint(0, size[0])
        rect.top = -100
        dy = random.randint(3, 9)   # 폭탄의 속도를 정해주는 dy 변수를 선언해주는데 각 폭탄이 떨어지는 속도를 다르게 하기위해 random.randint() 함수를 통해 랜덤값을 넣어줍니다
        bombs.append({'rect': rect, 'dy': dy})  # 앞서 생성한 객체와 변수를 bombs 리스트 안에 삽입하는 코드

    # 캐릭터 관련 코드
    # Rect() 안에 person_image를 담아 생성해주는 코드
    person_image = pygame.image.load('person.png')
    person_image = pygame.transform.scale(person_image, (100, 100))
    person = pygame.Rect(person_image.get_rect())
    person.left = size[0] // 2 - person.width // 2  # person의 x 좌표 위치를 담는 변수입니다. 초기에는 정중앙에 설정을 해야 함으로, 게임판의 width(size[0])을 기반으로 중앙에 설정
    person.top = size[1] - person.height    # 게임판의 heigth(size[1])을 기반으로 최하단에 위치 시키는 코드
    # 폭탄과 다르게 캐릭터는 사용자의 입력 기반으로 이벤트 처리가 일어나기에 이동속도는 0으로 초기화 해주는 코드
    person_dx = 0
    person_dy = 0

    global done
    while not done:
        clock.tick(30)
        screen.fill(BLACK)

        # 키보드 이벤트 처리를 통한 캐릭터 제어
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # 키보드의 왼쪽 방향키 이벤트가 발생했을 때, person_dx의 값을 -5로 설정하여 person의 left를 5의 값으로 빼주기
                    person_dx = -5
                elif event.key == pygame.K_RIGHT:   # 반대로 오른쪽 방향키 이벤트가 발생했을 때, person_dx의 값을 5로 설정하여 person의 left를 5의 값으로 더해주기
                    person_dx = 5

            # 위의 라인대로 키보드가 눌려지고 있을 때는 지속적으로 이동하도록 하며 이번에는 키보드가 눌렀다 띄어졌을 때는 이동하지 않도록 설정
            # 키보드의 왼쪽 방향키와 오른쪽 방향키가 띄어지는 이벤트가 각각 발생했을 때는, person_dx값을 0으로 설정하여 person의 left값이 변하지 않도록 설정
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    person_dx = 0
                elif event.key == pygame.K_RIGHT:
                    person_dx = 0

        # 폭탄 출력
        for bomb in bombs:  # 먼저 for in 문을 통해 bombs 리스트의 bomb 요소들을 반목분을 돌며 처리
            bomb['rect'].top += bomb['dy']  # bomb 객체 안의 'rect'라는 사격형 도형의 위치에 랜덤으로 생성한 dy값을 추가하여 -100 부터 시작된 위치에서 점점 내려오도록 설정
            if bomb['rect'].top > size[1]:  # 폭탄의 위치가 heigth 바닥을 넘어갔을때, 새롭게 생성하도록 하는 코드
                bombs.remove(bomb)  # 해당 폭탄 객체를 제거
                rect = pygame.Rect(bomb_image.get_rect())   # 앞서 폭탄을 초기화 하던 방식과 동일하게 새로운 폭탄을 생성해주고 리스트에 추가해주도록 해주는 코드
                rect.left = random.randint(0, size[0])
                rect.top = -100
                dy = random.randint(3, 9)
                bombs.append({'rect': rect, 'dy': dy})

        # 캐릭터 출력
        person.left = person.left + person_dx   # person의 left 값에 키보드 처리로 설정한 person_dx 값을 더해 위치를 조정

        # 캐릭터가 만약 좌측 끝점(0값) 혹은 우측 끝 지점(size[0] 값: 600) 에 도달하게 되면 더 이상 이동하지 않도록 설정하는 코드입니다.
        # 만약 캐릭터의 끝값을 조정해주지 않는다면 무한정 옆으로 이동하게 되어 초기에 설정한 게임판 안에 더이상 캐릭터가 보이지 않게 되기 때문에 필수적으로 처리해야 하는 부분
        if person.left < 0:
            person.left = 0
        elif person.left > size[0] - person.width:
            person.left = size[0] - person.width

        screen.blit(person_image, person)   # blit()함수를 통해 person 이미지를 기반으로 person 사각형을 그려주는 코드

        # 캐릭터와 폭탄이 접촉했을 때 게임 종료 코드
        # 앞서 선언한 bombs리스트 안의 요소들을 돌면서 반복문을 실행 
        for bomb in bombs:
            # bomb객체 안의 사각형을 이용하여 colliderect() 함수에 캐릭터 사각형 도형(person)을 인자로 넣어 접촉을 판단
            # 접촉이 되면(True 가 리턴) done을 True로 변경하여 게임을 종료
            if bomb['rect'].colliderect(person):    
                done = True
            screen.blit(bomb_image, bomb['rect'])   # 리스트를 반목문을 통해 돌며 폭탄을 화면에 출력

        pygame.display.update() # 마지막으로 게임판의 디스플레이를 업데이트 하여 앞서 설정한 요소들이 화면에 업데이트


runGame()
pygame.quit()