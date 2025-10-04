#
# @lc app=leetcode id=92 lang=python3
#
# [92] Reverse Linked List II
#


# @lc code=start
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseBetween(
        self, head: Optional[ListNode], left: int, right: int
    ) -> Optional[ListNode]:

        # Handle edge cases where no reversal is needed.
        if not head or left == right:
            return head

        # Use a dummy node to simplify handling the case where left=1.
        dummy = ListNode(0, head)
        # 'prev' will point to the node just before the reversal section.
        prev = dummy

        # 1. Move 'prev' to the (left - 1)-th node.
        for _ in range(left - 1):
            prev = prev.next

        # 2. Initialize pointers for the reversal.
        # 'start' is the first node of the sublist to be reversed.
        start = prev.next
        # 'then' is the node that we will move.
        then = start.next

        # 3. Perform the reversal 'right - left' times.
        for _ in range(right - left):
            # The four key steps to move 'then' to the front:
            start.next = then.next
            then.next = prev.next
            prev.next = then
            # Reset 'then' for the next iteration.
            then = start.next

        return dummy.next


# @lc code=end
