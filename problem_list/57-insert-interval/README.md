# 57\. Insert Interval - Solution Explanation

## Problem Overview

You are given a list of **non-overlapping** intervals, already **sorted** by their start times. You are also given a `newInterval`. The task is to insert this `newInterval` into the list, merging it with any existing intervals it overlaps with. The final list must remain sorted and non-overlapping.

**Key Definitions:**

  - **Sorted Input**: The initial `intervals` list is guaranteed to be sorted by the start time. This is a huge hint.
  - **Non-overlapping Input**: The initial `intervals` list has no overlaps. The only overlaps that need to be resolved are ones created by inserting `newInterval`.
  - **In-place Not Required**: You can create a new list for the result.

**Examples:**

```python
Input: intervals = [[1,3],[6,9]], newInterval = [2,5]
Output: [[1,5],[6,9]]
Explanation: newInterval [2,5] overlaps with [1,3], so they merge into [1,5].

Input: intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]
Output: [[1,2],[3,10],[12,16]]
Explanation: newInterval [4,8] overlaps with [3,5], [6,7], and [8,10], merging them all into a single interval [3,10].
```

## Key Insights

### A Single-Pass Solution

Because the initial `intervals` list is already **sorted**, we don't need to sort it again. This allows for a very efficient **single-pass** solution. We can iterate through the existing intervals and build our `result` list as we go.

### The Three Phases

As we iterate through the `intervals`, each interval will fall into one of three distinct phases relative to our `newInterval`:

1.  **Phase 1: "Before"**: The interval comes entirely before `newInterval` and does not overlap. We can simply add these intervals to our result list. An interval `[s, e]` is "before" if `e < newInterval.start`.

2.  **Phase 2: "The Merge"**: The interval overlaps with `newInterval`. Instead of adding these intervals to the result list right away, we merge them into our `newInterval` by updating its start and end times to be the union of both. We continue this for all overlapping intervals.

3.  **Phase 3: "After"**: The interval comes entirely after the merged `newInterval` and does not overlap. Once we've finished the merging phase, we can add the final merged `newInterval` to our result, followed by all the remaining "after" intervals.

## Solution Approach

This solution iterates through the sorted `intervals` in a single pass, using three distinct `while` loops to handle the three phases: before, during, and after the merge.

```python
from typing import List

class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        result = []
        i = 0
        n = len(intervals)

        # --- Phase 1: Add all intervals that end before the new one starts ---
        while i < n and intervals[i][1] < newInterval[0]:
            result.append(intervals[i])
            i += 1
            
        # --- Phase 2: Merge all overlapping intervals with newInterval ---
        while i < n and intervals[i][0] <= newInterval[1]:
            # The new start is the minimum of the two starts.
            newInterval[0] = min(newInterval[0], intervals[i][0])
            # The new end is the maximum of the two ends.
            newInterval[1] = max(newInterval[1], intervals[i][1])
            i += 1
        
        # After the merging loop, add the final, potentially expanded newInterval.
        result.append(newInterval)
        
        # --- Phase 3: Add all remaining intervals ---
        while i < n:
            result.append(intervals[i])
            i += 1
            
        return result
```

## Detailed Code Analysis

### Step 1: Initialization

```python
result = []
i = 0
n = len(intervals)
```

  - `result`: An empty list where we will build our final merged list of intervals.
  - `i`: An index that we will use to manually iterate through the `intervals` list. We use a manual index with `while` loops instead of a `for` loop because we need to process different parts of the list in different ways.

### Step 2: Phase 1 - Add "Before" Intervals

```python
while i < n and intervals[i][1] < newInterval[0]:
    result.append(intervals[i])
    i += 1
```

  - **`while i < n`**: A safety check to make sure we don't go past the end of the list.
  - **`intervals[i][1] < newInterval[0]`**: This is the core condition for this phase. It checks if the **end** of the current interval (`intervals[i][1]`) is strictly less than the **start** of our `newInterval`. If so, it means this interval is completely to the left and does not overlap.
  - **`result.append(intervals[i])`**: We add this non-overlapping interval directly to our result.
  - **`i += 1`**: We advance our index to check the next interval.

### Step 3: Phase 2 - The Merge Loop

