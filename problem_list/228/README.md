# 228. Summary Ranges - Solution Explanation

## Problem Overview

Summarize consecutive integers in a sorted array into ranges.

**Input**: A sorted unique integer array
**Output**: List of strings representing the smallest sorted list of ranges

**Range Formats:**
- **Single number**: `"a"` (when range contains only one number)
- **Range**: `"a->b"` (when range spans from a to b)

**Examples:**
```python
Input: [0,1,2,4,5,7]
Output: ["0->2","4->5","7"]
Explanation: 
- [0,1,2] → "0->2" (consecutive range)
- [4,5] → "4->5" (consecutive range)  
- [7] → "7" (single number)

Input: [0,2,3,5,6,8,9]
Output: ["0","2->3","5->6","8->9"]
Explanation:
- [0] → "0" (single number)
- [2,3] → "2->3" (consecutive range)
- [5,6] → "5->6" (consecutive range)
- [8,9] → "8->9" (consecutive range)
```

## Key Insights

### Range Detection Strategy
```python
# Core Approach: Detect "breaks" in consecutive sequences
# 1. Track the start of current range
# 2. Detect when consecutiveness breaks
# 3. Finalize the completed range
# 4. Start a new range from the breaking point
```

### Consecutive Detection Logic
```python
# Two numbers are consecutive if: nums[i] == nums[i-1] + 1
# If NOT consecutive → current range ends, new range begins
# This is why we compare each number with its predecessor
```

### Why Adjacent Element Comparison?
```python
# We need to check: "Does this sequence continue?"
# Method: Compare current element with previous element
# nums[i] vs nums[i-1] tells us if the sequence breaks
```

## Solution Approach

Our solution uses **Break-Point Detection** with optimal loop design:

```python
def summaryRanges(self, nums: List[int]) -> List[str]:
    # Handle the edge case of an empty list
    if not nums:
        return []

    ranges = []
    # The start of our current range is the first number
    start = nums[0]

    # Iterate through the list to find the end of each range
    for i in range(1, len(nums)):
        # Check if the current number is NOT consecutive with the previous number
        # This means the range has just ended
        if nums[i] != nums[i - 1] + 1:
            # Add the completed range to our list
            if start == nums[i - 1]:
                ranges.append(str(start))
            else:
                ranges.append(f"{start}->{nums[i-1]}")

            # Start a new range with the current number
            start = nums[i]

    # After the loop, the very last range still needs to be added
    if start == nums[-1]:
        ranges.append(str(start))
    else:
        ranges.append(f"{start}->{nums[-1]}")

    return ranges
```

**Strategy:**
1. **Initialize Range**: Start first range with nums[0]
2. **Break Detection**: Compare adjacent elements for consecutiveness
3. **Range Finalization**: When break found, format and store completed range
4. **Range Restart**: Begin new range from breaking element
5. **Final Range**: Handle the last range after loop completion

## Critical Design Decision: `for i in range(1, len(nums)):`

### Why Start from Index 1?

#### Reason 1: Adjacent Element Comparison Safety
```python
# Loop body uses: nums[i] vs nums[i-1]
# If i starts from 1: nums[1] vs nums[0] ✓ (safe)
# If i starts from 0: nums[0] vs nums[-1] ✗ (wrong comparison)

# Example with nums = [0,1,2,4,5,7]:
# i=1: compare nums[1]=1 with nums[0]=0 → 1 vs 0+1 = 1 ✓
# i=2: compare nums[2]=2 with nums[1]=1 → 2 vs 1+1 = 2 ✓
```

#### Reason 2: Logical Processing Flow
```python
# start = nums[0]  # First element begins the first range
# i=1: Check if nums[1] continues the range started by nums[0]
# i=2: Check if nums[2] continues the range from nums[1]
# Pattern: Each element checks relationship with its predecessor
```

#### Reason 3: Index Boundary Safety
```python
# Ensures i-1 is always a valid index
# i ≥ 1 guarantees i-1 ≥ 0
# Prevents array out-of-bounds errors
```

