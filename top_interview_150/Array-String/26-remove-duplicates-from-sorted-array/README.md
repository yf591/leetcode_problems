# 26. Remove Duplicates from Sorted Array - Solution Explanation

## Problem Overview
Given an integer array `nums` sorted in **non-decreasing order**, remove the duplicates **in-place** such that each unique element appears only once. The **relative order** of the elements should be kept the same. Then return the number of unique elements in `nums`.

**Key Constraints:**
- Modify the array **in-place** (no extra array allowed)
- Return the number of unique elements `k`
- The first `k` elements of `nums` should contain the unique elements

**Examples:**
- `nums = [1,1,2]` → `nums = [1,2,_]`, return `2`
- `nums = [0,0,1,1,1,2,2,3,3,4]` → `nums = [0,1,2,3,4,_,_,_,_,_]`, return `5`

## Understanding the Problem

### What "In-Place" Means
**In-place** modification means we cannot create a new array. We must rearrange the existing array so that:
- First `k` positions contain unique elements in sorted order
- Remaining positions can contain anything (marked as `_`)

**Example:**
```
Original: [1, 1, 2, 2, 2, 3, 4, 4]
Result:   [1, 2, 3, 4, _, _, _, _]  ← Return k=4
          ↑―――――――――↑  ↑―――――――↑
          Unique elements  Ignored
```

## Algorithm: Two Pointers Technique

The core idea uses **Two Pointers**:
- **`i` (Read pointer)**: Scans through the array sequentially
- **`k` (Write pointer)**: Points to where the next unique element should be placed

**Key Insight**: In a sorted array, if `nums[i] != nums[i-1]`, then `nums[i]` is a new unique element.

## Step-by-Step Algorithm Breakdown

### Step 1: Handle Edge Case
```python
if not nums:
    return 0
```
**Purpose**: Return 0 for empty arrays
**Example**: `[]` → `0`

### Step 2: Initialize Write Pointer
```python
k = 1
```
**Why start at 1?**
- The first element (`nums[0]`) is always unique
- `k` represents the position where the **next** unique element should be placed
- Start placing from index 1

**Initial State:**
```
nums: [1, 1, 2, 2, 2, 3, 4, 4]
       ↑                          
   nums[0] is always unique

k = 1  ← Next unique element goes here
```

### Step 3: Scan Array Starting from Second Element
```python
for i in range(1, len(nums)):
```
**Purpose**: Check each element starting from index 1
**Why i=1?** First element is already confirmed unique

### Step 4: Detect New Unique Elements
```python
if nums[i] != nums[i - 1]:
```
**Condition**: Current element differs from previous element
**Meaning**: Found a new unique element!

**Sorted Array Property:**
```
[1, 1, 2, 2, 2, 3, 4, 4]
    ↑  ↑        ↑  ↑
   Same Different Same Different
```

### Step 5: Place Unique Element and Advance Pointer
```python
nums[k] = nums[i]
k += 1
```
**Actions:**
1. Copy the new unique element to position `k`
2. Move `k` to the next available position

## Detailed Example Walkthrough

**Input:** `nums = [1, 1, 2, 2, 2, 3, 4, 4]`

### Initial State
```
nums: [1, 1, 2, 2, 2, 3, 4, 4]
       ↑  
    k=1, i=1 (starting position)
```

### i=1: nums[1]=1 vs nums[0]=1
```
1 == 1 (same) → No action needed

nums: [1, 1, 2, 2, 2, 3, 4, 4]
       ↑  ↑
       k=1, i=1→2
```

### i=2: nums[2]=2 vs nums[1]=1  
```
2 != 1 (different) → New unique element found!
nums[k] = nums[i] → nums[1] = 2
k++ → k=2

nums: [1, 2, 2, 2, 2, 3, 4, 4]
          ↑  ↑
          k=2, i=2→3
```

### i=3: nums[3]=2 vs nums[2]=2
```
2 == 2 (same) → No action needed

nums: [1, 2, 2, 2, 2, 3, 4, 4]
          ↑     ↑
          k=2, i=3→4
```

### i=4: nums[4]=2 vs nums[3]=2
```
2 == 2 (same) → No action needed

nums: [1, 2, 2, 2, 2, 3, 4, 4]
          ↑        ↑
          k=2, i=4→5
```

### i=5: nums[5]=3 vs nums[4]=2
```
3 != 2 (different) → New unique element found!
nums[k] = nums[i] → nums[2] = 3
k++ → k=3

nums: [1, 2, 3, 2, 2, 3, 4, 4]
             ↑        ↑
             k=3, i=5→6
```

### i=6: nums[6]=4 vs nums[5]=3
```
4 != 3 (different) → New unique element found!
nums[k] = nums[i] → nums[3] = 4
k++ → k=4

nums: [1, 2, 3, 4, 2, 3, 4, 4]
                ↑           ↑
                k=4, i=6→7
```

### i=7: nums[7]=4 vs nums[6]=4
```
4 == 4 (same) → No action needed

nums: [1, 2, 3, 4, 2, 3, 4, 4]
                ↑              ↑
                k=4, i=7 (end)
```

### Final Result
```
nums: [1, 2, 3, 4, _, _, _, _]
       ↑―――――――↑
       k=4 unique elements

return k = 4
```

## Visual Step-by-Step Transformation

### Array State Changes
```
Step 0: [1, 1, 2, 2, 2, 3, 4, 4]  k=1
        ↑
      First element always unique

Step 2: [1, 2, 2, 2, 2, 3, 4, 4]  k=2
        ↑  ↑
       Found 2, placed at position 1

Step 5: [1, 2, 3, 2, 2, 3, 4, 4]  k=3
        ↑  ↑  ↑
       Found 3, placed at position 2

Step 6: [1, 2, 3, 4, 2, 3, 4, 4]  k=4
        ↑  ↑  ↑  ↑
       Found 4, placed at position 3

Final:  [1, 2, 3, 4, _, _, _, _]
        ↑―――――――――↑
        Result section (k=4)
```

