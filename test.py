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
    entities = minescript.entities(max_distance=20)
    for e in entities:
        if e.name == "Bat":
            smooth_look.smooth_look_at_entity([e.position[0], e.position[1] + 1,e.position[2]])