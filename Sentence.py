"""
1. 用Python的方式实现Sentence可迭代对象: 不实现SentenceIteraot, 而在Senternce的__iter__实现一个生成器
"""
import re
import reprlib


RE_WORD = re.compile('\w+')


class Sentence:
    def __init__(self, text):
        self.text = text
        self.word = RE_WORD.findall(text)

    def __iter__(self):                              # 这里可以用iter(self.word)直接实现
        for word in self.word:
            yield word

        return                                       # 这一句可以不要

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