```python
while i < n and intervals[i][0] <= newInterval[1]:
    newInterval[0] = min(newInterval[0], intervals[i][0])
    newInterval[1] = max(newInterval[1], intervals[i][1])
    i += 1
result.append(newInterval)
```

  - **`while i < n and intervals[i][0] <= newInterval[1]`**: This condition defines an overlap. It checks if the **start** of the current interval (`intervals[i][0]`) is less than or equal to the **end** of our `newInterval`. As long as this is true, the intervals are overlapping.
  - **The Merge Logic**:
      - `newInterval[0] = min(...)`: The start of the merged interval must be the earliest start time of the two.
      - `newInterval[1] = max(...)`: The end of the merged interval must be the latest end time of the two.
  - We repeatedly update `newInterval` in place, expanding it to "absorb" every overlapping interval.
  - **`result.append(newInterval)`**: Crucially, we only add the `newInterval` to our `result` list **after** this merging loop is finished.

### Step 4: Phase 3 - Add "After" Intervals

```python
while i < n:
    result.append(intervals[i])
    i += 1
```

  - When the merge loop (Phase 2) ends, our index `i` is now at the first interval that is completely to the right of our merged `newInterval`.
  - This final `while` loop simply takes all the remaining intervals and appends them to the `result` list.

## Step-by-Step Execution Trace

Let's trace `intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]]`, `newInterval = [4,8]` with extreme detail.

### **Initial State:**

  - `result = []`
  - `i = 0`
  - `newInterval = [4, 8]`

-----

### **Phase 1: "Before"**

  - **Loop 1 (`i=0`)**: `intervals[0]` is `[1,2]`. Check `2 < 4`? **True**.
      - `result.append([1,2])`. `result` is now `[[1,2]]`.
      - `i` becomes `1`.
  - **Loop 2 (`i=1`)**: `intervals[1]` is `[3,5]`. Check `5 < 4`? **False**.
  - The "Before" loop terminates.

**State after Phase 1:** `i = 1`, `result = [[1,2]]`, `newInterval = [4,8]`

-----

### **Phase 2: "The Merge"**

  - **Loop 1 (`i=1`)**: `intervals[1]` is `[3,5]`. Check `3 <= 8`? **True**.

      - Merge `[4,8]` with `[3,5]`.
      - `newInterval[0] = min(4, 3) = 3`.
      - `newInterval[1] = max(8, 5) = 8`.
      - `newInterval` is now `[3, 8]`.
      - `i` becomes `2`.

  - **Loop 2 (`i=2`)**: `intervals[2]` is `[6,7]`. Check `6 <= 8`? **True**.

      - Merge `[3,8]` with `[6,7]`.
      - `newInterval[0] = min(3, 6) = 3`.
      - `newInterval[1] = max(8, 7) = 8`.
      - `newInterval` is still `[3, 8]`.
      - `i` becomes `3`.

  - **Loop 3 (`i=3`)**: `intervals[3]` is `[8,10]`. Check `8 <= 8`? **True**.

      - Merge `[3,8]` with `[8,10]`.
      - `newInterval[0] = min(3, 8) = 3`.
      - `newInterval[1] = max(8, 10) = 10`.
      - `newInterval` is now `[3, 10]`.
      - `i` becomes `4`.

  - **Loop 4 (`i=4`)**: `intervals[4]` is `[12,16]`. Check `12 <= 10`? **False**.

  - The "Merge" loop terminates.

  - **Append Merged Interval**: `result.append(newInterval)`.

      - `result.append([3,10])`.

**State after Phase 2:** `i = 4`, `result = [[1,2], [3,10]]`, `newInterval = [3,10]`

-----

### **Phase 3: "After"**

  - **Loop 1 (`i=4`)**: `i < n` is `4 < 5` -\> True.
      - `result.append(intervals[4])` -\> `result.append([12,16])`.
      - `i` becomes `5`.
  - **Loop 2 (`i=5`)**: `i < n` is `5 < 5` -\> **False**.
  - The "After" loop terminates.

-----

### **Final Result**

  - The function returns `result`: **`[[1,2], [3,10], [12,16]]`**.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of intervals. The algorithm iterates through the `intervals` list with the index `i` exactly once.

### Space Complexity: O(n)

  - The `result` list can, in the worst case, contain all the original intervals plus the new one. The space required is proportional to the number of intervals.