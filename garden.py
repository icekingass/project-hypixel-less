import minescript, system, time, sys

isHoldingAttack = False

folderPath = "/home/icekingas/Documents/gardenScripts"

configName = sys.argv[1] if len(sys.argv) > 1 else 0
configName = str(configName)

temp = list(configName)
temp[0] = temp[0].upper()
configName = "".join(temp)

scriptPath = folderPath + "/" + configName + ".txt"

minescript.echo(f"Reading File\n{scriptPath}\n")

configFile = open(scriptPath, 'r')
lines = configFile.readlines()

instructions = {}
for line in lines:
    line = line.split(' ')
    if len(line) != 2:
        raise ValueError(f"Expected line to have 2 arguments, but found {len(line)}")
    instructions[line[0]] = line[1]
    # minescript.echo(f"At {line[0]} I do {line[1]}")

if(len(instructions) > 0):
    minescript.echo(f"Succsesfully Loaded {len(instructions)} Positions")
else:
    raise ValueError(f"Found 0 Positions")

running = True

while True:
    pos = minescript.player_position()
    posParsed = f"{int(round(pos[0]))},{int(round(pos[1]))},{int(round(pos[2]))}"
    #minescript.echo(posParsed)
    if posParsed in instructions:
        command = instructions[posParsed]
        for char in command:
            if char == 'W':
                minescript.player_press_forward(True)
            elif char == 'w':
                minescript.player_press_forward(False)
            elif char == 'A':
                minescript.player_press_left(True)
            elif char == 'a':
                minescript.player_press_left(False)
            elif char == 'S':
                minescript.player_press_backward(True)
            elif char == 's':
                minescript.player_press_backward(False)
            elif char == 'D':
                minescript.player_press_right(True)
            elif char == 'd':
                minescript.player_press_right(False)
            elif char == '&':
                minescript.player_press_right(False)
                minescript.player_press_backward(False)
                minescript.player_press_left(False)
                minescript.player_press_forward(False)
                minescript.player_press_attack(False)
                minescript.execute("/warp garden")
                time.sleep(0.5)
                isHoldingAttack = False
    if posParsed in instructions:
        if '&' not in instructions[posParsed] and not isHoldingAttack:
            isHoldingAttack = True
            minescript.player_press_attack(True)
