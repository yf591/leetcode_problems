#
# @lc app=leetcode id=49 lang=python3
#
# [49] Group Anagrams
#


# @lc code=start
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:

        # Create a dictionary where keys will be the sorted-character version of a word,
        # and values will be a list of all anagrams for that key.
        # defaultdict(list) simplifies the code by creating an empty list for new keys.
        anagram_map = collections.defaultdict(list)

        # Iterate through each word in the input list.
        for word in strs:
            # Create the canonical key by sorting the word's characters.
            # e.g., "eat" -> ('e','a','t') -> "aet"
            sorted_key = "".join(sorted(word))

            # Append the original word to the list associated with its sorted key.
            anagram_map[sorted_key].append(word)

        # The values of the map are the lists of grouped anagrams.
        # We return them as a list.
        return list(anagram_map.values())


# @lc code=end
