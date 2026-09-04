# BCS-403 - Introduction to Functional and Logic Programming
## Detailed Step-Wise Solutions — Units I–IV (Combined)

## Detailed Step-Wise Solutions — UNIT I: Distinctive Features of Functional Programming
### Section A: Definitions & Concept Questions

**Q1. [Unit I | Topic: Distinctive features of functional programming | Type: Theory | Difficulty: Basic]**  
**Question:** Define functional programming and describe its distinctive features.  

*Concept from scratch:* Functional programming is a programming paradigm that treats computation as the evaluation of mathematical functions and avoids changing state and mutable data. The key distinctive features of functional programming include:  

1. **First-Class and Higher-Order Functions**: Functions can be passed as arguments to other functions, returned as values from other functions, and assigned to variables.

2. **Pure Functions**: Functions that always produce the same output for the same input and do not cause side effects.

3. **Immutability**: Data is immutable, meaning once a data structure is created, it cannot be changed.

4. **Recursion**: Functional programming languages rely on recursive functions rather than iterative loops for control flow.

5. **Lazy Evaluation**: Expressions are not evaluated until their values are needed, which can improve performance and enable the creation of potentially infinite data structures.

*Result:* Functional programming is a paradigm characterized by the use of first-class functions, pure functions, immutability, recursion, and lazy evaluation.

---

**Q2. [Unit I | Topic: Recursion | Type: Theory | Difficulty: Basic]**  
**Question:** Explain the concept of recursion in programming with an example.  

*Concept from scratch:* Recursion is a method where a function calls itself in order to solve a problem. This approach breaks a problem into smaller subproblems. A recursive function typically consists of two main parts: the base case, which stops the recursion, and the recursive case, which continues to call the function.  

*Example:* A common example is calculating the factorial of a number n.  

1. **Base case**: If n = 0, return 1.

2. **Recursive case**: If n > 0, return n * factorial(n - 1).

*Result:* The recursive definition of factorial can be expressed as follows:

```python
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)
```

---

**Q3. [Unit I | Topic: Tail Recursion | Type: Theory | Difficulty: Basic]**  
**Question:** What is tail recursion and how does it differ from regular recursion?  

*Concept from scratch:* Tail recursion occurs when a recursive function's final action is to call itself. In tail recursion, the function does not need to retain any state after the recursive call, allowing for optimization by the compiler or interpreter.  

*Difference from regular recursion:* In regular recursion, each function call must remain in memory until the base case is reached, leading to stack overflow for deep recursions. In contrast, tail recursion enables the re-use of the current function's stack frame, thus preventing stack overflow and improving performance.  

*Result:* Tail recursion is a form of recursion where the recursive call is the last operation in the function, allowing for optimization and reduced memory usage.

---

### Section B: Computational & Applied Problems

**Q1. [Unit I | Topic: Higher Order Functions | Type: Numericals | Difficulty: Intermediate]**  
**Question:** Write a higher order function in a functional programming language that takes a function and a list as arguments and applies the function to each element of the list.  

*Concept from scratch:* A higher-order function is a function that can take another function as an argument or return a function. The idea is to create a function that takes another function (e.g., a mathematical operation) and a list, then applies that function to each element of the list.  

*Step 1 — Define the higher-order function:* In Haskell, this can be done using the `map` function.  

*Example:*

```haskell
applyFunction :: (a -> b) -> [a] -> [b]
applyFunction f lst = map f lst
```
Here, `f` is the function, and `lst` is the list.

*Result:* The function `applyFunction` applies the function `f` to each element of the list `lst`.

---

**Q2. [Unit I | Topic: Lazy Evaluation | Type: Numericals | Difficulty: Intermediate]**  
**Question:** Explain lazy evaluation and demonstrate it with a code snippet in a functional programming language of your choice.  

*Concept from scratch:* Lazy evaluation is a programming technique where an expression is not evaluated until its value is needed. This allows for the creation of infinite data structures and can lead to performance improvements by avoiding unnecessary computations.  

*Step 1 — Example of lazy evaluation in Haskell:*

```haskell
numbers = [1..]  -- This creates an infinite list of numbers
takeFive = take 5 numbers  -- Only takes the first 5 elements
```
In this example, `numbers` is an infinite list, but the `take` function only evaluates the first five elements, demonstrating lazy evaluation.

