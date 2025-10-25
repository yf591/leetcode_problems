#
# @lc app=leetcode id=547 lang=python3
#
# [547] Number of Provinces
#


# @lc code=start
class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        n = len(isConnected)
        # Keep track of visited cities (nodes).
        visited = [False] * n
        province_count = 0

        def dfs(city_index):
            """Recursive DFS function to mark all cities in a province."""
            # Mark the current city as visited.
            visited[city_index] = True
            # Check all potential neighbors of the current city.
            for neighbor_index in range(n):
                # If there's a connection and the neighbor hasn't been visited...
                if (
                    isConnected[city_index][neighbor_index] == 1
                    and not visited[neighbor_index]
                ):
                    # ...recursively visit the neighbor.
                    dfs(neighbor_index)

        # Iterate through all cities.
        for i in range(n):
            # If a city hasn't been visited yet, it's part of a new province.
            if not visited[i]:
                # Increment the province count.
                province_count += 1
                # Start DFS to find and mark all cities in this new province.
                dfs(i)

        return province_count


# @lc code=end
