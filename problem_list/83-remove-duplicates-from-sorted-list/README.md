# 83. Remove Duplicates from Sorted List - Solution Explanation

## Problem Overview

Given the `head` of a sorted linked list, delete all duplicates such that each element appears only once. Return the linked list sorted as well.

**Examples:**
```
Input:  1 → 1 → 2 → 3 → 3
Output: 1 → 2 → 3

Input:  1 → 1 → 2
Output: 1 → 2

Input:  1 → 2 → 3
Output: 1 → 2 → 3
```

**Constraints:**
- The number of nodes in the list is in the range `[0, 300]`
- `-100 <= Node.val <= 100`
- The list is guaranteed to be **sorted** in ascending order

## Key Insights

### Sorted List Property
```python
# Sorted = Duplicates are always adjacent
# Example: [1,1,1,2,2,3] → Same values are consecutive
# Therefore: current.val == current.next.val indicates a duplicate
```

### Linked List Deletion Principle
```python
# Node deletion = Pointer manipulation
# A → B → C  to remove B
# A.next = C  (skip B by pointing directly to C)
```

## Solution Approach

Our solution uses **in-place deletion** with a single traversal:

```python
def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
    # Use a 'current' pointer to traverse the list, starting at the head.
    current = head

    # We need to loop as long as 'current' and 'current.next' are valid nodes.
    while current and current.next:
        # Check if the next node is a duplicate of the current node.
        if current.val == current.next.val:
            # If it is a duplicate, we skip over the next node by
            # pointing the current node's 'next' to the one after the duplicate.
            current.next = current.next.next
        else:
            # If it's not a duplicate, we just move our pointer forward.
            current = current.next

    # Return the head of the modified list.
    return head
```

**Strategy:**
1. **Single traversal**: One pass through the list
2. **In-place deletion**: Modify original list without extra space
3. **Pointer manipulation**: Skip duplicate nodes by updating `next` pointers
4. **Safe traversal**: Check both current and next node validity

## Step-by-Step Breakdown

### Step 1: Initialize Traversal Pointer
```python
current = head
```

**Purpose**: Set up a working pointer for list traversal

**Key Point**: 
- `head` remains unchanged (needed for return value)
- `current` serves as our working pointer

### Step 2: Safe Loop Condition
```python
while current and current.next:
```

**Why Both Conditions Are Necessary:**

#### Condition Analysis
```python
# current: Check if current node exists
# current.next: Check if next node exists for comparison

# Both required because:
# 1. current == None → Reached end of list
# 2. current.next == None → No node to compare with (last node)
```

#### Concrete Examples
```python
# List: 1 → 2 → None
# current=1, current.next=2 → Continue ✓
# current=2, current.next=None → Stop ✗ (loop ends)

# Empty list: None
# current=None → Stop ✗ (loop never executes)
```

### Step 3: Duplicate Detection and Removal
```python
if current.val == current.next.val:
    current.next = current.next.next
else:
    current = current.next
```

#### Duplicate Removal Mechanism

**When Duplicate Found:**
```python
# Before: current → duplicate → after
#         [1]    →   [1]    →  [2]
current.next = current.next.next
# After:  current ────────────→ after  
#         [1]    ────────────→  [2]
#         Duplicate node becomes unreachable (garbage collected)
```

**When No Duplicate:**
```python
# Before: current → different
#         [1]    →   [2]
current = current.next
# After:          current
#         [1]    →   [2]
#         Move pointer to next node
```

## Detailed Execution Trace

### Example: [1, 1, 2, 3, 3]

#### Initial State
```python
List: 1 → 1 → 2 → 3 → 3 → None
current = Node(1)  # First node with value 1
```

#### Iteration 1
```python
current.val = 1, current.next.val = 1  # Duplicate found!
# Execute deletion:
current.next = current.next.next

# Before: 1 → 1 → 2 → 3 → 3 → None
#         ↑
#       current
# After:  1 ────→ 2 → 3 → 3 → None
#         ↑
#       current (stays in place!)
```

#### Iteration 2
```python
current.val = 1, current.next.val = 2  # No duplicate
# Move pointer:
current = current.next

# List:   1 ────→ 2 → 3 → 3 → None
#                 ↑
#               current
```

#### Iteration 3
```python
current.val = 2, current.next.val = 3  # No duplicate
# Move pointer:
current = current.next

# List:   1 ────→ 2 → 3 → 3 → None
#                      ↑
#                    current
```

