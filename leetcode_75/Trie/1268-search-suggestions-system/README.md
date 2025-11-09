# 1268\. Search Suggestions System - Solution Explanation

## Problem Overview

You are asked to design an auto-complete system. You're given a list of `products` and a `searchWord`. After a user types *each character* of the `searchWord`, you must return a list of up to three product names from the `products` list that share the current typed prefix.

**Key Rules & Constraints:**

  - The suggestions must match the prefix as it's being typed.
  - If there are more than three matching products, you must return the three that are **lexicographically smallest** (i.e., in alphabetical order).
  - The final output should be a list of lists, where each inner list is the set of suggestions after each character of `searchWord` is typed.

**Example:**

```python
Input: products = ["mobile","mouse","moneypot","monitor","mousepad"], searchWord = "mouse"
Output: [
  ["mobile","moneypot","monitor"],  # After "m"
  ["mobile","moneypot","monitor"],  # After "mo"
  ["mouse","mousepad"],             # After "mou"
  ["mouse","mousepad"],             # After "mous"
  ["mouse","mousepad"]              # After "mouse"
]
```

## Deep Dive: What is a `Trie`? 🌳

(This is one way to solve the problem, and good to know\!)

A **Trie** (pronounced "try"), or **Prefix Tree**, is a special tree-like data structure designed to store and search for strings very efficiently. It's the data structure that powers most auto-complete and spell-checker systems.

**How it works:**

1.  **Nodes**: Each node in the tree represents a single character.
2.  **Paths**: A path from the root to any node forms a *prefix*.
3.  **Children**: Each node has a set of children, typically stored in a dictionary (e.g., `{'a': Node, 'b': Node, ...}`).
4.  **End Marker**: A node can be marked with a special flag (e.g., `isEndOfWord = True`) to signify that a complete word ends at that node.

**Example: Inserting "app" and "apple"**

```
      (root)
        | 'a'
        o (Node for 'a')
        | 'p'
        o (Node for 'p')
        | 'p'
        o (Node for 'p') --- isEndOfWord = True (for "app")
        | 'l'
        o (Node for 'l')
        | 'e'
        o (Node for 'e') --- isEndOfWord = True (for "apple")
```

**How it Applies to This Problem:**
You could insert all `products` into a Trie. Then, for each character in `searchWord`, you would traverse the Trie. From the node you land on, you would then perform a search (like a DFS) to find all words that descend from that node, stopping after you find 3 lexicographically. This is a very common solution, but the code you've been given uses a different, also very clever approach.

## Key Insights: The Sorting + Two Pointers Approach

The solution provided uses a different technique. The problem's requirement for **lexicographically sorted** results is a massive hint.

### 1\. The Power of Sorting

If we **sort the `products` list** just one time at the beginning, we get two huge advantages:

1.  All the words that share a common prefix (like "mouse" and "mousepad") will be **grouped together** in a contiguous block.
2.  The words within that block will **already be in alphabetical order**.

This means we don't need a complex Trie or a separate sorting step for every suggestion. We just need to find the *block* of words that matches the current prefix.

### 2\. The "Shrinking Window" (Two Pointers)

We can find this "block" of matching words using two pointers, `left` and `right`.

  - Initially, the window `[left...right]` covers the entire sorted list.
  - When the user types `'m'`, we shrink the window from both ends, moving `left` forward and `right` backward until they point to the start and end of the block of words that start with "m".
  - When the user types `'o'`, we *don't* restart. We just continue shrinking our *current* window (`left` and `right`) to find the sub-block that starts with "mo".

This "shrinking window" is very efficient because the `left` and `right` pointers only ever move in one direction (inward) and never reset.

## Solution Approach (The Two-Pointer Method)

This solution first sorts the `products` array. Then, it iterates through the `searchWord` one character at a time. In each iteration, it "shrinks" a `left` and `right` pointer to find the range of products that match the prefix typed so far. It then appends the first 3 items in that range to the result.

