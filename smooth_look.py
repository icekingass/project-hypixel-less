import minescript, math, random, time

def smooth_look_at(yaw : float, pitch : float):
    orientation = minescript.player_orientation()

    delta_yaw = yaw - orientation[0]
    delta_pitch = pitch - orientation[1]

    angle_mag = math.sqrt(delta_yaw**2 + delta_pitch**2)
    steps = int(max(15, min(40, angle_mag * 0.4)))

    for i in range(steps + 1):
        progress = i / steps
        ease = progress * progress * (3 - 2 * progress)

        yaw = orientation[0] + delta_yaw * ease
        pitch = orientation[1] + delta_pitch * ease

        minescript.player_set_orientation(yaw, pitch)
        time.sleep(0.005 + random.uniform(-0.001, 0.001))

def smooth_look_at_pos(block_pos: list):
    player_pos = minescript.player_position()
    player_pos[1] += 1.62
    block_pos[0] += 0.5
    block_pos[1] += 0.5
    block_pos[2] += 0.5
    current_yaw, current_pitch = minescript.player_orientation()
    start_yaw, start_pitch = minescript.player_orientation()

    dx = block_pos[0] - player_pos[0]
    dy = block_pos[1] - player_pos[1]
    dz = block_pos[2] - player_pos[2]
    
    horizontal_dist = math.sqrt(dx*dx + dz*dz)

    target_yaw = -math.degrees(math.atan2(dx, dz))
    target_pitch = -math.degrees(math.atan2(dy, horizontal_dist))

    max_offset = 2.5

    yaw_offset = random.gauss(0, max_offset / 2)
    pitch_offset = random.gauss(0, max_offset / 3)

    target_yaw += yaw_offset
    target_pitch += pitch_offset

    delta_yaw = target_yaw - current_yaw
    delta_pitch = target_pitch - current_pitch

    while delta_yaw > 180:
        delta_yaw -= 360
    while delta_yaw < -180:
        delta_yaw += 360

    angle_mag = math.sqrt(delta_yaw**2 + delta_pitch**2)
    steps = int(max(15, min(40, angle_mag * 0.4)))

    for i in range(steps + 1):
        progress = i / steps
        ease = progress * progress * (3 - 2 * progress)

        yaw = start_yaw + delta_yaw * ease
        pitch = start_pitch + delta_pitch * ease

        yaw += random.uniform(-0.15, 0.15)
        pitch += random.uniform(-0.1, 0.1)

        minescript.player_set_orientation(yaw, pitch)
        time.sleep(0.005 + random.uniform(-0.001, 0.001))

def smooth_look_at_entity(entity_pos : list[float]):
    player_pos = minescript.player_position()
    player_pos[1] += 1.62  # eye height
    
    MIN_THRESHOLD = 5

    target_pos = entity_pos

    dx = target_pos[0] - player_pos[0]
    dy = target_pos[1] - player_pos[1]
    dz = target_pos[2] - player_pos[2]

    horizontal_dist = math.sqrt(dx*dx + dz*dz)

    target_yaw = -math.degrees(math.atan2(dx, dz))
    target_pitch = -math.degrees(math.atan2(dy, horizontal_dist))

    start_yaw, start_pitch = minescript.player_orientation()

    delta_yaw = target_yaw - start_yaw
    delta_pitch = target_pitch - start_pitch

    # Normalize yaw
    while delta_yaw > 180:
        delta_yaw -= 360
    while delta_yaw < -180:
        delta_yaw += 360

    if(abs((delta_pitch + delta_yaw) / 2) <= MIN_THRESHOLD):
        minescript.player_set_orientation(target_yaw, target_pitch)
        return

    angle_mag = math.sqrt(delta_yaw**2 + delta_pitch**2)
    steps = int(max(5, min(15, angle_mag * 0.5)))

    for i in range(steps + 1):
        progress = i / steps
        ease = progress * progress * (3 - 2 * progress)

        yaw = start_yaw + delta_yaw * ease
        pitch = start_pitch + delta_pitch * ease

        yaw += random.uniform(-0.15, 0.15)
        pitch += random.uniform(-0.1, 0.1)

        minescript.player_set_orientation(yaw, pitch)
        time.sleep(0.001 + random.uniform(-0.001, 0.001))