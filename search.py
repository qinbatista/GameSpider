import os
import time
import subprocess
from CodeLibrary.tool.data_manage import read_json
from CodeLibrary.tool.data_manage import save_json
from CodeLibrary.tool.data_manage import save_excel
import shutil
PATH = os.path.join(os.path.dirname(__file__))


def verify_path(path) -> None:
    os.path.exists(path) or os.mkdir(path)


class AppFinder:
    def __init__(self, apps):
        self.apps = apps
        self.spiders = []
        self.spider_dir = os.path.join(PATH, 'CodeLibrary/spider')
        self.caches = {}
        self.cache_dir = os.path.join(PATH, f'CodeLibrary/cache')
        self.result_dir = os.path.join(PATH, f'CodeLibrary/result')
        self.timestamp = f'{time.time()}'.replace('.', '')
        self.cmd = 'python' if os.name == 'nt' else 'python3'

    def __find_spider(self):
        files = os.listdir(self.spider_dir)
        self.spiders = [os.path.join(self.spider_dir, f) for f in files if f[-3:] == ".py"]

    def __create_cache(self):
        os.path.exists(self.cache_dir) or os.mkdir(self.cache_dir)
        self.caches = {app: os.path.join(self.cache_dir, f'{app}_{self.timestamp}') for app in self.apps}
        [os.path.exists(path) or os.mkdir(path) for path in self.caches.values()]

    def __execute_spider(self):
        processes = []
        for sd in self.spiders:
            processes += [subprocess.Popen([self.cmd, sd, app, path]) for app, path in self.caches.items()]
        for process in processes:
            process.wait()

    def __save(self, fk):
        results = []
        temp_dir = os.path.join(self.cache_dir, fk)
        for f in os.listdir(temp_dir):
            data = read_json(os.path.join(temp_dir, f))
            for k, vs in data[0].items():
                results.append({'渠道': f[:-5], '游戏名': k, **vs})
        dir_json = f'{self.result_dir}/{fk}'
        dir_excel = f'{self.result_dir}/{fk}'
        verify_path(dir_json)
        verify_path(dir_excel)
        save_json(f'{dir_json}/results.json', results)
        save_excel(f'{dir_json}/results.xlsx', results)
        if os.path.exists(dir_excel+"/results.xlsx"):os.remove(PATH+"/results.xlsx")
        shutil.copy(dir_excel+"/results.xlsx",PATH+"/results.xlsx")

    def run(self):
        self.__find_spider()
        self.__create_cache()
        self.__execute_spider()
        [self.__save(f'{app}_{self.timestamp}') for app in self.apps]


if __name__ == '__main__':
    # af = AppFinder(['一起玩陶艺', '王者荣耀', 'qq飞车'])
    af = AppFinder([input("输入游戏名字:")])
    af.run()

