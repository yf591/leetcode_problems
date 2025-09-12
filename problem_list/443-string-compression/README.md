# 443\. String Compression - Solution Explanation

## Problem Overview

You are given an array of characters, `chars`. The task is to compress the array by grouping consecutive repeating characters.

**Compression Rules:**

1.  Find groups of consecutive, identical characters.
2.  If a group's length is 1 (e.g., `["a"]`), its representation is just the character itself.
3.  If a group's length is greater than 1 (e.g., `["a", "a", "a"]`), its representation is the character followed by the digits of its length (e.g., `['a', '3']`).
4.  If a group's length is 10 or more (e.g., 12), the length is split into individual characters (e.g., `['1', '2']`).

**Key Constraints:**

  - The compression must happen **in-place**, meaning you must modify the input `chars` array directly.
  - You must use **O(1) constant extra space**.
  - The function should return the **new length** of the compressed array.

**Example:**

```python
Input: chars = ["a","a","b","b","c","c","c"]
Output: Return 6, and the first 6 characters of the array should be: ["a","2","b","2","c","3"]
Explanation: "aa" becomes "a2", "bb" becomes "b2", "ccc" becomes "c3".
```

[Image showing characters being grouped and compressed]

## Key Insights

### In-Place Modification with Two Pointers

The constraints of modifying the array **in-place** with **constant extra space** are the biggest clues. This immediately tells us we cannot create a new array to build our result.

This leads to the **read-and-write pointer** technique (a form of two-pointer algorithm).

  - One pointer, which we'll call the **`read` pointer**, will scan through the original, unmodified parts of the array.
  - A second pointer, the **`write` pointer**, will lag behind. Its job is to overwrite the array from the beginning with the new, compressed data.

The reason this is safe is that the compressed version of a group is always shorter than or equal to its original length (e.g., `"a"` -\> `"a"`, `"aa"` -\> `"a2"`, `"aaa"` -\> `"a3"`). This guarantees that our `write` pointer will never overtake our `read` pointer, so we'll never overwrite data we haven't processed yet.

## Solution Approach

This solution iterates through the array, identifying groups of consecutive characters. It uses a `read` pointer (`i`) to find the end of each group and a `write` pointer (`j`) to place the compressed result back into the start of the same array.

```python
from typing import List

class Solution:
    def compress(self, chars: List[str]) -> int:
        i = 0  # The read pointer, scans the original array.
        j = 0  # The write pointer, tracks the end of the compressed part.
        n = len(chars)

        while i < n:
            # Identify the character for the current group.
            char_group = chars[i]
            count = 0
            
            # Count the number of consecutive occurrences of this character.
            # This inner loop advances the read pointer 'i' to the end of the group.
            while i < n and chars[i] == char_group:
                count += 1
                i += 1
            
            # --- Write the compressed result back to the array ---
            
            # 1. Write the character of the group.
            chars[j] = char_group
            j += 1

            # 2. If the group was larger than 1, write its count.
            if count > 1:
                # Convert the count to a string to handle multi-digit numbers (e.g., 12).
                for digit in str(count):
                    chars[j] = digit
                    j += 1
            
        # 'j' is now the new length of the compressed array.
        return j
```

## Detailed Code Analysis

### Step 1: Pointer Initialization

```python
i = 0  # read_pointer
j = 0  # write_pointer
n = len(chars)
```

  - We set up our two pointers. `i` will be used to scan ahead and find the end of character groups. `j` will be used to carefully place the compressed data at the beginning of the array.

### Step 2: The Main (Outer) Loop

```python
while i < n:
```

  - This loop ensures we process the entire array. Since the inner loop moves `i` forward by the size of each group, this outer loop effectively processes the array one group at a time.

### Step 3: Finding and Counting a Group

```python
char_group = chars[i]
count = 0
while i < n and chars[i] == char_group:
    count += 1
    i += 1
```

  - At the start of the outer loop, `chars[i]` is the first character of a new group.
  - The inner `while` loop is the counting mechanism. It continues as long as we're still in the array and the character at `i` is the same as the one we started the group with.
  - Crucially, this loop **advances the `i` pointer**. When it finishes, `i` will be pointing at the start of the *next* group.

