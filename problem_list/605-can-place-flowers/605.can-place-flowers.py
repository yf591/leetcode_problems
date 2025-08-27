#
# @lc app=leetcode id=605 lang=python3
#
# [605] Can Place Flowers
#


# @lc code=start
class Solution:
    def canPlaceFlowers(self, flowerbed: List[int], n: int) -> bool:
        # If we need to plant 0 flowers, the answer is always true.
        if n == 0:
            return True

        # We can modify the flowerbed list in-place.
        for i in range(len(flowerbed)):
            # Check if the current plot is empty.
            if flowerbed[i] == 0:
                # Check if the left plot is empty.
                # This is true if we're at the beginning (i=0) or the plot to the left is 0.
                is_left_empty = (i == 0) or (flowerbed[i - 1] == 0)

                # Check if the right plot is empty.
                # This is true if we're at the end or the plot to the right is 0.
                is_right_empty = (i == len(flowerbed) - 1) or (flowerbed[i + 1] == 0)

                # If both sides are empty, we can plant a flower here.
                if is_left_empty and is_right_empty:
                    # Place the flower.
                    flowerbed[i] = 1
                    # Decrement the number of flowers we still need to plant.
                    n -= 1
                    # If we've planted all required flowers, we can stop early.
                    if n == 0:
                        return True

        # If the loop finishes and n is 0, we succeeded.
        return n == 0


# @lc code=end
