# import os
# import logging
# import aiohttp
# import asyncio
# import chardet
# import contextlib
# from functools import lru_cache
# from datetime import datetime
# from fake_useragent import UserAgent

# path = os.path.dirname(__file__)
# logging.basicConfig(
#     filename=os.path.join(path, '../log/spider.log'),
#     format="%(asctime)s %(thread)d %(filename)s[line:%(lineno)d] %(levelname)s %(message)s",
# )
# logger = logging.getLogger()
# UA = UserAgent()


# def run(ts, s):
#     # 创建并执行协程任务
#     loop = asyncio.get_event_loop()
#     tasks = asyncio.gather(*[asyncio.ensure_future(s.check(t)) for t in ts], loop=loop)
#     loop.run_until_complete(tasks)
#     loop.close()
#     return s.get_results()


# def get_encoding(content) -> str:
#     with contextlib.suppress(AttributeError):
#         return chardet.detect(content).get('encoding')


# def rinse(text) -> str:
#     return ''.join(text.split()).upper()


# def cmp(target, text, eq=True) -> bool:
#     return (rinse(target) == rinse(text)) if eq else (rinse(target) in rinse(text))


# class Spider:
#     """爬虫模块的底层结构体"""
#     def __init__(self, name, url, wait=5, now=False):
#         self.name = name  # 渠道名称
#         self.url = url  # 构建的基础url
#         self.wait = wait  # 等待时间，暂未使用
#         self.results = []  # 所有结果
#         self.now = now
#         self.s_now = None
#         self.e_now = None
#         not self.now or self.print_s_now()

#     def print_s_now(self):
#         self.s_now = datetime.now()
#         print(f's_now：{self.s_now.strftime("%Y-%m-%d %H:%M:%S")}===name：{self.name}')

#     def print_e_now(self):
#         self.e_now = datetime.now()
#         print(f'e_now：{self.e_now.strftime("%Y-%m-%d %H:%M:%S")}===name：{self.name}'
#               f'===s：{(self.s_now-self.e_now).microseconds/1000000}')

#     def get_url(self) -> str:
#         return self.url

#     def get_name(self) -> str:
#         return self.name

#     def get_results(self) -> tuple:
#         not self.now or self.print_e_now()
#         return self.name, self.results

#     @staticmethod
#     def get_param(url, method='get', headers=None, data=None, proxy=None, timeout=None):
#         return url, method, headers or {'User-Agent': UA.random}, data, proxy, timeout

#     async def check(self, target: str):
#         """检查查找对象是否存在"""
#         async with aiohttp.ClientSession() as session:
#             url, method, headers, data, proxy, timeout = self.build_param(target)
#             can, exact_url = False, False
#             with contextlib.suppress(aiohttp.ServerDisconnectedError):
#                 async with session.request(method, url, headers=headers, data=data,
#                                            proxy=proxy, timeout=timeout) as res:
#                     if res.status == 200:
#                         content = await res.read()
#                         can, exact_url = await self.dispose(target, content)
#             self.results.append((target, url, can, exact_url))

#     # TODO 继承之后需要重写此方法
#     @lru_cache(maxsize=128, typed=True)
#     def build_param(self, target):
#         url = self.url
#         return self.get_param(url)

#     # TODO 继承之后需要重写此方法
#     async def dispose(self, target, content) -> tuple:
#         """处理请求后的结果"""
#         encoding = get_encoding(content)
#         print(content.decode('utf-8'))
#         return (True, 'url') if target in content.decode(encoding) else (False, None)
