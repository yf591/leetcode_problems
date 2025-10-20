#
# @lc app=leetcode id=210 lang=python3
#
# [210] Course Schedule II
#


# @lc code=start
class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:

        # Step 1: Build the graph and calculate in-degrees.
        graph = collections.defaultdict(list)
        in_degree = [0] * numCourses

        for course, prereq in prerequisites:
            graph[prereq].append(course)  # Edge: prereq -> course
            in_degree[course] += 1

        # Step 2: Initialize the queue with courses having 0 in-degree.
        queue = collections.deque([i for i in range(numCourses) if in_degree[i] == 0])

        # Step 3: Initialize the list to store the result order.
        result_order = []

        # Step 4: Process the queue.
        while queue:
            # Dequeue a course whose prerequisites are met.
            course = queue.popleft()
            # Add it to our result order.
            result_order.append(course)

            # For each neighbor (courses that depend on this one)...
            for neighbor in graph[course]:
                # ...decrement their in-degree.
                in_degree[neighbor] -= 1
                # If all prerequisites for the neighbor are now met...
                if in_degree[neighbor] == 0:
                    # ...add it to the queue.
                    queue.append(neighbor)

        # Step 5: Check if a valid order including all courses was found.
        if len(result_order) == numCourses:
            return result_order
        else:
            # If not, a cycle exists, and it's impossible.
            return []


# @lc code=end
