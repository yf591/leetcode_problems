# 1732\. Find the Highest Altitude - Solution Explanation

## Problem Overview

You are given an integer array `gain`, where `gain[i]` represents the net change in altitude between point `i` and point `i+1` on a road trip. The trip starts at point 0 with an altitude of `0`. The goal is to find the **highest altitude** reached at any point during the trip.

**Key Definitions:**

  - **The Trip**: Consists of `n + 1` points, starting at point 0.
  - **Starting Point**: Altitude is always `0`.
  - **Altitude at point `i+1`**: Altitude at point `i` + `gain[i]`.

**Examples:**

```python
Input: gain = [-5,1,5,0,-7]
Output: 1
Explanation:
- Start at altitude 0.
- Point 1: 0 + (-5) = -5
- Point 2: -5 + 1 = -4
- Point 3: -4 + 5 = 1
- Point 4: 1 + 0 = 1
- Point 5: 1 + (-7) = -6
The sequence of altitudes is [0, -5, -4, 1, 1, -6]. The highest value in this sequence is 1.
```

## Key Insights

### Simulation and Accumulation

This problem is a straightforward **simulation**. There are no complex tricks required. The core idea is to simulate the biker's journey step by step, calculating the altitude at each point.

### Tracking Two States

To solve this, we only need to keep track of two pieces of information as we move through the `gain` array:

1.  **`current_altitude`**: The altitude of the biker right now.
2.  **`max_altitude`**: The highest altitude the biker has reached *at any point* in their journey so far.

By iterating through the gains and continuously updating these two variables, we can find the overall maximum by the end of the trip.

## Solution Approach

This solution iterates through the `gain` array a single time. It uses one variable to track the current altitude and another to track the maximum altitude seen so far.

```python
from typing import List

class Solution:
    def largestAltitude(self, gain: List[int]) -> int:
        # The biker starts at an altitude of 0.
        # This is also the highest altitude seen so far.
        current_altitude = 0
        max_altitude = 0
        
        # Iterate through each gain in altitude, simulating each leg of the journey.
        for altitude_gain in gain:
            # Calculate the new altitude after the current step.
            current_altitude += altitude_gain
            
            # Update the maximum altitude if the current one is higher.
            max_altitude = max(max_altitude, current_altitude)
            
        return max_altitude
```

**Strategy:**

1.  **Initialize**: Set both `current_altitude` and `max_altitude` to `0`, representing the starting point.
2.  **Iterate**: Loop through each `altitude_gain` in the `gain` list.
3.  **Accumulate**: Add the `altitude_gain` to `current_altitude`.
4.  **Compare**: Compare the new `current_altitude` with `max_altitude` and update `max_altitude` if necessary.
5.  **Return**: After the loop has processed all gains, `max_altitude` will hold the highest point reached.

## Detailed Code Analysis

### Step 1: Initialization

```python
current_altitude = 0
max_altitude = 0
```

  - We start `current_altitude` at `0` because the problem explicitly states, "The biker starts his trip on point 0 with altitude equal 0."
  - We also start `max_altitude` at `0`. The starting point is part of the journey, so it is our initial candidate for the highest point. This correctly handles cases where all gains are negative (e.g., the biker only goes downhill).

### Step 2: The Loop

```python
for altitude_gain in gain:
```

  - This `for` loop simulates the journey, step by step. Each `altitude_gain` represents one leg of the trip, from the current point to the next.

### Step 3: Updating the Current Altitude

```python
current_altitude += altitude_gain
```

  - This is the core of the simulation. `current_altitude` is an accumulator. With each step, we update our position by adding the net gain. For example, if we are at `-5` and the gain is `1`, our new altitude becomes `-4`.

### Step 4: Updating the Maximum Altitude

```python
max_altitude = max(max_altitude, current_altitude)
```

  - After arriving at a new altitude, we must check if we've set a new record. The `max()` function is a clean way to do this. It compares our `max_altitude` from all *previous* steps with the `current_altitude` and keeps the larger of the two.

## Step-by-Step Execution Trace

### Example: `gain = [-5, 1, 5, 0, -7]`

This table shows the state of the variables at the **end** of each loop iteration.

| Loop Step (`altitude_gain`) | `current_altitude` (before `+=`) | `current_altitude` (after `+=`) | `max_altitude` (before `max`) | `max_altitude` (after `max`) |
| :--- | :--- | :--- | :--- | :--- |
| **Start** | 0 | - | 0 | - |
| **-5** | 0 | **-5** | 0 | `max(0, -5)` -\> **0** |
| **1** | -5 | **-4** | 0 | `max(0, -4)` -\> **0** |
| **5** | -4 | **1** | 0 | `max(0, 1)` -\> **1** |
| **0** | 1 | **1** | 1 | `max(1, 1)` -\> **1** |
| **-7** | 1 | **-6** | 1 | `max(1, -6)` -\> **1** |

  - The loop finishes.
  - The function returns the final `max_altitude`, which is **1**.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the length of the `gain` array. We iterate through the list exactly once.

### Space Complexity: O(1)

  - We only use two variables (`current_altitude`, `max_altitude`) to store our state. The space required is constant and does not grow with the size of the input.

## Key Learning Points

  - **The "Running Total" or "Accumulation" Pattern**: This is a fundamental pattern in programming where you iterate through a sequence and maintain a running state (like a sum, count, or, in this case, `current_altitude`).
  - **Tracking a Running Maximum**: The technique of initializing a `max_variable` and comparing it against the current state in each step of a loop is a very common and essential pattern.
  - **Translating a Story Problem**: This problem shows how a real-world scenario (a bike trip) can be modeled with a simple loop and a few variables.