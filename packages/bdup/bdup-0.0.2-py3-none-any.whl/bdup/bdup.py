# -*- coding: UTF-8 –*-
import getpass
import os
import pathlib
import platform
import subprocess
from bypy import ByPy
from concurrent.futures import ThreadPoolExecutor


class BaiDu:
    """
    如果通过调用命令行终端运行, 云端路径必须使用linux格式，不要使用windows格式,否则在windows系统里面会上传失败(无法在云端创建文件)
    """
    def __init__(self):
        self.local_path = None
        self.remote_path = None
        self.delete_file = False
        self.suffix: list = []
        self.local_file = None
        self.remote_file = None

    def upload_path(self):
        """
        文件夹 -> 文件夹, (整个文件夹上传, 不能筛选文件)
        delete_file : 上传文件后是否删除原文件
        """
        if not self.local_path or not self.remote_path:
            return
        local_path = str(self.local_path)
        remote_path = str(self.remote_path)
        delete_file = self.delete_file
        if not os.path.exists(local_path):
            return
        # print(f'正在上传百度云...')
        if platform.system() == 'Windows':
            bp = ByPy()  
            bp.upload(localpath=str(local_path), remotepath=str(remote_path))  # 上传文件夹到百度云
        else:
            command = f'bypy upload "{str(local_path)}" "{str(remote_path)}" --on-dup skip'  # 相同文件跳过
            try:  # 如果通过调用命令行终端运行, 云端路径必须使用linux格式，不要使用windows格式,否则在windows系统里面会报错
                subprocess.run(command, shell=True)
            except Exception as e:
                print(e)

        if delete_file:
            for root, dirs, files in os.walk(local_path, topdown=False):
                for name in files:
                    if 'ini' not in name:
                        os.remove(os.path.join(root, name))

    def upload_path2(self):
        """
        文件夹 -> 文件夹 (读取文件夹并逐个文件上传), 筛选文件设置 self.suffix
        """
        if not self.local_path or not self.remote_path:
            return
        local_path = str(self.local_path)
        remote_path = str(self.remote_path)
        delete_file = self.delete_file
        suffix = self.suffix
        upload_infos = []
        for root, dirs, files in os.walk(local_path, topdown=False):
            for name in files:
                if 'ini' in name or 'desktop' in name or '.DS_Store' in name:
                    continue
                if suffix:
                    if os.path.splitext(name)[1] in suffix:
                        upload_infos += [[os.path.join(root, name), f'{remote_path}/{name}']]
                else:
                    upload_infos += [[os.path.join(root, name), f'{remote_path}/{name}']]

        if not upload_infos:
            return
        # print(f'正在上传百度云...')
        with ThreadPoolExecutor() as pool:  # 线程池
            pool.map(self.uploads, upload_infos)

        if delete_file:
            for root, dirs, files in os.walk(local_path, topdown=False):
                for name in files:
                    if 'ini' not in name:
                        os.remove(os.path.join(root, name))

    def upload_file(self):
        """ 
        文件 -> 文件 (上传单个文件), 筛选文件设置 self.suffix
        """
        if not self.local_file or not self.remote_file:
            return
        suffix = self.suffix
        if suffix:
            if os.path.splitext(self.local_file)[1] not in suffix:
                return
        local_file = str(self.local_file)
        remote_file = str(self.remote_file)
        delete_file = self.delete_file
        self.uploads([local_file, remote_file])
        if delete_file:
            os.remove(local_file)

    @staticmethod
    def uploads(upload_info):  # 被调用函数
        _up_load, _remote = upload_info
        _up_load = str(_up_load)
        _remote = str(_remote)
        if platform.system() == 'Windows':
            bp = ByPy()
            bp.upload(localpath=_up_load, remotepath=_remote)  # 上传文件到百度云
        else:
            command = f'bypy upload "{_up_load}" "{_remote}" --on-dup skip --chunk 1MB'  # 相同文件跳过
            try:
                subprocess.run(command, shell=True)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    print(1)
