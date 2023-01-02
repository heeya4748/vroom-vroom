import pygame
import time
import random
import pickle
from functools import cache
# import ctypes

pygame.init()
pygame.key.set_repeat(800, 50)
pygame.display.set_caption("붕붕붕")

WHITE = (255, 255, 255)
RED = (255, 50, 50)
BLUE = (0, 0, 255)
GREEN = (50, 255, 50)
GRAY = (50, 50, 50)
BLACK = (0, 0 ,0)
FPS = 60
# u32 = ctypes.windll.user32
# size = (u32.GetSystemMetrics(0), u32.GetSystemMetrics(1)) # (1536, 864)
size = (1280, 720)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
done = False

check_sound = pygame.mixer.Sound("./audio/notice.mp3")
ready_sound = pygame.mixer.Sound("./audio/race_ready.wav")
bgm = pygame.mixer.music.load("./audio/Hey_Bumboo_opening.mp3")
atk_sound = []
for i in ["right", "left", "back", "up"]:
    atk_sound.append(pygame.mixer.Sound(f"./audio/{i}.wav"))
play_sound = True

@cache
def font(size):
    return pygame.font.Font('./font/NotoSansKR-Medium.otf', size)

pygame.mixer.music.play(-1)

# 글씨 작성
def write(txt, font_size, color, center_pos):
    txt = font(font_size).render(txt, True, color)
    txt_center = txt.get_rect()
    txt_center.center = center_pos
    screen.blit(txt, txt_center)

with open("play_log.pickle", "rb") as fr:
    player_log = pickle.load(fr)
player_info = ["" for i in range(6)]
player_coin = ["" for i in range(6)]

