"""
用coroutine实现pipeline
多路pipeline
"""


import time

def coroutine(func):                            # 装饰器
    def wrapper(*args, **kwargs):
        c = func(*args, **kwargs)
        c.send(None)
        return c
    return wrapper


def follow(the_file, target):                  # pipeline的source, 用于源源不断地产生data, 这个通常不是coroutine
    the_file.seek(0, 2)                        # source的形参必然包括下一个pipe的对象 这里是target. 必须用到send方法
    while True:
        line = the_file.readline()
        if not line:
            time.sleep(0.1)
            continue
        target.send(line)

@coroutine
def grep(pattern, target):                    # filter. 属于source和sink之间的部分. 用于过滤
    while True:                               # 他必须接受上一节的data(即=yield), 处理数据后, 把data send到下一节.
        line = yield
        if pattern in line:
            target.send(line)

@coroutine
def printer():                                # sink, 用于最终接受数据, 并处理数据, 这个是coroutine
    while True:                               # sink必须接受上一节pipe senf的data(即包含=yield), 但不包含下一节的pipe, 因为sink就是最后一节
        line = yield
        print(line)

@coroutine
def broadcast(targets):
    while True:
        line = yield
        for target in targets:
            target.send(line)

if __name__ == '__main__':
    with open('log.log') as f:
        follow(f, broadcast([grep('gao', printer()), grep('guo', printer()), grep('wei', printer())]))