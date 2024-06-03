import maya.cmds as cmds

from .scene_base import CMDagNodeBase


class CMDagNodeWrapper(CMDagNodeBase):
    def __init__(self, name):
        super().__init__()

        self.__name = name

    def get_name(self):
        return self.__name

    def get_long_name(self):
        return cmds.ls(self.__name, long=True)[0]
