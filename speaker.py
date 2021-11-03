import RPi.GPIO as GPIO
from time import sleep
import pygame
from threading import Timer
from mutagen.mp3 import MP3
import random

pygame.mixer.init()
music = pygame.mixer.music

pin = 40
frequency = 700
start_val = 50
reps = 10

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)

p = GPIO.PWM(pin, 50)

def old_alarm_until(should_stop, duration=0.4, delay=0.2):
    i = 0
    while not should_stop(i):
        i += 1
        sleep(delay)

def old_alarm_beep(duration=0.4):
    p.start(start_val)
    p.ChangeFrequency(frequency)
    sleep(duration)
    p.stop()

def notification():
    for _ in range(2):
        old_alarm_beep(duration=0.15)
        sleep(0.025)

old_alarm_on = False
old_alarm_timer = None
def old_alarm_start(stay_on=True):
    global old_alarm_timer

    if stay_on: old_alarm_on = True

    old_alarm_timer = Timer(0.6, lambda : old_alarm_start(False))
    old_alarm_timer.start()

    old_alarm_beep()

def old_alarm_stop():
    old_alarm_on = False
    if old_alarm_timer is not None:
        old_alarm_timer.cancel()
        old_alarm_timer.join()

all_songs = [
    'music/fix_you.mp3',
    'music/spis.mp3',
]

songs = all_songs.copy()

alarm_on = False
alarm_timer = None
def alarm_start(stay_on=True):
    global alarm_timer

    if stay_on: alarm_on = True

    song = random.choice(songs)
    songs.remove(song)
    songs.append(random.choice(all_songs))

    music.load(song)
    music.play()

    song_length = MP3(song).info.length

    alarm_timer = Timer(song_length, lambda : alarm_start(False))
    alarm_timer.start()

def alarm_stop():
    music.stop()
    if alarm_timer is not None:
        alarm_timer.cancel()
        alarm_timer.join()

if __name__ == '__main__':
    notification()
    GPIO.cleanup()

    alarm_until(lambda i: i > 20)
