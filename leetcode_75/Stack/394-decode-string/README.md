# 394\. Decode String - Solution Explanation

## Problem Overview

You are given an encoded string `s`. The task is to decode it and return the original string.

**The Encoding Rule:**
The format is `k[encoded_string]`, where the `encoded_string` inside the square brackets is repeated exactly `k` times. `k` is always a positive integer.

**Key Feature:** The encoding can be nested inside other encodings.

**Examples:**

```python
Input: s = "3[a]2[bc]"
Output: "aaabcbc"
# "a" is repeated 3 times, then "bc" is repeated 2 times.

Input: s = "3[a2[c]]"
Output: "accaccacc"
# First, the inner "2[c]" becomes "cc".
# This is combined with "a" to make "acc".
# Finally, "acc" is repeated 3 times.

Input: s = "2[abc]3[cd]ef"
Output: "abcabccdcdcdef"
```

## Key Insights

### Nested Structure -\> Stack

The key insight comes from the nested brackets. A structure like `3[a2[c]]` is recursive. To decode the outer part, you must first decode the inner part. This "pause and resume" pattern, where you have to finish an inner task before you can complete the outer one, is a classic sign that a **stack** is the perfect data structure.

A stack operates on a **Last-In, First-Out (LIFO)** principle. It's like a stack of plates: you put a new plate on top and you take a plate from the top. We can use it to "save our work."

**The Strategy:**

  - We'll iterate through the string, building up a `current_string` and a `current_num`.
  - When we see `[`, it means a new, nested task has begun. We **push** our `current_string` and `current_num` onto the stack to save them. Then we reset them for the new task.
  - When we see `]`, it means the nested task is done. We **pop** the saved string and number from the stack and use them to process the string we just built.

## Solution Approach

This solution iterates through the string character by character, using a stack to manage the nested decoding tasks.

```python
class Solution:
    def decodeString(self, s: str) -> str:
        stack = []
        current_num = 0
        current_string = ""
        
        for char in s:
            # Case 1: The character is a digit.
            if char.isdigit():
                current_num = current_num * 10 + int(char)
            
            # Case 2: The character is an opening bracket.
            elif char == '[':
                # Save the current state by pushing them onto the stack.
                stack.append(current_string)
                stack.append(current_num)
                # Reset the state for the new substring inside the brackets.
                current_string = ""
                current_num = 0
                
            # Case 3: The character is a closing bracket.
            elif char == ']':
                # Pop the multiplier and the previous string from the stack.
                num = stack.pop()
                prev_string = stack.pop()
                
                # Perform the decoding.
                current_string = prev_string + current_string * num
            
            # Case 4: The character is a letter.
            else:
                current_string += char
                
        return current_string
```

## Detailed Code Analysis

### Step 1: Initialization

```python
stack = []
current_num = 0
current_string = ""
```

  - `stack`: An empty list that will function as our stack. We will store pairs of `(string, number)` on it, but we'll push them one by one.
  - `current_num`: An integer to build the repeat count `k`.
  - `current_string`: A string to build the current segment of the decoded string.

### Step 2: The Loop and Logic

The `for` loop processes each character, and the `if/elif/else` block directs the logic.

**`if char.isdigit():`**

```python
current_num = current_num * 10 + int(char)
```

  - This handles multi-digit numbers. For example, if `current_num` is `12` and the `char` is `'3'`, this line calculates `12 * 10 + 3 = 123`.

**`elif char == '[':`**

```python
stack.append(current_string)
stack.append(current_num)
current_string = ""
current_num = 0
```

  - This is the "save" step. We've just finished reading a number and are about to start a new nested string.
  - We push the `current_string` (what we had before this new part) and the `current_num` (the multiplier for this new part) onto the stack.
  - We then reset the state variables to start building the new string inside the brackets from scratch.

**`elif char == ']':`**

```python
num = stack.pop()
prev_string = stack.pop()
current_string = prev_string + current_string * num
```

  - This is the "decode and restore" step. A `]` signifies the end of a nested segment.
  - `num = stack.pop()`: We pop the multiplier that corresponds to this segment.
  - `prev_string = stack.pop()`: We pop the string that was being built before this segment started.
  - `current_string = prev_string + current_string * num`: This is the core decoding operation. We take the string we just built (`current_string`), repeat it `num` times, and prepend the `prev_string` to it. The result becomes the new `current_string`.

**`else:`**

```python
current_string += char
```

  - This is the simplest case. If the character is a letter, we just append it to the string we're currently building.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `s = "3[a2[c]]"` with extreme detail.

| `char` | Action | `current_num` | `current_string` | `stack` |
| :--- | :--- | :--- | :--- | :--- |
| **Start** | - | `0` | `""` | `[]` |
| **'3'** | Digit | `3` | `""` | `[]` |
| **'['** | Open Bracket | `0` | `""` | `["", 3]` |
| **'a'** | Letter | `0` | `"a"` | `["", 3]` |
| **'2'** | Digit | `2` | `"a"` | `["", 3]` |
| **'['** | Open Bracket | `0` | `""` | `["", 3, "a", 2]` |
| **'c'** | Letter | `0` | `"c"` | `["", 3, "a", 2]` |
| **']'** | Close Bracket | `0` | `pop num=2`<br>`pop str="a"`<br>`"a"+"c"*2` -\> `"acc"` | `["", 3]` |
| **']'** | Close Bracket | `0` | `pop num=3`<br>`pop str=""`<br>`""+"acc"*3` -\> `"accaccacc"` | `[]` |

  - **Final Step**: The loop finishes. The function returns the final `current_string`: **`"accaccacc"`**.

## Performance Analysis

### Time Complexity: O(N)

  - Where `N` is the length of the **decoded** string. Although we loop through the input string `s` once, the string concatenation and multiplication operations (`* num`) mean that the total work is proportional to the size of the final output.

### Space Complexity: O(D)

  - Where `D` is the maximum nesting depth of the brackets. The space is determined by the maximum size of the `stack`, which depends on how many `[` we encounter before we see a `]`.

## Key Learning Points

  - **Stacks for Nested Structures**: Stacks are the ideal data structure for parsing or evaluating problems with nested, "last-in, first-out" structures like parentheses, brackets, or XML/HTML tags.
  - **State Management**: The solution expertly manages its state (`current_string`, `current_num`) by saving and restoring it on the stack as it enters and exits nested contexts.
  - **Parsing Numbers**: The `current_num = current_num * 10 + int(char)` pattern is a standard technique for building an integer from a stream of digit characters.