# 151\. Reverse Words in a String - Solution Explanation

## Problem Overview

Given an input string `s`, the task is to reverse the order of the **words** within the string.

**Key Definitions & Rules:**

  - **Word**: A sequence of non-space characters.
  - **Input Spacing**: The input string `s` can have extra, messy spaces: leading spaces, trailing spaces, and multiple spaces between words.
  - **Output Spacing**: The returned string must have only a single space separating the words and must not contain any leading or trailing spaces.

**Examples:**

```python
Input: s = "the sky is blue"
Output: "blue is sky the"

Input: s = "  hello world  "
Output: "world hello"

Input: s = "a good   example"
Output: "example good a"
```

## Key Insights

### The "Split, Reverse, Join" Strategy

The most direct and powerful way to think about this problem in Python is to break it down into a sequence of three simple, high-level operations:

1.  **Split**: Take the messy input string and break it apart into a clean list of words.
2.  **Reverse**: Reverse the order of the words in that list.
3.  **Join**: Join the words from the reversed list back together into a clean, new string.

Python's built-in methods are perfectly designed to handle each of these steps elegantly, which allows us to avoid complex manual parsing of the string.

## Solution Approach

This solution is a direct implementation of the "Split, Reverse, Join" strategy. It is often written as a single, expressive line of code in Python.

```python
class Solution:
    def reverseWords(self, s: str) -> str:
        # 1. Split the string by any whitespace into a list of words.
        word_list = s.split()
        
        # 2. Reverse the list of words.
        reversed_list = word_list[::-1]
        
        # 3. Join the reversed list back into a string with single spaces.
        return " ".join(reversed_list)
```

For conciseness, these three steps are often chained together:

```python
class Solution:
    def reverseWords(self, s: str) -> str:
        return " ".join(s.split()[::-1])
```

## Detailed Code Analysis

Let's break down each part of the chained one-line solution `" ".join(s.split()[::-1])` with extreme detail. The code is executed from the inside out.

### **Step 1: `s.split()`**

  - **What it does**: This is the most powerful part of the solution. When `split()` is called with no arguments on a string, it does two crucial things:
    1.  It splits the string into a list of substrings using *any sequence of whitespace* as the delimiter.
    2.  It automatically **discards any empty strings** that result from leading, trailing, or multiple spaces.
  - **Example**:
      - **Input `s`**: `"  a good   example  "`
      - **Result of `s.split()`**: `['a', 'good', 'example']`
  - This single method cleanly handles all the messy spacing rules from the problem description.

### **Step 2: `[...]` (The List) `[::-1]`**

  - **What it does**: This is Python's standard slice notation for reversing a sequence. It takes the list of words generated in Step 1 and creates a new list with the elements in reverse order.
  - **Example**:
      - **Input list**: `['a', 'good', 'example']`
      - **Result of `[::-1]`**: `['example', 'good', 'a']`

### **Step 3: `" ".join(...)`**

  - **What it does**: The `.join()` method is called on a "separator" string and takes a list of strings as its argument. It concatenates all the elements from the list into a single new string, placing the separator string between each element.
  - **Example**:
      - **Separator**: `" "` (a single space)
      - **Input list**: `['example', 'good', 'a']`
      - **Result of `" ".join(...)`**: `"example good a"`

## Step-by-Step Execution Trace

Let's trace the full execution for the input `s = "  the sky   is blue  "`.

| Step | Code Being Executed | Intermediate Result | Explanation |
| :--- | :--- | :--- | :--- |
| **1** | `s.split()` | `['the', 'sky', 'is', 'blue']` | The string is split by any amount of whitespace. The leading and trailing spaces are gone, and the multiple spaces between "sky" and "is" are treated as a single delimiter. |
| **2** | `...[::-1]` | `['blue', 'is', 'sky', 'the']` | The list of words created in the previous step is reversed. |
| **3** | `" ".join(...)` | `"blue is sky the"` | The words in the reversed list are joined together into a new string, with a single space `" "` placed between each word. |
| **4** | `return ...` | `"blue is sky the"` | The final, clean string is returned as the answer. |

## Performance Analysis

### Time Complexity: O(N)

  - Where `N` is the length of the input string `s`.
  - The `split()` operation takes `O(N)` time to scan the string.
  - Reversing the list of words takes time proportional to the number of words, which is at most `O(N)`.
  - The `join()` operation also takes `O(N)` time as it needs to build the new string.
  - Overall, the complexity is linear.

### Space Complexity: O(N)

  - The `split()` method creates a new list of words, which in the worst case (e.g., `"a b c d"`) can have a total number of characters proportional to `N`. This requires `O(N)` space. The final joined string also requires `O(N)` space.

## Key Learning Points

  - **Leverage the Standard Library**: Python's built-in string and list methods are highly optimized and expressive. Recognizing when to use them (`split`, `join`, slicing) can turn a complex manual parsing task into a simple one-liner.
  - **The Power of `s.split()`**: Understanding that `s.split()` (with no arguments) is specifically designed to handle messy whitespace is crucial for many string parsing problems.
  - **Method Chaining**: Chaining operations (`s.split()[::-1]`) is a common and readable pattern in Python for performing a sequence of transformations on data.