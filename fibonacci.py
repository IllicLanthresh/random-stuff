class CacheDict(dict):
    def __init__(self, *args, **kwargs):
        super(CacheDict, self).__init__(*args, **kwargs)
    def __setitem__(self, key, value):
        if len(self) > 1:
            self.pop(list(self.keys())[0])
        super(CacheDict, self).__setitem__(key, value)
        self.lastAdded = key

cache = CacheDict()
class Solution:
    def fib(self, n: int) -> int:
        if n < 2: return n
        if n in cache: return cache[n]
        result = self.fib(n-1) + self.fib(n-2)
        cache[n] = result
        return result