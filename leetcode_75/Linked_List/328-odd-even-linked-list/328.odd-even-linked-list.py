#
# @lc app=leetcode id=328 lang=python3
#
# [328] Odd Even Linked List
#


# @lc code=start
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def oddEvenList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # Handle edge cases: if the list has 0, 1, or 2 nodes,
        # it is already correctly ordered.
        if not head or not head.next or not head.next.next:
            return head

        # 'odd_tail' will track the end of the odd-indexed list.
        odd_tail = head
        # 'even_tail' will track the end of the even-indexed list.
        # We also need to save the head of the even list to link it later.
        even_head = head.next
        even_tail = head.next

        # Loop as long as there is an even node to process and an odd node after it.
        while even_tail and even_tail.next:
            # 1. Link the next odd node (even_tail.next) to the odd chain.
            odd_tail.next = even_tail.next

            # 2. Advance the odd_tail pointer to this new node.
            odd_tail = odd_tail.next

            # 3. Link the next even node (which is now odd_tail.next) to the even chain.
            even_tail.next = odd_tail.next

            # 4. Advance the even_tail pointer.
            even_tail = even_tail.next

        # 5. After the loop, connect the end of the odd list to the head of the even list.
        odd_tail.next = even_head

        return head


# @lc code=end
