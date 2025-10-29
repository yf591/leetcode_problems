# 17\. Letter Combinations of a Phone Number - Solution Explanation

## Problem Overview

You are given a string `digits` containing digits from 2 to 9. The task is to return all possible letter combinations that these digits could represent, based on the standard telephone keypad mapping.

**Key Mapping:**

  - 2: "abc"
  - 3: "def"
  - 4: "ghi"
  - 5: "jkl"
  - 6: "mno"
  - 7: "pqrs"
  - 8: "tuv"
  - 9: "wxyz"

**Examples:**

```python
Input: digits = "23"
Output: ["ad","ae","af","bd","be","bf","cd","ce","cf"]

Input: digits = "2"
Output: ["a","b","c"]
```

## Key Insights

### 1\. The Combinatorial Explosion

The problem asks for *all possible* combinations. For each digit, there are 3 or 4 letter choices. If you have multiple digits, the number of combinations multiplies rapidly. This suggests a search algorithm that explores all branches of possibilities.

### 2\. Building Combinations Step-by-Step

Imagine building a combination for `"23"`.

  - You start with an empty string `""`.
  - For the first digit `'2'`, you have choices: `'a'`, `'b'`, `'c'`.
      - If you choose `'a'`, your current combination is `"a"`.
      - If you choose `'b'`, your current combination is `"b"`.
      - If you choose `'c'`, your current combination is `"c"`.
  - Now, consider the path where you chose `'a'`. You move to the second digit `'3'`, which gives choices `'d'`, `'e'`, `'f'`.
      - If you choose `'d'`, the final combination is `"ad"`.
      - If you choose `'e'`, the final combination is `"ae"`.
      - If you choose `'f'`, the final combination is `"af"`.
  - You need to do this for *all* initial choices (`'a'`, `'b'`, `'c'`) and all subsequent choices.

### 3\. Backtracking: Exploring All Paths

