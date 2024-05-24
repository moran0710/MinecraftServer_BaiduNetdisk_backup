from mcdreforged.api.types import PluginServerInterface, Info
from bypy import ByPy
import shutil
import yaml

import os

def on_load(server:PluginServerInterface, perv_moudle):
    show_title(server)

    # 检车百度网盘配置
    has_baidu_check(server)
    # 检查插件配置文件是否存在
    has_config_check(server)
    # 载入配置
    config = get_config(server)
    # 完成载入
    server.logger.info("插件正确载入！")


def show_title(server):
    server.logger.info("#####################################")
    server.logger.info("#                                   #")
    server.logger.info("#    Baidu Netdisk Backup Plugin    #")
    server.logger.info("#                                   #")
    server.logger.info("#  --Powered By ByPy & Moran0710    #")
    server.logger.info("#                                   #")
    server.logger.info("#####################################")


def has_baidu_check(server):
    server.logger.info("正在测试百度网盘登录状态..")
    server.logger.info("如果出现url，请登录")
    baidu_netdisk = ByPy()
    try:
        baidu_netdisk.info()
    except Exception as e:
        server.logger.error(f"出现异常！", e)
        server.logger.error("本插件将不会正常加载")
        raise e


def has_config_check(server):
    server.logger.info("正在检查配置文件....")
    config_dir_path = server.get_data_folder()
    config_file_name = "baidu_netdisk_backup_config.yaml"
    config_file_path = os.path.join(config_dir_path, config_file_name)
    if not os.path.exists(config_file_path):
        server.logger.error("配置文件不存在！")
        local_dir_path = os.path.abspath(os.path.dirname(__file__))
        local_config_file_path = os.path.join(local_dir_path, config_file_name)

        shutil.copyfile(local_config_file_path, config_file_path)
        server.logger.error(f"已经释放配置文件到{config_file_path}")

def get_config(server):
    server.logger.info("正在载入配置...")
    config_dir_path = server.get_data_folder()
    config_file_name = "baidu_netdisk_backup_config.yaml"
    config_file_path = os.path.join(config_dir_path, config_file_name)
    with open(config_file_path, "r", encoding="utf8") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data
