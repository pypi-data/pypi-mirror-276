import os
import time
from pygame import mixer
import keyboard

def pomodoro_timer():
    work_time = 25 * 60  
    short_break = 5 * 60  
    long_break = 15 * 60  

    cycles = 0  

    script_dir = os.path.dirname(os.path.abspath(__file__))
    audio_file = os.path.join(script_dir, 'ting-tong.mp3')

    mixer.init()  # Initialize the mixer once before the loop

    print("Press the spacebar at any time to stop the timer and exit.")

    while True:
        print("Start working! Pomodoro timer started.")
        for i in range(work_time, 0, -1):
            if keyboard.is_pressed('space'):
                print("\nTimer interrupted. Exiting...")
                return
            mins = i // 60
            secs = i % 60
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(timer, end='\r')
            time.sleep(1)

        cycles += 1

        if cycles % 4 == 0:
            print("\nTime for a long break!")
            mixer.music.load(audio_file)
            mixer.music.play()
            time.sleep(4)
            mixer.music.stop()
            for j in range(long_break, 0, -1):
                if keyboard.is_pressed('space'):
                    print("\nTimer interrupted. Exiting...")
                    return
                mins = j // 60
                secs = j % 60
                timer = '{:02d}:{:02d}'.format(mins, secs)
                print(timer, end='\r')
                time.sleep(1)
        else:
            print("\nTime for a short break!")
            mixer.music.load(audio_file)
            mixer.music.play()
            time.sleep(10)
            mixer.music.stop()
            for k in range(short_break, 0, -1):
                if keyboard.is_pressed('space'):
                    print("\nTimer interrupted. Exiting...")
                    return
                mins = k // 60
                secs = k % 60
                timer = '{:02d}:{:02d}'.format(mins, secs)
                print(timer, end='\r')
                time.sleep(1)

        exit = input("\nContinue? (if yes press y else press n): ")
        if exit.lower() != 'y':
            print("Sayonara!")
            break

# pomodoro_timer()
