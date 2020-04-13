
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def reverseList(head):
        if head.next == None: return head
        prev = Solution.reverseList(head.next)
        head.next.next = head
        head.next = None
        return prev

l = list(range(1, 6))

node = None
head = None
for i, j in zip(l[:-1], l[1:]):
    if node ==  None:
        node = ListNode(i)
        head = node
    node2 = ListNode(j)
    node.next = node2
    node = node2

Solution.reverseList(head)
