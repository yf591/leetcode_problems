# 1204. Last Person to Fit in the Bus - Solution Explanation

## Problem Overview

Find the **last person** who can board a bus without exceeding the **1000kg weight limit**. People board in order of their `turn` value, and we need the cumulative weight to stay within the limit.

**Table Schema:**
```sql
Queue table:
+-----------+-------------+--------+------+
| person_id | person_name | weight | turn |
+-----------+-------------+--------+------+
| 5         | Alice       | 250    | 1    |
| 4         | Bob         | 175    | 5    |
| 3         | Alex        | 350    | 2    |
| 6         | John Cena   | 400    | 3    |
| 1         | Winston     | 500    | 6    |
| 2         | Marie       | 200    | 4    |
+-----------+-------------+--------+------+
```

**Expected Process:**
```sql
Boarding order (sorted by turn):
+------+-----------+--------+--------------+
| Turn | Name      | Weight | Total Weight |
+------+-----------+--------+--------------+
| 1    | Alice     | 250    | 250          |
| 2    | Alex      | 350    | 600          |
| 3    | John Cena | 400    | 1000         | ← Last person to fit
| 4    | Marie     | 200    | 1200         | ← Exceeds limit
| 5    | Bob       | 175    | 1375         | ← Cannot board
| 6    | Winston   | 500    | 1875         | ← Cannot board
+------+-----------+--------+--------------+

Answer: John Cena
```

## Key Insights

### Running Sum (Cumulative Weight) Concept
```sql
-- Need to calculate cumulative weight for each person
-- Must follow the boarding order (sorted by turn)
-- Window function SUM() OVER() is perfect for this
```

### "Last Person to Fit" Definition
```sql
-- Condition: cumulative_weight <= 1000
-- Goal: Person with MAXIMUM turn value among those who fit
-- Approach: Filter + Sort + Limit pattern
```

### Window Function Power
```sql
-- Traditional approach: Self-join or correlated subquery
-- Modern approach: Window function with ORDER BY
-- Benefit: Single scan, efficient, readable
```

## Solution Approach

Our solution uses **Window Functions with Running Sum** to calculate cumulative weights, then finds the last person within the limit:

```sql
WITH
    RunningTotal AS (
        -- First, calculate the cumulative (running) sum of weight
        -- order by the turn.
        SELECT
            person_name,
            turn,
            SUM(weight) OVER (ORDER BY turn) AS cumulative_weight
        FROM
            Queue
    )
-- Then, from the people whose cumulative weight is within the limit,
-- find the one with the latest turn.
SELECT
    person_name
FROM
    RunningTotal
WHERE
    cumulative_weight <= 1000
ORDER BY
    turn DESC
LIMIT 1;
```

**Strategy:**
1. **CTE with Window Function**: Calculate running sum of weights ordered by turn
2. **Filter within limit**: Keep only people whose cumulative weight ≤ 1000
3. **Find maximum turn**: Sort by turn DESC and take first result
4. **Return last person**: The person with highest turn value who fits

## Step-by-Step Breakdown

### Step 1: CTE with Window Function
```sql
RunningTotal AS (
    SELECT
        person_name,
        turn,
        SUM(weight) OVER (ORDER BY turn) AS cumulative_weight
    FROM
        Queue
)
```

**Window Function Mechanics:**
```sql
-- SUM(weight) OVER (ORDER BY turn)
-- Calculates cumulative sum following turn order
-- Each row gets "total weight up to this person"
-- ORDER BY turn ensures correct boarding sequence
```

**Why Window Function is Optimal:**
```sql
-- Alternative: Correlated subquery (inefficient)
SELECT person_name, 
       (SELECT SUM(weight) FROM Queue q2 WHERE q2.turn <= q1.turn)
FROM Queue q1

-- Our approach: Window function (efficient)
SELECT person_name, SUM(weight) OVER (ORDER BY turn)
FROM Queue

-- Benefits: Single scan, optimized execution, cleaner syntax
```

### Step 2: Window Function Execution

