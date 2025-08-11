#
# @lc app=leetcode id=392 lang=python3
#
# [392] Is Subsequence
#


# @lc code=start
class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        # Pointers for the subsequence 's' and the main string 't'
        s_pointer = 0
        t_pointer = 0

        # Loop as long as we haven't reached the end of either string.
        while s_pointer < len(s) and t_pointer < len(t):
            # If the characters match, it means we have found the next character
            # of the subsequence, so we advance the 's' pointer.
            if s[s_pointer] == t[t_pointer]:
                s_pointer += 1

            # We always advance the 't' pointer to scan through the main string.
            t_pointer += 1

        # If we have successfully found all characters in 's', the s_pointer
        # will be equal to the length of 's'.
        return s_pointer == len(s)


# @lc code=end
