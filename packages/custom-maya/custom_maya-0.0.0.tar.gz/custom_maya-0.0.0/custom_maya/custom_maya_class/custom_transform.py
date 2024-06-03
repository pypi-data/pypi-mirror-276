import maya.cmds as cmds

from .scene_dag import CMDagNode
from .scene_property import CMDetailPropertyManager, CMDetailProperty, CustomDataType


class CMTransform(CMDagNode):
    def __init__(self, name):
        '''
        '''

        super().__init__(name)
        self.name = self.get_name()
        self.long_name = self.get_long_name()

        self.translation_x = cmds.getAttr(f"{self.name}.translateX")
        self.translation_y = cmds.getAttr(f"{self.name}.translateY")
        self.translation_z = cmds.getAttr(f"{self.name}.translateZ")
        self.rotation_x = cmds.getAttr(f"{self.name}.rotateX")
        self.rotation_y = cmds.getAttr(f"{self.name}.rotateY")
        self.rotation_z = cmds.getAttr(f"{self.name}.rotateZ")
        self.scale_x = cmds.getAttr(f"{self.name}.scaleX")
        self.scale_y = cmds.getAttr(f"{self.name}.scaleY")
        self.scale_z = cmds.getAttr(f"{self.long_name}.scaleZ")
        self.visibility = cmds.getAttr(f"{self.name}.visibility")
        self.node_type = cmds.nodeType(self.name)

        self.property_manager.add_members([
            CMDetailProperty(display_name='TranslationX', value=self.translation_x, data_type=CustomDataType.fl),
            CMDetailProperty(display_name='TranslationY', value=self.translation_y, data_type=CustomDataType.fl),
            CMDetailProperty(display_name='TranslationZ', value=self.translation_z, data_type=CustomDataType.fl),
            CMDetailProperty(display_name='RotationX', value=self.rotation_x, data_type=CustomDataType.fl),
            CMDetailProperty(display_name='RotationY', value=self.rotation_y, data_type=CustomDataType.fl),
            CMDetailProperty(display_name='RotationZ', value=self.rotation_z, data_type=CustomDataType.fl),
            CMDetailProperty(display_name='ScaleX', value=self.scale_x, data_type=CustomDataType.fl),
            CMDetailProperty(display_name='ScaleY', value=self.scale_y, data_type=CustomDataType.fl),
            CMDetailProperty(display_name='ScaleZ', value=self.scale_z, data_type=CustomDataType.fl),
            CMDetailProperty(display_name='Visibility', value=self.visibility, data_type=CustomDataType.bo),
            CMDetailProperty(display_name='NodeType', value=self.node_type, data_type=CustomDataType.st),

        ])


class CMTransformManager():
    def __init__(self):
        pass

    def get_custom_transforms(self) -> list[CMTransform]:
        return [CMTransform(i) for i in cmds.ls(type="transform")]

    def get_custom_transforms_by_node_type(self, node_type_list=[]) -> list[CMTransform]:
        result = []
        for nt in node_type_list:
            result.extend([CMTransform(i) for i in cmds.ls(type=nt)])
        return result

    def get_all_transforms(self):
        result = []
        for i in cmds.ls(transforms=True):
            result.append(CMTransform(i))
        return result
