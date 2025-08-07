# 1341. Movie Rating - SQL Solution Explanation

## Problem Overview
This problem requires two different results in a single query:
1. **Find the user who has rated the greatest number of movies** (lexicographically smallest in case of tie)
2. **Find the movie with the highest average rating in February 2020** (lexicographically smallest in case of tie)

**Input Example:**
```
Movies: [Avengers, Frozen 2, Joker]
Users: [Daniel, Monica, Maria, James]
MovieRating: 9 rating records
```

**Output Example:**
```
+--------------+
| results      |
+--------------+
| Daniel       |
| Frozen 2     |
+--------------+
```

## Understanding the Problem

### Requirements Analysis
1. **Part 1**: Aggregate user rating counts and identify the most active user
2. **Part 2**: Calculate movie average ratings for February 2020 and find the highest-rated movie
3. **Common Condition**: In case of ties, select lexicographically smallest value (alphabetical order)

**Visual Understanding:**
```
Part 1: User Rating Count Analysis
Daniel: 3 movies (Avengers, Frozen 2, Joker)
Monica: 3 movies (Avengers, Frozen 2, Joker)
→ Tie-breaker: Daniel < Monica (lexicographically)

Part 2: February 2020 Average Rating Analysis
Frozen 2: (5+2)/2 = 3.5 average
Joker: (3+4)/2 = 3.5 average
→ Tie-breaker: Frozen 2 < Joker (lexicographically)
```

## Algorithm: UNION ALL + Subqueries

**Core Idea:**
- **UNION ALL**: Vertically combine two independent query results
- **GROUP BY + Aggregate Functions**: Data aggregation processing
- **ORDER BY + LIMIT**: Top 1 selection based on conditions
- **JOIN**: Retrieve related data between tables

## Step-by-Step Solution Breakdown

### Step 1: Understanding the Overall Structure

```sql
(SELECT ... -- Part 1: Most Active User
 FROM ... 
 ORDER BY COUNT(*) DESC, u.name ASC
 LIMIT 1)

UNION ALL

(SELECT ... -- Part 2: Best Rated Movie in Feb 2020
 FROM ...
 WHERE ...  -- February 2020 filter
 ORDER BY AVG(mr.rating) DESC, m.title ASC
 LIMIT 1);
```

### Step 2: Part 1 - Identifying the Most Active User

```sql
(SELECT
    u.name AS results
FROM
    MovieRating AS mr
LEFT JOIN
    Users AS u ON mr.user_id = u.user_id
GROUP BY
    u.name
ORDER BY
    COUNT(*) DESC, u.name ASC
LIMIT
    1)
```

#### Understanding COUNT(*) in Detail

**What is COUNT(*)？**
- `COUNT(*)` is an **aggregate function that counts rows**
- The asterisk (`*`) means "all columns"
- **Counts the existence of rows themselves, regardless of specific column values**

**How COUNT(*) Works:**
```sql
-- Example: Daniel's rating data
| user_id | movie_id | rating | created_at |
|---------|----------|--------|------------|
| 1       | 1        | 3      | 2020-01-12 |
| 1       | 2        | 5      | 2020-02-17 |
| 1       | 3        | 3      | 2020-02-22 |

-- After GROUP BY u.name for Daniel's group
COUNT(*) = 3  -- 3 rows exist
```

**Difference between COUNT(*) and COUNT(column):**
```sql
-- COUNT(*): Counts all rows (including those with NULL)
SELECT COUNT(*) FROM table;  -- Total row count

-- COUNT(column): Counts non-NULL values in specific column
SELECT COUNT(rating) FROM table;  -- Count of non-NULL ratings

-- Practical comparison example
| user_id | rating |
|---------|--------|
| 1       | 5      |
| 2       | NULL   |
| 3       | 4      |

COUNT(*) = 3        -- All 3 rows
COUNT(rating) = 2   -- 2 non-NULL ratings
```

**Why use COUNT(*) in this problem:**
- We want to know **how many movies each user rated**
- The content of the rating value doesn't matter, **the number of rating actions is important**
- 1 row in MovieRating table = 1 rating action

#### Understanding GROUP BY and COUNT(*) Relationship

