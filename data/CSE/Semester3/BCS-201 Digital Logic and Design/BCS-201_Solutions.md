# BCS-201 - Digital Logic and Design
## Detailed Step-Wise Solutions — Units I–IV (Combined)

## Detailed Step-Wise Solutions — UNIT I: Binary Codes and Boolean Algebra
### Section A: Definitions & Concept Questions

**Q1. [Unit I | Topic: Binary Codes | Type: Theory | Difficulty: Basic]**  
**Question:** Define weighted and non-weighted binary codes with examples.  

*Concept from scratch:*  
Binary codes are numerical representations of data in binary form (0s and 1s). They can be classified into two types: weighted and non-weighted binary codes. 

- **Weighted Codes:** In weighted codes, each position of a digit in the binary number has a specific weight associated with it. The value of the code is determined by the sum of the weights of the positions that have a '1'. An example of a weighted code is Binary Coded Decimal (BCD), where the weights are 8, 4, 2, and 1 for a 4-bit representation.

- **Non-Weighted Codes:** In non-weighted codes, the positions do not have a specific weight. The value is assigned arbitrarily and does not depend on the position. An example is the Gray Code, where two successive values differ in only one bit.

*Step 1 — Identify the codes:*  
- Weighted Code Example: BCD (0000 to 1001 for decimal 0 to 9)
- Non-Weighted Code Example: Gray Code (0000, 0001, 0011, 0010...)

*Result:*  
Weighted codes (e.g., BCD) have specific weights; non-weighted codes (e.g., Gray Code) do not.

---

**Q2. [Unit I | Topic: Binary Arithmetic | Type: Theory | Difficulty: Basic]**  
**Question:** Explain binary addition and subtraction with suitable examples.  

*Concept from scratch:*  
Binary arithmetic is similar to decimal arithmetic but operates on binary numbers. The basic operations include addition and subtraction.

- **Binary Addition:** The rules for binary addition are as follows:
  - 0 + 0 = 0
  - 0 + 1 = 1
  - 1 + 0 = 1
  - 1 + 1 = 10 (0 with a carry of 1)

*Step 1 — Example:*  
Let’s add two binary numbers:  
  1011 (11 in decimal)  
+  1101 (13 in decimal)  

----------------  
  11000 (24 in decimal)

- **Binary Subtraction:** The rules for binary subtraction are as follows:
  - 0 - 0 = 0
  - 1 - 0 = 1
  - 1 - 1 = 0
  - 0 - 1 requires borrowing.

*Step 1 — Example:*  
Subtracting 1010 from 1100:  
  1100 (12 in decimal)  
-  1010 (10 in decimal)  

------------------  
  0010 (2 in decimal)  

*Result:*  
Binary addition and subtraction are performed using similar rules to decimal arithmetic, with special attention to carrying and borrowing.

---

**Q3. [Unit I | Topic: Conversion Algorithms | Type: Theory | Difficulty: Basic]**  
**Question:** Describe the procedure to convert binary numbers to decimal.  

*Concept from scratch:*  
To convert a binary number (base-2) to decimal (base-10), each bit is multiplied by 2 raised to the power of its position, counting from right to left, starting at zero.

*Step 1 — Procedure:*  

1. Write the binary number.

2. Assign powers of 2 to each position in the binary number.

3. Multiply each bit by its corresponding power of 2.

4. Sum all the results.

*Step 2 — Example:*  
Convert 1011 to decimal:  
- Positions: 3  2  1  0  
- Binary:   1  0  1  1  
- Calculation:  
  - (1 * 2^3) + (0 * 2^2) + (1 * 2^1) + (1 * 2^0)  
  - = 8 + 0 + 2 + 1 = 11

*Result:*  
The binary number 1011 converts to decimal 11 through multiplication by powers of 2 and summation.

### Section B: Computational & Applied Problems

**Q1. [Unit I | Topic: Error Detecting Codes | Type: Theory | Difficulty: Intermediate]**  
**Question:** Given a binary number, explain how to detect errors using a parity bit.  

*Concept from scratch:*  
A parity bit is a bit added to data to ensure that the total number of 1s is even (even parity) or odd (odd parity). It helps in detecting errors during transmission.

*Step 1 — Even Parity Example:*  
Consider the binary number 1101001 (has 5 ones, which is odd).  
To make it even, add a parity bit of 1: 11010011.

