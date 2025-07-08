class Solution:
    def addTwoNumbers(
        self, l1: Optional[ListNode], l2: Optional[ListNode]
    ) -> Optional[ListNode]:
        dummy = ListNode(0)  # Create dummy node as the starting point of result list
        current = dummy
        carry = 0  # Track carry-over value

        # Continue processing while l1, l2, or carry exists
        while l1 or l2 or carry:
            # Get current digit values (0 if node doesn't exist)
            val1 = l1.val if l1 else 0
            val2 = l2.val if l2 else 0

            # Calculate sum of current digits
            total = val1 + val2 + carry
            carry = total // 10  # Calculate new carry
            digit = total % 10  # Current digit value

            # Create new node and add to result list
            current.next = ListNode(digit)
            current = current.next

            # Move to next nodes (if they exist)
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None

        return dummy.next  # Return actual result starting from dummy's next