**How GROUP BY u.name works:**
```sql
-- Original data (after MovieRating + Users JOIN)
| user_id | name   | movie_id | rating |
|---------|--------|----------|--------|
| 1       | Daniel | 1        | 3      |
| 1       | Daniel | 2        | 5      |
| 1       | Daniel | 3        | 3      |
| 2       | Monica | 1        | 4      |
| 2       | Monica | 2        | 2      |
| 2       | Monica | 3        | 4      |
| 3       | Maria  | 1        | 2      |
| 3       | Maria  | 2        | 2      |
| 4       | James  | 1        | 1      |

-- After GROUP BY u.name - Logical groups
Group 1 (Daniel): 
| 1 | Daniel | 1 | 3 |
| 1 | Daniel | 2 | 5 |
| 1 | Daniel | 3 | 3 |

Group 2 (Monica):
| 2 | Monica | 1 | 4 |
| 2 | Monica | 2 | 2 |
| 2 | Monica | 3 | 4 |

Group 3 (Maria):
| 3 | Maria  | 1 | 2 |
| 3 | Maria  | 2 | 2 |

Group 4 (James):
| 4 | James  | 1 | 1 |
```

**COUNT(*) operates on each group:**
```sql
-- Execute COUNT(*) for each group
SELECT u.name, COUNT(*)
FROM MovieRating AS mr
LEFT JOIN Users AS u ON mr.user_id = u.user_id
GROUP BY u.name;

-- Result:
| name   | COUNT(*) |
|--------|----------|
| Daniel | 3        |  ← Row count in Daniel group
| Monica | 3        |  ← Row count in Monica group  
| Maria  | 2        |  ← Row count in Maria group
| James  | 1        |  ← Row count in James group
```

#### Detailed Operation of ORDER BY COUNT(*) DESC, u.name ASC

**Step 1: Primary Sort - COUNT(*) DESC**
```sql
-- Sort by COUNT(*) value in descending order
| name   | COUNT(*) |
|--------|----------|
| Daniel | 3        |  ← Most ratings
| Monica | 3        |  ← Most ratings
| Maria  | 2        |  ← Second most
| James  | 1        |  ← Least ratings
```

**Step 2: Tie-breaker - u.name ASC**
```sql
-- When COUNT(*) is the same, sort by name in ascending order
| name   | COUNT(*) |
|--------|----------|
| Daniel | 3        |  ← Daniel < Monica (alphabetically)
| Monica | 3        |  
| Maria  | 2        |  
| James  | 1        |  
```

**Step 3: Select top 1 with LIMIT 1**
```sql
-- Final result
| name   |
|--------|
| Daniel |  ← Most ratings & alphabetically smallest
```

### Step 3: Understanding JOIN vs LEFT JOIN in Detail

#### JOIN (INNER JOIN) Properties
```sql
-- INNER JOIN: Returns only records that match in both tables
FROM MovieRating AS mr
JOIN Users AS u ON mr.user_id = u.user_id
```

**INNER JOIN Behavior:**
```
MovieRating Table:     Users Table:
| user_id | movie_id |  | user_id | name   |
|---------|----------|  |---------|--------|
| 1       | 1        |  | 1       | Daniel |
| 2       | 1        |  | 2       | Monica |
| 99      | 2        |  | 3       | Maria  |

INNER JOIN Result:
| user_id | movie_id | name   |
|---------|----------|--------|
| 1       | 1        | Daniel |
| 2       | 1        | Monica |
-- user_id=99 record is excluded (doesn't exist in Users table)
```

#### LEFT JOIN Properties
```sql
-- LEFT JOIN: All records from left table + matching records from right table
FROM MovieRating AS mr
LEFT JOIN Users AS u ON mr.user_id = u.user_id
```

**LEFT JOIN Behavior:**
```
LEFT JOIN Result:
| user_id | movie_id | name   |
|---------|----------|--------|
| 1       | 1        | Daniel |
| 2       | 1        | Monica |
| 99      | 2        | NULL   |  -- No match in right table, filled with NULL
```

#### Which is More Appropriate for This Problem?

**Problem Constraints:**
- MovieRating table's `user_id` always exists in Users table (foreign key constraint)
- Similarly, `movie_id` always exists in Movies table

**Conclusion:**
```sql
-- ✅ Both produce the same result (no orphan records due to constraints)
JOIN Users AS u ON mr.user_id = u.user_id
LEFT JOIN Users AS u ON mr.user_id = u.user_id

-- ✅ More accurate choice: JOIN (INNER JOIN)
-- Reason: Clear intent that we only deal with guaranteed matching data
```

**Best Practices:**
- **When data integrity is guaranteed**: Use `JOIN`
- **When orphan records are possible**: Use `LEFT JOIN`
- **Intent clarification**: JOIN type expresses design intent

### Step 4: Part 2 - Finding the Best Rated Movie

```sql
(SELECT
    m.title AS results
FROM
    MovieRating AS mr
LEFT JOIN
    Movies AS m ON mr.movie_id = m.movie_id
WHERE
    mr.created_at >= '2020-02-01' AND mr.created_at < '2020-03-01'
GROUP BY
    m.title
ORDER BY
    AVG(mr.rating) DESC, m.title ASC
LIMIT
    1)
```

