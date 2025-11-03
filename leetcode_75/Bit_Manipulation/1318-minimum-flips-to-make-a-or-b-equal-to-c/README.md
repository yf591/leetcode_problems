# 1318\. Minimum Flips to Make a OR b Equal to c - Solution Explanation

## Problem Overview

You are given three integers: `a`, `b`, and `c`. The goal is to find the **minimum number of bit flips** required on `a` and `b` so that the bitwise `OR` operation (`a | b`) results in `c`.

**Key Definitions:**

  - **Bitwise OR (`|`)**: An operation that compares two numbers bit by bit. The resulting bit is `1` if *at least one* of the corresponding bits is `1`.
  - **Flip**: Changing a single bit from `0` to `1` or `1` to `0`.

**Example:**

```
Input: a = 2, b = 6, c = 5
Binary:
a = 010
b = 110
c = 101

Goal: (a | b) must equal c
     a_bit | b_bit == c_bit

Position 0 (rightmost): a=0, b=0, c=1. We need 0|0 to be 1. This fails.
We must flip one bit (e.g., a=0->1).  (Flips: 1)

Position 1: a=1, b=1, c=0. We need 1|1 to be 0. This fails.
We must flip both a=1->0 and b=1->0. (Flips: 2)

Position 2: a=0, b=1, c=1. We need 0|1 to be 1. This is already true. (Flips: 0)

Total Flips: 1 + 2 + 0 = 3.
```

## Deep Dive: What are Bitwise Operators?

This problem is impossible to solve without understanding bitwise operators. They are operations that work on the individual bits (0s and 1s) of a number, rather than the number's decimal value.

Let's use two example 4-bit numbers: `x = 5` (binary `0101`) and `y = 3` (binary `0011`).

