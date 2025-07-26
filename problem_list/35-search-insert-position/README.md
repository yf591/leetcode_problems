# 35. Search Insert Position - Solution Explanation

## Problem Overview
Given a sorted array of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.

You must write an algorithm with **O(log n)** runtime complexity.

**Examples:**
- `nums = [1,3,5,6]`, `target = 5` → `2`
- `nums = [1,3,5,6]`, `target = 2` → `1`
- `nums = [1,3,5,6]`, `target = 7` → `4`

**Constraints:**
- 1 ≤ nums.length ≤ 10⁴
- -10⁴ ≤ nums[i] ≤ 10⁴
- `nums` contains **distinct** values sorted in **ascending** order
- -10⁴ ≤ target ≤ 10⁴

## Understanding the Problem

### Two Scenarios
1. **Target exists**: Return the exact index where target is found
2. **Target doesn't exist**: Return the index where target should be inserted to maintain sorted order

### Visual Example
```
Array: [1, 3, 5, 6]
Index:  0  1  2  3

Case 1: target = 5
Result: 2 (found at index 2)

Case 2: target = 2  
Result: 1 (should be inserted between 1 and 3)
Insert: [1, 2, 3, 5, 6]
        0  1  2  3  4

Case 3: target = 7
Result: 4 (should be inserted at the end)
Insert: [1, 3, 5, 6, 7]
        0  1  2  3  4
```

## Algorithm: Binary Search

Since the array is sorted, we can use **Binary Search** to achieve O(log n) time complexity by eliminating half of the search space in each iteration.

**Key Insight**: When binary search terminates without finding the target, the `low` pointer will be positioned exactly at the insertion point.

## Step-by-Step Algorithm Breakdown

### Step 1: Initialize Search Boundaries
```python
low, high = 0, len(nums) - 1
```
**Purpose**: 
- `low`: Left boundary of search range
- `high`: Right boundary of search range
- Initially covers the entire array

### Step 2: Binary Search Loop
```python
while low <= high:
```
**Condition**: Continue while search range is valid
**Termination**: When `low > high`, no more elements to check

### Step 3: Calculate Middle Index
```python
mid = low + (high - low) // 2
```
**Overflow-safe calculation**: Prevents integer overflow in languages with fixed integer sizes
**Alternative**: `(low + high) // 2` works in Python but less portable

### Step 4: Compare and Narrow Search Range

#### Case 1: Target Found
```python
if nums[mid] == target:
    return mid
```
**Action**: Return the exact index immediately

#### Case 2: Target is Larger
```python
elif nums[mid] < target:
    low = mid + 1
```
**Logic**: Target must be in the right half, discard left half
**Update**: Move left boundary to eliminate left portion

#### Case 3: Target is Smaller
```python
else:  # nums[mid] > target
    high = mid - 1
```
**Logic**: Target must be in the left half, discard right half
**Update**: Move right boundary to eliminate right portion

### Step 5: Return Insertion Position
```python
return low
```
**Key Property**: When loop terminates, `low` points to the correct insertion position

## Detailed Example Walkthrough

### Example 1: Target Found
**Input:** `nums = [1, 3, 5, 6]`, `target = 5`

#### Initial State
```
Array: [1, 3, 5, 6]
Index:  0  1  2  3
low = 0, high = 3
```

#### Iteration 1
```
mid = 0 + (3-0)//2 = 1
nums[1] = 3
3 < 5 → search right half
low = mid + 1 = 2

New range: [5, 6]
low = 2, high = 3
```

#### Iteration 2
```
mid = 2 + (3-2)//2 = 2
nums[2] = 5
5 == 5 → Found!
return 2
```

### Example 2: Target Not Found (Middle Insertion)
**Input:** `nums = [1, 3, 5, 6]`, `target = 2`

#### Complete Trace Table
| Iteration | low | high | mid | nums[mid] | Comparison | Action | New Range |
|-----------|-----|------|-----|-----------|------------|---------|-----------|
| 1 | 0 | 3 | 1 | 3 | 3 > 2 | high = 0 | [1] |
| 2 | 0 | 0 | 0 | 1 | 1 < 2 | low = 1 | Invalid |