## Key Algorithm Insights

### 1. In-Place Modification Strategy
- **Read position** (`i`): Always moves forward
- **Write position** (`k`): Only advances when unique element found
- **Overwriting**: Safe because we only overwrite duplicates

### 2. Why k=1 Starting Point?
```python
nums: [1, 1, 2, 3, 3]
       ↑              
   nums[0] is guaranteed unique

k=1 ← Start placing from here
```

### 3. Sorted Array Advantage
```python
# Only need to compare adjacent elements
if nums[i] != nums[i-1]:  # New unique element
    # In unsorted array, would need to check entire prefix
```

### 4. Two Pointers Pattern
```
Reading:  i → → → → → → → →
Writing:    k   k   k   k
           ↑   ↑   ↑   ↑
         Unique elements only
```

## Alternative Approaches

### Approach 1: Using Set (Not In-Place)
```python
def removeDuplicates(self, nums):
    unique_nums = list(set(nums))
    unique_nums.sort()
    for i in range(len(unique_nums)):
        nums[i] = unique_nums[i]
    return len(unique_nums)
```
**Problems**: 
- Not truly in-place (creates additional data structures)
- Less efficient due to set operations and sorting

### Approach 2: Creating New Array (Not Allowed)
```python
def removeDuplicates(self, nums):
    result = []
    for i in range(len(nums)):
        if i == 0 or nums[i] != nums[i-1]:
            result.append(nums[i])
    # Copy back to nums...
    return len(result)
```
**Problem**: Violates in-place constraint

### Approach 3: Single Pass with Different Logic
```python
def removeDuplicates(self, nums):
    if not nums:
        return 0
    
    k = 0  # Start from 0
    for i in range(len(nums)):
        if i == 0 or nums[i] != nums[i-1]:
            nums[k] = nums[i]
            k += 1
    return k
```
**Difference**: Starts `k` from 0, includes first element in loop

## Time & Space Complexity Analysis

### Current Solution
- **Time Complexity**: **O(n)** where n = length of array
  - Single pass through the array
  - Each element examined exactly once
  - Constant time operations per element

- **Space Complexity**: **O(1)** - constant extra space
  - Only uses two integer variables (`i`, `k`)
  - No additional data structures
  - True in-place modification

### Complexity Comparison
| Approach | Time | Space | In-Place? | Notes |
|----------|------|-------|-----------|-------|
| Two Pointers (current) | O(n) | O(1) | ✅ | Most efficient |
| Set + Sort | O(n log n) | O(n) | ❌ | Extra space needed |
| New Array | O(n) | O(n) | ❌ | Violates constraint |

## Edge Cases Handled

### Empty Array
```python
nums = []
# Result: return 0
```

### Single Element
```python
nums = [1]
# k starts at 1, loop doesn't run
# Result: [1], return 1
```

### All Elements Same
```python
nums = [2, 2, 2, 2]
# No nums[i] != nums[i-1] conditions met
# Result: [2, _, _, _], return 1
```

### All Elements Different
```python
nums = [1, 2, 3, 4]
# Every nums[i] != nums[i-1] is true
# Result: [1, 2, 3, 4], return 4
```

### Two Elements
```python
nums = [1, 2]  → [1, 2], return 2
nums = [1, 1]  → [1, _], return 1
```

## Common Pitfalls and Tips

### 1. Starting k from Wrong Position
```python
# ❌ Wrong: k=0 requires special handling
k = 0
for i in range(len(nums)):
    if i == 0 or nums[i] != nums[i-1]:  # Need special case

# ✅ Correct: k=1 is cleaner
k = 1
for i in range(1, len(nums)):
    if nums[i] != nums[i-1]:  # No special case needed
```

### 2. Forgetting to Advance k
```python
# ❌ Wrong: k never advances
if nums[i] != nums[i-1]:
    nums[k] = nums[i]
    # k += 1  # Missing this line!

# ✅ Correct: Always increment k
if nums[i] != nums[i-1]:
    nums[k] = nums[i]
    k += 1
```

### 3. Wrong Array Access
```python
# ❌ Wrong: Can cause index error
if nums[i] != nums[i+1]:  # Looking ahead

# ✅ Correct: Looking back is safe
if nums[i] != nums[i-1]:  # i starts from 1
```

## Key Programming Concepts Demonstrated

1. **Two Pointers Technique**: Read and write pointers moving independently
2. **In-Place Array Modification**: Modifying array without extra space
3. **Sorted Array Properties**: Leveraging order for efficient duplicate detection
4. **Edge Case Handling**: Managing empty arrays and boundary conditions
5. **Loop Invariants**: Maintaining consistency throughout iteration

## Practice Tips

1. **Trace through examples**: Walk through with small arrays step by step
2. **Understand pointer roles**: `i` reads, `k` writes unique elements
3. **Visualize the transformation**: Draw array states at each step
4. **Test edge cases**: Empty array, single element, all same, all different
5. **Check invariants**: After each iteration, verify first `k` elements are unique

## Why This Algorithm is Optimal

1. **Minimal comparisons**: Only adjacent element comparisons needed
2. **Single pass**: Each element visited exactly once
3. **Constant space**: No additional data structures
4. **Leverages input properties**: Takes advantage of sorted order
5. **Clean implementation**: Simple logic with few edge cases

This algorithm demonstrates an elegant application of the two pointers technique for in-place array modification, efficiently removing duplicates while maintaining sorted order.