*Result:* Lazy evaluation allows for the creation and manipulation of potentially infinite data structures without immediate computation.

---

### Section C: Advanced Theory & Numericals

**Q1. [Unit I | Topic: Lambda Calculus | Type: Theory | Difficulty: Advanced]**  
**Question:** Discuss the significance of lambda calculus in functional programming and provide examples of its application.  

*Concept from scratch:* Lambda calculus is a formal system for expressing computation based on function abstraction and application. It serves as the theoretical foundation of functional programming languages, allowing for the representation of functions as first-class citizens.  

*Significance:* In functional programming, lambda calculus allows for the creation of anonymous functions, supports higher-order functions, and enables reasoning about functions mathematically.  

*Example:*
- A simple function in lambda calculus to add two numbers can be expressed as:  
  `λx. λy. x + y`  
- This corresponds to a function that takes two arguments, `x` and `y`, and returns their sum.

*Result:* Lambda calculus is fundamental to functional programming, enabling the representation and manipulation of functions.

---

**Q2. [Unit I | Topic: Types in Functional Programming | Type: Theory | Difficulty: Advanced]**  
**Question:** Analyze the role of types in functional programming and how they enhance program reliability.  

*Concept from scratch:* Types in functional programming define the kind of data that can be processed by functions. Strongly typed languages enforce type checking at compile-time, reducing runtime errors. Types enhance program reliability by:  

1. **Type Safety**: Preventing type errors by ensuring that functions receive the correct type of arguments.

2. **Abstraction**: Allowing for the creation of generic functions that can operate on different types.

3. **Documentation**: Providing a form of documentation that describes how functions and data can be used.

*Result:* Types in functional programming ensure correctness, enhance reliability, and serve as a form of documentation for functions and data structures.

---

## Detailed Step-Wise Solutions — UNIT II: Introduction to Haskell
### Section A: Definitions & Concept Questions

**Q1. [Unit II | Topic: Haskell | Type: Theory | Difficulty: Basic]**  
**Question:** What is Haskell and what are its key features?  

*Concept from scratch:* Haskell is a statically typed, purely functional programming language known for its strong type system and lazy evaluation. It is designed for high-level abstraction and code clarity.  
*Key features include:*  

1. **Purely Functional**: All computations are expressed as functions without side effects.

2. **Lazy Evaluation**: Expressions are evaluated only when needed.

3. **Strong Static Typing**: Types are checked at compile-time, preventing many runtime errors.

4. **Type Inference**: The compiler can often deduce types automatically.

5. **First-Class Functions**: Functions can be passed as arguments, returned from other functions, and stored in data structures.

*Result:* Haskell is a purely functional programming language with features like lazy evaluation, strong static typing, and first-class functions.

---

**Q2. [Unit II | Topic: Guards in Haskell | Type: Theory | Difficulty: Basic]**  
**Question:** Explain guards in Haskell with an example function.  

*Concept from scratch:* Guards in Haskell are a way to specify conditions that determine which function definition to execute. They act like if-else statements and are used to provide more readable code.  

*Example:*

```haskell
absoluteValue :: Int -> Int
absoluteValue x
    | x < 0     = -x
    | otherwise = x
```
In this example, the function `absoluteValue` uses guards to return the absolute value of `x`.

*Result:* Guards allow for more expressive and cleaner conditional expressions in Haskell functions.

---

### Section B: Computational & Applied Problems

**Q1. [Unit II | Topic: Pattern Matching | Type: Numericals | Difficulty: Intermediate]**  
**Question:** Write a Haskell function that uses pattern matching to calculate the factorial of a number.  

*Concept from scratch:* Pattern matching in Haskell allows functions to behave differently based on the structure of their arguments. For calculating factorial, we will match the input against patterns.  

*Step 1 — Define the function using pattern matching:*

```haskell
factorial :: Int -> Int
factorial 0 = 1
factorial n = n * factorial (n - 1)
```
Here, the function directly matches the input `0` and provides a base case, while for any other integer `n`, it computes `n * factorial (n - 1)`.

