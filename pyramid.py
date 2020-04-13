class Solution:
    def generate(numRows):
        if numRows <= 0: return []
        l = []
        for i in range(numRows):
            r = []
            for j in range(i+1):
                if j == 0 or j == i:
                    r.append(1)
                else:
                    r.append(l[i-1][j-1] + l[i-1][j])
            l.append(r)
        return l
Solution.generate(5)