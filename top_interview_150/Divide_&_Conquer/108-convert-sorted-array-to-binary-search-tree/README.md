# 108. Convert Sorted Array to Binary Search Tree - Solution Explanation

## Problem Overview
Convert a sorted array into a **height-balanced Binary Search Tree (BST)**.

**Input Example:**
```
nums = [-10, -3, 0, 5, 9]
```

**Output Example (BST Structure):**
```
      0
     / \
   -3   9
   /   /
 -10  5
```

**Array Representation:** `[0,-3,9,-10,null,5]` (LeetCode format)

## Understanding Height-Balanced BST

### Binary Search Tree (BST) Properties
- **Left child < Parent node < Right child**
- Inorder traversal produces sorted sequence

### Height-Balanced Definition
**Definition**: For every node, the height difference between left and right subtrees is at most 1

**Visual Understanding:**
```
✅ Balanced BST (height difference ≤ 1)
      4
     / \
    2   6
   / \ / \
  1  3 5  7
Height: 3

❌ Unbalanced BST (height difference > 1)
  1
   \
    2
     \
      3
       \
        4
Height: 4 (linear)
```

**Advantages of Balanced BST:**
- **Search time**: O(log n) - efficient
- **Insert/Delete time**: O(log n) - efficient

**Problems with Unbalanced BST:**
- **Search time**: O(n) - same as linear list
- **Insert/Delete time**: O(n) - inefficient

## Algorithm: Divide and Conquer

**Core Idea:**
1. **Choose middle element as root** → Guarantees BST property
2. **Left half becomes left subtree** → Recursively construct
3. **Right half becomes right subtree** → Recursively construct
4. **Middle selection** → Automatically ensures balance

## Step-by-Step Solution Breakdown

### Step 1: Understanding Overall Structure

```python
def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
    def build_tree(left_index, right_index):
        # Recursively build BST
        pass
    
    # Start with entire array
    return build_tree(0, len(nums) - 1)
```

### Step 2: Detailed Python Syntax Explanation

#### 2-1. Middle Index Calculation
```python
mid_index = (left_index + right_index) // 2
```

**`//` Operator Details:**
```python
# // is "floor division" (integer division)
print(7 // 2)   # Result: 3 (3.5 rounded down)
print(6 // 2)   # Result: 3 (exact division)
print(8 // 2)   # Result: 4

# Difference from /
print(7 / 2)    # Result: 3.5 (floating point)
print(7 // 2)   # Result: 3 (integer)
```

**Middle Selection Examples:**
```python
# Array [-10, -3, 0, 5, 9] (indices 0-4)
left_index = 0, right_index = 4
mid_index = (0 + 4) // 2 = 2  # Index 2 = value 0

# Array [-10, -3] (indices 0-1)  
left_index = 0, right_index = 1
mid_index = (0 + 1) // 2 = 0  # Index 0 = value -10
```

#### 2-2. Node Creation
```python
root = TreeNode(nums[mid_index])
```

**Understanding TreeNode Class:**
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val      # Node value
        self.left = left    # Left child node
        self.right = right  # Right child node

# Usage example
root = TreeNode(0)  # Create node with value 0
# At this point: root.val = 0, root.left = None, root.right = None
```

#### 2-3. Recursive Left Subtree Construction
```python
root.left = build_tree(left_index, mid_index - 1)
```

**What happens:**
```python
# Original array: [-10, -3, 0, 5, 9]
# Current: left_index=0, right_index=4, mid_index=2

# Left subtree range: indices 0 to 1 (values: [-10, -3])
root.left = build_tree(0, 2-1)  # build_tree(0, 1)

# This recursive call builds left subtree from left half of array
```

#### 2-4. Recursive Right Subtree Construction
```python
root.right = build_tree(mid_index + 1, right_index)
```

**What happens:**
```python
# Right subtree range: indices 3 to 4 (values: [5, 9])
root.right = build_tree(2+1, 4)  # build_tree(3, 4)

