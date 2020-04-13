import cProfile
def reverseString(s):
    l = len(s)
    half = l//2
    for i, j in zip(range(half), range(l-1, l-1-half, -1)):
        s[i], s[j] = s[j], s[i]
s = list("hello")
reverseString(s)
print(s)