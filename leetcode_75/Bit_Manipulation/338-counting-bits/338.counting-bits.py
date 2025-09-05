#
# @lc app=leetcode id=338 lang=python3
#
# [338] Counting Bits
#


# @lc code=start
class Solution:
    def countBits(self, n: int) -> List[int]:

        # Initialize an array 'ans' of size n+1 with all zeros.
        # ans[0] is already correctly set to 0.
        ans = [0] * (n + 1)

        # Iterate from 1 up to n.
        for i in range(1, n + 1):
            # Apply the dynamic programming formula.
            # The number of 1s in 'i' is the number of 1s in 'i / 2'
            # plus the last bit of 'i'.

            # i >> 1 is a fast bitwise operation for i // 2
            # i % 2 gives the last bit (0 if even, 1 if odd)
            ans[i] = ans[i >> 1] + (i % 2)

        return ans


# @lc code=end
