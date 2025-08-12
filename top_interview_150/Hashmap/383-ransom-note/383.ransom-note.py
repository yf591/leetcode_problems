#
# @lc app=leetcode id=383 lang=python3
#
# [383] Ransom Note
#


# @lc code=start
class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        # Step 1: Create a frequency map (inventory) of the characters in the magazine.
        # e.g., for magazine="aab", this become {'a': 2, 'b': 1}
        magazine_counts = collections.Counter(magazine)

        # Step 2: Go through the ransomNote and and "use" characters from the inventory.
        for char in ransomNote:
            # Check if we have the required character in out inventory
            if magazine_counts[char] > 0:
                # If yes, use one by decrementing the count.
                magazine_counts[char] -= 1
            else:
                # If no, we can't build the note. Return False immediately.
                return False

        # If the loop completes, it means we had enough of every character.
        return True


# @lc code=end