#### Iteration 4
```python
current.val = 3, current.next.val = 3  # Duplicate found!
# Execute deletion:
current.next = current.next.next

# Before: 1 ────→ 2 → 3 → 3 → None
#                      ↑
#                    current
# After:  1 ────→ 2 → 3 ───→ None
#                      ↑
#                    current
```

#### Iteration 5
```python
current.val = 3, current.next = None  # Loop condition fails
# Loop terminates
```

#### Final Result
```python
Result: 1 → 2 → 3 → None
```

## Critical Design Decisions

### Why Don't We Move `current` When Deleting?

**Key Insight**: Handle consecutive duplicates correctly

```python
# Consecutive duplicates example: 1 → 1 → 1 → 2
# After 1st deletion: 1 ───→ 1 → 2

# If we moved current:
# current = current.next  # ← This would be wrong!
# We'd miss the remaining duplicate

# Correct approach:
# Keep current in same position to check remaining duplicates
```

#### Consecutive Duplicate Processing
```python
# Initial: 1 → 1 → 1 → 2
#          ↑
#        current

# Round 1: 1 ───→ 1 → 2  (Remove 1st duplicate)
#          ↑
#        current (don't move)

# Round 2: 1 ───────→ 2  (Remove 2nd duplicate)  
#          ↑
#        current (don't move)

# Round 3: current.val=1, current.next.val=2 (no duplicate)
#          current = current.next  (finally move)
```

### Loop Condition Sophistication

```python
while current and current.next:
```

**What This Condition Prevents:**

```python
# NullPointerException prevention:
# 1. If current is None, doesn't access current.next
# 2. If current.next is None, doesn't access current.next.val

# Unnecessary processing avoidance:
# Last node has no comparison target, so no processing needed
```

## Alternative Solutions Comparison

### Solution 1: Recursive Approach
```python
def deleteDuplicates(self, head):
    if not head or not head.next:
        return head
    
    head.next = self.deleteDuplicates(head.next)
    
    if head.val == head.next.val:
        return head.next
    else:
        return head
```

**Analysis:**
- ✅ **Elegant**: Functional programming style
- ✅ **Concise**: Fewer lines of code
- ❌ **Space overhead**: O(n) stack space for recursion
- ❌ **Complexity**: Harder to understand and debug

### Solution 2: Dummy Node Approach
```python
def deleteDuplicates(self, head):
    dummy = ListNode(0)
    dummy.next = head
    current = dummy
    
    while current.next and current.next.next:
        if current.next.val == current.next.next.val:
            val = current.next.val
            while current.next and current.next.val == val:
                current.next = current.next.next
        else:
            current = current.next
    
    return dummy.next
```

**Analysis:**
- ✅ **General pattern**: Useful for many linked list problems
- ✅ **Handles edge cases**: Systematic approach to boundary conditions
- ❌ **Over-engineering**: Unnecessary complexity for this problem
- ❌ **More code**: Additional complexity without benefit

### Solution 3: Create New List
```python
def deleteDuplicates(self, head):
    if not head:
        return head
    
    new_head = ListNode(head.val)
    current_new = new_head
    current_old = head.next
    
    while current_old:
        if current_old.val != current_new.val:
            current_new.next = ListNode(current_old.val)
            current_new = current_new.next
        current_old = current_old.next
    
    return new_head
```

**Analysis:**
- ✅ **Clear logic**: Doesn't modify original list
- ✅ **Easy to understand**: Straightforward approach
- ❌ **Space inefficient**: O(n) extra space
- ❌ **Unnecessary allocation**: Creates new nodes unnecessarily

## Why Our Solution is Optimal

### 1. **Optimal Time Complexity: O(n)**
```python
# Single pass through the list
# Each node visited at most once
# Deletion operations are O(1)
# Total: O(n) time
```

### 2. **Optimal Space Complexity: O(1)**
```python
# Only uses one pointer variable
# No additional data structures
# In-place modification
# Total: O(1) space
```

### 3. **Memory Efficiency**
```python
# In-place operation saves memory
# No unnecessary node creation
# Garbage collection handles deleted nodes automatically
```

### 4. **Simplicity and Clarity**
```python
# Straightforward logic flow
# Easy to understand and maintain
# Minimal code complexity
```

### 5. **Robust Edge Case Handling**
```python
# Empty list: Handled by loop condition
# Single node: Handled by loop condition  
# All duplicates: Correctly leaves one instance
# No duplicates: Preserves original list
```

## Performance Analysis

### Time Complexity: O(n)
```python
# n = number of nodes in the list
# Each node visited exactly once
# Comparison and deletion are O(1) operations
# Total: O(n)
```

