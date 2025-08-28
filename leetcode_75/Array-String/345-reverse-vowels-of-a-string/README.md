# 345\. Reverse Vowels of a String - Solution Explanation

## Problem Overview

Given a string `s`, the task is to reverse the positions of **only the vowels** within the string. The consonants must remain in their original positions.

**Vowel Definition:**
The vowels are `'a'`, `'e'`, `'i'`, `'o'`, and `'u'`. The problem specifies that they can appear in both **lowercase and uppercase**.

**Examples:**

```python
Input: s = "hello"
Output: "holle"
# The vowels are 'e' and 'o'. They swap positions.

Input: s = "leetcode"
Output: "leotcede"
# The vowels are 'e', 'o', 'e', 'e'.
# The first 'e' swaps with the last 'e'.
# The 'o' swaps with the second 'e'.
```

## Key Insights

### The Two-Pointer Technique

The core of this problem is swapping elements from opposite ends of a sequence while ignoring others (the consonants). This is a classic scenario for the **two-pointer** algorithm.

We can place one pointer at the beginning of the string (`left`) and another at the end (`right`). We then move them towards each other, and when they both point to vowels, we swap them. This ensures that the first vowel is swapped with the last, the second vowel with the second-to-last, and so on, which is exactly what "reversing" means.

### String Immutability in Python

In Python, strings are **immutable**, which means they cannot be changed after they are created. You cannot directly swap characters in a string like you would in a list. The standard way to handle this is to:

1.  Convert the string to a `list` of characters.
2.  Perform all the swaps on the `list`.
3.  Convert the `list` back into a single string at the end.

## Solution Approach

This solution implements the two-pointer technique. It first converts the string to a list, then uses `left` and `right` pointers to find and swap vowels until the pointers meet or cross.

```python
class Solution:
    def reverseVowels(self, s: str) -> str:
        # A set provides very fast O(1) lookups to check if a character is a vowel.
        vowels = {'a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'}
        
        # Convert the string to a list of characters to allow modification.
        s_list = list(s)
        
        # Initialize left and right pointers.
        left, right = 0, len(s_list) - 1
        
        while left < right:
            # Move the left pointer forward until it lands on a vowel.
            while left < right and s_list[left] not in vowels:
                left += 1
            
            # Move the right pointer backward until it lands on a vowel.
            while left < right and s_list[right] not in vowels:
                right -= 1
                
            # If the pointers haven't crossed, swap the vowels.
            if left < right:
                s_list[left], s_list[right] = s_list[right], s_list[left]
                
                # Move both pointers inward to continue the search.
                left += 1
                right -= 1
                
        # Join the list of characters back into a string.
        return "".join(s_list)
```

## Detailed Code Analysis

### Step 1: Initialization

```python
vowels = {'a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'}
s_list = list(s)
left, right = 0, len(s_list) - 1
```

  - `vowels`: We create a `set` for all vowel characters. A set is much faster than a list for checking membership (`... in vowels`) because it has an average O(1) lookup time.
  - `s_list`: We convert the input string `s` into a list of its characters, like `['l', 'e', 'e', 't', 'c', 'o', 'd', 'e']`.
  - `left`, `right`: We initialize our two pointers. `left` starts at the first character (index 0), and `right` starts at the last character.

### Step 2: The Main Loop

```python
while left < right:
```

  - This is the main condition that keeps the process going. As long as the `left` pointer is to the left of the `right` pointer, there are still characters to check. The moment they meet or cross, we know we have processed the entire string.

### Step 3: Finding the Vowels

```python
while left < right and s_list[left] not in vowels:
    left += 1

while left < right and s_list[right] not in vowels:
    right -= 1
```

  - These are two inner loops that "scan" for the next vowel.
  - The first loop moves the `left` pointer forward, skipping over any consonants.
  - The second loop moves the `right` pointer backward, skipping over any consonants.
  - The `left < right` check inside these loops is a crucial safety measure to ensure they don't run past each other during the scan.

### Step 4: The Swap

