"""
1. __iter__方法用生成器表达式改写
"""
import re
import reprlib


RE_WORD = re.compile('\w+')


class Sentence:
    def __init__(self, text):
        self.text = text

    def __iter__(self):                              
        return (word.group() for word in RE_WORD.finditer(self.text)) # 注意, 这里的return不能省略

    def __repr__(self):
        return 'Sentence is {}'.format(reprlib.repr(self.text))


    """
    >> s = Sentence('asdasdasdad')
    >> next(s)         # 会报错
    >> it = iter(s)    # 把iterale变成iterator
    >> next(it)        # 成功, 元素输出完后报StopIteration异常
    >> for i in s:     # 可迭代
            print(s)
    """