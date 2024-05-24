from zipfile import ZipFile
from mcdreforged.api.types import PluginServerInterface
import datetime
import os

def upload_to_baidu():
    pass

def zip_server(server_name, server:PluginServerInterface) -> str:
    """
    将server文件夹压缩.
    并返回所在的临时目录字符串.
    :return: 临时目录字符串
    """
    # 获取当前时间字符串
    now = datetime.datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    # 获取服务端路径和mcdr插件路径和mcdr插件配置路径和mcdr配置路径

    # 基本路径
    running_path = os.getcwd()
    mcdr_config = server.get_mcdr_config()
    # 可以确定的路径
    server = os.path.join(running_path, mcdr_config['working_directory'])
    mcdr_plugin_config = os.path.join(running_path, "config")
    # TODO 少一个mcdr配置文件没压缩

    # 获取所有支持的插件路径
    all_mcdr_plugin_path = mcdr_config['plugin_directories']
    # 获取真正的插件路径列表
    mcdr_plugin_path = list()
    for plugin_path in all_mcdr_plugin_path:
        mcdr_plugin_path.append(os.path.join(
            running_path,
            plugin_path
        ))

    with ZipFile(f"{server_name}_backup_{datetime}", "w") as zipfile:
        zip_dir(server, zipfile)
        zip_dir(mcdr_plugin_config, zipfile)
        for path in mcdr_plugin_path:
            zip_dir(path, zipfile)


def zip_dir(path:str, zipfile:ZipFile):
    for root, dirs, files in os.walk(path):
        relative_root = '' if root == path else root.replace(path, '') + os.sep  # 计算文件相对路径
        for filename in files:
            zipfile.write(os.path.join(root, filename), relative_root + filename)  # 文件路径 压缩文件路径（相对路径）
