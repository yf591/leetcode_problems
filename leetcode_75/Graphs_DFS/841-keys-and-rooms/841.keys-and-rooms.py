#
# @lc app=leetcode id=841 lang=python3
#
# [841] Keys and Rooms
#


# @lc code=start
class Solution:
    def canVisitAllRooms(self, rooms: List[List[int]]) -> bool:

        num_rooms = len(rooms)
        # A set to keep track of rooms we have visited.
        visited = set()
        # A stack to manage the rooms we need to explore. Start with room 0.
        stack = [0]

        # Mark the starting room as visited.
        visited.add(0)

        # While there are still rooms to explore...
        while stack:
            # Get the next room to visit from the stack.
            current_room = stack.pop()

            # Look at the keys in the current room.
            for key in rooms[current_room]:
                # If the key unlocks a room we haven't visited yet...
                if key not in visited:
                    # ...mark it as visited...
                    visited.add(key)
                    # ...and add it to the stack to explore later.
                    stack.append(key)

        # After the traversal, check if we visited all rooms.
        return len(visited) == num_rooms


# @lc code=end
