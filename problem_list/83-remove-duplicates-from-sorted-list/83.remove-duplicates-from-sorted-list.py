#
# @lc app=leetcode id=83 lang=python3
#
# [83] Remove Duplicates from Sorted List
#


# @lc code=start
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # Use a 'current' pointer to traverse the list, starting at the head.
        current = head

        # We need to loop as long as 'current' and 'current.next' are valid nodes.
        while current and current.next:
            # Check if the next node is a duplicate of the current node.
            if current.val == current.next.val:
                # If it is a duplicate, we skip over the next node by
                # pointing the current node's 'next' to the one after the duplicate.
                current.next = current.next.next
            else:
                # If it's not a duplicate, we just move our pointer forward.
                current = current.next

        # Return the head of the modified list.
        return head


# @lc code=end
