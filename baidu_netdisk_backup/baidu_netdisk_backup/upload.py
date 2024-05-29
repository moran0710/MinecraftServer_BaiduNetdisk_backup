from mcdreforged.command.command_source import CommandSource
from mcdreforged.command.builder.common import CommandContext
from multiprocessing import Process

from bypy import ByPy

from .utils import get_config, get_server
from .slot import rewrite_solt

import datetime
import os
from zipfile import ZipFile


def upload_to_baidu(_: CommandSource, __: CommandContext):
    """实际的上传函数"""
    server = get_server()
    zipfile_path, zipfile_name = make_server_zip()
    is_filled, removed = rewrite_solt(zipfile_name)
    if is_filled:
        server.logger.info(f"移除了{removed}")
    server.logger.info(f"上传了{zipfile_name}")

    upload_process = Process(target=upload_to_baidu_process, args=(zipfile_path, zipfile_name, removed, is_filled,))
    upload_process.start()


def upload_to_baidu_process(zipfile_path, zipfile_name, need_removed, can_remove):
    netdisk = ByPy()
    if can_remove:
       os.system(f"bypy remove MinecraftServer/{need_removed}")
    netdisk.upload(zipfile_path, f"MinecraftServer/{zipfile_name}")

    # 清理
    os.remove(zipfile_path)


def make_server_zip():
    """
    将server文件夹压缩.
    并返回所在的临时目录字符串.
    :return: 临时目录字符串
    """
    # 获取服务器实例和参数
    server = get_server()
    config = get_config(server)
    server_name = config["ServerName"]

    # 获取当前时间字符串
    now = datetime.datetime.now()
    now_str = now.strftime("%Y_%m_%d_%H_%M_%S")
    # 基本路径
    running_path = os.getcwd()
    mcdr_config = server.get_mcdr_config()
    # 可以确定的路径
    server_path = os.path.join(running_path, mcdr_config['working_directory'])
    mcdr_plugin_config = os.path.join(running_path, "config")
    mcdr_config_file = os.path.join(running_path, "config.yml")
    # 获取所有支持的插件路径
    mcdr_plugin_path = get_all_mcdr_plugin_path(mcdr_config, running_path)
    # 确定压缩后文件位置
    zipfile_name = f"{server_name}_backup_{now_str}.zip"
    backup_zipfile_path = os.path.join(running_path, "temp", zipfile_name)

    # 开始备份
    server.stop()
    server.wait_until_stop()
    # 开始压缩
    try:
        zip_server(backup_zipfile_path, mcdr_config_file, mcdr_plugin_config, mcdr_plugin_path, server_path)
    except PermissionError:
        pass
    server.logger.info("压缩完成")
    server.start()
    return backup_zipfile_path, zipfile_name


def get_all_mcdr_plugin_path(mcdr_config, running_path):
    """获取全部插件路径"""
    all_mcdr_plugin_path = mcdr_config['plugin_directories']
    mcdr_plugin_path = list()
    for plugin_path in all_mcdr_plugin_path:
        mcdr_plugin_path.append(os.path.join(running_path, plugin_path))
    return mcdr_plugin_path


def zip_server(backup_zipfile, mcdr_config_file, mcdr_plugin_config, mcdr_plugin_path, server):
    """压缩服务器"""
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