*Result:* The function `factorial` successfully calculates the factorial of a number using pattern matching.

---

**Q2. [Unit II | Topic: Lists | Type: Numericals | Difficulty: Intermediate]**  
**Question:** Create a Haskell program that takes a list of integers and returns a list of their squares.  

*Concept from scratch:* In Haskell, we can utilize list comprehensions or the `map` function to apply a function to each element of a list.  

*Step 1 — Define the function:*

```haskell
squareList :: [Int] -> [Int]
squareList lst = map (^2) lst
```
In this example, `map (^2) lst` applies the squaring function to each element in the list.

*Result:* The function `squareList` takes a list of integers and returns a list containing their squares.

---

### Section C: Advanced Theory & Numericals

**Q1. [Unit II | Topic: Types and Polymorphism | Type: Theory | Difficulty: Advanced]**  
**Question:** Discuss the importance of polymorphism in Haskell and provide examples of its implementation.  

*Concept from scratch:* Polymorphism in Haskell allows functions to operate on different types, enhancing code reusability and flexibility. There are two main types of polymorphism:  

1. **Parametric Polymorphism**: Functions are written generically so they can handle values uniformly without depending on their type.

2. **Ad-hoc Polymorphism**: Achieved through type classes, allowing different types to be treated as the same type when they share a common interface.

*Example of Parametric Polymorphism:*

```haskell
identity :: a -> a
identity x = x
```

*Example of Ad-hoc Polymorphism using Type Classes:*

```haskell
class Show a where
    show :: a -> String
```
In this case, any type that implements the `Show` type class can be converted to a `String`.

*Result:* Polymorphism in Haskell significantly enhances code flexibility and reusability through parametric and ad-hoc polymorphism.

---

**Q2. [Unit II | Topic: Infinite Data Structures | Type: Theory | Difficulty: Advanced]**  
**Question:** Explain the concept of infinite data structures in Haskell and how they can be utilized effectively.  

*Concept from scratch:* Infinite data structures in Haskell are possible due to lazy evaluation, allowing the creation of potentially unbounded collections without immediate computation. This enables the definition of structures like infinite lists.  

*Example:* An infinite list of natural numbers can be defined as follows:

```haskell
naturals :: [Int]
naturals = [0..]  -- An infinite list starting from 0
```
We can utilize functions like `take` to operate only on the required portions of the infinite list:

```haskell
firstTenNaturals = take 10 naturals  -- Produces [0, 1, 2, ..., 9]
```

*Result:* Infinite data structures allow for the concise representation of unbounded sequences, enabling powerful abstractions in Haskell programming.

---

## Detailed Step-Wise Solutions — UNIT III: Logic and Reasoning
### Section A: Definitions & Concept Questions

**Q1. [Unit III | Topic: Logic Programs | Type: Theory | Difficulty: Basic]**  
**Question:** What is a logic program and how does it differ from functional programming?  

*Concept from scratch:* A logic program is a set of sentences in logical form that expresses facts and rules about some problem domain. Logic programming is based on formal logic and allows for automated reasoning.  

*Difference from functional programming:*  
- **Functional programming** focuses on function evaluation and treats computation as the application of functions to arguments.
- **Logic programming** emphasizes the use of logical statements and inference to derive conclusions from given facts and rules.

*Result:* Logic programs consist of logical statements that facilitate reasoning, contrasting with the function-oriented approach of functional programming.

---

**Q2. [Unit III | Topic: Prolog Syntax | Type: Theory | Difficulty: Basic]**  
**Question:** Describe the basic syntax of Prolog.  

*Concept from scratch:* Prolog (Programming in Logic) is a logic programming language characterized by its use of facts, rules, and queries.  
*Basic syntax includes:*  

1. **Facts**: Declared using predicates.  
   - Example: `parent(john, mary).` states that John is a parent of Mary.

2. **Rules**: Defined using implications.  
   - Example: `grandparent(X, Y) :- parent(X, Z), parent(Z, Y).` means X is a grandparent of Y if X is a parent of Z and Z is a parent of Y.

3. **Queries**: Used to ask questions about the knowledge base.  
   - Example: `?- parent(john, mary).` asks if John is a parent of Mary.

