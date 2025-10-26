#
# @lc app=leetcode id=1466 lang=python3
#
# [1466] Reorder Routes to Make All Paths Lead to the City Zero
#


# @lc code=start
class Solution:
    def minReorder(self, n: int, connections: List[List[int]]) -> int:

        # Build an adjacency list representing the graph.
        # Store tuples: (neighbor, cost_if_traversed_this_way)
        # cost = 1 if the original edge points away from the source node
        # cost = 0 if the original edge points towards the source node
        graph = collections.defaultdict(list)
        for u, v in connections:
            graph[u].append((v, 1))  # Original edge u -> v (cost 1 to traverse u to v)
            graph[v].append(
                (u, 0)
            )  # Represents edge u -> v (cost 0 to traverse v to u)

        # Perform BFS starting from city 0
        queue = collections.deque([0])
        visited = {0}
        reorder_count = 0

        while queue:
            city = queue.popleft()

            for neighbor, cost in graph[city]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    # If cost is 1, it means the original edge was city -> neighbor,
                    # which is away from city 0 (our traversal direction). Needs reorder.
                    reorder_count += cost
                    queue.append(neighbor)

        return reorder_count


# @lc code=end
