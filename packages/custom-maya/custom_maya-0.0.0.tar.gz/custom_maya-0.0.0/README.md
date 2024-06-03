# 项目说明

此工具内含各种实用工具。**仅为测试用！！！**

仅支持Maya2023及以上版本。

参照

* [如何使用mayapy运行venv](https://knowledge.autodesk.com/zh-hans/support/maya/learn-explore/caas/CloudHelp/cloudhelp/2023/CHS/Maya-Scripting/files/GUID-6AF99E9C-1473-481E-A144-357577A53717-htm.html)
* [Maya Python 解释器 mayapy](https://knowledge.autodesk.com/zh-hans/support/maya/learn-explore/caas/CloudHelp/cloudhelp/2023/CHS/Maya-Scripting/files/GUID-D64ACA64-2566-42B3-BE0F-BCE843A1702F-htm.html)

## 安装并获取更新

使用 pip 安装

```shell
pip install custom-maya
```

需要使用 mayapy 环境安装。

测试用

```shell
Xcopy custom_maya "C:\Program Files\Autodesk\Maya2023\Python\Lib\site-packages\custom_maya" /E/H/C/I
```

## 如何设置IDE

### 制作从名为 python 的命令创建指向 mayapy 的软链接

```shell
cd "C:\Program Files\Autodesk\Maya2023\bin"
mklink python.exe mayapy.exe
```

### 将IDE的解释器设置为

```
"C:\Program Files\Autodesk\Maya2023\bin\python.exe"
```

## 例子

### 获取某根目录下所有Maya文件的信息

```python

```

## 打包上传到pipy

升级

```shell
#cd "C:\Program Files\Autodesk\Maya2023\bin"
mayapy.exe -m pip install --upgrade pip
mayapy.exe -m pip install --upgrade build
mayapy.exe -m pip install --upgrade pip
```

```shell
python -m build
```

上传测试包

```shell
python -m twine upload --repository testpypi dist/*
```

上传正式版本包

```shell
python -m twine upload dist/*
```

## 安装本地whl包

```shell
cd "C:\Program Files\Autodesk\Maya2023\bin"
mayapy.exe -m pip install D:\github\custom_maya\dist\custom_maya-0.0.23-py3-none-any.whl
```

## 测试本地代码

### 构建

```shell
python -m build
```

### 安装到本地

```shell
cd "C:\Program Files\Autodesk\Maya2023\bin"
mayapy.exe -m pip install D:\github\custom_maya\dist\custom_maya-0.0.23-py3-none-any.whl --force-reinstall

```