*Result:* Prolog syntax includes facts, rules, and queries, forming the basis for knowledge representation and reasoning.

---

### Section B: Computational & Applied Problems

**Q1. [Unit III | Topic: Tail Recursion in Prolog | Type: Numericals | Difficulty: Intermediate]**  
**Question:** Implement a tail recursive function in Prolog to compute the sum of a list.  

*Concept from scratch:* Tail recursion in Prolog allows a function to call itself as its last action, optimizing memory usage.  

*Step 1 — Define the tail-recursive sum function:*

```prolog
sum_list(List, Sum) :- sum_list(List, 0, Sum).

sum_list([], Acc, Acc).  % Base case: when the list is empty, return the accumulator
sum_list([Head|Tail], Acc, Sum) :- 
    NewAcc is Acc + Head,   % Update the accumulator
    sum_list(Tail, NewAcc, Sum).  % Recursive call
```

*Result:* The Prolog code defines a tail-recursive function `sum_list` that computes the sum of a list using an accumulator.

---

**Q2. [Unit III | Topic: Accumulators | Type: Numericals | Difficulty: Intermediate]**  
**Question:** Write a Prolog program that uses an accumulator to reverse a list.  

*Concept from scratch:* Accumulators are used to carry intermediate results through recursive calls, facilitating operations like reversing a list.  

*Step 1 — Define the reverse function with an accumulator:*

```prolog
reverse_list(List, Reversed) :- reverse_list(List, [], Reversed).

reverse_list([], Acc, Acc).  % Base case: when the list is empty, return the accumulator
reverse_list([Head|Tail], Acc, Reversed) :- 
    reverse_list(Tail, [Head|Acc], Reversed).  % Prepend head to accumulator
```

*Result:* The Prolog code implements a list reversal function using an accumulator.

---

### Section C: Advanced Theory & Numericals

**Q1. [Unit III | Topic: Difference Lists | Type: Theory | Difficulty: Advanced]**  
**Question:** Explain the concept of difference lists in Prolog and demonstrate their use in list manipulation.  

*Concept from scratch:* Difference lists provide an efficient way to represent lists in Prolog by expressing lists as pairs of lists. A difference list can be defined as `A-B`, where `A` is the list and `B` is a list that, when appended to `A`, gives the same result as the original list.  

*Example of using difference lists:*

```prolog
append_diff([], L, L).
append_diff([Head|Tail], L, [Head|R]) :- append_diff(Tail, L, R).
```
Here, `append_diff` uses difference lists to append two lists efficiently without reconstructing the entire list structure.

*Result:* Difference lists enhance list manipulation efficiency in Prolog by representing lists as pairs, optimizing append operations.

---

**Q2. [Unit III | Topic: Logic and Reasoning | Type: Theory | Difficulty: Advanced]**  
**Question:** Analyze the relationship between logic and reasoning in the context of logic programming.  

*Concept from scratch:* Logic programming combines formal logic with programming, allowing for automated reasoning over facts and rules. The relationship can be analyzed as follows:  

1. **Logical Inference**: Logic programming allows for the derivation of new information from known facts using inference rules.

2. **Declarative Nature**: Logic programs describe what the program should accomplish rather than how to achieve it, emphasizing declarative reasoning.

3. **Automated Reasoning**: Logic programming languages like Prolog can execute queries and derive conclusions without explicit procedural instructions.

*Result:* The relationship between logic and reasoning in logic programming enables automated inference and emphasizes a declarative approach to problem-solving.

---

## Detailed Step-Wise Solutions — UNIT IV: Applications of Logic Programming
### Section A: Definitions & Concept Questions

**Q1. [Unit IV | Topic: Theorem Proving | Type: Theory | Difficulty: Basic]**  
**Question:** Define theorem proving and its significance in logic programming.  

*Concept from scratch:* Theorem proving is the process of demonstrating the truth of mathematical statements or logical assertions through formal methods. In logic programming, it involves using logical rules and facts to derive conclusions from premises.  

*Significance:* Theorem proving is crucial for verifying the correctness of programs, ensuring that they adhere to specified properties and behaviors.

*Result:* Theorem proving in logic programming enables the formal verification of program correctness through logical inference.

---

