#
# @lc app=leetcode id=399 lang=python3
#
# [399] Evaluate Division
#


# @lc code=start
class Solution:
    def calcEquation(
        self, equations: List[List[str]], values: List[float], queries: List[List[str]]
    ) -> List[float]:
        # Step 1: Build the graph (adjacency list).
        # graph maps a variable -> list of (neighbor, ratio)
        # An edge from A to B with weight 'val' represents A / B = val.
        graph = collections.defaultdict(list)
        for i, (A, B) in enumerate(equations):
            val = values[i]
            graph[A].append((B, val))
            graph[B].append((A, 1.0 / val))

        def bfs(start_node, end_node):
            """
            Performs BFS to find the product of weights from start to end.
            Returns start_node / end_node.
            """
            # Handle cases where one of the nodes was never seen in the equations.
            if start_node not in graph or end_node not in graph:
                return -1.0

            # Queue stores tuples of (current_node, current_product_value)
            # where current_product_value = start_node / current_node
            queue = collections.deque([(start_node, 1.0)])
            # 'visited' set is crucial for each query to avoid cycles.
            visited = {start_node}

            while queue:
                current_node, current_product = queue.popleft()

                if current_node == end_node:
                    return current_product  # Path found!

                # Explore neighbors
                for neighbor, ratio in graph[current_node]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        # New product = (start / current) * (current / neighbor) = start / neighbor
                        new_product = current_product * ratio
                        queue.append((neighbor, new_product))

            # If the loop finishes, no path was found between start and end.
            return -1.0

        # Step 2: Process all queries.
        results = []
        for C, D in queries:
            results.append(bfs(C, D))

        return results


# @lc code=end
