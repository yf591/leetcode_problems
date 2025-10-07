#
# @lc app=leetcode id=86 lang=python3
#
# [86] Partition List
#


# @lc code=start
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def partition(self, head: Optional[ListNode], x: int) -> Optional[ListNode]:

        # Create dummy heads for the two new lists.
        less_head = ListNode()  # Head for the list of nodes < x
        greater_head = ListNode()  # Head for the list of nodes >= x

        # Create tail pointers to build the new lists.
        less_tail = less_head
        greater_tail = greater_head

        # Use a 'current' pointer to traverse the original list.
        current = head

        while current:
            # If the current node's value is less than x...
            if current.val < x:
                # ...append it to the 'less' list.
                less_tail.next = current
                less_tail = less_tail.next
            else:
                # ...otherwise, append it to the 'greater or equal' list.
                greater_tail.next = current
                greater_tail = greater_tail.next

            # Move to the next node in the original list.
            current = current.next

        # After the loop, terminate the 'greater or equal' list.
        greater_tail.next = None

        # Connect the end of the 'less' list to the start of the 'greater' list.
        less_tail.next = greater_head.next

        # The head of our final list is the node after our 'less_head' dummy node.
        return less_head.next


# @lc code=end
