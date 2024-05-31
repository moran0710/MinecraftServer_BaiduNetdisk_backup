import os
import traceback

from apscheduler.schedulers.background import BackgroundScheduler
from bypy import ByPy
from mcdreforged.api.command import SimpleCommandBuilder
from mcdreforged.api.types import PluginServerInterface

from . import upload
from .utils import get_config

scheduler = BackgroundScheduler()

job_used = False


def on_load(server: PluginServerInterface, _):
    global job_used
    show_title(server)

    # 检查百度网盘配置
    has_baidu_check(server)
    # 检查插件配置文件是否存在
    has_config_check(server)
    # 载入配置
    config = get_config(server)
    server.logger.info(config)
    # 载入mcdr命令
    builder = SimpleCommandBuilder()
    builder.command("!!baidu_backup", callback=upload.upload_to_baidu)
    builder.register(server)
    # 载入定时任务
    if config['AutoSave']['enable']:
        scheduler.add_job(upload.upload_to_baidu, 'cron',
                          day=config['AutoSave']['time']['d'],
                          hour=config['AutoSave']['time']['h'],
                          minute=config['AutoSave']['time']['m'],
                          second=config['AutoSave']['time']['s'],
                          args=[None, None],
                          id="baidu_backup"
                          )
        scheduler.start()
        job_used = True
        server.logger.info("定时任务启动成功")

    # 完成载入
    server.logger.info("插件正确载入！")


def on_unload(server: PluginServerInterface):
    if job_used:
        scheduler.remove_job("baidu_backup")
    server.logger.info("已经卸载本插件，感谢使用")


def show_title(server):
    server.logger.info("                                     ")
    server.logger.info("          Baidu Netdisk Backup Plugin     ")
    server.logger.info("              --Powered By ByPy & Moran0710     ")
    server.logger.info("                                     ")


def has_baidu_check(server):
    server.logger.info("正在测试百度网盘登录状态..")
    server.logger.info("如果出现url，请登录")
    baidu_netdisk = ByPy()
    try:
        baidu_netdisk.info()
    except Exception as e:
        server.logger.error(f"出现异常！", e)
        server.logger.error(traceback.format_exc())
        server.logger.error("本插件将不会正常加载")
        raise e


def has_config_check(server):
    server.logger.info("正在检查配置文件....")
    config_dir_path = server.get_data_folder()
    config_file_name = "baidu_netdisk_backup_config.yaml"
    config_file_path = os.path.join(config_dir_path, config_file_name)
    if not os.path.exists(config_file_path):
        server.logger.error("配置文件不存在！")
        with server.open_bundled_file("baidu_netdisk_backup_config.yaml") as file_handler:
            config_file = file_handler.read().decode('utf8')

        with open(config_file_path, 'w', encoding="utf-8") as file:
            file.write(config_file)
        server.logger.error(f"已经释放配置文件到{config_file_path}")
    running_path = os.getcwd()
    if not os.path.exists(os.path.join(running_path, "temp")):
        os.mkdir("temp")