# 붕붕붕 이용자 정보 입력(중복 확인), 배팅 금액 입력
def add_player_info():
    global player_info
    global player_coin
    max_play = 2

    class txt_box():
        def __init__(self, size, pos, is_indi_info):
            self.size = size
            self.pos = pos
            self.text = ""
            self.check_log = is_indi_info

        def show(self):
            pygame.draw.rect(screen, WHITE, (self.pos[0], self.pos[1], self.size[0], self.size[1]))
            txt = font(50).render(self.text, True, BLACK)
            txt_topleft = txt.get_rect()
            txt_topleft.topleft = (self.pos[0], self.pos[1]-13)
            screen.blit(txt, txt_topleft)

        def click(self, cursor_pos):
            if cursor_pos[0] >= self.pos[0] and cursor_pos[0] <= self.pos[0] + self.size[0]:
                if cursor_pos[1] >= self.pos[1] and cursor_pos[1] <= self.pos[1] + self.size[1]:
                    return True
            return False

    class button():
        def __init__(self, size, pos):
            self.size = size
            self.pos = pos
            self.confirmed = False

        def show(self):
            color = RED
            text = "입장 불가"
            if self.confirmed:
                color = GREEN
                text = "입장 가능"
            pygame.draw.rect(screen, color, (self.pos[0], self.pos[1], self.size[0], self.size[1]))
            txt = font(30).render(text, True, BLACK)
            txt_topleft = txt.get_rect()
            txt_topleft.topleft = (self.pos[0]+7, self.pos[1])
            screen.blit(txt, txt_topleft)

    def get_num(num):
        key = [[i+48 for i in range(10)], [i+1073741913 for i in range(9)]]
        key[1].insert(0, 1073741922)

        for i in range(10):
            if num == key[0][i] or num == key[1][i]:
                return i
        if num == 8:
            return -1
        elif num == 13 or num == 1073741903:
            return 10
        elif num == 1073741904:
            return 11
        elif num == 1073741906:
            return 12
        return -2

    def check_log(player_num):
        if len(player_num) != 5:
            return False
        for i in range(len(player_log["class_num"])):
            if player_num == player_log["class_num"][i]:
                if player_log["play_num"][i] >= max_play:
                    return False
        return True

    done = False
    input_num = -2
    cursor_pos = (0, 0)

    box_on_cursor = 0
    box_list = []
    button_list = []

    volume_t = time.time()
    volume = 1

    for i in range(6):
        box_list.append(txt_box((500, 50), (100, 100+100*i), True))
        box_list.append(txt_box((100, 50), (800, 100+100*i), False))
        button_list.append(button((130, 50), (600, 100+100*i)))

    while not done:
        clock.tick(FPS)
        screen.fill(BLACK)

        if time.time() - volume_t >= 0.1 and volume > 0.5:
            volume -= 0.1
            pygame.mixer.music.set_volume(volume)
            volume_t = time.time()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                cursor_pos = pygame.mouse.get_pos()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    done = True
                input_num = get_num(event.key)

        if input_num == -1:
            # 백스패이스를 눌러 끝 글자 지우기
            box_list[box_on_cursor].text = box_list[box_on_cursor].text[:-1]
            input_num = -2
        elif input_num == 10 and box_on_cursor < len(box_list)-1:
            # 엔터 또는 화살표를 눌러 다음 박스에 커서 이동
            box_on_cursor += 1
            input_num = -2
        elif input_num == 11:
            # 화살표를 눌러 이전 박스에 커서 이동
            box_on_cursor -= 1
            input_num = -2
        elif input_num == 12:
            # 위 화살표를 눌러 이전 학번 데이터 불러오기
            with open("./record_log.pickle", "rb") as fr:
                player_info_log = pickle.load(fr)
            player_info = player_info_log[-1]
            del player_info[-1]
            for i in range(len(player_info[-1])):
                player_coin[i] = str(player_info[-1][i])
            del player_info[-1]
            for i in range(6):
                box_list[2*i].text = player_info[i]
            for i in range(6):
                box_list[2*i+1].text = player_coin[i]
            input_num = -2
        elif input_num != -2:
            # 숫자 입력시 텍스트로 저장
            box_list[box_on_cursor].text += str(input_num)
            input_num = -2

        for i in range(6):
            player_info[i] = box_list[2*i].text

        for i in range(6):
            player_coin[i] = box_list[2*i+1].text

        for i in range(len(box_list)):
            if box_list[i].click(cursor_pos):
                box_on_cursor = i
                cursor_pos = (0, 0)
            box_list[i].show()
        for i in range(len(button_list)):
            button_list[i].confirmed = check_log(player_info[i])
            button_list[i].show()

        pygame.display.update()

    # 입력된 정보 바탕으로 이용자 기록 업데이트
    for i in player_info:
        is_new_player = True
        if i == "":
            continue
        for j in range(len(player_log["class_num"])):
            if i == player_log["class_num"][j]:
                player_log["play_num"][j] += 1
                is_new_player = False
                break
        if is_new_player:
            player_log["class_num"].append(i)
            player_log["play_num"].append(1)

    # 배팅 코인을 정수로 변환
    for i in range(len(player_coin)):
        if player_coin[i] != "":
            player_coin[i] = int(player_coin[i])
        else:
            player_coin[i] = 0

    with open("play_log.pickle", "wb") as fw:
        pickle.dump(player_log, fw)

