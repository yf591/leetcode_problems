#
# @lc app=leetcode id=66 lang=python3
#
# [66] Plus One
#


# @lc code=start
class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        n = len(digits)

        # Iterate through the digits from right to left.
        for i in range(n - 1, -1, -1):
            # If the current digit is less than 9, we can just add one
            # and there's no need to 'carry over'. We can return immediately.
            if digits[i] < 9:
                digits[i] += 1
                return digits

            # If the digit is 9, it becomes 0, and the 'carry' will be
            # handled by adding one to the next digit in the loop.
            digits[i] = 0

        # If the loop completes, it means all digits were 9s(e.g., [9, 9]).
        # The array has become all 0s (e.g., [0, 0]). and we need to add a leading 1.
        return [1] + digits


# @lc code=end
