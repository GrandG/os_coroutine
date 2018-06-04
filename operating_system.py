"""
用coroutine实现multitasking的operating system
"""
import time


class Task:                                       # 把target(generator或coroutie)变成Task对象, Task在这里主要是维护一个task_id. 还有维护一个sendval, 这个在以后用到.
    task_id = 0
    def __init__(self, target):
        self.target = target
        self.tid = Task.task_id
        self.sendval = None

    def run(self):
        self.target.send(self.sendval)


def foo():
    while True:
        print('I am foo')
        time.sleep(1)
        yield

if __name__ == '__main__':
    t = Task(foo())
    while True:
        t.run()