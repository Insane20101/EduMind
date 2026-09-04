# BCS-302 - Principles of Compiler Design
## Complete Unit-Wise Question Bank (Theory + Numericals, Basic → Advanced)

> **Course:** BCS-302 - Principles of Compiler Design  
> **Credits:** 5  
> **Coverage:** Strictly mapped to the syllabus.

## Syllabus Reference
### UNIT-I
Compiler Structure: analysis-synthesis model, phases of a compiler, tool-based approach. Lexical Analysis: interface with input/parser/symbol table, tokens, lexemes, patterns, error reporting, regular definitions, transition diagrams, LEX.  
### UNIT-II
Syntax Analysis: context free grammars, ambiguity, associativity, precedence, top-down/recursive descent parsing, predictive parsing, bottom-up parsing, operator precedence grammars, LR parsers (SLR, LALR, LR), YACC.  
### UNIT-III
Syntax Directed Definitions: inherited/synthesized attributes, dependency graph, evaluation order, L- and S-attributed definitions. Type Checking: type system, type expressions, type conversion, polymorphic functions. Intermediate Code Generation.  
### UNIT-IV
Symbol Table Management, Runtime Environments, storage organization/allocation strategies, parameter passing. Code Optimization: peephole optimization, optimization of basic blocks and loops, global dataflow analysis, introduction to code generation.  

## UNIT I — Compiler Structure and Lexical Analysis
### Section A: Definitions & Concept Questions (Basic, 2–3 Marks)

1. **[Unit I | Topic: Compiler Structure | Type: Theory | Difficulty: Basic]**  
   Define the analysis-synthesis model in compiler design.

2. **[Unit I | Topic: Lexical Analysis | Type: Theory | Difficulty: Basic]**  
   What are tokens and lexemes? Provide examples.

3. **[Unit I | Topic: Error Reporting | Type: Theory | Difficulty: Basic]**  
   Explain the significance of error reporting in lexical analysis.

### Section B: Computational & Applied Problems (Intermediate, 7 Marks)

1. **[Unit I | Topic: Transition Diagrams | Type: Numericals | Difficulty: Intermediate]**  
   Construct a transition diagram for a lexical analyzer that recognizes identifiers and keywords in a programming language.

2. **[Unit I | Topic: Regular Definitions | Type: Numericals | Difficulty: Intermediate]**  
   Write the regular definition for a simple arithmetic expression containing integers and operators (+, -, *, /).

### Section C: Advanced Theory & Numericals

1. **[Unit I | Topic: Tool-based Approach | Type: Theory | Difficulty: Advanced]**  
   Discuss the tool-based approach in compiler design and its advantages.

2. **[Unit I | Topic: LEX | Type: Numericals | Difficulty: Advanced]**  
   Using LEX, write a specification for a lexical analyzer that can tokenize a simple programming language syntax.

## UNIT II — Syntax Analysis
### Section A: Definitions & Concept Questions (Basic, 2–3 Marks)

1. **[Unit II | Topic: Context Free Grammars | Type: Theory | Difficulty: Basic]**  
   What is a context-free grammar? Provide a simple example.

2. **[Unit II | Topic: Ambiguity | Type: Theory | Difficulty: Basic]**  
   Define ambiguity in the context of syntax analysis.

### Section B: Computational & Applied Problems (Intermediate, 7 Marks)

1. **[Unit II | Topic: Parsing Techniques | Type: Numericals | Difficulty: Intermediate]**  
   Construct a parse tree for the expression `a + b * c` using a suitable grammar.

2. **[Unit II | Topic: LR Parsers | Type: Numericals | Difficulty: Intermediate]**  
   Describe the steps to construct an SLR parser for a given grammar and demonstrate with an example.

### Section C: Advanced Theory & Numericals

1. **[Unit II | Topic: Operator Precedence Grammars | Type: Theory | Difficulty: Advanced]**  
   Explain operator precedence parsing with an example.

2. **[Unit II | Topic: YACC | Type: Numericals | Difficulty: Advanced]**  
   Write a YACC specification for a calculator that supports addition and multiplication.

## UNIT III — Syntax Directed Definitions and Type Checking
### Section A: Definitions & Concept Questions (Basic, 2–3 Marks)

1. **[Unit III | Topic: Inherited Attributes | Type: Theory | Difficulty: Basic]**  
   What are inherited attributes? Provide an example of their use.

2. **[Unit III | Topic: Type Checking | Type: Theory | Difficulty: Basic]**  
   Define type checking and its importance in compilers.

### Section B: Computational & Applied Problems (Intermediate, 7 Marks)

1. **[Unit III | Topic: Dependency Graph | Type: Numericals | Difficulty: Intermediate]**  
   Given a set of synthesized attributes, create a dependency graph and explain its significance.

2. **[Unit III | Topic: Type Conversion | Type: Numericals | Difficulty: Intermediate]**  
   Illustrate type conversion with examples in a programming language.

### Section C: Advanced Theory & Numericals

1. **[Unit III | Topic: Intermediate Code Generation | Type: Theory | Difficulty: Advanced]**  
   Discuss different intermediate representations used in compilers.

2. **[Unit III | Topic: Polymorphic Functions | Type: Numericals | Difficulty: Advanced]**  
   Explain polymorphic functions and demonstrate type checking for a polymorphic function example.

## UNIT IV — Symbol Table Management and Code Optimization
### Section A: Definitions & Concept Questions (Basic, 2–3 Marks)

1. **[Unit IV | Topic: Symbol Table | Type: Theory | Difficulty: Basic]**  
   Define a symbol table and its role in a compiler.

2. **[Unit IV | Topic: Runtime Environments | Type: Theory | Difficulty: Basic]**  
   What is a runtime environment? Describe its components.

### Section B: Computational & Applied Problems (Intermediate, 7 Marks)

1. **[Unit IV | Topic: Storage Allocation | Type: Numericals | Difficulty: Intermediate]**  
   Explain different storage allocation strategies with examples.

2. **[Unit IV | Topic: Parameter Passing | Type: Numericals | Difficulty: Intermediate]**  
   Compare and contrast different parameter passing techniques.

### Section C: Advanced Theory & Numericals

1. **[Unit IV | Topic: Code Optimization | Type: Theory | Difficulty: Advanced]**  
   What are peephole optimizations? Discuss their effectiveness with examples.

2. **[Unit IV | Topic: Global Dataflow Analysis | Type: Numericals | Difficulty: Advanced]**  
   Describe global dataflow analysis and provide an example of its application in optimization.

## Coverage Summary
| Unit | Topics Fully Covered                          | Question Types                     | Difficulty Range         |
|------|-----------------------------------------------|------------------------------------|--------------------------|
| I    | Compiler Structure, Lexical Analysis          | Definitions, Computational, Theory | Basic → Advanced         |
| II   | Syntax Analysis, Parsing Techniques            | Definitions, Computational, Theory | Basic → Advanced         |
| III  | Syntax Directed Definitions, Type Checking     | Definitions, Computational, Theory | Basic → Advanced         |
| IV   | Symbol Table Management, Code Optimization     | Definitions, Computational, Theory | Basic → Advanced         |