*Step 2 — Error Detection:*  
When the data is received, count the number of 1s.  
- If the count is odd, an error has occurred.
- If the count is even, the data is assumed correct.

*Result:*  
Parity bits can detect single-bit errors in transmitted binary numbers by ensuring the total number of 1s is even or odd.

---

**Q2. [Unit I | Topic: Canonical Boolean Expressions | Type: Theory | Difficulty: Intermediate]**  
**Question:** Convert the given truth table into its canonical form.  

*Concept from scratch:*  
Canonical forms are standardized representations of Boolean functions. The Sum of Products (SOP) canonical form lists all minterms for which the output is true (1).

*Step 1 — Identify Minterms:*  
Consider a truth table with inputs A, B, C and an output F. Assuming F is 1 for minterms 1, 3, and 5:  
- Minterm 1: A'B'C  
- Minterm 3: A'BC  
- Minterm 5: AB'C  

*Step 2 — Write the SOP:*  
F(A, B, C) = A'B'C + A'BC + AB'C

*Result:*  
The canonical SOP form of the Boolean expression from the truth table is F(A, B, C) = A'B'C + A'BC + AB'C.

### Section C: Advanced Theory & Numericals

**Q1. [Unit I | Topic: Truth Tables | Type: Theory | Difficulty: Advanced]**  
**Question:** Derive the truth table for the given Boolean expression: A'B + AB'.  

*Concept from scratch:*  
A truth table lists all possible values of input variables and the corresponding output for a given Boolean expression.

*Step 1 — Identify Variables:*  
The expression A'B + AB' involves two variables: A and B.

*Step 2 — List All Combinations:*  
There are four combinations (00, 01, 10, 11).

| A | B | A' | B' | A'B | AB' | A'B + AB' |
|---|---|----|----|-----|-----|-----------|
| 0 | 0 |  1 |  1 |  0  |  0  |     0     |
| 0 | 1 |  1 |  0 |  1  |  0  |     1     |
| 1 | 0 |  0 |  1 |  0  |  1  |     1     |
| 1 | 1 |  0 |  0 |  0  |  0  |     0     |

*Step 3 — Result:*  
The truth table for A'B + AB' is completed, with outputs showing the results for each combination of A and B.

---

**Q2. [Unit I | Topic: Binary Arithmetic | Type: Theory | Difficulty: Advanced]**  
**Question:** Perform binary addition for the binary numbers 1101 and 1011.  

*Concept from scratch:*  
Binary addition follows specific rules, similar to decimal addition, but with carries based on powers of 2.

*Step 1 — Add the numbers:*  
Align the binary numbers:  

```
  1101
+ 1011
------
```

*Step 2 — Perform addition from right to left:*  
- 1 + 1 = 10 (write down 0, carry 1)  
- 0 + 1 + 1 (carry) = 10 (write down 0, carry 1)  
- 1 + 0 + 1 (carry) = 10 (write down 0, carry 1)  
- 1 + 1 + 1 (carry) = 11 (write down 1, carry 1)  

*Step 3 — Final carry:*  

```
  1101
+ 1011
------
 11000
```

*Result:*  
The binary addition of 1101 and 1011 results in 11000.

---

## Detailed Step-Wise Solutions — UNIT II: Combinational Logic Design
### Section A: Definitions & Concept Questions

**Q1. [Unit II | Topic: K-Map Reduction | Type: Theory | Difficulty: Basic]**  
**Question:** What is a Karnaugh Map and how is it used for simplifying Boolean expressions?  

*Concept from scratch:*  
A Karnaugh Map (K-map) is a visual method for simplifying Boolean expressions without the need for algebraic manipulation. It organizes truth values of a function into a grid format, making it easier to identify common patterns.

*Step 1 — Constructing a K-map:*  
For a 2-variable function, the K-map is a 2x2 grid; for 3 variables, it’s a 2x4 grid, and for 4 variables, it’s a 4x4 grid.

*Step 2 — Filling the K-map:*  
Each cell in the K-map corresponds to a minterm of the function. Fill in the cells with 1s and 0s according to the truth table.

*Step 3 — Grouping:*  
Adjacent cells with 1s can be grouped in powers of two (1, 2, 4, 8...), which helps in deriving the simplified Boolean expression.

*Result:*  
Karnaugh Maps simplify Boolean expressions by allowing visual grouping of minterms, leading to reduced expressions.

---

**Q2. [Unit II | Topic: Adders/Subtractors | Type: Theory | Difficulty: Basic]**  
**Question:** Define a half adder and full adder. What are their differences?  

