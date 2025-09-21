#
# @lc app=leetcode id=2130 lang=python3
#
# [2130] Maximum Twin Sum of a Linked List
#


# @lc code=start
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def pairSum(self, head: Optional[ListNode]) -> int:

        # --- Step 1: Find the middle of the linked list ---
        slow = head
        fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        # 'slow' is now at the head of the second half of the list.

        # --- Step 2: Reverse the second half of the list ---
        prev = None
        current = slow
        while current:
            next_temp = current.next
            current.next = prev
            prev = current
            current = next_temp
        # 'prev' is now the head of the reversed second half.

        # --- Step 3: Pair up nodes and find the max twin sum ---
        max_sum = 0
        first_half_head = head
        second_half_head = prev

        # Iterate through both halves simultaneously.
        while second_half_head:
            current_twin_sum = first_half_head.val + second_half_head.val
            max_sum = max(max_sum, current_twin_sum)

            # Move to the next pair.
            first_half_head = first_half_head.next
            second_half_head = second_half_head.next

        return max_sum


# @lc code=end
