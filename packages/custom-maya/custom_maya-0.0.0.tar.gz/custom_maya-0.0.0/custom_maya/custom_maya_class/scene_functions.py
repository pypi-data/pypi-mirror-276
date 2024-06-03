import maya.cmds as cmds


def is_standalone():
    return not hasattr(cmds, 'about') or cmds.about(batch=True)


def convert_unit_to_fps(fps):
    '''将单位转换为帧率'''

    if fps == 'game':
        return 15
    elif fps == 'film':
        return 24
    elif fps == 'pal':
        return 25
    elif fps == 'ntsc':
        return 30
    elif fps == 'show':
        return 48
    elif fps == 'palf':
        return 50
    elif fps == 'ntscf':
        return 60
    else:
        return fps


def convert_bytes(size):
    """ Convert bytes to KB, or MB or GB"""
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0
    return size