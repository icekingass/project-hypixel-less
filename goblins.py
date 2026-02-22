import minescript, smooth_look, time, threading, math

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
                    minescript.player_press_jump(False)
                else:
                    flag = False
                    minescript.player_press_attack(False)
                    minescript.player_press_forward(False)
                    minescript.player_press_jump(False)

                minescript.echo(f"Ended")
                return
            
t1 = threading.Thread(target=listen_for_flags)
t1.start()

def get_distance(pos_1 : list[float], pos_2 : list[float]) -> float:
    return math.sqrt((pos_1[0] - pos_2[0])**2 + (pos_1[1] - pos_2[1])**2 + (pos_1[2] - pos_2[2])**2)

minescript.player_press_jump(True)

while flag:
    entity : minescript.EntityData | None = None
    min_distance = 999
    player_pos = minescript.player_position()
    entities = minescript.entities(max_distance=20)
    for e in entities:
        if e.name.__contains__("❤") and not e.name.__contains__(" 0/") and e.position[1] - 5 < player_pos[1]:
            dist = get_distance(player_pos, list(e.position))
            if dist < min_distance:
                entity = e
                min_distance = dist
    if entity is not None:
        smooth_look.smooth_look_at_entity([entity.position[0],entity.position[1] - 0.5,entity.position[2]])
        targeted_entity = minescript.player_get_targeted_entity()
        minescript.player_press_use(True)
        time.sleep(0.03)
        minescript.player_press_use(False)
        time.sleep(0.5)