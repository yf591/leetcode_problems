# 185. Department Top Three Salaries - SQL Solution Explanation

## Problem Overview
Find **employees with top 3 salaries** in each department.
- **Top 3 unique salaries**: Employees with same salary get same rank
- **Department-wise ranking**: Calculate ranking within each department
- **Result**: Return department name, employee name, and salary

## Input Data Understanding

### Original Data
```sql
Employee table:
+----+-------+--------+--------------+
| id | name  | salary | departmentId |
+----+-------+--------+--------------+
| 1  | Joe   | 85000  | 1            |
| 2  | Henry | 80000  | 2            |
| 3  | Sam   | 60000  | 2            |
| 4  | Max   | 90000  | 1            |
| 5  | Janet | 69000  | 1            |
| 6  | Randy | 85000  | 1            |
| 7  | Will  | 70000  | 1            |
+----+-------+--------+--------------+

Department table:
+----+-------+
| id | name  |
+----+-------+
| 1  | IT    |
| 2  | Sales |
+----+-------+
```

### Department-wise Salary Analysis
```
IT Department (departmentId=1):
- Max: 90000 (1st unique salary)
- Joe, Randy: 85000 (2nd unique salary, 2 employees with same salary)
- Will: 70000 (3rd unique salary)
- Janet: 69000 (4th unique salary) ← Excluded from top 3

Sales Department (departmentId=2):
- Henry: 80000 (1st unique salary)
- Sam: 60000 (2nd unique salary)
- No 3rd salary (only 2 employees)
```

## Key Concept: Understanding DENSE_RANK()

### Common Misconception
❌ **Incorrect syntax**: `DENSE_RANK(salary)` - This doesn't exist!

### Correct Understanding
✅ **Correct syntax**: 
```sql
DENSE_RANK() OVER (PARTITION BY departmentID ORDER BY salary DESC)
```

#### Important Points:
1. **`DENSE_RANK()` takes no arguments**: Ranking is based on `ORDER BY` clause
2. **`OVER` clause is mandatory**: Functions as window function
3. **`ORDER BY salary DESC`**: This part specifies ranking by salary

### Ranking Functions Comparison

```sql
-- Example data (IT Department)
Max: 90000    ← 1st place
Joe: 85000    ← 2nd place (tied)
Randy: 85000  ← 2nd place (tied)
Will: 70000   ← 3rd place
Janet: 69000  ← 4th place
```

#### **DENSE_RANK() Operation:**
```sql
DENSE_RANK() OVER (ORDER BY salary DESC):
Max: 90000    → DENSE_RANK = 1
Joe: 85000    → DENSE_RANK = 2
Randy: 85000  → DENSE_RANK = 2 (same salary, same rank)
Will: 70000   → DENSE_RANK = 3 (next rank is 3)
Janet: 69000  → DENSE_RANK = 4
```

#### **Comparison with Other Ranking Functions:**
```sql
-- ROW_NUMBER(): Always consecutive numbers
Max: 90000    → ROW_NUMBER = 1
Joe: 85000    → ROW_NUMBER = 2
Randy: 85000  → ROW_NUMBER = 3 (different number despite same salary)
Will: 70000   → ROW_NUMBER = 4
Janet: 69000  → ROW_NUMBER = 5

-- RANK(): Same values get same rank, but skips next rank
Max: 90000    → RANK = 1
Joe: 85000    → RANK = 2
Randy: 85000  → RANK = 2 (same rank)
Will: 70000   → RANK = 4 (skips 3, goes to 4)
Janet: 69000  → RANK = 5
```

### **Why DENSE_RANK() is Optimal?**
```sql
-- This problem requires "top 3 unique salaries"
-- DENSE_RANK() ensures same salaries get same rank,
-- and next rank is consecutive

DENSE_RANK() ≤ 3 retrieves:
Rank 1: Max (90000)
Rank 2: Joe, Randy (85000) ← Both included
Rank 3: Will (70000)

If using RANK():
Rank 1: Max (90000)
Rank 2: Joe, Randy (85000) ← Both included
Rank 4: Will (70000) ← No Rank 3, Will might be excluded
```

## Step-by-Step Solution Analysis

### Step 1: CTE with Ranking Calculation

