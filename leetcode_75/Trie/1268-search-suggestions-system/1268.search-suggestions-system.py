#
# @lc app=leetcode id=1268 lang=python3
#
# [1268] Search Suggestions System
#


# @lc code=start
class Solution:
    def suggestedProducts(
        self, products: List[str], searchWord: str
    ) -> List[List[str]]:

        products.sort()

        result = []

        left, right = 0, len(products) - 1

        for i in range(len(searchWord)):
            char = searchWord[i]

            while left <= right and (
                len(products[left]) <= i or products[left][i] != char
            ):
                left += 1

            while left <= right and (
                len(products[right]) <= i or products[right][i] != char
            ):
                right -= 1

            suggestions = []
            num_sugge = min(3, right - left + 1)

            for j in range(num_sugge):
                suggestions.append(products[left + j])

            result.append(suggestions)

        return result


# @lc code=end
