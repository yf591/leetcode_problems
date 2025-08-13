#
# @lc app=leetcode id=141 lang=python3
#
# [141] Linked List Cycle
#

# @lc code=start
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None


class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        # Initialize two pointers, a slow one and a fast one.
        slow = head
        fast = head

        # Traverse the list as long as the fast pointer and the node after it are valid.
        # This prevents errors from trying to access `fast.next.next`
        while fast and fast.next:
            # The slow pointer moves one step at a time.
            slow = slow.next
            # The fast pointer moves two steps at a time.
            fast = fast.next.next

            # If the pointers ever meetm, we have found a cycle.
            if slow == fast:
                return True

        # If the loop finishes, it means the fast pointer reached the end of the list,
        # so there is no cycle.
        return False


# @lc code=end
