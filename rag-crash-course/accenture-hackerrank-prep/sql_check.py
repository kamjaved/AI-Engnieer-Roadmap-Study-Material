from __future__ import annotations

import sqlite3

import pandas as pd

SCHEMA = """
CREATE TABLE departments (dept_id INTEGER PRIMARY KEY, dept_name TEXT);
CREATE TABLE employees (
  emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, manager_id INTEGER,
  salary INTEGER, hire_date TEXT);
CREATE TABLE orders (order_id INTEGER PRIMARY KEY, emp_id INTEGER, amount INTEGER, order_date TEXT);
INSERT INTO departments VALUES (1,'Engineering'),(2,'Sales'),(3,'HR'),(4,'Legal');
INSERT INTO employees VALUES
 (1,'Asha',1,NULL,200000,'2019-01-10'),
 (2,'Ravi',1,1,150000,'2020-03-01'),
 (3,'Meera',1,1,150000,'2021-07-15'),
 (4,'Karan',1,2,160000,'2022-02-01'),
 (5,'Neha',2,1,90000,'2020-05-20'),
 (6,'Vikram',2,5,95000,'2023-01-05'),
 (7,'Pooja',3,1,70000,'2021-11-11'),
 (8,'Ravi',1,1,150000,'2020-03-01');
INSERT INTO orders VALUES
 (1,5,1000,'2026-01-05'),(2,5,1500,'2026-01-20'),(3,6,700,'2026-01-25'),
 (4,6,1200,'2026-02-02'),(5,5,300,'2026-02-10');
"""

QUERIES = {
    "Q1 second highest distinct salary": """
        SELECT MAX(salary) AS second_highest FROM employees
        WHERE salary < (SELECT MAX(salary) FROM employees);""",
    "Q1b nth highest with DENSE_RANK (n=2)": """
        SELECT DISTINCT salary FROM (
          SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk FROM employees)
        WHERE rnk = 2;""",
    "Q2 top 2 earners per dept (DENSE_RANK)": """
        SELECT dept_name, name, salary FROM (
          SELECT d.dept_name, e.name, e.salary,
                 DENSE_RANK() OVER (PARTITION BY e.dept_id ORDER BY e.salary DESC) AS rnk
          FROM employees e JOIN departments d ON d.dept_id = e.dept_id)
        WHERE rnk <= 2 ORDER BY dept_name, salary DESC, name;""",
    "Q3 earn more than manager (self join)": """
        SELECT e.name AS employee, m.name AS manager
        FROM employees e JOIN employees m ON e.manager_id = m.emp_id
        WHERE e.salary > m.salary;""",
    "Q4 depts with avg salary > 100000 (HAVING)": """
        SELECT d.dept_name, ROUND(AVG(e.salary)) AS avg_salary, COUNT(*) AS headcount
        FROM employees e JOIN departments d ON d.dept_id = e.dept_id
        GROUP BY d.dept_name HAVING AVG(e.salary) > 100000;""",
    "Q5 departments with no employees (LEFT JOIN / anti-join)": """
        SELECT d.dept_name FROM departments d
        LEFT JOIN employees e ON e.dept_id = d.dept_id
        WHERE e.emp_id IS NULL;""",
    "Q6 running total of order amount per employee": """
        SELECT emp_id, order_date, amount,
               SUM(amount) OVER (PARTITION BY emp_id ORDER BY order_date
                                 ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
        FROM orders ORDER BY emp_id, order_date;""",
    "Q7 duplicate rows (same name, dept, salary, hire_date)": """
        SELECT name, dept_id, salary, hire_date, COUNT(*) AS cnt
        FROM employees GROUP BY name, dept_id, salary, hire_date HAVING COUNT(*) > 1;""",
    "Q8 monthly sales + month-over-month change (LAG)": """
        SELECT month, total, total - LAG(total) OVER (ORDER BY month) AS mom_change FROM (
          SELECT strftime('%Y-%m', order_date) AS month, SUM(amount) AS total
          FROM orders GROUP BY month);""",
    "Q9 RANK vs DENSE_RANK vs ROW_NUMBER in Engineering": """
        SELECT name, salary,
               ROW_NUMBER() OVER (ORDER BY salary DESC) AS rn,
               RANK()       OVER (ORDER BY salary DESC) AS rnk,
               DENSE_RANK() OVER (ORDER BY salary DESC) AS drnk
        FROM employees WHERE dept_id = 1 ORDER BY salary DESC, emp_id;""",
}

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
for title, q in QUERIES.items():
    print(f"--- {title}")
    print(pd.read_sql_query(q, con).to_string(index=False))

# pandas equivalents
emp = pd.read_sql_query("SELECT * FROM employees", con)
dept = pd.read_sql_query("SELECT * FROM departments", con)
df = emp.merge(dept, on="dept_id", how="left")
print("--- P1 avg salary & headcount per dept")
print(df.groupby("dept_name", as_index=False).agg(avg_salary=("salary", "mean"), headcount=("emp_id", "count")).to_string(index=False))
print("--- P2 top 2 per dept")
df["rnk"] = df.groupby("dept_id")["salary"].rank(method="dense", ascending=False)
print(df.loc[df["rnk"] <= 2, ["dept_name", "name", "salary"]].sort_values(["dept_name", "salary", "name"], ascending=[True, False, True]).to_string(index=False))
print("--- P3 drop duplicates")
print(len(emp), "->", len(emp.drop_duplicates(subset=["name", "dept_id", "salary", "hire_date"])))