#### What Would Happen with Different Ranges?

**If `range(0, len(nums))`:**
```python
# i=0: nums[0] vs nums[-1] comparison
# Compares first element with last element → meaningless
# Example: [0,1,2,4,5,7] → 0 vs 7+1 = 8 → incorrect break detection
```

**If `range(2, len(nums))`:**
```python
# Skips comparison between nums[1] and nums[0]
# Misses potential break between first two elements
# Example: [0,5,6] → would miss the break between 0 and 5
```

## Detailed Code Analysis

### Step 1: Edge Case Handling
```python
if not nums:
    return []
```
**Purpose**: Prevent errors when processing empty arrays
**Alternative**: Could also check `len(nums) == 0`

### Step 2: Range Initialization
```python
ranges = []
start = nums[0]
```
**Logic**: 
- `ranges`: Stores final result strings
- `start`: Tracks beginning of current range (always starts with first element)

### Step 3: Break Detection Loop
```python
for i in range(1, len(nums)):
    if nums[i] != nums[i - 1] + 1:
```

**Consecutiveness Test**:
```python
# nums[i-1] + 1: Expected next value if consecutive
# nums[i]: Actual current value
# If they don't match → consecutiveness broken → range ends
```

### Step 4: Range Finalization
```python
if start == nums[i - 1]:
    ranges.append(str(start))           # Single element: "5"
else:
    ranges.append(f"{start}->{nums[i-1]}")  # Range: "2->5"
```

**Format Decision**:
- **Single element**: When range start equals range end
- **Multi-element range**: When range spans multiple numbers

### Step 5: New Range Initialization
```python
start = nums[i]
```
**Logic**: Current element (where break occurred) becomes start of next range

### Step 6: Final Range Processing
```python
if start == nums[-1]:
    ranges.append(str(start))
else:
    ranges.append(f"{start}->{nums[-1]}")
```
**Necessity**: Loop only processes breaks; final range has no subsequent break to trigger processing

## Step-by-Step Execution Trace

### Example: nums = [0,1,2,4,5,7]

#### Initialization
```python
start = 0
ranges = []
```

#### Loop Execution

**i=1: nums[1]=1, nums[0]=0**
```python
if 1 != 0 + 1:  # 1 != 1 → False
    # Consecutive → no action
# start=0, ranges=[]
```

**i=2: nums[2]=2, nums[1]=1**
```python
if 2 != 1 + 1:  # 2 != 2 → False
    # Consecutive → no action
# start=0, ranges=[]
```

**i=3: nums[3]=4, nums[2]=2**
```python
if 4 != 2 + 1:  # 4 != 3 → True ← BREAK DETECTED!
    # Range [0,2] completed
    if start == nums[2]:  # 0 == 2 → False
        ranges.append(str(start))
    else:
        ranges.append(f"{start}->{nums[2]}")  # "0->2"
    
    start = nums[3] = 4  # New range starts
# start=4, ranges=["0->2"]
```

**i=4: nums[4]=5, nums[3]=4**
```python
if 5 != 4 + 1:  # 5 != 5 → False
    # Consecutive → no action
# start=4, ranges=["0->2"]
```

**i=5: nums[5]=7, nums[4]=5**
```python
if 7 != 5 + 1:  # 7 != 6 → True ← BREAK DETECTED!
    # Range [4,5] completed
    if start == nums[4]:  # 4 == 5 → False
        ranges.append(f"{start}->{nums[4]}")  # "4->5"
    
    start = nums[5] = 7  # New range starts
# start=7, ranges=["0->2","4->5"]
```

#### Final Range Processing
```python
# After loop: start=7, nums[-1]=7
if start == nums[-1]:  # 7 == 7 → True
    ranges.append(str(start))  # "7"
# Final result: ["0->2","4->5","7"]
```

## Edge Cases Analysis

### Edge Case 1: Empty Array
```python
nums = []
# if not nums: return [] → immediate return
# Result: []
```

### Edge Case 2: Single Element
```python
nums = [5]
# start = 5
# Loop range(1,1) → no iterations
# Final processing: start == nums[-1] → "5"
# Result: ["5"]
```

