# 103\. Binary Tree Zigzag Level Order Traversal - Solution Explanation

## Problem Overview

You are given the `root` of a binary tree. The task is to return a **zigzag level order traversal** of its nodes' values.

**Zigzag Traversal Definition:**
This means visiting the nodes level by level, but alternating the direction of traversal for each level.

  - Level 0: Traversed from left to right.
  - Level 1: Traversed from right to left.
  - Level 2: Traversed from left to right.
  - ...and so on.

The final output should be a list of lists, where each inner list contains the node values for one level, ordered according to the zigzag pattern.

**Example:**

```python
Input: root = [3,9,20,null,null,15,7]
Output: [[3],[20,9],[15,7]]
Explanation:
- Level 0: [3] (left to right)
- Level 1: [9, 20]. We need right to left, so: [20, 9]
- Level 2: [15, 7] (left to right)
```

## Key Insights

### Building on Standard Level-Order Traversal

The core of this problem is still a **level-by-level** traversal. This is a massive clue that the fundamental algorithm we need is **Breadth-First Search (BFS)**, which naturally explores a tree in layers. The zigzag requirement is just an extra twist we need to apply on top of the standard BFS logic.

### The Simple "Collect then Reverse" Strategy

We don't need a complex traversal algorithm with two stacks or other complicated machinery. The simplest and cleanest insight is to:

1.  Perform a standard, left-to-right BFS to collect all the node values for a given level into a temporary list.
2.  Keep track of which level we are on (e.g., an even or odd level number).
3.  **After** collecting the nodes for a level, decide if that level's list needs to be reversed based on whether it's an odd or even level.
4.  Add the (possibly reversed) list to our final result.

This separates the traversal logic from the ordering logic, making the code much easier to understand and write.

## Solution Approach

This solution implements a standard BFS using a queue. A boolean flag, `left_to_right`, is used to keep track of the required ordering for the current level. After each level is processed, its temporary list is reversed if the flag indicates a right-to-left traversal.

```python
import collections
from typing import Optional, List

class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []

        result = []
        queue = collections.deque([root])
        # A flag to track the traversal direction for the current level.
        left_to_right = True

        # Loop as long as there are levels (nodes in the queue) to process.
        while queue:
            level_size = len(queue)
            current_level = []

            # Perform a standard left-to-right collection for this level.
            for _ in range(level_size):
                node = queue.popleft()
                current_level.append(node.val)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            
            # Apply the zigzag logic.
            if not left_to_right:
                current_level.reverse()
            
            result.append(current_level)
            
            # Flip the direction for the next level.
            left_to_right = not left_to_right
            
        return result
```

## Detailed Code Analysis

### Step 1: Initialization

```python
if not root:
    return []
result = []
queue = collections.deque([root])
left_to_right = True
```

  - **Edge Case**: We handle an empty tree.
  - **`result`**: The final list of lists.
  - **`queue`**: A `deque` for an efficient BFS, initialized with the root node.
  - **`left_to_right = True`**: A boolean flag to manage the state. We start with `True` because the first level (Level 0) is always left-to-right.

### Step 2: The Main (Level) Loop

```python
while queue:
```

  - This `while` loop is the main engine of the BFS. Each full iteration of this loop processes **one entire level**.

### Step 3: Standard Level Processing

```python
level_size = len(queue)
current_level = []
for _ in range(level_size):
    node = queue.popleft()
    current_level.append(node.val)
    if node.left:
        queue.append(node.left)
    if node.right:
        queue.append(node.right)
```

  - This is the standard, classic BFS pattern for level-order traversal.
  - `level_size = len(queue)`: We capture the number of nodes on the current level **before** the inner loop starts.
  - `current_level = []`: A temporary list to store the values for this level.
  - The `for` loop runs exactly `level_size` times, dequeueing each node from the current level and enqueueing its children for the next level. The values are always collected in a left-to-right order in `current_level`.

### Step 4: Applying the Zigzag Logic

```python
if not left_to_right:
    current_level.reverse()
result.append(current_level)
```

  - This is the simple but powerful step that handles the zigzag requirement.
  - `if not left_to_right:`: We check our direction flag. If it's `False`, it means this level should be ordered right-to-left.
  - `current_level.reverse()`: We perform an in-place reversal of the list of values we just collected.
  - `result.append(current_level)`: We add the correctly ordered level list to our final result.

### Step 5: Flipping the Direction

```python
left_to_right = not left_to_right
```

  - After processing a level, we flip the boolean flag. If it was `True`, it becomes `False`, and vice versa. This prepares the correct direction for the *next* iteration of the `while` loop.

## Step-by-Step Execution Trace

Let's trace the algorithm with `root = [3, 9, 20, null, null, 15, 7]` with extreme detail.

### **Initial State:**

  - `result = []`
  - `queue = deque([Node(3)])`
  - `left_to_right = True`

-----

### **Level 0 (First `while` loop iteration)**

1.  `level_size = 1`. `current_level = []`.
2.  Inner loop runs once:
      - `node = Node(3)` is dequeued.
      - `current_level` becomes `[3]`.
      - `Node(9)` and `Node(20)` are enqueued. `queue` is now `deque([Node(9), Node(20)])`.
3.  Check direction: `left_to_right` is `True`. No reversal needed.
4.  `result.append([3])`. `result` is now `[[3]]`.
5.  Flip direction: `left_to_right` becomes `False`.

-----

### **Level 1 (Second `while` loop iteration)**

1.  `level_size = 2`. `current_level = []`.
2.  Inner loop runs twice:
      - `node = Node(9)` is dequeued. `current_level` becomes `[9]`. No children.
      - `node = Node(20)` is dequeued. `current_level` becomes `[9, 20]`. `Node(15)` and `Node(7)` are enqueued.
3.  `queue` is now `deque([Node(15), Node(7)])`. `current_level` is `[9, 20]`.
4.  Check direction: `left_to_right` is **`False`**.
      - `current_level.reverse()`. `current_level` becomes `[20, 9]`.
5.  `result.append([20, 9])`. `result` is now `[[3], [20, 9]]`.
6.  Flip direction: `left_to_right` becomes `True`.

-----

### **Level 2 (Third `while` loop iteration)**

1.  `level_size = 2`. `current_level = []`.
2.  Inner loop runs twice:
      - `node = Node(15)` is dequeued. `current_level` becomes `[15]`. No children.
      - `node = Node(7)` is dequeued. `current_level` becomes `[15, 7]`. No children.
3.  `queue` is now empty. `current_level` is `[15, 7]`.
4.  Check direction: `left_to_right` is `True`. No reversal needed.
5.  `result.append([15, 7])`. `result` is now `[[3], [20, 9], [15, 7]]`.
6.  Flip direction: `left_to_right` becomes `False`.

-----

### **End of Traversal**

  - The `while queue:` condition is now **False**. The loop terminates.
  - The function returns the final `result`.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of nodes in the tree. Each node is enqueued and dequeued exactly once. The reversal operation on each level, when summed up across all levels, also takes `O(n)` time in total.

### Space Complexity: O(w)

  - Where `w` is the **maximum width** of the tree. This is the maximum number of nodes that can be in the `queue` at any one time. In the worst case (a full, complete binary tree), this can be `O(n)`.