*Concept from scratch:*  
Adders are digital circuits that perform addition of binary numbers. A half adder adds two single-bit binary numbers, while a full adder adds three bits.

*Step 1 — Half Adder:*  
A half adder has two inputs (A and B) and two outputs (Sum and Carry).  
- **Sum = A ⊕ B** (XOR operation)  
- **Carry = A AND B**  

*Step 2 — Full Adder:*  
A full adder has three inputs (A, B, and Carry-In) and two outputs (Sum and Carry-Out).  
- **Sum = A ⊕ B ⊕ Carry-In**  
- **Carry-Out = (A AND B) OR (Carry-In AND (A ⊕ B))**  

*Step 3 — Differences:*  
- Half adder cannot handle carry input; full adder can handle it.
- Half adder has 2 inputs; full adder has 3 inputs.

*Result:*  
A half adder adds two bits without carry input, while a full adder adds three bits, including carry input.

### Section B: Computational & Applied Problems

**Q1. [Unit II | Topic: Carry Look-Ahead Adder | Type: Theory | Difficulty: Intermediate]**  
**Question:** Design a carry look-ahead adder for 4-bit binary numbers.  

*Concept from scratch:*  
A carry look-ahead adder improves speed by calculating carry signals in advance rather than waiting for them to propagate through each bit.

*Step 1 — Define Inputs and Outputs:*  
- Inputs: A3 A2 A1 A0 and B3 B2 B1 B0  
- Outputs: S3 S2 S1 S0 (sum) and C4 (carry out)

*Step 2 — Generate Propagate and Generate Signals:*  
- Propagate (P) = A XOR B  
- Generate (G) = A AND B  

*Step 3 — Carry Generation:*  
Using the propagate and generate signals:  
- C1 = G0 + P0*C0  
- C2 = G1 + P1*C1  
- C3 = G2 + P2*C2  
- C4 = G3 + P3*C3  

*Step 4 — Sum Calculation:*  
Each sum bit is calculated as:  
S0 = P0 XOR C0  
S1 = P1 XOR C1  
S2 = P2 XOR C2  
S3 = P3 XOR C3  

*Result:*  
A 4-bit carry look-ahead adder is designed using propagate and generate signals to calculate carry outputs rapidly.

---

**Q2. [Unit II | Topic: Code Converters | Type: Theory | Difficulty: Intermediate]**  
**Question:** Convert the binary number 1011 to its Gray code equivalent.  

*Concept from scratch:*  
Gray code is a binary numeral system where two successive values differ in only one bit. The conversion from binary to Gray code can be done using a simple rule.

*Step 1 — Conversion Rule:*  
- The most significant bit (MSB) of the Gray code is the same as the MSB of the binary code.  
- Each subsequent bit is obtained by XORing the current bit with the previous bit of the binary number.

*Step 2 — Convert 1011 to Gray Code:*  
- MSB: G3 = B3 = 1  
- G2 = B3 XOR B2 = 1 XOR 0 = 1  
- G1 = B2 XOR B1 = 0 XOR 1 = 1  
- G0 = B1 XOR B0 = 1 XOR 1 = 0  

Thus, Gray code for 1011 is 1110.

*Result:*  
The binary number 1011 converts to Gray code 1110.

### Section C: Advanced Theory & Numericals

**Q1. [Unit II | Topic: Magnitude Comparator | Type: Theory | Difficulty: Advanced]**  
**Question:** Design a 2-bit magnitude comparator using logic gates.  

*Concept from scratch:*  
A magnitude comparator is a combinational circuit that compares two binary numbers and determines their relationship (A>B, A<B, or A=B).

*Step 1 — Define Inputs and Outputs:*  
- Inputs: A1 A0 (first number) and B1 B0 (second number)  
- Outputs: A>B, A<B, A=B  

*Step 2 — Logic Implementation:*  

1. A=B if A1 = B1 and A0 = B0. This can be implemented using an AND gate after checking for equality.

2. A>B if A1 > B1 or (A1 = B1 and A0 > B0). Use OR and AND gates to construct this logic.

3. A<B if B1 > A1 or (B1 = A1 and B0 > A0). Similar to A>B, this can be implemented using OR and AND gates.

*Step 3 — Circuit Design:*  
Logic gates will be used to connect these comparisons appropriately.

