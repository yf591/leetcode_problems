# 626. Exchange Seats - SQL Solution Explanation

## Problem Overview
Given a `Seat` table, swap the seat id of every two consecutive students. If the number of students is odd, the id of the last student is not swapped.

**Input Example:**
```
+----+---------+
| id | student |
+----+---------+
| 1  | Abbot   |
| 2  | Doris   |
| 3  | Emerson |
| 4  | Green   |
| 5  | Jeames  |
+----+---------+
```

**Output Example:**
```
+----+---------+
| id | student |
+----+---------+
| 1  | Doris   |
| 2  | Abbot   |
| 3  | Green   |
| 4  | Emerson |
| 5  | Jeames  |
+----+---------+
```

## Understanding the Problem

### Seat Exchange Patterns
- **Odd ID (1, 3, 5...)**: Exchange with next student (first in pair)
- **Even ID (2, 4, 6...)**: Exchange with previous student (second in pair)
- **Last odd ID**: No exchange partner, remains unchanged

**Visual Understanding:**
```
Original:  [1:Abbot] [2:Doris] [3:Emerson] [4:Green] [5:Jeames]
After:     [1:Doris] [2:Abbot] [3:Green]   [4:Emerson] [5:Jeames]
           ↑────────swap────────↑ ↑───────swap───────↑    ↑
           Pair 1               Pair 2              Alone(unchanged)
```

## Algorithm: Using Window Functions

**Core Idea:**
- **LEAD()**: Get value from next row
- **LAG()**: Get value from previous row  
- **CASE statement**: Conditional logic based on odd/even ID
- **COALESCE()**: Handle NULL values

## Step-by-Step Solution Breakdown

### Step 1: Understanding the Basic Structure

```sql
SELECT
    id,
    CASE
        WHEN id % 2 = 1  -- For odd IDs
            THEN [get next student]
        ELSE             -- For even IDs  
            [get previous student]
    END AS student
FROM Seat
```

### Step 2: Understanding COALESCE() in Detail

#### What is COALESCE()?
**COALESCE(value1, value2, value3, ...)**
- Checks values from left to right
- **Returns the first non-NULL value**
- Returns NULL only if all values are NULL

#### Practical Examples
```sql
-- Basic examples
SELECT COALESCE(NULL, NULL, 'Hello', 'World');  -- Result: 'Hello'
SELECT COALESCE(NULL, 'First', 'Second');       -- Result: 'First' 
SELECT COALESCE('Found', 'Backup');             -- Result: 'Found'
SELECT COALESCE(NULL, NULL, NULL);              -- Result: NULL
```

#### Purpose in This Problem
```sql
COALESCE(LEAD(student) OVER (ORDER BY id), student)
```

**Behavior Patterns:**
- **When LEAD() returns a value**: Use that value (normal exchange)
- **When LEAD() returns NULL**: Use original student (last student)

**Concrete Examples:**
```sql
-- ID 1 (odd): LEAD() returns 'Doris'
COALESCE('Doris', 'Abbot') → 'Doris'

-- ID 3 (odd): LEAD() returns 'Green'  
COALESCE('Green', 'Emerson') → 'Green'

-- ID 5 (odd, last): LEAD() returns NULL
COALESCE(NULL, 'Jeames') → 'Jeames'  ★ Key point!
```

### Step 3: Window Functions Operation

#### Understanding LEAD() and LAG()
```sql
-- Original table with window function results
| id | student  | LEAD(student) | LAG(student) |
|----|----------|---------------|--------------|
| 1  | Abbot    | Doris        | NULL         |
| 2  | Doris    | Emerson      | Abbot        |
| 3  | Emerson  | Green        | Doris        |
| 4  | Green    | Jeames       | Emerson      |
| 5  | Jeames   | NULL         | Green        |
```

#### Detailed Conditional Logic
```sql
CASE
    WHEN id % 2 = 1  -- Odd case
        THEN COALESCE(LEAD(student) OVER (ORDER BY id), student)
    ELSE             -- Even case
        LAG(student) OVER (ORDER BY id)
END
```

## Detailed Processing Trace for Each Row

### ID 1 (Odd) Processing
```sql
-- Condition: 1 % 2 = 1 (odd)
-- LEAD(student): 'Doris' (next row's student)
-- COALESCE('Doris', 'Abbot'): 'Doris'
-- Result: 'Doris' assigned to ID 1
```

### ID 2 (Even) Processing  
```sql
-- Condition: 2 % 2 = 0 (even)
-- LAG(student): 'Abbot' (previous row's student)
-- Result: 'Abbot' assigned to ID 2
```

### ID 3 (Odd) Processing
```sql
-- Condition: 3 % 2 = 1 (odd)
-- LEAD(student): 'Green' (next row's student)
-- COALESCE('Green', 'Emerson'): 'Green'
-- Result: 'Green' assigned to ID 3
```

### ID 4 (Even) Processing
```sql
-- Condition: 4 % 2 = 0 (even)
-- LAG(student): 'Emerson' (previous row's student)
-- Result: 'Emerson' assigned to ID 4
```

