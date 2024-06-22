# 百度网盘备份插件

## 补充

~~有问题提了issue，我解决之后能不能issue回复一句啊，我真的真的很想知道你们的问题解决没有，我真的很想知道issue能不能关，不要提完issue之后我回复之后旧突然消失好吗~~

## 介绍
这是一个基于[ByPy](https://github.com/houtianze/bypy)来~~白嫖~~用来利用百度网盘的免费空间来备份整个服务端的插件

支持自动保存和指令`!!baidu_backup`保存，自动上传到百度网盘，不占用本地空间

支持多槽位，超出槽位个数的百度网盘备份将被删除

## 安装

1. 前往release下载.mcdr文件
2. 丢进你的mcdr plugin文件夹
3. 你需要安装以下依赖，直接执行以下命令
```
pip install bypy
pip install APScheduler
```
4. 第一次运行时，Bypy会要求你登录百度网盘，请根据bypy在命令行的提示登录（点击提供的链接，并复制授权码到命令行）
5. done

## 配置&使用
插件会在./config下释放配置文件文件夹`./config/baidu_netdisk_backup/baidu_netdisk_backup_config.yaml`，
按照说明填写即可

使用`!!baidu_backup`手动备份

备份时会重启服务器

## 反馈
请在issue提供

## 鸣谢
1. [ByPy](https://github.com/houtianze/bypy)
2. [MCDReforged](https://github.com/MCDReforged/MCDReforged)
