import minescript, time, sys

command = sys.argv[1] if len(sys.argv) > 1 else ""
if command == "":
    raise ValueError("No command provided")
time.sleep(0.01)
for char in command:
    if char == 'W':
        minescript.player_press_forward(True)
    elif char == 'A':
        minescript.player_press_left(True)
    elif char == 'S':
        minescript.player_press_backward(True)
    elif char == 'D':
        minescript.player_press_right(True)
minescript.player_press_attack(True)