*Result:*  
A 2-bit magnitude comparator is designed using AND and OR gates to compare inputs and yield outputs indicating their magnitude relationship.

---

**Q2. [Unit II | Topic: Multiplexers | Type: Theory | Difficulty: Advanced]**  
**Question:** Implement a 4-to-1 multiplexer using basic gates and write its truth table.  

*Concept from scratch:*  
A multiplexer (MUX) is a device that selects one of many input signals and forwards the selected input to a single output line.

*Step 1 — Define Inputs and Outputs:*  
- Inputs: I0, I1, I2, I3 (data inputs)  
- Select Lines: S0, S1  
- Output: Y  

*Step 2 — Truth Table:*  
| S1 | S0 | Y (Output) |
|----|----|------------|
| 0  | 0  | I0         |
| 0  | 1  | I1         |
| 1  | 0  | I2         |
| 1  | 1  | I3         |

*Step 3 — Logic Implementation:*  
The output Y can be implemented using OR gates and AND gates:  
- Y = (I0 AND S1' AND S0') OR (I1 AND S1' AND S0) OR (I2 AND S1 AND S0') OR (I3 AND S1 AND S0).

*Result:*  
A 4-to-1 multiplexer is implemented using basic gates, with the truth table showing the output based on select lines.

---

## Detailed Step-Wise Solutions — UNIT III: Sequential Logic
### Section A: Definitions & Concept Questions

**Q1. [Unit III | Topic: Flip-Flops | Type: Theory | Difficulty: Basic]**  
**Question:** Explain the operation of an SR flip-flop.  

*Concept from scratch:*  
An SR flip-flop is a type of bistable multivibrator that has two inputs, S (Set) and R (Reset), and two outputs, Q and Q' (not Q).

*Step 1 — Functionality:*  
- When S = 1 and R = 0, Q is set to 1.  
- When S = 0 and R = 1, Q is reset to 0.  
- When S = 0 and R = 0, Q retains its previous state.  
- When S = 1 and R = 1, the state is considered invalid.

*Step 2 — Truth Table:*  
| S | R | Q | Q' |
|---|---|---|----|
| 0 | 0 | Q | Q' |
| 0 | 1 | 0 | 1  |
| 1 | 0 | 1 | 0  |
| 1 | 1 | X | X  |

*Result:*  
An SR flip-flop sets or resets output Q based on inputs S and R following specified rules, with an invalid state for both inputs high.

---

**Q2. [Unit III | Topic: Counters | Type: Theory | Difficulty: Basic]**  
**Question:** What is a binary counter? Describe its functioning.  

*Concept from scratch:*  
A binary counter is a digital device that counts in binary numbers. It increments or decrements its output based on clock pulses.

*Step 1 — Types of Binary Counters:*  
- **Asynchronous (Ripple) Counter:** Each flip-flop is triggered by the previous one.
- **Synchronous Counter:** All flip-flops are triggered simultaneously by the clock.

*Step 2 — Functioning of a 3-bit Asynchronous Counter:*  

1. The first flip-flop toggles on every clock pulse.

2. The second flip-flop toggles when the first flip-flop transitions from 1 to 0 (falling edge).

3. The third flip-flop toggles when both the first and second flip-flops transition from 1 to 0.

*Result:*  
Binary counters count in binary format, with asynchronous counters relying on the previous flip-flop's state for triggering.

### Section B: Computational & Applied Problems

**Q1. [Unit III | Topic: Ripple Counter | Type: Theory | Difficulty: Intermediate]**  
**Question:** Construct a 3-bit ripple counter and illustrate its state transition diagram.  

*Concept from scratch:*  
A 3-bit ripple counter counts from 0 to 7 in binary, using three flip-flops.

*Step 1 — Flip-Flop Configuration:*  
- Use three T flip-flops, where each flip-flop represents a bit.

*Step 2 — State Transition Diagram:*  
- State transitions for a 3-bit counter are as follows:

```
State:   000 → 001 → 010 → 011 → 100 → 101 → 110 → 111
Count:   0    1    2    3    4    5    6    7 
```

*Step 3 — Diagram Representation:*  
Draw arrows to represent the transitions between states.

*Result:*  
A 3-bit ripple counter is designed, counting from 0 to 7, with a state transition diagram illustrating its operation.

---

**Q2. [Unit III | Topic: Synchronous Counter | Type: Theory | Difficulty: Intermediate]**  
**Question:** Design a synchronous 4-bit counter using D flip-flops.  

