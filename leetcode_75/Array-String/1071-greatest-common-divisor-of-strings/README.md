# 1071\. Greatest Common Divisor of Strings - Solution Explanation

## Problem Overview

Given two strings, `str1` and `str2`, the task is to find the **largest string `x`** that "divides" both of them.

**"Divides" Definition:**
We say that a string `t` "divides" a string `s` if and only if `s` can be formed by concatenating `t` with itself one or more times.

  - **Example:** `"ABC"` divides `"ABCABC"` because `"ABCABC" = "ABC" + "ABC"`.
  - **Example:** `"AB"` does **not** divide `"ABC"` because `"ABC"` cannot be formed by repeating `"AB"`.

**The Goal:** Find the longest string `x` that is a divisor of both `str1` and `str2`.

**Examples:**

```python
Input: str1 = "ABCABC", str2 = "ABC"
Output: "ABC"
# "ABC" is the largest string that divides both.

Input: str1 = "ABABAB", str2 = "ABAB"
Output: "AB"
# "AB" divides "ABABAB" (3 times) and "ABAB" (2 times).

Input: str1 = "LEET", str2 = "CODE"
Output: ""
# There is no common string that can form both.
```

## Key Insights

### The Concatenation Property

This is the most critical insight. If a common divisor string `x` exists, it means both `str1` and `str2` are made of repeating copies of `x`.

  - Let `str1 = x * m` (meaning `x` repeated `m` times)
  - Let `str2 = x * n` (meaning `x` repeated `n` times)

If this is true, then what happens when we concatenate `str1` and `str2`?

  - `str1 + str2` = `(x repeated m times)` + `(x repeated n times)` = `x` repeated `m+n` times.
  - `str2 + str1` = `(x repeated n times)` + `(x repeated m times)` = `x` repeated `n+m` times.

Therefore, a common divisor can only exist if **`str1 + str2` is identical to `str2 + str1`**. This gives us a simple, powerful test to see if a solution is even possible.

### The Length Property

If a common divisor string `x` exists, its length must be a common divisor of the lengths of `str1` and `str2`. To find the *greatest* common divisor string, its length must be the **Greatest Common Divisor (GCD)** of the two string lengths.

## Solution Approach

The solution combines the two insights above into a simple, three-step algorithm.

```python
import math

class Solution:
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        # Step 1: Check if a common divisor is even possible using the concatenation property.
        if str1 + str2 != str2 + str1:
            return ""
        
        # Step 2: If a divisor exists, its length must be the GCD of the two string lengths.
        gcd_length = math.gcd(len(str1), len(str2))
        
        # Step 3: The greatest common divisor string is the prefix of this length.
        return str1[:gcd_length]
```

**Strategy:**

1.  **Check Compatibility**: First, perform the concatenation check. If `str1 + str2` is not equal to `str2 + str1`, we know immediately that no common divisor exists, so we return an empty string.
2.  **Find GCD Length**: If the check passes, we are guaranteed that a solution exists. We then calculate the greatest common divisor of the lengths of the two strings.
3.  **Extract Prefix**: The answer is simply the prefix of `str1` (or `str2`) that has the calculated GCD length.

## Detailed Code Analysis

### Step 1: The Compatibility Check

```python
if str1 + str2 != str2 + str1:
    return ""
```

  - This is the powerful first step. It validates the fundamental structure of the strings. If they are not composed of the same repeating unit, their concatenations in different orders will not be the same, and we can stop right away. This handles cases like `"LEET"` and `"CODE"` perfectly.

### Step 2: Calculating the GCD Length

```python
gcd_length = math.gcd(len(str1), len(str2))
```

  - `len()` gets the integer lengths of the strings.
  - `math.gcd()` is a standard Python function that efficiently calculates the greatest common divisor of two integers. The result is the length of our answer string. For example, `math.gcd(6, 4)` is `2`.

### Step 3: Returning the Result

```python
return str1[:gcd_length]
```

  - This uses Python's string slicing. `str1[:k]` returns a new string containing the first `k` characters of `str1`. Because of the initial check in Step 1, we are guaranteed that this prefix is the correct greatest common divisor string.

## Step-by-Step Execution Trace

### Example 1: `str1 = "ABABAB"`, `str2 = "ABAB"`

1.  **Start `gcdOfStrings("ABABAB", "ABAB")`**.
2.  **Compatibility Check**:
      * `str1 + str2` -\> `"ABABAB"` + `"ABAB"` -\> `"ABABABABAB"`
      * `str2 + str1` -\> `"ABAB"` + `"ABABAB"` -\> `"ABABABABAB"`
      * Is `"ABABABABAB" != "ABABABABAB"`? No, the condition is **False**. The code proceeds.
3.  **GCD of Lengths**:
      * `len(str1)` is `6`.
      * `len(str2)` is `4`.
      * `gcd_length = math.gcd(6, 4)` calculates `2`.
4.  **Extract Prefix**:
      * `return str1[:2]`
      * The slice of `"ABABAB"` from the start up to index 2 (exclusive) is `"AB"`.
5.  **Final Output**: The function returns `"AB"`.

### Example 2: `str1 = "LEET"`, `str2 = "CODE"`

1.  **Start `gcdOfStrings("LEET", "CODE")`**.
2.  **Compatibility Check**:
      * `str1 + str2` -\> `"LEET"` + `"CODE"` -\> `"LEETCODE"`
      * `str2 + str1` -\> `"CODE"` + `"LEET"` -\> `"CODELEET"`
      * Is `"LEETCODE" != "CODELEET"`? Yes, the condition is **True**.
3.  **Return**: The function immediately returns `""`.

## Performance Analysis

### Time Complexity: O(M + N)

  - Where `M` and `N` are the lengths of the strings. The dominant operations are the string concatenations and comparison, which take time proportional to the sum of the lengths. The GCD calculation is very fast (`O(log(min(M,N)))`).

### Space Complexity: O(M + N)

  - The space is required to create the temporary concatenated strings for the initial comparison.

## Key Learning Points

  - How a problem about strings can be elegantly solved using a concept from number theory (GCD).
  - The powerful property that if two strings `s1` and `s2` are formed by a repeating unit `x`, then `s1+s2` must equal `s2+s1`. This is a useful pattern for similar problems.
  - The importance of using built-in, optimized functions like `math.gcd` when applicable.