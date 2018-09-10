import os
import sys
from shutil import copyfile


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")

    isExists = os.path.exists(path)

    if not isExists:
        #print(path + ' 创建成功')
        os.makedirs(path)
        return True
    else:
        print(path + ' 目录已存在')
        return False


def doo():
    sweetest_dir = os.path.dirname(os.path.realpath(__file__))
    current_dir = os.getcwd()
    doo_folder = os.path.join(current_dir, 'doo_example')
    if not mkdir(doo_folder):
        return
    copyfile(os.path.join(sweetest_dir, 'example.xlsx'),
             os.path.join(doo_folder, 'example.xlsx'))
    copyfile(os.path.join(sweetest_dir, 'example.yml'),
             os.path.join(doo_folder, 'example.yml'))
    copyfile(os.path.join(sweetest_dir, 'app.py'),
             os.path.join(doo_folder, 'app.py'))
    copyfile(os.path.join(sweetest_dir, 'doo.postman_collection.json'),
             os.path.join(doo_folder, 'doo.postman_collection.json'))

    print('\n生成 doo example 成功\n\n请运行如下命令启动示例 Mock 服务\n\ncd doo_example\npython app.py example.yml')
