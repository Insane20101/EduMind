# BCS-401 - Fault Tolerance Analysis
## Complete Unit-Wise Question Bank (Theory + Numericals, Basic → Advanced)

> **Course:** BCS-401 - Fault Tolerance Analysis  
> **Credits:** 4  
> **Coverage:** Strictly mapped to the syllabus.

## Syllabus Reference

1. Fault Classification, types of redundancy, basic measures of fault tolerance, failure rate, reliability, MTTF, canonical/resilient structures, reliability evaluation techniques, processor-level techniques, Byzantine failures.

2. Fault Tolerant Design: N-Modular Redundancy, error correcting codes, dynamic/hybrid/self-purging redundancy, Sift-out Modular Redundancy, Triple Modular Redundancy and reconfiguration.

3. Information Redundancy Coding, resilient disk systems, data replication, algorithm-based fault tolerance; fault-tolerant networks, resilience measures, fault-tolerant routing; software fault tolerance - N-version programming, recovery blocks, exception handling.

4. Checkpointing: levels, optimal checkpointing, cache-aided rollback recovery, checkpointing in distributed/shared-memory/real-time systems; fault detection in cryptographic systems.

## UNIT I — Fault Classification and Reliability Measures
### Section A: Definitions & Concept Questions (Basic, 2–3 Marks)

1. **[Unit I | Topic: Fault Classification | Type: Theory | Difficulty: Basic]**  
   Define fault classification and list its main categories.

2. **[Unit I | Topic: Redundancy Types | Type: Theory | Difficulty: Basic]**  
   Explain the different types of redundancy used in fault tolerance.

3. **[Unit I | Topic: MTTF | Type: Theory | Difficulty: Basic]**  
   What is Mean Time To Failure (MTTF) and why is it important in reliability analysis?

### Section B: Computational & Applied Problems (Intermediate, 7 Marks)

1. **[Unit I | Topic: Reliability Evaluation Techniques | Type: Numerical | Difficulty: Intermediate]**  
   Given a system with a failure rate of 0.01 failures/hour, calculate its reliability after 100 hours using the reliability function.

2. **[Unit I | Topic: Byzantine Failures | Type: Theory | Difficulty: Intermediate]**  
   Discuss Byzantine failures and how they differ from other types of failures in distributed systems.

### Section C: Advanced Theory & Numericals

1. **[Unit I | Topic: Canonical Structures | Type: Theory | Difficulty: Advanced]**  
   Describe canonical structures in fault tolerance and their significance.

2. **[Unit I | Topic: Processor-Level Techniques | Type: Numerical | Difficulty: Advanced]**  
   Analyze a system using processor-level techniques and calculate the overall system reliability based on given component reliabilities.

## UNIT II — Fault Tolerant Design
### Section A: Definitions & Concept Questions (Basic, 2–3 Marks)

1. **[Unit II | Topic: N-Modular Redundancy | Type: Theory | Difficulty: Basic]**  
   What is N-Modular Redundancy and how does it enhance fault tolerance?

2. **[Unit II | Topic: Error Correcting Codes | Type: Theory | Difficulty: Basic]**  
   Define error correcting codes and their role in fault-tolerant design.

### Section B: Computational & Applied Problems (Intermediate, 7 Marks)

1. **[Unit II | Topic: Triple Modular Redundancy | Type: Numerical | Difficulty: Intermediate]**  
   Given a system using Triple Modular Redundancy, calculate the probability of system failure if the individual component reliability is 0.9.

2. **[Unit II | Topic: Reconfiguration Techniques | Type: Theory | Difficulty: Intermediate]**  
   Explain dynamic redundancy and its advantages over static redundancy.

### Section C: Advanced Theory & Numericals

1. **[Unit II | Topic: Sift-out Modular Redundancy | Type: Theory | Difficulty: Advanced]**  
   Discuss the principles of Sift-out Modular Redundancy and its application in fault tolerance.

2. **[Unit II | Topic: Hybrid Redundancy | Type: Numerical | Difficulty: Advanced]**  
   Calculate the expected time to recovery in a hybrid redundancy system given specific component failure rates.

## UNIT III — Information Redundancy and Fault Tolerance
### Section A: Definitions & Concept Questions (Basic, 2–3 Marks)

1. **[Unit III | Topic: Data Replication | Type: Theory | Difficulty: Basic]**  
   What is data replication and how does it contribute to fault tolerance?

2. **[Unit III | Topic: N-Version Programming | Type: Theory | Difficulty: Basic]**  
   Explain N-version programming and its effectiveness in software fault tolerance.

### Section B: Computational & Applied Problems (Intermediate, 7 Marks)

1. **[Unit III | Topic: Fault-Tolerant Networks | Type: Numerical | Difficulty: Intermediate]**  
   Given a fault-tolerant network design, calculate the maximum number of nodes that can fail without losing connectivity.

2. **[Unit III | Topic: Resilience Measures | Type: Theory | Difficulty: Intermediate]**  
   Discuss various resilience measures for fault-tolerant networks.

### Section C: Advanced Theory & Numericals

1. **[Unit III | Topic: Algorithm-Based Fault Tolerance | Type: Theory | Difficulty: Advanced]**  
   Analyze the concept of algorithm-based fault tolerance and its applications in computing systems.

2. **[Unit III | Topic: Exception Handling | Type: Numerical | Difficulty: Advanced]**  
   Evaluate a software system implementing exception handling and compute its fault tolerance metrics based on given parameters.

## UNIT IV — Checkpointing and Recovery
### Section A: Definitions & Concept Questions (Basic, 2–3 Marks)

1. **[Unit IV | Topic: Checkpointing Levels | Type: Theory | Difficulty: Basic]**  
   Define the different levels of checkpointing in fault tolerance.

2. **[Unit IV | Topic: Cache-Aided Recovery | Type: Theory | Difficulty: Basic]**  
   What is cache-aided rollback recovery and when is it used?

### Section B: Computational & Applied Problems (Intermediate, 7 Marks)

1. **[Unit IV | Topic: Optimal Checkpointing | Type: Numerical | Difficulty: Intermediate]**  
   Calculate the optimal checkpointing intervals for a system with a known failure rate and recovery time.

2. **[Unit IV | Topic: Checkpointing in Distributed Systems | Type: Theory | Difficulty: Intermediate]**  
   Discuss the challenges of implementing checkpointing in distributed systems.

### Section C: Advanced Theory & Numericals

1. **[Unit IV | Topic: Fault Detection in Cryptographic Systems | Type: Theory | Difficulty: Advanced]**  
   Analyze the methods of fault detection in cryptographic systems and their significance.

2. **[Unit IV | Topic: Checkpointing in Real-Time Systems | Type: Numerical | Difficulty: Advanced]**  
   Given a real-time system, calculate the impact of various checkpointing strategies on system performance.

## Coverage Summary
| Unit | Topics Fully Covered | Question Types | Difficulty Range |
|------|----------------------|----------------|------------------|
| I    | Fault Classification, Redundancy, Reliability Measures | Definitions, Computational, Advanced | Basic, Intermediate, Advanced |
| II   | Fault Tolerant Design, N-Modular Redundancy, Reconfiguration | Definitions, Computational, Advanced | Basic, Intermediate, Advanced |
| III  | Information Redundancy, Fault-Tolerant Networks, Software Fault Tolerance | Definitions, Computational, Advanced | Basic, Intermediate, Advanced |
| IV   | Checkpointing, Fault Detection in Cryptographic Systems | Definitions, Computational, Advanced | Basic, Intermediate, Advanced |