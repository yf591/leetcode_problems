# 12\. Integer to Roman - Solution Explanation

## Problem Overview

You are given an integer `num` (between 1 and 3999). The task is to convert this integer into its corresponding Roman numeral representation as a string.

**Roman Numeral Rules:**
The conversion is based on seven symbols. The core idea is to represent numbers by combining these symbols. Usually, this is additive (e.g., `VI` = 5 + 1 = 6), but there are special "subtractive" rules for 4s and 9s to avoid repeating a symbol four times (e.g., 4 is `IV`, not `IIII`).

**Examples:**

```python
Input: num = 58
Output: "LVIII"
Explanation: L = 50, V = 5, III = 3.

Input: num = 1994
Output: "MCMXCIV"
Explanation: M = 1000, CM = 900, XC = 90, IV = 4.
```

## Key Insights

### The Inefficient Approach

A naive solution might involve a lot of complex `if/else` logic for each decimal place. You would handle the thousands place, then the hundreds, then tens, then ones, with special checks for 4s and 9s in each category. This can become very messy and hard to read.

### The Greedy Algorithm Insight

A much cleaner and more scalable approach is a **greedy algorithm**. The key insight is to treat all Roman numeral representations, including the special subtractive ones (`CM`, `CD`, `XC`, `XL`, `IX`, `IV`), as distinct "symbols" or "chunks."

If we create a list of all these symbols and their corresponding integer values, and we **sort this list from the largest value to the smallest**, we can build the Roman numeral by greedily subtracting the largest possible chunk from our number at each step.

For example, to convert `900`, the greedy choice is not `D` (500) followed by `CCCC`. By including `CM` (900) in our list of symbols and checking it before `D`, our algorithm will correctly choose `CM` first. This works for all cases.

## Solution Approach

This solution defines a static, ordered list of all possible Roman numeral symbols (from `M` down to `I`, including the subtractive forms). It then iterates through this list, greedily subtracting values from the input `num` and appending the corresponding symbols to a result list until `num` becomes zero.

```python
class Solution:
    def intToRoman(self, num: int) -> str:
        # Step 1: Create a mapping of values to Roman numeral symbols.
        # It is CRUCIAL that this list is ordered from largest value to smallest.
        symbols = [
            (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
            (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
            (10, "X"), (9, "IX"), (5, "V"), (4, "IV"),
            (1, "I")
        ]
        
        # Step 2: Initialize an empty list to build the result string efficiently.
        result_parts = []
        
        # Step 3: Iterate through the list of symbols, from largest to smallest.
        for value, symbol in symbols:
            # Step 4: For each symbol, greedily subtract its value as many times as possible.
            while num >= value:
                # Append the corresponding symbol to our result list.
                result_parts.append(symbol)
                # Subtract the value from our number.
                num -= value
                
        # Step 5: Join the list of symbol parts into the final string.
        return "".join(result_parts)
```

## Detailed Code Analysis

### Step 1: The Symbol Map

```python
symbols = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    # ... and so on
]
```

  - This is the heart of the solution. It's a pre-defined list of tuples, where each tuple contains an integer `value` and its corresponding string `symbol`.
  - **The order is absolutely critical.** By sorting this in descending order of value, we ensure our greedy approach works. We always try to match the largest possible chunk first (e.g., we check for `900` ("CM") before we check for `500` ("D") or `100` ("C")).

### Step 2: The Main `for` Loop

```python
result_parts = []
for value, symbol in symbols:
    # ...
```

  - We initialize an empty list, `result_parts`. Appending to a list and joining at the end is much more efficient in Python than repeatedly concatenating strings with `+`.
  - The `for` loop iterates through each `(value, symbol)` pair in our `symbols` list, starting with the largest.

### Step 3: The Greedy `while` Loop

```python
while num >= value:
    result_parts.append(symbol)
    num -= value
```

  - This inner loop is what performs the greedy subtraction.
  - **`while num >= value:`**: It checks if the remaining `num` is big enough to accommodate the current symbol's `value`. For a given symbol, this loop might run multiple times. For example, if `num = 3000` and the current symbol is `(1000, "M")`, this loop will run three times. If `num = 994` and the symbol is `(900, "CM")`, it will run once.
  - **`result_parts.append(symbol)`**: If the condition is met, we add the Roman numeral `symbol` to our list of parts.
  - **`num -= value`**: We then subtract the `value` from `num`, and the `while` loop checks its condition again with the new, smaller `num`.