```sql
WITH DepartmentRank AS (
    SELECT
        name,
        salary,
        departmentID,
        DENSE_RANK() OVER (PARTITION BY departmentID ORDER BY salary DESC) AS salary_rank
    FROM
        Employee
)
```

#### **PARTITION BY departmentID Operation:**
```sql
-- Data grouped by department
IT Department (departmentID=1):
+-------+--------+--------------+
| name  | salary | departmentID |
+-------+--------+--------------+
| Max   | 90000  | 1            |
| Joe   | 85000  | 1            |
| Randy | 85000  | 1            |
| Will  | 70000  | 1            |
| Janet | 69000  | 1            |
+-------+--------+--------------+

Sales Department (departmentID=2):
+-------+--------+--------------+
| name  | salary | departmentID |
+-------+--------+--------------+
| Henry | 80000  | 2            |
| Sam   | 60000  | 2            |
+-------+--------+--------------+
```

#### **ORDER BY salary DESC Operation:**
Sort by salary in descending order within each department and calculate ranking

#### **DepartmentRank CTE Result:**
```sql
+-------+--------+--------------+-------------+
| name  | salary | departmentID | salary_rank |
+-------+--------+--------------+-------------+
| Max   | 90000  | 1            | 1           |
| Joe   | 85000  | 1            | 2           |
| Randy | 85000  | 1            | 2           |
| Will  | 70000  | 1            | 3           |
| Janet | 69000  | 1            | 4           |
| Henry | 80000  | 2            | 1           |
| Sam   | 60000  | 2            | 2           |
+-------+--------+--------------+-------------+
```

### Step 2: JOIN with Department Information

```sql
SELECT
    d.name AS Department,
    dr.name AS Employee,
    dr.salary AS Salary
FROM
    DepartmentRank AS dr
LEFT JOIN
    Department AS d ON dr.departmentID = d.id
WHERE
    salary_rank <= 3;
```

## Understanding LEFT JOIN vs JOIN

### **Conclusion: Same result for this problem**

#### **Detailed Analysis:**

**Data Relationship:**
```sql
-- Employee.departmentId is foreign key to Department.id
-- Problem constraints ensure all employees belong to valid departments

Employee.departmentId → Department.id (foreign key constraint)
```

**Actual Data Verification:**
```sql
Employee table departmentId: [1, 2, 1, 1, 1, 1, 2]
Department table id: [1, 2]

→ All departmentId values exist in Department.id
```

#### **JOIN vs LEFT JOIN Result Comparison:**

**LEFT JOIN Operation:**
```sql
-- Preserves all rows from DepartmentRank
-- Joins with Department if match exists, otherwise NULL
-- In this problem, all match, so effectively same as INNER JOIN
```

**JOIN (INNER JOIN) Operation:**
```sql
-- Returns only rows where DepartmentRank and Department match
-- In this problem, all match, so same result as LEFT JOIN
```

#### **Which Should You Use?**

**LEFT JOIN is Recommended:**
```sql
# ✅ Data integrity consideration: Won't lose employee data even if department data is inconsistent
# ✅ Defensive programming: Handles future data changes
# ✅ Clear intent: Shows "employee data is primary"
```

**Practical Example:**
```sql
-- If Department table missing id=3
Employee with departmentId=3 exists:

LEFT JOIN: Employee included in result (Department=NULL)
INNER JOIN: Employee excluded from result
```

### Step 3: Conditional Filtering

```sql
WHERE salary_rank <= 3;
```

#### **Filtering Result:**
```sql
-- Only rows with salary_rank <= 3
+-------+--------+--------------+-------------+
| name  | salary | departmentID | salary_rank |
+-------+--------+--------------+-------------+
| Max   | 90000  | 1            | 1           | ✅
| Joe   | 85000  | 1            | 2           | ✅
| Randy | 85000  | 1            | 2           | ✅
| Will  | 70000  | 1            | 3           | ✅
| Janet | 69000  | 1            | 4           | ❌ Excluded
| Henry | 80000  | 2            | 1           | ✅
| Sam   | 60000  | 2            | 2           | ✅
+-------+--------+--------------+-------------+
```

## Final Result

### Final Output After JOIN:
```sql
+------------+----------+--------+
| Department | Employee | Salary |
+------------+----------+--------+
| IT         | Max      | 90000  |
| IT         | Joe      | 85000  |
| IT         | Randy    | 85000  |
| IT         | Will     | 70000  |
| Sales      | Henry    | 80000  |
| Sales      | Sam      | 60000  |
+------------+----------+--------+
```

