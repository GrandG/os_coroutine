"""
这是一个实时监测文件内容的程序.
当目标文件的新增内容时, 该程序就会打印出新增的内容

这里用generator实现pipeline, 即follow的输出结果, 作为grep的输入
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

def grep(pattern, lines):
    for line in lines:
        if pattern in line:
            yield line


if __name__ == '__main__':
    with open('log.log', encoding='utf-8') as f:
        for line in grep('python', follow(f)):
            print(line)