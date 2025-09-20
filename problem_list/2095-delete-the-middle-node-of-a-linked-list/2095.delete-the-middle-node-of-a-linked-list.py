#
# @lc app=leetcode id=2095 lang=python3
#
# [2095] Delete the Middle Node of a Linked List
#


# @lc code=start
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def deleteMiddle(self, head: Optional[ListNode]) -> Optional[ListNode]:

        # Edge Case: If the list has 0 or 1 nodes, there is no middle to delete,
        # so the result is an empty list.
        if not head or not head.next:
            return None

        # Initialize three pointers. 'slow' and 'fast' start at the head.
        # 'prev' will track the node just before 'slow'.
        slow = head
        fast = head
        prev = None

        # Loop until the 'fast' pointer reaches the end of the list.
        while fast and fast.next:
            # Advance the pointers.
            prev = slow
            slow = slow.next
            fast = fast.next.next

        # At this point, 'slow' is pointing at the middle node, and
        # 'prev' is pointing at the node right before it.

        # Delete the middle node by having 'prev' skip over 'slow'.
        prev.next = slow.next

        return head


# @lc code=end