### Edge Case 3: All Consecutive
```python
nums = [1,2,3,4,5]
# No breaks detected in loop
# All elements form single range
# Final processing: start(1) != nums[-1](5) → "1->5"
# Result: ["1->5"]
```

### Edge Case 4: No Consecutive Pairs
```python
nums = [1,3,5,7,9]
# Every comparison detects break
# Each element becomes individual range
# Result: ["1","3","5","7","9"]
```

### Edge Case 5: Two Elements (Consecutive)
```python
nums = [1,2]
# start = 1
# i=1: 2 == 1+1 → consecutive, no break
# Final processing: start(1) != nums[-1](2) → "1->2"
# Result: ["1->2"]
```

### Edge Case 6: Two Elements (Non-consecutive)
```python
nums = [1,5]
# start = 1
# i=1: 5 != 1+1 → break detected
# Process range [1,1] → "1", start = 5
# Final processing: start(5) == nums[-1](5) → "5"
# Result: ["1","5"]
```

### Edge Case 7: Negative Numbers
```python
nums = [-3,-2,-1,1,2,4]
# start = -3
# i=1: -2 == -3+1 → consecutive
# i=2: -1 == -2+1 → consecutive  
# i=3: 1 != -1+1 → break → "-3->-1", start=1
# i=4: 2 == 1+1 → consecutive
# i=5: 4 != 2+1 → break → "1->2", start=4
# Final: "4"
# Result: ["-3->-1","1->2","4"]
```

## Performance Analysis

### Time Complexity: O(n)
```python
# Single pass through array: O(n)
# Each element processed exactly once
# Consecutive check per element: O(1)
# String formatting and append: O(1) amortized
# Total: O(n)
```

### Space Complexity: O(1) excluding output
```python
# Additional variables: start, i, ranges
# ranges stores output (not counted in space analysis)
# Excluding output: O(1) auxiliary space
# Including output: O(n) in worst case (all individual elements)
```

### Worst Case Scenarios
```python
# Time: O(n) regardless of input pattern
# Space: O(n) when every element is individual range
# Example: [1,3,5,7,9,...] → ["1","3","5","7","9",...]
```

## Alternative Approaches Comparison

### Approach 1: Two-Pointer with Inner Loop
```python
def summaryRanges(self, nums):
    if not nums:
        return []
    
    ranges = []
    i = 0
    
    while i < len(nums):
        start = i
        # Find end of current consecutive sequence
        while i + 1 < len(nums) and nums[i + 1] == nums[i] + 1:
            i += 1
        
        # Format range
        if start == i:
            ranges.append(str(nums[start]))
        else:
            ranges.append(f"{nums[start]}->{nums[i]}")
        
        i += 1
    
    return ranges
```

**Analysis**:
- ✅ **Explicit Range Finding**: Inner loop clearly finds range boundaries
- ✅ **No Final Processing**: Handles last range within main loop
- ❌ **Nested Loops**: More complex control flow
- ❌ **Index Management**: More complex boundary checking

### Approach 2: Grouping with Collections
```python
from itertools import groupby

def summaryRanges(self, nums):
    ranges = []
    for k, g in groupby(enumerate(nums), lambda x: x[1] - x[0]):
        group = list(g)
        if len(group) == 1:
            ranges.append(str(group[0][1]))
        else:
            ranges.append(f"{group[0][1]}->{group[-1][1]}")
    return ranges
```

**Analysis**:
- ✅ **Elegant Grouping**: Uses mathematical property for grouping
- ✅ **Functional Style**: Leverages Python's itertools
- ❌ **Import Dependency**: Requires itertools import
- ❌ **Complexity**: Harder to understand grouping logic
- ❌ **Memory Usage**: Creates intermediate lists

