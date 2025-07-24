# 21. Merge Two Sorted Lists - Solution Explanation

## Problem Overview
Merge two sorted linked lists and return it as a new sorted list. The new list should be made by splicing together the nodes of the first two lists.

**Examples:**
- `list1 = [1,2,4]`, `list2 = [1,3,4]` → `[1,1,2,3,4,4]`
- `list1 = []`, `list2 = [0]` → `[0]`
- `list1 = []`, `list2 = []` → `[]`

## Understanding Linked Lists

A **Linked List** is like a chain of connected nodes, where each node contains data and a reference to the next node:

```
Node 1      Node 2      Node 3
┌─────┐    ┌─────┐    ┌─────┐
│val=1│───→│val=3│───→│val=5│───→ None
│next │    │next │    │next │
└─────┘    └─────┘    └─────┘
```

### ListNode Class Structure
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val    # The value stored in this node
        self.next = next  # Reference to the next node (or None)
```

## Visual Problem Example

**Input:**
```
list1: 1 → 3 → 5 → None
list2: 2 → 4 → 6 → None
```

**Goal:**
```
result: 1 → 2 → 3 → 4 → 5 → 6 → None
```

## Step-by-Step Algorithm Breakdown

### Step 1: Create Dummy Node
```python
dummy = ListNode()
current = dummy
```

**Why use a dummy node?**
- Simplifies edge cases (empty lists)
- Provides a consistent starting point for building the result
- Eliminates special handling for the first node

**Visualization:**
```
dummy (placeholder)
┌─────┐
│ ??? │───→ This is where we'll build our result
│next │
└─────┘
  ↑
current
```

### Step 2: Compare and Merge Loop
```python
while list1 and list2:
```

**Condition**: Continue while both lists have remaining nodes
- `list1` is not `None` AND `list2` is not `None`

### Step 3: Compare Values and Choose Smaller
```python
if list1.val < list2.val:
    current.next = list1    # Attach list1's node to result
    list1 = list1.next      # Move list1 pointer forward
else:
    current.next = list2    # Attach list2's node to result
    list2 = list2.next      # Move list2 pointer forward
```

**Key Insight**: We're **reusing existing nodes**, not creating new ones!

### Step 4: Advance Result Pointer
```python
current = current.next
```

**Purpose**: Move to the end of our result list for the next attachment

### Step 5: Handle Remaining Nodes
```python
if list1:
    current.next = list1
elif list2:
    current.next = list2
```

**Why needed?**: When the loop ends, one list might still have remaining nodes

### Step 6: Return Result
```python
return dummy.next
```

**Why `dummy.next`?**: The actual result starts after our dummy placeholder

## Detailed Example Walkthrough

**Input:** `list1 = [1,3,5]`, `list2 = [2,4,6]`

### Initial State
```
list1: 1 → 3 → 5 → None
       ↑
     list1

list2: 2 → 4 → 6 → None  
       ↑
     list2

dummy: dummy
       ↑
    current
```

### Step 1: Compare 1 vs 2
```
1 < 2, so choose list1

list1: 1 → 3 → 5 → None
           ↑
         list1 (advanced)

list2: 2 → 4 → 6 → None  
       ↑
     list2

result: dummy → 1
                ↑
             current (advanced)
```

### Step 2: Compare 3 vs 2
```
3 > 2, so choose list2

list1: 1 → 3 → 5 → None
           ↑
         list1

list2: 2 → 4 → 6 → None  
           ↑
         list2 (advanced)

result: dummy → 1 → 2
                    ↑
                 current (advanced)
```

### Step 3: Compare 3 vs 4
```
3 < 4, so choose list1

list1: 1 → 3 → 5 → None
               ↑
             list1 (advanced)

list2: 2 → 4 → 6 → None  
           ↑
         list2

result: dummy → 1 → 2 → 3
                        ↑
                     current (advanced)
```

### Step 4: Compare 5 vs 4
```
5 > 4, so choose list2

list1: 1 → 3 → 5 → None
               ↑
             list1

list2: 2 → 4 → 6 → None  
               ↑
             list2 (advanced)

result: dummy → 1 → 2 → 3 → 4
                            ↑
                         current (advanced)
```

### Step 5: Compare 5 vs 6
```
5 < 6, so choose list1

list1: 1 → 3 → 5 → None
                   ↑
                 list1 (None)

list2: 2 → 4 → 6 → None  
               ↑
             list2

result: dummy → 1 → 2 → 3 → 4 → 5
                                ↑
                             current (advanced)
```

### Step 6: Handle Remaining Nodes
```
list1 is None, but list2 still has [6]
Attach remaining list2 to result

