# 202\. Happy Number - Solution Explanation

## Problem Overview

Write an algorithm to determine if a number `n` is a "happy number."

**Happy Number Definition**
A number is happy if the following process, starting with the number, eventually ends at 1:

1.  Replace the number with the sum of the squares of its digits.
2.  Repeat this process.

If the process reaches 1, the original number is **happy**. If the process gets stuck in a cycle of numbers that does not include 1, the number is **unhappy**.

**Examples**

```python
Input: n = 19
Output: true
Explanation:
1^2 + 9^2 = 1 + 81 = 82
8^2 + 2^2 = 64 + 4 = 68
6^2 + 8^2 = 36 + 64 = 100
1^2 + 0^2 + 0^2 = 1 + 0 + 0 = 1 (The process ends at 1)

Input: n = 2
Output: false
Explanation:
2^2 = 4
4^2 = 16
1^2 + 6^2 = 1 + 36 = 37
... this process continues and eventually enters a cycle (4 -> 16 -> 37 -> 58 -> 89 -> 145 -> 42 -> 20 -> 4) that does not include 1.
```

## Key Insights

### Cycle Detection

The core of this problem is recognizing that the process will either reach 1 or get stuck in a loop. How do we know if we're in a loop? We'll eventually see a number that we have **already seen before**.

This transforms the problem into a **cycle detection** problem. The most straightforward way to detect a cycle is to keep a record of every number we encounter. If we generate a new number and find it in our record, we've found a cycle.

A **hash set** is the perfect data structure for this because it allows us to add numbers and check for their existence very quickly.

## Solution Approach

This solution simulates the process step-by-step. It uses a helper function to calculate the sum of squares and a set to keep track of the numbers seen so far to detect cycles.

```python
class Solution:
    def isHappy(self, n: int) -> bool:
        
        def get_sum_of_squares(num: int) -> int:
            output = 0
            while num > 0:
                digit = num % 10
                output += digit ** 2
                num //= 10
            return output

        seen = set()
        
        while n != 1 and n not in seen:
            seen.add(n)
            n = get_sum_of_squares(n)
            
        return n == 1
```

**Strategy**

1.  **Initialize a Set**: Create an empty set called `seen` to store the history of numbers encountered.
2.  **Loop**: Start a loop that continues as long as the current number `n` is not 1 and has not been seen before.
3.  **Record and Update**: Inside the loop, add the current `n` to the `seen` set. Then, calculate the next number in the sequence using a helper function and update `n`.
4.  **Check Result**: The loop terminates for one of two reasons:
      * `n` becomes 1 (a happy number).
      * `n` is found in `seen` (an unhappy number caught in a cycle).
        The final check `return n == 1` correctly handles both outcomes.

## Deep Dive: `get_sum_of_squares`

This helper function's job is to take a number (e.g., `82`) and return the sum of the squares of its digits (`8^2 + 2^2 = 68`). It does this by extracting the digits one by one.

**How it works**

  - The **modulo operator (`% 10`)** gets the last digit of a number.
  - **Integer division (`// 10`)** removes the last digit from a number.

### Step-by-Step Example: `get_sum_of_squares(82)`

| Iteration | `num` (start) | `digit` (`num % 10`) | `output` (after `+=`) | `num` (after `// 10`) |
| :--- | :--- | :--- | :--- | :--- |
| **Start** | `82` | | `0` | `82` |
| **1** | `82` | `2` | `0 + 2^2 = 4` | `8` |
| **2** | `8` | `8` | `4 + 8^2 = 68` | `0` |

  - The `while num > 0` loop now terminates because `num` is `0`.
  - The function returns the final `output`, which is **68**.

## Deep Dive: Python's `set`

  * **What is a `set`?** 🗃️
    A `set` is a collection of items, much like a list, but with two key differences:

    1.  **No Duplicates**: A set cannot contain duplicate elements. If you try to add an item that's already there, nothing happens.
    2.  **Unordered**: The items in a set have no specific order.

  * **Why is it so useful here?**
    The most important feature of a set is its speed. Checking if an item is `in` a set is extremely fast (O(1) on average), no matter how many items are in the set.

      - Think of a set like a **guest list at a party**. When a new person (`n`) arrives, you can instantly check your list (`seen`) to see if they've been here before (`n in seen`). If not, you add them to the list (`seen.add(n)`). This is much faster than scanning a long, ordered list from beginning to end every time.

## Step-by-Step Execution Trace

### Example: `isHappy(19)`

| `n` | `seen` (start of loop) | `n != 1`? | `n not in seen`? | Action |
| :--- | :--- | :--- | :--- | :--- |
| **19** | `{}` | True | True | Add 19 to `seen`. `n` becomes `82`. |
| **82** | `{19}` | True | True | Add 82 to `seen`. `n` becomes `68`. |
| **68** | `{19, 82}` | True | True | Add 68 to `seen`. `n` becomes `100`. |
| **100** | `{19, 82, 68}` | True | True | Add 100 to `seen`. `n` becomes `1`. |
| **1** | `{19, 82, 68, 100}`| **False** | - | Loop terminates. |

  - The function proceeds to `return n == 1`. Since `n` is `1`, it returns **`True`**.

## Performance Analysis

### Time Complexity: O(log n)

  - The size of the numbers in the sequence does not grow indefinitely. For any number with many digits, the sum of the squares of its digits will be a number with fewer digits. The process quickly converges to smaller numbers, making the time complexity related to the number of digits, which is logarithmic.

### Space Complexity: O(log n)

  - The space is determined by the number of unique values stored in the `seen` set before a cycle is detected or 1 is reached. This is also related to the number of digits in the input.

## Key Learning Points

  - Recognizing problems that can be solved by detecting cycles.
  - Using a hash set (`set`) for efficient tracking of "seen" states.
  - Using modulo (`%`) and integer division (`//`) to manipulate the digits of a number.