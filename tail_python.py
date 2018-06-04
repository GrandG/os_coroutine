"""
加上一个装饰器, 这样coroutine就不用primed了
这里把grep变成了一个coroutine, 区别在于用了=yield, 使得func可consum数据而不仅仅是产生数据
"""


import time

def follow(the_file):
    the_file.seek(0, 2)              # 这是把移到文件的底部, seek的第一个参数指从第几个字符开始; 第二个参数指位置, 0是开头, 1是当前位置, 2是最底部
    while True:
        line = f.readline()          # 读一行
        if not line:
            time.sleep(0.1)          # 如没有新的内容, 隔0.1s再读一次
            continue
        yield line

def coroutine(func):                # 装饰器, 使得从routine可以直接使用, 不用primed
    def wrapper(*args, **kwargs):
        c = func(*args, **kwargs)
        c.send(None)
        return c
    return wrapper

 
@coroutine                           # 加上装饰器
def grep(pattern):                   # 这个coroutine在命令行中执行效果更佳, coroutine在send真实数据之前, 一定要send(None)或next()
    try:
        while True:
            line = yield
            if pattern in line:
                print(line)
    except GeneratorExit:
        print('Grep close, goodbye')


if __name__ == '__main__':
    with open('log.log', encoding='utf-8') as f:
        for line in grep('python', follow(f)):
            print(line)