### Approach 3: State Machine
```python
def summaryRanges(self, nums):
    if not nums:
        return []
    
    ranges = []
    start = nums[0]
    prev = nums[0]
    
    for num in nums[1:]:
        if num != prev + 1:
            # End current range
            if start == prev:
                ranges.append(str(start))
            else:
                ranges.append(f"{start}->{prev}")
            start = num
        prev = num
    
    # Final range
    if start == prev:
        ranges.append(str(start))
    else:
        ranges.append(f"{start}->{prev}")
    
    return ranges
```

**Analysis**:
- ✅ **Clear State Tracking**: Explicit tracking of previous element
- ✅ **Readable Logic**: Clear separation of concerns
- ❌ **Extra Variable**: Additional prev variable needed
- ❌ **Similar Pattern**: Not significantly different from original

## Why Your Solution is Optimal

### 1. **Perfect Loop Design**
```python
# range(1, len(nums)) is optimal for adjacent comparison
# Ensures safe access to nums[i-1]
# Processes each element exactly once
# Natural boundary handling
```

### 2. **Minimal Variable Usage**
```python
# Only essential variables: start, ranges, i
# No redundant state tracking
# Clear variable responsibilities
```

### 3. **Efficient Break Detection**
```python
# Direct comparison: nums[i] != nums[i-1] + 1
# Immediate break detection
# No unnecessary computations
```

### 4. **Clean String Formatting**
```python
# Clear distinction between single element and range
# Consistent format with problem requirements
# Efficient f-string usage
```

### 5. **Comprehensive Edge Case Handling**
```python
# Empty array: Early return
# Single element: Handled by loop design
# All consecutive: Final processing
# No consecutive: Loop handles all breaks
```

## Real-World Applications

### Data Compression
```python
# Compress consecutive IDs: [1,2,3,4,8,9,10] → "1-4,8-10"
# Log file timestamp ranges: "09:00-09:15, 10:30-10:45"
# Version number summarization: "v1.0-v1.5, v2.0, v3.1-v3.3"
```

### Resource Management
```python
# Available time slots: "9:00-11:00, 13:00-15:00"
# Hotel room availability: "101-105, 201, 301-310"
# IP address range allocation: "192.168.1.1-192.168.1.50"
```

### Database Optimization
```python
# Index range queries: WHERE id BETWEEN 100 AND 200
# Partition pruning: Skip partitions outside ranges
# Query result summarization for large datasets
```

### Scheduling Systems
```python
# Meeting room availability summaries
# Employee shift scheduling ranges
# Resource allocation time windows
```

## Key Learning Points

### Loop Design Principles
```python
# 1. Choose index range based on access patterns
# 2. Ensure boundary safety for array operations
# 3. Consider what each iteration needs to accomplish
# 4. Optimize for the most common operation
```

### Range Processing Patterns
```python
# 1. Initialize range start
# 2. Detect range boundaries (breaks)
# 3. Process completed ranges immediately
# 4. Handle final range after main processing
```

### Adjacent Element Comparison
```python
# Common pattern in array problems
# Requires careful index range selection
# Always validate boundary conditions
# Consider edge cases with minimal elements
```

## Common Pitfalls Avoided

### Pitfall 1: Wrong Loop Range
```python
# ❌ range(0, len(nums)) → invalid nums[i-1] access
# ❌ range(2, len(nums)) → misses first comparison
# ✅ range(1, len(nums)) → perfect for adjacent comparison
```

### Pitfall 2: Missing Final Range
```python
# ❌ Only processing ranges found during loop
# ✅ Adding final range processing after loop
# The last range never triggers a "break" so needs special handling
```

### Pitfall 3: Incorrect Range Boundaries
```python
# ❌ Using current index for range end
# ✅ Using previous index (nums[i-1]) for range end
# When break detected, previous element is actual range end
```

### Pitfall 4: String Formatting Errors
```python
# ❌ Always using range format "start->end"
# ✅ Single element check: start == end → "start"
# ❌ Inconsistent arrow format: "start-end" vs "start->end"
```

This solution demonstrates excellent understanding of array traversal patterns, optimal loop design, and efficient range processing. The choice of `range(1, len(nums))` is particularly well-suited for adjacent element comparison problems and showcases thoughtful algorithm design.