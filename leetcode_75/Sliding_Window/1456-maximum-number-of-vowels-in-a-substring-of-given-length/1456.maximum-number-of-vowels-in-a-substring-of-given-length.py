#
# @lc app=leetcode id=1456 lang=python3
#
# [1456] Maximum Number of Vowels in a Substring of Given Length
#


# @lc code=start
class Solution:
    def maxVowels(self, s: str, k: int) -> int:

        vowels = {"a", "e", "i", "o", "u"}

        # --- Step 1: Initialize the window ---
        # Calculate the vowel count for the first window of size 'k'.
        current_vowel_count = 0
        for i in range(k):
            if s[i] in vowels:
                current_vowel_count += 1

        # This is the maximum we've seen so far.
        max_vowel_count = current_vowel_count

        # --- Step 2: Slide the window across the rest of the string ---
        for i in range(k, len(s)):
            # Check the new character entering the window from the right.
            if s[i] in vowels:
                current_vowel_count += 1

            # Check the old character leaving the window from the left.
            # The leaving character is at index i - k.
            if s[i - k] in vowels:
                current_vowel_count -= 1

            # --- Step 3: Update the maximum ---
            max_vowel_count = max(max_vowel_count, current_vowel_count)

        return max_vowel_count


# @lc code=end
