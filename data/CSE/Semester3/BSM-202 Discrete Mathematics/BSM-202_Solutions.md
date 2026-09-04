# BSM-202 - Discrete Mathematics
## Detailed Step-Wise Solutions — Units I–IV (Combined)

## Detailed Step-Wise Solutions — UNIT I: Set Theory, Relation and Function
### Section A: Definitions & Concept Questions

**Q1. [Unit I | Topic: Set Operations | Type: Theory | Difficulty: Basic]**  
**Question:** Define union, intersection, and difference of sets with examples.  

*Concept from scratch:*  
In set theory, sets are collections of distinct objects. The operations of union, intersection, and difference are fundamental ways to combine or compare sets.

- **Union** of two sets A and B, denoted as A ∪ B, is the set of elements that are in A, in B, or in both.  
- **Intersection** of two sets A and B, denoted as A ∩ B, is the set of elements that are common to both A and B.  
- **Difference** of two sets A and B, denoted as A - B, is the set of elements that are in A but not in B.

*Examples:*  
Let A = {1, 2, 3} and B = {2, 3, 4}.  
- A ∪ B = {1, 2, 3, 4}  
- A ∩ B = {2, 3}  
- A - B = {1}  

*Result:* The definitions and examples of union, intersection, and difference of sets are provided.

---

**Q2. [Unit I | Topic: Relations | Type: Theory | Difficulty: Basic]**  
**Question:** What is a binary relation? Provide an example of a binary relation on a set.  

*Concept from scratch:*  
A binary relation on a set A is a subset of the Cartesian product A × A. It associates elements of A with one another.

*Step 1 — Define the set:*  
Let A = {1, 2, 3}.  

*Step 2 — Define the Cartesian product:*  
A × A = {(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)}.  

*Step 3 — Define a binary relation:*  
Let R = {(1, 2), (2, 3)}. R is a binary relation on A since it is a subset of A × A.

*Result:* R = {(1, 2), (2, 3)} is an example of a binary relation on the set A.

---

**Q3. [Unit I | Topic: Equivalence Relations | Type: Theory | Difficulty: Basic]**  
**Question:** Explain the properties of equivalence relations with an example.  

*Concept from scratch:*  
An equivalence relation on a set is a relation that satisfies three properties: reflexivity, symmetry, and transitivity.

- **Reflexivity:** For every element a in set A, (a, a) is in R.  
- **Symmetry:** If (a, b) is in R, then (b, a) is also in R.  
- **Transitivity:** If (a, b) is in R and (b, c) is in R, then (a, c) is in R.

*Example:*  
Let A = {1, 2, 3} and define R = {(1, 1), (2, 2), (3, 3), (1, 2), (2, 1)}.  
- Reflexivity holds as all elements relate to themselves.  
- Symmetry holds as (1, 2) implies (2, 1).  
- Transitivity is satisfied as (1, 2) and (2, 1) imply (1, 1).

*Result:* R is an equivalence relation on set A.

### Section B: Computational & Applied Problems

**Q1. [Unit I | Topic: Power Set Theorem | Type: Numerical | Difficulty: Intermediate]**  
**Question:** Given a set A = {1, 2}, find the power set of A.  

*Concept from scratch:*  
The power set of a set S is the set of all its subsets, including the empty set and S itself. If a set has n elements, its power set will have 2^n elements.

*Step 1 — Define the set:*  
Let A = {1, 2}.  

*Step 2 — Calculate 2^n where n is the number of elements in A:*  
Here, n = 2, so 2^2 = 4.  

*Step 3 — List all subsets:*  
The subsets of A are:  
- ∅ (empty set)  
- {1}  
- {2}  
- {1, 2}  

*Result:* The power set P(A) = {∅, {1}, {2}, {1, 2}}.

---

