#
# @lc app=leetcode id=207 lang=python3
#
# [207] Course Schedule
#


# @lc code=start
class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        # Step 1: Build the graph (adjacency list) and calculate in-degrees.
        graph = collections.defaultdict(list)
        in_degree = [0] * numCourses

        for course, prereq in prerequisites:
            graph[prereq].append(course)  # Edge: prereq -> course
            in_degree[course] += 1

        # Step 2: Initialize the queue with courses having 0 in-degree.
        queue = collections.deque([i for i in range(numCourses) if in_degree[i] == 0])

        # Step 3: Keep track of the number of courses completed.
        courses_taken = 0

        # Step 4: Process the queue.
        while queue:
            # Dequeue a course whose prerequisites are met.
            course = queue.popleft()
            courses_taken += 1

            # For each neighbor (courses that depend on this one)...
            for neighbor in graph[course]:
                # ...decrement their in-degree.
                in_degree[neighbor] -= 1
                # If all prerequisites for the neighbor are now met...
                if in_degree[neighbor] == 0:
                    # ...add it to the queue.
                    queue.append(neighbor)

        # Step 5: Check if all courses were completed.
        return courses_taken == numCourses


# @lc code=end
