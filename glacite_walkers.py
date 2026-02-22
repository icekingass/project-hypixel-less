import minescript, math, smooth_look, time, threading, random

PLAYER_ATTACK_REACH = 3

flag = True

def listen_for_flags():
    with minescript.EventQueue() as event_queue:
        event_queue.register_key_listener()
        while True:
            event = event_queue.get()
            if event.type == minescript.EventType.KEY and event.key == 269:#'END'
                global flag
                if event.action == 0:
                    pass
                elif event.action == 1:
                    flag = False
                    minescript.player_press_attack(False)
                    minescript.player_press_forward(False)
                    minescript.player_press_sprint(False)
                else:
                    flag = False
                    minescript.player_press_attack(False)
                    minescript.player_press_forward(False)
                    minescript.player_press_sprint(False)

                minescript.echo(f"Ended")
                return

def get_distance(pos_1 : list[float], pos_2 : list[float]) -> float:
    return math.sqrt((pos_1[0] - pos_2[0])**2 + (pos_1[1] - pos_2[1])**2 + (pos_1[2] - pos_2[2])**2)

def trigger_bot():
    global flag
    while flag:
        time.sleep(0.01)
        targeted_entity = minescript.player_get_targeted_entity(PLAYER_ATTACK_REACH + 2)
        if targeted_entity is not None and targeted_entity.name.__contains__("Ice Walker"):
            minescript.player_press_attack(True)
            time.sleep(0.03)
            minescript.player_press_attack(False)
            time.sleep(0.03)

t1 = threading.Thread(target=listen_for_flags)
t1.start()

t2 = threading.Thread(target=trigger_bot)
t2.start()

holding = False
found = False
close = False
crouching = False
minescript.player_press_sprint(True)
while flag:
    found = False
    close = False
    entities = minescript.entities(max_distance=35)
    min_distance : float = 999
    target_entity : minescript.EntityData | None = None
    for e in entities:
        if e.name.__contains__("❤") and not e.name.__contains__("0/") and e.position[1] < 130:
            player_pos = minescript.player_position()
            distance = math.sqrt((e.position[0] - player_pos[0])**2 + (e.position[2] - player_pos[2])**2)
            if distance < min_distance + 2:
                min_distance = distance
                target_entity = e

    player_pos = minescript.player_position()
    if target_entity is not None:
        found = True
        smooth_look.smooth_look_at_entity([target_entity.position[0], target_entity.position[1] - 0.5, target_entity.position[2]])
        if get_distance(list(player_pos), list(target_entity.position)) < 4.5 + random.uniform(-0.25, 0.25):
            if not crouching:
                minescript.player_press_sneak(True)
                crouching = True
        else:
            if crouching:
                minescript.player_press_sneak(False)
                crouching = False
        if minescript.player_get_targeted_entity(PLAYER_ATTACK_REACH) is None:
            minescript.player_press_forward(True)
            holding = True
        else:
            close = True
    else:
        player_pos = minescript.player_position()
        if math.sqrt((player_pos[0] - 0)**2 + (player_pos[2] - 160)**2) > 3:
            smooth_look.smooth_look_at_pos([0, 129, 160])
            minescript.player_press_forward(True)
            holding = True
            found = True
            if crouching:
                minescript.player_press_sneak(False)
                crouching = False
        else:
            close = True

    if (not found or close) and holding:
        minescript.player_press_forward(False)
        holding = False
    