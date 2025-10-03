#
# @lc app=leetcode id=138 lang=python3
#
# [138] Copy List with Random Pointer
#

# @lc code=start
"""
# Definition for a Node.
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random
"""


class Solution:
    def copyRandomList(self, head: "Optional[Node]") -> "Optional[Node]":

        # Edge case: If the head is null, return null.
        if not head:
            return None

        # --- Pass 1: Create a copy of each node and interweave them ---
        # Original: A -> B -> C
        # After:    A -> A' -> B -> B' -> C -> C'
        current = head
        while current:
            # Create a copy of the current node
            new_node = Node(current.val)
            # Link the new node to the rest of the original list
            new_node.next = current.next
            # Link the original node to its copy
            current.next = new_node
            # Move to the next original node
            current = new_node.next

        # --- Pass 2: Set the random pointers for the copied nodes ---
        current = head
        while current:
            # If the original node has a random pointer...
            if current.random:
                # ...the copied node's random pointer should point to the
                # copy of the original's random target. The copy is always
                # the .next of the original random target.
                current.next.random = current.random.next

            # Move to the next original node in the interwoven list
            current = current.next.next

        # --- Pass 3: Separate the original and copied lists ---
        dummy_head = Node(0)
        new_list_tail = dummy_head
        current = head

        while current:
            # Save the next original node
            next_original = current.next.next

            # Extract the copied node
            copied_node = current.next

            # Append the copied node to our new list
            new_list_tail.next = copied_node
            new_list_tail = new_list_tail.next

            # Restore the original list's next pointer
            current.next = next_original

            # Move to the next original node
            current = next_original

        return dummy_head.next


# @lc code=end
