# 585. Investments in 2016 - SQL Solution Explanation

## Problem Overview
Calculate the **sum of 2016 investment values** for policyholders meeting specific criteria from an insurance table.

**Target Policyholder Criteria:**
1. **Shared tiv_2015 value**: Have the same 2015 investment value as other policyholders
2. **Unique location**: Not located in the same city as any other policyholder (unique lat, lon combination)

## Input Data Understanding

### Original Data
```sql
Insurance table:
+-----+----------+----------+-----+-----+
| pid | tiv_2015 | tiv_2016 | lat | lon |
+-----+----------+----------+-----+-----+
| 1   | 10       | 5        | 10  | 10  |
| 2   | 20       | 20       | 20  | 20  |
| 3   | 10       | 30       | 20  | 20  |
| 4   | 10       | 40       | 40  | 40  |
+-----+----------+----------+-----+-----+
```

### Criteria Analysis
```
pid 1: tiv_2015=10 (shared by 3 people), location(10,10) (unique) → ✅ Meets criteria
pid 2: tiv_2015=20 (only 1 person), location(20,20) (shared with pid 3) → ❌ Fails both
pid 3: tiv_2015=10 (shared by 3 people), location(20,20) (shared with pid 2) → ❌ Location conflict
pid 4: tiv_2015=10 (shared by 3 people), location(40,40) (unique) → ✅ Meets criteria

Result: pid 1 + pid 4 = 5 + 40 = 45
```

## Step-by-Step Solution Breakdown

### Step 1: CTE with Window Functions

```sql
WITH PolicyCounts AS (
    SELECT
        tiv_2016,
        COUNT(*) OVER (PARTITION BY tiv_2015) AS count_2015,
        COUNT(*) OVER (PARTITION BY lat, lon) AS loc_count
    FROM
        Insurance
)
```

#### Window Function Operations

**PARTITION BY tiv_2015:**
```sql
-- Group by tiv_2015 and count occurrences
pid 1: tiv_2015=10 → Group{1,3,4} → COUNT(*) = 3
pid 2: tiv_2015=20 → Group{2}     → COUNT(*) = 1  
pid 3: tiv_2015=10 → Group{1,3,4} → COUNT(*) = 3
pid 4: tiv_2015=10 → Group{1,3,4} → COUNT(*) = 3
```

**PARTITION BY lat, lon:**
```sql
-- Group by location and count occurrences
pid 1: (10,10) → Group{1}   → COUNT(*) = 1
pid 2: (20,20) → Group{2,3} → COUNT(*) = 2
pid 3: (20,20) → Group{2,3} → COUNT(*) = 2
pid 4: (40,40) → Group{4}   → COUNT(*) = 1
```

### Step 2: PolicyCounts Table Result

```sql
PolicyCounts:
+----------+------------+-----------+
| tiv_2016 | count_2015 | loc_count |
+----------+------------+-----------+
| 5        | 3          | 1         |
| 20       | 1          | 2         |
| 30       | 3          | 2         |
| 40       | 3          | 1         |
+----------+------------+-----------+
```

#### Detailed Row Analysis

**Row 1 (tiv_2016=5):**
- `count_2015=3`: 3 people have tiv_2015=10 (pid 1,3,4)
- `loc_count=1`: Only 1 person at location (10,10) (unique)
- **Criteria**: ✅ count_2015>1 AND loc_count=1

**Row 2 (tiv_2016=20):**
- `count_2015=1`: Only 1 person has tiv_2015=20 (pid 2)
- `loc_count=2`: 2 people at location (20,20) (pid 2,3)
- **Criteria**: ❌ count_2015=1 (fails first condition)

**Row 3 (tiv_2016=30):**
- `count_2015=3`: 3 people have tiv_2015=10 (pid 1,3,4)
- `loc_count=2`: 2 people at location (20,20) (pid 2,3)
- **Criteria**: ❌ loc_count=2 (location conflict)

