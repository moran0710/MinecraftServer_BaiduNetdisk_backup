from .utils import get_server, get_config

import json
import os


def rewrite_solt(filename):
    """
    检查槽位是否已满，并更新槽位
    :param filename: 新文件路径
    :return: (bool, filename)是否已满，以及要删除的文件名
    """
    server = get_server()
    plugin_config_path = server.get_data_folder()
    slot_file = os.path.join(plugin_config_path, "slot.json")
    max_slot = get_config(server)["slot"]

    server.logger.info(filename)
    if not os.path.exists(slot_file):
        with open(slot_file, "w", encoding="utf-8") as f:
            slot = [filename]
            server.logger.info("没有槽位文件 正在新建")
            server.logger.info(slot)
            json.dump(slot, f)
            return False, None
    else:
        with open(slot_file, "r", encoding="utf-8") as f:
            slot = list(json.load(f))
    if len(slot) >= max_slot:
        removed = slot.pop(0)
        slot.append(filename)
        with open(slot_file, "w", encoding="utf-8") as f:
            json.dump(slot, f)
            return True, removed
    else:
        slot.append(filename)
        with open(slot_file, "w", encoding="utf-8") as f:
            json.dump(slot, f)
        return False, None
