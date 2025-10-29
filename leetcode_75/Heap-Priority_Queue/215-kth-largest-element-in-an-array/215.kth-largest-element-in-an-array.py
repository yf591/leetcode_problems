#
# @lc app=leetcode id=215 lang=python3
#
# [215] Kth Largest Element in an Array
#

import heapq
from typing import List


# @lc code=start
class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:

        # We use a min-heap to keep track of the k largest elements seen so far.
        # Initialize an empty min-heap.
        min_heap = []

        for num in nums:
            # Add the current number to the heap.
            heapq.heappush(min_heap, num)

            # If the heap size exceeds k, remove the smallest element.
            if len(min_heap) > k:
                heapq.heappop(min_heap)

        # After iterating through all numbers, the root of the min-heap
        # (the smallest element among the k largest) is the k-th largest element.
        return min_heap[0]


# @lc code=end