*Concept from scratch:*  
A synchronous counter allows all flip-flops to be triggered by the same clock pulse, which improves speed and reliability.

*Step 1 — Define Inputs and Outputs:*  
- Inputs: Clock signal  
- Outputs: Q3, Q2, Q1, Q0 (4 bits)

*Step 2 — Flip-Flop Connection:*  

1. Connect the clock signal to all D flip-flops.

2. Implement logic to toggle the state of each flip-flop based on the required counting sequence.

*Step 3 — D Flip-Flop Logic:*  
- D0 = NOT(Q0)  
- D1 = Q0 XOR Q1  
- D2 = Q1 XOR Q2  
- D3 = Q2 XOR Q3  

*Result:*  
A synchronous 4-bit counter is designed using D flip-flops, with each flip-flop's D input determined by the previous states.

### Section C: Advanced Theory & Numericals

**Q1. [Unit III | Topic: Master-Slave Flip-Flop | Type: Theory | Difficulty: Advanced]**  
**Question:** Explain the working principle of a master-slave JK flip-flop.  

*Concept from scratch:*  
A master-slave JK flip-flop consists of two JK flip-flops connected in series, ensuring stable operation and avoiding race conditions.

*Step 1 — Operation:*  
- The master flip-flop receives the input and changes state on the clock's rising edge.
- The slave flip-flop, connected to the output of the master, changes its state on the falling edge of the clock.

*Step 2 — Truth Table:*  
| J | K | Q (Present) | Q (Next) |
|---|---|-------------|----------|
| 0 | 0 | 0           | 0        |
| 0 | 0 | 1           | 1        |
| 0 | 1 | 0           | 0        |
| 0 | 1 | 1           | 0        |
| 1 | 0 | 0           | 1        |
| 1 | 0 | 1           | 1        |
| 1 | 1 | 0           | 1        |
| 1 | 1 | 1           | 0        |

*Result:*  
A master-slave JK flip-flop operates in two stages, preventing race conditions and ensuring stable outputs based on J and K inputs.

---

**Q2. [Unit III | Topic: Design Procedure for Counters | Type: Theory | Difficulty: Advanced]**  
**Question:** Describe the design procedure for a BCD counter with appropriate examples.  

*Concept from scratch:*  
A Binary-Coded Decimal (BCD) counter counts from 0 to 9 (0000 to 1001 in binary) and then resets to 0.

*Step 1 — Define Requirements:*  
- The counter must count in BCD format.
- Use 4 flip-flops to represent 4 bits.

*Step 2 — State Transition Table:*  
| State | Binary | Output |
|-------|--------|--------|
| 0     | 0000   | 0      |
| 1     | 0001   | 1      |
| 2     | 0010   | 2      |
| 3     | 0011   | 3      |
| 4     | 0100   | 4      |
| 5     | 0101   | 5      |
| 6     | 0110   | 6      |
| 7     | 0111   | 7      |
| 8     | 1000   | 8      |
| 9     | 1001   | 9      |
| 10    | 1010   | Reset to 0 |

*Step 3 — Logic Implementation:*  
Use combinational logic to reset the counter when it reaches 1010.

*Result:*  
The design procedure for a BCD counter includes defining states, constructing a transition table, and implementing logic for resetting after reaching 9.

---

## Detailed Step-Wise Solutions — UNIT IV: Registers and Memory Units
### Section A: Definitions & Concept Questions

**Q1. [Unit IV | Topic: Shift Registers | Type: Theory | Difficulty: Basic]**  
**Question:** Define a shift register and explain its types.  

*Concept from scratch:*  
A shift register is a sequential circuit that shifts its binary data in a serial or parallel manner through its flip-flops.

*Step 1 — Types of Shift Registers:*  

1. **Serial-In Serial-Out (SISO):** Data is input and output serially.

2. **Serial-In Parallel-Out (SIPO):** Data is input serially but output in parallel.

3. **Parallel-In Serial-Out (PISO):** Data is input in parallel and output serially.

4. **Parallel-In Parallel-Out (PIPO):** Data is input and output in parallel.

*Result:*  
Shift registers are classified based on their data input and output methods, and they facilitate data storage and manipulation.

---

**Q2. [Unit IV | Topic: Memory Units | Type: Theory | Difficulty: Basic]**  
**Question:** What is the difference between RAM and ROM?  

*Concept from scratch:*  
RAM (Random Access Memory) and ROM (Read-Only Memory) are two types of memory used in computers.

