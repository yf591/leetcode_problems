# 82\. Remove Duplicates from Sorted List II - Solution Explanation

## Problem Overview

You are given the `head` of a **sorted** linked list. The task is to delete **all nodes that have duplicate numbers**, leaving only the numbers that were unique in the original list.

**The Crucial Rule:**
Unlike simpler versions of this problem, if a number appears more than once, *all* of its occurrences must be removed.

**Examples:**

```python
Input: head = [1,2,3,3,4,4,5]
Output: [1,2,5]
Explanation: The two 3's and the two 4's are completely removed.

Input: head = [1,1,1,2,3]
Output: [2,3]
Explanation: The entire block of 1's at the beginning is removed.
```

## Key Insights

### The Challenge: Deleting the Entire Block

The main difficulty is that when you identify a duplicate, you can't just delete the current node. You have to remove the entire contiguous block of nodes with that same value. This requires a "look-ahead" approach.

### The "Predecessor" and the "Dummy Node"

1.  **Look-Ahead**: As we traverse the list with a main pointer (let's call it `head`), we can determine if `head` is part of a duplicate block by checking if its value is the same as the next node's value (`head.val == head.next.val`).
2.  **The Predecessor Pointer (`pred`)**: To delete a node or a block of nodes, we need a pointer to the node *just before* the block. We'll call this the **`pred`** (predecessor) pointer. `pred` will always point to the last known "safe" node that is guaranteed to be in our final list. The deletion is done by re-wiring `pred.next`.
3.  **The Dummy Node Trick**: What if the duplicates are at the very beginning of the list (e.g., `[1,1,2,3]`)? The `pred` for the block of `1`s would be `None`, which would require special `if` conditions to handle. To make our code clean and universal, we use a **`dummy` node**. This is a placeholder node that we place before the original `head`. Our `pred` pointer can then start at this `dummy` node, ensuring that every node/block in the list always has a valid predecessor.

## Solution Approach

This solution uses a `dummy` node to simplify edge cases. It then uses two main pointers: `pred`, which points to the tail of the "good" list, and `head`, which is used to scan the original list.

```python
from typing import Optional

class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # 1. Create a dummy node that points to the head of the list.
        dummy = ListNode(0, head)
        
        # 2. 'pred' is the predecessor node, the last node before the
        #    sublist we are currently inspecting.
        pred = dummy
        
        # 3. We use the 'head' pointer to traverse the list.
        while head:
            # 4. Check if the current node is the start of a duplicate section.
            if head.next and head.val == head.next.val:
                # 5. If it is, skip all nodes with this value.
                #    The inner loop moves 'head' to the last node of the duplicate block.
                while head.next and head.val == head.next.val:
                    head = head.next
                
                # 6. Re-wire the predecessor's 'next' to skip the entire block.
                pred.next = head.next
            else:
                # 7. If the node is not a duplicate, it's safe. Advance 'pred'.
                pred = pred.next
            
            # 8. Advance the main pointer to continue the scan.
            head = head.next
            
        # 9. Return the head of the cleaned list.
        return dummy.next
```

## Detailed Code Analysis

### Step 1 & 2: Initialization

```python
dummy = ListNode(0, head)
pred = dummy
```

  - We create a `dummy` node. Its `next` pointer is set to the original `head`. Our list is now conceptually `Dummy -> 1 -> 2 -> ...`.
  - We initialize our `pred` pointer to point at this `dummy` node. `pred`'s job is to always be the tail of the list we are building.

### Step 3: The Main Traversal Loop

```python
while head:
```

  - We use the `head` variable itself as our main traversal pointer. The loop will continue until we have processed every node in the original list.

### Step 4: The Look-Ahead Check

```python
if head.next and head.val == head.next.val:
```

  - This is the core of the logic. It checks if the current `head` is the start of a duplicate block.
  - `head.next`: This is a safety check to ensure we don't try to access `.val` on a `None` object at the end of the list.
  - `head.val == head.next.val`: This compares the current node's value with the next one.

### Step 5 & 6: Handling Duplicates

```python
while head.next and head.val == head.next.val:
    head = head.next
pred.next = head.next
```

  - If the `if` condition is true, we enter this block.
  - **Inner `while` loop**: This loop's job is to fast-forward the `head` pointer through the entire block of duplicates. When this loop finishes, `head` will be pointing to the *last* node in the duplicate sequence.
  - **`pred.next = head.next`**: This is the actual deletion. We re-wire the `next` pointer of our last "good" node (`pred`) to skip over the entire duplicate block and point to whatever came after it. `head.next` is the first node of the next, potentially different, value.

### Step 7: Handling Unique Nodes

```python
else:
    pred = pred.next
```

  - If the initial `if` condition was false, it means the current `head` is a unique node (at least for now). It is safe to keep.
  - We advance `pred` to this "good" node. We do this by setting `pred = pred.next`. Note that since `pred.next` was already pointing to `head`, this is the same as `pred = head`.

### Step 8: Advancing the Main Pointer

```python
head = head.next
```

  - This line executes at the end of every outer loop iteration. It advances our main `head` pointer one step forward so we can process the next part of the list.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `head = [1, 2, 3, 3, 4]` with extreme detail.

### **Initial State:**

```
pred    head
  |       |
Dummy -> 1 -> 2 -> 3 -> 3 -> 4 -> None
```

-----

### **Loop 1 (`head` at Node 1)**

  - **Look-ahead**: `head.next` is Node 2. `1 != 2`.
  - **Action**: `else` block runs. `pred` advances to Node 1. `head` advances to Node 2.
  - **State**:
    ```
    Dummy -> 1 -> 2 -> 3 -> 3 -> 4 -> None
             |    |
            pred head
    ```

-----

### **Loop 2 (`head` at Node 2)**

  - **Look-ahead**: `head.next` is Node 3. `2 != 3`.
  - **Action**: `else` block runs. `pred` advances to Node 2. `head` advances to Node 3.
  - **State**:
    ```
    Dummy -> 1 -> 2 -> 3 -> 3 -> 4 -> None
                  |    |
                 pred head
    ```

-----

### **Loop 3 (`head` at the first Node 3)**

  - **Look-ahead**: `head.next` is the second Node 3. `3 == 3`. **Duplicate found\!**
  - **Action**: `if` block runs.
      - **Inner `while` loop**: `head` moves to the second Node 3. Loop ends.
      - `pred.next = head.next`: `Node(2).next` is set to the second `Node(3).next`, which is `Node(4)`. The block of 3s is now skipped.
      - `head` (main pointer) advances to the second Node 3's `next`, which is `Node(4)`.
  - **State**:
    ```
            pred             head
             |                |
    Dummy -> 1 -> 2 ------> 4 -> None
                  |
                  3 -> 3 -> 4 (orphaned)
    ```

-----

### **Loop 4 (`head` at Node 4)**

  - **Look-ahead**: `head.next` is `None`. The `if` condition is false.
  - **Action**: `else` block runs. `pred` advances to Node 4. `head` advances to `None`.
  - **State**:
    ```
    Dummy -> 1 -> 2 -> 4 -> None
                       |
                      pred
    ```

-----

### **End of Loop**

  - The `while head:` condition is now false. The loop terminates.

### **Final Result**

  - The function returns `dummy.next`, which is `Node(1)`.
  - The final list is `1 -> 2 -> 4 -> None`.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of nodes. Although there is a nested `while` loop, each node in the list is visited exactly once by the main `head` pointer. The inner loop only advances this same pointer, so it doesn't add to the complexity.

### Space Complexity: O(1)

  - The solution uses only a few pointers (`dummy`, `pred`, `head`). The space required is constant and does not depend on the size of the list.