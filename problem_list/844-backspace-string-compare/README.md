# 844\. Backspace String Compare - Solution Explanation

## Problem Overview

You are given two strings, `s` and `t`. Imagine typing each string into a separate, empty text editor. The character `#` acts like a **backspace**, deleting the character immediately before it. The task is to determine if the final text results are **equal** after processing all characters and backspaces in both strings.

**Key Rules:**

  - `#` deletes the character to its left.
  - Backspace on an empty text results in an empty text.

**Examples:**

```python
Input: s = "ab#c", t = "ad#c"
Output: true
Explanation:
- For s: type 'a', type 'b', backspace '#'(deletes 'b'), type 'c'. Final text: "ac".
- For t: type 'a', type 'd', backspace '#'(deletes 'd'), type 'c'. Final text: "ac".
Both become "ac".

Input: s = "ab##", t = "c#d#"
Output: true
Explanation:
- For s: type 'a', type 'b', backspace '#'(deletes 'b'), backspace '#'(deletes 'a'). Final text: "".
- For t: type 'c', backspace '#'(deletes 'c'), type 'd', backspace '#'(deletes 'd'). Final text: "".
Both become "".

Input: s = "a#c", t = "b"
Output: false
Explanation:
- For s: type 'a', backspace '#'(deletes 'a'), type 'c'. Final text: "c".
- For t: type 'b'. Final text: "b".
"c" is not equal to "b".
```

## Key Insights

### 1\. Simulating the Process

The most direct way to solve this is to actually simulate the typing process for each string. We need a way to keep track of the characters that *would* be in the text editor.

### 2\. The Backspace -\> LIFO Connection

The key insight comes from the backspace behavior. A backspace always deletes the **most recently typed** character. This "Last-In, First-Out" (LIFO) behavior is the defining characteristic of a **stack** data structure.

### 3\. Using a Stack

We can perfectly simulate the text editor using a stack (which can be implemented easily with a Python list):

  - When we encounter a **letter**, we add it to our editor (push it onto the stack).
  - When we encounter a **backspace (`#`)**, we delete the last typed character (pop from the stack, but only if the stack is not empty).

After processing the entire input string this way, the characters remaining on the stack, when joined together, represent the final text.

## Solution Approach

This solution uses a helper function, `build`, which takes an input string and simulates the typing process using a stack (implemented as a list). The main function calls `build` for both `s` and `t` and compares their final results.

```python
from typing import List

class Solution:
    def backspaceCompare(self, s: str, t: str) -> bool:
        
        # Helper function to simulate typing and return the final string.
        def build(input_str: str) -> str:
            # Use a list as a stack.
            stack = []
            # Iterate through the input string character by character.
            for char in input_str:
                # If it's a backspace...
                if char == '#':
                    # ...and the stack is not empty, pop the last character.
                    if stack:
                        stack.pop()
                # If it's a letter...
                else:
                    # ...push it onto the stack.
                    stack.append(char)
            # Join the remaining characters in the stack to form the final string.
            return "".join(stack)
            
        # Build the final strings resulting from typing s and t.
        final_s = build(s)
        final_t = build(t)
        
        # Compare the final strings for equality.
        return final_s == final_t
```

## Detailed Code Analysis

### The `build(input_str)` Helper Function

This function takes one of the input strings (`s` or `t`) and returns the string that would result after processing all the characters and backspaces.

**1. Initialization:**

```python
stack = []
```

  - We create an empty list. This list will store the characters that are "currently in the editor" as we simulate the typing. We will use list methods `append` (like `push`) and `pop` (like `pop`) to mimic stack behavior.

**2. The Loop:**

```python
for char in input_str:
```

  - This loop iterates through the input string (`s` or `t`) one character at a time.

**3. Handling Backspace (`#`):**

```python
if char == '#':
    if stack:
        stack.pop()
```

  - If the current character is a `#`, we need to simulate a backspace.
  - `if stack:`: This is a crucial check. We only perform a `pop` if the stack (our simulated editor) is not empty. If it's empty, a backspace does nothing.
  - `stack.pop()`: If the stack is not empty, this removes the last element that was added, perfectly simulating the backspace deleting the most recent character.

**4. Handling Letters:**

```python
else:
    stack.append(char)
```

  - If the character is not a `#`, it must be a letter.
  - `stack.append(char)`: We add the letter to the end of our list (push it onto the stack), simulating typing the character.

**5. Returning the Final String:**

```python
return "".join(stack)
```

  - After the loop has processed all characters, the `stack` contains the sequence of characters that remain in the editor.
  - `"".join(stack)` joins these characters together into a single string (e.g., `['a', 'c']` becomes `"ac"`).

### The Main `backspaceCompare` Function

```python
final_s = build(s)
final_t = build(t)
return final_s == final_t
```

  - This part is straightforward. It calls the `build` helper function for both input strings `s` and `t` to get their final resulting text.
  - It then compares these two final strings using the equality operator (`==`) and returns the boolean result (`True` if they are identical, `False` otherwise).

## Step-by-Step Execution Trace

Let's trace the `build` function for `s = "ab#c"` with extreme detail.

| `char` | `char == '#'`? | `if stack`? | Action | `stack` State |
| :--- | :--- | :--- | :--- | :--- |
| **Start** | - | - | - | `[]` |
| **'a'** | False | - | `stack.append('a')` | `['a']` |
| **'b'** | False | - | `stack.append('b')` | `['a', 'b']` |
| **'\#'** | True | `True` (`['a', 'b']` is not empty) | `stack.pop()` (removes 'b') | `['a']` |
| **'c'** | False | - | `stack.append('c')` | `['a', 'c']` |

  - The loop finishes.
  - `"".join(['a', 'c'])` is called.
  - The `build` function returns `"ac"`.

The same process for `t = "ad#c"` would also result in `"ac"`. Since `"ac" == "ac"`, the main function returns `True`.

## Performance Analysis

### Time Complexity: O(M + N)

  - Where `M` is the length of string `s` and `N` is the length of string `t`.
  - The `build` function iterates through its input string once. Stack operations (`append`, `pop`) take `O(1)` time on average.
  - We call `build` once for `s` (`O(M)`) and once for `t` (`O(N)`). The final string comparison also takes time proportional to the lengths of the resulting strings (at most `O(M+N)`).
  - The total time complexity is linear with respect to the total length of the input strings.

### Space Complexity: O(M + N)

  - In the worst case (if there are no backspaces), the stack within the `build` function can grow to the size of the input string.
  - Since we call `build` for both strings, the maximum space used could be proportional to `M + N`.