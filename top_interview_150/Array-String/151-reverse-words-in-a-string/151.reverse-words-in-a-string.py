#
# @lc app=leetcode id=151 lang=python3
#
# [151] Reverse Words in a String
#


# @lc code=start
class Solution:
    def reverseWords(self, s: str) -> str:

        # Step 1: Split the string into a list of words.
        # The split() method, when called without arguments, automatically
        # handles any amount of whitespace and removes empty strings.
        # e.g., "  a good   example  " -> ['a', 'good', 'example']
        word_list = s.split()

        # Step 2: Reverse the order of the words in the list.
        # The slice notation [::-1] is a common Python idiom for reversing a list.
        # e.g., ['a', 'good', 'example'] -> ['example', 'good', 'a']
        reversed_list = word_list[::-1]

        # Step 3: Join the words in the reversed list back into a single string,
        # with a single space (" ") as the separator.
        # e.g., ['example', 'good', 'a'] -> "example good a"
        return " ".join(reversed_list)


# @lc code=end
