"""
1. 实现Sentence的lazy版本. 之前的做法在构造函数的时候直接生成了要迭代的所有的值. 现在实现只有当迭代的时候在生成具体的值
"""
import re
import reprlib


RE_WORD = re.compile('\w+')


class Sentence:
    def __init__(self, text):
        self.text = text

    def __iter__(self):                              
        for word in RE_WORD.finditer(self.text):          # finditer是findall的lazy版本
            yield word.group()                            # 这里调用group返回具体文本
        return

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