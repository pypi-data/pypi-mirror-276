import maya.cmds as cmds

from .scene_base import CMObject, CMNode
from .scene_property import CMDetailPropertyManager, CMDetailProperty, CustomDataType


class CMBlendShape(CMNode):

    def __init__(self, short_name):
        super().__init__()
        self.short_name = short_name
        self.envelope = cmds.getAttr(f'{self.short_name}.envelope')
        self.morph_targets = [
            CMMorphTarget(i, self.short_name).property_manager.get_members_dict() for idx, i in
            enumerate(cmds.aliasAttr(self.short_name, q=True), start=1) if idx % 2
        ]
        self.property_manager = CMDetailPropertyManager()
        self.property_manager.add_members([
            CMDetailProperty(display_name='blend_shape_name', value=self.short_name, data_type=CustomDataType.st),
            CMDetailProperty(display_name='morph_targets_list', value=self.morph_targets, data_type=CustomDataType.li)
        ]
        )


class CMMorphTarget(CMNode):
    def __init__(self, morph_target_name, blend_shape_name):
        super().__init__()
        self.morph_target_name = morph_target_name
        self.blend_shape_name = blend_shape_name
        self.property_manager = CMDetailPropertyManager()
        self.property_manager.add_members([
            CMDetailProperty(display_name='name', value=self.morph_target_name, data_type=CustomDataType.st),
            # CMDetailProperty(display_name='blend_shape_name', value=self.blend_shape_name, data_type=CustomDataType.st)
        ]
        )


class CMBlendShapeManager():
    def __init__(self) -> None:
        pass

    def get_custom_blendshapes(self) -> list[CMBlendShape]:
        return [CMBlendShape(i) for i in cmds.ls(type='blendShape')]
