"""
1. 根据迭代器协议, 实现Iterable和Iterator
2. Iterable要实现__iter__方法, 但不能实现__next__方法; Iterator要实现__iter__和__next__
3. 这样写法对Python来说比较复杂, 下一节用Python的方法实现可迭代对象和迭代器
"""
import re
import reprlib


RE_WORD = re.compile('\w+')


class SentenceIterator:
    def __init__(self, word):
        self.word = word
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            word = self.word[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return word

class Sentence:
    def __init__(self, text):
        self.text = text
        self.word = RE_WORD.findall(text)

    def __iter__(self):
        return SentenceIterator(self.word)

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