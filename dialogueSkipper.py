import pyautogui
import keyboard
import pydirectinput
import dotenv
import time
import random


def overwrite_env(values: dict):
    with open('./.env', "w") as f:
        for key, value in values.items():
            f.write(f"{key}={value}\n")


def get_resolution():
    resolution = [0, 0]
    while True:
        try:
            resolution[0] = int(input("\nEnter screen width: "))
            resolution[1] = int(input("Enter screen height: "))
        except ValueError:
            print("\nInvalid input. Please enter numeric values for width and height.\n")
        else:
            return resolution


def set_resolution(res_x: int, res_y: int):
    if res_x is not None and res_y is not None:
        resolution = [res_x, res_y]
    else:
        resolution = [pyautogui.size().width, pyautogui.size().height]

    while True:
        print(f"\nDetected resolution: {resolution[0]}x{resolution[1]}")
        response = input("\nIs this correct? (y/n): ").lower()
        if response == 'n':
            resolution = get_resolution()
        elif response == 'y':
            break
        else:
            print("\nInvalid input. Please enter 'y' or 'n'.\n")

    overwrite_env({'screenResolutionX': resolution[0], 'screenResolutionY': resolution[1]})
    return tuple(resolution)


def calculate_resolution():
    env = dotenv.dotenv_values('.env')
    try:
        screenWidth = int(env.get('screenResolutionX', None))
        screenHeight = int(env.get('screenResolutionY', None))
    except (TypeError, ValueError):
        screenWidth = None
        screenHeight = None

    return set_resolution(screenWidth, screenHeight)


def toggle_start():
    global game_running
    game_running = True
    print("Dialogue skipper started...")


def toggle_pause():
    global game_running
    game_running = False
    print("Dialogue skipper paused...")


def toggle_exit():
    global program_running, game_running
    game_running = False
    program_running = False
    print("Exiting dialogue skipper...\n")


def randomize_cursor_position(target_pos: tuple, variance: int):
    rand_x = target_pos[0] + random.randint(-variance, variance)
    rand_y = target_pos[1] + random.randint(-variance, variance)
    return (rand_x, rand_y)


def randomize_sleep_time(target_time: int, variance: int):
    rand_time = target_time + random.uniform(-variance, variance)
    return rand_time


def game(resolution: list):
    global game_running
    game_running = False

    target_pos = (resolution[0] // 2, resolution[1] // 2)

    print()
    print("Press F8 to start the dialogue skipper...")
    print("Press F9 to pause the dialogue skipper...")
    print("Press F12 to exit the dialogue skipper...")
    print()

    keyboard.add_hotkey('F8', toggle_start)
    keyboard.add_hotkey('F9', toggle_pause)
    keyboard.add_hotkey('F12', toggle_exit)

    while program_running:
        while game_running:
            click_pos = randomize_cursor_position(target_pos, 250)
            sleep_time = randomize_sleep_time(0.25, 0.2)

            pydirectinput.leftClick(click_pos[0], click_pos[1], duration=randomize_sleep_time(0.1, 0.04))
            pydirectinput.keyDown('f')

            time.sleep(sleep_time*0.2)
            pydirectinput.keyUp('f')
            time.sleep(sleep_time*0.3)
        else:
            time.sleep(0.1)



def main():
    global program_running
    global game_running

    program_running = True
    game_running = False

    resolution = calculate_resolution()
    game(resolution)


if __name__ == "__main__":
    main()