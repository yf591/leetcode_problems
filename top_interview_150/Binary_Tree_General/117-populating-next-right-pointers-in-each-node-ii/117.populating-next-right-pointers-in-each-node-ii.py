#
# @lc app=leetcode id=117 lang=python3
#
# [117] Populating Next Right Pointers in Each Node II
#

# @lc code=start
"""
# Definition for a Node.
class Node:
    def __init__(self, val: int = 0, left: 'Node' = None, right: 'Node' = None, next: 'Node' = None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next
"""


class Solution:
    def connect(self, root: "Node") -> "Node":
        if not root:
            return None

        # 'level_start' is the first node of the current level we are on.
        level_start = root

        # This outer loop moves us from one level to the next.
        while level_start:
            # 'dummy_head' is a placeholder for the start of the next level.
            # 'tail' is our "builder" pointer for the next level's connections.
            dummy_head = Node(0)
            tail = dummy_head

            # 'current' traverses the current level using the .next pointers.
            current = level_start

            # This inner loop processes the current level to build the next level.
            while current:
                # If the current node has a left child, link it.
                if current.left:
                    tail.next = current.left
                    tail = tail.next

                # If the current node has a right child, link it.
                if current.right:
                    tail.next = current.right
                    tail = tail.next

                # Move to the next node on the same level.
                current = current.next

            # Move to the start of the next level that we just built.
            level_start = dummy_head.next

        return root


# @lc code=end
