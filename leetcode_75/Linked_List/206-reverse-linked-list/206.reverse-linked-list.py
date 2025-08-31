#
# @lc app=leetcode id=206 lang=python3
#
# [206] Reverse Linked List
#


# @lc code=start
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # 'prev' will store the previous node, starting as None.
        prev_node = None
        # 'current' starts at the head of the list.
        current_node = head

        # Iterate through the entire list.
        while current_node:
            # 1. Store the next node before we overwrite the pointer.
            next_temp = current_node.next

            # 2. This is the reversal: point the current node's 'next' to the previous node.
            current_node.next = prev_node

            # 3. Move both pointers one step forward for the next iteration.
            prev_node = current_node
            current_node = next_temp

        # When the loop finishes, 'current_node' is None, and 'prev_node' is the new head.
        return prev_node


# @lc code=end
