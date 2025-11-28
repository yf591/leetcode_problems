#
# @lc app=leetcode id=373 lang=python3
#
# [373] Find K Pairs with Smallest Sums
#

import heapq
from typing import List


# @lc code=start
class Solution:
    def kSmallestPairs(
        self, nums1: List[int], nums2: List[int], k: int
    ) -> List[List[int]]:

        # Min-heap to store tuples: (current_sum, index_in_nums1, index_in_nums2)
        min_heap = []
        result = []

        # Step 1: Initialize the heap.
        # We treat the problem like merging 'k' sorted arrays.
        # We take the first element of nums1 paired with the first element of nums2,
        # the second element of nums1 paired with the first of nums2, etc.
        # Optimization: We only need to check the first 'k' elements of nums1,
        # because any element after index k in nums1 paired with nums2[0]
        # is guaranteed to be larger than the k-th smallest sum.
        for i in range(min(k, len(nums1))):
            current_sum = nums1[i] + nums2[0]
            # Push (sum, index_i, index_j)
            heapq.heappush(min_heap, (current_sum, i, 0))

        # Step 2: Extract the smallest pairs and add next candidates
        while k > 0 and min_heap:
            current_sum, i, j = heapq.heappop(min_heap)
            result.append([nums1[i], nums2[j]])

            # If there is a next element in nums2 for the current nums1[i],
            # add that pair to the heap.
            if j + 1 < len(nums2):
                next_sum = nums1[i] + nums2[j + 1]
                heapq.heappush(min_heap, (next_sum, i, j + 1))

            k -= 1

        return result


# @lc code=end
