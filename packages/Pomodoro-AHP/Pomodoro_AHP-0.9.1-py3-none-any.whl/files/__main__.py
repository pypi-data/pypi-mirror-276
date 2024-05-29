#starting of the project
import sys
from .stopwatch_default import pomodoro_timer as prova 
from .stopwatch_custom_time import pomodoro_timer as prova_CT
from .stopwatch import customizable_timer as stopwatch
import os
def cls():
    os.system('cls' if os.name in ('nt', 'dos') else 'clear')
cls()
# print("hell ow")
def start():
    print("""    
    =====================================
    |1| Default: 25m focus / 5m break  ||
    |==================================|| 
    |2| Custom Time                    ||
    |==================================||
    |3| Timer                          ||
    =====================================
    """
    )

    if len(sys.argv) > 1:
        if sys.argv[1] == "1":
            prova()

        elif sys.argv[1] == "2":
            prova_CT()

        elif sys.argv[1] == "3":
            stopwatch()

        else:
            print("Invalid input. Please select a valid mode.")
            return

        return

    while True:
        user_input = input("Which mode do you want to select: ")

        if user_input == "1":
            prova()  
            break

        elif user_input == "2":
            prova_CT()  
            break

        elif user_input == "3":
            stopwatch()  
            break

        else:
            print("Invalid input. Please select a valid mode.")
            
if __name__ == "__main__":
    start()