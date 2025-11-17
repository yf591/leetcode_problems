# 208\. Implement Trie (Prefix Tree) - Solution Explanation

## Problem Overview

The task is to implement a `Trie` (also known as a "prefix tree"). This is a special tree-like data structure used to store and retrieve strings. We need to implement three main methods:

  - **`Trie()`**: Initializes the data structure.
  - **`insert(String word)`**: Adds a new `word` to the trie.
  - **`search(String word)`**: Returns `true` if the *exact word* has been inserted.
  - **`startsWith(String prefix)`**: Returns `true` if any previously inserted word has the given `prefix`.

**Example:**

```python
trie = Trie()
trie.insert("apple")
trie.search("apple")     # -> true
trie.search("app")       # -> false (it's a prefix, but not an inserted *word*)
trie.startsWith("app")   # -> true
trie.insert("app")
trie.search("app")       # -> true
```

## Key Insights

### 1\. What is a Trie?

A Trie is a tree structure where each path from the root to a node represents a string prefix. Each node in the tree corresponds to a single character.

  - The **root** node is empty.
  - Children of the root are the first letters of all words.
  - Their children are the second letters, and so on.

### 2\. The `TrieNode`

To build a Trie, we first need to define what a single node in the tree looks like. Each node needs to store two key pieces of information:

1.  **A list of its children**: Since the next character could be any of the 26 lowercase letters, a **hash map (or dictionary)** is the most efficient way to store this. We can map a character (e.g., `'a'`) to the child `TrieNode` that represents it.
2.  **An end-of-word marker**: How do we distinguish between `trie.insert("app")` and `trie.insert("apple")`? When we search for `"app"`, we need to know that a word *actually ended* at the second `'p'`. We use a boolean flag, `isEndOfWord`, for this.

So, we will create a helper class:

```python
class TrieNode:
    def __init__(self):
        self.children = {}  # A map from character -> child TrieNode
        self.isEndOfWord = False
```

### 3\. The Difference Between `search` and `startsWith`

This is the most critical distinction in the problem:

  - **`search("app")`** asks: "Does the path `a->p->p` exist, AND is the final `p` node marked as `isEndOfWord = True`?"
  - **`startsWith("app")`** asks: "Does the path `a->p->p` exist?" It doesn't care if a word ends there.

## Solution Approach

The solution involves first defining the `TrieNode` helper class. Then, the main `Trie` class will be built using these nodes. The `Trie` class itself will only need to store one thing: the `root` of the tree. All the logic will be implemented by traversing this tree.

```python
#
# @lc app=leetcode id=208 lang=python3
#
# [208] Implement Trie (Prefix Tree)
#

# @lc code=start

# First, define the helper class for each node in the Trie.
class TrieNode:
    def __init__(self):
        # 'children' will be a dictionary mapping a character (e.g., 'a')
        # to its corresponding child TrieNode.
        self.children = {}
        # 'isEndOfWord' marks the end of a complete word.
        self.isEndOfWord = False

class Trie:

    def __init__(self):
        """
        Initializes the Trie by creating a single root node.
        """
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """
        Inserts a word into the trie.
        """
        # Start at the root node.
        current_node = self.root
        
        # Iterate over each character in the word.
        for char in word:
            # If the character is not already a child of the current node,
            # we need to create a new TrieNode for it.
            if char not in current_node.children:
                current_node.children[char] = TrieNode()
            # Move down to the child node to continue the path.
            current_node = current_node.children[char]
            
        # After the loop, 'current_node' is the node for the last character.
        # We mark it as the end of a word.
        current_node.isEndOfWord = True

    def search(self, word: str) -> bool:
        """
        Returns true if the exact word is in the trie.
        """
        current_node = self.root
        
        # Traverse the trie along the path of the word.
        for char in word:
            if char not in current_node.children:
                # If a character is missing, the path doesn't exist.
                return False
            current_node = current_node.children[char]
            
        # After the loop, we are at the last node of the path.
        # We must check if this node is marked as the end of a word.
        return current_node.isEndOfWord

    def startsWith(self, prefix: str) -> bool:
        """
        Returns true if there is any word in the trie that starts with the prefix.
        """
        current_node = self.root
        
        # Traverse the trie along the path of the prefix.
        for char in prefix:
            if char not in current_node.children:
                # If a character is missing, no word can start with this prefix.
                return False
            current_node = current_node.children[char]
            
        # If we successfully traversed the entire prefix, a path exists.
        # This means some word (or words) must start with it.
        return True
        


# Your Trie object will be instantiated and called as such:
# obj = Trie()
# obj.insert(word)
# param_2 = obj.search(word)
# param_3 = obj.startsWith(prefix)
# @lc code=end
```

## Detailed Code Analysis

### `__init__(self)`

```python
self.root = TrieNode()
```

  - Initializes the `Trie` class. The entire data structure is represented by a single `root` node. This `root` is an empty `TrieNode`, and its `children` map is empty.

### `insert(self, word: str)`