**Q2. [Unit IV | Topic: NLP | Type: Theory | Difficulty: Basic]**  
**Question:** What is Natural Language Processing (NLP) and how is logic programming applied in it?  

*Concept from scratch:* NLP is a subfield of artificial intelligence that deals with the interaction between computers and human language. It involves processing and analyzing large amounts of natural language data.  
*Application of logic programming:* Logic programming can be used in NLP for tasks such as parsing natural language sentences, representing semantic knowledge, and reasoning about language constructs. Prolog, in particular, is well-suited for implementing grammars and inference mechanisms in NLP applications.

*Result:* Logic programming plays a vital role in NLP by enabling efficient parsing and reasoning over natural language data.

---

### Section B: Computational & Applied Problems

**Q1. [Unit IV | Topic: Expert Systems | Type: Numericals | Difficulty: Intermediate]**  
**Question:** Describe how to implement a simple expert system using Prolog.  

*Concept from scratch:* An expert system is a computer program that mimics the decision-making ability of a human expert. In Prolog, an expert system can be implemented using facts, rules, and queries to infer conclusions based on user input.  

*Step 1 — Define the knowledge base:*  

```prolog
% Facts
symptom(fever).
symptom(cough).
symptom(headache).

% Rules
flu(X) :- symptom(fever), symptom(cough), symptom(headache).
cold(X) :- symptom(cough), \+ symptom(fever).
```

*Step 2 — Implement the query mechanism:*  

```prolog
diagnose(Disease) :- flu(Disease).
diagnose(Disease) :- cold(Disease).
```

*Result:* The Prolog code outlines a simple expert system that diagnoses flu or cold based on symptoms.

---

**Q2. [Unit IV | Topic: Constraint Satisfaction | Type: Numericals | Difficulty: Intermediate]**  
**Question:** Design a Prolog program that solves a simple constraint satisfaction problem.  

*Concept from scratch:* Constraint satisfaction problems involve finding values for variables that satisfy a set of constraints. In Prolog, this can be achieved using rules and predicates.  

*Step 1 — Define the variables and constraints:*  

```prolog
% Variables
domain(X) :- X in 1..10.
domain(Y) :- Y in 1..10.

% Constraints
constraint(X, Y) :- X + Y #= 10.
```

*Step 2 — Solve the problem using backtracking:*  

```prolog
solve(X, Y) :- domain(X), domain(Y), constraint(X, Y).
```

*Result:* The Prolog program defines a constraint satisfaction problem where it finds values for `X` and `Y` that satisfy the equation `X + Y = 10`.

---

### Section C: Advanced Theory & Numericals

**Q1. [Unit IV | Topic: Implementation of Logic Programs | Type: Theory | Difficulty: Advanced]**  
**Question:** Discuss the challenges and techniques in implementing logic programs effectively.  

*Concept from scratch:* Implementing logic programs presents challenges such as efficiency, handling large search spaces, and ensuring correctness.  
*Techniques to address challenges include:*  

1. **Optimization Techniques**: Using indexing and memoization to speed up query resolution.

2. **Modular Design**: Structuring programs in a modular fashion for better maintainability and reusability.

3. **Debugging Tools**: Employing debugging tools and techniques specific to logic programming for effective troubleshooting.

*Result:* Effective implementation of logic programs requires optimization techniques, modular design, and debugging tools to overcome challenges.

---

**Q2. [Unit IV | Topic: Constraint Logic Programming | Type: Theory | Difficulty: Advanced]**  
**Question:** Examine the principles of Constraint Logic Programming and provide examples of constraint satisfaction and propagation.  

*Concept from scratch:* Constraint Logic Programming (CLP) extends logic programming by incorporating constraints, allowing for more expressive problem-solving capabilities.  
*Principles include:*  

1. **Constraint Satisfaction**: Finding variable assignments that satisfy all constraints.

2. **Constraint Propagation**: Reducing the search space by inferring variable values based on constraints.

*Example of constraint satisfaction in CLP:*  

```prolog
% Define constraints
solve(X, Y) :- X + Y #= 10, X #>= 1, Y #=< 5.
```

*Result:* CLP principles enable solving complex problems through constraint satisfaction and propagation, enhancing the expressiveness of logic programming.