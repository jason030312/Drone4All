# import numpy as np
#
#
# def calculate_destination(theta=0, phi=0):
#     return np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), np.cos(theta)
#
#
# def get_command(vec, is_arrived=False):
#     x, y, z = vec
#     commands = []
#     if is_arrived:
#         commands.append('backspace')
#     else:
#         if x > 0:
#             if y > 0:
#                 if z
#             commands.append('w')
#         elif x < 0:
#             commands.append('s')
#         if y > 0:
#             commands.append('d')
#         elif y < 0:
#             commands.append('a')
#         if z > 0:
#             commands.append('space')
#         elif z < 0:
#             commands.append('left shift')
#     return commands


def back_left_down(drone, speed):
    getattr(drone, 'backward')(speed)
    getattr(drone, 'left')(speed)
    drone.down(speed*2)


def back_left(drone, speed):
    getattr(drone, 'backward')(speed)
    getattr(drone, 'left')(speed)


def back_left_up(drone, speed):
    getattr(drone, 'backward')(speed)
    getattr(drone, 'left')(speed)
    drone.up(speed*2)


def back_down(drone, speed):
    getattr(drone, 'backward')(speed)
    drone.down(speed*2)


def back(drone, speed):
    getattr(drone, 'backward')(speed)


def back_up(drone, speed):
    getattr(drone, 'backward')(speed)
    drone.up(speed*2)


def back_right_down(drone, speed):
    getattr(drone, 'backward')(speed)
    getattr(drone, 'right')(speed)
    drone.down(speed*2)


def back_right(drone, speed):
    getattr(drone, 'backward')(speed)
    getattr(drone, 'right')(speed)


def back_right_up(drone, speed):
    getattr(drone, 'backward')(speed)
    getattr(drone, 'right')(speed)
    drone.up(speed*2)


def left_down(drone, speed):
    getattr(drone, 'left')(speed)
    drone.down(speed*2)


def left(drone, speed):
    getattr(drone, 'left')(speed)


def left_up(drone, speed):
    getattr(drone, 'left')(speed)
    drone.up(speed*2)


def down(drone, speed):
    drone.down(speed*2)


def stop(drone, speed):
    getattr(drone, 'backward')(0)
    getattr(drone, 'left')(0)
    drone.up(0)


def up(drone, speed):
    drone.up(speed*2)


def right_down(drone, speed):
    getattr(drone, 'right')(speed)
    drone.down(speed*2)


def right(drone, speed):
    getattr(drone, 'right')(speed)


def right_up(drone, speed):
    getattr(drone, 'right')(speed)
    drone.up(speed*2)


def fw_left_down(drone, speed):
    getattr(drone, 'forward')(speed)
    getattr(drone, 'left')(speed)
    drone.down(speed*2)


def fw_left(drone, speed):
    getattr(drone, 'forward')(speed)
    getattr(drone, 'left')(speed)


def fw_left_up(drone, speed):
    getattr(drone, 'fowward')(speed)
    getattr(drone, 'left')(speed)
    drone.up(speed*2)


def fw_down(drone, speed):
    getattr(drone, 'forward')(speed)
    drone.down(speed*2)


def fw(drone, speed):
    getattr(drone, 'forward')(speed)


def fw_up(drone, speed):
    getattr(drone, 'forward')(speed)
    drone.up(speed*2)


def fw_right_down(drone, speed):
    getattr(drone, 'forward')(speed)
    getattr(drone, 'right')(speed)
    drone.down(speed*2)


def fw_right(drone, speed):
    getattr(drone, 'forward')(speed)
    getattr(drone, 'right')(speed)


def fw_right_up(drone, speed):
    getattr(drone, 'forward')(speed)
    getattr(drone, 'right')(speed)
    drone.up(speed*2)


command_list = [[[back_left_down,  back_left,  back_left_up],
                 [back_down,       back,       back_up],
                 [back_right_down, back_right, back_right_up]],
                [[left_down,       left,       left_up],
                 [down,            stop,       up],
                 [right_down,      right,      right_up]],
                [[fw_left_down,    fw_left,    fw_left_up],
                 [fw_down,         fw,         fw_up],
                 [fw_right_down,   fw_right,   fw_right_up]]]