### Space Complexity: O(1)
```python
# Uses only one pointer variable: current
# Space usage independent of input size
# In-place modification
# Total: O(1)
```

### Performance Characteristics
```python
# Best case (no duplicates): n comparisons, 0 deletions
# Worst case (all duplicates): n comparisons, (n-1) deletions  
# Average case: O(n) regardless of duplicate distribution
```

## Edge Cases and Robustness

### Edge Case 1: Empty List
```python
head = None
current = None  # current = head
while None and None.next:  # False - loop doesn't execute
return None  # Correctly returns empty list
```

### Edge Case 2: Single Node
```python
head = [1]
current = Node(1)
while Node(1) and None:  # False - loop doesn't execute
return [1]  # Correctly returns single node
```

### Edge Case 3: All Same Values
```python
Input: [1,1,1,1]
# Iteration 1: [1] → [1,1,1] becomes [1] → [1,1]
# Iteration 2: [1] → [1,1] becomes [1] → [1]
# Iteration 3: [1] → [1] becomes [1] (condition fails)
Output: [1]  # Correctly keeps one instance
```

### Edge Case 4: No Duplicates
```python
Input: [1,2,3,4]
# Each iteration advances current pointer
# No deletion operations performed
Output: [1,2,3,4]  # Original list preserved
```

### Edge Case 5: Alternating Pattern
```python
Input: [1,1,2,2,3,3]
# Processes each duplicate pair independently
# current doesn't move during duplicate removal
Output: [1,2,3]  # Each value appears once
```

## Linked List Fundamentals

### Pointer Manipulation Principles
```python
# Node deletion essence:
# - Don't actually "delete" nodes
# - Change previous node's next pointer to "skip" the target
# - Skipped node becomes unreachable and gets garbage collected
```

### Memory Management
```python
# Python's garbage collection:
# current.next = current.next.next
# ↑ This operation removes reference to middle node
# → Automatically frees memory when no references remain
```

### Pointer Safety
```python
# Null pointer access prevention:
# while current and current.next:
# ↑ Short-circuit evaluation ensures safety
# If current is None, current.next is never evaluated
```

## Real-World Applications

### Database Record Processing
```python
# Remove duplicate records from sorted result sets
# Memory-efficient processing of large datasets
# Streaming data deduplication
```

### Data Pipeline Operations
```python
# ETL processes with duplicate removal
# Real-time data stream cleaning
# Memory-constrained environments
```

### System Design Considerations
```python
# In-place operations for memory optimization
# O(1) space complexity importance in resource-limited systems
# Efficient linked list manipulation patterns
```

## Code Quality Improvements

### Enhanced Error Handling (Optional)
```python
def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
    # Early return for empty list (defensive programming)
    if not head:
        return head
    
    current = head
    
    while current and current.next:
        if current.val == current.next.val:
            current.next = current.next.next
        else:
            current = current.next
    
    return head
```

### Alternative Variable Names
```python
def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
    # More descriptive variable name
    node = head
    
    while node and node.next:
        if node.val == node.next.val:
            node.next = node.next.next
        else:
            node = node.next
    
    return head
```

## Interview Considerations

### Key Points to Mention
```python
# 1. Recognize sorted list property (duplicates are adjacent)
# 2. Explain in-place modification approach
# 3. Discuss pointer safety with loop conditions
# 4. Highlight why current doesn't move during deletion
# 5. Analyze time/space complexity
```

### Follow-up Questions
```python
# Q: What if list wasn't sorted?
# A: Would need O(n²) comparison or O(n) hash set

# Q: How to remove ALL occurrences of duplicates?
# A: Different algorithm - need dummy node approach

# Q: How to handle multiple consecutive duplicates?
# A: Current algorithm already handles this correctly
```

## Best Practices Demonstrated

### 1. **Efficient Pointer Management**
```python
# Use working pointer while preserving original head
# Safe traversal with proper null checks
```

### 2. **In-Place Optimization**
```python
# Modify existing structure instead of creating new one
# Minimize memory allocation and deallocation
```

### 3. **Clear Logic Flow**
```python
# Simple conditional structure
# Self-documenting variable names and comments
```

### 4. **Robust Edge Case Handling**
```python
# Single loop condition handles multiple edge cases
# No special case code needed for boundary conditions
```

### 5. **Optimal Algorithm Design**
```python
# Single pass solution
# Minimal space usage
# Maximum efficiency for the problem constraints
```

This solution exemplifies excellent linked list manipulation techniques, demonstrating how to efficiently solve duplicate removal while maintaining optimal time and space complexity. The approach showcases fundamental pointer operations essential for linked list mastery and technical interviews.