| Operator | Name | Rule | Example | Result (Decimal) |
| :--- | :--- | :--- | :--- | :--- |
| **`&`** | **AND** | `1` if **both** bits are `1`. | `0101 & 0011 = 0001` | 1 |
| **`Vertical bar (Bitwise OR) operator`** | **OR** | `1` if **at least one** bit is `1`.| `0101 Vertical bar 0011 = 0111` | 7 |
| **`^`** | **XOR** | `1` if bits are **different**. | `0101 ^ 0011 = 0110` | 6 |
| **`~`** | **NOT** | Flips all bits (32-bit). | `~5 (0101) = ...11111010` | -6 (2's complement) |
| **`<<`** | **Left Shift**| Moves all bits to the left. | `0101 << 1 = 1010` | 10 (Multiplies by 2) |
| **`>>`** | **Right Shift**| Moves all bits to the right. | `0101 >> 1 = 0010` | 2 (Divides by 2) |

### **Operators Used in This Solution:**

1.  **`& 1` (Get Last Bit)**: This is a "bit mask." It performs an AND with `1` (binary `...0001`). This zeroes out all bits *except* the last one. It's a perfect, `O(1)` way to check if the last bit of a number is `0` or `1`.

      - `6 & 1` -\> `110 & 001 = 000` -\> **`0`** (Even)
      - `5 & 1` -\> `101 & 001 = 001` -\> **`1`** (Odd)

2.  **`>>= 1` (Move to Next Bit)**: This is the "right shift assignment" operator. It shifts all bits in the number one position to the right, effectively discarding the last bit and moving the next bit into the last position, ready to be checked.

      - `a = 6` (`110`)
      - `a >>= 1`
      - `a` is now `3` (`011`).

## Key Insights

The problem must be solved bit by bit. We can iterate through all the bit positions (up to 32, or until all numbers are 0) and sum the flips required at each position.

For any single bit position, there are two main cases, based on our target `c_bit`:

  * **Case 1: Target bit `c_bit` is `0`.**

      - We need `a_bit | b_bit` to be `0`.
      - The *only* way for an OR to be `0` is if **both `a_bit` and `b_bit` are `0`**.
      - If `a_bit` is `1`, we must flip it (1 flip).
      - If `b_bit` is `1`, we must flip it (1 flip).
      - The total flips needed in this case is `a_bit + b_bit`. (If `a_bit=1, b_bit=0`, 1 flip. If `a_bit=1, b_bit=1`, 2 flips).

  * **Case 2: Target bit `c_bit` is `1`.**

      - We need `a_bit | b_bit` to be `1`.
      - This is already true if `a_bit=1` or `b_bit=1`.
      - The *only* time this fails is if **both `a_bit` and `b_bit` are `0`**.
      - In that single failure case, we need to flip one of them to `1`. This costs exactly **1 flip**.

## Solution Approach

This solution implements the bit-by-bit analysis. It uses a `while` loop to iterate through each bit position of the three numbers. It checks the last bit of each number, applies the logic from our two cases, and then right-shifts all three numbers to process the next bit position.

```python
from typing import List

class Solution:
    def minFlips(self, a: int, b: int, c: int) -> int:
        
        flips = 0
        
        # We loop as long as any of the numbers still have bits (are not 0).
        # This will check all 32 bits if necessary.
        while a > 0 or b > 0 or c > 0:
            
            # --- Get the last bit for each number ---
            a_bit = a & 1
            b_bit = b & 1
            c_bit = c & 1
            
            # --- Apply our two cases ---
            
            # Case 1: The target bit (c_bit) is 1
            if c_bit == 1:
                # We need (a_bit | b_bit) to be 1.
                # A flip is only needed if both are 0.
                if (a_bit | b_bit) == 0:
                    flips += 1
            
            # Case 2: The target bit (c_bit) is 0
            else: # c_bit == 0
                # We need (a_bit | b_bit) to be 0.
                # This means both a_bit and b_bit must be 0.
                # We add 1 flip for each bit that is currently 1.
                flips += (a_bit + b_bit)
            
            # --- Move to the next bit position ---
            # Right-shift all numbers to process the next bit.
            a >>= 1
            b >>= 1
            c >>= 1
            
        return flips
```

## Detailed Code Analysis

### Step 1: Initialization

```python
flips = 0
```

  - We initialize our accumulator variable that will store the total number of flips.

### Step 2: The Main Loop

```python
while a > 0 or b > 0 or c > 0:
```

  - This `while` loop continues as long as *any* of the numbers are non-zero. If a number is `0`, it means all its bits have been processed (or were 0 to begin with). The loop will only stop once all bits of all three numbers have been considered.

### Step 3: Bit Extraction

```python
a_bit = a & 1
b_bit = b & 1
c_bit = c & 1
```

  - Using the `& 1` (bitwise AND) mask, we extract the least significant bit (the rightmost bit) from each number. The result will be either `0` or `1`.

### Step 4: Logic for `c_bit == 1`

```python
if c_bit == 1:
    if (a_bit | b_bit) == 0:
        flips += 1
```

  - We check our target. If `c_bit` is `1`, we *want* `a_bit | b_bit` to be `1`.
  - We check if our current state is failing: `(a_bit | b_bit) == 0`. This only happens when `a_bit` is 0 AND `b_bit` is 0.
  - If it's failing, we must perform **one flip** (e.g., change `a_bit` from 0 to 1) to satisfy the condition.

### Step 5: Logic for `c_bit == 0`

```python
else: # c_bit == 0
    flips += (a_bit + b_bit)
```

  - If our target `c_bit` is `0`, we *want* `a_bit | b_bit` to be `0`. This only happens if `a_bit=0` and `b_bit=0`.
  - `flips += (a_bit + b_bit)` is a very clever and concise way to count the needed flips.
      - If `a_bit=1` and `b_bit=1`, `a_bit + b_bit = 2`. We need 2 flips.
      - If `a_bit=1` and `b_bit=0`, `a_bit + b_bit = 1`. We need 1 flip.
      - If `a_bit=0` and `b_bit=1`, `a_bit + b_bit = 1`. We need 1 flip.
      - If `a_bit=0` and `b_bit=0`, `a_bit + b_bit = 0`. We need 0 flips.
  - This line perfectly handles all sub-cases for when `c_bit` is `0`.

### Step 6: Advancing to the Next Bit

```python
a >>= 1
b >>= 1
c >>= 1
```

  - We use the right shift assignment operator to "chop off" the last bit of each number. This moves the next bit into the last position, ready to be processed in the next loop iteration.

## Step-by-Step Execution Trace

Let's trace the algorithm with `a = 2, b = 6, c = 5` with extreme detail.

  - **Initial State**: `a=2` (`010`), `b=6` (`110`), `c=5` (`101`), `flips = 0`

| Loop | `a` / `b` / `c` (binary) | `a_bit` | `b_bit` | `c_bit` | Logic Check | `flips` (after) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Start** | `010` / `110` / `101` | - | - | - | - | 0 |
| **1** | `010` / `110` / `101` | 0 | 0 | 1 | `c_bit==1`. Check `a_bit|b_bit == 0`? `(0|0)==0` is True. Add 1 flip. | **1** |
| (Shift) | `01` / `11` / `10` | - | - | - | - | 1 |
| **2** | `01` / `11` / `10` | 1 | 1 | 0 | `c_bit==0`. Add `a_bit+b_bit` (`1+1`). Add 2 flips. | **3** |
| (Shift) | `0` / `1` / `1` | - | - | - | - | 3 |
| **3** | `0` / `1` / `1` | 0 | 1 | 1 | `c_bit==1`. Check `a_bit|b_bit == 0`? `(0|1)==0` is False. Add 0 flips. | 3 |
| (Shift) | `0` / `0` / `0` | - | - | - | - | 3 |
| **End** | `0` / `0` / `0` | - | - | - | Loop condition `a>0 or b>0 or c>0` is False. Loop stops. | - |

  - **Final Step**: The loop terminates. The function returns the final `flips` value, which is **3**.

## Performance Analysis

### Time Complexity: O(log N)

  - Where `N` is the maximum value of `a`, `b`, or `c`.
  - The algorithm's work is proportional to the number of bits in the largest number, not its decimal value. The number of bits in a number `N` is `log₂(N)`.
  - Since the constraints are based on 32-bit integers, the loop will run at most 32 times, making it `O(32)`, which is effectively constant time, `O(1)`.

### Space Complexity: O(1)

  - We only use a few variables (`flips`, `a_bit`, `b_bit`, `c_bit`). The space required is constant and does not depend on the input size.