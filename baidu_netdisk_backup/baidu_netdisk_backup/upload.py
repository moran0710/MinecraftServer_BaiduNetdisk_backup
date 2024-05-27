import shutil
from zipfile import ZipFile

from mcdreforged.command.command_source import CommandSource
from mcdreforged.api.types import PluginServerInterface
from mcdreforged.command.builder.common import CommandContext
import datetime
import os

from mcdreforged.plugin.server_interface import ServerInterface

from .utils import get_config


def upload_to_baidu(source: CommandSource, context: CommandContext):
    pass


def make_server_zip(source: CommandSource, context: CommandContext):
    """
    将server文件夹压缩.
    并返回所在的临时目录字符串.
    :return: 临时目录字符串
    """
    # 获取服务器实例和参数
    server = PluginServerInterface.get_instance().as_plugin_server_interface()
    config = get_config(server)
    server_name = config['ServerName']

    # 获取当前时间字符串
    now = datetime.datetime.now()
    now_str = now.strftime("%Y_%m_%d_%H_%M_%S")
    # 获取服务端路径和mcdr插件路径和mcdr插件配置路径和mcdr配置路径

    # 基本路径
    running_path = os.getcwd()
    mcdr_config = server.get_mcdr_config()
    # 可以确定的路径
    server_path = os.path.join(running_path, mcdr_config['working_directory'])
    mcdr_plugin_config = os.path.join(running_path, "config")
    mcdr_config_file = os.path.join(running_path, "config.yml")

    # 获取所有支持的插件路径
    all_mcdr_plugin_path = mcdr_config['plugin_directories']
    mcdr_plugin_path = list()
    for plugin_path in all_mcdr_plugin_path:
        mcdr_plugin_path.append(os.path.join(running_path, plugin_path))
    server.logger.info(mcdr_plugin_path)

    # 获取真正的插件路径列表

    # 确定压缩后文件位置
    backup_zipfile = os.path.join(running_path, f"{server_name}_backup_{now_str}.zip")

    server.execute("save-off")
    server.execute("save-all")
    # 开始压缩
    try:
        zip_server(backup_zipfile, mcdr_config_file, mcdr_plugin_config, mcdr_plugin_path, server_path)
    except PermissionError as e:
        pass
    server.logger.info("done")
    server.execute("save-on")
    return backup_zipfile


def zip_server(backup_zipfile, mcdr_config_file, mcdr_plugin_config, mcdr_plugin_path, server):
    with ZipFile(backup_zipfile, "w") as zipfile:
        zipfile.write(mcdr_config_file, os.path.join("mcdr", "mcdr_config.yml"))  # mcdr配置文件
        zip_dir(mcdr_plugin_config, zipfile, os.path.join("mcdr", "plugin_config"))  # mcdr插件配置
        for plugin_path in mcdr_plugin_path:
            zip_dir(plugin_path, zipfile, os.path.join("mcdr", "plugins"))
        zip_dir(server, zipfile, "minecraft_server")  # 服务器本体


def zip_dir(path: str, zipfile: ZipFile, temp: str):
    for root, dirs, files in os.walk(path):
        relative_root = temp if root == path else temp + root.replace(path, '') + os.sep  # 计算文件相对路径
        for filename in files:
            zipfile.write(os.path.join(root, filename), os.path.join(relative_root, filename))  # 文件路径 压缩文件路径（相对路径）