result: dummy → 1 → 2 → 3 → 4 → 5 → 6 → None
```

### Final Result
```
Return dummy.next = 1 → 2 → 3 → 4 → 5 → 6 → None
```

## Key Algorithm Insights

### 1. Pointer Manipulation vs Node Creation
```python
# ❌ Inefficient: Creating new nodes
new_node = ListNode(smaller_value)
current.next = new_node

# ✅ Efficient: Reusing existing nodes
current.next = smaller_node
```

### 2. Dummy Node Benefits
- **Simplifies code**: No special case for first node
- **Handles edge cases**: Works seamlessly with empty lists
- **Consistent pattern**: Always use `current.next` for attachment

### 3. Two-Pointer Technique
- `list1` and `list2`: Track current position in input lists
- `current`: Track current position in result list
- All three move independently based on algorithm logic

## Alternative Approaches

### Approach 1: Recursive Solution
```python
def mergeTwoLists(self, list1, list2):
    # Base cases
    if not list1:
        return list2
    if not list2:
        return list1
    
    # Choose smaller and recurse
    if list1.val < list2.val:
        list1.next = self.mergeTwoLists(list1.next, list2)
        return list1
    else:
        list2.next = self.mergeTwoLists(list1, list2.next)
        return list2
```

**Pros**: Elegant and concise
**Cons**: O(m+n) space complexity due to recursion stack

### Approach 2: Create New Nodes
```python
def mergeTwoLists(self, list1, list2):
    dummy = ListNode()
    current = dummy
    
    while list1 and list2:
        if list1.val < list2.val:
            current.next = ListNode(list1.val)  # Create new node
            list1 = list1.next
        else:
            current.next = ListNode(list2.val)  # Create new node
            list2 = list2.next
        current = current.next
    
    # Handle remaining nodes...
```

**Pros**: Doesn't modify original lists
**Cons**: Uses extra memory for new nodes

## Time & Space Complexity Analysis

### Current Solution (Iterative with Node Reuse)
- **Time Complexity**: **O(m + n)** where m, n are lengths of the two lists
  - Each node is visited exactly once
  - Comparison and pointer operations are O(1)

- **Space Complexity**: **O(1)** - constant extra space
  - Only uses a few pointer variables
  - Reuses existing nodes instead of creating new ones

### Comparison with Alternatives
| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Iterative (current) | O(m+n) | O(1) | Most efficient |
| Recursive | O(m+n) | O(m+n) | Elegant but uses call stack |
| New nodes | O(m+n) | O(m+n) | Preserves original lists |

## Edge Cases Handled

### Empty Lists
```python
list1 = None, list2 = [1,2,3]
# Result: [1,2,3] (list2 is attached directly)

list1 = [1,2,3], list2 = None  
# Result: [1,2,3] (list1 is attached directly)

list1 = None, list2 = None
# Result: None (dummy.next is None)
```

### Single Node Lists
```python
list1 = [1], list2 = [2]
# Result: [1,2]

list1 = [2], list2 = [1]  
# Result: [1,2]
```

### Lists of Different Lengths
```python
list1 = [1], list2 = [2,3,4,5]
# After 1 vs 2 comparison, list1 becomes None
# Remaining [2,3,4,5] is attached directly
# Result: [1,2,3,4,5]
```

## Common Pitfalls and Tips

### 1. Forgetting to Handle Remaining Nodes
```python
# ❌ Incomplete - missing remaining nodes
while list1 and list2:
    # merge logic...
# What about leftover nodes?

# ✅ Complete
while list1 and list2:
    # merge logic...
if list1:
    current.next = list1
elif list2:
    current.next = list2
```

### 2. Returning Wrong Node
```python
# ❌ Wrong - returns dummy node
return dummy

# ✅ Correct - returns actual result
return dummy.next
```

### 3. Not Advancing Pointers
```python
# ❌ Infinite loop - forgot to advance current
current.next = smaller_node
# current = current.next  # Missing this line!

# ✅ Correct
current.next = smaller_node
current = current.next  # Always advance current
```

## Key Programming Concepts Demonstrated

1. **Linked List Manipulation**: Understanding node references and pointer operations
2. **Two-Pointer Technique**: Managing multiple pointers simultaneously
3. **Dummy Node Pattern**: Simplifying edge case handling
4. **Iterative Merging**: Combining sorted sequences efficiently
5. **Memory Efficiency**: Reusing existing structures vs creating new ones

## Practice Tips

1. **Draw it out**: Visualize the pointer movements step by step
2. **Trace examples**: Walk through small examples manually
3. **Handle edge cases**: Always consider empty lists and single nodes
4. **Check pointer updates**: Ensure all pointers advance correctly
5. **Verify result**: Make sure `dummy.next` gives the correct starting point

This algorithm demonstrates a fundamental technique for merging sorted data structures efficiently while maintaining the sorted property throughout the process.