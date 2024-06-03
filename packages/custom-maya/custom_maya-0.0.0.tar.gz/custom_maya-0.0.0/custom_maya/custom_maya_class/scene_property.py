import os

from maya import cmds

from .scene_base import CMProperty
from .scene_functions import is_standalone, convert_bytes

# from base_function import is_ascii

from custom_maya import is_ascii


class CustomDataType():
    fl = 'float'
    st = 'string'
    i = 'int'
    li = 'list'
    obj = 'obj'
    bo = 'bool'


class CMFileOptions(CMProperty):
    def __init__(self):
        super().__init__()
        '''
        https://help.autodesk.com/view/MAYAUL/2024/ENU/?guid=__CommandsPython_index_html
        '''

        # 打开文件时的参数
        self.__open_file_options = None

    def get_open_file_options(self):
        """获取打开文件时的参数"""
        return self.__open_file_options

    def set_open_file_options(self, *args, **kwargs):
        """设置打开文件时的参数"""
        self.__open_file_options = (args, kwargs)

    def set_save_file_options(self, *args, **kwargs):
        """设置保存文件时的参数"""
        self.__save_file_options = (args, kwargs)

    def get_save_file_options(self):
        """获取保存文件时的参数"""
        return self.__save_file_options


class CMStandaloneProperty(CMProperty):
    def __init__(self):
        super().__init__()

    @staticmethod
    def is_standalone():
        return is_standalone()


class CMFileProperty(CMProperty):
    def __init__(self, file_path):
        super().__init__()
        self.__file_path = file_path

    def get_file_evaluate(self):
        base_name, suffix = os.path.splitext(os.path.basename(self.__file_path))
        return {
            'FileName': base_name,
            'Suffix': suffix,
            'Size': convert_bytes(os.path.getsize(self.__file_path)),
            'IsPathAscii': is_ascii(self.__file_path),
            'FirstLetterIsNumber': True if base_name[0].isdigit() else False,
            'FullPath': self.__file_path,
        }


class CMVector(CMProperty):
    def __init__(self, v1, v2, v3):
        super().__init__()
        self.__v1 = v1
        self.__v2 = v2
        self.__v3 = v3
        self.__vector = [self.__v1, self.__v2, self.__v3]

    def get_vector(self, decimal=3):
        return [round(i, decimal) for i in self.__vector]

    def data(self, *args, **kwargs):
        return self.get_vector(args, kwargs)


class CMList(CMProperty):
    def __init__(self, l=[]):
        super().__init__()
        self.__list = l

    def to_string(self):
        return str(self.__list)


class CMString(CMProperty):
    def __init__(self):
        super().__init__()


class CMName(CMProperty):
    def __init__(self):
        super().__init__()

    @property
    def long_name(self):
        return self.__long_name

    @property
    def short_name(self):
        return self.__short_name


class CMDetailProperty(CMProperty):
    '''
    用于存储详细信息的类
    此属性的主要目的是为了将特定的描述信息存储在一个地方，以便在需要时进行访问。
    '''

    def __init__(self, display_name: str = None, value=None, data_type: CustomDataType = None, decimal_round: int = 5):
        super().__init__()
        # 设置数据类型
        self.data_type = data_type
        self.decimal_round = decimal_round

        # 设置显示名
        self.display_name = display_name
        # 设置值
        self.init_value(value)

        self.__detail = {}

    def init_value(self, value):
        if self.data_type == CustomDataType.fl:
            self.value = round(value, self.decimal_round)

        else:
            self.value = value

    def set_detail(self, **kwargs):
        self.__detail = kwargs

    def get_detail(self):
        return self.__detail


class CMDetailPropertyManager(CMProperty):
    '''
    CMDetailProperty的管理类
    '''

    def __init__(self):
        super().__init__()

        self.__member_list: list[CMDetailProperty] = []

    def add_member(self, member: CMDetailProperty):
        self.__member_list.append(member)

    def add_members(self, members: list[CMDetailProperty]):
        self.__member_list.extend(members)

    def get_member_list(self):
        return self.__member_list

    def get_members_dict(self):
        result = {}
        for i in self.__member_list:
            result[i.display_name] = i.value
        return result


class CMObjectsInScene(CMProperty):
    def __init__(self):
        super().__init__()
        # 获取场景中基于ls命令的属性
        self.__init_ls_property()
        self.__data = {}

    @property
    def property_list(self):
        return self.__ls_property_list

    @property
    def __ls_property_list(self):
        return ['joint', 'mesh', 'camera', 'light', 'nurbsCurve', 'nurbsSurface', 'cluster', 'blendShape', ]

    def __init_ls_property(self):
        """获取场景中的所有物体"""
        for i in self.property_list:
            setattr(self, i, (lambda i=i: cmds.ls(type=i, long=True)))

    def ls_dict(self):
        # 使用 lambda 表达式定义匿名函数
        get_nodes_by_type = lambda x: cmds.ls(type=x, long=True)
        # 将 lambda 函数应用到列表中的所有元素
        return {node_type: get_nodes_by_type(node_type) for node_type in self.__ls_property_list}

    def ls_dict_custom(self):
        # 使用 lambda 表达式定义匿名函数
        get_nodes_by_type = lambda x: cmds.ls(type=x, long=True)
        # 将 lambda 函数应用到列表中的所有元素
        return {node_type: get_nodes_by_type(node_type) for node_type in self.__ls_property_list}
