# 238\. Product of Array Except Self - Solution Explanation

## Problem Overview

You are given an array of integers `nums`. The task is to create a new array, `answer`, where each element `answer[i]` is the product of all the elements in the original `nums` array **except for the element at index `i`**.

**Key Constraints:**

  - The algorithm must run in **O(n)** time.
  - You are **not allowed to use the division operator**.

**Examples:**

```python
Input: nums = [1,2,3,4]
Output: [24,12,8,6]
Explanation:
- answer[0] = 2 * 3 * 4 = 24
- answer[1] = 1 * 3 * 4 = 12
- answer[2] = 1 * 2 * 4 = 8
- answer[3] = 1 * 2 * 3 = 6

Input: nums = [-1,1,0,-3,3]
Output: [0,0,9,0,0]
```

## Key Insights

### The "No Division" Challenge

The most obvious solution would be to first calculate the total product of all numbers in the array, and then for each element `nums[i]`, calculate `total_product / nums[i]`. However, the "no division" rule forbids this and forces us to find a more clever approach.

### Prefix and Suffix Products

The key insight is that the product of all elements except `nums[i]` can be broken down into two distinct parts:

1.  The product of all elements to the **left** of `nums[i]` (the "prefix product").
2.  The product of all elements to the **right** of `nums[i]` (the "suffix product").

`answer[i] = (prefix_product_at_i) * (suffix_product_at_i)`

We can calculate all the prefix products in one pass (left-to-right) and all the suffix products in a second pass (right-to-left).

## Solution Approach

This solution efficiently calculates the final result in two passes over the array. We use the `answer` array itself as a workspace to first store the prefix products and then multiply them by the suffix products.

```python
from typing import List

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        # 1. Initialize the answer array with all 1s.
        answer = [1] * n
        
        # --- Pass 1: Calculate and store the prefix products ---
        prefix_product = 1
        for i in range(n):
            # For index i, store the product of all elements to its left.
            answer[i] = prefix_product
            # Then, update the prefix product for the next iteration.
            prefix_product *= nums[i]
            
        # --- Pass 2: Calculate suffix products and get the final result ---
        suffix_product = 1
        for i in range(n - 1, -1, -1):
            # Multiply the existing prefix product by the suffix product.
            answer[i] *= suffix_product
            # Then, update the suffix product for the next iteration.
            suffix_product *= nums[i]
            
        return answer
```

**Strategy:**

1.  **Initialize `answer` array**: Create the final `answer` array and fill it with `1`s.
2.  **Left Pass**: Make a pass from left to right. For each index `i`, `answer[i]` is first set to the product of all elements to its left.
3.  **Right Pass**: Make a pass from right to left. For each index `i`, multiply the current value in `answer[i]` (which is the prefix product) by the product of all elements to its right.

## Detailed Code Analysis

### Step 1: Initialization

```python
n = len(nums)
answer = [1] * n
```

  - We create our `answer` array. It's crucial to initialize it with `1`s, because `1` is the multiplicative identity (anything multiplied by 1 is itself).

### Step 2: The First Pass (Left to Right)

```python
prefix_product = 1
for i in range(n):
    answer[i] = prefix_product
    prefix_product *= nums[i]
```

  - We initialize a running `prefix_product` to `1`.
  - **`answer[i] = prefix_product`**: This is the key. For the current index `i`, we first assign the `prefix_product` that has been accumulated from all elements *before* `i`.
  - **`prefix_product *= nums[i]`**: After using the `prefix_product`, we update it by multiplying it with the current number `nums[i]`. This prepares it to be correct for the *next* index, `i+1`.

### Step 3: The Second Pass (Right to Left)

```python
suffix_product = 1
for i in range(n - 1, -1, -1):
    answer[i] *= suffix_product
    suffix_product *= nums[i]
```

  - This works just like the first pass but in reverse.
  - **`answer[i] *= suffix_product`**: We take the value already in `answer[i]` (which is the product of everything to the left) and multiply it by the `suffix_product` (the product of everything to the right). This gives us the final desired result for index `i`.
  - **`suffix_product *= nums[i]`**: We then update the `suffix_product` by including the current number, preparing it for the next index to the left (`i-1`).

## Step-by-Step Execution Trace

Let's trace the algorithm for `nums = [1, 2, 3, 4]` with extreme detail.

1.  **Initialization**: `n = 4`, `answer = [1, 1, 1, 1]`

-----

### **Pass 1: Prefix Products (Left to Right)**

  - **Initial State**: `prefix_product = 1`

| `i` | `prefix_product` (at start of loop) | Action (`answer[i] = prefix_product`) | `prefix_product` (at end of loop) | `answer` Array State |
| :-- | :--- | :--- | :--- | :--- |
| **0** | 1 | `answer[0] = 1` | `1 * nums[0]` -\> `1 * 1 = 1` | `[1, 1, 1, 1]` |
| **1** | 1 | `answer[1] = 1` | `1 * nums[1]` -\> `1 * 2 = 2` | `[1, 1, 1, 1]` |
| **2** | 2 | `answer[2] = 2` | `2 * nums[2]` -\> `2 * 3 = 6` | `[1, 1, 2, 1]` |
| **3** | 6 | `answer[3] = 6` | `6 * nums[3]` -\> `6 * 4 = 24`| `[1, 1, 2, 6]` |

  - **End of Pass 1**: The `answer` array now stores the prefix product for each position: `[1, 1, 2, 6]`.

-----

### **Pass 2: Suffix Products (Right to Left)**

  - **Initial State**: `suffix_product = 1`

| `i` | `suffix_product` (at start of loop) | Action (`answer[i] *= suffix_product`) | `suffix_product` (at end of loop) | `answer` Array State |
| :-- | :--- | :--- | :--- | :--- |
| **3** | 1 | `answer[3] = 6 * 1 = 6` | `1 * nums[3]` -\> `1 * 4 = 4` | `[1, 1, 2, 6]` |
| **2** | 4 | `answer[2] = 2 * 4 = 8` | `4 * nums[2]` -\> `4 * 3 = 12` | `[1, 1, 8, 6]` |
| **1** | 12| `answer[1] = 1 * 12 = 12`| `12 * nums[1]` -\> `12 * 2 = 24`| `[1, 12, 8, 6]` |
| **0** | 24| `answer[0] = 1 * 24 = 24`| `24 * nums[0]` -\> `24 * 1 = 24`| `[24, 12, 8, 6]` |

  - **End of Pass 2**: The `answer` array is now `[24, 12, 8, 6]`.

-----

4.  **Return**: The function returns the final `answer` array.

## Performance Analysis

### Time Complexity: O(n)

  - The algorithm makes two separate, non-nested passes through the array of length `n`. The total number of operations is proportional to `n + n = 2n`, which simplifies to `O(n)`.

### Space Complexity: O(1)

  - The problem states that the output array does not count as extra space. Besides the `answer` array, we only use a few constant-space variables (`n`, `prefix_product`, `suffix_product`).

## Key Learning Points

  - **Prefix/Suffix Pattern**: The idea of using prefix and suffix calculations is a powerful technique for solving many array problems that require information about elements on both sides of an index.
  - **Problem Decomposition**: This solution breaks a complex requirement (product of everything else) into two simpler parts (product of the left, product of the right) that can be solved with simple loops.
  - **In-Place State Management**: Using the output array itself as a workspace to store intermediate results (the prefix products) is an efficient use of space.