#
# @lc app=leetcode id=443 lang=python3
#
# [443] String Compression
#


# @lc code=start
class Solution:
    def compress(self, chars: List[str]) -> int:

        i = 0  # read_pointer
        j = 0  # write_pointer
        n = len(chars)

        while i < n:
            # Start of a new group.
            char_to_write = chars[i]
            count = 0

            # Count how many consecutive characters are the same as char_to_write.
            # This inner loop moves 'i' forward to the end of the current group.
            while i < n and chars[i] == char_to_write:
                count += 1
                i += 1

            # --- Write the compressed result ---

            # 1. Write the character itself.
            chars[j] = char_to_write
            j += 1

            # 2. If the group was larger than 1, write the count.
            if count > 1:
                # Convert count to string and write each digit.
                for digit in str(count):
                    chars[j] = digit
                    j += 1

        # 'j' is now the new length of the compressed array.
        return j


# @lc code=end