**Row 4 (tiv_2016=40):**
- `count_2015=3`: 3 people have tiv_2015=10 (pid 1,3,4)
- `loc_count=1`: Only 1 person at location (40,40) (unique)
- **Criteria**: ✅ count_2015>1 AND loc_count=1

### Step 3: Conditional Filtering

```sql
SELECT
    ROUND(SUM(tiv_2016), 2) AS tiv_2016
FROM
    PolicyCounts
WHERE
    count_2015 > 1 AND loc_count = 1;
```

#### WHERE Condition Details

**count_2015 > 1**: Shares tiv_2015 value with other policyholders
```sql
pid 1: count_2015=3 > 1 → ✅ True
pid 2: count_2015=1 > 1 → ❌ False (excluded)
pid 3: count_2015=3 > 1 → ✅ True  
pid 4: count_2015=3 > 1 → ✅ True
```

**loc_count = 1**: Unique location (no duplicates)
```sql
pid 1: loc_count=1 = 1 → ✅ True
pid 2: loc_count=2 = 1 → ❌ False (excluded)
pid 3: loc_count=2 = 1 → ❌ False (excluded)
pid 4: loc_count=1 = 1 → ✅ True
```

#### AND Condition Results
```sql
pid 1: True  AND True  → ✅ Meets criteria (tiv_2016=5)
pid 2: False AND False → ❌ Excluded
pid 3: True  AND False → ❌ Excluded  
pid 4: True  AND True  → ✅ Meets criteria (tiv_2016=40)
```

## Final Calculation

### SUM(tiv_2016) Computation
```sql
SUM(tiv_2016) = 5 + 40 = 45
ROUND(45, 2) = 45.00
```

### Final Result
```sql
+----------+
| tiv_2016 |
+----------+
| 45.00    |
+----------+
```

## Window Functions Deep Dive

### PARTITION BY Mechanism

#### Partitioning by tiv_2015
```sql
Data grouped by tiv_2015 value:
Group 1 (tiv_2015=10): {pid 1, pid 3, pid 4} → COUNT(*) = 3
Group 2 (tiv_2015=20): {pid 2}               → COUNT(*) = 1

Count assigned to each row in the group:
pid 1 → count_2015 = 3
pid 3 → count_2015 = 3  
pid 4 → count_2015 = 3
pid 2 → count_2015 = 1
```

#### Partitioning by (lat, lon)
```sql
Data grouped by location:
Group 1 (10,10): {pid 1}       → COUNT(*) = 1
Group 2 (20,20): {pid 2, pid 3} → COUNT(*) = 2
Group 3 (40,40): {pid 4}       → COUNT(*) = 1

Count assigned to each row in the group:
pid 1 → loc_count = 1
pid 2 → loc_count = 2
pid 3 → loc_count = 2  
pid 4 → loc_count = 1
```

## Alternative Approaches Comparison

### Approach 1: Subquery Method
```sql
SELECT 
    ROUND(SUM(tiv_2016), 2) AS tiv_2016
FROM Insurance i1
WHERE 
    -- Condition 1: Shared tiv_2015 with other policyholders
    (SELECT COUNT(*) FROM Insurance i2 WHERE i2.tiv_2015 = i1.tiv_2015) > 1
    AND
    -- Condition 2: Unique location
    (SELECT COUNT(*) FROM Insurance i3 WHERE i3.lat = i1.lat AND i3.lon = i1.lon) = 1;
```

### Approach 2: EXISTS Method
```sql
SELECT 
    ROUND(SUM(tiv_2016), 2) AS tiv_2016
FROM Insurance i1
WHERE 
    -- Condition 1: Other policyholders with same tiv_2015 exist
    EXISTS (SELECT 1 FROM Insurance i2 WHERE i2.tiv_2015 = i1.tiv_2015 AND i2.pid != i1.pid)
    AND
    -- Condition 2: No other policyholders at same location
    NOT EXISTS (SELECT 1 FROM Insurance i3 WHERE i3.lat = i1.lat AND i3.lon = i1.lon AND i3.pid != i1.pid);
```

