from sounddevice import*
import numpy as np
from pygame import *
from random import randint

sr = 16000
block = 256
mic_level = 0.0

def audio_cb(indata, frames, time, status):
    global mic_level

    if status:
        return
    rms = float(np.sqrt(np.mean(indata**2)))
    mic_level = 0.85 * mic_level + 0.15 * rms

init()

win_size = 1200, 800
win = display.set_mode(win_size)
clock = time.Clock()

player_rect = Rect(150,
                   win_size[1] // 2-100,
                   100,100 )

def generate_pipes(count, pipe_width = 140, gap = 280, min_height=50,
                   max_height = 440, distance = 650):
    pipes = []
    start_x = win_size[0]

    for i in range(count):
        height = randint(min_height, max_height)

        top_pipe = Rect(start_x, 0, pipe_width, height)

        bottom_pipe = Rect(start_x, height + gap, pipe_width, win_size[1] - (height+gap))
        pipes.extend([top_pipe, bottom_pipe])
        start_x += distance
    return pipes

pies = generate_pipes(150)

main_font = font.Font(None, 100)
score = 0
lose = False
wait = 40

y_vel = 0.0
gravity = 0.6

THRESH = 0.07
IMPULSE = -8.0

with InputStream(samplerate=sr,
                 channels = 1,
                 blocksize=block,
                 callback=audio_cb):
    while True:
        for e in event.get():
            if e.type == QUIT:
                quit()

        if mic_level > THRESH:
            y_vel = IMPULSE
            y_vel += gravity
            player_rect.y += int(y_vel)
            win.fill('sky blue')
            draw.rect(win, "red", player_rect)

            for pie in pies[:]:
                if not lose:
                    pie.x -= 10

                draw.rect(win, "green", pie)

                if pie.x <= -100:
                    pies.remove(pie)
                    score += 0.5

                if player_rect.colliderect(pie):
                    lose = True

            if len(pies)<8:
                pies+= generate_pipes(150)

            score_text = main_font.render(f"{int(score)}", True, "black")
            win.blit(score_text, (win_size[0] // 2 - score_text.get_rect().w//2,40))
            display.update()
            clock.tick(60)

            keys = key.get_pressed()
            if keys[K_r] and lose:
                lose = False
                score = 0

                pies = generate_pipes(150)
                player_rect.y = win_size[1] // 2-100
                y_vel = 0.0

            if player_rect.bottom > win_size[1]:
                player_rect.bottom = win_size[1]
                y_vel = 0.0

            if player_rect.top < 0:
                player_rect.top = 0

                if y_vel < 0:
                    y_vel = 0.0

            if lose and wait > 1:

                for pie in pies:
                    pie.x += 8
                wait -= 1
            else:
                lose = False
                wait = 40