This process of making a choice, exploring the consequences of that choice, and then *undoing* the choice to try another option is called **backtracking**. It's like exploring a maze: you go down one path, and if it's a dead end (or you've found a solution), you backtrack to the last decision point and try a different path. **Recursion** is the most natural way to implement backtracking.

## Deep Dive: What is Backtracking? 🤔

Think of backtracking as a systematic way to explore all possible solutions to a problem by building a solution step-by-step. It's like navigating a maze:

1.  **Start**: You are at the entrance.
2.  **Decision Point**: You reach a junction with multiple paths.
3.  **Choose a Path**: You pick one path to explore.
4.  **Explore**: You follow that path. You might hit another junction (go back to step 2) or a dead end.
5.  **Hit a Dead End / Found Solution**: If you hit a dead end, or if you find what you're looking for (like the exit, or in our case, a full-length letter combination), you stop going forward on this path.
6.  **Backtrack**: You return to the *last decision point* (the previous junction).
7.  **Choose a Different Path**: You pick a path you haven't tried yet from that junction (go back to step 4). If there are no untried paths left, you backtrack further up.

**How it Applies Here:**

  - **Decision Point**: Each digit in the `digits` string is a decision point.
  - **Choices**: The letters corresponding to that digit are the different paths you can take.
  - **Building the Path**: Adding a letter to your `current_combination` is like moving down a path.
  - **Found Solution**: When `len(current_combination) == len(digits)`, you've reached the "exit" – a valid combination. You record it.
  - **Backtracking (Implicitly)**: In our recursive solution, when a `for` loop finishes exploring all letters for a given digit and the function returns, it automatically "backtracks" to the previous function call (the previous digit's decision point). Because we build *new* strings in each recursive call (`current_combination + letter`), we don't need an explicit "undo" step; the state is naturally managed by the call stack.

## Solution Approach

This solution uses a recursive helper function (`backtrack`) that implements the backtracking algorithm. It builds the letter combinations character by character.

```python
from typing import List

class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        # Handle the edge case of an empty input string.
        if not digits:
            return []
            
        # Mapping from digits to letters.
        digit_to_char = {
            '2': "abc", '3': "def", '4': "ghi", '5': "jkl",
            '6': "mno", '7': "pqrs", '8': "tuv", '9': "wxyz"
        }
        
        # List to store the final combinations.
        result = []

        # Define the recursive backtracking function.
        def backtrack(index: int, current_combination: str):
            # Base Case: If we have built a combination of the required length.
            if len(current_combination) == len(digits):
                result.append(current_combination)
                return # Stop this path and backtrack.

            # Get the letters corresponding to the current digit.
            current_digit = digits[index]
            possible_letters = digit_to_char[current_digit]
            
            # Recursive Step: Try adding each possible letter and explore further.
            for letter in possible_letters:
                # Explore the next level of recursion.
                backtrack(index + 1, current_combination + letter)
                # (Implicit Backtracking happens when this loop continues or the function returns)

        # Start the backtracking process from index 0 with an empty combination.
        backtrack(0, "")
        
        return result
```

## Detailed Code Analysis

### Step 1: Initialization and Mapping

```python
if not digits:
    return []
digit_to_char = { ... }
result = []
```

  - We handle the edge case where the input `digits` string is empty.
  - We create the `digit_to_char` dictionary, which acts as our phone keypad mapping.
  - `result` is initialized as an empty list to store the final combinations we find.

### Step 2: The `backtrack` Helper Function

This function does the main work. It explores the different paths.

  - `index`: Keeps track of which digit in the `digits` string we are currently processing.
  - `current_combination`: Stores the string of letters built so far along the current path.

**The Base Case:**

```python
if len(current_combination) == len(digits):
    result.append(current_combination)
    return
```

  - This is the stopping condition for the recursion. When the length of the string we are building (`current_combination`) matches the length of the input `digits`, we have formed a complete, valid combination.
  - We add this complete combination to our `result` list.
  - We `return` to stop exploring further down this path (there's nowhere else to go) and allow the function to backtrack.

**The Recursive Step:**

```python
current_digit = digits[index]
possible_letters = digit_to_char[current_digit]

for letter in possible_letters:
    backtrack(index + 1, current_combination + letter)
```

  - We get the `current_digit` based on the `index`.
  - We look up the `possible_letters` for that digit in our map.
  - The `for` loop iterates through each `letter` that corresponds to the `current_digit`. This represents making a choice at the current decision point.
  - **`backtrack(index + 1, current_combination + letter)`**: This is the recursive call. We make the choice (`letter`) and explore the consequences:
      - We move to the next digit by passing `index + 1`.
      - We pass down the *new*, extended combination (`current_combination + letter`). This is crucial – we are not modifying the `current_combination` of the *current* function call, but creating a new one for the next level. This is how the implicit backtracking works. When the recursive call eventually returns, the `for` loop simply continues to the next `letter`, effectively trying a different path.

### Step 3: The Initial Call

```python
backtrack(0, "")
```

  - We kick off the entire process by calling `backtrack` for the first time.
  - We start at `index = 0` (the first digit).
  - We start with an empty `current_combination`.

## Step-by-Step Execution Trace

Let's trace the algorithm for `digits = "23"` with extreme detail.

1.  **Initial Call**: `backtrack(index=0, combo="")`

      - `index=0`. `current_digit='2'`. `possible_letters="abc"`.
      - **Loop 1 (`letter='a'`)**: Calls `backtrack(index=1, combo="a")`
          - `index=1`. `current_digit='3'`. `possible_letters="def"`.
          - **Loop 1.1 (`letter='d'`)**: Calls `backtrack(index=2, combo="ad")`
              - `len("ad") == len("23")`. Base case hit. `result.append("ad")`. Returns.
          - **Loop 1.2 (`letter='e'`)**: Calls `backtrack(index=2, combo="ae")`
              - `len("ae") == len("23")`. Base case hit. `result.append("ae")`. Returns.
          - **Loop 1.3 (`letter='f'`)**: Calls `backtrack(index=2, combo="af")`
              - `len("af") == len("23")`. Base case hit. `result.append("af")`. Returns.
          - Inner loop finishes. `backtrack(index=1, combo="a")` returns.
      - **Loop 2 (`letter='b'`)**: Calls `backtrack(index=1, combo="b")`
          - `index=1`. `current_digit='3'`. `possible_letters="def"`.
          - **Loop 2.1 (`letter='d'`)**: Calls `backtrack(index=2, combo="bd")` -\> Adds "bd" to result.
          - **Loop 2.2 (`letter='e'`)**: Calls `backtrack(index=2, combo="be")` -\> Adds "be" to result.
          - **Loop 2.3 (`letter='f'`)**: Calls `backtrack(index=2, combo="bf")` -\> Adds "bf" to result.
          - Inner loop finishes. `backtrack(index=1, combo="b")` returns.
      - **Loop 3 (`letter='c'`)**: Calls `backtrack(index=1, combo="c")`
          - `index=1`. `current_digit='3'`. `possible_letters="def"`.
          - **Loop 3.1 (`letter='d'`)**: Calls `backtrack(index=2, combo="cd")` -\> Adds "cd" to result.
          - **Loop 3.2 (`letter='e'`)**: Calls `backtrack(index=2, combo="ce")` -\> Adds "ce" to result.
          - **Loop 3.3 (`letter='f'`)**: Calls `backtrack(index=2, combo="cf")` -\> Adds "cf" to result.
          - Inner loop finishes. `backtrack(index=1, combo="c")` returns.
      - Outer loop finishes. `backtrack(index=0, combo="")` returns.

2.  **Final Result**: The function returns `result`, which now contains `["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]`.

## Performance Analysis

### Time Complexity: O(4^N \* N)

  - Where `N` is the length of the `digits` string.
  - In the worst case (digits like '7' or '9'), each digit has 4 possible letters. The number of possible combinations is roughly `4^N`.
  - For each combination, we potentially do `N` work (e.g., string concatenation, although Python might optimize this).
  - So, the complexity is roughly proportional to the number of solutions times the length of each solution.

### Space Complexity: O(N)

  - The space complexity is determined primarily by the depth of the recursion call stack. In the worst case, the stack will go as deep as the length of the `digits` string, `N`.
  - The space used to store the `result` list is not typically counted in the space complexity analysis, but it would be `O(4^N * N)`.