```python
from typing import List

class Solution:
    def suggestedProducts(self, products: List[str], searchWord: str) -> List[List[str]]:
        
        # --- Step 1: Sort the products list ---
        # This is the most important setup step. It takes O(N*L*logN) time.
        # Now, all matching prefixes are grouped together lexicographically.
        products.sort()
        
        result = []
        # --- Step 2: Initialize the "window" pointers ---
        left, right = 0, len(products) - 1
        
        # --- Step 3: Iterate through each character of the searchWord ---
        for i in range(len(searchWord)):
            char_to_match = searchWord[i]
            
            # --- Step 4: Shrink the window from the left ---
            # Move 'left' forward as long as the word at 'left'
            # does NOT match the current prefix.
            while left <= right and (len(products[left]) <= i or products[left][i] != char_to_match):
                left += 1
                
            # --- Step 5: Shrink the window from the right ---
            # Move 'right' backward as long as the word at 'right'
            # does NOT match the current prefix.
            while left <= right and (len(products[right]) <= i or products[right][i] != char_to_match):
                right -= 1
            
            # --- Step 6: Record the suggestions ---
            # At this point, all words from 'left' to 'right' (inclusive)
            # match the prefix.
            suggestions = []
            num_suggestions = min(3, right - left + 1)
            
            for j in range(num_suggestions):
                suggestions.append(products[left + j])
                
            result.append(suggestions)
            
        return result
```

## Detailed Code Analysis

### Step 1: Sorting

```python
products.sort()
```

  - **Action**: Sorts the `products` list in-place alphabetically.
  - **Example**: `["mouse","mousepad","mobile","moneypot","monitor"]` -\> `["mobile","moneypot","monitor","mouse","mousepad"]`.

### Step 2: Pointer Initialization

```python
result = []
left, right = 0, len(products) - 1
```

  - `result`: An empty list to store our final list of lists.
  - `left = 0`: The left pointer starts at the beginning of the sorted list.
  - `right = len(products) - 1`: The right pointer starts at the end. The window `[left...right]` currently contains all products.

### Step 3: The Main Loop (Character by Character)

```python
for i in range(len(searchWord)):
    char_to_match = searchWord[i]
```

  - This `for` loop iterates through `searchWord`. `i` is the index of the char (0, 1, 2...), and `char_to_match` is the char itself.

### Step 4 & 5: The "Shrinking Window"

```python
while left <= right and (len(products[left]) <= i or products[left][i] != char_to_match):
    left += 1
```

  - This is the logic to shrink the window from the left.
  - **`while left <= right`**: Ensures our pointers don't cross.
  - **`len(products[left]) <= i`**: This is a critical check. It checks if the word at `products[left]` is *shorter* than the prefix we are currently checking. For example, if we are checking the prefix "mou" (`i=2`) and the word is "mo", this word is too short and cannot be a match. We must discard it.
  - **`products[left][i] != char_to_match`**: This checks if the character at the correct position matches the one we just typed. If `products[left]` is "monitor" and we are checking for "mou" (`i=2`, `char='u'`), `products[left][2]` is 'n'. 'n' is not 'u', so we discard this word.
  - **`left += 1`**: Move the left pointer one step to the right.
  - The same logic is applied in reverse for the `right` pointer, moving it backward.

### Step 6: Recording the Suggestions

```python
suggestions = []
num_suggestions = min(3, right - left + 1)
for j in range(num_suggestions):
    suggestions.append(products[left + j])
result.append(suggestions)
```

  - After the `while` loops, our window `[left...right]` contains *only* words that match the current prefix (e.g., `searchWord[0...i]`).
  - `right - left + 1` calculates the total number of items in our window.
  - `num_suggestions = min(3, ...)`: We get the number of suggestions we need, which is either 3 or the total number of matching words if there are fewer than 3.
  - We then add the first `num_suggestions` items from our window (starting at `left`) to our `suggestions` list and append that to the final `result`.

## Step-by-Step Execution Trace

Let's trace `products = ["mobile","moneypot","monitor","mouse","mousepad"]`, `searchWord = "mouse"`.

1.  **Sort**: `products` = `["mobile", "moneypot", "monitor", "mouse", "mousepad"]`
2.  **Initialize**: `result = []`, `left = 0`, `right = 4`

-----

