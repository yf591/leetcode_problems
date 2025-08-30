#
# @lc app=leetcode id=1207 lang=python3
#
# [1207] Unique Number of Occurrences
#


# @lc code=start
class Solution:
    def uniqueOccurrences(self, arr: List[int]) -> bool:
        # Step 1: Create a frequency map of the numbers in the array.
        # For arr = [1,2,2,1,1,3], this becomes {1: 3, 2: 2, 3: 1}
        counts = collections.Counter(arr)

        # Step 2: Get just the frequencies (the values from the map).
        # For our example, this would be a list like [3, 2, 1]
        occurrences = counts.values()

        # Step 3: Check if the frequencies are unique.
        # The length of the list of occurrences should be equal to the
        # number of unique occurrences (which is the length of a set of them).
        # For [3, 2, 1], len is 3. For set({3, 2, 1}), len is 3. They are equal.
        # For [1, 1, 2], len is 3. For set({1, 1, 2}), len is 2. They are not equal.
        return len(occurrences) == len(set(occurrences))


# @lc code=end