## Alternative Approaches Comparison

### Approach 1: Subquery Method
```sql
SELECT 
    d.name AS Department,
    e.name AS Employee,
    e.salary AS Salary
FROM Employee e
JOIN Department d ON e.departmentId = d.id
WHERE (
    SELECT COUNT(DISTINCT e2.salary)
    FROM Employee e2
    WHERE e2.departmentId = e.departmentId 
    AND e2.salary >= e.salary
) <= 3;
```

### Approach 2: Correlated Subquery
```sql
SELECT 
    d.name AS Department,
    e.name AS Employee,
    e.salary AS Salary
FROM Employee e
JOIN Department d ON e.departmentId = d.id
WHERE 3 >= (
    SELECT COUNT(DISTINCT e2.salary)
    FROM Employee e2
    WHERE e2.departmentId = e.departmentId 
    AND e2.salary > e.salary
);
```

### Current Solution (Window Functions) Advantages
```sql
# ✅ Readability: Clear logic separation with CTE
# ✅ Performance: Single table scan completion
# ✅ Maintainability: Easy to modify ranking logic
# ✅ Extensibility: Simple to add other ranking conditions
```

## Debugging and Validation Methods

### Step-by-Step Execution Check
```sql
-- Step 1: Verify ranking calculation
SELECT
    name,
    salary,
    departmentID,
    DENSE_RANK() OVER (PARTITION BY departmentID ORDER BY salary DESC) AS salary_rank
FROM Employee
ORDER BY departmentID, salary_rank;

-- Step 2: Verify JOIN before filtering
WITH DepartmentRank AS (
    SELECT
        name,
        salary,
        departmentID,
        DENSE_RANK() OVER (PARTITION BY departmentID ORDER BY salary DESC) AS salary_rank
    FROM Employee
)
SELECT
    d.name AS Department,
    dr.name AS Employee,
    dr.salary AS Salary,
    dr.salary_rank
FROM DepartmentRank dr
LEFT JOIN Department d ON dr.departmentID = d.id
ORDER BY d.name, dr.salary_rank;
```

## Performance Considerations

### Index Optimization
```sql
-- For department-wise partitioning
CREATE INDEX idx_employee_dept_salary ON Employee(departmentId, salary DESC);

-- For JOIN performance improvement
CREATE INDEX idx_department_id ON Department(id);
```

### Large Dataset Optimization
```sql
-- Composite index for comprehensive optimization
CREATE INDEX idx_employee_comprehensive ON Employee(departmentId, salary DESC, name);
```

## Real-World Applications

1. **HR Analytics**: Identify high earners by department
2. **Promotion Candidate Selection**: Identify top performers
3. **Salary Adjustment**: Understand market-competitive employees
4. **Budget Planning**: Cost analysis of high-earning employees
5. **Organizational Analysis**: Evaluate salary disparities between departments

## Key Takeaways

1. **DENSE_RANK() syntax**: `DENSE_RANK() OVER (...)` with no arguments
2. **Ranking criteria**: Specified in `ORDER BY` clause of OVER
3. **PARTITION BY**: Enables department-wise ranking calculation
4. **LEFT JOIN benefits**: Data integrity and defensive programming
5. **Window Functions**: Provide efficient solutions for ranking problems

This solution demonstrates an exemplary use of Window Functions for ranking problems, showcasing how to efficiently identify records meeting complex multi-criteria requirements within groups.

## Answer to Several Questions

### **Question 1: Why not `DENSE_RANK(salary)` but `DENSE_RANK()`?**
- **Reason**: `DENSE_RANK()` function takes no arguments
- **Ranking criteria**: Specified in `ORDER BY salary DESC` within OVER clause
- **Correct syntax**: `DENSE_RANK() OVER (PARTITION BY ... ORDER BY ...)`
- **Key insight**: The OVER clause defines the window and sorting for ranking

### **Question 2: LEFT JOIN vs JOIN - Same result?**
- **Answer**: Yes, same result for this problem
- **Reason**: All employees have valid department references
- **Recommendation**: LEFT JOIN is better practice for data integrity
- **Defensive approach**: Handles potential future data inconsistencies
