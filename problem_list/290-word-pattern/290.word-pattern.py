#
# @lc app=leetcode id=290 lang=python3
#
# [290] Word Pattern
#


# @lc code=start
class Solution:
    def wordPattern(self, pattern: str, s: str) -> bool:
        # Split the string 's' into a list of words.
        words = s.split(" ")

        # If the number of characters in the pattern doesn't match the
        # number of words, it's impossible for them to be isomorphic.
        if len(pattern) != len(words):
            return False

        # Use two maps to check the one-to-one mapping in both directions.
        map_pattern_to_words = {}
        map_words_to_pattern = {}

        for char, word in zip(pattern, words):

            # --- Check for a forward mapping conflict ---
            # If we have seen this character before...
            if char in map_pattern_to_words:
                # ...it must map to the same word it did before.
                if map_pattern_to_words[char] != word:
                    return False

            # --- Check for a backward mapping conflict
            # If the char in new, it the word has already been mapped to...
            elif word in map_words_to_pattern:
                # ...it's a conflict, because a new character can't map
                # to an already-used word.
                return False

            # If no conflicts, this is a new, valid mapping.
            else:
                map_pattern_to_words[char] = word
                map_words_to_pattern[word] = char

        # If the loop completes, the pattern is valid.
        return True


# @lc code=end