```python
current_node = self.root
for char in word:
    if char not in current_node.children:
        current_node.children[char] = TrieNode()
    current_node = current_node.children[char]
current_node.isEndOfWord = True
```

  - This method builds the path for a word.
  - `current_node = self.root`: We always start our traversal from the root.
  - `for char in word:`: We process the word one character at a time.
  - `if char not in current_node.children:`: We check if the current node already has a child for this `char`.
  - `current_node.children[char] = TrieNode()`: If it doesn't, we **create a new, empty `TrieNode`** and add it to the `children` dictionary with the `char` as the key.
  - `current_node = current_node.children[char]`: We move our `current_node` pointer down to the child node (either the one we just created or the one that already existed).
  - `current_node.isEndOfWord = True`: After the loop finishes, `current_node` is pointing to the node corresponding to the *last* character of the word. We mark this node as `isEndOfWord` to signify that a complete word ends here.

### `search(self, word: str)`

```python
current_node = self.root
for char in word:
    if char not in current_node.children:
        return False
    current_node = current_node.children[char]
return current_node.isEndOfWord
```

  - This method *only* follows a path; it never creates new nodes.
  - `if char not in current_node.children:`: If at any point we can't find the next `char` in the current node's `children`, it means the path doesn't exist, so the word cannot be in the trie. We return `False`.
  - `return current_node.isEndOfWord`: If the loop finishes, it means the *path* for the word exists. However, we must return `True` only if a word was explicitly inserted to end at this node. This is the critical check.

### `startsWith(self, prefix: str)`

```python
current_node = self.root
for char in prefix:
    if char not in current_node.children:
        return False
    current_node = current_node.children[char]
return True
```

  - This is almost identical to `search`.
  - **The Key Difference**: `return True`. If the loop completes, it means the path for the `prefix` exists. Since *any* path in the trie is a prefix for some inserted word, we can immediately return `True` without checking the `isEndOfWord` flag.

## Step-by-Step Execution Trace

Let's trace the example `["insert", "apple"], ["search", "apple"], ["search", "app"], ["startsWith", "app"]`.

### **1. `trie = Trie()`**

  - `self.root` is created. It is an empty `TrieNode`. `root.children = {}`, `root.isEndOfWord = False`.

### **2. `trie.insert("apple")`**

  - `current_node` starts at `root`.
  - `char = 'a'`: 'a' is not in `root.children`. Create `TrieNode` for 'a'. Set `root.children['a']` to this new node. Move `current_node` to `Node(a)`.
  - `char = 'p'`: 'p' is not in `Node(a).children`. Create `TrieNode` for 'p'. Set `Node(a).children['p']` to this new node. Move `current_node` to `Node(p)`.
  - `char = 'p'`: 'p' is not in `Node(p).children`. Create `TrieNode` for 'p'. Set `Node(p).children['p']` to this new node. Move `current_node` to `Node(p)_2`.
  - `char = 'l'`: 'l' is not in `Node(p)_2.children`. Create `TrieNode` for 'l'. Set `Node(p)_2.children['l']` to this new node. Move `current_node` to `Node(l)`.
  - `char = 'e'`: 'e' is not in `Node(l).children`. Create `TrieNode` for 'e'. Set `Node(l).children['e']` to this new node. Move `current_node` to `Node(e)`.
  - Loop finishes. Set `Node(e).isEndOfWord = True`.

**Trie structure:**

```
root
  | 'a'
  o (isEnd=False)
    | 'p'
    o (isEnd=False)
      | 'p'
      o (isEnd=False)
        | 'l'
        o (isEnd=False)
          | 'e'
          o (isEnd=True)
```

### **3. `trie.search("apple")`**

  - `current_node` starts at `root`.
  - `char = 'a'`: Found in `root.children`. `current_node` becomes `Node(a)`.
  - `char = 'p'`: Found in `Node(a).children`. `current_node` becomes `Node(p)`.
  - `char = 'p'`: Found in `Node(p).children`. `current_node` becomes `Node(p)_2`.
  - `char = 'l'`: Found in `Node(p)_2.children`. `current_node` becomes `Node(l)`.
  - `char = 'e'`: Found in `Node(l).children`. `current_node` becomes `Node(e)`.
  - Loop finishes.
  - Return `current_node.isEndOfWord`, which is `True`.
  - **Output: `True`**

### **4. `trie.search("app")`**

  - `current_node` starts at `root`.
  - `char = 'a'`: `current_node` becomes `Node(a)`.
  - `char = 'p'`: `current_node` becomes `Node(p)`.
  - `char = 'p'`: `current_node` becomes `Node(p)_2`.
  - Loop finishes.
  - Return `current_node.isEndOfWord`, which is `False`.
  - **Output: `False`**

### **5. `trie.startsWith("app")`**

  - `current_node` starts at `root`.
  - `char = 'a'`: `current_node` becomes `Node(a)`.
  - `char = 'p'`: `current_node` becomes `Node(p)`.
  - `char = 'p'`: `current_node` becomes `Node(p)_2`.
  - Loop finishes.
  - Return `True`.
  - **Output: `True`**

## Performance Analysis

Let `N` be the number of words inserted, `L` be the maximum length of a word, and `P` be the length of a prefix.

### `insert(word)`

  - **Time Complexity**: `O(L)`. We iterate once through the word's length. Dictionary lookups/insertions are `O(1)` on average.
  - **Space Complexity**: `O(L)`. In the worst case, we add `L` new nodes to the trie (if the word is new).

### `search(word)`

  - **Time Complexity**: `O(L)`. We iterate once through the word's length.
  - **Space Complexity**: `O(1)`. We only use one pointer.

### `startsWith(prefix)`

  - **Time Complexity**: `O(P)`. We iterate once through the prefix's length.
  - **Space Complexity**: `O(1)`. We only use one pointer.