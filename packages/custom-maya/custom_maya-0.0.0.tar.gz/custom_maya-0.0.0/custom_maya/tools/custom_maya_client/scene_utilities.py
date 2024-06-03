'''
各种关于场景信息的数据
'''
import os
import tempfile
import json

import maya.api.OpenMaya as om

from maya import cmds

from custom_maya.custom_maya_class.custom_blendshapes import CMBlendShapeManager
from custom_maya.custom_maya_class.custom_transform import CMTransformManager
from custom_maya.custom_maya_class.scene_dag import CMDagNodeManager, CMDagNode
from custom_maya.custom_maya_class.scene_property import CustomDataType, CMDetailProperty
from custom_maya.custom_maya_class.scenefile_application import CMSceneCounter, CMSceneEvaluate


class _CMDagNode(CMDagNode):
    def __init__(self, name):
        super().__init__(name)
        self.property_manager.add_members([
            # CMDetailProperty(display_name='BoundingBox', value=self.get_bounding_box(), data_type=CustomDataType.li),
            CMDetailProperty(display_name='typ', value=cmds.nodeType(self.get_long_name()),
                             data_type=CustomDataType.st),
            CMDetailProperty(display_name='is_shape',
                             value=self.is_shape(), data_type=CustomDataType.bo)
        ])

    def is_shape(self):
        # 用你想检查的物体的名字替换 'your_object_name'
        object_name = self.get_name()

        # 获取MSelectionList对象
        selection_list = om.MSelectionList()
        selection_list.add(object_name)

        # 尝试获取MObject
        try:
            mobject = selection_list.getDependNode(0)
            # 使用MFn的hasObj方法检查是否是shape
            is_shape = mobject.hasFn(om.MFn.kShape)
            return True
        except:
            return False


class _CMDagNodeManager(CMDagNodeManager):

    @classmethod
    def get_custom_nodes(cls):
        return [_CMDagNode(i) for i in cmds.ls(dag=True)]


class SceneInformation:
    def __init__(self):
        '''
        用于场景信息收集信息汇总的类
        '''
        self.scene_counter: CMSceneCounter = CMSceneCounter()
        self.scene_evaluate: CMSceneEvaluate = CMSceneEvaluate()
        self.transform_manager = CMTransformManager()
        self.dag_nodes_manager = _CMDagNodeManager()
        self.blendshapes_manager = CMBlendShapeManager()

    def get_data(self):
        '''
        获取场景内所有必要信息
        '''
        return {
            'scene_counter': self.scene_counter.get_scene_counter(),
            'scene_evaluate': self.scene_evaluate.get_settings_evaluate(),
            'nodes': [i.property_manager.get_members_dict() for i in self.dag_nodes_manager.get_custom_nodes()],
            'blend_shapes': [i.property_manager.get_members_dict() for i in
                             self.blendshapes_manager.get_custom_blendshapes()],

        }


if __name__ == '__main__':
    save_json_path = os.path.join(tempfile.gettempdir(), 'test_save_data.json')

    with open(save_json_path, 'w') as f:
        json.dump(SceneInformation().get_data(), f, indent=4)

    os.startfile(save_json_path)