### ID 5 (Odd, Last) Processing ★Important★
```sql
-- Condition: 5 % 2 = 1 (odd)
-- LEAD(student): NULL (no next row exists)
-- COALESCE(NULL, 'Jeames'): 'Jeames' (original value used)
-- Result: 'Jeames' assigned to ID 5 (unchanged)
```

## Why Last Odd ID Remains Unchanged?

### Automatic Preservation Mechanism

1. **LEAD() Characteristic**: Returns NULL for last row (no next row exists)
2. **COALESCE() Function**: When first value is NULL, adopts next value
3. **Result**: `COALESCE(NULL, student)` → Original `student` value

### Visual Understanding
```
Odd ID Processing Logic:
┌─────────────────┐
│ For Odd IDs     │
├─────────────────┤
│ Get next student│ → LEAD(student)
│ ↓              │
│ Exists?        │
│ ├─ Yes: Use that student │ → Execute exchange
│ └─ No(NULL): Use original│ → Keep unchanged
└─────────────────┘

Concrete Examples:
ID 1: LEAD() → 'Doris' → Use 'Doris' (exchange)
ID 3: LEAD() → 'Green' → Use 'Green' (exchange)  
ID 5: LEAD() → NULL → Use 'Jeames' (keep unchanged)
```

## Complete Processing Flow

### Input Data
```sql
| id | student  |
|----|----------|
| 1  | Abbot    |
| 2  | Doris    |
| 3  | Emerson  |
| 4  | Green    |
| 5  | Jeames   |
```

### Processing Result Table for Each Row
| id | Condition | LEAD(student) | LAG(student) | COALESCE Result | Final Result |
|----|-----------|---------------|--------------|----------------|-------------|
| 1  | Odd       | 'Doris'       | -           | 'Doris'        | 'Doris'     |
| 2  | Even      | -             | 'Abbot'     | -              | 'Abbot'     |
| 3  | Odd       | 'Green'       | -           | 'Green'        | 'Green'     |
| 4  | Even      | -             | 'Emerson'   | -              | 'Emerson'   |
| 5  | Odd       | NULL          | -           | 'Jeames'       | 'Jeames'    |

### Final Output
```sql
| id | student  |
|----|----------|
| 1  | Doris    |  ← Exchanged with Abbot
| 2  | Abbot    |  ← Exchanged with Doris  
| 3  | Green    |  ← Exchanged with Emerson
| 4  | Emerson  |  ← Exchanged with Green
| 5  | Jeames   |  ← Unchanged (no exchange partner)
```

## Edge Cases Handling

### Case 1: Even Number of Students (Complete Pairs)
```sql
-- Input: 4 students
| id | student  |
|----|----------|
| 1  | A        |
| 2  | B        |
| 3  | C        |
| 4  | D        |

-- Output: All pairs exchanged
| id | student  |
|----|----------|
| 1  | B        |
| 2  | A        |
| 3  | D        |
| 4  | C        |
```

### Case 2: Single Student (Odd)
```sql
-- Input: 1 student
| id | student  |
|----|----------|
| 1  | A        |

-- Process: LEAD() → NULL, COALESCE(NULL, 'A') → 'A'
-- Output: Unchanged
| id | student  |
|----|----------|
| 1  | A        |
```

### Case 3: Two Students Only (Even)
```sql
-- Input: 2 students  
| id | student  |
|----|----------|
| 1  | A        |
| 2  | B        |

-- Output: Complete exchange
| id | student  |
|----|----------|
| 1  | B        |
| 2  | A        |
```

## Alternative Approaches Comparison

### Approach 1: UNION ALL Method (Complex)
```sql
-- Even ID processing
SELECT id-1 as id, student FROM Seat WHERE id % 2 = 0
UNION ALL
-- Odd ID processing  
SELECT id+1 as id, student FROM Seat WHERE id % 2 = 1 AND id < (SELECT MAX(id) FROM Seat)
UNION ALL
-- Last odd ID processing
SELECT id, student FROM Seat WHERE id % 2 = 1 AND id = (SELECT MAX(id) FROM Seat)
ORDER BY id;
```
**Problems:**
- Complex conditional logic
- Multiple subqueries required
- Poor readability

### Approach 2: Self Join Method (Complex)
```sql
SELECT 
    s1.id,
    CASE 
        WHEN s1.id % 2 = 1 THEN COALESCE(s2.student, s1.student)
        ELSE s3.student 
    END as student
FROM Seat s1
LEFT JOIN Seat s2 ON s1.id = s2.id - 1  -- Next student
LEFT JOIN Seat s3 ON s1.id = s3.id + 1  -- Previous student
ORDER BY s1.id;
```
**Problems:**
- Multiple JOINs required
- Potentially worse performance

