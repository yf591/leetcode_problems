#
# @lc app=leetcode id=82 lang=python3
#
# [82] Remove Duplicates from Sorted List II
#


# @lc code=start
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # Create a dummy node to act as a placeholder before the head.
        # This simplifies handling duplicates at the beginning of the list.
        dummy = ListNode(0, head)

        # 'pred' (predecessor) is the last node we know is not a duplicate.
        pred = dummy

        while head:
            # Check if the current node is the start of a duplicate section.
            if head.next and head.val == head.next.val:
                # If it is, skip all nodes with this value.
                # The inner loop moves 'head' to the last node of the duplicate block.
                while head.next and head.val == head.next.val:
                    head = head.next

                # Re-wire the predecessor's 'next' to skip the entire duplicate block.
                pred.next = head.next
            else:
                # If the current node is not a duplicate, it's a "good" node.
                # We can advance our predecessor pointer.
                pred = pred.next

            # Advance the main pointer to check the next node in the original list.
            head = head.next

        # Return the head of the cleaned list.
        return dummy.next


# @lc code=end
