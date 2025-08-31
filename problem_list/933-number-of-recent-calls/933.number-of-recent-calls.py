#
# @lc app=leetcode id=933 lang=python3
#
# [933] Number of Recent Calls
#


# @lc code=start
class RecentCounter:

    def __init__(self):
        # We use a deque (double-ended queue) to efficiently add to the right
        # and remove from the left.
        self.requests = collections.deque()

    def ping(self, t: int) -> int:
        # Step 1: Add the new request's timestamp to our queue.
        self.requests.append(t)

        # Step 2: Remove any old requests from the front of the queue
        # that are no longer in the [t - 3000, t] window.
        # The start of the window is `t - 3000`.
        while self.requests[0] < t - 3000:
            self.requests.popleft()

        # Step 3: The size of the queue is now the number of recent requests.
        return len(self.requests)


# Your RecentCounter object will be instantiated and called as such:
# obj = RecentCounter()
# param_1 = obj.ping(t)
# @lc code=end
