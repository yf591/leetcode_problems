#
# @lc app=leetcode id=2542 lang=python3
#
# [2542] Maximum Subsequence Score
#

import heapq
from typing import List


# @lc code=start
class Solution:
    def maxScore(self, nums1: List[int], nums2: List[int], k: int) -> int:

        # 1. Create pairs of (nums1[i], nums2[i])
        pairs = list(zip(nums1, nums2))

        # 2. Sort the pairs based on nums2 in descending order
        #    We sort by the second element (x[1]) of the pair
        pairs.sort(key=lambda x: x[1], reverse=True)

        # 3. Use a min-heap to keep track of the k largest nums1 values
        min_heap = []
        current_sum = 0
        max_score = 0

        # 4. Iterate through the sorted pairs
        for n1, n2 in pairs:
            # Add the current nums1 value to the heap and sum
            heapq.heappush(min_heap, n1)
            current_sum += n1

            # If the heap is larger than k, remove the smallest element
            if len(min_heap) > k:
                smallest_n1 = heapq.heappop(min_heap)
                current_sum -= smallest_n1

            # If the heap has exactly k elements, we have a valid subsequence
            # We can calculate a potential score
            if len(min_heap) == k:
                # current_sum is the Sum(nums1) of the k largest elements
                # n2 is the Min(nums2) for this group (because we sorted)
                score = current_sum * n2
                max_score = max(max_score, score)

        return max_score


# @lc code=end
