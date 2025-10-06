#
# @lc app=leetcode id=61 lang=python3
#
# [61] Rotate List
#


# @lc code=start
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def rotateRight(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        # Handle edge cases: empty list, single node list, or k=0.
        if not head or not head.next or k == 0:
            return head

        # --- Step 1: Find the length and the tail of the list ---
        length = 1
        tail = head
        while tail.next:
            tail = tail.next
            length += 1

        # --- Step 2: Make the list circular ---
        tail.next = head

        # --- Step 3: Calculate the effective rotation and find the new tail ---
        # The number of steps to the new tail is (length - (k % length)).
        # We find the node at position (length - k - 1).
        k = k % length
        steps_to_new_tail = length - k - 1

        new_tail = head
        for _ in range(steps_to_new_tail):
            new_tail = new_tail.next

        # --- Step 4: Find the new head and break the circle ---
        new_head = new_tail.next
        new_tail.next = None

        return new_head


# @lc code=end
