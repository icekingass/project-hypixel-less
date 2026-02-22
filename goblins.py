import minescript, smooth_look, time, threading

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

while flag:
    entities = minescript.entities(max_distance=10)
    for e in entities:
        if e.name.__contains__("❤") and not e.name.__contains__(" 0/"):
            smooth_look.smooth_look_at_entity([e.position[0],e.position[1] - 0.2,e.position[2]])
            time.sleep(0.1)
            minescript.player_press_attack(True)
            time.sleep(0.03)
            minescript.player_press_attack(False)
            time.sleep(0.03)
            break