# stopwatch_function.py
import sys
import time
import keyboard

def customizable_timer():
    # Get timer duration from the user
    try:
        duration_minutes = int(input("Enter the timer duration in minutes: "))  if len(sys.argv) < 3 else int(sys.argv[2])
        if duration_minutes <= 0:
            raise ValueError("Duration must be a positive number.")
    except ValueError as e:
        print(f"Invalid input: {e}")
        return
    
    total_duration = duration_minutes * 60
    print("Timer started. Press SPACE to pause.")

    start_time = time.time()
    remaining_time = total_duration
    running = True

    while True:
        if keyboard.is_pressed('space') and running:
            running = False

        if not running:
            while True:
                if keyboard.is_pressed('space+c'):
                    start_time = time.time() - (total_duration - remaining_time)
                    running = True
                    print("Timer continued.")
                    break
                elif keyboard.is_pressed('space'):
                    print("\nTimer stopped.")
                    return
                time.sleep(0.1)  # To avoid high CPU usage

        if running:
            elapsed_time = time.time() - start_time
            remaining_time = total_duration - elapsed_time
            if remaining_time <= 0:
                print("\nTime's up!")
                return
            mins = int(remaining_time // 60)
            secs = int(remaining_time % 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(timer, end='\r')
            time.sleep(0.01)

# Testing the customizable timer function
if __name__ == "__main__":
    customizable_timer()
