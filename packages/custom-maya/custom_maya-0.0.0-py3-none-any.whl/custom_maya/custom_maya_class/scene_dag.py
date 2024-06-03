import maya.OpenMaya as om
import maya.cmds as cmds
from .scene_base_wrapper import CMDagNodeWrapper
from .scene_property import CMDetailPropertyManager, CMDetailProperty, CustomDataType


class CMDagNode(CMDagNodeWrapper):
    def __init__(self, name):
        super().__init__(name)

        self.__dag_node = self.get_dag_node_object()

        self.property_manager = CMDetailPropertyManager()
        self.property_manager.add_members([
            CMDetailProperty(display_name='name', value=self.get_name(), data_type=CustomDataType.st),
            CMDetailProperty(display_name='long_name', value=self.get_long_name(), data_type=CustomDataType.st),

        ])

    def get_dag_node_object(self):
        """
        获取OpenMaya.MObject对象
        """
        selection_list = om.MSelectionList()
        selection_list.add(self.get_name())
        node_mobject = om.MObject()
        selection_list.getDependNode(0, node_mobject)

        return om.MFnDagNode(node_mobject)

    def get_bounding_box(self):
        bounding_box = self.__dag_node.boundingBox()
        return [
            [bounding_box.min().x, bounding_box.min().y, bounding_box.min().z],
            [bounding_box.max().x, bounding_box.max().y, bounding_box.max().z]
        ]


class CMDagNodeManager:
    def __init__(self):
        pass

    @classmethod
    def get_custom_nodes(cls):
        return [CMDagNode(i) for i in cmds.ls(dag=True)]