*Step 1 — RAM Characteristics:*  
- **Volatile Memory:** Loses data when power is off.
- **Read and Write:** Data can be read from and written to RAM.
- **Used for Temporary Storage:** Stores data and programs that the CPU is currently using.

*Step 2 — ROM Characteristics:*  
- **Non-Volatile Memory:** Retains data even when power is off.
- **Read-Only:** Generally cannot be written to, except in certain types (like EEPROM).
- **Used for Permanent Storage:** Stores firmware or software that will not change.

*Result:*  
RAM is volatile and read-write memory, while ROM is non-volatile and primarily read-only.

### Section B: Computational & Applied Problems

**Q1. [Unit IV | Topic: Registers with Parallel Load | Type: Theory | Difficulty: Intermediate]**  
**Question:** Design a 4-bit register with parallel load capability and explain its operation.  

*Concept from scratch:*  
A register with parallel load allows data to be loaded into the register simultaneously across all bits.

*Step 1 — Define Inputs and Outputs:*  
- Inputs: D3, D2, D1, D0 (data inputs), Load (control signal)  
- Outputs: Q3, Q2, Q1, Q0 (register outputs)

*Step 2 — Flip-Flop Configuration:*  
- Use 4 D flip-flops, with each flip-flop corresponding to one bit of the data.

*Step 3 — Logic Implementation:*  
- When Load = 1, the data inputs D3, D2, D1, D0 are loaded into the flip-flops.  
- When Load = 0, the outputs retain their previous states.

*Result:*  
A 4-bit register with parallel load is designed using D flip-flops, allowing simultaneous data loading.

---

**Q2. [Unit IV | Topic: Memory Unit | Type: Theory | Difficulty: Intermediate]**  
**Question:** Describe the working of a PROM and how it differs from EPROM.  

*Concept from scratch:*  
A Programmable Read-Only Memory (PROM) is a type of non-volatile memory that can be programmed once after manufacturing.

*Step 1 — Working of PROM:*  
- PROM is programmed using a special device that blows fuses within the chip.
- Once programmed, the data is permanent and cannot be altered.

*Step 2 — Working of EPROM:*  
- EPROM (Erasable Programmable Read-Only Memory) can be erased by exposing it to UV light.
- After erasure, the EPROM can be reprogrammed multiple times.

*Result:*  
PROM is a one-time programmable memory, while EPROM can be erased and reprogrammed, offering more flexibility.

### Section C: Advanced Theory & Numericals

**Q1. [Unit IV | Topic: Reduction of State Tables | Type: Theory | Difficulty: Advanced]**  
**Question:** Given a state transition table, perform state reduction and provide the minimized table.  

*Concept from scratch:*  
State reduction is the process of minimizing the number of states in a state machine while preserving its functionality.

*Step 1 — Analyze State Transitions:*  
Identify equivalent states in the state transition table that produce the same outputs and transitions.

*Step 2 — Merge Equivalent States:*  
Combine the equivalent states into single states and update the transitions accordingly.

*Step 3 — Generate Minimized Table:*  
Create a new state transition table reflecting the reduced number of states.

*Result:*  
The minimized state transition table is produced by merging equivalent states, leading to a more efficient state machine.

---

**Q2. [Unit IV | Topic: Race-Free State Assignment | Type: Theory | Difficulty: Advanced]**  
**Question:** Explain the concept of race-free state assignment with an example.  

*Concept from scratch:*  
Race-free state assignment refers to assigning binary values to states in a state machine to avoid race conditions, ensuring stable transitions.

*Step 1 — Identify Potential Races:*  
Analyze the state transitions to identify conditions where multiple transitions could occur simultaneously, potentially leading to instability.

*Step 2 — Assign Binary Values:*  
Assign binary codes to states in such a way that no two states that can transition into each other can have values that differ in more than one bit (this is known as Hamming distance).

*Step 3 — Example:*  
Consider three states A, B, and C, where A transitions to B and C. Assign values:
- A = 00
- B = 01
- C = 10  

This assignment prevents races, as the maximum Hamming distance between states is 1.

*Result:*  
Race-free state assignment ensures stable operation of state machines by carefully assigning binary values to states that prevent simultaneous transitions.

--- 

This completes the detailed step-wise solutions for the entire question bank for BCS-201 - Digital Logic and Design. Each question is addressed with a clear structure, ensuring clarity and completeness in the explanations.