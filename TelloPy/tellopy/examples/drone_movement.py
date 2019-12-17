import numpy as np


def calculate_destination(theta=0, phi=0):
    return np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), np.cos(theta)


def get_command(x, y, z, is_arrived=False):
    commands = []
    if is_arrived:
        commands.append('backspace')
    else:
        if x > 0:
            commands.append('w')
        elif x < 0:
            commands.append('s')
        if y > 0:
            commands.append('d')
        elif y < 0:
            commands.append('a')
        if z > 0:
            commands.append('space')
        elif z < 0:
            commands.append('left shift')
    return commands
