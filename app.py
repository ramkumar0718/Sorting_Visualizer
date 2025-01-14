import pygame
import random
import math
import time
from sorting_algorithms import *
pygame.init()

class Draw_Information():
    TOP_PAD = 150
    SIDE_PAD = 100

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)

    LARGE_FONT = pygame.font.Font("fonts/Poppins-Medium.ttf", 30)
    FONT = pygame.font.Font("fonts/Poppins-Regular.ttf", 20)

    def __init__(self, WIDTH, HEIGHT, num_list):
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(num_list)

    def set_list(self, num_list):
        self.num_list = num_list
        self.min_val = min(num_list)
        self.max_val = max(num_list)

        self.bar_width = round((self.WIDTH - self.SIDE_PAD) / len(num_list))
        self.bar_height = math.floor((self.HEIGHT - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_bar = self.SIDE_PAD // 2

def draw_win(draw_info, algo_name, ascending, timer, speed):
    draw_info.WIN.fill(draw_info.BLACK)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.WHITE)
    draw_info.WIN.blit(title, (draw_info.WIDTH/2 - title.get_width()/2, 10))

    time = draw_info.FONT.render(f"Time : {round(timer,2) if (timer is not None and isinstance(timer, float)) else '---'} sec", 1, draw_info.GREEN)
    draw_info.WIN.blit(time, ((draw_info.WIDTH - time.get_width()/2)-draw_info.SIDE_PAD, draw_info.TOP_PAD//10))

    speed = draw_info.FONT.render(f"Speed : {speed}", 1, draw_info.GREEN)
    draw_info.WIN.blit(speed, ((draw_info.SIDE_PAD - speed.get_width()/2)-draw_info.SIDE_PAD//10, draw_info.TOP_PAD//10))

    control_letters = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.WHITE)
    draw_info.WIN.blit(control_letters, (draw_info.WIDTH/2 - control_letters.get_width()/2, (draw_info.TOP_PAD//3)*1.1))

    control_arrows = draw_info.FONT.render("UP - Speed Inc | DOWN - Speed Dec | RIGHT - Step By Step", 1, draw_info.WHITE)
    draw_info.WIN.blit(control_arrows, (draw_info.WIDTH/2 - control_arrows.get_width()/2, (draw_info.TOP_PAD//3)*1.7))

    sorting_algos = draw_info.FONT.render("B - Bubble Sort | I - Insertion Sort | S - Selection Sort", 1, draw_info.WHITE)
    draw_info.WIN.blit(sorting_algos, (draw_info.WIDTH/2 - sorting_algos.get_width()/2, (draw_info.TOP_PAD//3)*2.3))

    sorting_algos = draw_info.FONT.render("M - Merge Sort | Q - Quick Sort | H - Heap Sort", 1, draw_info.WHITE)
    draw_info.WIN.blit(sorting_algos, (draw_info.WIDTH/2 - sorting_algos.get_width()/2, (draw_info.TOP_PAD//3)*2.9))

    draw_list(draw_info)
    pygame.display.update()

def draw_speed(draw_info, speed):
    clear_rect = (0, 0, draw_info.WIDTH//4, draw_info.HEIGHT//14)
    pygame.draw.rect(draw_info.WIN, draw_info.BLACK, clear_rect)

    speed = draw_info.FONT.render(f"Speed : {speed}", 1, draw_info.GREEN)
    draw_info.WIN.blit(speed, ((draw_info.SIDE_PAD - speed.get_width()/2)-draw_info.SIDE_PAD//10, draw_info.TOP_PAD//10))

    pygame.display.update()

def draw_list(draw_info, color_position={}, clear_bg=False):
    num_list = draw_info.num_list
    border_width = 2

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
                        draw_info.WIDTH - draw_info.SIDE_PAD, draw_info.HEIGHT - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.WIN, draw_info.BLACK, clear_rect)

    for i, bar in enumerate(num_list):
        x = draw_info.start_bar + i * draw_info.bar_width
        y = draw_info.HEIGHT - (bar - draw_info.min_val) * draw_info.bar_height
        color = draw_info.WHITE

        if i in color_position:
            color = color_position[i]

        bar_rect = pygame.Rect(x, y, draw_info.bar_width, draw_info.HEIGHT)
        pygame.draw.rect(draw_info.WIN, color, bar_rect)
        pygame.draw.rect(draw_info.WIN, draw_info.BLACK, (bar_rect.right - border_width, bar_rect.top, border_width, bar_rect.height))

    if clear_bg:
        pygame.display.update()

def generate_random_list(n, min_val, max_val):
    num_list = []

    for i in range(n):
        rand = random.randint(min_val, max_val)
        num_list.append(rand)
    return num_list


def main():
    run = True
    FPS = 60
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    sorting = False
    ascending = True

    algo_name = "Bubble Sort"
    algo_method = bubble_sort
    algo_generator = None

    num_list = generate_random_list(n, min_val, max_val)
    draw_info = Draw_Information(900, 700, num_list)
    algo_generator = algo_method(draw_info, ascending)

    start_time = None
    duration = None
    
    speed = 30
    button_used = ""
    pressed_space = False
    pressed_right = False

    while run:
        clock.tick(FPS)

        if sorting:
            if start_time is None:
                start_time = time.time()

            pygame.time.wait(max(1, 1000 // speed))
            try:
                if pressed_space or pressed_right:    
                    next(algo_generator)
                if pressed_right:
                    pressed_right = False

            except StopIteration:
                sorting = False
                pressed_space = False
                pressed_right = False
                duration = round(time.time() - start_time, 2) if "r" not in button_used else "0"
                start_time = None

        else:
            if start_time is not None:
                duration = round(time.time() - start_time, 2)
            draw_win(draw_info, algo_name, ascending, duration, speed)
        draw_speed(draw_info, speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if (event.key == pygame.K_SPACE and not sorting) or (event.key == pygame.K_RIGHT and not sorting):
                algo_generator = algo_method(draw_info, ascending)

            if event.key == pygame.K_SPACE:
                sorting = True
                button_used += "s"
                pressed_space = True
                pressed_right = False

            elif event.key == pygame.K_RIGHT:
                sorting = True
                button_used += "r"
                pressed_space = False
                pressed_right = True

            elif event.key == pygame.K_r:
                sorting = False
                button_used = ""
                speed = 30
                num_list = generate_random_list(n, min_val, max_val)
                draw_info.set_list(num_list)
                start_time = None
                duration = None

            elif event.key == pygame.K_a and not sorting:
                ascending = True

            elif event.key == pygame.K_d and not sorting:
                ascending = False

            elif event.key == pygame.K_b and not sorting:
                algo_name = "Bubble Sort"
                algo_method = bubble_sort

            elif event.key == pygame.K_i and not sorting:
                algo_name = "Insertion Sort"
                algo_method = insertion_sort

            elif event.key == pygame.K_s and not sorting:
                algo_name = "Selection Sort"
                algo_method = selection_sort

            elif event.key == pygame.K_m and not sorting:
                algo_name = "Merge Sort"
                algo_method = merge_sort

            elif event.key == pygame.K_q and not sorting:
                algo_name = "Quick Sort"
                algo_method = quick_sort    

            elif event.key == pygame.K_h and not sorting:
                algo_name = "Heap Sort"
                algo_method = heap_sort 

            elif event.key == pygame.K_UP and speed <= 90:
                speed += 10

            elif event.key == pygame.K_DOWN and speed >= 20:
                speed -= 10

if __name__ == "__main__":
    main()