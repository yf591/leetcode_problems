#
# @lc app=leetcode id=1431 lang=python3
#
# [1431] Kids With the Greatest Number of Candies
#


# @lc code=start
class Solution:
    def kidsWithCandies(self, candies: List[int], extraCandies: int) -> List[bool]:
        # max_candies = max(candies)

        # result_list = []
        # for candy_count in candies:
        #     result_bool = candy_count + extraCandies >= max_candies
        #     result_list.append(result_bool)

        # return result_list

        # Step 1: Find the maximum number of candies any kid currently has.
        max_candies = max(candies)

        # Step 2: Use a list comprehension to create the result list.
        # For each kid's candy_count, check if their new total would be the greatest.
        # The expression `(candy_count + extraCandies >= max_candies)`
        # evaluates directly to True or False.
        return [candy_count + extraCandies >= max_candies for candy_count in candies]


# @lc code=end
