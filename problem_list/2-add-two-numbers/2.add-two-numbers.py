#
# @lc app=leetcode id=2 lang=python3
#
# [2] Add Two Numbers
#


# @lc code=start
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def addTwoNumbers(
        self, l1: Optional[ListNode], l2: Optional[ListNode]
    ) -> Optional[ListNode]:

        dummy = ListNode(
            0
        )  # Create a dummy node to simplify the result list construction
        current = dummy  # Pointer to the current node in the result list
        carry = 0  # Initialize carry to 0

        # Loop until both lists are processed and no carry remains
        while l1 or l2 or carry:
            # Get the current values from l1 and l2, defaulting to 0 if the list is exhausted
            val1 = l1.val if l1 else 0
            val2 = l2.val if l2 else 0

            # Calculate the total sum of the two digits and the carry
            total = val1 + val2 + carry
            carry = total // 10  # Carry for next digit
            digit = total % 10  # Get the last digit to store in the result

            # Create a new node with the digit and append it to the result list
            current.next = ListNode(digit)
            current = current.next

            # Move to the next nodes in the input lists
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None

        # Return the next node of dummy to skip the initial zero node
        return dummy.next


# @lc code=end