### Current Solution Advantages (Window Functions)
```sql
SELECT
    id,
    CASE
        WHEN id % 2 = 1
            THEN COALESCE(LEAD(student) OVER (ORDER BY id), student)
        ELSE
            LAG(student) OVER (ORDER BY id)
    END AS student
FROM Seat
ORDER BY id;
```

**Advantages:**
- ✅ **Conciseness**: Single query solution
- ✅ **Readability**: Clear intent
- ✅ **Efficiency**: Single table scan
- ✅ **Maintainability**: Easy to understand and modify

## Key SQL Concepts Demonstrated

### 1. Window Functions
```sql
-- Syntax: function() OVER (ORDER BY column)
LEAD(student) OVER (ORDER BY id)   -- Next row
LAG(student) OVER (ORDER BY id)    -- Previous row
```

### 2. COALESCE Function
```sql
-- Standard method for NULL value handling
COALESCE(value1, value2, default_value)
-- If value1 is not NULL → value1, if NULL → value2, if that's also NULL → default_value
```

### 3. Conditional Logic (CASE Statement)
```sql
CASE
    WHEN condition1 THEN result1
    WHEN condition2 THEN result2
    ELSE default_result
END
```

### 4. Modulo Operator (%)
```sql
id % 2 = 1  -- Odd number check
id % 2 = 0  -- Even number check
```

## Practical Debugging Methods

### Step 1: Verify Window Functions Results
```sql
SELECT 
    id, 
    student,
    LEAD(student) OVER (ORDER BY id) as next_student,
    LAG(student) OVER (ORDER BY id) as prev_student
FROM Seat;
```

### Step 2: Check Conditional Logic
```sql
SELECT 
    id,
    student,
    id % 2 as remainder,
    CASE WHEN id % 2 = 1 THEN 'odd' ELSE 'even' END as id_type
FROM Seat;
```

### Step 3: Verify COALESCE Behavior
```sql
SELECT 
    id,
    student,
    LEAD(student) OVER (ORDER BY id) as lead_result,
    COALESCE(LEAD(student) OVER (ORDER BY id), student) as coalesce_result
FROM Seat
WHERE id % 2 = 1;  -- Odd IDs only
```

## Performance Analysis

### Time Complexity
- **Single Pass**: O(n) where n = number of rows
- **Window Functions**: Efficient built-in operations
- **No Joins**: Avoids expensive join operations

### Space Complexity
- **Memory Usage**: O(1) additional space
- **Window Buffer**: Minimal overhead for LEAD/LAG operations

### Scalability
- **Large Tables**: Performs well with proper indexing on `id`
- **Memory Efficient**: No temporary table creation required

## Real-World Applications

1. **Seat Management Systems**: Theater and airline seat swapping
2. **Team Formation**: Sports pair reorganization
3. **Data Pairing**: Sequential data reorganization processing
4. **Rotation Management**: Work shift exchanges
5. **Experimental Data**: Control group reorganization

## Common Mistakes and Solutions

### 1. Forgetting COALESCE for Last Row
```sql
-- ❌ Wrong: Last odd ID would get NULL
WHEN id % 2 = 1 THEN LEAD(student) OVER (ORDER BY id)

-- ✅ Correct: Handle NULL case with COALESCE
WHEN id % 2 = 1 THEN COALESCE(LEAD(student) OVER (ORDER BY id), student)
```

### 2. Incorrect Modulo Logic
```sql
-- ❌ Wrong: Confusing odd/even logic
WHEN id % 2 = 0 THEN LEAD(student) OVER (ORDER BY id)

-- ✅ Correct: Odd IDs get next student
WHEN id % 2 = 1 THEN COALESCE(LEAD(student) OVER (ORDER BY id), student)
```

### 3. Missing ORDER BY in Window Functions
```sql
-- ❌ Wrong: Undefined order
LEAD(student) OVER ()

-- ✅ Correct: Specify order
LEAD(student) OVER (ORDER BY id)
```

### 4. Forgetting Final ORDER BY
```sql
-- ❌ Wrong: Result order not guaranteed
SELECT id, ... FROM Seat

-- ✅ Correct: Ensure proper ordering
SELECT id, ... FROM Seat ORDER BY id
```

## Advanced Variations

### Variation 1: Exchange Every N Students
```sql
-- Exchange every 3 students instead of 2
SELECT 
    id,
    CASE 
        WHEN id % 3 = 1 THEN COALESCE(LEAD(student, 2) OVER (ORDER BY id), student)
        WHEN id % 3 = 2 THEN student  -- Middle stays
        ELSE LAG(student, 2) OVER (ORDER BY id)
    END as student
FROM Seat;
```

### Variation 2: Reverse Exchange Pattern
```sql
-- Even IDs get next, Odd IDs get previous
SELECT 
    id,
    CASE 
        WHEN id % 2 = 0 THEN COALESCE(LEAD(student) OVER (ORDER BY id), student)
        ELSE LAG(student) OVER (ORDER BY id)
    END as student
FROM Seat;
```

This SQL solution demonstrates an excellent example of practical window function usage and the importance of NULL value handling with the COALESCE function for robust data processing.