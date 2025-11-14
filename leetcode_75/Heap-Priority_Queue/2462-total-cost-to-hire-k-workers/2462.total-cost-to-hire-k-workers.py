#
# @lc app=leetcode id=2462 lang=python3
#
# [2462] Total Cost to Hire K Workers
#

import heapq
from typing import List


# @lc code=start
class Solution:
    def totalCost(self, costs: List[int], k: int, candidates: int) -> int:

        n = len(costs)
        total_cost = 0

        # Pointers for the next available worker to add to the heaps
        left_ptr = 0
        right_ptr = n - 1

        # Heaps store (cost, index)
        left_heap = []
        right_heap = []

        # --- Step 1: Initialize the heaps with the first 'candidates' from each side ---

        # Fill the left heap
        for _ in range(candidates):
            if left_ptr <= right_ptr:
                heapq.heappush(left_heap, (costs[left_ptr], left_ptr))
                left_ptr += 1

        # Fill the right heap
        for _ in range(candidates):
            if left_ptr <= right_ptr:
                heapq.heappush(right_heap, (costs[right_ptr], right_ptr))
                right_ptr -= 1

        # --- Step 2: Run the k hiring sessions ---
        for _ in range(k):
            # Check if one of the heaps is empty
            if not right_heap:
                # Must hire from left
                cost, _ = heapq.heappop(left_heap)
                total_cost += cost
            elif not left_heap:
                # Must hire from right
                cost, _ = heapq.heappop(right_heap)
                total_cost += cost

            # Both heaps have candidates, so compare them
            elif left_heap[0] <= right_heap[0]:
                # Left heap wins (lower cost or same cost with lower index)
                cost, _ = heapq.heappop(left_heap)
                total_cost += cost

                # Refill the left heap from the middle
                if left_ptr <= right_ptr:
                    heapq.heappush(left_heap, (costs[left_ptr], left_ptr))
                    left_ptr += 1
            else:
                # Right heap wins
                cost, _ = heapq.heappop(right_heap)
                total_cost += cost

                # Refill the right heap from the middle
                if left_ptr <= right_ptr:
                    heapq.heappush(right_heap, (costs[right_ptr], right_ptr))
                    right_ptr -= 1

        return total_cost


# @lc code=end
