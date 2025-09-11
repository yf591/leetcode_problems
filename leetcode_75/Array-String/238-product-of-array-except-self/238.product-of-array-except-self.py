#
# @lc app=leetcode id=238 lang=python3
#
# [238] Product of Array Except Self
#


# @lc code=start
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:

        n = len(nums)
        # Step 1: Initialize the answer array, for now it will hold prefix products.
        answer = [1] * n

        # --- Pass 1: Calculate and store the prefix products ---
        # The prefix product is the product of all elements to the left of the current index.
        prefix_product = 1
        for i in range(n):
            # For the current index 'i', the prefix product is what we've calculated so far.
            answer[i] = prefix_product
            # Then, update the prefix product for the next iteration by including the current number.
            prefix_product *= nums[i]

        # At the end of this loop, `answer` array looks like: [1, 1, 2, 6] for the input [1,2,3,4]

        # --- Pass 2: Calculate suffix products and get the final result ---
        # The suffix product is the product of all elements to the right of the current index.
        suffix_product = 1
        # Iterate from right to left.
        for i in range(n - 1, -1, -1):
            # Multiply the existing prefix product in `answer[i]` with the suffix product.
            # answer[i] (prefix) * suffix_product = final result
            answer[i] *= suffix_product
            # Then, update the suffix product for the next iteration by including the current number.
            suffix_product *= nums[i]

        return answer


# @lc code=end
