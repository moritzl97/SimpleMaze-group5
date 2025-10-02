import sys

from game.utils import clear_screen
import os

def title_screen():
    # start game
    # load game
    # highscores
    # credits
    cmd = 'mode 50,20'
    os.system(cmd)
    cmd = 'color 5E'
    os.system(cmd)

    while True:
        clear_screen()
        print("Escape of the Nightmare\n")
        print("Start game\nLoad game\nHighscores\nCredits\nExit game")
        command = input("").strip().lower()

        if command == "start game":
            clear_screen()
            return None
        elif command == "load game":
            #load game
            pass
        elif command == "highscores":
            # call status command
            pass
        elif command == "credits":
            end_screen()
        elif command == "exit" or command == "exit game":
            # call exit function
            sys.exit()

def pause_screen():
    clear_screen()
    print("Resume\nExit game")
    # call pause function

    command = input("").strip().lower()
    if command == "exit" or command == "exit game":
        # call exit function
        pass
    return

def end_screen():
    # credits
    clear_screen()
    print("Moritz Lackner\nOskar Lukáč\nDominika Nowakiewicz\nMihail Petrov\nRodrigo Polo Lopez\nTieme van Rees")

    input("").strip().lower()
    return
