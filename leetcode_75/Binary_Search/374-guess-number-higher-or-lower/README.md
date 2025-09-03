# 374\. Guess Number Higher or Lower - Solution Explanation

## Problem Overview

This is an interactive problem where you need to guess a secret number.

  - **The Game**: A number is picked secretly from `1` to `n`.
  - **Your Task**: Find that secret number.
  - **Your Tool**: You have a helper function `guess(num)` that you can call. It gives you feedback:
      - It returns `-1` if your `num` is **higher** than the secret number.
      - It returns `1` if your `num` is **lower** than the secret number.
      - It returns `0` if your `num` is **correct**.

## Key Insights

### The Power of "Higher or Lower"

A simple approach would be to guess 1, then 2, then 3, and so on, until you find the number. This is called a **linear search**, but it would be very slow if `n` is large.

The key insight is that the feedback from the `guess()` API ("higher" or "lower") allows you to eliminate a huge number of possibilities with every single guess. If you guess a number in the middle of a range and it tells you "too high," you instantly know the answer *cannot* be in the entire upper half of that range.

This process of repeatedly halving the search space is the core idea of the **Binary Search** algorithm, which is extremely efficient.

## Solution Approach

The solution implements a classic binary search. We maintain a "search space" defined by a `low` and `high` pointer. With each guess, we shrink this space by half until there is only one number left, which must be the answer.

```python
# The guess API is already defined for you.
# @param num, your guess
# @return -1 if num is higher than the picked number
#          1 if num is lower than the picked number
#          otherwise return 0
# def guess(num: int) -> int:

class Solution:
    def guessNumber(self, n: int) -> int:
        # Step 1: Initialize the boundaries of our search space.
        low = 1
        high = n
        
        # Step 2: Continue searching as long as our range is valid.
        while low <= high:
            # Step 3: Guess the number in the middle of the current range.
            mid = low + (high - low) // 2
            
            # Step 4: Call the API to check our guess.
            result = guess(mid)
            
            # Step 5: Adjust our search space based on the API's feedback.
            if result == 0:
                # We found the number!
                return mid
            elif result == 1:
                # Our guess was too low, so the number must be in the upper half.
                low = mid + 1
            else: # result == -1
                # Our guess was too high, so the number must be in the lower half.
                high = mid - 1
```

## Detailed Code Analysis

### Step 1: Initialization

```python
low = 1
high = n
```

  - We set up our search space. We know the secret number must be somewhere between `1` and `n`, inclusive. `low` and `high` represent the boundaries of this space.

### Step 2: The Loop Condition

```python
while low <= high:
```

  - This loop will continue as long as our search space is valid (i.e., the lower bound is not greater than the upper bound). The moment `low` becomes greater than `high`, it means the number wasn't found (though the problem guarantees a pick exists).

### Step 3: The Guess

```python
mid = low + (high - low) // 2
```

  - This is the heart of binary search. Instead of a random guess, we always guess the exact middle of our current search space (`low` to `high`). This guarantees that we eliminate the maximum number of possibilities with each guess.
  - This formula is a safe way to calculate the midpoint that avoids potential integer overflow in other programming languages.

### Step 5: Adjusting the Search Space

```python
if result == 0:
    return mid
elif result == 1:
    low = mid + 1
else: # result == -1
    high = mid - 1
```

  - This is where we use the API's feedback to shrink our search space.
  - **If `result == 1` (guess is too low)**: We know the secret number is greater than `mid`. So, we can discard `mid` and every number below it. We do this by moving our lower boundary up to `mid + 1`.
  - **If `result == -1` (guess is too high)**: We know the secret number is less than `mid`. So, we can discard `mid` and every number above it. We do this by moving our upper boundary down to `mid - 1`.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `n = 10` and `pick = 6`.

| Iteration | `low` | `high` | `mid` (Your Guess) | `guess(mid)` Result | Action |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Start** | 1 | 10 | - | - | The search space is `[1...10]`. |
| **1** | 1 | 10 | `1+(10-1)//2 = 5` | `1` (Guess is too low) | The answer must be \> 5. New search space is `[6...10]`. `low` becomes `6`. |
| **2** | 6 | 10 | `6+(10-6)//2 = 8` | `-1` (Guess is too high) | The answer must be \< 8. New search space is `[6...7]`. `high` becomes `7`. |
| **3** | 6 | 7 | `6+(7-6)//2 = 6` | `0` (Correct\!) | The guess is correct. **Return `mid` (6)**. |

## Performance Analysis

### Time Complexity: O(log n)

  - This is the main advantage of binary search. With each guess, we cut the number of possibilities in half. The number of times you can halve a range of size `n` is `log₂(n)`. This is extremely fast, even for very large values of `n`.

### Space Complexity: O(1)

  - We only use a few variables to keep track of our state (`low`, `high`, `mid`). The space required is constant and does not grow with `n`.

## Key Learning Points

  - **Binary Search**: This problem is a perfect illustration of when and how to use binary search. Look for problems where you have a sorted (or implicitly sorted) range of possibilities and a way to get "higher" or "lower" feedback.
  - **Divide and Conquer**: Binary search is a classic "divide and conquer" algorithm. It solves a problem by repeatedly breaking it down into smaller subproblems.
  - **Pointer Manipulation**: The core implementation relies on correctly manipulating the `low` and `high` pointers to shrink the search space.

## Real-World Applications

  - **Searching in Databases**: Database indexes often use a structure called a B-Tree, which is a generalization of a binary search tree, to find data in logarithmic time.
  - **Finding a Value in Any Large, Sorted Dataset**: This is the most common use case. For example, looking up a word in a physical dictionary is a form of binary search.
  - **Debugging**: A technique called "git bisect" uses binary search to efficiently find the exact code commit that introduced a bug in a long history of commits.