```python
if left < right:
    s_list[left], s_list[right] = s_list[right], s_list[left]
    left += 1
    right -= 1
```

  - After the inner loops, if `left` is still less than `right`, it means `left` is pointing to a vowel and `right` is pointing to a vowel.
  - `s_list[left], s_list[right] = s_list[right], s_list[left]` is a Pythonic way to swap the two elements in the list.
  - After the swap, we must move both pointers inward (`left += 1`, `right -= 1`) to continue searching for the next pair of vowels.

### Step 5: Final String Creation

```python
return "".join(s_list)
```

  - After the main `while` loop finishes, our `s_list` contains the characters in their final, correct order.
  - `"".join(s_list)` efficiently combines all the characters in the list back into a single string.

## Deep Dive: `while` Loops

A `while` loop is a fundamental control structure in programming. Think of it like giving a robot a command that it must repeat **as long as a certain condition is true**.

  - **The Condition**: `while left < right:` The condition is `left < right`.
  - **The Action**: The code inside the loop is the action.
  - **The Process**:
    1.  The robot first checks the condition. Is `left` less than `right`?
    2.  If **True**, it performs all the actions inside the loop one time. After it's done, it goes back to step 1 to check the condition again.
    3.  If **False**, it ignores the actions inside the loop and skips to the code that comes after the loop.

This is perfect for our problem because we don't know exactly how many swaps we'll need, but we know we should keep going as long as our pointers haven't met in the middle.

## Deep Dive: `"".join()` Method

The `.join()` method is a tool that belongs to strings. It's used to build a single string from a list of smaller strings.

  - **The "Glue"**: The string you call the method on is the "glue" or separator. In `"".join(result)`, the glue is an empty string `""`.
  - **The "Pieces"**: The list you pass to the method (`result`) contains the pieces you want to stick together.
  - **The Action**: It goes through the list of pieces and puts the glue in between each one.

**Example**:
Imagine you have pieces of paper with letters on them: `['l', 'e', 'o', 't', 'c', 'e', 'd', 'e']`.

  - `"".join(...)` is like taping them together with no space in between, creating `"leotcede"`.
  - `"-".join(...)` is like taping them together with a hyphen in between, creating `"l-e-o-t-c-e-d-e"`.

## Step-by-Step Execution Trace

### Example: `s = "leetcode"`

1.  **Initialization**:
      * `vowels = {'a', 'e', ...}`
      * `s_list = ['l', 'e', 'e', 't', 'c', 'o', 'd', 'e']`
      * `left = 0`, `right = 7`

| `left` | `right` | `s_list[left]` | `s_list[right]` | Action | `s_list` State |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **0** | **7** | 'l' | 'e' | `left` is not a vowel. `left++`. | `['l', 'e', 'e', 't', 'c', 'o', 'd', 'e']` |
| **1** | **7** | 'e' | 'e' | Both are vowels. Swap them. `left++`, `right--`. | `['l', 'e', 'e', 't', 'c', 'o', 'd', 'e']` |
| **2** | **6** | 'e' | 'd' | `right` is not a vowel. `right--`. | `['l', 'e', 'e', 't', 'c', 'o', 'd', 'e']` |
| **2** | **5** | 'e' | 'o' | Both are vowels. Swap them. `left++`, `right--`. | `['l', 'e', 'o', 't', 'c', 'e', 'd', 'e']` |
| **3** | **4** | 't' | 'c' | Neither is a vowel. `left++`, `right--`. | `['l', 'e', 'o', 't', 'c', 'e', 'd', 'e']` |
| **4** | **3** | - | - | `left < right` is now `False`. Loop terminates. | `['l', 'e', 'o', 't', 'c', 'e', 'd', 'e']` |

2.  **Final Step**:
      * `return "".join(['l', 'e', 'o', 't', 'c', 'e', 'd', 'e'])`
      * The final output is **`"leotcede"`**.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the length of the string. Although there are nested loops, the `left` and `right` pointers each traverse the string at most once.

### Space Complexity: O(n)

  - We create a list of characters (`s_list`) from the string, which requires space proportional to the length of the string.