# This recursive call builds right subtree from right half of array
```

### Step 3: Complete Execution Example

**Input Array**: `nums = [-10, -3, 0, 5, 9]`

#### Level 1: Root Node Creation
```python
# build_tree(0, 4)
left_index = 0, right_index = 4
mid_index = (0 + 4) // 2 = 2
root = TreeNode(nums[2])  # TreeNode(0)

# Current state:
#   0
```

#### Level 2: Left and Right Child Creation
```python
# Left subtree: build_tree(0, 1) for [-10, -3]
left_index = 0, right_index = 1
mid_index = (0 + 1) // 2 = 0
left_child = TreeNode(nums[0])  # TreeNode(-10)

# Right subtree: build_tree(3, 4) for [5, 9]
left_index = 3, right_index = 4  
mid_index = (3 + 4) // 2 = 3
right_child = TreeNode(nums[3])  # TreeNode(5)

# Current state:
#     0
#   /   \
# -10    5
```

#### Level 3: Further Child Node Creation
```python
# -10's right child: build_tree(1, 1) for [-3]
mid_index = 1
TreeNode(-3)

# 5's right child: build_tree(4, 4) for [9]  
mid_index = 4
TreeNode(9)

# Final state:
#     0
#   /   \
# -10    5
#   \     \
#   -3     9
```

### Step 4: Recursive Base Case

```python
if left_index > right_index:
    return None
```

**Why this condition is necessary:**
```python
# Example: When trying to create left child of -3 node
# build_tree(1, 0)  # left_index > right_index
# This range is invalid → return None → no left child
```

## Detailed Recursion Trace

### Complete Call Tree
```
build_tree(0, 4)  # [-10, -3, 0, 5, 9]
├── root = TreeNode(0)
├── root.left = build_tree(0, 1)  # [-10, -3]
│   ├── root = TreeNode(-10)
│   ├── root.left = build_tree(0, -1) → None
│   └── root.right = build_tree(1, 1)  # [-3]
│       ├── root = TreeNode(-3)
│       ├── root.left = build_tree(1, 0) → None
│       └── root.right = build_tree(2, 1) → None
└── root.right = build_tree(3, 4)  # [5, 9]
    ├── root = TreeNode(5)
    ├── root.left = build_tree(3, 2) → None
    └── root.right = build_tree(4, 4)  # [9]
        ├── root = TreeNode(9)
        ├── root.left = build_tree(4, 3) → None
        └── root.right = build_tree(5, 4) → None
```

### Construction Process Visualization
```
Step 1: Root node
  0

Step 2: Left and right children
    0
   / \
 -10  5

Step 3: Grandchildren
     0
   /   \
 -10    5
   \     \
   -3     9

Final BST:
     0
   /   \
 -10    5
   \     \
   -3     9
```

## Why This Algorithm Produces Balanced BST

### Mathematical Explanation
1. **Middle element selection**: Left and right parts have approximately equal number of elements
2. **Recursive application**: Same property applies to each subtree
3. **Height difference guarantee**: Always `|left_height - right_height| ≤ 1`

### Verification with Concrete Example
```
Array: [-10, -3, 0, 5, 9] (5 elements)

Root node 0:
- Left subtree: [-10, -3] (2 elements) → height 2
- Right subtree: [5, 9] (2 elements) → height 2
- Height difference: |2 - 2| = 0 ≤ 1 ✅

Node -10:
- Left subtree: none → height 0
- Right subtree: [-3] (1 element) → height 1
- Height difference: |0 - 1| = 1 ≤ 1 ✅
```

## Time & Space Complexity

### Time Complexity: O(n)
```python
# Each node is created exactly once
# n nodes → O(n) time
```

### Space Complexity: O(log n)
```python
# Recursion stack depth = tree height
# Balanced BST → height = O(log n)
```

## Edge Cases Handling

### Single Element Array
```python
nums = [1]
# build_tree(0, 0)
# mid_index = 0
# root = TreeNode(1)
# left = build_tree(0, -1) → None
# right = build_tree(1, 0) → None
# Result: single node
```

### Two Element Array
```python
nums = [1, 2]
# build_tree(0, 1)
# mid_index = 0
# root = TreeNode(1)
# left = build_tree(0, -1) → None  
# right = build_tree(1, 1) → TreeNode(2)
# Result:
#   1
#    \
#     2
```

### Empty Array
```python
nums = []
# build_tree(0, -1)
# left_index > right_index → None
```

## LeetCode Multiple Solutions

### Understanding Array Representation
LeetCode uses **level-order traversal** array representation:

```
Tree:        Array representation:
     0       [0, -10, 5, null, -3, null, 9]
   /   \      ↑   ↑   ↑    ↑    ↑    ↑    ↑
 -10    5     0   1   2    3    4    5    6
   \     \
   -3     9
