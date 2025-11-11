#
# @lc app=leetcode id=2300 lang=python3
#
# [2300] Successful Pairs of Spells and Potions
#

# @lc code=start
import bisect
from typing import List


class Solution:
    def successfulPairs(
        self, spells: List[int], potions: List[int], success: int
    ) -> List[int]:

        # Step 1: Sort the potions array to enable binary search.
        potions.sort()

        m = len(potions)
        answer = []

        # Step 2: Iterate through each spell.
        for spell in spells:
            # Step 3: Calculate the minimum potion strength needed for this spell.
            target = success / spell

            # Step 4: Use binary search (bisect_left) to find the
            # leftmost index 'i' in 'potions' where potions[i] >= target.
            index = bisect.bisect_left(potions, target)

            # Step 5: The number of successful potions is the total number
            # of potions minus the index we found.
            # All potions from 'index' to the end of the list will be successful.
            count = m - index
            answer.append(count)

        return answer


# @lc code=end