### Step 4: Writing the Compressed Data

```python
chars[j] = char_group
j += 1

if count > 1:
    for digit in str(count):
        chars[j] = digit
        j += 1
```

  - First, we always write the character of the group (e.g., 'a') to the `j` position and advance `j`.
  - Then, we check if the `count` was greater than 1.
  - If it was, we convert the integer `count` to a string. The `for digit in str(count)` loop is a clever way to handle counts of any size. For example, if `count` is `12`, `str(count)` is `"12"`, and the loop will run twice: once for the character `'1'` and once for the character `'2'`.
  - For each digit, we write it to the `j` position and advance `j`.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `chars = ['a', 'a', 'b', 'b', 'b', 'c']` with extreme detail.

1.  **Initialization**: `i = 0`, `j = 0`, `n = 6`.

-----

### **First Group ('a')**

  - **Outer loop starts.** `i=0`.
  - `char_group` is set to `chars[0]`, which is `'a'`. `count` is `0`.
  - **Inner count loop:**
      - `i=0`: `chars[0]=='a'`. `count` becomes 1, `i` becomes 1.
      - `i=1`: `chars[1]=='a'`. `count` becomes 2, `i` becomes 2.
      - `i=2`: `chars[2]=='b'`. Loop terminates.
  - `count` is **2**.
  - **Write character**: `chars[j=0] = 'a'`. `j` becomes 1. Array is `['a', 'a', 'b', 'b', 'b', 'c']`.
  - **Write count**: `count > 1` is true. `str(2)` is `"2"`.
      - Loop for `digit` in `"2"`: `chars[j=1] = '2'`. `j` becomes 2.
  - **End of group processing.** `i` is `2`, `j` is `2`. Array is `['a', '2', 'b', 'b', 'b', 'c']`.

-----

### **Second Group ('b')**

  - **Outer loop continues.** `i=2`.
  - `char_group` is set to `chars[2]`, which is `'b'`. `count` is `0`.
  - **Inner count loop:**
      - `i=2`: `chars[2]=='b'`. `count` becomes 1, `i` becomes 3.
      - `i=3`: `chars[3]=='b'`. `count` becomes 2, `i` becomes 4.
      - `i=4`: `chars[4]=='b'`. `count` becomes 3, `i` becomes 5.
      - `i=5`: `chars[5]=='c'`. Loop terminates.
  - `count` is **3**.
  - **Write character**: `chars[j=2] = 'b'`. `j` becomes 3. Array is `['a', '2', 'b', 'b', 'b', 'c']`.
  - **Write count**: `count > 1` is true. `str(3)` is `"3"`.
      - Loop for `digit` in `"3"`: `chars[j=3] = '3'`. `j` becomes 4.
  - **End of group processing.** `i` is `5`, `j` is `4`. Array is `['a', '2', 'b', '3', 'b', 'c']`.

-----

### **Third Group ('c')**

  - **Outer loop continues.** `i=5`.
  - `char_group` is set to `chars[5]`, which is `'c'`. `count` is `0`.
  - **Inner count loop:**
      - `i=5`: `chars[5]=='c'`. `count` becomes 1, `i` becomes 6.
      - `i=6`: `i < n` is false. Loop terminates.
  - `count` is **1**.
  - **Write character**: `chars[j=4] = 'c'`. `j` becomes 5. Array is `['a', '2', 'b', '3', 'c', 'c']`.
  - **Write count**: `count > 1` is false. This step is skipped.
  - **End of group processing.** `i` is `6`, `j` is `5`.

-----

### **End of Algorithm**

  - The outer `while i < n` loop condition (`6 < 6`) is now false. The loop terminates.
  - The function returns the final value of `j`, which is **5**.
  - The first 5 characters of the array have been modified to `['a', '2', 'b', '3', 'c']`.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of characters in the `chars` array. Although there are nested `while` loops, the read pointer `i` traverses the array exactly once from beginning to end.

### Space Complexity: O(1)

  - The modification is done in-place. We only use a few variables to track our state (`i`, `j`, `count`, etc.), so the extra space required is constant.