```

**Index relationship:**
- `index 0`: root = 0
- `index 1`: left child of 0 = -10
- `index 2`: right child of 0 = 5
- `index 3`: left child of -10 = null
- `index 4`: right child of -10 = -3
- `index 5`: left child of 5 = null
- `index 6`: right child of 5 = 9

### Multiple Valid Solutions
```
Problem statement:
Input: nums = [-10,-3,0,5,9]
Output: [0,-3,9,-10,null,5]
Explanation: [0,-10,5,null,-3,null,9] is also accepted:
```

**Your implementation** produces: `[0,-10,5,null,-3,null,9]` ✅ **"also accepted"**
**LeetCode example** shows: `[0,-3,9,-10,null,5]` ✅ **another valid solution**

Both are correct height-balanced BSTs!

### Why Multiple Solutions Exist
Different middle selection strategies produce different valid BSTs:

```python
# Strategy 1: Left-biased middle (your code)
mid_index = (left + right) // 2

# Strategy 2: Right-biased middle (possible LeetCode approach)
mid_index = (left + right + 1) // 2

# Both produce valid height-balanced BSTs
```

## Alternative Approaches Comparison

### Approach 1: List Slicing
```python
def sortedArrayToBST(self, nums):
    if not nums:
        return None
    
    mid = len(nums) // 2
    root = TreeNode(nums[mid])
    root.left = self.sortedArrayToBST(nums[:mid])
    root.right = self.sortedArrayToBST(nums[mid+1:])
    return root
```
**Problem**: List slicing takes O(n) time → Overall O(n log n)

### Approach 2: Different Middle Selection
```python
mid_index = (left_index + right_index + 1) // 2
```
**Result**: Different but valid BST

### Current Solution Advantages
- ✅ **Efficiency**: O(n) time
- ✅ **Memory efficient**: Uses indices only
- ✅ **Stability**: Always produces balanced BST

## Practical Debugging Methods

### BST Validation
```python
def is_valid_bst(root, min_val=float('-inf'), max_val=float('inf')):
    if not root:
        return True
    
    if root.val <= min_val or root.val >= max_val:
        return False
        
    return (is_valid_bst(root.left, min_val, root.val) and 
            is_valid_bst(root.right, root.val, max_val))
```

### Balance Validation
```python
def is_balanced(root):
    def height(node):
        if not node:
            return 0
        
        left_height = height(node.left)
        right_height = height(node.right)
        
        if left_height == -1 or right_height == -1:
            return -1
        
        if abs(left_height - right_height) > 1:
            return -1
            
        return max(left_height, right_height) + 1
    
    return height(root) != -1
```

### Tree to Array Conversion
```python
def tree_to_array(root):
    if not root:
        return []
    
    result = []
    queue = [root]
    
    while queue:
        node = queue.pop(0)
        if node:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            result.append(None)
    
    # Remove trailing None values
    while result and result[-1] is None:
        result.pop()
    
    return result
```

## Real-World Applications

1. **Database Indexing**: B-tree structures
2. **Search Systems**: Efficient range queries
3. **Game Development**: Score ranking systems
4. **File Systems**: Directory structure optimization
5. **Compilers**: Syntax tree construction

This algorithm demonstrates a classic example of divide-and-conquer methodology and serves as a fundamental concept in efficient data structure design.

## Key Takeaways

1. **Your implementation is completely correct** ✅
2. **Multiple valid solutions exist** for height-balanced BST construction
3. **LeetCode accepts all valid solutions**, not just the one shown in examples
4. **Divide-and-conquer** approach ensures both efficiency and balance
5. **Understanding tree-to-array conversion** helps with LeetCode format comprehension