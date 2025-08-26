# 380\. Insert Delete GetRandom O(1) - Solution Explanation

## Problem Overview

The goal is to design a data structure, `RandomizedSet`, that can store a set of unique integers and perform three operations, all in **average O(1) time complexity**:

1.  **`insert(val)`**: Adds an item `val` to the set if it's not already there.
2.  **`remove(val)`**: Removes an item `val` from the set if it exists.
3.  **`getRandom()`**: Returns a random element from the set with equal probability for all elements.

## Key Insights

### The O(1) Time Complexity Challenge

The requirement for all three methods to work in **O(1) average time** is the central challenge. Let's analyze standard Python data structures:

  * **List (or Array)**

      * `append(val)`: `O(1)`. Great for insertion.
      * `getRandom()`: Can be done in `O(1)` by picking a random index. Great for random access.
      * `remove(val)`: Requires searching for `val` (`O(n)`) and then shifting elements (`O(n)`). **This is too slow.**

  * **Set or Dictionary (Hash Map)**

      * `add(val)` (`insert`): `O(1)` on average. Great.
      * `remove(val)`: `O(1)` on average. Great.
      * `getRandom()`: **Not O(1)**. Sets and dictionaries do not have indices, so you can't just pick a random index. You would have to convert to a list first, which is an `O(n)` operation.

### The Hybrid Solution

Neither a list nor a dictionary alone can satisfy all constraints. The key insight is to **combine them** to leverage the strengths of both:

1.  A **List** will store the actual numbers. This gives us `O(1)` `getRandom` by picking a random index.
2.  A **Dictionary (Hash Map)** will store the location of each number within the list. This gives us `O(1)` lookup to find any number's index, which will help us overcome the slow `remove` operation of a list. The map will store `{value: index_in_list}`.

## Solution Approach

This solution maintains a list and a dictionary in sync. The `insert` and `getRandom` methods are straightforward, while the `remove` method uses a clever "swap-and-pop" trick to achieve `O(1)` time.

```python
import random

class RandomizedSet:
    def __init__(self):
        # Dictionary maps a value to its index in the list
        self.val_to_index = {}
        # List stores the actual values for O(1) random access
        self.val_list = []

    def insert(self, val: int) -> bool:
        if val in self.val_to_index:
            return False
        
        self.val_to_index[val] = len(self.val_list)
        self.val_list.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.val_to_index:
            return False

        # --- The O(1) Removal Trick ---
        index_to_remove = self.val_to_index[val]
        last_val = self.val_list[-1]

        # 1. Move the last element to the position of the element to remove.
        self.val_list[index_to_remove] = last_val
        
        # 2. Update the index of the moved element in the dictionary.
        self.val_to_index[last_val] = index_to_remove

        # 3. Remove the last element from the list (now a duplicate). This is fast.
        self.val_list.pop()
        
        # 4. Remove the target value from the dictionary.
        del self.val_to_index[val]
        
        return True

    def getRandom(self) -> int:
        return random.choice(self.val_list)
```

## Detailed Code Analysis

### `__init__(self)`

```python
self.val_to_index = {}
self.val_list = []
```

  - Initializes the two core data structures. `val_list` will hold the numbers, and `val_to_index` will act as our high-speed directory to find where each number lives in the list.

### `insert(self, val: int)`

```python
if val in self.val_to_index:
    return False
```

  - This is an `O(1)` average time check using the dictionary to see if the value already exists.

<!-- end list -->

```python
self.val_to_index[val] = len(self.val_list)
self.val_list.append(val)
```

  - If the value is new, we first record its position in the dictionary. Its index will be the current size of the list (e.g., if the list has 3 items at indices 0, 1, 2, the new item will be at index 3).
  - Then we append the value to the list. `append` is an `O(1)` operation.

### `remove(self, val: int)`

This is the most complex method. It achieves `O(1)` removal by avoiding a linear search and a shift.

```python
# 1. Get the index of the element we want to remove (`val`)
#    and the value of the very last element in the list.
index_to_remove = self.val_to_index[val]
last_val = self.val_list[-1]
```

  - Both of these are `O(1)` operations.

<!-- end list -->

```python
# 2. Overwrite the element to be removed with the last element.
self.val_list[index_to_remove] = last_val
```

  - The element `val` is now effectively gone from its original position. That spot now holds the value that used to be at the end of the list.

<!-- end list -->

```python
# 3. Update the dictionary for the element we just moved.
self.val_to_index[last_val] = index_to_remove
```

  - This is a critical step. We must update our dictionary to record the new location of `last_val`.

<!-- end list -->

```python
# 4. Remove the last element from the list.
self.val_list.pop()
```

  - The last element is now a duplicate of the one we just moved. Removing the last element of a list is an `O(1)` operation.

<!-- end list -->

```python
# 5. Remove the original `val` from our dictionary.
del self.val_to_index[val]
```

  - The removal is now complete from both data structures.

### `getRandom(self)`

```python
return random.choice(self.val_list)
```

  - Python's `random.choice()` is specifically designed to select a random element from a list (a sequence with indices) in `O(1)` time.

## Step-by-Step Execution Trace

Let's trace a sequence of operations to see the "swap-and-pop" trick in detail.

| Operation | `val_list` State | `val_to_index` State | Explanation |
| :--- | :--- | :--- | :--- |
| **`__init__()`** | `[]` | `{}` | Initialize empty structures. |
| **`insert(10)`** | `[10]` | `{10: 0}` | `10` is new. Append to list, add `10: 0` to map. |
| **`insert(20)`** | `[10, 20]` | `{10:0, 20:1}` | `20` is new. Append, add `20:1`. |
| **`insert(30)`** | `[10, 20, 30]`| `{10:0, 20:1, 30:2}` | `30` is new. Append, add `30:2`. |
| **`remove(20)`** | `[10, 20, 30]`| `{10:0, 20:1, 30:2}` | **Begin `remove(20)`.** `val=20`. |
| | | | 1. Find index of `20`: `index_to_remove = 1`. Find last value: `last_val = 30`. |
| | `[10, 30, 30]`| `{10:0, 20:1, 30:2}` | 2. Copy `30` into index `1`, overwriting `20`. |
| | `[10, 30, 30]`| `{10:0, 20:1, 30:1}` | 3. Update map for `30`: its new index is `1`. |
| | `[10, 30]` | `{10:0, 20:1, 30:1}` | 4. `pop()` the last element from the list. |
| | `[10, 30]` | `{10:0, 30:1}` | 5. `del` the entry for `20` from the map. |
| **`getRandom()`** | `[10, 30]` | `{10:0, 30:1}` | Returns either `10` or `30` with equal probability. |

## Performance Analysis

### Time Complexity: O(1) on average

  - **`insert`**: `O(1)` on average. A dictionary check and a list append are both `O(1)`.
  - **`remove`**: `O(1)` on average. All steps—dictionary lookups, list access by index, `list.pop()`, and dictionary deletion—are `O(1)`.
  - **`getRandom`**: `O(1)`.

### Space Complexity: O(N)

  - Where `N` is the number of elements in the set. Both the list and the dictionary will store `N` elements.

## Key Learning Points

  - **Combining Data Structures**: No single built-in data structure meets all requirements. The solution is to combine a list and a dictionary to leverage the strengths of both.
  - **The Swap-and-Pop Trick**: This is a crucial and widely applicable pattern for achieving `O(1)` removal from an array or list when the order of elements does not need to be preserved.
  - **Synchronization is Key**: The list and the dictionary must always be kept perfectly in sync for the data structure to remain consistent.