#### Internal Sorting Process
```sql
-- Window function automatically sorts by turn:
Original data → Sort by turn → Calculate running sum
```

#### Cumulative Sum Calculation
```sql
-- For each row, sum all weights from turn=1 to current turn:
Turn 1: SUM(250) = 250
Turn 2: SUM(250 + 350) = 600  
Turn 3: SUM(250 + 350 + 400) = 1000
Turn 4: SUM(250 + 350 + 400 + 200) = 1200
Turn 5: SUM(...previous... + 175) = 1375
Turn 6: SUM(...previous... + 500) = 1875
```

#### CTE Result Generation
```sql
RunningTotal:
+-------------+------+-------------------+
| person_name | turn | cumulative_weight |
+-------------+------+-------------------+
| Alice       | 1    | 250               |
| Alex        | 2    | 600               |
| John Cena   | 3    | 1000              | ← Exactly at limit
| Marie       | 4    | 1200              | ← Exceeds limit
| Bob         | 5    | 1375              | ← Exceeds limit
| Winston     | 6    | 1875              | ← Exceeds limit
+-------------+------+-------------------+
```

### Step 3: Final Query Execution

#### WHERE Clause Filtering
```sql
WHERE cumulative_weight <= 1000
```

**Filtering Logic:**
```sql
-- Keep only people who can board without exceeding limit
-- Include people with cumulative_weight exactly equal to 1000
-- Exclude all people whose boarding would exceed limit
```

**Filtered Result:**
```sql
+-------------+------+-------------------+
| person_name | turn | cumulative_weight |
+-------------+------+-------------------+
| Alice       | 1    | 250               | ✓ Within limit
| Alex        | 2    | 600               | ✓ Within limit
| John Cena   | 3    | 1000              | ✓ Exactly at limit
+-------------+------+-------------------+
```

#### ORDER BY turn DESC
```sql
-- Sort by turn in descending order
-- Brings person with highest turn value to top
-- "Last person to board" appears first in result
```

**Sorted Result:**
```sql
+-------------+------+-------------------+
| person_name | turn | cumulative_weight |
+-------------+------+-------------------+
| John Cena   | 3    | 1000              | ← Highest turn value
| Alex        | 2    | 600               |
| Alice       | 1    | 250               |
+-------------+------+-------------------+
```

#### LIMIT 1 Selection
```sql
-- Take only the first row
-- Gets person with maximum turn value among those who fit
-- Final answer: John Cena
```

**Final Result:**
```sql
+-------------+
| person_name |
+-------------+
| John Cena   |
+-------------+
```

## Detailed Execution Analysis

### Input Data Transformation

#### Original Queue Table (Unordered)
```sql
+-----------+-------------+--------+------+
| person_id | person_name | weight | turn |
+-----------+-------------+--------+------+
| 5         | Alice       | 250    | 1    |
| 4         | Bob         | 175    | 5    |
| 3         | Alex        | 350    | 2    |
| 6         | John Cena   | 400    | 3    |
| 1         | Winston     | 500    | 6    |
| 2         | Marie       | 200    | 4    |
+-----------+-------------+--------+------+
```

#### Window Function Internal Processing
```sql
-- Step 1: Sort by turn (internal to window function)
+-------------+--------+------+
| person_name | weight | turn |
+-------------+--------+------+
| Alice       | 250    | 1    |
| Alex        | 350    | 2    |
| John Cena   | 400    | 3    |
| Marie       | 200    | 4    |
| Bob         | 175    | 5    |
| Winston     | 500    | 6    |
+-------------+--------+------+

-- Step 2: Calculate running sum for each row
Row 1: 250 (Alice only)
Row 2: 250 + 350 = 600 (Alice + Alex)
Row 3: 600 + 400 = 1000 (Alice + Alex + John Cena)
Row 4: 1000 + 200 = 1200 (+ Marie)
Row 5: 1200 + 175 = 1375 (+ Bob)
Row 6: 1375 + 500 = 1875 (+ Winston)
```

