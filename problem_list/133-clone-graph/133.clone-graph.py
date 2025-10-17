#
# @lc app=leetcode id=133 lang=python3
#
# [133] Clone Graph
#

# @lc code=start
"""
# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
"""

from typing import Optional


class Solution:
    def cloneGraph(self, node: Optional["Node"]) -> Optional["Node"]:

        # A hash map to store the mapping from old nodes to their new copies.
        # This also acts as our "visited" set.
        old_to_new = {}

        def dfs_clone(original_node):
            # If we have already created a copy of this node, return it.
            # This is the base case for our recursion and handles cycles.
            if original_node in old_to_new:
                return old_to_new[original_node]

            # If not, create a new copy.
            copy_node = Node(original_node.val)
            # Add the new copy to our map. This must be done before the
            # recursive calls to prevent infinite loops in a cycle.
            old_to_new[original_node] = copy_node

            # Now, recursively clone all of its neighbors.
            for neighbor in original_node.neighbors:
                copy_node.neighbors.append(dfs_clone(neighbor))

            return copy_node

        # Handle the edge case of an empty graph.
        if not node:
            return None

        # Start the recursive cloning process from the given starting node.
        return dfs_clone(node)


# @lc code=end