#### Loop Termination
```
After iteration 2: low = 1, high = 0
Condition: low > high → loop ends
return low = 1
```

#### Result Verification
```
Insert target at index 1: [1, 2, 3, 5, 6]
                           0  1  2  3  4
Maintains sorted order ✓
```

### Example 3: Target Not Found (End Insertion)
**Input:** `nums = [1, 3, 5, 6]`, `target = 7`

#### Complete Trace
| Iteration | low | high | mid | nums[mid] | Comparison | Action |
|-----------|-----|------|-----|-----------|------------|---------|
| 1 | 0 | 3 | 1 | 3 | 3 < 7 | low = 2 |
| 2 | 2 | 3 | 2 | 5 | 5 < 7 | low = 3 |
| 3 | 3 | 3 | 3 | 6 | 6 < 7 | low = 4 |

#### Final State
```
low = 4, high = 3 → low > high
return 4 (append to end)
```

## Why `low` Points to Insertion Position

### Mathematical Invariant
During binary search, the following invariant holds:
- All elements with index < `low` are < `target`
- All elements with index > `high` are > `target`

### Loop Termination Analysis
When `low > high`:
- `high` points to the largest element < `target`
- `low` points to the smallest element ≥ `target`
- Therefore, `low` is the correct insertion position

### Visual Representation
```
Array after termination:
[... elements < target ...] [... elements ≥ target ...]
                           ↑
                         low (insertion point)
```

## Edge Cases Analysis

### Edge Case 1: Insert at Beginning
```python
nums = [2, 3, 4], target = 1

Trace:
low=0, high=2 → mid=1, nums[1]=3, 3>1 → high=0
low=0, high=0 → mid=0, nums[0]=2, 2>1 → high=-1
low=0, high=-1 → low > high, return 0

Result: Insert at beginning [1, 2, 3, 4]
```

### Edge Case 2: Insert at End
```python
nums = [1, 2, 3], target = 4

Trace:
low=0, high=2 → mid=1, nums[1]=2, 2<4 → low=2
low=2, high=2 → mid=2, nums[2]=3, 3<4 → low=3
low=3, high=2 → low > high, return 3

Result: Insert at end [1, 2, 3, 4]
```

### Edge Case 3: Single Element Array
```python
nums = [1], target = 2

Trace:
low=0, high=0 → mid=0, nums[0]=1, 1<2 → low=1
low=1, high=0 → low > high, return 1

Result: [1, 2]
```

### Edge Case 4: Single Element Array (Insert Before)
```python
nums = [3], target = 1

Trace:
low=0, high=0 → mid=0, nums[0]=3, 3>1 → high=-1
low=0, high=-1 → low > high, return 0

Result: [1, 3]
```

## Alternative Approaches

### Approach 1: Linear Search
```python
def searchInsert(self, nums, target):
    for i in range(len(nums)):
        if nums[i] >= target:
            return i
    return len(nums)
```

**Analysis:**
- ✅ **Simple to understand**
- ✅ **Handles all cases correctly**
- ❌ **Time complexity: O(n)** - doesn't meet requirement
- ❌ **Inefficient for large arrays**

### Approach 2: Built-in bisect module
```python
import bisect

def searchInsert(self, nums, target):
    return bisect.bisect_left(nums, target)
```

**Analysis:**
- ✅ **Correct and efficient O(log n)**
- ✅ **Very concise**
- ❌ **Doesn't demonstrate algorithm understanding**
- ❌ **Not allowed in most interviews**

### Approach 3: Recursive Binary Search
```python
def searchInsert(self, nums, target):
    def binary_search(left, right):
        if left > right:
            return left
        
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            return binary_search(mid + 1, right)
        else:
            return binary_search(left, mid - 1)
    
    return binary_search(0, len(nums) - 1)
```

**Analysis:**
- ✅ **Correct O(log n) time complexity**
- ✅ **Elegant recursive structure**
- ❌ **O(log n) space complexity** due to call stack
- ❌ **More complex than iterative version**

## Current Solution Advantages

