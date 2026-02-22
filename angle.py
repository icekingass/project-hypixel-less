import minescript
import sys, smooth_look

if len(sys.argv) <= 2:
    raise ValueError("No command provided")

yaw = float(sys.argv[1])
pitch = float(sys.argv[2])

smooth_look.smooth_look_at(yaw, pitch)