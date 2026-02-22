from system.lib import minescript
import time, sys

if len(sys.argv) <= 2:
    raise ValueError("No command provided")

yaw = float(sys.argv[1])
pitch = float(sys.argv[2])

minescript.player_set_orientation(yaw, pitch)