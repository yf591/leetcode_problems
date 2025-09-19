#
# @lc app=leetcode id=649 lang=python3
#
# [649] Dota2 Senate
#


# @lc code=start
class Solution:
    def predictPartyVictory(self, senate: str) -> str:
        n = len(senate)

        # Create two queues to store the indices of senators from each party.
        radiant_q = collections.deque()
        dire_q = collections.deque()

        # Populate the queues with the initial indices.
        for i, party in enumerate(senate):
            if party == "R":
                radiant_q.append(i)
            else:
                dire_q.append(i)

        # Loop as long as both parties still have senators in the queue.
        while radiant_q and dire_q:
            # Get the index of the next senator to vote from each party.
            r_idx = radiant_q.popleft()
            d_idx = dire_q.popleft()

            # The senator with the smaller index came first in the round
            # and gets to ban the other.
            if r_idx < d_idx:
                # Radiant senator bans the Dire senator. The Radiant senator's
                # right to vote is recycled to the next round.
                # We add 'n' to their index to signify they are at the end of the line.
                radiant_q.append(r_idx + n)
            else:
                # Dire senator bans the Radiant senator.
                dire_q.append(d_idx + n)

        # The loop ends when one queue is empty. The party with senators
        # remaining is the winner.
        return "Radiant" if radiant_q else "Dire"


# @lc code=end
