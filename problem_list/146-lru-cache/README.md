# 146\. LRU Cache - Solution Explanation

## Problem Overview

The task is to design and implement a **Least Recently Used (LRU) Cache**. This is a data structure that stores key-value pairs up to a certain `capacity`.

**The Core Rules:**

1.  **`get(key)`**: If the key exists in the cache, retrieve its value. This action should also mark the key as **recently used**.
2.  **`put(key, value)`**:
      - If the key already exists, update its value. This action also marks the key as **recently used**.
      - If the key is new, insert the key-value pair.
      - If inserting a new key causes the cache to exceed its `capacity`, the **least recently used (LRU)** item must be removed (evicted) before the new item is inserted.

**The Crucial Constraint:**

  - Both the `get` and `put` operations must run in **O(1) average time complexity**.

**Example:**

```
lRUCache = new LRUCache(2); // Create a cache with capacity 2
lRUCache.put(1, 1); // cache is {1=1}
lRUCache.put(2, 2); // cache is {1=1, 2=2}
lRUCache.get(1);    // return 1. Key 1 is now the most recently used. cache is {2=2, 1=1}
lRUCache.put(3, 3); // LRU key was 2, so evict 2. cache is {1=1, 3=3}
lRUCache.get(2);    // return -1 (not found)
```

## Key Insights

### The O(1) Time Complexity Challenge

This is the heart of the problem. Let's analyze what we need:

  - **For `get` and `put` lookups**: We need to find a key in O(1) time. This immediately suggests a **Hash Map** (a `dict` in Python).
  - **For "Recently Used" ordering**: We need a way to track the order of usage. When an item is accessed (`get` or `put`), it becomes the "most recently used." When the cache is full, we must evict the "least recently used." This implies an ordered data structure.

### Why Standard Structures Fail on Their Own

  - **Hash Map (`dict`)**: Perfect for O(1) lookups, but it has no inherent order. There's no O(1) way to know which item was least recently used.
  - **List or Array**: Good for order, but bad for O(1) operations. Finding an item is O(n). Moving an item from the middle to the end (to mark it as most recent) is also O(n).
  - **Queue (`deque`)**: Good for adding to the end and removing from the front in O(1). However, if you access an item in the *middle* of the queue, moving it to the end is an O(n) operation.

### The Hybrid Solution: Hash Map + Doubly Linked List

The optimal solution is to combine two data structures, leveraging the strengths of each:

1.  A **Hash Map** (`dict`): This will store key-to-node mappings (`{key: Node}`). This gives us the O(1) lookup we need. We can instantly find any node in our list.
2.  A **Doubly Linked List (DLL)**: This will store the actual key-value data, ordered by usage. A DLL is perfect because we can add or remove any node in O(1) time **if we have a direct pointer to it**.
      - We'll maintain the list such that the **most recently used (MRU)** item is at one end (e.g., the right/tail).
      - The **least recently used (LRU)** item is at the other end (e.g., the left/head).

When `get(key)` is called, we use the hash map to find the node in O(1), then move that node to the MRU end of the DLL in O(1). When we need to evict, we just remove the node at the LRU end in O(1).

## Solution Approach

This solution implements the Hash Map + Doubly Linked List strategy. We define a simple `Node` class for our list. To make adding/removing from the ends easier and avoid edge cases, we use two dummy nodes, `left` (for the LRU side) and `right` (for the MRU side), which act as sentinels.

```python
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
            # Move to MRU: remove from current position and re-insert at the right.
            self._remove(node)
            self._insert(node)
            return node.val
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # If key exists, update its value and move it to the MRU position.
            node = self.cache[key]
            node.val = value
            self._remove(node)
            self._insert(node)
        else:
            # If the key is new, create a new node and add it.
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._insert(new_node)

            # If we've exceeded capacity, evict the LRU item.
            if len(self.cache) > self.cap:
                lru_node = self.left.next
                self._remove(lru_node)
                del self.cache[lru_node.key]
```

## Detailed Code Analysis

### `__init__(self, capacity: int)`

```python
self.cap = capacity
self.cache = {}
self.left, self.right = Node(0, 0), Node(0, 0)
self.left.next, self.right.prev = self.right, self.left
```

  - We store the `capacity`.
  - We initialize the `cache` hash map.
  - We create two dummy nodes, `left` and `right`. These act as fixed start and end points for our DLL. We link them together to form an empty list: `left <-> right`. `left` will always be just before the LRU node, and `right` will be just after the MRU node.

