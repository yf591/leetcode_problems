#
# @lc app=leetcode id=146 lang=python3
#
# [146] LRU Cache
#


# @lc code=start


# First, define the Node for our Doubly Linked List
class Node:
    def __init__(self, key, val):
        self.key, self.val = key, val
        self.prev = self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = {}  # The hash map: key -> Node

        # Dummy nodes for the ends of the linked list
        # self.left is the LRU side, self.right is the MRU side
        self.left, self.right = Node(0, 0), Node(0, 0)
        self.left.next, self.right.prev = self.right, self.left

    # Helper function to remove a node from the list
    def _remove(self, node: Node):
        prev_node, next_node = node.prev, node.next
        prev_node.next, next_node.prev = next_node, prev_node

    # Helper function to insert a node at the right (most recent) end
    def _insert(self, node: Node):
        prev_node, next_node = self.right.prev, self.right
        prev_node.next = next_node.prev = node
        node.next, node.prev = next_node, prev_node

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            # Move the accessed node to the most recently used position
            self._remove(node)
            self._insert(node)
            return node.val
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # If key exists, just update the value and move it to the MRU position
            node = self.cache[key]
            node.val = value
            self._remove(node)
            self._insert(node)
        else:
            # If the key is new, create a new node and add it
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._insert(new_node)

            # If we've exceeded capacity, evict the LRU item
            if len(self.cache) > self.cap:
                # The LRU item is always the one at the left end of the list
                lru_node = self.left.next
                self._remove(lru_node)
                del self.cache[lru_node.key]


# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
# @lc code=end
