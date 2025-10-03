# 150\. Evaluate Reverse Polish Notation - Solution Explanation

## Problem Overview

You are given an array of strings `tokens` that represents an arithmetic expression in **Reverse Polish Notation (RPN)**. The task is to evaluate this expression and return the final integer value.

**Reverse Polish Notation (RPN) Definition:**
Also known as postfix notation, RPN is a mathematical notation in which every operator follows all of its operands.

  - Standard (infix) notation: `(2 + 1) * 3`
  - Reverse Polish (postfix) notation: `2 1 + 3 *`

**Rules:**

  - Valid operators are `+`, `-`, `*`, `/`.
  - Division `a / b` must **truncate toward zero**.
  - The input is always a valid RPN expression.

**Examples:**

```python
Input: tokens = ["2","1","+","3","*"]
Output: 9
Explanation: ((2 + 1) * 3) = 9

Input: tokens = ["4","13","5","/","+"]
Output: 6
Explanation: (4 + (13 / 5)) = 6
```

## Key Insights

### The Perfect Match: RPN and the Stack

The core insight is that RPN is *designed* to be evaluated using a **stack**. The structure of the notation perfectly matches the **Last-In, First-Out (LIFO)** behavior of a stack.

Let's think about how we would evaluate an RPN expression by hand:

1.  Read the tokens from left to right.
2.  If you see a **number**, you don't know what to do with it yet, so you just hold onto it.
3.  If you see an **operator**, you know it needs to be applied to the *two most recent numbers* you've been holding.
4.  You perform the calculation and now hold onto the new result.

This process of "holding onto" numbers and then using the "most recent" ones is exactly what a stack does.

  - Seeing a number -\> **Push** it onto the stack.
  - Seeing an operator -\> **Pop** two numbers, calculate, and then **push** the result back on.

## Solution Approach

This solution implements the classic stack-based algorithm. It iterates through the tokens. Numbers are pushed onto a stack. When an operator is encountered, it pops the top two numbers, performs the operation, and pushes the result back onto the stack. At the end, the stack will contain a single element: the final result.

```python
from typing import List

class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        # We use a standard Python list to function as our stack.
        stack = []
        
        # Iterate through each token in the input list.
        for token in tokens:
            # Case 1: The token is an addition operator.
            if token == "+":
                # For '+' and '*', the order of popping doesn't matter.
                stack.append(stack.pop() + stack.pop())
            
            # Case 2: The token is a subtraction operator.
            elif token == "-":
                # Order matters! The second operand is popped first.
                b, a = stack.pop(), stack.pop()
                stack.append(a - b)
            
            # Case 3: The token is a multiplication operator.
            elif token == "*":
                stack.append(stack.pop() * stack.pop())
            
            # Case 4: The token is a division operator.
            elif token == "/":
                # Order matters!
                b, a = stack.pop(), stack.pop()
                # Use int(a / b) to handle truncation towards zero correctly for all cases.
                stack.append(int(a / b))
            
            # Case 5: The token is a number.
            else:
                # Convert the string to an integer and push it onto the stack.
                stack.append(int(token))
                
        # After the loop, the stack will contain exactly one number: the final result.
        return stack[0]
```

## Detailed Code Analysis

### Step 1: Initialization

```python
stack = []
```

  - We initialize an empty list. In Python, a `list` is a perfect and efficient choice for implementing a stack, as its `append()` (push) and `pop()` (pop from the end) methods are both `O(1)` operations.

### Step 2: The Loop

```python
for token in tokens:
```

  - This loop drives the algorithm, processing each token from the input list one by one, from left to right.

### Step 3: Handling Operators

The `if/elif` structure checks if the current `token` is one of the four operators.

**For `+` and `*`:**

```python
stack.append(stack.pop() + stack.pop())
```

  - Because addition and multiplication are commutative (`a + b = b + a`), the order in which we pop the two numbers from the stack doesn't matter. This is a concise way to perform the operation.

**For `-` and `/` (The Critical Part):**

