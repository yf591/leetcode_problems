#
# @lc app=leetcode id=14 lang=python3
#
# [14] Longest Common Prefix
#


# @lc code=start
class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        # if the list is empty, there is no prefix.
        if not strs:
            return ""

        prefix = []
        # zip(*strs) groups characters at the same position from all strings.
        # For ["flower", "flow", "flight"], it creates tuples:
        # ('f', 'f', 'f'), ('l', 'l', 'l'), ('o', 'o', 'i'), ('w', 'w', 'g'), ...
        for char_tuple in zip(*strs):
            # A set will only have one element if all items in tuple are identical.
            if len(set(char_tuple)) == 1:
                # Add the common character to our prefix.
                prefix.append(char_tuple[0])
            else:
                # As soon as characters differ, the common prefix ends.
                break

        return "".join(prefix)


# @lc code=end