### Complete Execution Trace

#### CTE Generation Process
```sql
-- Window function processes rows in turn order:
Processing turn=1: Alice (250) → cumulative = 250
Processing turn=2: Alex (350) → cumulative = 250 + 350 = 600
Processing turn=3: John Cena (400) → cumulative = 600 + 400 = 1000
Processing turn=4: Marie (200) → cumulative = 1000 + 200 = 1200
Processing turn=5: Bob (175) → cumulative = 1200 + 175 = 1375
Processing turn=6: Winston (500) → cumulative = 1375 + 500 = 1875
```

#### Final Query Step-by-Step
```sql
-- Step 1: Apply WHERE filter
WHERE cumulative_weight <= 1000:
- Alice (250) ✓
- Alex (600) ✓  
- John Cena (1000) ✓
- Marie (1200) ✗
- Bob (1375) ✗
- Winston (1875) ✗

-- Step 2: Apply ORDER BY turn DESC
Sorted result: [John Cena (turn=3), Alex (turn=2), Alice (turn=1)]

-- Step 3: Apply LIMIT 1
Final result: John Cena
```

## Critical Design Decisions

### Window Function vs Alternatives

#### Our Approach: Window Function
```sql
-- Efficient single-pass solution
SUM(weight) OVER (ORDER BY turn)
-- Time: O(n log n) - due to sorting
-- Space: O(n) - for result set
-- Readability: Excellent
```

#### Alternative 1: Correlated Subquery
```sql
SELECT person_name
FROM Queue q1
WHERE (
    SELECT SUM(weight)
    FROM Queue q2  
    WHERE q2.turn <= q1.turn
) <= 1000
ORDER BY turn DESC LIMIT 1;

-- Time: O(n²) - subquery for each row
-- Space: O(1) - no intermediate storage
-- Readability: Poor - nested structure
```

#### Alternative 2: Self-Join with Aggregation
```sql
SELECT q1.person_name
FROM Queue q1
JOIN Queue q2 ON q2.turn <= q1.turn
GROUP BY q1.person_id, q1.person_name, q1.turn
HAVING SUM(q2.weight) <= 1000
ORDER BY q1.turn DESC LIMIT 1;

-- Time: O(n²) - join creates n² combinations
-- Space: O(n²) - temporary join result
-- Readability: Moderate - complex join logic
```

### ORDER BY Placement Strategy
```sql
-- Window function ORDER BY: Defines calculation sequence
SUM(weight) OVER (ORDER BY turn)  -- Controls running sum order

-- Final query ORDER BY: Defines result order  
ORDER BY turn DESC  -- Controls which row appears first

-- Both are necessary for correct solution
```

### LIMIT 1 vs MAX() Comparison
```sql
-- Our approach: ORDER BY + LIMIT
ORDER BY turn DESC LIMIT 1  -- Gets full row information

-- Alternative: MAX() approach
WHERE turn = (SELECT MAX(turn) FROM filtered_results)  -- More complex

-- LIMIT approach is simpler and more efficient
```

## Performance Analysis

### Time Complexity: O(n log n)
```sql
-- Window function: O(n log n) - internal sorting required
-- WHERE filtering: O(n) - linear scan
-- ORDER BY: O(k log k) where k = number of qualifying rows
-- LIMIT 1: O(1) - constant time
-- Overall: O(n log n) - dominated by window function sorting
```

### Space Complexity: O(n)
```sql
-- CTE result set: O(n) - stores all rows with cumulative weights
-- Window function buffer: O(n) - internal sorting space
-- Final result: O(1) - single row output
-- Overall: O(n) - linear space requirement
```

### Database Optimization Opportunities
```sql
-- Recommended indexes:
CREATE INDEX idx_queue_turn ON Queue(turn);
CREATE INDEX idx_queue_turn_weight ON Queue(turn, weight);

-- Benefits:
-- Faster window function sorting
-- Efficient ORDER BY operations  
-- Better overall query performance
```

## Edge Cases and Robustness