### Iterative Binary Search - Our Solution
```python
def searchInsert(self, nums, target):
    low, high = 0, len(nums) - 1
    
    while low <= high:
        mid = low + (high - low) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    
    return low
```

**Advantages:**
- ✅ **Optimal time complexity: O(log n)**
- ✅ **Optimal space complexity: O(1)**
- ✅ **Handles both search and insertion cases**
- ✅ **Clear and readable implementation**
- ✅ **No recursion overhead**

## Time & Space Complexity Analysis

### Current Solution
- **Time Complexity**: **O(log n)** where n = array length
  - Each iteration eliminates half the search space
  - Maximum iterations: ⌈log₂(n)⌉
  - For array of 1000 elements: maximum 10 iterations

- **Space Complexity**: **O(1)** - constant extra space
  - Only uses three integer variables (`low`, `high`, `mid`)
  - No additional data structures needed

### Complexity Comparison
| Approach | Time | Space | Interview Suitable? |
|----------|------|-------|-------------------|
| **Binary Search (current)** | **O(log n)** | **O(1)** | ✅ **Optimal** |
| Linear Search | O(n) | O(1) | ❌ Too slow |
| Built-in bisect | O(log n) | O(1) | ❌ Doesn't show skills |
| Recursive Binary | O(log n) | O(log n) | ⚠️ Suboptimal space |

## Common Pitfalls and Tips

### 1. Incorrect Loop Condition
```python
# ❌ Wrong: Misses some cases
while low < high:  # Should be <=

# ✅ Correct: Covers all valid ranges
while low <= high:
```

### 2. Integer Overflow (In Other Languages)
```python
# ❌ Potential overflow in C++/Java
mid = (low + high) / 2

# ✅ Overflow-safe calculation
mid = low + (high - low) // 2
```

### 3. Incorrect Boundary Updates
```python
# ❌ Wrong: Can cause infinite loops
if nums[mid] < target:
    low = mid  # Should be mid + 1

# ✅ Correct: Properly narrows search space
if nums[mid] < target:
    low = mid + 1
```

### 4. Forgetting the Insertion Case
```python
# ❌ Incomplete: Only handles found case
if nums[mid] == target:
    return mid
# Missing: what if not found?

# ✅ Complete: Handles both cases
# ... binary search logic ...
return low  # Insertion position
```

## Key Programming Concepts Demonstrated

1. **Binary Search Algorithm**: Divide and conquer approach
2. **Loop Invariants**: Maintaining valid search boundaries
3. **Edge Case Handling**: Empty ranges, boundary insertions
4. **Overflow Prevention**: Safe arithmetic operations
5. **Dual-purpose Algorithm**: Single code for search and insertion

## Practice Tips

1. **Trace through examples**: Follow pointer movements step by step
2. **Understand invariants**: Why `low` points to insertion position
3. **Test edge cases**: Beginning, end, single element, not found
4. **Verify boundary updates**: Ensure search space properly narrows
5. **Check termination**: Confirm loop exits correctly

## Real-World Applications

1. **Database Indexing**: Finding or inserting records in sorted structures
2. **Auto-complete Systems**: Inserting new suggestions in sorted lists
3. **Scheduling Systems**: Finding optimal time slots
4. **Memory Management**: Maintaining sorted free block lists
5. **Version Control**: Inserting commits in chronological order

## Binary Search Variations

### Related Problems
1. **Search in Rotated Array**: Modified binary search
2. **Find Peak Element**: Binary search on unsorted data
3. **Square Root**: Binary search for mathematical functions
4. **Search 2D Matrix**: Extended binary search

### Template Pattern
```python
# Standard binary search template
def binary_search_template(nums, target):
    low, high = 0, len(nums) - 1
    
    while low <= high:
        mid = low + (high - low) // 2
        if condition_met(nums[mid], target):
            return mid
        elif should_search_right(nums[mid], target):
            low = mid + 1
        else:
            high = mid - 1
    
    return insertion_position  # Often `low`
```

This algorithm demonstrates the elegance and efficiency of binary search, solving both search and insertion problems with optimal time complexity while maintaining clear, readable code.