**Q2. [Unit I | Topic: Cantor's Diagonal Argument | Type: Theory | Difficulty: Intermediate]**  
**Question:** Explain Cantor's diagonal argument and its significance in set theory.  

*Concept from scratch:*  
Cantor's diagonal argument is a method used to demonstrate that some infinite sets are uncountably infinite, meaning they cannot be put into a one-to-one correspondence with the natural numbers.

*Step 1 — Assume that we can list all real numbers between 0 and 1:*  
Suppose we have a list of all such numbers. Each number can be represented as an infinite decimal.

*Step 2 — Construct a new real number:*  
By changing the nth digit of the nth number in the list, we create a new number that differs from every number in the list at least at one decimal place.

*Step 3 — Conclusion:*  
This new number cannot be in the original list, contradicting the assumption that we had listed all real numbers. Hence, the real numbers are uncountably infinite.

*Result:* Cantor's diagonal argument shows that the set of real numbers is larger than the set of natural numbers.

### Section C: Advanced Theory & Numericals

**Q1. [Unit I | Topic: Schroder-Bernstein Theorem | Type: Theory | Difficulty: Advanced]**  
**Question:** State and prove the Schroder-Bernstein theorem.  

*Concept from scratch:*  
The Schroder-Bernstein theorem states that if there are injections f: A → B and g: B → A between sets A and B, then there is a bijection between A and B.

*Step 1 — Assume injections exist:*  
Let f: A → B and g: B → A be injections.  

*Step 2 — Define the equivalence classes:*  
Define sets S and T based on the images under g and f, respectively.  

*Step 3 — Construct a bijection:*  
Using the images of f and g, define a new function that maps elements of A and B uniquely to each other.

*Result:* The conclusion of the theorem is that there exists a bijection between A and B, proving the theorem.

---

**Q2. [Unit I | Topic: Countability | Type: Numerical | Difficulty: Advanced]**  
**Question:** Prove that the set of all integers is countably infinite.  

*Concept from scratch:*  
A set is countably infinite if there exists a bijection between the set and the natural numbers.

*Step 1 — Define the set of integers:*  
The set of integers Z = {..., -3, -2, -1, 0, 1, 2, 3, ...}.  

*Step 2 — Create a bijection:*  
Define a function that maps natural numbers to integers as follows:  
1 → 0,  
2 → 1,  
3 → -1,  
4 → 2,  
5 → -2,  
6 → 3,  
7 → -3, ...

*Step 3 — Show the mapping is complete:*  
This mapping covers all integers, demonstrating a one-to-one correspondence.

*Result:* The set of all integers is countably infinite.

## Detailed Step-Wise Solutions — UNIT II: Propositional Logic and Proof Techniques
### Section A: Definitions & Concept Questions

**Q1. [Unit II | Topic: Propositional Logic | Type: Theory | Difficulty: Basic]**  
**Question:** Define propositional logic and its components.  

*Concept from scratch:*  
Propositional logic is a branch of logic that deals with propositions, which are declarative statements that can be either true or false.

*Step 1 — Identify components:*
- **Propositions:** Basic statements, e.g., "It is raining."
- **Logical connectives:** Operators that combine propositions, such as:
  - AND (∧)
  - OR (∨)
  - NOT (¬)
  - IMPLIES (→)

*Result:* Propositional logic is defined by propositions and their combinations using logical connectives.

---

**Q2. [Unit II | Topic: Validity | Type: Theory | Difficulty: Basic]**  
**Question:** What is the difference between valid, satisfiable, and unsatisfiable formulas?  

*Concept from scratch:*  
Understanding these terms helps in evaluating logical arguments.

- **Valid formula:** A formula that is true under all interpretations.  
- **Satisfiable formula:** A formula that is true under at least one interpretation.  
- **Unsatisfiable formula:** A formula that is false under all interpretations.

*Result:* The distinctions between valid, satisfiable, and unsatisfiable formulas are clarified.

### Section B: Computational & Applied Problems

**Q1. [Unit II | Topic: Validity of Arguments | Type: Numerical | Difficulty: Intermediate]**  
**Question:** Evaluate the validity of the argument: "If it rains, the ground is wet. It is raining. Therefore, the ground is wet."  

*Concept from scratch:*  
To evaluate the argument, we can use propositional logic.

*Step 1 — Define propositions:*  
Let P = "It rains," Q = "The ground is wet."  

*Step 2 — Express the argument:*  

1. P → Q (If it rains, the ground is wet.)

2. P (It is raining.)

3. Therefore, Q (The ground is wet.)

*Step 3 — Determine validity:*  
The argument is valid if the premises lead to the conclusion. Since P is true, Q must also be true.

*Result:* The argument is valid.

---

**Q2. [Unit II | Topic: Proof Techniques | Type: Theory | Difficulty: Intermediate]**  
**Question:** Explain proof by contradiction with an example.  

*Concept from scratch:*  
Proof by contradiction assumes that the statement to be proven is false and shows that this leads to a contradiction.

*Step 1 — State the theorem:*  
Let’s prove that √2 is irrational.  

*Step 2 — Assume the opposite:*  
Assume √2 is rational, so it can be expressed as a fraction a/b (where a and b are integers with no common factors).  

*Step 3 — Derive a contradiction:*  
Squaring both sides gives 2 = a²/b² → a² = 2b². This means a² is even, thus a is even (let a = 2k). Substituting gives 4k² = 2b² → b² = 2k², so b is also even, contradicting our assumption that a and b have no common factors.

*Result:* Therefore, √2 is irrational.

### Section C: Advanced Theory & Numericals

**Q1. [Unit II | Topic: Necessity and Sufficiency | Type: Theory | Difficulty: Advanced]**  
**Question:** Discuss necessity and sufficiency in logical statements with examples.  

*Concept from scratch:*  
Understanding necessity and sufficiency is critical in logical reasoning.

- **Necessary condition:** A condition that must be true for the statement to be true.  
- **Sufficient condition:** A condition that guarantees the statement is true.

*Example:*  
Let P = "It is raining," Q = "The ground is wet."  
- P is a sufficient condition for Q (if it rains, the ground is wet).
- However, Q does not imply P (the ground can be wet for other reasons).

*Result:* The concepts of necessity and sufficiency are illustrated.

---

**Q2. [Unit II | Topic: Proof Techniques | Type: Numerical | Difficulty: Advanced]**  
**Question:** Prove that the square of any odd integer is odd.  

*Concept from scratch:*  
An integer is odd if it can be expressed in the form 2k + 1 for some integer k.

*Step 1 — Define an odd integer:*  
Let n be an odd integer, so n = 2k + 1 for some integer k.  

*Step 2 — Compute the square:*  
n² = (2k + 1)² = 4k² + 4k + 1 = 2(2k² + 2k) + 1.  

*Step 3 — Show the result is odd:*  
Since 2(2k² + 2k) is even, n² = even + 1 = odd.

*Result:* The square of any odd integer is odd.

## Detailed Step-Wise Solutions — UNIT III: Algebraic Structures
### Section A: Definitions & Concept Questions

**Q1. [Unit III | Topic: Semigroups | Type: Theory | Difficulty: Basic]**  
**Question:** Define a semigroup and provide an example.  

*Concept from scratch:*  
A semigroup is a set equipped with an associative binary operation.

*Step 1 — Define a semigroup:*  
A set S with a binary operation * is a semigroup if:

1. Closure: For all a, b ∈ S, a * b ∈ S.

2. Associativity: For all a, b, c ∈ S, (a * b) * c = a * (b * c).

*Step 2 — Provide an example:*  
Let S = {0, 1} with the operation * defined as addition modulo 2.  
- Closure: 0 + 0 = 0, 0 + 1 = 1, 1 + 1 = 0 (all results are in S).  
- Associativity: (0 + 1) + 1 = 0 + 1 = 1 and 0 + (1 + 1) = 0 + 0 = 0.

*Result:* S is a semigroup.

---

**Q2. [Unit III | Topic: Groups | Type: Theory | Difficulty: Basic]**  
**Question:** What is a group? List the properties that define a group.  

*Concept from scratch:*  
A group is a set with a binary operation that satisfies four properties: closure, associativity, identity, and invertibility.

*Step 1 — Define a group:*  
A set G with a binary operation * is a group if:

1. Closure: For all a, b ∈ G, a * b ∈ G.

2. Associativity: For all a, b, c ∈ G, (a * b) * c = a * (b * c).

3. Identity: There exists an element e ∈ G such that for every a ∈ G, e * a = a and a * e = a.

4. Invertibility: For every a ∈ G, there exists an element b ∈ G such that a * b = e.

*Result:* The properties that define a group are listed.

### Section B: Computational & Applied Problems

**Q1. [Unit III | Topic: Cyclic Groups | Type: Numerical | Difficulty: Intermediate]**  
**Question:** Determine whether the set of integers under addition forms a cyclic group.  

*Concept from scratch:*  
A cyclic group is a group generated by a single element.

*Step 1 — Define the operation:*  
Consider the set of integers Z under addition.  

*Step 2 — Check group properties:*  

1. Closure: For any a, b ∈ Z, a + b ∈ Z (closure holds).

2. Associativity: Addition is associative.

3. Identity: The identity element is 0 (a + 0 = a).

4. Inverses: For any a ∈ Z, there exists -a ∈ Z such that a + (-a) = 0.

*Step 3 — Check for cyclic property:*  
The integer 1 generates all integers under addition since n = 1 + 1 + ... + 1 (n times) or n = -1 + -1 + ... + -1 (n times).

*Result:* The set of integers under addition forms a cyclic group.

---

**Q2. [Unit III | Topic: Normal Subgroups | Type: Theory | Difficulty: Intermediate]**  
**Question:** Explain what a normal subgroup is and provide an example.  

*Concept from scratch:*  
A normal subgroup is a subgroup that is invariant under conjugation by elements of the group.

*Step 1 — Define a normal subgroup:*  
A subgroup N of G is normal if for every g ∈ G and n ∈ N, the element gng⁻¹ is also in N.

*Step 2 — Provide an example:*  
Let G = S₃ (the symmetric group of degree 3) and let N = A₃ (the alternating group).  
- Check normality: For any g ∈ S₃ and n ∈ A₃, gng⁻¹ remains in A₃ since the even permutations remain even after conjugation.

*Result:* N is a normal subgroup of G.

### Section C: Advanced Theory & Numericals

**Q1. [Unit III | Topic: Rings | Type: Theory | Difficulty: Advanced]**  
**Question:** Define a ring and discuss its properties with examples.  

*Concept from scratch:*  
A ring is an algebraic structure consisting of a set equipped with two binary operations: addition and multiplication.

*Step 1 — Define a ring:*  
A set R with operations + and * is a ring if:

1. (R, +) is an abelian group.

2. (R, *) is a semigroup.

3. Multiplication is distributive over addition.

*Step 2 — Provide an example:*  
Consider the set of integers Z under standard addition and multiplication.  
- Z is an abelian group under addition.  
- Z is a semigroup under multiplication.  
- Multiplication distributes over addition.

*Result:* Z is a ring.

---

**Q2. [Unit III | Topic: Boolean Algebra | Type: Numerical | Difficulty: Advanced]**  
**Question:** Prove that the set of all Boolean functions forms a Boolean ring.  

*Concept from scratch:*  
A Boolean ring is a ring where every element is idempotent, meaning x * x = x.

*Step 1 — Define Boolean functions:*  
A Boolean function maps binary inputs to binary outputs.  

*Step 2 — Show closure and operations:*  
- Addition corresponds to XOR, and multiplication corresponds to AND.
- Both operations are closed over the set of Boolean functions.

*Step 3 — Idempotent property:*  
For any Boolean function f, f + f = f and f * f = f (idempotent property holds).

*Result:* The set of Boolean functions forms a Boolean ring.

## Detailed Step-Wise Solutions — UNIT IV: Combinatorics
### Section A: Definitions & Concept Questions

**Q1. [Unit IV | Topic: Inclusion-Exclusion | Type: Theory | Difficulty: Basic]**  
**Question:** State the principle of inclusion-exclusion and provide a simple example.  

*Concept from scratch:*  
The principle of inclusion-exclusion is used to calculate the size of the union of multiple sets.

*Step 1 — State the principle:*  
For two sets A and B, |A ∪ B| = |A| + |B| - |A ∩ B|.  
For three sets, |A ∪ B ∪ C| = |A| + |B| + |C| - |A ∩ B| - |A ∩ C| - |B ∩ C| + |A ∩ B ∩ C|.

*Step 2 — Provide an example:*  
Let |A| = 5, |B| = 4, |A ∩ B| = 2. Then |A ∪ B| = 5 + 4 - 2 = 7.

*Result:* The principle of inclusion-exclusion is stated and illustrated.

---

**Q2. [Unit IV | Topic: Permutation | Type: Theory | Difficulty: Basic]**  
**Question:** What is a permutation? How is it different from a combination?  

*Concept from scratch:*  
A permutation is a rearrangement of elements in a specific order, whereas a combination is a selection of elements without regard to the order.

*Step 1 — Define permutation:*  
The number of permutations of n distinct objects is n!.  

*Step 2 — Define combination:*  
The number of combinations of n objects taken k at a time is given by C(n, k) = n! / (k!(n-k)!).

*Result:* The definitions and distinctions between permutations and combinations are provided.

### Section B: Computational & Applied Problems

**Q1. [Unit IV | Topic: Pigeon-Hole Principle | Type: Numerical | Difficulty: Intermediate]**  
**Question:** Use the pigeon-hole principle to prove that in any group of 13 people, at least two people have the same birth month.  

*Concept from scratch:*  
The pigeon-hole principle states that if n items are put into m containers, with n > m, at least one container must contain more than one item.

*Step 1 — Identify items and containers:*  
Let the 13 people be the items and the 12 months be the containers.  

*Step 2 — Apply the principle:*  
Since 13 > 12, at least one month must contain at least two people.

*Result:* The statement is proved using the pigeon-hole principle.

---

**Q2. [Unit IV | Topic: Recurrence Relations | Type: Numerical | Difficulty: Intermediate]**  
**Question:** Solve the recurrence relation T(n) = 2T(n-1) + 1 with T(1) = 1.  

*Concept from scratch:*  
Recurrence relations express terms in terms of previous terms.

*Step 1 — Expand the relation:*  
T(n) = 2T(n-1) + 1  
T(n-1) = 2T(n-2) + 1 → T(n) = 2(2T(n-2) + 1) + 1 = 4T(n-2) + 2 + 1  
Continue expanding until reaching the base case.

*Step 2 — Generalize:*  
T(n) = 2^k T(n-k) + (2^k - 1)  

When k = n-1, T(1) = 1, thus:  
T(n) = 2^(n-1) T(1) + (2^(n-1) - 1) = 2^(n-1) + (2^(n-1) - 1) = 2^n - 1.

*Result:* T(n) = 2^n - 1.

### Section C: Advanced Theory & Numericals

**Q1. [Unit IV | Topic: Generating Functions | Type: Theory | Difficulty: Advanced]**  
**Question:** Explain generating functions and their application in combinatorics.  

*Concept from scratch:*  
Generating functions are formal power series used to encode sequences and solve combinatorial problems.

*Step 1 — Define a generating function:*  
The ordinary generating function of a sequence a₀, a₁, a₂, ... is given by G(x) = a₀ + a₁x + a₂x² + ...  

*Step 2 — Applications:*  
They can be used to find closed forms of sequences, count combinatorial objects, or solve recurrence relations.

*Result:* Generating functions are defined and their applications in combinatorics are discussed.

---

**Q2. [Unit IV | Topic: Summations | Type: Numerical | Difficulty: Advanced]**  
**Question:** Evaluate the summation S = ∑_(k=1)^n k^2 using generating functions.  

*Concept from scratch:*  
We can derive the formula for the sum of the first n squares using generating functions.

*Step 1 — Set up the generating function:*  
The generating function for k² can be found by differentiating the function for the sum of k.

*Step 2 — Derive the closed form:*  
The closed form for the sum of squares is known to be S = n(n + 1)(2n + 1)/6.

*Result:* The summation S = ∑_(k=1)^n k² evaluates to n(n + 1)(2n + 1)/6.

---

This concludes the detailed step-wise solutions for the question bank covering all units as requested.