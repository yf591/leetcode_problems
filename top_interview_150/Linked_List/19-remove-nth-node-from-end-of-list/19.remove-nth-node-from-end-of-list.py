#
# @lc app=leetcode id=19 lang=python3
#
# [19] Remove Nth Node From End of List
#


# @lc code=start
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:

        # Create a dummy node that points to the head. This simplifies
        # handling the edge case of removing the first node.
        dummy = ListNode(0, head)

        # Initialize two pointers, both starting at the dummy node.
        slow = dummy
        fast = dummy

        # 1. Advance the 'fast' pointer n + 1 steps ahead.
        #    This creates the initial gap between slow and fast.
        for _ in range(n + 1):
            fast = fast.next

        # 2. Move both pointers in tandem until 'fast' reaches the end (None).
        #    Because of the initial gap, when 'fast' is at the end, 'slow'
        #    will be at the node right before the one we want to delete.
        while fast:
            slow = slow.next
            fast = fast.next

        # 3. 'slow' is now at the predecessor of the target node.
        #    Delete the target node by re-wiring the 'next' pointer.
        slow.next = slow.next.next

        # The dummy's 'next' will be the head of the modified list.
        return dummy.next


# @lc code=end
