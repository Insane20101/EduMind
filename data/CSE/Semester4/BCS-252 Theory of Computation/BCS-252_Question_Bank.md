# BCS-252 - Theory of Computation
## Complete Unit-Wise Question Bank (Theory + Numericals, Basic → Advanced)

> **Course:** BCS-252 - Theory of Computation  
> **Credits:** 4  
> **Coverage:** Strictly mapped to the syllabus.

## Syllabus Reference
- UNIT-I: Alphabets, strings, languages, automata and grammars. DFA - formal definition, transition graph/table. NFA, NFA with epsilon transitions, equivalence of NFA and DFA, minimization of finite automata, Myhill-Nerode theorem.
- UNIT-II: Regular Expressions: definition, operators, algebraic laws, Kleene's theorem, RE to FA and back, Arden theorem, non-regular languages, pumping lemma, closure/decision properties, Moore and Mealy machines.
- UNIT-III: Context Free Grammar and Languages: derivation, derivation trees, ambiguity, normal forms (CNF, GNF), closure/decision properties, pumping lemma for CFL. Push Down Automata: description, acceptance by final state/empty stack, equivalence of PDA and CFG.
- UNIT-IV: Turing Machines: basic model, instantaneous description, language acceptance, variants, universal TM, Church's thesis, recursive and recursively enumerable languages, halting problem, undecidability, Post Correspondence Problem.

## UNIT I — Automata and Grammars
### Section A: Definitions & Concept Questions (Basic, 2–3 Marks)

1. **[Unit I | Topic: Alphabets | Type: Theory | Difficulty: Basic]**  
   Define the terms "alphabet," "string," and "language" in the context of formal languages.

2. **[Unit I | Topic: DFA | Type: Theory | Difficulty: Basic]**  
   What is a Deterministic Finite Automaton (DFA)? Describe its formal definition.

3. **[Unit I | Topic: NFA | Type: Theory | Difficulty: Basic]**  
   Explain the difference between a Non-deterministic Finite Automaton (NFA) and a DFA.

### Section B: Computational & Applied Problems (Intermediate, 7 Marks)

1. **[Unit I | Topic: Transition Graph | Type: Numerical | Difficulty: Intermediate]**  
   Construct a transition graph for a DFA that accepts the language of strings over {0, 1} that contain an even number of 1's.

2. **[Unit I | Topic: NFA to DFA | Type: Numerical | Difficulty: Intermediate]**  
   Convert the given NFA (with epsilon transitions) into its equivalent DFA.

### Section C: Advanced Theory & Numericals

1. **[Unit I | Topic: Myhill-Nerode Theorem | Type: Theory | Difficulty: Advanced]**  
   State and explain the Myhill-Nerode theorem and its significance in determining language regularity.

2. **[Unit I | Topic: Minimization of Finite Automata | Type: Numerical | Difficulty: Advanced]**  
   Given a DFA, perform the minimization process and provide the equivalent minimal DFA.

## UNIT II — Regular Expressions and Machines
### Section A: Definitions & Concept Questions (Basic, 2–3 Marks)

1. **[Unit II | Topic: Regular Expression | Type: Theory | Difficulty: Basic]**  
   Define a regular expression and list its operators.

2. **[Unit II | Topic: Kleene's Theorem | Type: Theory | Difficulty: Basic]**  
   What is Kleene's theorem, and what does it state about regular languages?

### Section B: Computational & Applied Problems (Intermediate, 7 Marks)

1. **[Unit II | Topic: RE to FA | Type: Numerical | Difficulty: Intermediate]**  
   Convert the regular expression (0|1)*01(0|1)* into a finite automaton.

2. **[Unit II | Topic: Pumping Lemma | Type: Numerical | Difficulty: Intermediate]**  
   Use the pumping lemma to prove that the language L = {a^n b^n | n ≥ 0} is not regular.

### Section C: Advanced Theory & Numericals

1. **[Unit II | Topic: Moore and Mealy Machines | Type: Theory | Difficulty: Advanced]**  
   Compare and contrast Moore machines and Mealy machines in terms of their output generation.

2. **[Unit II | Topic: Closure Properties | Type: Numerical | Difficulty: Advanced]**  
   Demonstrate the closure properties of regular languages with examples.

## UNIT III — Context Free Grammar and Push Down Automata
### Section A: Definitions & Concept Questions (Basic, 2–3 Marks)

1. **[Unit III | Topic: Context Free Grammar | Type: Theory | Difficulty: Basic]**  
   Define Context Free Grammar (CFG) and explain its components.

2. **[Unit III | Topic: Ambiguity | Type: Theory | Difficulty: Basic]**  
   What is ambiguity in context-free grammars? Provide an example.

### Section B: Computational & Applied Problems (Intermediate, 7 Marks)

1. **[Unit III | Topic: Derivation Trees | Type: Numerical | Difficulty: Intermediate]**  
   Construct a derivation tree for the string "ab" using the CFG S → aSb | ε.

2. **[Unit III | Topic: Pumping Lemma for CFL | Type: Numerical | Difficulty: Intermediate]**  
   Use the pumping lemma for context-free languages to show that the language L = {a^n b^n c^n | n ≥ 0} is not context-free.

### Section C: Advanced Theory & Numericals

1. **[Unit III | Topic: PDA | Type: Theory | Difficulty: Advanced]**  
   Explain the concept of Push Down Automata (PDA) and how it accepts context-free languages.

2. **[Unit III | Topic: Equivalence of PDA and CFG | Type: Numerical | Difficulty: Advanced]**  
   Prove the equivalence of PDAs and context-free grammars.

## UNIT IV — Turing Machines and Computability
### Section A: Definitions & Concept Questions (Basic, 2–3 Marks)

1. **[Unit IV | Topic: Turing Machine | Type: Theory | Difficulty: Basic]**  
   Define a Turing machine and describe its components.

2. **[Unit IV | Topic: Language Acceptance | Type: Theory | Difficulty: Basic]**  
   What does it mean for a Turing machine to accept a language?

### Section B: Computational & Applied Problems (Intermediate, 7 Marks)

1. **[Unit IV | Topic: Variants of Turing Machines | Type: Numerical | Difficulty: Intermediate]**  
   Describe the differences between a single-tape and a multi-tape Turing machine.

2. **[Unit IV | Topic: Halting Problem | Type: Numerical | Difficulty: Intermediate]**  
   Explain the halting problem and why it is undecidable.

### Section C: Advanced Theory & Numericals

1. **[Unit IV | Topic: Church's Thesis | Type: Theory | Difficulty: Advanced]**  
   Discuss Church's thesis and its implications in the theory of computation.

2. **[Unit IV | Topic: Post Correspondence Problem | Type: Numerical | Difficulty: Advanced]**  
   Provide an example of the Post Correspondence Problem and explain its undecidability.

## Coverage Summary
| Unit | Topics Fully Covered | Question Types | Difficulty Range |
|------|---------------------|----------------|------------------|
| I    | Automata, DFA, NFA, Myhill-Nerode theorem | Theory, Numerical | Basic, Intermediate, Advanced |
| II   | Regular Expressions, Pumping Lemma, Moore and Mealy machines | Theory, Numerical | Basic, Intermediate, Advanced |
| III  | Context Free Grammar, PDA, Pumping Lemma for CFL | Theory, Numerical | Basic, Intermediate, Advanced |
| IV   | Turing Machines, Halting Problem, Church's thesis | Theory, Numerical | Basic, Intermediate, Advanced |