### Current Solution (Window Functions) Advantages
```sql
# ✅ Efficient: Single table scan
# ✅ Readable: Clear logic separation with CTE
# ✅ Performance: Avoids repeated subquery execution
# ✅ Scalable: Easy to add additional aggregation conditions
```

## Debugging and Validation

### Step-by-Step Execution Check
```sql
-- Step 1: Verify Window Function results
SELECT 
    pid,
    tiv_2015,
    tiv_2016,
    lat,
    lon,
    COUNT(*) OVER (PARTITION BY tiv_2015) AS count_2015,
    COUNT(*) OVER (PARTITION BY lat, lon) AS loc_count
FROM Insurance;

-- Expected result:
-- +-----+----------+----------+-----+-----+------------+-----------+
-- | pid | tiv_2015 | tiv_2016 | lat | lon | count_2015 | loc_count |
-- +-----+----------+----------+-----+-----+------------+-----------+
-- | 1   | 10       | 5        | 10  | 10  | 3          | 1         |
-- | 2   | 20       | 20       | 20  | 20  | 1          | 2         |
-- | 3   | 10       | 30       | 20  | 20  | 3          | 2         |
-- | 4   | 10       | 40       | 40  | 40  | 3          | 1         |
-- +-----+----------+----------+-----+-----+------------+-----------+
```

```sql
-- Step 2: Verify filter conditions
WITH PolicyCounts AS (
    SELECT
        pid,
        tiv_2016,
        COUNT(*) OVER (PARTITION BY tiv_2015) AS count_2015,
        COUNT(*) OVER (PARTITION BY lat, lon) AS loc_count
    FROM Insurance
)
SELECT 
    pid,
    tiv_2016,
    count_2015,
    loc_count,
    CASE WHEN count_2015 > 1 AND loc_count = 1 THEN 'INCLUDED' ELSE 'EXCLUDED' END AS status
FROM PolicyCounts;

-- Expected result:
-- +-----+----------+------------+-----------+----------+
-- | pid | tiv_2016 | count_2015 | loc_count | status   |
-- +-----+----------+------------+-----------+----------+
-- | 1   | 5        | 3          | 1         | INCLUDED |
-- | 2   | 20       | 1          | 2         | EXCLUDED |
-- | 3   | 30       | 3          | 2         | EXCLUDED |
-- | 4   | 40       | 3          | 1         | INCLUDED |
-- +-----+----------+------------+-----------+----------+
```

## Performance Considerations

### Index Optimization
```sql
-- Speed up grouping by tiv_2015
CREATE INDEX idx_tiv_2015 ON Insurance(tiv_2015);

-- Speed up location grouping
CREATE INDEX idx_location ON Insurance(lat, lon);
```

### Large Dataset Optimization
```sql
-- Composite index for further optimization
CREATE INDEX idx_composite ON Insurance(tiv_2015, lat, lon, tiv_2016);
```

## Real-World Applications

1. **Insurance Risk Analysis**: Identify policyholders with similar investment amounts but geographic diversification
2. **Fraud Detection**: Discover unusual investment patterns
3. **Regional Analysis**: Customer segmentation with geographic uniqueness
4. **Investment Strategy**: Portfolio geographic diversification assessment
5. **Regulatory Compliance**: Insurance industry concentration risk management

## Key Takeaways

1. **Window Functions** provide efficient solutions for conditional aggregation
2. **PARTITION BY** enables grouping without traditional GROUP BY limitations
3. **CTE structure** improves query readability and maintainability
4. **Multiple conditions** can be elegantly handled with window function results
5. **Performance optimization** through proper indexing is crucial for large datasets

This problem demonstrates an excellent use case for Window Functions in conditional aggregation scenarios, showcasing how to efficiently identify records meeting complex multi-criteria requirements.