### Step 4: Final String Construction

```python
return "".join(result_parts)
```

  - After the `for` loop has finished, `num` will have been reduced to `0`, and `result_parts` will contain all the necessary Roman numeral characters in the correct order.
  - `"".join(result_parts)` is an efficient Python method that concatenates all the strings in the list into a single final string.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `num = 3749` with extreme detail.

1.  **Initialization**: `num = 3749`, `result_parts = []`.

| `(value, symbol)` | `num` (start) | `while num >= value`? | Action | `result_parts` |
| :--- | :--- | :--- | :--- | :--- |
| **(1000, "M")** | 3749 | `3749>=1000`-\>True | Append "M", num=2749 | `["M"]` |
| | 2749 | `2749>=1000`-\>True | Append "M", num=1749 | `["M", "M"]` |
| | 1749 | `1749>=1000`-\>True | Append "M", num=749 | `["M", "M", "M"]`|
| | 749 | `749>=1000`-\>False | Loop ends. | |
| **(900, "CM")** | 749 | `749>=900`-\>False | - | `["M", "M", "M"]` |
| **(500, "D")** | 749 | `749>=500`-\>True | Append "D", num=249 | `[..., "D"]` |
| | 249 | `249>=500`-\>False | Loop ends. | |
| **(400, "CD")** | 249 | `249>=400`-\>False | - | `[..., "D"]` |
| **(100, "C")** | 249 | `249>=100`-\>True | Append "C", num=149 | `[..., "D", "C"]` |
| | 149 | `149>=100`-\>True | Append "C", num=49 | `[..., "D", "C", "C"]` |
| | 49 | `49>=100`-\>False | Loop ends. | |
| **(90, "XC")** | 49 | `49>=90`-\>False | - | `[..., "D", "C", "C"]` |
| **(50, "L")** | 49 | `49>=50`-\>False | - | `[..., "D", "C", "C"]` |
| **(40, "XL")** | 49 | `49>=40`-\>True | Append "XL", num=9 | `[..., "C", "C", "XL"]` |
| | 9 | `9>=40`-\>False | Loop ends. | |
| **(10, "X")** | 9 | `9>=10`-\>False | - | `[..., "C", "C", "XL"]` |
| **(9, "IX")** | 9 | `9>=9`-\>True | Append "IX", num=0 | `[..., "XL", "IX"]` |
| | 0 | `0>=9`-\>False | Loop ends. | |
| **(Remaining)** | 0 | - | All remaining `while` checks will be false. | `[..., "XL", "IX"]` |

2.  **Final Step**: The outer `for` loop finishes.
      - The code returns `"".join(["M", "M", "M", "D", "C", "C", "XL", "IX"])`.
      - The final output is **`"MMMDCCXLIX"`**.

## Performance Analysis

### Time Complexity: O(1)

  - The number of symbols in our `symbols` list is constant (13). The outer `for` loop runs a fixed number of times. The inner `while` loop for any given symbol can run at most 3 times (e.g., for 'M' in 3000). Therefore, the total number of operations is bounded by a small constant and does not grow with the size of the input `num` (within its constraints).

### Space Complexity: O(1)

  - The space used for the `symbols` list is constant. The `result_parts` list will hold at most a few characters (the longest Roman numeral for a number up to 3999 is `MMMDCCCLXXXVIII`, which is 15 characters). This is also constant space.

## Key Learning Points

  - **Greedy Algorithms**: This problem is a perfect demonstration of a greedy algorithm. By making the locally optimal choice at each step (subtracting the largest possible value), we arrive at the globally correct solution.
  - **Data-Driven Logic**: Instead of writing complex `if/else` statements, the solution is driven by a well-structured list of data (`symbols`). This makes the code cleaner, easier to understand, and easier to modify.
  - **Efficient String Building**: Using a list to collect parts of a string and then calling `"".join()` at the end is a standard, efficient pattern in Python.