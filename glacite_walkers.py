import minescript, math, smooth_look, time, threading

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
                else:
                    flag = False
                    minescript.player_press_attack(False)
                    minescript.player_press_forward(False)
                minescript.echo(f"Ended")
                return

t1 = threading.Thread(target=listen_for_flags)
t1.start()
holding = False
found = False
close = False
        
while flag:
    found = False
    close = False
    targeted_entity = minescript.player_get_targeted_entity(PLAYER_ATTACK_REACH)
    if targeted_entity is not None and targeted_entity.name.__contains__("Ice Walker"):
        minescript.player_press_attack(True)
        time.sleep(0.03)
        minescript.player_press_attack(False)
        time.sleep(0.03)
        continue
    entities = minescript.entities(max_distance=30)
    min_distance : float = 999
    target_entity : minescript.EntityData | None = None
    for e in entities:
        if e.name.__contains__("❤") and not e.name.__contains__("0/") and e.position[1] < 130:
            player_pos = minescript.player_position()
            distance = math.sqrt((e.position[0] - player_pos[0])**2 + (e.position[2] - player_pos[2])**2)
            if distance < min_distance:
                min_distance = distance
                target_entity = e

    if target_entity is not None:
        found = True
        smooth_look.smooth_look_at_entity([target_entity.position[0], target_entity.position[1] - 0.5, target_entity.position[2]])
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
        else:
            close = True

    if (not found or close) and holding:
        minescript.player_press_forward(False)
        holding = False
    