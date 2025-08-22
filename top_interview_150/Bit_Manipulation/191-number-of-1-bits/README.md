# 191\. Number of 1 Bits - Solution Explanation

## Problem Overview

Given a positive integer `n`, the task is to write a function that returns the number of `1`s in its binary representation. This count is also known as the **Hamming weight**.

**Key Definitions:**

  - **Binary Representation**: The base-2 number system, which uses only the digits 0 and 1. For example, the decimal number 11 is `1011` in binary.
  - **Set Bit**: A bit that has a value of 1.
  - **Hamming Weight**: The total number of set bits (1s) in a binary string.

**Examples:**

```python
Input: n = 11 (binary: 1011)
Output: 3
Explanation: The binary string 1011 has three '1's.

Input: n = 128 (binary: 10000000)
Output: 1
Explanation: The binary string 10000000 has one '1'.
```

## Key Insights

### Processing Bits Individually

The most fundamental way to solve this is to inspect every single bit of the input number `n`. We can create a simple loop that runs until all bits have been checked. In each step of the loop, we need to do two things:

1.  Check the value of the current last bit.
2.  Get rid of that last bit so we can inspect the next one in the following iteration.

**Bitwise operators** are the perfect, highly efficient tools for these tasks.

## Solution Approach

This solution uses a `while` loop and bitwise operators to check each bit of the number `n` one by one.

```python
class Solution:
    def hammingWeight(self, n: int) -> int:
        count = 0
        
        # Loop until all bits have been shifted out (n becomes 0).
        while n > 0:
            # Check if the last bit is a 1.
            if (n & 1):
                count += 1
            
            # Shift all bits to the right to process the next bit.
            n >>= 1
            
        return count
```

**Strategy:**

1.  **Initialize Counter**: Start with `count = 0`.
2.  **Loop**: Continue as long as `n` is not zero (meaning there are still bits to check).
3.  **Check Last Bit**: Use the bitwise AND operator (`n & 1`) to see if the last bit is a `1`. If it is, increment `count`.
4.  **Shift Bits**: Use the right shift operator (`n >>= 1`) to discard the last bit and move all other bits one position to the right.
5.  **Return**: Once the loop finishes, `count` will hold the total number of `1` bits.

## Deep Dive: Bitwise Operators `&` and `>>=`

These operators are the core of the solution. Let's understand them with a concrete example.

### `n & 1` (Bitwise AND with 1)

This operation isolates the very last bit of a number. It answers the question: "Is this number odd?"

  * The `&` operator compares two numbers bit by bit. A resulting bit is `1` only if the corresponding bits in both numbers are `1`.
  * The number `1` in binary is `...0001`.

**Example: `n = 11` (binary `1011`)**

```
  1011  (11 in decimal)
& 0001  (1 in decimal)
------
  0001  (The result is 1)
```

Since the result is `1`, the `if (n & 1)` condition is true. The last bit of `11` was indeed a `1`.

**Example: `n = 10` (binary `1010`)**

```
  1010  (10 in decimal)
& 0001  (1 in decimal)
------
  0000  (The result is 0)
```

Since the result is `0`, the `if (n & 1)` condition is false. The last bit of `10` was a `0`.

-----

### `n >>= 1` (Right Shift by 1)

This operation effectively discards the last bit of a number, which is the same as performing integer division by 2.

  * The `>>` operator takes all the bits in a number and shifts them one position to the right. The rightmost bit is dropped.

**Example: `n = 11` (binary `1011`)**

  * Before: `1011`
  * After `n >>= 1`: `_101` -\> `0101` (The leading bit is filled with 0)
  * The new value of `n` is `0101` in binary, which is **5** in decimal.

## Step-by-Step Execution Trace

### Example: `hammingWeight(11)`

| `n` (start of loop) | `n` (binary) | `n & 1` | `count` (after check) | `n` (after `>>= 1`) |
| :--- | :--- | :--- | :--- | :--- |
| **11** | `1011` | 1 | 1 | 5 (`0101`) |
| **5** | `0101` | 1 | 2 | 2 (`0010`) |
| **2** | `0010` | 0 | 2 | 1 (`0001`) |
| **1** | `0001` | 1 | 3 | 0 (`0000`) |

  - The `while n > 0` loop now terminates because `n` is `0`.
  - The function returns the final `count`, which is **3**.

## Performance Analysis

### Time Complexity: O(1)

  - The loop runs once for each bit in the integer. Since the input is a fixed-size integer (32 or 64 bits depending on the system), the number of iterations is constant.

### Space Complexity: O(1)

  - We only use one variable (`count`) to store the result. The space required is constant.

## Alternative Approaches Comparison

### Approach 1: Bitwise Manipulation (Our Solution)

  - ✅ **Time: O(1)**, **Space: O(1)**.
  - ✅ The most efficient, language-agnostic method.
  - ✅ Demonstrates a fundamental understanding of bit manipulation.

### Approach 2: Built-in String Conversion

```python
class Solution:
    def hammingWeight(self, n: int) -> int:
        return bin(n).count('1')
```

  - ✅ Very concise and readable in Python.
  - ❌ Less performant due to the overhead of converting the integer to a string.
  - ❌ Might not be allowed in interviews that are specifically testing bit manipulation skills.

## Key Learning Points

  - The concept of Hamming weight is simply counting `1`s in a binary representation.
  - Bitwise operators (`&`, `>>`) provide a highly efficient way to inspect and manipulate individual bits of a number.
  - The `n & 1` pattern is a standard trick to check the last bit (or check for oddness).
  - The `n >>= 1` pattern is a standard trick to discard the last bit (or perform integer division by 2).