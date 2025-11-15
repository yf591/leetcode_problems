#
# @lc app=leetcode id=2336 lang=python3
#
# [2336] Smallest Number in Infinite Set
#

import heapq


# @lc code=start
class SmallestInfiniteSet:

    def __init__(self):
        # The next integer in the infinite sequence (1, 2, 3, ...)
        self.current_smallest = 1

        # A min-heap to store any numbers that are added back.
        self.added_back_heap = []

        # A set to keep track of what's in the heap for O(1) duplicate checks.
        self.added_back_set = set()

    def popSmallest(self) -> int:

        # Check if the heap has any items that are smaller than
        # the next number in the main sequence.
        if self.added_back_heap and self.added_back_heap[0] < self.current_smallest:
            # The smallest number is in the heap.
            # Pop it from the heap.
            smallest = heapq.heappop(self.added_back_heap)
            # Remove it from the tracking set.
            self.added_back_set.remove(smallest)
            return smallest

        else:
            # The smallest number is from the main sequence.
            smallest = self.current_smallest
            # Advance the main sequence counter.
            self.current_smallest += 1
            return smallest

    def addBack(self, num: int) -> None:
        # We only add the number back if...
        # 1. It's smaller than our current sequence (i.e., it's a number
        #    that has been popped before).
        # 2. It's not *already* in our heap (to avoid duplicates).
        if num < self.current_smallest and num not in self.added_back_set:
            # Add to the heap and the tracking set.
            heapq.heappush(self.added_back_heap, num)
            self.added_back_set.add(num)


# Your SmallestInfiniteSet object will be instantiated and called as such:
# obj = SmallestInfiniteSet()
# param_1 = obj.popSmallest()
# obj.addBack(num)
# @lc code=end
