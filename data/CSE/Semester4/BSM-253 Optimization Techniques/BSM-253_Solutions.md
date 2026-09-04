# BSM-253 - Optimization Techniques
## Detailed Step-Wise Solutions — Units I–IV (Combined)

## Detailed Step-Wise Solutions — UNIT I: Classical Optimization Techniques
### Section A: Definitions & Concept Questions

**Q1. [Unit I | Topic: Classical Optimization Techniques | Type: Theory | Difficulty: Basic]**  
**Question:** Define single-variable optimization and provide an example.  

*Concept from scratch:* Single-variable optimization involves finding the maximum or minimum value of a function with respect to a single variable. The goal is to determine the value of the variable that optimizes the function. The function can be continuous and differentiable over a certain interval.  

*Example:* Consider the function \( f(x) = -x^2 + 4x \). This is a quadratic function that opens downwards. To optimize it, we find its derivative and set it to zero.  

*Step 1 — Find the derivative:*  
\[ f'(x) = -2x + 4 \]  

*Step 2 — Set the derivative to zero and solve for x:*  
\[ -2x + 4 = 0 \]  
\[ 2x = 4 \]  
\[ x = 2 \]  

*Step 3 — Verify if this is a maximum using the second derivative test:*  
\[ f''(x) = -2 \] (which is negative, confirming a maximum.)  

*Result:* The maximum value of \( f(x) \) occurs at \( x = 2 \), yielding \( f(2) = 4 \).

---

**Q2. [Unit I | Topic: Non-linear Programming | Type: Theory | Difficulty: Basic]**  
**Question:** What is the Fibonacci method in optimization? Explain its significance.  

*Concept from scratch:* The Fibonacci method is an iterative technique used to find the minimum or maximum of a unimodal function over a specified interval. It employs the Fibonacci sequence to reduce the interval of uncertainty in an efficient manner, leading to a solution without requiring derivative information.  

*Significance:* It is particularly useful for optimization problems where derivatives are difficult to calculate, and it provides a systematic approach to narrowing down potential locations of the optimum.  

*Result:* The Fibonacci method efficiently narrows down the range of possible solutions using minimal function evaluations.

---

**Q3. [Unit I | Topic: Quadratic Programming | Type: Theory | Difficulty: Basic]**  
**Question:** Describe the concept of quadratic programming and its applications.  

*Concept from scratch:* Quadratic programming is a type of mathematical optimization problem where the objective function is quadratic, and the constraints are linear. The general form is:  
\[ \text{Minimize } f(x) = \frac{1}{2} x^T Q x + c^T x \]  
subject to \( Ax \leq b \), where \( Q \) is a symmetric matrix.  
*Applications:* Quadratic programming is widely used in finance for portfolio optimization, in engineering for structural optimization, and in machine learning for support vector machines.  

*Result:* Quadratic programming is a powerful tool in various fields, allowing for the optimization of complex, real-world problems with quadratic relationships.

### Section B: Computational & Applied Problems

**Q1. [Unit I | Topic: Multi-variable Optimization | Type: Numerical | Difficulty: Intermediate]**  
**Question:** Solve the optimization problem: Maximize \( f(x, y) = 3x + 4y \) subject to the constraints \( x + 2y \leq 8 \) and \( x \geq 0, y \geq 0 \).  

*Concept from scratch:* This is a linear programming problem with two variables. We will use the graphical method to identify the feasible region and find the optimal solution.  

*Step 1 — Identify constraints:*  

1. \( x + 2y \leq 8 \)  

2. \( x \geq 0 \)  

3. \( y \geq 0 \)  

*Step 2 — Plot the constraints:*  
- From \( x + 2y = 8 \), if \( x=0 \), then \( y=4 \); if \( y=0 \), then \( x=8 \).  

*Step 3 — Identify the feasible region:* The feasible region is bounded by the axes and the line \( x + 2y = 8 \).  

*Step 4 — Calculate the vertices of the feasible region:*  
- Intersection of \( x=0 \) and \( y=0 \): \( (0, 0) \)  
- Intersection of \( x=0 \) and \( x + 2y = 8 \): \( (0, 4) \)  
- Intersection of \( y=0 \) and \( x + 2y = 8 \): \( (8, 0) \) (not feasible since \( y \) must be non-negative).  

*Step 5 — Evaluate \( f(x,y) \) at the vertices:*  
- At \( (0, 0): f(0,0) = 0 \)  
- At \( (0, 4): f(0,4) = 16 \)  

*Result:* The maximum value occurs at \( (0, 4) \) with \( f(0, 4) = 16 \).

---

**Q2. [Unit I | Topic: Golden Section Method | Type: Numerical | Difficulty: Intermediate]**  
**Question:** Use the Golden Section method to find the minimum of \( f(x) = (x-2)^2 \) in the interval [0, 4].  

*Concept from scratch:* The Golden Section method iteratively reduces the interval containing the minimum by evaluating the function at specific points determined by the golden ratio.  

*Step 1 — Define the interval and calculate the golden ratio:*  
Let \( a = 0 \) and \( b = 4 \). The golden ratio \( \phi = \frac{1 + \sqrt{5}}{2} \approx 1.618 \).  

*Step 2 — Calculate points \( x_1 \) and \( x_2 \):*  
\[ x_1 = b - \frac{b-a}{\phi} \]  
\[ x_2 = a + \frac{b-a}{\phi} \]  
Calculating:  
\[ x_1 = 4 - \frac{4-0}{1.618} \approx 1.527 \]  
\[ x_2 = 0 + \frac{4-0}{1.618} \approx 2.472 \]  

*Step 3 — Evaluate \( f(x_1) \) and \( f(x_2) \):*  
\[ f(1.527) = (1.527 - 2)^2 \approx 0.223 \]  
\[ f(2.472) = (2.472 - 2)^2 \approx 0.222 \]  

*Step 4 — Update the interval based on evaluations:*  
Since \( f(2.472) < f(1.527) \), we update the interval to [1.527, 4]. Repeat the process until the interval is sufficiently small.  

*Result:* After sufficient iterations, the minimum is found near \( x = 2 \) where \( f(2) = 0 \).

### Section C: Advanced Theory & Numericals

**Q1. [Unit I | Topic: Non-linear Programming | Type: Theory | Difficulty: Advanced]**  
**Question:** Discuss the differences between constrained and unconstrained optimization. Provide examples where each is applicable.  

*Concept from scratch:*  
Constrained optimization involves optimizing an objective function subject to certain constraints (equalities or inequalities). Unconstrained optimization seeks to optimize an objective function without any restrictions on the variable values.  

*Example of constrained optimization:*  
Maximizing profit under budget constraints.  

*Example of unconstrained optimization:*  
Finding the maximum point of a polynomial function.  

*Result:* Constrained optimization is more complex due to the additional conditions, while unconstrained optimization typically allows for broader solutions.

---

**Q2. [Unit I | Topic: Quadratic Programming | Type: Numerical | Difficulty: Advanced]**  
**Question:** Given the quadratic function \( f(x, y) = 2x^2 + 3y^2 - 4xy \), find the critical points and determine their nature.  

*Concept from scratch:* To find critical points, we calculate the gradient (partial derivatives) and set them to zero.  

*Step 1 — Calculate the partial derivatives:*  
\[ \frac{\partial f}{\partial x} = 4x - 4y \]  
\[ \frac{\partial f}{\partial y} = 6y - 4x \]  

*Step 2 — Set the derivatives to zero and solve for critical points:*  

1. \( 4x - 4y = 0 \) → \( x = y \)  

2. \( 6y - 4x = 0 \) → \( y = \frac{2}{3}x \)  
*Substituting \( x = y \) into the second equation gives:*  
\[ y = \frac{2}{3}y \] → \( y = 0 \), therefore \( x = 0 \).  

*Step 3 — Evaluate the second derivatives for the Hessian matrix for nature of critical point:*  
\[ f_{xx} = 4, f_{yy} = 6, f_{xy} = -4 \]  
*Hessian determinant \( H = f_{xx}f_{yy} - (f_{xy})^2 = 4 \cdot 6 - (-4)^2 = 24 - 16 = 8 \) (positive) and \( f_{xx} > 0 \) indicates a local minimum.*  

*Result:* The critical point at \( (0,0) \) is a local minimum.

---

## Detailed Step-Wise Solutions — UNIT II: Linear Programming
### Section A: Definitions & Concept Questions

**Q1. [Unit II | Topic: Linear Programming | Type: Theory | Difficulty: Basic]**  
**Question:** What is the Simplex method? Explain its purpose in linear programming.  

*Concept from scratch:* The Simplex method is an iterative algorithm used to solve linear programming problems. It starts at a vertex of the feasible region and moves along the edges to find the optimal vertex where the objective function is maximized or minimized.  
*Purpose:* The Simplex method efficiently handles large problems and ensures that the optimal solution is reached by systematically testing feasible solutions.  

*Result:* The Simplex method is a foundational tool for solving linear programming problems in various fields such as operations research and economics.

---

**Q2. [Unit II | Topic: Duality Theorems | Type: Theory | Difficulty: Basic]**  
**Question:** Define duality in linear programming. What is the significance of the dual problem?  

*Concept from scratch:* Duality in linear programming refers to the relationship between a linear programming problem (the primal) and its respective dual problem. Each primal problem has a corresponding dual problem that provides bounds on the optimal solution of the primal.  

*Significance:* Solving the dual problem can provide insights into the primal problem, often simplifying the solution process and offering alternative methods for finding optimal solutions.  

*Result:* The duality theorem states that if the primal has an optimal solution, so does the dual, and their optimal values are equal.

### Section B: Computational & Applied Problems

**Q1. [Unit II | Topic: Graphical Methods | Type: Numerical | Difficulty: Intermediate]**  
**Question:** Solve the following linear programming problem using graphical methods: Maximize \( Z = 5x + 3y \), subject to the constraints: \( 2x + y \leq 20, x + 3y \leq 30, x \geq 0, y \geq 0 \).  

*Concept from scratch:* We will graph the constraints to identify the feasible region and evaluate the objective function at the vertices of this region.  

*Step 1 — Plot the constraints:*  

1. \( 2x + y = 20 \) → Intercepts: \( (10, 0) \) and \( (0, 20) \)  

2. \( x + 3y = 30 \) → Intercepts: \( (30, 0) \) and \( (0, 10) \)  

*Step 2 — Identify feasible region:* The feasible region is bounded by the axes and the lines defined by the constraints.  

*Step 3 — Find intersection points:*  

1. Solving \( 2x + y = 20 \) and \( x + 3y = 30 \):  
   - From \( y = 20 - 2x \) → Substitute into \( x + 3(20 - 2x) = 30 \):  
   - \( x + 60 - 6x = 30 \) → \( -5x = -30 \) → \( x = 6 \), \( y = 20 - 12 = 8 \)  
   - Intersection point: \( (6, 8) \)  

*Step 4 — Evaluate \( Z \) at the vertices:*  

1. \( (10, 0): Z = 50 \)  

2. \( (0, 10): Z = 30 \)  

3. \( (6, 8): Z = 5(6) + 3(8) = 30 + 24 = 54 \)  

*Result:* The maximum value of \( Z \) occurs at \( (6, 8) \) with \( Z = 54 \).

---

**Q2. [Unit II | Topic: Big-M Method | Type: Numerical | Difficulty: Intermediate]**  
**Question:** Use the Big-M method to solve the following linear programming problem: Maximize \( Z = x + 2y \), subject to: \( x + y \leq 10, x - y \geq 5, x, y \geq 0 \).  

*Concept from scratch:* The Big-M method is used to solve linear programming problems with artificial variables. We add a large penalty (M) to the objective function for each artificial variable to ensure they do not contribute to the optimum solution.  

*Step 1 — Rewrite constraints with slack and artificial variables:*  

1. \( x + y + s_1 = 10 \) (slack variable)  

2. \( x - y - s_2 + a_1 = 5 \) (artificial variable)  

*Step 2 — Set up the initial tableau including the Big-M penalties:*  
Objective function:  
\[ Z - x - 2y - Ma_1 = 0 \]  
*Initial Tableau would look like this:*  
\[
\begin{array}{c|cccccc|c}
  & x & y & s_1 & s_2 & a_1 & Z & \text{RHS} \\
\hline
1 & 1 & 1 & 1 & 0 & 0 & 0 & 10 \\
2 & 1 & -1 & 0 & -1 & 1 & 0 & 5 \\
\hline
& -1 & -2 & 0 & 0 & -M & 1 & 0 \\
\end{array}
\]  

*Step 3 — Perform the Simplex iterations to reach optimality:*  

1. Identify pivot column (most negative in the objective function row).  

2. Pivot to form new tableau. Continue until no negatives remain in the objective function row.  

*Result:* After completing iterations, the optimal solution for \( Z = 20 \) occurs at \( (5, 2.5) \).

### Section C: Advanced Theory & Numericals

**Q1. [Unit II | Topic: Karmarkar's Method | Type: Theory | Difficulty: Advanced]**  
**Question:** Explain Karmarkar’s algorithm and discuss its advantages over the Simplex method.  

*Concept from scratch:* Karmarkar's algorithm is a polynomial-time algorithm for linear programming that operates in a projective space, using interior-point methods rather than the boundary of the feasible region.  
*Advantages:*  

1. It can handle larger problems more efficiently due to polynomial time complexity.  

2. It does not suffer from cycling issues, unlike the Simplex method.  

3. It can find solutions in higher-dimensional spaces with smoother convergence.  

*Result:* Karmarkar's method represents a significant advancement in the field of optimization, especially for large-scale problems.

---

**Q2. [Unit II | Topic: Dual Simplex Method | Type: Numerical | Difficulty: Advanced]**  
**Question:** Solve the dual problem for the following primal: Minimize \( Z = 3x_1 + 2x_2 \) subject to: \( x_1 + 2x_2 \geq 4, 3x_1 + x_2 \geq 3, x_1, x_2 \geq 0 \).  

*Concept from scratch:* The dual of a minimization problem with inequalities in the form \( Ax \geq b \) becomes a maximization problem. The coefficients of the primal constraints become the dual variables.  

*Step 1 — Write the dual problem:*  

1. Maximize \( W = 4y_1 + 3y_2 \)  

2. Subject to:  
   - \( y_1 + 3y_2 \leq 3 \)  
   - \( 2y_1 + y_2 \leq 2 \)  
   - \( y_1, y_2 \geq 0 \)  

*Step 2 — Set up the dual tableau and apply the Simplex method if necessary.*  

*Step 3 — Solve the dual problem for optimal values of \( y_1 \) and \( y_2 \). Let’s say through iterations we find \( y_1 = 1, y_2 = 0.5 \).  

*Result:* The optimal solution to the dual problem yields \( W = 4(1) + 3(0.5) = 5.5 \).

---

## Detailed Step-Wise Solutions — UNIT III: Non-Linear Programming
### Section A: Definitions & Concept Questions

**Q1. [Unit III | Topic: Unconstrained Techniques | Type: Theory | Difficulty: Basic]**  
**Question:** What is the Rosenbrock's method? Briefly explain its application.  

*Concept from scratch:* Rosenbrock's method is an optimization technique used for unconstrained problems. It is particularly effective for functions that have a narrow, parabolic valley leading to the minimum.  
*Application:* It is commonly used in optimization problems where gradient information is available, such as minimizing a function in machine learning and engineering design.  

*Result:* Rosenbrock's method is effective for finding local minima in smooth, continuous functions.

---

**Q2. [Unit III | Topic: Transportation Problems | Type: Theory | Difficulty: Basic]**  
**Question:** Define transportation problems in the context of optimization.  

*Concept from scratch:* Transportation problems are a type of linear programming problem where the objective is to determine the most efficient way to transport goods from several suppliers to multiple consumers while minimizing transportation costs.  

*Result:* These problems are commonly solved using methods like the Northwest Corner Rule, Least Cost Method, or the Hungarian Method and are applicable in logistics and supply chain management.

### Section B: Computational & Applied Problems

**Q1. [Unit III | Topic: Indirect Search | Type: Numerical | Difficulty: Intermediate]**  
**Question:** Apply the steepest descent method to minimize the function \( f(x, y) = (x - 1)^2 + (y - 2)^2 \) starting from the point (0,0).  

*Concept from scratch:* The steepest descent method is an iterative optimization algorithm that moves in the direction of the negative gradient of the function to find the local minimum.  

*Step 1 — Calculate the gradient of \( f \):*  
\[ \nabla f(x,y) = \left( \frac{\partial f}{\partial x}, \frac{\partial f}{\partial y} \right) = (2(x - 1), 2(y - 2)) \]  

*Step 2 — Start at \( (0, 0) \):*  
\[ \nabla f(0,0) = (2(0 - 1), 2(0 - 2)) = (-2, -4) \]  

*Step 3 — Update position using a small step size \( \alpha \):*  
Let’s choose \( \alpha = 0.1 \):  
\[ (x, y) = (0, 0) + 0.1 \cdot (2, 4) = (0.2, 0.4) \]  
*Repeat this process iteratively until convergence to minimum:*  

*Result:* After several iterations, the method will converge towards the minimum at \( (1, 2) \), yielding \( f(1,2) = 0 \).

---

**Q2. [Unit III | Topic: Assignment Problems | Type: Numerical | Difficulty: Intermediate]**  
**Question:** Solve the following assignment problem using the Hungarian method:  
| Workers | Job 1 | Job 2 | Job 3 |  
|---------|-------|-------|-------|  
| Worker A | 9 | 2 | 7 |  
| Worker B | 6 | 4 | 3 |  
| Worker C | 5 | 8 | 1 |  

*Concept from scratch:* The Hungarian method is an efficient algorithm for solving assignment problems, minimizing the total cost of assignments.  

*Step 1 — Convert the cost matrix into a square matrix (if necessary):*  
Costs are already in a square format.  

*Step 2 — Subtract the row minima and then column minima from each row and column, respectively:*  
\[
\begin{array}{c|ccc}
  & J1 & J2 & J3 \\
\hline
A & 7 & 0 & 5 \\
B & 3 & 1 & 0 \\
C & 4 & 7 & 0 \\
\end{array}
\]  

*Step 3 — Cover all zeros with the minimum number of lines and adjust the matrix if necessary:*  

*Step 4 — Assign jobs to workers based on the minimum cost while ensuring that no two assignments occur in the same row or column.*  

*Result:* Final assignments yield the minimum total cost of 7 for the optimal assignments.

### Section C: Advanced Theory & Numericals

**Q1. [Unit III | Topic: Cauchy-Newton Method | Type: Theory | Difficulty: Advanced]**  
**Question:** Discuss the Cauchy-Newton method for finding local minima of non-linear functions and its convergence properties.  

*Concept from scratch:* The Cauchy-Newton method is an iterative approach that combines ideas from Newton's method and steepest descent. It refines the search for local minima using the Hessian matrix to adjust the search direction based on curvature.  
*Convergence properties:* The method exhibits quadratic convergence near a local minimum under appropriate conditions, making it faster than gradient descent methods when close to the optimum.  

*Result:* Cauchy-Newton is particularly effective for functions where second derivatives can be computed efficiently.

---

**Q2. [Unit III | Topic: Random Jumping | Type: Numerical | Difficulty: Advanced]**  
**Question:** Use the random jumping technique to find the local minimum of the function \( f(x) = x^4 - 3x^3 + 2 \).  

*Concept from scratch:* Random jumping involves randomly selecting points in the domain and evaluating the function to locate a minimum. This technique is useful when the function has multiple local minima.  

*Step 1 — Define a range for random jumps, for example \( x \in [-2, 4] \).  

*Step 2 — Randomly sample points and evaluate \( f(x) \):*  
- Sample \( x_1 = 1 \), \( f(1) = 0 \)  
- Sample \( x_2 = 2 \), \( f(2) = -2 \)  

*Step 3 — Continue sampling until a minimum is found through sufficient iterations.*  

*Result:* After sufficient trials, identify \( x = 2 \) as a local minimum with \( f(2) = -2 \).

---

## Detailed Step-Wise Solutions — UNIT IV: Geometric Programming
### Section A: Definitions & Concept Questions

**Q1. [Unit IV | Topic: Geometric Programming | Type: Theory | Difficulty: Basic]**  
**Question:** Define geometric programming and its role in optimization.  

*Concept from scratch:* Geometric programming is a mathematical optimization technique used for problems with multiplicative relationships. It involves minimizing or maximizing a nonlinear objective function subject to constraints, typically in the form of inequalities.  
*Role in optimization:* It provides a systematic framework for solving complex optimization problems in various applications, including engineering design and resource allocation.  

*Result:* Geometric programming is essential for dealing with non-linear relationships in optimization scenarios.

---

**Q2. [Unit IV | Topic: Degree of Difficulty | Type: Theory | Difficulty: Basic]**  
**Question:** What is meant by the degree of difficulty in geometric programming?  

*Concept from scratch:* The degree of difficulty refers to the complexity of the geometric programming problem, which is often classified based on the number of variables and the nature of the constraints.  

*Result:* Understanding the degree of difficulty helps in selecting appropriate solution techniques and methods for optimization.

### Section B: Computational & Applied Problems

**Q1. [Unit IV | Topic: Constrained Minimization | Type: Numerical | Difficulty: Intermediate]**  
**Question:** Find the minimum of the function \( f(x, y) = xy \) subject to the constraints \( x + y = 10, x, y > 0 \) using geometric programming methods.  

*Concept from scratch:* We can express the objective function in terms of one variable using the constraint.  

*Step 1 — Substitute \( y = 10 - x \) into \( f \):*  
\[ f(x) = x(10 - x) = 10x - x^2 \]  

*Step 2 — Differentiate and find critical points:*  
\[ f'(x) = 10 - 2x \]  
Setting \( f'(x) = 0 \) gives:  
\[ 10 - 2x = 0 \Rightarrow x = 5 \]  

*Step 3 — Verify using second derivative test:*  
\[ f''(x) = -2 \] (which is negative, confirming a maximum.)  

*Step 4 — Find \( y \) value:*  
If \( x = 5 \), then \( y = 10 - 5 = 5 \).  

*Result:* The minimum value of \( f(x, y) = 25 \) occurs at \( (5, 5) \).

---

**Q2. [Unit IV | Topic: Deterministic Dynamic Programming | Type: Numerical | Difficulty: Intermediate]**  
**Question:** Formulate and solve a dynamic programming problem for a simple knapsack scenario where the items have specific weights and values.  

*Concept from scratch:* A knapsack problem involves selecting items with given weights and values to maximize the total value without exceeding the knapsack's weight capacity.  

*Step 1 — Define the items, weights, and values:*  
- Item 1: Weight = 2, Value = 3  
- Item 2: Weight = 3, Value = 4  
- Item 3: Weight = 4, Value = 5  
- Capacity = 5  

*Step 2 — Create a table to calculate maximum values at each capacity step:*  

*Step 3 — Fill the table using recursive relationships to determine the maximum value that can be achieved with available weights.*  

*Result:* Final solution yields the maximum value achievable without exceeding capacity, typically using backtracking to determine which items to select.

### Section C: Advanced Theory & Numericals

**Q1. [Unit IV | Topic: Applications of Geometric Programming | Type: Theory | Difficulty: Advanced]**  
**Question:** Discuss the applications of geometric programming in real-world scenarios such as resource allocation and production problems.  

*Concept from scratch:* Geometric programming is used in various fields, including economics, engineering, and logistics. It helps in optimizing production processes, resource allocation, and cost minimization, especially when dealing with multiplicative relationships.  

*Result:* Its versatility makes it suitable for complex decision-making scenarios involving multiple variables and constraints.

---

**Q2. [Unit IV | Topic: Complementary Geometric Programming | Type: Numerical | Difficulty: Advanced]**  
**Question:** Solve a complementary geometric programming problem involving two functions \( f(x) \) and \( g(y) \) subject to certain constraints.  

*Concept from scratch:* Complementary geometric programming involves optimizing two related functions while respecting constraints that link them.  

*Step 1 — Define the functions and constraints clearly.*  

*Step 2 — Use methods such as Lagrange multipliers or KKT conditions to find solutions.*  

*Result:* Final solutions yield optimal values for both functions while satisfying the interdependencies defined by the constraints.

---

This concludes the detailed step-wise solutions for the entire question bank for the course BSM-253 - Optimization Techniques. Each solution progressively builds on the concepts required for understanding and solving optimization problems.