### **`i = 0`, `char = 'm'`**

  - **Shrink `left`**: `while 0 <= 4` and (`len("mobile") <= 0` is F or `"mobile"[0] != 'm'` is F). Loop does not run. `left = 0`.
  - **Shrink `right`**: `while 0 <= 4` and (`len("mousepad") <= 0` is F or `"mousepad"[0] != 'm'` is F). Loop does not run. `right = 4`.
  - **Get Suggestions**: Window is `[0...4]`. `num_suggestions = min(3, 4-0+1) = 3`.
  - `result.append([products[0], products[1], products[2]])` -\> `[["mobile", "moneypot", "monitor"]]`

-----

### **`i = 1`, `char = 'o'`**

  - **Shrink `left`**: `while 0 <= 4` and (`len("mobile") <= 1` is F or `"mobile"[1] != 'o'` is F). Loop does not run. `left = 0`.
  - **Shrink `right`**: `while 0 <= 4` and (`len("mousepad") <= 1` is F or `"mousepad"[1] != 'o'` is F). Loop does not run. `right = 4`.
  - **Get Suggestions**: Window `[0...4]`. `num_suggestions = 3`.
  - `result.append([["mobile", "moneypot", "monitor"]])`

-----

### **`i = 2`, `char = 'u'`**

  - **Shrink `left`**:
      - `products[0]` is "mobile". `[0][2]` is 'b'. `'b' != 'u'`. `left` becomes 1.
      - `products[1]` is "moneypot". `[1][2]` is 'n'. `'n' != 'u'`. `left` becomes 2.
      - `products[2]` is "monitor". `[2][2]` is 'n'. `'n' != 'u'`. `left` becomes 3.
      - `products[3]` is "mouse". `[3][2]` is 'u'. `'u' == 'u'`. Loop stops. `left = 3`.
  - **Shrink `right`**:
      - `products[4]` is "mousepad". `[4][2]` is 'u'. `'u' == 'u'`. Loop stops. `right = 4`.
  - **Get Suggestions**: Window `[3...4]`. `num_suggestions = min(3, 4-3+1) = 2`.
  - `result.append([products[3], products[4]])` -\> `[["mouse", "mousepad"]]`

-----

### **`i = 3`, `char = 's'`**

  - **Shrink `left`**: `while 3 <= 4` and (`len("mouse") <= 3` is F or `"mouse"[3] != 's'` is F). Loop does not run. `left = 3`.
  - **Shrink `right`**: `while 3 <= 4` and (`len("mousepad") <= 3` is F or `"mousepad"[3] != 's'` is F). Loop does not run. `right = 4`.
  - **Get Suggestions**: Window `[3...4]`. `num_suggestions = 2`.
  - `result.append([["mouse", "mousepad"]])`

-----

### **`i = 4`, `char = 'e'`**

  - **Shrink `left`**: `while 3 <= 4` and (`len("mouse") <= 4` is F or `"mouse"[4] != 'e'` is F). Loop does not run. `left = 3`.
  - **Shrink `right`**: `while 3 <= 4` and (`len("mousepad") <= 4` is F or `"mousepad"[4] != 'e'` is F). Loop does not run. `right = 4`.
  - **Get Suggestions**: Window `[3...4]`. `num_suggestions = 2`.
  - `result.append([["mouse", "mousepad"]])`

-----

### **End of Algorithm**

  - The main `for` loop finishes.
  - The final `result` list is returned.

## Performance Analysis

### Time Complexity: O(N*L*logN + M\*L)

  - `N` = number of products, `M` = length of `searchWord`, `L` = max length of a product.
  - **Sorting**: `O(N * L * log N)`. Sorting `N` items. String comparison takes up to `O(L)` time in the worst case.
  - **Traversal**:
      - Outer `for` loop runs `M` times.
      - The two `while` loops *in total* (over the entire `for` loop) move the `left` and `right` pointers at most `N` times. Each check inside the `while` loop is `O(1)` (string indexing). So, all pointer movement is `O(N)`.
      - Building the result list: `M` times, we copy up to 3 strings of length `L`. This is `O(M * L)`.
  - **Total**: `O(N*L*logN + N + M*L)`. The sorting step is the bottleneck.

### Space Complexity: O(M \* L)

  - This is the space required to store the `result` list. We store `M` lists, each containing up to 3 strings of length at most `L`.