import yaml
import os
from mcdreforged.api.types import PluginServerInterface


def get_config(server):
    server.logger.info("正在载入配置...")
    config_dir_path = server.get_data_folder()
    config_file_name = "baidu_netdisk_backup_config.yaml"
    config_file_path = os.path.join(config_dir_path, config_file_name)
    with open(config_file_path, "r", encoding="utf8") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data


def get_server():
    """获取服务器实例"""
    server = PluginServerInterface.get_instance().as_plugin_server_interface()
    return server
