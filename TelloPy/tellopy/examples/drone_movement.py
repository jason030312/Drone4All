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
    getattr(drone, 'backward')(speed * 1.207)
    getattr(drone, 'left')(speed * 1.102)
    drone.down(speed*2)


def back_left(drone, speed):
    getattr(drone, 'backward')(speed / 1.414 * 1.207)
    getattr(drone, 'left')(speed / 1.414 * 1.102)


def back_left_up(drone, speed):
    getattr(drone, 'backward')(speed / 1.414 *1.207)
    getattr(drone, 'left')(speed / 1.414 *1.102)
    drone.up(speed*2)


def back_down(drone, speed):
    getattr(drone, 'backward')(speed*1.207)
    drone.down(speed*2)


def back(drone, speed):
    getattr(drone, 'backward')(speed*1.207)


def back_up(drone, speed):
    getattr(drone, 'backward')(speed*1.207)
    drone.up(speed*2)


def back_right_down(drone, speed):
    getattr(drone, 'backward')(speed / 1.414 *1.207)
    getattr(drone, 'right')(speed / 1.414 *1.102)
    drone.down(speed*2)


def back_right(drone, speed):
    getattr(drone, 'backward')(speed / 1.414 *1.207)
    getattr(drone, 'right')(speed / 1.414 *1.102)


def back_right_up(drone, speed):
    getattr(drone, 'backward')(speed / 1.414 *1.207)
    getattr(drone, 'right')(speed / 1.414 *1.102)
    drone.up(speed*2)


def left_down(drone, speed):
    getattr(drone, 'left')(speed)
    drone.down(speed*2)


def left(drone, speed):
    getattr(drone, 'left')(speed*1.102)


def left_up(drone, speed):
    getattr(drone, 'left')(speed*1.102)
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
    getattr(drone, 'right')(speed*1.102)
    drone.down(speed*2)


def right(drone, speed):
    getattr(drone, 'right')(speed*1.102)


def right_up(drone, speed):
    getattr(drone, 'right')(speed*1.102)
    drone.up(speed*2)


def fw_left_down(drone, speed):
    getattr(drone, 'forward')(speed / 1.414 *1.207)
    getattr(drone, 'left')(speed / 1.414 *1.102)
    drone.down(speed*2)


def fw_left(drone, speed):
    getattr(drone, 'forward')(speed / 1.414 *1.207)
    getattr(drone, 'left')(speed / 1.414 *1.102)


def fw_left_up(drone, speed):
    getattr(drone, 'forward')(speed / 1.414 *1.207)
    getattr(drone, 'left')(speed / 1.414 *1.102)
    drone.up(speed*2)


def fw_down(drone, speed):
    getattr(drone, 'forward')(speed*1.207)
    drone.down(speed*2)


def fw(drone, speed):
    getattr(drone, 'forward')(speed*1.207)


def fw_up(drone, speed):
    getattr(drone, 'forward')(speed*1.207)
    drone.up(speed*2)


def fw_right_down(drone, speed):
    getattr(drone, 'forward')(speed / 1.414 *1.207)
    getattr(drone, 'right')(speed / 1.414 *1.102)
    drone.down(speed*2)


def fw_right(drone, speed):
    getattr(drone, 'forward')(speed / 1.414 *1.207)
    getattr(drone, 'right')(speed / 1.414 *1.102)


def fw_right_up(drone, speed):
    getattr(drone, 'forward')(speed / 1.414 *1.207)
    getattr(drone, 'right')(speed / 1.414 *1.102)
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