#### February 2020 Filter Details
```sql
-- Precise February 2020 range specification
WHERE mr.created_at >= '2020-02-01' AND mr.created_at < '2020-03-01'

-- Alternative patterns (same result)
WHERE mr.created_at BETWEEN '2020-02-01' AND '2020-02-29'
WHERE YEAR(mr.created_at) = 2020 AND MONTH(mr.created_at) = 2
```

### Step 5: Result Combination with UNION ALL

```sql
-- UNION ALL: Vertically combine results without removing duplicates
(SELECT ...) UNION ALL (SELECT ...)
```

**UNION vs UNION ALL Difference:**
```sql
-- UNION: Removes duplicate rows
SELECT 'A' UNION SELECT 'A'     -- Result: 'A' (1 row)

-- UNION ALL: Keeps duplicate rows
SELECT 'A' UNION ALL SELECT 'A' -- Result: 'A', 'A' (2 rows)
```

**Why use UNION ALL in this problem:**
- Combining answers to two different questions
- No possibility of duplication (user names vs movie titles)
- UNION ALL is faster (no duplicate checking required)

## Detailed Example Walkthrough

### Part 1: User Rating Count Calculation

**MovieRating Data Analysis:**
```sql
-- User rating count aggregation
| user_id | name   | ratings_count |
|---------|--------|---------------|
| 1       | Daniel | 3             | (movies: 1,2,3)
| 2       | Monica | 3             | (movies: 1,2,3)
| 3       | Maria  | 2             | (movies: 1,2)
| 4       | James  | 1             | (movie: 1)

-- ORDER BY COUNT(*) DESC, u.name ASC
-- 1. COUNT(*) DESC: Order 3,3,2,1
-- 2. u.name ASC: Daniel < Monica (for ties)
-- LIMIT 1: Daniel
```

### Part 2: February 2020 Movie Average Rating Calculation

**February 2020 Data Filtering:**
```sql
-- Data after filtering
| movie_id | title    | rating | created_at |
|----------|----------|--------|------------|
| 1        | Avengers | 4      | 2020-02-11 |
| 1        | Avengers | 2      | 2020-02-12 |
| 2        | Frozen 2 | 5      | 2020-02-17 |
| 2        | Frozen 2 | 2      | 2020-02-01 |
| 3        | Joker    | 3      | 2020-02-22 |
| 3        | Joker    | 4      | 2020-02-25 |

-- Movie average ratings
| title    | avg_rating |
|----------|------------|
| Avengers | (4+2)/2 = 3.0 |
| Frozen 2 | (5+2)/2 = 3.5 |
| Joker    | (3+4)/2 = 3.5 |

-- ORDER BY AVG(mr.rating) DESC, m.title ASC
-- 1. AVG DESC: Order 3.5, 3.5, 3.0
-- 2. m.title ASC: Frozen 2 < Joker (for ties)
-- LIMIT 1: Frozen 2
```

### Final Result
```sql
| results  |
|----------|
| Daniel   |  ← Part 1 result
| Frozen 2 |  ← Part 2 result
```

## Edge Cases Handling

### Case 1: All Users Have Same Rating Count
```sql
-- When everyone has rated 2 movies
| name   | count |
|--------|-------|
| Alice  | 2     |
| Bob    | 2     |
| Charlie| 2     |

-- ORDER BY COUNT(*) DESC, name ASC
-- Result: Alice (alphabetically smallest)
```

### Case 2: Movies with No Ratings in February 2020
```sql
-- Automatically excluded by WHERE clause
-- Not subject to GROUP BY
-- Not included in average rating calculation
```

### Case 3: Multiple Movies with Same Average Rating
```sql
-- ORDER BY AVG(rating) DESC, title ASC
-- Alphabetically smallest title is selected
```

## Alternative Approaches Comparison

### Approach 1: Using CTEs
```sql
WITH user_ratings AS (
    SELECT u.name, COUNT(*) as rating_count
    FROM MovieRating mr
    JOIN Users u ON mr.user_id = u.user_id
    GROUP BY u.name
),
movie_avg AS (
    SELECT m.title, AVG(mr.rating) as avg_rating
    FROM MovieRating mr
    JOIN Movies m ON mr.movie_id = m.movie_id
    WHERE mr.created_at >= '2020-02-01' AND mr.created_at < '2020-03-01'
    GROUP BY m.title
)
SELECT name as results FROM user_ratings 
ORDER BY rating_count DESC, name ASC LIMIT 1
UNION ALL
SELECT title as results FROM movie_avg 
ORDER BY avg_rating DESC, title ASC LIMIT 1;
```

**Advantages:**
- Higher readability
- Easier debugging

