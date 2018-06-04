# os_coroutine
A simple operating system used coroutine

Tags:
- nothing. 一开始, 什么都没有.
- follow. 用generator实现实时监控文件的新增内容.
- pipeline例子. 用generator实现pipeline. 即增加一个过滤器, 新增的内容只有包含过滤器的关键字才显示出来.
- coroutine. 把grep由generator变成coroutine.
- coroutine_decorator. 手动写coroutine装饰器, 使得coroutine可以直接使用.
- exception. 捕抓close引起得异常
- pipeine. 一条线的pipeline
- multi-pipe. 多路pipe
- Task. 创建任务类, 把target(generator或coroutine变成Task对象)
- multasking. 第一个multitasking的os