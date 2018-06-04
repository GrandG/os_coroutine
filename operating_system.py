"""
第一个multitasking system
"""
import time
from queue import Queue


class Task:                                       # 把target(generator或coroutie)变成Task对象, Task在这里主要是维护一个task_id. 还有维护一个sendval, 这个在以后用到.
    task_id = 0
    def __init__(self, target):
        self.target = target
        self.tid = Task.task_id
        self.sendval = None

    def run(self):
        self.target.send(self.sendval)


class Schedualer:
    def __init__(self):
        self.ready = Queue()                  # 阻塞队列
        self.task_map = {}                    # 这里现在还没用到

    def new(self, target):                    # 创建一个新的task, 把target变为task对象, 在放到queue和task_map中
        task = Task(target)
        self.schedual(task)
        self.task_map[task.tid] = task
        return task.tid

    def schedual(self, task):
        self.ready.put(task)


    def main_loop(self):
        while True:
            task = self.ready.get()            # 把task从queue中取出, 这时queue少了一个任务
            result = task.run()                # 把task运行的结果, 即task的yield右边的表达式返回值赋给result. 这里是后面才用到
            self.schedual(task)                # 把task再放回队列中

def foo():
    while True:
        print('I am foo')
        time.sleep(1)
        yield

def bar():
    while True:
        print('I am bar')
        time.sleep(0.5)
        yield

if __name__ == '__main__':
    sched = Schedualer()
    sched.new(foo())
    sched.new(bar())
    sched.main_loop()