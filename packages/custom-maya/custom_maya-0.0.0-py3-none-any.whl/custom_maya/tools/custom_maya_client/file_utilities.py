'''
打开并且处理场景的模块
'''
import json
import os
import tempfile
from dataclasses import dataclass

from custom_maya.custom_maya_class.scene_property import CMFileOptions
from custom_maya.custom_maya_class.scenefile_application import CMApplication
from custom_maya.tools.custom_maya_client.scene_utilities import SceneInformation


@dataclass
class FileOpenStatus:
    opened_successfully: bool
    opened_file_path: str
    detail: str = 'Opened successfully'


@dataclass
class FileCloseStatus:
    saved_successfully: bool
    saved_file_path: str
    detail: str = ''


class SceneFileInformation:
    def __init__(self, open_file_option: CMFileOptions):
        self.app = CMApplication()
        self.open_file_option = open_file_option
        self.opened_file_status = self.open_scene_file()

    def open_scene_file(self) -> FileOpenStatus:
        open_file_options = self.open_file_option.get_open_file_options()
        file_path = open_file_options[0][0]
        try:
            self.app.open_file(fo)

        except RuntimeError as e:
            if str(e).startswith('File not found:'):
                return FileOpenStatus(False, file_path, detail=str(e))

        except Exception as e:
            return FileOpenStatus(False, file_path, detail=str(e))

        return FileOpenStatus(True, file_path, )

    def get_data(self):
        if self.opened_file_status.opened_successfully:
            scene_information = SceneInformation().get_data()
        else:
            scene_information = {}

        return {
            'scene_file_information': self.opened_file_status.__dict__,
            'scene_information': scene_information
        }


if __name__ == '__main__':
    save_json_path = os.path.join(tempfile.gettempdir(), 'test_save_data.json')
    print(save_json_path)
    fo = CMFileOptions()
    file_path = r'D:\svn_project_test\my_data_svn\RootFolder\maya_proj\_test_file.mb'
    fo.set_open_file_options(file_path, o=True, force=True)

    zz = SceneFileInformation(fo)
    with open(save_json_path, 'w') as f:
        json.dump(zz.get_data(), f, indent=4)

    os.startfile(save_json_path)
