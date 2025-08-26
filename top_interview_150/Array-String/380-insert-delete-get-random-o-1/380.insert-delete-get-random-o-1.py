#
# @lc app=leetcode id=380 lang=python3
#
# [380] Insert Delete GetRandom O(1)
#


# @lc code=start
class RandomizedSet:

    def __init__(self):
        # Dictionary to map a value to its index in the list
        self.val_to_index = {}
        # List to store the actual values for O(1) random access
        self.val_list = []

    def insert(self, val: int) -> bool:
        # Check for existence in O(1) using the dictionary
        if val in self.val_to_index:
            return False

        # Add the new value's index to the map. The new index is the
        # current length of the list.
        self.val_to_index[val] = len(self.val_list)
        # Append the new value to the end of the list.
        self.val_list.append(val)
        return True

    def remove(self, val: int) -> bool:
        # Check for existence in O(1) using the dictionary
        if val not in self.val_to_index:
            return False

        # --- The Swap-and-Pop Trick ---
        # 1. Get the index of the element to remove and the value of the last element.
        index_to_remove = self.val_to_index[val]
        last_val = self.val_list[-1]

        # 2. Move the last element to the position of the element to be removed.
        self.val_list[index_to_remove] = last_val

        # 3. Update the index of the moved element in the dictionary.
        self.val_to_index[last_val] = index_to_remove

        # 4. Remove the last element from the list (this is O(1)).
        self.val_list.pop()

        # 5. Remove the target value from the dictionary.
        del self.val_to_index[val]

        return True

    def getRandom(self) -> int:
        # random.choice provides O(1) random selection from a list.
        return random.choice(self.val_list)


# Your RandomizedSet object will be instantiated and called as such:
# obj = RandomizedSet()
# param_1 = obj.insert(val)
# param_2 = obj.remove(val)
# param_3 = obj.getRandom()
# @lc code=end
