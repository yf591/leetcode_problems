#
# @lc app=leetcode id=205 lang=python3
#
# [205] Isomorphic Strings
#


# @lc code=start
class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        # We need two maps to check the one-to-one mapping in both directions.
        map_s_to_t = {}
        map_t_to_s = {}

        # The zip function is a clean way to iterate through both strings in parallel.
        for char_s, char_t in zip(s, t):

            # Check forward mapping: s -> t
            if char_s in map_s_to_t:
                # If We have seen this character in a before, it must map
                # to the same character in t as it did before.
                if map_s_to_t[char_s] != char_t:
                    return False

            # Check backward mapping: t -> s
            elif char_t in map_t_to_s:
                # If we have not seen char_s before, but we have seen char_t,
                # it mean char_t is already mapped to by a different character
                # from s, which violates the one-to-one rule.
                return False

            else:
                # If this is a new, valid mapping, record it in both directions.
                map_s_to_t[char_s] = char_t
                map_t_to_s[char_t] = char_s

        # If the loop completes without finding any inconsistencies,
        # the strings are isomorphic.
        return True


# @lc code=end
