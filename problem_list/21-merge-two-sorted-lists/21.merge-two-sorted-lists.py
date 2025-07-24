#
# @lc app=leetcode id=21 lang=python3
#
# [21] Merge Two Sorted Lists
#


# @lc code=start
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def mergeTwoLists(
        self, list1: Optional[ListNode], list2: Optional[ListNode]
    ) -> Optional[ListNode]:
        # Create a dummy node to act as the starting point of the new list.
        # This simplifies ege cases like an empty merged list.
        dummy = ListNode()
        # 'current' will be our pointer to build the new list.
        current = dummy

        # While as lonf as both lists have nodes.
        while list1 and list2:
            # Compare the value of the two lists' current nodes.
            if list1.val < list2.val:
                # If list1's node is smaller, attach it to the new list.
                current.next = list1
                # Move the list1 pointer to its next node.
                list1 = list1.next
            else:
                # Otherwise, attach list2's node.
                current.next = list2
                # Move the list2 pointer to its next node.
                list2 = list2.next

            # Move the 'current' pointer forward to the end of the new list.
            current = current.next

        # After the loop, at least one list is empty.
        # Attach the remaining part of non-empty list.
        if list1:
            current.next = list1
        elif list2:
            current.next = list2

        # The merged list starts after the dummy node, so return dummy.next.
        return dummy.next


# @lc code=end
