# 136\. Single Number - Solution Explanation

## Problem Overview

Given a non-empty array of integers `nums`, where every element appears twice except for one, the task is to find that single, unique element.

**Key Constraints:**

1.  **Linear Runtime Complexity**: The solution must run in `O(n)` time, meaning it should ideally process the array in a single pass.
2.  **Constant Extra Space**: The solution must use `O(1)` space, meaning you cannot use auxiliary data structures like hash maps or sets whose size grows with the input.

**Examples:**

```python
Input: nums = [2,2,1]
Output: 1

Input: nums = [4,1,2,1,2]
Output: 4
```

## Key Insights

### The Constraints are the Biggest Clue

The strict constraints of `O(n)` time and `O(1)` space rule out many common approaches:

  - A nested loop to compare each element with every other element would be `O(n²)`, which is too slow.
  - Using a hash map or a set to count frequencies would be `O(n)` time but would require `O(n)` space, violating the space constraint.

These constraints strongly suggest that the solution lies in a mathematical property or a **bitwise operation**. The perfect tool for this problem is the **XOR (exclusive OR)** operator.

### The Magic of XOR

The XOR operator (`^`) has two crucial properties that make it ideal for this problem:

1.  **A number XORed with itself is zero:** `x ^ x = 0`
2.  **A number XORed with zero is itself:** `x ^ 0 = x`

Because of these properties, if you XOR all the numbers in the list, every number that appears twice will pair up and cancel itself out (becoming zero), leaving only the single, unique number.

## Solution Approach

The solution is to iterate through the array once, accumulating the XOR sum of all the elements.

```python
from typing import List

class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        # Initialize a variable to 0.
        # XORing with 0 doesn't change the number (x ^ 0 = x).
        result = 0
        
        # Iterate through all numbers in the list.
        for num in nums:
            # Apply the XOR operation between the running result and the current number.
            result ^= num
            
        # The final result will be the single, unique number.
        return result
```

**Strategy:**

1.  **Initialize**: Start with a `result` variable set to `0`.
2.  **Iterate & Accumulate**: Loop through each `num` in the `nums` list and apply the XOR operation: `result = result ^ num`.
3.  **Return**: The final value of `result` will be the single number that did not have a pair to cancel it out.

## Deep Dive: The XOR Operator (`^` and `^=`)

### `^` (XOR - Exclusive OR)

The XOR operator works on the binary representation of numbers. It compares two numbers bit by bit. A resulting bit is `1` if **one and only one** of the corresponding bits is `1`. If both bits are the same (both `0` or both `1`), the result is `0`.

Think of it as the "one or the other, but not both" operator.

**Truth Table for XOR:**
| Bit A | Bit B | A ^ B |
| :--- | :--- | :--- |
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

**Example: `5 ^ 3`**

  * 5 in binary is `0101`
  * 3 in binary is `0011`

<!-- end list -->

```
  0101  (5)
^ 0011  (3)
------
  0110  (The result is 6)
```

### `^=` (Compound XOR Assignment)

The `^=` operator is simply a shorthand.
`result ^= num` is the exact same as writing `result = result ^ num`.
It means: "Take the current value of `result`, XOR it with `num`, and then store the new value back into `result`."

### Difference Between `^` (XOR) and `|` (OR)

While they sound similar, they behave differently when both bits are `1`.

  * **`|` (OR)**: The result is `1` if **at least one** of the bits is `1`.
  * **`^` (XOR)**: The result is `1` if **exactly one** of the bits is `1`.

**Example: `5 | 3` vs. `5 ^ 3`**

```
  0101  (5)         0101  (5)
| 0011  (3)       ^ 0011  (3)
------            ------
  0111  (Result is 7)   0110  (Result is 6)
```

Notice the first bit from the right: `1 | 1` is `1`, but `1 ^ 1` is `0`. This "canceling" property is what makes XOR so powerful for this problem.

## Step-by-Step Execution Trace

### Example 1: `nums = [2, 2, 1]`

| `num` | `result` (before `^=`) | `result` (binary) | `num` (binary) | `result` (after `^=`) |
| :--- | :--- | :--- | :--- | :--- |
| **Start** | `0` | `000` | | `0` |
| **2** | `0` | `000` | `010` | `2` (`010`) |
| **2** | `2` | `010` | `010` | `0` (`000`) |
| **1** | `0` | `000` | `001` | `1` (`001`) |

  - The function returns **1**.

### Example 2: `nums = [4, 1, 2, 1, 2]`

| `num` | `result` (before `^=`) | `result` (binary) | `num` (binary) | `result` (after `^=`) |
| :--- | :--- | :--- | :--- | :--- |
| **Start** | `0` | `000` | | `0` |
| **4** | `0` | `000` | `100` | `4` (`100`) |
| **1** | `4` | `100` | `001` | `5` (`101`) |
| **2** | `5` | `101` | `010` | `7` (`111`) |
| **1** | `7` | `111` | `001` | `6` (`110`) |
| **2** | `6` | `110` | `010` | `4` (`100`) |

  - The function returns **4**.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of elements in `nums`. We iterate through the list exactly once.

### Space Complexity: O(1)

  - We only use a single variable (`result`) to store the accumulated XOR value. The space required is constant and does not grow with the size of the input list.

## Key Learning Points

  - The constraints of a problem (like time and space complexity) are powerful hints toward the expected type of solution.
  - Bitwise operators, especially XOR, have unique mathematical properties that can solve certain problems with extreme efficiency.
  - Understanding the "canceling out" property of XOR (`x ^ x = 0`) is key to solving this and similar problems.

## Real-World Applications

  - **Data Integrity/Checksums**: XOR is used in some algorithms (like RAID parity) to check if data has been corrupted.
  - **Cryptography**: XOR is a fundamental component in many encryption algorithms because it's easily reversible (`(A ^ B) ^ B = A`).
  - **Graphics**: Used for simple sprite drawing on a screen, as XORing an image onto a background and then XORing it again restores the original background.