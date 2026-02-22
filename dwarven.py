import minescript, math, smooth_look, time, threading

flag = True
PLAYER_REACH = 4.5
HOLDING = False

def compute_angles(pos_1 : list[float], pos_2 : list[float], crr_orientation : list[float]) -> list[float]:
    current_yaw, current_pitch = crr_orientation

    dx = pos_2[0] - pos_1[0]
    dy = pos_2[1] - pos_1[1]
    dz = pos_2[2] - pos_1[2]
    
    horizontal_dist = math.sqrt(dx*dx + dz*dz)

    target_yaw = -math.degrees(math.atan2(dx, dz))
    target_pitch = -math.degrees(math.atan2(dy, horizontal_dist))
    
    delta_yaw = target_yaw - current_yaw
    delta_pitch = target_pitch - current_pitch

    while delta_yaw > 180:
        delta_yaw -= 360
    while delta_yaw < -180:
        delta_yaw += 360
    
    return [delta_yaw, delta_pitch]

def get_exposed_faces(block_center, block_map):
    x = int(block_center[0])
    y = int(block_center[1])
    z = int(block_center[2])

    directions = {
        "east":  ([x+1, y, z],  (0.5, 0, 0)),
        "west":  ([x-1, y, z],  (-0.5, 0, 0)),
        "top":   ([x, y+1, z],  (0, 0.5, 0)),
        "bottom":([x, y-1, z],  (0, -0.5, 0)),
        "south": ([x, y, z+1],  (0, 0, 0.5)),
        "north": ([x, y, z-1],  (0, 0, -0.5)),
    }

    exposed_faces = []

    for (name, (neighbor_pos, offset)) in directions.items():
        block = block_map.get(tuple(neighbor_pos), "air")
        if block.__contains__("air") or block.__contains__("carpet"):
            exposed_faces.append(offset)

    return exposed_faces

def listen_for_flags():
    with minescript.EventQueue() as event_queue:
        event_queue.register_key_listener()
        #event_queue.register_chat_listener()
        while True:
            event = event_queue.get()
            if event.type == minescript.EventType.KEY and event.key == 269:#'END'
                global flag
                if event.action == 0:
                    pass
                elif event.action == 1:
                    flag = False
                    minescript.player_press_attack(False)
                else:
                    flag = False
                    minescript.player_press_attack(False)
                minescript.echo(f"Ended")
                minescript.execute("/shmouselock")
                return
            '''
            if event.type == minescript.EventType.CHAT:
                if event.message.__contains__("A Golden Goblin has spawned!") or event.message.__contains__("A Diamond Goblin has spawned!"):
                    minescript.echo("Goblin spawn detected")
                    minescript.player_press_attack(False)
                    time.sleep(0.5)
                    minescript.player_press_attack(True)
            '''

def check_for_entities():
    while flag:
        if minescript.player_get_targeted_entity(PLAYER_REACH) is not None:
            if HOLDING:
                minescript.player_press_attack(False)
                minescript.echo("Entity detected")

def get_distance(pos_1 : list[float], pos_2 : list[float]) -> float:
    return math.sqrt((pos_1[0] - pos_2[0])**2 + (pos_1[1] - pos_2[1])**2 + (pos_1[2] - pos_2[2])**2)

t1 = threading.Thread(target=listen_for_flags)
t1.start()

t2 = threading.Thread(target=check_for_entities)
t2.start()

minescript.execute("/shmouselock")

blacklist = []
player_pos = minescript.player_position()
player_pos[1] += 1.12 #eye height
while flag:
    orientation = minescript.player_orientation()
    block_pos_1 = [round(player_pos[0] - PLAYER_REACH), round(player_pos[1] - PLAYER_REACH), round(player_pos[2] - PLAYER_REACH)]
    block_pos_2 = [round(player_pos[0] + PLAYER_REACH), round(player_pos[1] + PLAYER_REACH), round(player_pos[2] + PLAYER_REACH)]

    positions = []

    for x in range(block_pos_1[0], block_pos_2[0]):
        for y in range(block_pos_1[1], block_pos_2[1]):
            for z in range(block_pos_1[2], block_pos_2[2]):
                positions.append([x, y, z])

    blocks = minescript.get_block_list(positions)

    block_map = {}

    for i in range(len(positions)):
        pos = tuple(positions[i])
        block = blocks[i]
        block_map[pos] = block

    targeted_block : minescript.TargetedBlock | None = minescript.player_get_targeted_block()

    if targeted_block is not None:
        targeted_block_pos = targeted_block[0]
    else:
        targeted_block_pos = player_pos
        minescript.echo("Using player pos")
        
    if isinstance(targeted_block_pos, list):
        min_distance = 999
        final_position = []
        final_block_position = []
        for i in range(len(positions)):
            if positions[i] in blacklist:
                continue
            if blocks[i].__contains__("diorite") or blocks[i].__contains__("prismarine") or blocks[i].__contains__("gray_wool") or blocks[i].__contains__("light_blue_wool") or blocks[i].__contains__("cyan_terracotta"):
                crr_distance = get_distance(targeted_block_pos, positions[i])
                if crr_distance < min_distance and get_distance(player_pos, positions[i]) <= PLAYER_REACH:

                    faces = get_exposed_faces(positions[i], block_map)

                    if not faces:
                        continue  # fully enclosed

                    best_face = None
                    smallest_distance_face = 999
                    for offset in faces:
                        face_point = [
                            positions[i][0] + offset[0],
                            positions[i][1] + offset[1],
                            positions[i][2] + offset[2],
                        ]
                        face_pos = get_distance(player_pos, face_point)
                        if face_pos < smallest_distance_face:
                            smallest_distance_face = face_pos
                            best_face = face_point
                            final_block_position = [positions[i][0], positions[i][1], positions[i][2]]

                    min_distance = crr_distance
                    final_position = best_face
        if min_distance < 10 and final_position:
            smooth_look.smooth_look_at_pos(final_position)
            minescript.player_press_attack(True)
            HOLDING = True
            temp = minescript.player_get_targeted_block(PLAYER_REACH)
            while temp is not None and (str(temp[3]).__contains__("diorite") or str(temp[3]).__contains__("prismarine") or str(temp[3]).__contains__("gray_wool") or str(temp[3]).__contains__("light_blue_wool") or str(temp[3]).__contains__("cyan_terracotta")) and HOLDING:
                temp = minescript.player_get_targeted_block(PLAYER_REACH)
                time.sleep(0.01)
            temp = minescript.get_block(final_block_position[0], final_block_position[1], final_block_position[2])
            if temp is not None:
                if not temp.__contains__("bedrock"):
                    blacklist.append(final_block_position)
            minescript.player_press_attack(False)
            HOLDING = False