"""
在上一个例子中, IO operation block的有:
1. client, addr = sock.accept()
2. data = client.recv(1024)
3. client.send(data)
"""
import time
from queue import Queue
import socket


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

    def handle(self):                              # 通常情况下, handle里必须包括把现在取出的task, 放回到queue中, 即包含self.schedual(task)语句
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


class WaitTask(SystemCall):
    def __init__(self, tid):
        self.tid = tid

    def handle(self):
        result = self.sched.waitforexit(self.task, self.tid)
        if not result:
            self.sched.schedual(self.task)

class Schedualer:
    def __init__(self):
        self.ready = Queue()                  # 阻塞队列
        self.task_map = {}                    # 这里现在还没用到
        self.exit_waiting = {}

    def new(self, target):                    # 创建一个新的task, 把target变为task对象, 在放到queue和task_map中
        task = Task(target)
        self.schedual(task)
        self.task_map[task.tid] = task
        return task.tid

    def exit(self, task):
        del self.task_map[task.tid]
        print('Task {} exit'.format(task.tid))
        
        if task.tid in self.exit_waiting:
            [self.schedual(task) for task in self.exit_waiting.get(task.tid)]


    def waitforexit(self, task, tid):         # 在要等待的task退出之后, 在exit_waiting中把对应的等待的task重新加入queue中
        if tid in self.task_map:
            self.exit_waiting.setdefault(tid, []).append(task)
            return True
        return False

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
    yield WaitTask(task_id)
    for _ in range(3):
        yield
    result = yield KillTask(task_id)
    if result:
        print('Task Done')
    else:
        print('Task can not be deleted or task does not exit')

def handle_client(client, addr):
    print('Conecting from {}'.format(addr))
    while True:
        data = client.recv(1024)
        if data:
            client.send(data)
        else:
            break
    client.close()
    print('Client close')
    yield

def server(port):
    print('Server starting...')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', port))                                  # bind接受的是一个tuple
    sock.listen(5)

    while True:
        client, addr = sock.accept()
        yield NewTask(handle_client(client, addr))                  # handle_client是另一个任务

if __name__ == '__main__':
    sched = Schedualer()
    sched.new(foo())
    # sched.new(bar())
    # sched.new(some_task())
    sched.new(server(44444))
    sched.main_loop()