# n단계 클리어 후 멈췄을 때 개인별 지급 금액 출력
def stop_game(round):
    global player_info
    global player_coin
    global reward
    done = False
    round -= 1

    player_info.append(player_coin)
    if round == 1:
        player_info.append(10)
    elif round == 2:
        player_info.append(25)
    elif round == 3:
        player_info.append(45)

    with open("record_log.pickle", "rb") as fr:
        record_log = pickle.load(fr)
    record_log.append(player_info)
    with open("record_log.pickle", "wb") as fw:
        pickle.dump(record_log, fw)

    while not done:
        clock.tick(FPS)
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    done = True
        
        write(f"{round}단계 성공 보상", 100, WHITE, (size[0]//2, size[1]//2-100))

        for i in range(len(player_coin)):
            coin = player_coin[i]
            y = size[1]//2 + 40*i + 50
            if player_coin[i]:
                write(player_info[i], 40, WHITE, (size[0]//3, y))
                write(f"{coin}", 40, WHITE, (size[0]//2, y))
                write(">>", 40, WHITE, (size[0]*7//12, y))
                write(f"{coin*reward[round]}", 40, WHITE, (size[0]*2//3, y))

        pygame.display.update()
    
    player_info = ["" for i in range(6)]
    player_coin = ["" for i in range(6)]

# 실패 시
def game_over(round, record):
    global player_info
    global player_coin
    go_main = False

    check_sound.stop()
    ready_sound.stop()

    player_info.append(player_coin)
    if round == 1:
        player_info.append(record)
    if round == 2:
        player_info.append(record+10)
    if round == 3:
        player_info.append(record+25)

    with open("record_log.pickle", "rb") as fr:
        record_log = pickle.load(fr)
    record_log.append(player_info)
    with open("record_log.pickle", "wb") as fw:
        pickle.dump(record_log, fw)

    player_info = ["" for i in range(6)]
    player_coin = ["" for i in range(6)]

    while True:
        clock.tick(FPS)
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    go_main = True
        if go_main:
            break

        write(f"{round}단계 실패", 100, WHITE, (size[0]//2, size[1]//2))

        pygame.display.update()

# 게임 진행
def ingame(round, goal):
    fail = False
    color = WHITE
    state = "ready"
    ready_text = [f"{round}단계", "준비", "3", "2", "1", "출발"]
    count = 0
    success = 0 # 성공 횟수
    attack = ["우회전", "좌회전", "후진", "방지턱"]
    pre_atk = "출발"
    color = [WHITE for i in range(goal[round])]
    if round == 3:
        delay = 1 # default = 1
        red_pos = random.sample(list(range(0, goal[round])), 5)
    elif round == 2:
        delay = 2 # default = 2
        red_pos = random.sample(list(range(0, goal[round])), 5)
    elif round == 1:
        delay = 2 # default = 2
        red_pos = []
    for i in red_pos:
        color[i] = RED

    if round == 1 or player_info[0] == "":
        add_player_info()

    def get_atk(pre_atk):
        while True:
            atk = random.choice(attack)
            if atk != pre_atk:
                return atk

    start_t = time.time()

    while not fail:
        clock.tick(FPS)
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return False, success

        if state == "ready":
            write(ready_text[count], 100, WHITE, (size[0]//2, size[1]//2))
            if count < len(ready_text)-1 and time.time() - start_t >= 1:
                count += 1
                if count == 2 and play_sound:
                    ready_sound.play()
                start_t = time.time()
            if count == len(ready_text)-1 and time.time() - start_t >= 1.7:
                state = "game"
                start_t = time.time()
                atk_text = get_atk(pre_atk)
                pre_atk = atk_text
                if play_sound:
                    for i in range(len(attack)):
                        if attack[i] == atk_text:
                            atk_sound[i].play()
        elif state == "game":
            if time.time() - start_t >= delay:
                success += 1
                atk_text = get_atk(pre_atk)
                pre_atk = atk_text
                start_t = time.time()
                if success < goal[round] and play_sound:
                    for i in range(len(attack)):
                        if attack[i] == atk_text:
                            atk_sound[i].play()
            if success >= goal[round]:
                state = "end"
                start_t = time.time()
                continue
            write(atk_text, 100, color[success], (size[0]//2, size[1]//2))
        elif state == "end":
            if time.time() - start_t <= 2:
                write("정지", 100, WHITE, (size[0]//2, size[1]//2))
            else:
                pygame.display.update()
                break

        pygame.display.update()

    return True, 0

round = 1
goal = [0, 10, 15, 20]
reward = [0, 1, 2, 3]
success = False

volume_t = time.time()
volume = 0.5

while not done:
    clock.tick(FPS)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and not success:
                done = True
            if event.key == pygame.K_SPACE:
                success, record = ingame(round, goal)
                if success:
                    round += 1
                else:
                    game_over(round, record)
                    volume = 0.5
                    round = 1
            if event.key == pygame.K_BACKSPACE and round > 1:
                stop_game(round)
                volume = 0.5
                round = 1
                success = False
            if event.key == pygame.K_UP and round < 3:
                round += 1
            if event.key == pygame.K_DOWN and round > 1:
                round -= 1
    
    if success and round == 4:
        stop_game(round)
        round = 1
        success = False
    elif success and round != 4:
        write(f"{round}단계 도전?", 100, WHITE, (size[0]//2, size[1]//2))
        write(f"X{reward[round-1]}  >>  X{reward[round]}", 50, WHITE, (size[0]//2, size[1]//2+100))
    else:
        if time.time() - volume_t >= 0.1 and volume < 1:
            volume += 0.1
            pygame.mixer.music.set_volume(volume)
            volume_t = time.time()
        write("붕붕붕", 100, WHITE, (size[0]//2, size[1]//2))

    pygame.display.update()

pygame.quit()