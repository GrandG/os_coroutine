"""
第一个System call
可以看出: 
1. Target与Schudual完全没有关系, 编写target函数的时候, 完全不用考虑Schedual
2. Target函数可能会调用System call
3. Schedualer与System Call有紧密的联系
4. System Call相当于从Schedualer分离出来的方法
"""
import time
from queue import Queue


class Task:                                       # 把target(generator或coroutie)变成Task对象, Task在这里主要是维护一个task_id. 还有维护一个sendval, 这个在以后用到.
    task_id = 0
    def __init__(self, target):
        self.target = target
        self.tid = Task.task_id
        self.sendval = None
        Task.task_id += 1

    def run(self):
        return self.target.send(self.sendval)

class SystemCall:
    def __init__(self):
        pass

    def handle(self):
        pass

class GetTid(SystemCall):                          # System call
    def __init__(self):
        pass

    def handle(self):
        tid = self.task.tid
        self.task.sendval = tid
        self.sched.schedual(self.task)

class NewTask(SystemCall):
    def __init__(self, target):
        self.target = target

    def handle(self):
        tid = self.sched.new(self.target)
        self.sched.schedual(self.task)
        self.task.sendval = tid


class KillTask(SystemCall):
    def __init__(self, tid):
        self.tid = tid

    def handle(self):
        task = self.sched.task_map.get(self.tid)
        if task:
            task.target.close()
            self.sched.sendval = True
        else:
            self.sched.sendval = False
        self.sched.schedual(self.task)

class Schedualer:
    def __init__(self):
        self.ready = Queue()                  # 阻塞队列
        self.task_map = {}                    # 这里现在还没用到

    def new(self, target):                    # 创建一个新的task, 把target变为task对象, 在放到queue和task_map中
        task = Task(target)
        self.schedual(task)
        self.task_map[task.tid] = task
        return task.tid

    def exit(self, task):
        del self.task_map[task.tid]
        print('Task {} exit'.format(task.tid))

    def schedual(self, task):
        self.ready.put(task)


    def main_loop(self):
        while True:
            task = self.ready.get()            # 把task从queue中取出, 这时queue少了一个任务
            try:
                result = task.run()                # 把task运行的结果, 即task的yield右边的表达式返回值赋给result. 这里是后面才用到
                if isinstance(result, SystemCall):
                    result.task = task
                    result.sched = self
                    result.handle()
                    continue
            except StopIteration:
                self.exit(task)
                continue
            self.schedual(task)                # 把task再放回队列中

def foo():
    mytid = yield GetTid()
    while True:
        print('I am foo', mytid)
        time.sleep(1)
        yield

def bar():
    mytid = yield GetTid()                     # 调用system call
    for _ in range(5):
        print('I am bar', mytid)
        time.sleep(0.5)
        yield

def some_task():
    task_id = yield NewTask(bar())
    for _ in range(3):
        yield
    result = yield KillTask(task_id)
    if result:
        print('Task Done')
    else:
        print('Task can not be deleted or task does not exit')

if __name__ == '__main__':
    sched = Schedualer()
    sched.new(foo())
    sched.new(bar())
    sched.new(some_task())
    sched.main_loop()