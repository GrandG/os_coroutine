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
- task_exit. 处理任务退出
- task_management. 增加两个System Call. 一个是创建新任务, 一个是删除任务.
- task_waiting. 增加一个等待task的system call
- echo_server. 实现一个web server, 但是os被挂起.
- echo_server_note. 增加一些注释.
- Sentence. 实现一个可迭代对象
- Sentence_2. 根据可迭代设计模式, 重构Sentence可迭代对象, 新增SentencIterator迭代器.
- Sentence_3.用python的方式重构实现Iterable. 
- Sentence_4.实现Setence的Lazy版本, 即迭代的时候才生成具体的值. 
- Sentence_5.用生成器表达式语法糖改写```__iter__```方法. 

