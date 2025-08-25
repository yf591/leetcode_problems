#
# @lc app=leetcode id=274 lang=python3
#
# [274] H-Index
#


# @lc code=start
class Solution:
    def hIndex(self, citations: List[int]) -> int:
        n = len(citations)

        # Sort the citations in descending (high to low) order.
        citations.sort(reverse=True)

        h = 0
        # Iterate through the sorted list. The index 'i' represents
        # having seen i+1 papers.
        for i in range(n):
            # The number of papers we are considering is i + 1.
            # The minimum citation count for these papers is citations[i].

            # If the citation count is greater than or equal to the number of papers,
            # it means we have a valid h-index of at least i + 1.
            if citations[i] >= i + 1:
                h = i + 1
            else:
                # The moment this condition fails, we can't have a higher h-index,
                # so we can break early.
                break

        return h


# @lc code=end