```python
b, a = stack.pop(), stack.pop()
stack.append(a - b)
```

  - **Order is extremely important here.** When we evaluate `a - b`, `a` is the first operand and `b` is the second. In RPN, the second operand appears most recently in the token list. Since the stack is LIFO, the most recent item is the first one popped.
  - `stack.pop()` removes and returns `b`.
  - The next `stack.pop()` removes and returns `a`.
  - So, `b, a = stack.pop(), stack.pop()` correctly assigns the second operand to `b` and the first to `a`. We then calculate `a - b`.

**Division Truncation:**

```python
stack.append(int(a / b))
```

  - The problem requires division to truncate toward zero (e.g., `-1.5` becomes `-1`, `1.5` becomes `1`).
  - Python's standard division `/` produces a float (e.g., `13 / 5 = 2.6`).
  - The `int()` function, when applied to a float, correctly truncates toward zero for both positive and negative numbers. This is why `int(a / b)` is used instead of floor division `//`, which would truncate downwards (`-132 // 12 = -11`, but `6 // -132 = -1`). Here `int(6/-132)` is `0`, which is correct.

### Step 4: Handling Numbers

```python
else:
    stack.append(int(token))
```

  - If the `token` is not any of the recognized operators, it must be a number (given by the problem constraints).
  - `int(token)` converts the number from its string representation (e.g., `"13"`) to an actual integer (e.g., `13`).
  - `stack.append(...)` pushes this integer onto our stack.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `tokens = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]` with extreme detail.

| `token` | Action | `stack` State (after action) | Explanation |
| :--- | :--- | :--- | :--- |
| **Start** | - | `[]` | - |
| **"10"** | Push number | `[10]` | |
| **"6"** | Push number | `[10, 6]` | |
| **"9"** | Push number | `[10, 6, 9]` | |
| **"3"** | Push number | `[10, 6, 9, 3]` | |
| **"+"** | Pop 3, Pop 9. Calculate `9+3=12`. Push 12.| `[10, 6, 12]` | `(9+3)` is evaluated. |
| **"-11"**| Push number | `[10, 6, 12, -11]` | |
| **"\*"** | Pop -11, Pop 12. Calculate `12*(-11)=-132`. Push -132. | `[10, 6, -132]` | `(12 * -11)` is evaluated. |
| **"/"** | Pop -132, Pop 6. Calculate `int(6/-132)=0`. Push 0. | `[10, 0]` | `(6 / -132)` is evaluated. |
| **"\*"** | Pop 0, Pop 10. Calculate `10*0=0`. Push 0. | `[0]` | `(10 * 0)` is evaluated. |
| **"17"** | Push number | `[0, 17]` | |
| **"+"** | Pop 17, Pop 0. Calculate `0+17=17`. Push 17. | `[17]` | `(0 + 17)` is evaluated. |
| **"5"** | Push number | `[17, 5]` | |
| **"+"** | Pop 5, Pop 17. Calculate `17+5=22`. Push 22. | `[22]` | `(17 + 5)` is evaluated. |

  - **Final Step**: The `for` loop finishes. The function returns `stack[0]`, which is **`22`**.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of tokens. We iterate through the list of tokens exactly once. Each operation inside the loop (push, pop, arithmetic) is an `O(1)` operation.

### Space Complexity: O(n)

  - In the worst-case scenario, the input could consist of mostly numbers. For example, `["1", "2", "3", ..., "+"]`. The stack would have to store almost all `n` numbers before it starts processing operators. Therefore, the space required is proportional to the number of tokens.

## Key Learning Points

  - **Stack Applications**: This problem is a quintessential example of how stacks are used to evaluate expressions, a core concept in compiler and interpreter design.
  - **LIFO Logic**: Understanding that RPN's "operator-after-operands" structure perfectly matches a stack's "Last-In, First-Out" behavior is the main insight.
  - **Attention to Detail**: The solution requires careful handling of non-commutative operations like subtraction and division (ensuring correct operand order) and specific language behaviors (like integer division truncation).