### Edge Case 1: Single Person Within Limit
```sql
Input: One person with weight ≤ 1000
Processing:
- CTE: cumulative_weight = individual weight
- WHERE: passes if ≤ 1000
- ORDER BY + LIMIT: returns that person
Result: Correct ✓
```

### Edge Case 2: All People Exceed Limit
```sql
Input: Even first person exceeds 1000kg
Note: Problem states "first person does not exceed the limit"
This case is guaranteed not to occur by problem constraints
```

### Edge Case 3: Multiple People with Same Turn
```sql
Input: Two people with turn=3 (violates uniqueness constraint)
Note: Problem states turn contains all numbers 1 to n uniquely
This case is impossible by problem definition
```

### Edge Case 4: Exact Weight Limit Match
```sql
Input: Cumulative weight exactly equals 1000
Processing: WHERE cumulative_weight <= 1000 includes this case
Result: Person is correctly included as last to board ✓
```

### Edge Case 5: Two People with Cumulative Weight ≤ 1000
```sql
Input: First two people both fit, third exceeds limit
Processing:
- Both people pass WHERE filter
- ORDER BY turn DESC puts second person first
- LIMIT 1 selects second person
Result: Correct - latest person who fits ✓
```

### Edge Case 6: Empty Queue Table
```sql
Input: No rows in Queue table
Processing:
- CTE: Empty result set
- Final query: Empty result set
Result: Empty result (handled gracefully) ✓
```

## Alternative Solutions Comparison

### Solution 1: Recursive CTE Approach
```sql
WITH RECURSIVE BusLoading AS (
    -- Base case: first person
    SELECT person_name, turn, weight, weight as cumulative_weight
    FROM Queue WHERE turn = 1
    
    UNION ALL
    
    -- Recursive case: add next person if within limit
    SELECT q.person_name, q.turn, q.weight, 
           bl.cumulative_weight + q.weight
    FROM Queue q
    JOIN BusLoading bl ON q.turn = bl.turn + 1
    WHERE bl.cumulative_weight + q.weight <= 1000
)
SELECT person_name FROM BusLoading 
ORDER BY turn DESC LIMIT 1;
```

**Analysis:**
- ✅ **Logical**: Directly simulates boarding process
- ✅ **Clear stopping**: Automatically stops when limit exceeded  
- ❌ **Complexity**: Recursive CTE is advanced concept
- ❌ **Performance**: Recursive processing overhead
- ❌ **Portability**: Not supported by all databases

### Solution 2: Variables Simulation (MySQL-specific)
```sql
SELECT person_name
FROM (
    SELECT person_name, turn,
           @running_total := @running_total + weight as cumulative_weight
    FROM Queue, (SELECT @running_total := 0) r
    ORDER BY turn
) t
WHERE cumulative_weight <= 1000
ORDER BY turn DESC LIMIT 1;
```

**Analysis:**
- ✅ **Performance**: Single scan with variables
- ✅ **Simplicity**: Straightforward logic
- ❌ **Portability**: MySQL-specific syntax
- ❌ **Reliability**: Variable behavior can be unpredictable
- ❌ **Deprecated**: Variables discouraged in modern SQL

### Solution 3: Analytical Function with ROWS
```sql
WITH RunningTotals AS (
    SELECT person_name, turn,
           SUM(weight) OVER (
               ORDER BY turn 
               ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
           ) as cumulative_weight
    FROM Queue
)
SELECT person_name
FROM RunningTotals
WHERE cumulative_weight <= 1000
ORDER BY turn DESC LIMIT 1;
```

**Analysis:**
- ✅ **Explicit**: ROWS clause makes window frame clear
- ✅ **Standard**: ANSI SQL compliant
- ❌ **Verbose**: More complex than necessary
- ❌ **Redundant**: Default window frame is sufficient
- ✅ **Educational**: Good for learning window frames

## Why Our Solution is Optimal

### 1. **Optimal Performance**
```sql
-- Single table scan with efficient window function
-- O(n log n) time complexity - best possible for sorted results
-- Linear space usage - minimal memory overhead
-- No expensive joins or correlated subqueries
```