**Disadvantages:**
- More complex syntax
- Potential performance degradation in some SQL engines

### Approach 2: Using Subqueries
```sql
SELECT results FROM (
    SELECT u.name as results, COUNT(*) as cnt, 1 as order_col
    FROM MovieRating mr JOIN Users u ON mr.user_id = u.user_id
    GROUP BY u.name
    ORDER BY cnt DESC, u.name ASC LIMIT 1
) t1
UNION ALL
SELECT results FROM (
    SELECT m.title as results, AVG(mr.rating) as avg_rating, 2 as order_col
    FROM MovieRating mr JOIN Movies m ON mr.movie_id = m.movie_id
    WHERE mr.created_at >= '2020-02-01' AND mr.created_at < '2020-03-01'
    GROUP BY m.title
    ORDER BY avg_rating DESC, m.title ASC LIMIT 1
) t2;
```

### Current Solution Advantages
```sql
(SELECT u.name AS results FROM ...)
UNION ALL
(SELECT m.title AS results FROM ...)
```

**Advantages:**
- ✅ **Conciseness**: Direct approach
- ✅ **Efficiency**: No unnecessary intermediate table creation
- ✅ **Readability**: Two independent queries are clear
- ✅ **Maintainability**: Easy to modify and understand

## Key SQL Concepts Demonstrated

### 1. Aggregate Functions (COUNT, AVG)
```sql
COUNT(*) -- Row count
COUNT(column) -- Non-NULL value count
AVG(column) -- Average calculation
```

### 2. Grouping and Ordering
```sql
GROUP BY column -- Aggregation by group
ORDER BY expr1 DESC, expr2 ASC -- Multi-condition sorting
```

### 3. Date Range Filtering
```sql
WHERE date_column >= 'start' AND date_column < 'end'
WHERE date_column BETWEEN 'start' AND 'end'
```

### 4. JOIN Types
```sql
JOIN (INNER JOIN) -- Only matching records from both tables
LEFT JOIN -- All from left table + matching from right table
```

## Practical Debugging Methods

### Step 1: Verify Part 1 Intermediate Results
```sql
SELECT u.name, COUNT(*) as rating_count
FROM MovieRating AS mr
LEFT JOIN Users AS u ON mr.user_id = u.user_id
GROUP BY u.name
ORDER BY COUNT(*) DESC, u.name ASC;
```

### Step 2: Verify Part 2 Intermediate Results
```sql
SELECT m.title, AVG(mr.rating) as avg_rating, COUNT(*) as review_count
FROM MovieRating AS mr
LEFT JOIN Movies AS m ON mr.movie_id = m.movie_id
WHERE mr.created_at >= '2020-02-01' AND mr.created_at < '2020-03-01'
GROUP BY m.title
ORDER BY AVG(mr.rating) DESC, m.title ASC;
```

### Step 3: Verify Date Filter
```sql
SELECT *, 
    CASE 
        WHEN created_at >= '2020-02-01' AND created_at < '2020-03-01' 
        THEN 'Feb 2020' 
        ELSE 'Other' 
    END as period
FROM MovieRating
ORDER BY created_at;
```

### Step 4: Debug GROUP BY and COUNT(*) Relationship
```sql
-- Show detailed breakdown of what COUNT(*) counts for each user
SELECT 
    u.name,
    mr.movie_id,
    mr.rating,
    mr.created_at,
    COUNT(*) OVER (PARTITION BY u.name) as total_ratings_by_user
FROM MovieRating AS mr
LEFT JOIN Users AS u ON mr.user_id = u.user_id
ORDER BY u.name, mr.movie_id;
```

## Performance Optimization Tips

### Recommended Indexes
```sql
-- Recommended indexes
CREATE INDEX idx_movierating_userid ON MovieRating(user_id);
CREATE INDEX idx_movierating_movieid ON MovieRating(movie_id);
CREATE INDEX idx_movierating_created_at ON MovieRating(created_at);

-- Composite index (for Part 2)
CREATE INDEX idx_movierating_date_movie ON MovieRating(created_at, movie_id);
```

### Query Execution Plan Check
```sql
EXPLAIN SELECT ... -- Display execution plan
EXPLAIN ANALYZE SELECT ... -- Show actual execution statistics
```

## Real-World Applications

1. **Customer Analysis**: Identifying most active customers
2. **Product Rating**: Period-based top-rated product analysis
3. **Content Analysis**: User engagement measurement
4. **Recommendation Systems**: Recommendation based on rating patterns
5. **Quality Management**: Product/service rating trend analysis

This solution demonstrates an efficient approach to handling multiple analytical requirements and practical SQL patterns for tie-breaking (handling ties) in real-world scenarios.