"""
插进来的, 研究一下Iteraotr
"""
import re
import reprlib


RE_WORD = re.compile('\w+')

class Sentence:
    def __init__(self, text):
        self.text = text
        self.word = RE_WORD.findall(text)

    def __getitem__(self, index):                                 # 用了这个magic method, Sentence对象就可以迭代, 既可以用for循环迭代其实例
        return self.word[index]                                   # 一个理解的角度: 实现__geitem__后, 可以用s[0], s[1]的方式取值, 就跟list, tuple一样. list, tuple可以迭代, 所以这里也可以迭代.(鸭子类型)

    def __len__(self):
        return len(self.word)
 
    def __repr__(self):                                           # print实例得到的内容
        return "Sentence is {}".format(reprlib.repr(self.text))   # reprlib.repr()与内置的repr()不同的是, 前者可以控制字符的长度, 超出长度的用省略号代替

    """
    >> s = Sentence('asdasdasdad')
    >> next(s)         # 会报错
    >> it = iter(s)    # 把iterale变成iterator
    >> next(it)        # 成功, 元素输出完后报StopIteration异常
    >> for i in s:     # 可迭代
            print(s)
    """