### Helper: `_remove(self, node: Node)`

```python
prev_node, next_node = node.prev, node.next
prev_node.next, next_node.prev = next_node, prev_node
```

  - This is the core pointer manipulation for removal. To remove a `node`, we get its `prev` and `next` neighbors. We then "skip over" the `node` by linking its neighbors directly to each other. This is an O(1) operation.

### Helper: `_insert(self, node: Node)`

```python
prev_node, next_node = self.right.prev, self.right
prev_node.next = next_node.prev = node
node.next, node.prev = next_node, prev_node
```

  - This function always inserts a `node` at the very end of the list, just before the `right` dummy node, making it the new MRU item. This is also an O(1) operation.

### `get(self, key: int)`

```python
if key in self.cache:
    node = self.cache[key]
    self._remove(node)
    self._insert(node)
    return node.val
return -1
```

  - We use the hash map for an O(1) lookup. If the key doesn't exist, we return -1.
  - If it exists, we have our `node`. Accessing an item makes it the most recently used. We achieve this by **moving it to the MRU end of the list**.
  - `_remove(node)`: Unlink it from its current position.
  - `_insert(node)`: Re-link it at the MRU end.
  - Both helpers are O(1), so the whole `get` operation is O(1).

### `put(self, key: int, value: int)`

This method handles two main cases.

  - **Case 1: Key already exists.**
    ```python
    if key in self.cache:
        node = self.cache[key]
        node.val = value
        self._remove(node)
        self._insert(node)
    ```
      - We find the node, update its `value`, and move it to the MRU end just like in the `get` method.
  - **Case 2: Key is new.**
    ```python
    else:
        new_node = Node(key, value)
        self.cache[key] = new_node
        self._insert(new_node)
    ```
      - We create a `new_node`, add it to our `cache` map, and `_insert` it at the MRU end of our DLL.

      - **The Eviction Sub-Case:**

        ```python
        if len(self.cache) > self.cap:
            lru_node = self.left.next
            self._remove(lru_node)
            del self.cache[lru_node.key]
        ```

          - After adding a new node, we check if we've gone over capacity.
          - If so, we need to evict the LRU item. Because of our structure, the LRU item is **always** the node right after our `left` dummy node.
          - We get a reference to it (`lru_node = self.left.next`).
          - We `_remove` it from the DLL.
          - Crucially, we also `del` it from our `cache` hash map to complete the eviction.

## Step-by-Step Execution Trace

Let's trace the example `capacity = 2`. `L` and `R` are the dummy nodes.

| Operation | `cache` (map) State | DLL State (`L <-> ... <-> R`) | Explanation |
| :--- | :--- | :--- | :--- |
| **`__init__(2)`** | `{}` | `L <-> R` | Initialize with capacity 2. |
| **`put(1, 1)`** | `{1: Node(1)}` | `L <-> 1 <-> R` | New key. Insert `Node(1)` at MRU end. |
| **`put(2, 2)`** | `{1:N(1), 2:N(2)}` | `L <-> 1 <-> 2 <-> R` | New key. Insert `Node(2)` at MRU end. |
| **`get(1)`** | `{1:N(1), 2:N(2)}` | `L <-> 2 <-> 1 <-> R` | Key 1 found. Remove it from its spot and re-insert at MRU end. Returns 1. |
| **`put(3, 3)`** | `{1:N(1), 2:N(2), 3:N(3)}`| `L <-> 2 <-> 1 <-> 3 <-> R`| New key. Insert `Node(3)`. Cache size is now 3 (\> 2). |
| | | | **Eviction\!** LRU node is `L.next` (`Node(2)`). |
| | `{1:N(1), 3:N(3)}` | `L <-> 1 <-> 3 <-> R` | Remove `Node(2)` from DLL. Delete key 2 from `cache`. |
| **`get(2)`** | `{1:N(1), 3:N(3)}` | `L <-> 1 <-> 3 <-> R` | Key 2 not in `cache`. Returns -1. |

## Performance Analysis

### Time Complexity: O(1) for both `get` and `put`

  - All operations are a fixed sequence of hash map lookups/insertions/deletions (O(1) average) and doubly linked list pointer manipulations (O(1) direct access).

### Space Complexity: O(capacity)

  - The space is used by the hash map and the doubly linked list, both of which will store up to `capacity` items. The space required is proportional to the cache's capacity.