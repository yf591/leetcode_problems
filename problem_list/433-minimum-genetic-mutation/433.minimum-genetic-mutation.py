#
# @lc app=leetcode id=433 lang=python3
#
# [433] Minimum Genetic Mutation
#

import collections
from typing import List


# @lc code=start
class Solution:
    def minMutation(self, startGene: str, endGene: str, bank: List[str]) -> int:

        # --- Initialization ---

        # Convert the bank to a set for efficient O(1) lookups.
        bank_set = set(bank)

        # Edge case: If the endGene isn't even in the bank,
        # it's impossible to reach.
        if endGene not in bank_set:
            return -1

        # Initialize the queue for BFS with the starting gene and 0 steps.
        queue = collections.deque([(startGene, 0)])

        # Keep track of genes we've already visited to avoid loops.
        visited = {startGene}

        # --- BFS Traversal ---

        while queue:
            # Get the next gene and its step count from the front of the queue.
            current_gene, steps = queue.popleft()

            # If we've reached the target, return the number of steps.
            if current_gene == endGene:
                return steps

            # --- Generate all possible 1-character mutations ---

            # Iterate through each character position in the gene.
            for i in range(len(current_gene)):
                # For each position, try changing it to each possible gene character.
                for char in "ACGT":
                    # Create the new mutation.
                    new_gene = current_gene[:i] + char + current_gene[i + 1 :]

                    # Check if this new_gene is a valid next step.
                    if new_gene in bank_set and new_gene not in visited:
                        # If it is, mark it as visited and add it to the queue.
                        visited.add(new_gene)
                        queue.append((new_gene, steps + 1))

        # If the queue becomes empty and we never reached the endGene,
        # it's impossible.
        return -1


# @lc code=end