### 2. **Maximum Readability**
```sql
-- Clear separation of concerns with CTE
-- Self-documenting window function
-- Standard SQL patterns familiar to developers
-- Comments explain business logic
```

### 3. **Database Portability**
```sql
-- Uses standard SQL window functions
-- Works on PostgreSQL, SQL Server, Oracle, MySQL 8.0+
-- No vendor-specific extensions
-- Future-proof solution
```

### 4. **Maintainability**
```sql
-- Easy to modify weight limit (change 1000 to any value)
-- Simple to add additional filtering conditions
-- Debuggable structure - can examine CTE results
-- Follows established SQL patterns
```

### 5. **Robust Edge Case Handling**
```sql
-- Automatically handles boundary conditions
-- Works correctly with any data distribution
-- No special cases or conditional logic needed
-- Graceful handling of empty inputs
```

## Real-World Applications

### Transportation and Logistics
```sql
-- Vehicle loading optimization (trucks, ships, planes)
-- Passenger capacity management for buses/trains
-- Freight distribution with weight constraints
-- Elevator capacity management
```

### Manufacturing and Production
```sql
-- Batch processing with capacity limits
-- Assembly line optimization
-- Quality control threshold management
-- Resource allocation with constraints
```

### Financial Services
```sql
-- Risk limit management (cumulative exposure)
-- Transaction processing with daily limits
-- Portfolio weight allocation
-- Credit line utilization tracking
```

### Resource Management
```sql
-- Server capacity planning (CPU, memory, storage)
-- Network bandwidth allocation
-- Database connection pool management
-- Queue processing with rate limits
```

## SQL Concepts Demonstrated

### Window Functions Mastery
```sql
-- SUM() OVER() for running totals
-- ORDER BY in window specification
-- Efficient analytical processing
-- Alternative to complex self-joins
```

### CTE (Common Table Expression) Usage
```sql
-- Query structure organization
-- Intermediate result naming and reuse
-- Complex query decomposition
-- Improved readability and debugging
```

### Filtering and Sorting Patterns
```sql
-- WHERE clause for condition-based filtering
-- ORDER BY with DESC for maximum value queries
-- LIMIT for top-N result selection
-- Combined patterns for optimal queries
```

### Performance Optimization Techniques
```sql
-- Single-pass solutions over multiple passes
-- Window functions vs correlated subqueries
-- Efficient sorting and filtering strategies
-- Index-friendly query structures
```

## Best Practices Demonstrated

### 1. **Problem Decomposition**
```sql
-- Step 1: Calculate what we need (running totals)
-- Step 2: Filter based on constraints (weight limit)
-- Step 3: Find optimal result (latest person)
-- Clear logical progression
```

### 2. **Query Structure Organization**
```sql
-- CTE for data preparation
-- Main query for business logic
-- Comments explaining each step
-- Meaningful column aliases
```

### 3. **Performance Consciousness**
```sql
-- Choose efficient algorithms (window functions)
-- Avoid expensive operations (correlated subqueries)
-- Consider index implications
-- Scalable solution design
```

### 4. **Code Quality Standards**
```sql
-- Consistent formatting and indentation
-- Descriptive variable names
-- Clear comments explaining logic
-- Standard SQL conventions
```

## Minor Code Quality Improvements

### Typo Corrections
```sql
-- Original code had typos:
"caluculate" → "calculate"
"culculative_weight" → "cumulative_weight"

-- Corrected version:
WITH RunningTotal AS (
    -- First, calculate the cumulative (running) sum of weight
    -- ordered by turn.
    SELECT
        person_name,
        turn,
        SUM(weight) OVER (ORDER BY turn) AS cumulative_weight
    FROM Queue
)
```

This solution exemplifies how window functions can elegantly solve complex analytical problems. The running sum calculation combined with filtering and sorting creates an efficient, readable, and maintainable solution for constraint-based optimization problems commonly found in real-world applications.