# BEE-101 — Fundamentals of Electrical Engineering
## Complete Detailed Step-Wise Solutions (All 4 Units, Basic → Advanced)

> Companion solutions file to `BEE-101_Question_Bank.md`. Every question is restated in full immediately before its answer, and every answer builds the underlying concept from scratch before solving — no algebraic or reasoning step is skipped. Tags match the question bank exactly (`Unit`, `Topic`, `Type`, `Difficulty`) for RAG cross-referencing.

**Contents:**
- Unit I — DC Circuit Analysis and Network Theorems
- Unit II — Steady-State Analysis of Single-Phase & Three-Phase AC Circuits
- Unit III — Magnetic Circuits & Single-Phase Transformers
- Unit IV — Electrical Machines (DC Machines, Single-Phase & Three-Phase Induction Motors)

---

## Detailed Step-Wise Solutions — UNIT I: DC Circuit Analysis and Network Theorems


---

### Section A: Definitions & Concept Questions

**Q1. [Unit I | Topic: Network Concepts | Type: Theory | Difficulty: Basic]**

**Question:** Define the terms: node, branch, loop, and mesh in an electrical network.

*Concept from scratch:* An electrical network is an interconnection of circuit elements (resistors, sources, etc.) joined by conducting wires.

- **Node:** A point in a circuit where two or more circuit elements meet (a junction). Even a plain wire connecting two elements without a third element is still just part of one node.
- **Branch:** A single path connecting two nodes, containing one circuit element (or a series combination treated as one path).
- **Loop:** Any closed path in a circuit that starts and ends at the same node without passing through any other node more than once.
- **Mesh:** A special case of a loop — a loop that does **not** contain any other loop inside it (an "elementary" or innermost loop). Every mesh is a loop, but not every loop is a mesh.

---

**Q2. [Unit I | Topic: Active/Passive Elements | Type: Theory | Difficulty: Basic]**

**Question:** Distinguish between active and passive circuit elements with examples.

*Concept from scratch:* Classification is based on whether the element can deliver net energy to the circuit over time.
- **Active elements:** Capable of delivering energy to the circuit (i.e., can supply power). Example: voltage sources (batteries), current sources, generators.
- **Passive elements:** Can only absorb or store energy, never generate net energy on their own. Example: resistor (dissipates energy as heat), inductor and capacitor (store energy but return it — net energy delivered to the circuit over a full cycle is zero or negative).

---

**Q3. [Unit I | Topic: Sources | Type: Theory | Difficulty: Basic]**

**Question:** Differentiate between an ideal voltage source and an ideal current source.

*Concept from scratch:* Ideal sources are theoretical references with no internal losses.
- **Ideal voltage source:** Maintains a specified voltage across its terminals regardless of the current drawn from it. Its internal resistance is zero (0 Ω). It can supply infinite current if short-circuited.
- **Ideal current source:** Maintains a specified current through its branch regardless of the voltage across its terminals. Its internal resistance is infinite (∞ Ω, i.e., open circuit internally). It can produce infinite voltage if open-circuited.

---

**Q4. [Unit I | Topic: Sources | Type: Theory | Difficulty: Basic]**

**Question:** Define a practical (real) voltage source and a practical current source. Draw their equivalent circuits.

*Concept from scratch:* Real sources have internal losses, modeled by adding a resistance to the ideal source.
- **Practical voltage source:** An ideal voltage source V_s in **series** with a small internal resistance R_s. As load current increases, the terminal voltage drops below V_s due to the IR drop across R_s: V_terminal = V_s − I·R_s.
- **Practical current source:** An ideal current source I_s in **parallel** with a large internal resistance R_p. As load resistance increases, part of the source current gets diverted through R_p instead of the load.
- *Equivalent circuit description:* Practical voltage source = V_s (ideal source) → in series → R_s → output terminals. Practical current source = I_s (ideal source) shown with R_p connected in parallel directly across the output terminals.

---

**Q5. [Unit I | Topic: Linearity | Type: Theory | Difficulty: Basic]**

**Question:** State the properties that make a circuit "linear." Give one linear and one non-linear circuit element.

*Concept from scratch:* A circuit (or element) is linear if it satisfies two properties simultaneously:

1. **Homogeneity (scaling):** If input is scaled by k, output scales by the same factor k. (If voltage v produces current i, then kv produces ki.)

2. **Additivity (superposition):** The response to a sum of inputs equals the sum of the responses to each input applied separately.

- **Linear element example:** Resistor — V = IR is a straight-line relationship; doubling I doubles V.
- **Non-linear element example:** Diode — the V-I relationship is exponential, not proportional; doubling voltage does not double current.

---

**Q6. [Unit I | Topic: Source Transformation | Type: Theory | Difficulty: Basic]**

**Question:** What is source transformation? State the condition under which a voltage source can be converted to an equivalent current source.

*Concept from scratch:* Source transformation is a circuit-simplification technique that converts a practical voltage source into an equivalent practical current source (or vice versa) — "equivalent" meaning the two configurations produce the **same terminal V-I behavior** as seen by the rest of the circuit.

- **Condition:** A voltage source V_s in series with resistance R_s can be converted to a current source I_s = V_s/R_s in parallel with the same resistance R_s. This is valid **only if** the source has an internal series resistance (i.e., it's a practical, not ideal, source) — an ideal voltage source (R_s = 0) cannot be transformed this way, since I_s = V_s/0 would be undefined.

---

**Q7. [Unit I | Topic: Kirchhoff's Laws | Type: Theory | Difficulty: Basic]**

**Question:** State Kirchhoff's Current Law (KCL) and Kirchhoff's Voltage Law (KVL).

*Concept from scratch:*
- **KCL (Kirchhoff's Current Law):** The algebraic sum of currents entering a node equals the algebraic sum of currents leaving that node. Equivalently: ΣI_in = ΣI_out, or the algebraic sum of all currents at a node = 0 (currents entering taken as positive, leaving as negative, or vice versa).
- **KVL (Kirchhoff's Voltage Law):** The algebraic sum of all voltage drops and rises around any closed loop is zero. Equivalently: Σ(voltage rises) = Σ(voltage drops) around any loop.

---

**Q8. [Unit I | Topic: Kirchhoff's Laws | Type: Theory | Difficulty: Basic]**

**Question:** On what fundamental physical principles are KCL and KVL based?

*Concept from scratch:*
- **KCL** is based on the **law of conservation of charge** — charge cannot accumulate at a node (a node has no capacity to store charge), so whatever charge flows in per second must flow out per second.
- **KVL** is based on the **law of conservation of energy** — as a unit positive charge is moved around any closed path back to its starting point, the net work done on it must be zero, since it returns to the same electric potential.

---

**Q9. [Unit I | Topic: Loop/Nodal Analysis | Type: Theory | Difficulty: Basic]**

**Question:** Define mesh (loop) current and node voltage as used in circuit analysis.

*Concept from scratch:*
- **Mesh (loop) current:** A fictitious current assumed to circulate around a mesh, used as the unknown variable in mesh analysis. The actual branch current in any element shared by two meshes is the algebraic sum/difference of the two mesh currents flowing through it.
- **Node voltage:** The potential difference between a given node and a chosen reference node (ground/datum, assigned 0 V), used as the unknown variable in nodal analysis.

---

**Q10 & Q11. [Unit I | Topic: Star-Delta Transformation | Type: Theory | Difficulty: Basic]**

**Question:** Write the formulae for converting a star-connected resistor network to an equivalent delta network.

**Question (Q11):** Write the formulae for converting a delta-connected resistor network to an equivalent star network.

*Concept from scratch:* Star (Y) and delta (Δ) are two ways of connecting three resistors between three terminals; they are said to be "equivalent" if they present the same resistance between every pair of terminals as seen from outside.

Let the star resistances (each connected from a terminal to a common center point) be R_a, R_b, R_c (at terminals A, B, C respectively). Let the delta resistances (each connected directly between a pair of terminals) be R_AB, R_BC, R_CA.

**Star → Delta (Q10):**
R_AB = (R_a R_b + R_b R_c + R_c R_a) / R_c
R_BC = (R_a R_b + R_b R_c + R_c R_a) / R_a
R_CA = (R_a R_b + R_b R_c + R_c R_a) / R_b

(In words: numerator is always the sum of pairwise products of the star resistances; the denominator is the star resistance of the terminal **not** included in that delta side's name.)

**Delta → Star (Q11):**
R_a = (R_AB · R_CA) / (R_AB + R_BC + R_CA)
R_b = (R_AB · R_BC) / (R_AB + R_BC + R_CA)
R_c = (R_BC · R_CA) / (R_AB + R_BC + R_CA)

(In words: numerator is the product of the two delta resistances touching that terminal; denominator is always the sum of all three delta resistances.)

---

**Q12. [Unit I | Topic: Superposition Theorem | Type: Theory | Difficulty: Basic]**

**Question:** State the Superposition theorem. What condition must the network satisfy for it to be applicable?

*Concept from scratch:* **Statement:** In a linear network containing more than one independent source, the current (or voltage) in any branch is the algebraic sum of the currents (or voltages) produced by each source acting alone, with all other independent sources "turned off" (voltage sources replaced by a short circuit, current sources replaced by an open circuit).

**Condition:** The network must be **linear** (i.e., made of linear bilateral elements — resistors, inductors, capacitors) since superposition relies on the additivity property of linear systems. It does not apply to networks containing non-linear elements.

---

**Q13. [Unit I | Topic: Thevenin's Theorem | Type: Theory | Difficulty: Basic]**

**Question:** State Thevenin's theorem. Define Thevenin's voltage (V_th) and Thevenin's resistance (R_th).

*Concept from scratch:* **Statement:** Any linear two-terminal network containing sources and resistances can be replaced, as seen from those two terminals, by a single equivalent voltage source V_th in series with a single equivalent resistance R_th.

- **V_th (Thevenin voltage):** The open-circuit voltage measured across the two terminals after removing the load (i.e., with the load terminals left open).
- **R_th (Thevenin resistance):** The resistance measured (or calculated) between the two terminals with all independent sources deactivated (voltage sources shorted, current sources opened) and the load removed.

---

**Q14. [Unit I | Topic: Norton's Theorem | Type: Theory | Difficulty: Basic]**

**Question:** State Norton's theorem. Define Norton's current (I_N) and Norton's resistance (R_N).

*Concept from scratch:* **Statement:** Any linear two-terminal network containing sources and resistances can be replaced, as seen from those two terminals, by a single equivalent current source I_N in parallel with a single equivalent resistance R_N.

- **I_N (Norton current):** The short-circuit current that would flow between the two terminals if they were directly shorted together (load removed and replaced by a wire).
- **R_N (Norton resistance):** The resistance measured (or calculated) between the two terminals with all independent sources deactivated — numerically identical to R_th.

---

**Q15. [Unit I | Topic: Thevenin/Norton Equivalence | Type: Theory | Difficulty: Basic]**

**Question:** State the relationship between Thevenin's and Norton's equivalent circuit parameters.

*Concept from scratch:* Since Thevenin's and Norton's equivalents both represent the same physical network as seen from the same two terminals, they must be interchangeable via source transformation:

R_th = R_N
V_th = I_N × R_N  ⇔  I_N = V_th / R_th

---

**Q16. [Unit I | Topic: Maximum Power Transfer | Type: Theory | Difficulty: Basic]**

**Question:** State the Maximum Power Transfer theorem for a DC circuit.

*Concept from scratch:* **Statement:** A load resistance R_L connected to a DC source (represented by its Thevenin equivalent V_th, R_th) receives **maximum power** when the load resistance equals the source's internal (Thevenin) resistance:

R_L = R_th

Under this condition, the maximum power delivered is P_max = V_th² / (4 R_th).

---

**Q17. [Unit I | Topic: Maximum Power Transfer | Type: Theory | Difficulty: Intermediate]**

**Question:** Derive the condition for maximum power transfer to the load resistance R_L from a source with internal resistance R_s.

*Step 1 — Set up the circuit:* A Thevenin source V_th with internal resistance R_s (=R_th) is connected to a variable load R_L. The current flowing is:
I = V_th / (R_s + R_L)

*Step 2 — Write power delivered to the load:*
P_L = I² R_L = [V_th / (R_s + R_L)]² · R_L = V_th² · R_L / (R_s + R_L)²

*Step 3 — Maximize P_L with respect to R_L.* Take dP_L/dR_L and set it to zero. Using the quotient rule with numerator u = R_L and denominator w = (R_s + R_L)²:

dP_L/dR_L = V_th² · [ (R_s + R_L)² · 1 − R_L · 2(R_s + R_L) ] / (R_s + R_L)⁴

*Step 4 — Simplify the numerator.* Factor out (R_s + R_L):
Numerator = (R_s + R_L) [ (R_s + R_L) − 2R_L ] = (R_s + R_L)(R_s − R_L)

So:
dP_L/dR_L = V_th² (R_s + R_L)(R_s − R_L) / (R_s + R_L)⁴ = V_th² (R_s − R_L) / (R_s + R_L)³

*Step 5 — Set derivative to zero:*
V_th² (R_s − R_L) / (R_s + R_L)³ = 0  ⟹  R_s − R_L = 0  ⟹  **R_L = R_s (= R_th)**

*Step 6 — Confirm this is a maximum (not minimum).* For R_L < R_s, dP_L/dR_L > 0 (P_L increasing); for R_L > R_s, dP_L/dR_L < 0 (P_L decreasing). So P_L peaks exactly at R_L = R_s — confirmed maximum.

*Step 7 — Find P_max.* Substitute R_L = R_s into the power expression:
P_max = V_th² · R_s / (R_s + R_s)² = V_th² · R_s / (2R_s)² = V_th² · R_s / 4R_s² = **V_th² / (4R_s)**

---

**Q18. [Unit I | Topic: Network Concepts | Type: Theory | Difficulty: Intermediate]**

**Question:** Explain the difference between a planar and a non-planar network. Why does mesh analysis apply only to planar networks?

*Concept from scratch:*
- **Planar network:** A network that can be drawn on a flat plane such that no two branches cross each other (no branch needs to "jump over" another).
- **Non-planar network:** A network that cannot be drawn without at least one pair of branches crossing.

*Why mesh analysis applies only to planar networks:* Mesh analysis relies on identifying "windows" (meshes) in the network layout — clearly bounded, non-overlapping loop areas with no branch passing through the interior. This concept of a well-defined "mesh" only exists when the circuit can be drawn flat without crossings. In a non-planar network, branches cross each other, so there's no unambiguous way to identify distinct, non-overlapping mesh regions — the very geometric basis mesh analysis depends on breaks down. (Nodal analysis, by contrast, works on any network, planar or not, since it depends only on node connectivity, not on 2D layout.)

---

**Q19. [Unit I | Topic: Loop/Nodal Analysis | Type: Theory | Difficulty: Intermediate]**

**Question:** Compare mesh (loop) analysis and nodal analysis — when is one preferred over the other?

*Concept-based comparison:*

| Aspect | Mesh (Loop) Analysis | Nodal Analysis |
|---|---|---|
| Unknowns | Mesh currents | Node voltages |
| Equations from | KVL | KCL |
| Number of equations | (branches − nodes + 1), i.e., number of independent meshes | (nodes − 1), i.e., all nodes except reference |
| Best suited when | Circuit has many series elements/loops and few nodes; circuit is planar | Circuit has many parallel elements/current sources and few nodes |
| Restriction | Applicable only to planar networks | Applicable to any network |

*When one is preferred:* If the network has fewer nodes than meshes, nodal analysis needs fewer simultaneous equations and is faster. If the network has fewer meshes than nodes, mesh analysis is faster. Circuits dominated by current sources are usually easier with nodal analysis; circuits dominated by voltage sources are usually easier with mesh analysis.

---

**Q20. [Unit I | Topic: Superposition Theorem | Type: Theory | Difficulty: Intermediate]**

**Question:** Explain why the Superposition theorem is not valid for power calculations directly.

*Concept from scratch:* Power is related to current (or voltage) by a **squared** relationship: P = I²R (or V²/R). This is a **non-linear** (quadratic) function.

Superposition is valid only for linear quantities (current, voltage) because it depends on additivity: response to (source1 + source2) = response to source1 + response to source2. But for power:

If I_total = I₁ + I₂ (from source 1 and source 2 acting individually), then:
P_total = I_total² R = (I₁ + I₂)² R = I₁²R + I₂²R + 2I₁I₂R

This is **not equal** to P₁ + P₂ = I₁²R + I₂²R, because of the extra cross-term 2I₁I₂R. This cross term represents real interaction between the two sources' effects that superposition (a linear tool) cannot capture. Hence, to find power correctly, you must first find the actual total current/voltage (via superposition, added algebraically) and only then compute power from that total — never by adding individual powers from each source.

---

### Section B: Numerical Problems

**Q21. [Unit I | Topic: Kirchhoff's Laws | Type: Numerical | Difficulty: Basic]**

**Question:** A circuit has three resistors of 2 Ω, 3 Ω, and 5 Ω connected in series across a 20 V DC source. Find the current through each resistor and the voltage drop across each.

*Step 1 — Concept:* In a series circuit, the same current flows through every element (KCL at each junction — no other path exists), and the total resistance is the sum of individual resistances.

*Step 2 — Total resistance:*
R_total = R₁ + R₂ + R₃ = 2 + 3 + 5 = **10 Ω**

*Step 3 — Total (and hence branch) current using Ohm's law:*
I = V / R_total = 20 / 10 = **2 A** (same through all three resistors, since series)

*Step 4 — Voltage drop across each resistor (Ohm's law per element):*
V₁ = I × R₁ = 2 × 2 = **4 V**
V₂ = I × R₂ = 2 × 3 = **6 V**
V₃ = I × R₃ = 2 × 5 = **10 V**

*Step 5 — Verify with KVL:* V₁ + V₂ + V₃ = 4 + 6 + 10 = 20 V = supply voltage ✓ (confirms consistency).

---

**Q22. [Unit I | Topic: Kirchhoff's Laws | Type: Numerical | Difficulty: Basic]**

**Question:** Three resistors of 4 Ω, 6 Ω, and 12 Ω are connected in parallel across a 24 V supply. Find the total current drawn from the source and the current through each branch.

*Step 1 — Concept:* In a parallel circuit, the same voltage (24 V) appears across every branch, since all branches share the same two nodes.

*Step 2 — Current in each branch (Ohm's law):*
I₁ = V/R₁ = 24/4 = **6 A**
I₂ = V/R₂ = 24/6 = **4 A**
I₃ = V/R₃ = 24/12 = **2 A**

*Step 3 — Total current (KCL at the supply node: total current in = sum of branch currents out):*
I_total = I₁ + I₂ + I₃ = 6 + 4 + 2 = **12 A**

*Step 4 — Cross-check using equivalent resistance:*
1/R_eq = 1/4 + 1/6 + 1/12 = 3/12 + 2/12 + 1/12 = 6/12 = 1/2  ⟹  R_eq = 2 Ω
I_total = V/R_eq = 24/2 = 12 A ✓ (matches)

---

**Q23. [Unit I | Topic: Star-Delta Transformation | Type: Numerical | Difficulty: Basic]**

**Question:** A star-connected network has resistances R_a = 10 Ω, R_b = 10 Ω, R_c = 10 Ω. Find the equivalent delta network resistances.

*Step 1 — Recall the star→delta formula:*
R_AB = (R_aR_b + R_bR_c + R_cR_a)/R_c, and similarly for R_BC, R_CA.

*Step 2 — Compute the common numerator (sum of pairwise products):*
R_aR_b + R_bR_c + R_cR_a = (10×10) + (10×10) + (10×10) = 100+100+100 = 300

*Step 3 — Divide by each opposite star resistance:*
R_AB = 300/R_c = 300/10 = **30 Ω**
R_BC = 300/R_a = 300/10 = **30 Ω**
R_CA = 300/R_b = 300/10 = **30 Ω**

*Step 4 — Interpretation:* Since the star was symmetric (all three resistances equal), the equivalent delta is also symmetric, with each delta resistance = 3 × (star resistance) = 3×10 = 30 Ω. This "×3" rule is a useful shortcut whenever the star is balanced.

---

**Q24. [Unit I | Topic: Star-Delta Transformation | Type: Numerical | Difficulty: Intermediate]**

**Question:** A delta network has R_AB = 30 Ω, R_BC = 30 Ω, R_CA = 30 Ω. Convert it into an equivalent star network and verify the total resistance between any two terminals matches in both configurations.

*Step 1 — Recall the delta→star formula:*
R_a = (R_AB × R_CA)/(R_AB+R_BC+R_CA), and similarly for R_b, R_c.

*Step 2 — Sum of delta resistances:*
R_AB + R_BC + R_CA = 30+30+30 = 90

*Step 3 — Compute each star resistance:*
R_a = (R_AB × R_CA)/90 = (30×30)/90 = 900/90 = **10 Ω**
R_b = (R_AB × R_BC)/90 = (30×30)/90 = **10 Ω**
R_c = (R_BC × R_CA)/90 = (30×30)/90 = **10 Ω**

*Step 4 — Verification: compute resistance between terminals A and B in both configurations.*

**In the delta:** R_AB (30 Ω) is in parallel with the series path R_BC+R_CA (30+30=60 Ω):
R_AB(equiv) = (30 × 60)/(30+60) = 1800/90 = 20 Ω

**In the star:** Looking into terminals A and B, we see R_a in series with R_b (path A→center→B), with R_c "dangling" open (not part of the A-B path since C is open):
R_AB(equiv) = R_a + R_b = 10+10 = 20 Ω

*Step 5 — Conclusion:* Both give 20 Ω between A and B — the transformation is verified consistent. ✓

---

**Q25. [Unit I | Topic: Loop Analysis | Type: Numerical | Difficulty: Intermediate]**

**Question:** Using mesh analysis, find the current in each branch of a two-loop DC network containing two voltage sources (10 V and 5 V) and three resistors (2 Ω, 3 Ω, 4 Ω) arranged in a standard two-mesh configuration.

*Step 1 — Set up a standard two-mesh configuration:* Mesh 1 (left loop) contains the 10 V source and the 2 Ω resistor in its outer branch, with the 3 Ω resistor as the shared (middle) branch between the two meshes. Mesh 2 (right loop) contains the 4 Ω resistor and the 5 V source in its outer branch, sharing the same 3 Ω middle branch. Assume mesh currents I₁ (mesh 1, clockwise) and I₂ (mesh 2, clockwise).

*Step 2 — Apply KVL to Mesh 1 (sum of voltage drops = 0, going clockwise):*
Starting at the 10 V source (treated as a rise going in the direction of I₁), then drop across 2Ω (I₁), then drop across the shared 3Ω branch, where the net current through it (in mesh-1's clockwise direction) is (I₁ − I₂):

10 = 2I₁ + 3(I₁ − I₂)
10 = 2I₁ + 3I₁ − 3I₂
**10 = 5I₁ − 3I₂  ... (i)**

*Step 3 — Apply KVL to Mesh 2:*
The 5 V source drives current in mesh 2; drop across 4Ω (I₂), and drop across the shared 3Ω branch (net current in mesh-2's clockwise direction is (I₂ − I₁)):

5 = 4I₂ + 3(I₂ − I₁)
5 = 4I₂ + 3I₂ − 3I₁
**5 = 7I₂ − 3I₁  ... (ii)**

*Step 4 — Solve the simultaneous equations.* From (i): 5I₁ − 3I₂ = 10 → multiply by 7: 35I₁ − 21I₂ = 70
From (ii): −3I₁ + 7I₂ = 5 → multiply by 3: −9I₁ + 21I₂ = 15

Add the two:
35I₁ − 21I₂ − 9I₁ + 21I₂ = 70 + 15
26I₁ = 85
**I₁ = 85/26 = 3.269 A**

*Step 5 — Back-substitute into (i):*
5(3.269) − 3I₂ = 10
16.346 − 3I₂ = 10
3I₂ = 6.346
**I₂ = 2.115 A**

*Step 6 — Branch currents:*
Current in 2Ω branch = I₁ = **3.269 A**
Current in 4Ω branch = I₂ = **2.115 A**
Current in shared 3Ω branch = I₁ − I₂ = 3.269 − 2.115 = **1.154 A** (in the direction of I₁)

---

**Q26. [Unit I | Topic: Nodal Analysis | Type: Numerical | Difficulty: Intermediate]**

**Question:** Using nodal analysis, determine the node voltages of a circuit with two nodes, a 10 A current source at node 1, a 5 A current source at node 2, and interconnecting resistors of 2 Ω, 4 Ω, and 5 Ω.

*Step 1 — Configuration:* Let node 1 (voltage V₁) connect to ground through 2 Ω, node 2 (voltage V₂) connect to ground through 4 Ω, and node 1 to node 2 through the 5 Ω resistor. A 10 A current source injects current into node 1; a 5 A source injects current into node 2. Ground = reference (0 V).

*Step 2 — Apply KCL at Node 1 (current in = current out):*
Current leaving node 1 through 2Ω = V₁/2. Current leaving node 1 through 5Ω (toward node 2) = (V₁−V₂)/5. These must sum to the injected current:

10 = V₁/2 + (V₁ − V₂)/5

Multiply through by 10 (LCM of 2 and 5) to clear denominators:
100 = 5V₁ + 2(V₁ − V₂)
100 = 5V₁ + 2V₁ − 2V₂
**100 = 7V₁ − 2V₂  ... (i)**

*Step 3 — Apply KCL at Node 2:*
Current leaving node 2 through 4Ω = V₂/4. Current leaving node 2 through 5Ω (toward node 1) = (V₂−V₁)/5.

5 = V₂/4 + (V₂ − V₁)/5

Multiply through by 20 (LCM of 4 and 5):
100 = 5V₂ + 4(V₂ − V₁)
100 = 5V₂ + 4V₂ − 4V₁
**100 = 9V₂ − 4V₁  ... (ii)**

*Step 4 — Solve simultaneously.* From (i): 7V₁ − 2V₂ = 100 → multiply by 2: 14V₁ − 4V₂ = 200
From (ii): −4V₁ + 9V₂ = 100

Add:
14V₁ − 4V₂ − 4V₁ + 9V₂ = 200+100  → wait, align properly: we add equation (i)×2 to equation (ii) directly:
(14V₁ − 4V₂) + (−4V₁ + 9V₂) = 200 + 100
10V₁ + 5V₂ = 300  ...this mixes — let's instead eliminate V₂ directly.

*Step 4 (corrected elimination) —* From (i): 7V₁ − 2V₂ = 100. From (ii): −4V₁ + 9V₂ = 100.
Multiply (i) by 9: 63V₁ − 18V₂ = 900
Multiply (ii) by 2: −8V₁ + 18V₂ = 200
Add the two:
63V₁ − 18V₂ − 8V₁ + 18V₂ = 900 + 200
55V₁ = 1100
**V₁ = 20 V**

*Step 5 — Back-substitute into (i):*
7(20) − 2V₂ = 100
140 − 2V₂ = 100
2V₂ = 40
**V₂ = 20 V**

*Step 6 — Result:* **V₁ = 20 V, V₂ = 20 V** (interesting special case — since V₁ = V₂, no current actually flows through the 5 Ω connecting resistor; each node's current source simply balances against its own ground resistor: check 10 = 20/2 = 10 ✓, and 5 = 20/4 = 5 ✓).

---

**Q27. [Unit I | Topic: Source Transformation | Type: Numerical | Difficulty: Basic]**

**Question:** A voltage source of 12 V with an internal resistance of 4 Ω is to be converted into an equivalent current source. Find the value of the equivalent current source and its parallel resistance.

*Step 1 — Recall the transformation rule:* I_s = V_s/R_s, with the same resistance now placed in parallel.

*Step 2 — Compute:*
I_s = 12/4 = **3 A**

*Step 3 — Parallel resistance:* remains **R_p = 4 Ω** (same numerical value as R_s, just reconnected in parallel instead of series).

*Result:* Equivalent current source = 3 A in parallel with 4 Ω.

---

**Q28. [Unit I | Topic: Superposition Theorem | Type: Numerical | Difficulty: Intermediate]**

**Question:** A circuit has two sources: a 20 V voltage source and a 2 A current source, both acting on a network of 5 Ω and 10 Ω resistors. Using the Superposition theorem, find the current through the 5 Ω resistor.

*Step 1 — Assume configuration:* The 20 V source is in series with the 10 Ω resistor, this combination connected across the 5 Ω resistor, and the 2 A current source is connected in parallel across the 5 Ω resistor as well (a common standard layout for this type of problem — 5Ω is the common/output branch).

*Step 2 — Consider the 20 V source acting alone (deactivate the 2 A source by opening its branch, since current sources are opened for superposition):*
With the 2 A source open, the circuit is simply the 20 V source in series with 10 Ω, driving current through 5 Ω (10Ω and 5Ω now in series, since the current-source branch is open):
I' = V/(R_10+R_5) = 20/(10+5) = 20/15 = **1.333 A** (through the 5Ω resistor, direction: as driven by the 20V source)

*Step 3 — Consider the 2 A source acting alone (deactivate the 20 V source by shorting it):*
With the 20 V source shorted, the 10 Ω resistor is now in parallel with the 5 Ω resistor (both connected between the same two nodes), and this parallel combination carries the 2 A from the current source. Current divides between 10Ω and 5Ω using the current-divider rule:
I'' (through 5Ω) = I_total × [R_10/(R_10+R_5)] = 2 × [10/(10+5)] = 2 × (10/15) = 2 × 0.667 = **1.333 A**

*Step 4 — Combine using superposition (add algebraically, respecting assumed reference direction — here both currents happen to flow in the same reference direction through the 5Ω branch):*
I_5Ω(total) = I' + I'' = 1.333 + 1.333 = **2.667 A**

---

**Q29. [Unit I | Topic: Thevenin's Theorem | Type: Numerical | Difficulty: Intermediate]**

**Question:** Find the Thevenin's equivalent circuit (V_th and R_th) as seen from terminals A-B for a network consisting of a 20 V source, a 4 Ω series resistor, and a 6 Ω resistor across the output terminals.

*Step 1 — Concept:* V_th = open-circuit voltage at A-B (i.e., remove whatever load normally sits there — here the "6Ω across output terminals" is treated as the internal network element, not the external load, since the question asks us to find the Thevenin equivalent as seen from A-B, meaning A-B are the terminals beyond the 6Ω). We treat the network as: 20V source — 4Ω (series) — node — 6Ω (to the other rail) — terminals A-B taken across the 6Ω.

*Step 2 — Find V_th (open-circuit voltage across 6Ω, i.e., across A-B):*
With A-B open (no load drawing current beyond this network), the 4Ω and 6Ω form a simple series loop with the 20V source (since no current can flow anywhere else). Current in this loop:
I = V/(R_4+R_6) = 20/(4+6) = 20/10 = 2 A

Voltage across the 6Ω resistor (this is V_th, since A-B is measured across it):
**V_th = I × R_6 = 2 × 6 = 12 V**

*Step 3 — Find R_th (deactivate the 20V source — replace with a short — then find resistance seen from A-B):*
With the source shorted, the 4Ω resistor's far end is now tied to the same rail as one end of the 6Ω (through the short), so as seen from terminals A-B, the 4Ω and 6Ω appear in **parallel**:
**R_th = (R_4 × R_6)/(R_4+R_6) = (4×6)/(4+6) = 24/10 = 2.4 Ω**

*Result:* **V_th = 12 V, R_th = 2.4 Ω**

---

**Q30. [Unit I | Topic: Norton's Theorem | Type: Numerical | Difficulty: Intermediate]**

**Question:** For the same network as above, find the Norton's equivalent circuit (I_N and R_N) as seen from terminals A-B.

*Step 1 — Recall relation:* R_N = R_th = 2.4 Ω (already found).

*Step 2 — Find I_N via I_N = V_th/R_th (simplest route, since we already have Thevenin values):*
I_N = V_th/R_th = 12/2.4 = **5 A**

*Step 3 — Cross-check by direct definition (short-circuit A-B and find the current through the short):* With A-B shorted, the 6Ω resistor is bypassed entirely (zero volts across it, so no current flows through it — all current flows through the short instead). The circuit reduces to just the 20V source driving current through the 4Ω resistor into the short:
I_sc = V/R_4 = 20/4 = 5 A ✓ (matches I_N found above)

*Result:* **I_N = 5 A, R_N = 2.4 Ω**

---

**Q31. [Unit I | Topic: Maximum Power Transfer | Type: Numerical | Difficulty: Intermediate]**

**Question:** A DC source has an EMF of 30 V and an internal resistance of 5 Ω. Find the value of load resistance R_L for maximum power transfer and calculate the maximum power delivered to the load.

*Step 1 — Apply the condition derived in Q17:*
**R_L = R_internal = 5 Ω**

*Step 2 — Compute maximum power using P_max = V²/(4R):*
P_max = 30²/(4×5) = 900/20 = **45 W**

*Step 3 — Verify by direct calculation:* At R_L=5Ω, total resistance = 5+5=10Ω, current I = 30/10 = 3A, power in load = I²R_L = 3²×5 = 9×5 = 45 W ✓

---

### Section C: Advanced Theory & Numericals

**Q32. [Unit I | Topic: Loop/Nodal Analysis | Type: Theory | Difficulty: Advanced]**

**Question:** Explain the supermesh and supernode techniques used when a current source (respectively voltage source) is shared between two loops (respectively nodes). Illustrate with a labeled circuit diagram description.

*Concept from scratch — why these techniques are needed:*

**Supermesh:** Normally, KVL is written for each mesh individually, which requires knowing the voltage across every element in that mesh. But if a **current source** lies on the boundary shared between two meshes, we don't directly know the voltage across it (a current source's terminal voltage is determined by the rest of the circuit, not fixed by the source itself) — so we cannot write a simple KVL equation for either mesh individually around that branch.

*Technique:* (1) Combine the two meshes sharing the current source into one larger loop called a "supermesh" — mentally treat the shared current-source branch as if it doesn't exist, and draw a single big loop around the outer boundary of both meshes combined. (2) Write one KVL equation around this outer supermesh boundary (this equation avoids needing the current source's voltage, since it's not on this boundary path). (3) Write a second equation directly relating the two mesh currents using the known value of the current source: (mesh current 1) − (mesh current 2) = ± I_source (sign depends on current source's direction relative to each mesh's assumed direction). Together, these two equations replace the two individual (otherwise unwritable) mesh equations.

**Supernode:** The dual situation in nodal analysis — normally KCL is written at each node, needing to know the current through every branch connected to it. But if a **voltage source** connects two non-reference nodes directly, we don't know the current through that source branch (a voltage source's current is determined by the rest of the circuit, not fixed by the source itself).

*Technique:* (1) Combine the two nodes connected by the voltage source into a single "supernode" — treat both nodes as one combined boundary enclosing both. (2) Write one KCL equation summing all currents leaving this combined boundary (this avoids needing the current through the voltage-source branch itself, since it's now "internal" to the supernode and doesn't cross the boundary). (3) Write a second equation using the known voltage-source value to relate the two node voltages directly: V_node1 − V_node2 = ± V_source (sign per source polarity). These two equations replace the two individual (otherwise unwritable) nodal equations.

*Labeled circuit description:* Picture two adjacent mesh "windows" in a circuit sharing one common vertical branch that contains a current source (arrow pointing, say, upward) instead of a resistor — this shared branch is excluded from the supermesh's outer boundary equation, and instead contributes the auxiliary constraint equation (I_mesh-left − I_mesh-right = I_source). Similarly, picture two adjacent nodes connected by a branch containing a voltage source (with + terminal at one node) instead of a resistor — the two nodes are enclosed together in one supernode boundary for the KCL sum, with the auxiliary constraint (V_node-left − V_node-right = V_source).

---

**Q33. [Unit I | Topic: Thevenin's Theorem | Type: Numerical | Difficulty: Advanced]**

**Question:** A bridge-type resistive network (five resistors: 10 Ω, 10 Ω, 10 Ω, 10 Ω, and a 20 Ω galvanometer branch) is connected to a 20 V source. Using Thevenin's theorem, find the current through the 20 Ω galvanometer branch.

*Step 1 — Set up the bridge:* Standard Wheatstone-bridge layout — source (20V) connected across nodes A and C (the "input" diagonal). Two arms from A: A→B (10Ω) and A→D (10Ω). Two arms from B and D to C: B→C (10Ω) and D→C (10Ω). The galvanometer (20Ω) bridges nodes B and D (the "output" diagonal), where we want the Thevenin equivalent.

*Step 2 — Find V_th (open-circuit voltage between B and D, i.e., remove the galvanometer):*
With the galvanometer removed, the bridge is simply two independent voltage-divider chains from A to C, both driven by the 20V source: chain 1 = A→B→C (10Ω, 10Ω), chain 2 = A→D→C (10Ω, 10Ω).

Voltage at B (relative to C, using voltage divider on chain A-B-C):
V_B = 20 × [R_BC/(R_AB+R_BC)] = 20 × [10/(10+10)] = 20 × 0.5 = 10 V (measuring toward C)

Voltage at D (relative to C, using voltage divider on chain A-D-C):
V_D = 20 × [R_DC/(R_AD+R_DC)] = 20 × [10/(10+10)] = 20 × 0.5 = 10 V

**V_th = V_B − V_D = 10 − 10 = 0 V**

*Step 3 — Interpretation:* Since all four bridge arms are equal (10Ω each), this is a **balanced bridge** — by definition, a balanced bridge always has zero potential difference across the galvanometer branch, regardless of the galvanometer's own resistance.

*Step 4 — Find R_th (deactivate the 20V source — short it — then find resistance from B to D):*
With A and C shorted together (since the source is shorted, A and C become the same node), resistor R_AB (10Ω) and R_AD (10Ω) are now both connected from B and D respectively to this same combined A-C node — so R_AB appears in parallel with R_BC (both between B and the combined A-C node... let's be careful): 

With A≡C (shorted), from node B we see two paths to the combined node: through R_AB (10Ω, to A≡C) and through R_BC (10Ω, to C≡A) — these are in parallel: R_B(equiv) = (10×10)/(10+10) = 5Ω, from B to the combined A-C node.
Similarly from node D: R_AD (10Ω) parallel with R_DC (10Ω) = 5Ω, from D to the combined A-C node.

These two 5Ω equivalents (B to A≡C, and D to A≡C) are now in **series** as seen from B to D (path: B → [A≡C] → D):
**R_th = 5 + 5 = 10 Ω**

*Step 5 — Find galvanometer current using the Thevenin equivalent (V_th=0V, R_th=10Ω, load=20Ω galvanometer):*
I_galvanometer = V_th/(R_th + R_galvanometer) = 0/(10+20) = **0 A**

*Result:* **The galvanometer current is 0 A** — this confirms the bridge is balanced (as expected, since all four arms were equal), and no current flows through the galvanometer branch regardless of its resistance value.

---

**Q34. [Unit I | Topic: Superposition + Source Transformation | Type: Numerical | Difficulty: Advanced]**

**Question:** A network contains two voltage sources (15 V, 10 V) and one current source (3 A) distributed across a three-loop resistive network. Using a combination of source transformation and superposition, find the current through the common branch.

*Step 1 — Assume a standard configuration:* Three-loop resistive network where Loop 1 has the 15V source with a 5Ω series resistor, Loop 3 has the 10V source with a 5Ω series resistor, and Loop 2 (the middle/common branch) has the 3A current source, with all three loops sharing a common central branch of 5Ω (the branch whose current we want).

*Step 2 — Apply source transformation first to simplify:* Convert the 15V+5Ω branch into an equivalent current source: I₁ = 15/5 = 3A in parallel with 5Ω. Convert the 10V+5Ω branch into an equivalent current source: I₂ = 10/5 = 2A in parallel with 5Ω. Now the network has three current sources (3A, existing 3A, and 2A) all feeding into a common node through their respective parallel resistances (5Ω, 5Ω(common branch), 5Ω), simplifying the topology to a single-node problem.

*Step 3 — Combine the current sources feeding the common node (using superposition, since all are now current sources acting into the same node — direction assumed: both transformed sources and the original 3A source inject current into the common node):*
I_total(injected) = I₁ + I_original + I₂ = 3 + 3 + 2 = 8A (this combined equivalent current source now feeds three parallel resistances of 5Ω each: two from the transformed sources, one being the common branch itself)

*Step 4 — Find equivalent parallel resistance of the two "side" 5Ω branches (excluding the common branch, since we want the current specifically in the common branch):*
R_sides(parallel) = (5×5)/(5+5) = 25/10 = 2.5 Ω

*Step 5 — Use current-divider rule to find the current through the common 5Ω branch:*
I_common = I_total × [R_sides/(R_sides + R_common)] = 8 × [2.5/(2.5+5)] = 8 × (2.5/7.5) = 8 × 0.333 = **2.667 A**

*Result:* **Current through the common branch ≈ 2.67 A**, flowing in the direction into the shared node (as set up by the combined equivalent source).

---

**Q35. [Unit I | Topic: Star-Delta + Nodal Analysis | Type: Numerical | Difficulty: Advanced]**

**Question:** A network contains a delta-connected set of three 15 Ω resistors embedded within a larger resistive circuit with two independent sources. Convert the delta to star, redraw the simplified network, and use nodal analysis to find all node voltages.

*Step 1 — Convert the delta (R_AB=R_BC=R_CA=15Ω, all equal — balanced delta) to star using the shortcut for a balanced delta:*
R_star(each) = R_delta/3 = 15/3 = **5 Ω** (so R_a = R_b = R_c = 5Ω, verified via the full formula: sum=45Ω, R_a=(15×15)/45=225/45=5Ω ✓)

*Step 2 — Redraw the simplified network:* The delta's three external terminals (A, B, C) now connect through individual 5Ω star arms to a new common center node (call it O), instead of three 15Ω arms directly between each pair. This reduces the network to a simpler star-connected sub-network with one new internal node O, embedded within the larger circuit that has its two independent sources connected at nodes A, B, C (or wherever they were originally attached) as per the "larger resistive circuit" framing.

*Step 3 — Set up nodal analysis on the simplified network:* Treating node O as an additional unknown along with whatever other nodes the two sources create (call them, for a representative worked case, node A with a source-derived injected current of I_A and node B with injected current I_B, node C tied to ground/reference as the third terminal), write KCL at each unknown node using the new 5Ω arms plus whatever other resistances the "larger circuit" contributes (represented generically as R_ext-A and R_ext-B, the external resistances at nodes A and B to ground, since the specific values of the "larger circuit" aren't numerically given in the question):

At node O (only connects to A, B, C via the three 5Ω star arms, no direct source):
(V_O−V_A)/5 + (V_O−V_B)/5 + (V_O−V_C)/5 = 0
⟹ 3V_O = V_A+V_B+V_C ⟹ **V_O = (V_A+V_B+V_C)/3**

This is the key structural result: the star center's voltage is always the simple average of the three terminal voltages, since all three arms are equal (5Ω each) — a direct consequence of symmetry.

*Step 4 — General solving procedure (to be completed with the specific external resistance/source values once given numerically):* Substitute V_O = (V_A+V_B+V_C)/3 into the KCL equations written at nodes A and B (which include their external source/resistance connections), eliminating V_O algebraically, then solve the resulting 2×2 (or 3×3 with C also unknown) system for V_A, V_B, V_C simultaneously, exactly as in Q26's method.

*Note:* Since the "larger resistive circuit" values are not numerically specified in the question as posed, this solution demonstrates the complete transformation and the reduced symmetric relation (V_O = average of the three terminal voltages) — the exact numeric node voltages depend on substituting the specific external resistances/source values from the full circuit diagram.

---

**Q36. [Unit I | Topic: Maximum Power Transfer | Type: Numerical | Difficulty: Advanced]**

**Question:** For a network with a variable load R_L connected to a Thevenin equivalent (V_th = 24 V, R_th = 8 Ω) in series with a fixed 4 Ω resistor, find R_L for maximum power transfer to R_L and calculate that maximum power. Comment on how the fixed series resistor changes the standard R_L = R_th condition.

*Step 1 — Combine the fixed series resistor with R_th first, since from R_L's perspective, both R_th and the fixed 4Ω resistor are just "internal" series resistance of the source it sees:*
R_total(internal, as seen by R_L) = R_th + R_fixed = 8 + 4 = **12 Ω**

*Step 2 — Apply the standard maximum power transfer condition, but now against this combined internal resistance (not just R_th alone):*
**R_L = R_total(internal) = 12 Ω**

*Step 3 — Compute P_max using P_max = V_th²/(4 × R_total(internal)):*
P_max = 24²/(4×12) = 576/48 = **12 W**

*Step 4 — Comment on how the fixed series resistor changes the standard condition:* The textbook rule "R_L = R_th" implicitly assumes R_th is the *entire* resistance between the source and the load. Here, an additional fixed 4Ω resistor sits between the Thevenin source and R_L, so it effectively becomes part of the "source-side" resistance for the purposes of this theorem. The correct generalized condition is **R_L = (sum of all fixed series resistance between source and load) = R_th + R_fixed**, not just R_th alone. Using only R_L = R_th = 8Ω here would be a common mistake, giving a smaller-than-maximum delivered power (verify: at R_L=8Ω, total R=8+4+8=20Ω, I=24/20=1.2A, P_L=1.2²×8=1.44×8=11.52W < 12W, confirming R_L=8Ω is indeed sub-optimal compared to the correct R_L=12Ω).

-e 

---

## Detailed Step-Wise Solutions — UNIT II: Steady-State Analysis of Single-Phase & Three-Phase AC Circuits

---

### Section A: Definitions & Concept Questions

**Q1. [Unit II | Topic: Waveforms | Type: Theory | Difficulty: Basic]**

**Question:** Define a sinusoidal waveform. Write its general mathematical expression.

*Concept from scratch:* A sinusoidal waveform is one whose instantaneous value varies with time following a sine function — the natural shape produced by a coil rotating at constant angular velocity in a uniform magnetic field (the basis of AC generation).

General expression: v(t) = V_m sin(ωt ± φ)
where V_m = peak (maximum) value, ω = angular frequency (rad/s) = 2πf, t = time, φ = phase angle (offset from a pure sine at t=0).

---

**Q2. [Unit II | Topic: Waveforms | Type: Theory | Difficulty: Basic]**

**Question:** Sketch and describe a square waveform and a triangular waveform, stating one application of each.

*Concept from scratch:*
- **Square waveform:** Alternates abruptly between two fixed levels (+V_m and −V_m), spending equal time at each, with instantaneous transitions. *Application:* digital clock/timing signals, switching power supplies (PWM).
- **Triangular waveform:** Rises linearly to a peak, then falls linearly to a trough, repeating — a smooth "up-down" ramp shape rather than a curve. *Application:* used as a reference/carrier signal in PWM generation, and in function generators for testing circuits.

---

**Q3. [Unit II | Topic: Average/RMS Values | Type: Theory | Difficulty: Basic]**

**Question:** Define the average value and RMS (effective) value of an AC waveform.

*Concept from scratch:*
- **Average value:** The arithmetic mean of instantaneous values over one half-cycle (for a symmetric AC wave, the average over a full cycle is zero, so it's conventionally computed over a half cycle). For a sinusoid: V_avg = (2/π)V_m ≈ 0.637V_m.
- **RMS (root-mean-square) / effective value:** The value of DC that would produce the same heating effect (same average power dissipation in a resistor) as the AC waveform. Found by squaring the instantaneous values, averaging over a cycle, then taking the square root. For a sinusoid: V_rms = V_m/√2 ≈ 0.707V_m.

---

**Q4. [Unit II | Topic: Average/RMS Values | Type: Theory | Difficulty: Basic]**

**Question:** Define form factor and peak factor (crest factor) of an AC waveform.

*Concept from scratch:*
- **Form factor** = RMS value / Average value. For a pure sinusoid: FF = 0.707V_m/0.637V_m ≈ 1.11.
- **Peak factor (crest factor)** = Peak (maximum) value / RMS value. For a pure sinusoid: PF = V_m/0.707V_m ≈ 1.414 (= √2).

---

**Q5. [Unit II | Topic: Phasors | Type: Theory | Difficulty: Basic]**

**Question:** What is a phasor? Why is phasor representation used for AC circuit analysis?

*Concept from scratch:* A phasor is a rotating vector (represented as a complex number) whose length equals the magnitude (RMS or peak) of a sinusoidal quantity, and whose angle equals its phase angle at t=0 — it's a static "snapshot" representation of a quantity that's actually varying sinusoidally with time.

*Why used:* Solving AC circuits directly with time-domain sine/cosine functions and calculus (for inductors/capacitors) is tedious. Phasor representation converts differential equations into simple complex-number algebra (addition, multiplication), because differentiation/integration of a sinusoid corresponds to multiplying/dividing its phasor by jω — this is far easier to manipulate.

---

**Q6. [Unit II | Topic: Phasors | Type: Theory | Difficulty: Basic]**

**Question:** Define phase and phase difference between two alternating quantities.

*Concept from scratch:*
- **Phase:** The fractional part of a cycle (expressed in angle, degrees or radians) that has elapsed relative to a chosen time reference (t=0), i.e., the argument (ωt+φ) of the sine function at a given instant.
- **Phase difference:** The angular separation between two alternating quantities of the same frequency, i.e., the difference between their phase angles φ₁ and φ₂. If φ₁ > φ₂, quantity 1 is said to "lead" quantity 2 by (φ₁−φ₂); if φ₁ < φ₂, quantity 1 "lags" quantity 2.

---

**Q7. [Unit II | Topic: RLC Circuits | Type: Theory | Difficulty: Basic]**

**Question:** Define impedance and admittance of an AC circuit. State their SI units.

*Concept from scratch:*
- **Impedance (Z):** The total opposition an AC circuit offers to current flow, combining resistance and reactance as a complex quantity: Z = R + jX. Unit: **ohm (Ω)**.
- **Admittance (Y):** The reciprocal of impedance, Y = 1/Z, representing how easily current flows. Unit: **siemens (S)**.

---

**Q8. [Unit II | Topic: RLC Circuits | Type: Theory | Difficulty: Basic]**

**Question:** Define reactance. Distinguish between inductive reactance and capacitive reactance.

*Concept from scratch:* **Reactance (X)** is the opposition offered by inductors/capacitors to AC current, arising from energy storage (not dissipation) — it's the imaginary part of impedance.
- **Inductive reactance (X_L)** = ωL = 2πfL. It **increases** with frequency (an inductor opposes rapid current changes more strongly at higher frequency). Current **lags** voltage by 90° in a pure inductor.
- **Capacitive reactance (X_C)** = 1/(ωC) = 1/(2πfC). It **decreases** with frequency (a capacitor charges/discharges more easily at higher frequency). Current **leads** voltage by 90° in a pure capacitor.

---

**Q9. [Unit II | Topic: RLC Circuits | Type: Theory | Difficulty: Basic]**

**Question:** Define power factor. State its significance in AC power systems.

*Concept from scratch:* **Power factor** = cos φ, where φ is the phase angle between voltage and current = R/Z (ratio of resistance to impedance magnitude) = (Active Power)/(Apparent Power).

*Significance:* It indicates what fraction of the apparent power (VA) drawn from the supply is actually converted to useful work (active power, W). A low power factor means the supply/distribution system carries more current than necessary for the useful work done, causing higher I²R losses in transmission lines, requiring oversized cables/transformers, and often incurring utility penalties for industrial consumers.

---

**Q10. [Unit II | Topic: Resonance | Type: Theory | Difficulty: Basic]**

**Question:** Define resonance in a series RLC circuit. Write the expression for resonant frequency.

*Concept from scratch:* **Resonance** in a series RLC circuit occurs at the frequency where the inductive reactance exactly cancels the capacitive reactance (X_L = X_C), so the circuit's net reactance is zero and impedance is purely resistive (minimum possible impedance, Z=R) — current is maximum at this frequency.

Setting X_L = X_C: ωL = 1/(ωC) ⟹ ω² = 1/(LC) ⟹ ω_r = 1/√(LC)

Resonant frequency: **f_r = 1/(2π√(LC))**

---

**Q11. [Unit II | Topic: Resonance | Type: Theory | Difficulty: Basic]**

**Question:** Define bandwidth and quality factor (Q-factor) of a resonant circuit.

*Concept from scratch:*
- **Bandwidth (BW):** The range of frequencies around resonance over which the current (or power) stays at or above 1/√2 (≈70.7%) of its maximum (resonant) value — i.e., the frequencies between the two "half-power points." BW = f_r/Q (in Hz), or equivalently BW = R/L (in rad/s).
- **Quality factor (Q-factor):** A dimensionless measure of the "sharpness" of resonance — the ratio of reactive power (energy stored) to average power dissipated, or equivalently Q = ω_rL/R = 1/(ω_rCR) = (1/R)√(L/C). Higher Q means a sharper, narrower resonance curve.

---

**Q12. [Unit II | Topic: Resonance | Type: Theory | Difficulty: Intermediate]**

**Question:** Distinguish between series resonance and parallel resonance in terms of impedance behavior at resonant frequency.

*Concept-based comparison:*
- **Series resonance:** At resonance, impedance is **minimum** (Z=R only), so current is **maximum**. The circuit behaves as a band-pass filter for current — it "accepts" the resonant frequency strongly.
- **Parallel resonance:** At resonance, impedance is **maximum** (purely resistive, called the "dynamic resistance"), so the line current drawn from the supply is **minimum**, while the circulating current between L and C branches internally can be very large. The circuit "rejects" the resonant frequency from the line current — hence parallel resonant circuits are sometimes called "rejector circuits," as opposed to series resonant "acceptor circuits."

---

**Q13. [Unit II | Topic: Three-Phase Circuits | Type: Theory | Difficulty: Basic]**

**Question:** Define a balanced three-phase supply. State the phase relationship between the three voltages.

*Concept from scratch:* A **balanced three-phase supply** consists of three sinusoidal voltages of the **same magnitude** and **same frequency**, mutually displaced by **120°** from each other in phase.

If V_R = V_m sin(ωt), then:
V_Y = V_m sin(ωt − 120°)
V_B = V_m sin(ωt − 240°) = V_m sin(ωt + 120°)

---

**Q14. [Unit II | Topic: Three-Phase Circuits | Type: Theory | Difficulty: Basic]**

**Question:** Distinguish between star (Y) and delta (Δ) connections in a three-phase system.

*Concept from scratch:*
- **Star (Y) connection:** One end of each of the three phase windings/loads is joined together at a common point called the **neutral**; the other ends are brought out as the three line terminals.
- **Delta (Δ) connection:** The three phase windings/loads are connected end-to-end in a closed loop (like a triangle), and the three junction points themselves serve as the line terminals — there is no neutral point.

---

**Q15 & Q16. [Unit II | Topic: Three-Phase Circuits | Type: Theory | Difficulty: Basic]**

**Question:** Write the relationships between line voltage/phase voltage and line current/phase current for a star connection.

**Question (Q16):** Write the relationships between line voltage/phase voltage and line current/phase current for a delta connection.

*Concept from scratch, derived from phasor geometry:*

**Star connection (Q15):**
Line voltage V_L = √3 × Phase voltage V_ph (the factor √3 arises from phasor subtraction of two phase voltages 120° apart)
Line current I_L = Phase current I_ph (since in star, each line wire carries the same current as its corresponding phase winding directly)

**Delta connection (Q16):**
Line voltage V_L = Phase voltage V_ph (each line is directly connected across one phase winding)
Line current I_L = √3 × Phase current I_ph (the √3 arises from phasor subtraction of two phase currents 120° apart feeding into each line terminal)

---

**Q17. [Unit II | Topic: Power Measurement | Type: Theory | Difficulty: Intermediate]**

**Question:** Describe the two-wattmeter method of power measurement in a three-phase circuit. Write the expressions for total power and power factor derived from the two wattmeter readings.

*Concept from scratch:* This method measures total power in a three-phase (3-wire) circuit using only **two** wattmeters, regardless of load balance or connection type (star/delta). Each wattmeter's current coil is placed in one of two chosen lines, and its voltage coil is connected between that line and the third (unused) line.

*Description:* Say wattmeters are placed in lines R and B (current coils), with their voltage coils each referenced to line Y. Wattmeter 1 reads W₁ = V_RY × I_R × cos(30°−φ), Wattmeter 2 reads W₂ = V_BY × I_B × cos(30°+φ), where φ is the load's power-factor angle.

**Total power:** P_total = W₁ + W₂ (this identity holds regardless of load power factor or balance — it's a general result of applying Blondel's theorem for n-wire systems, here n=3 needing n−1=2 wattmeters).

**Power factor from wattmeter readings** (valid specifically for a *balanced* load):
tan φ = √3 × (W₁ − W₂)/(W₁ + W₂)
⟹ cos φ = cos[tan⁻¹(√3 (W₁−W₂)/(W₁+W₂))]

---

**Q18. [Unit II | Topic: Three-Phase Power | Type: Theory | Difficulty: Basic]**

**Question:** Write the expression for total power in a balanced three-phase circuit in terms of line voltage, line current, and power factor.

*Concept from scratch:* Regardless of star or delta connection, the total active power in a balanced three-phase system, expressed in terms of *line* quantities, is:

**P = √3 × V_L × I_L × cos φ**

(This compact "√3 form" works uniformly for both star and delta because the individual √3 factors from V_L-V_ph and I_L-I_ph relations combine differently in each connection but always yield this same line-quantity formula for total power.)

---

### Section B: Numerical Problems

**Q19. [Unit II | Topic: Average/RMS Values | Type: Numerical | Difficulty: Basic]**

**Question:** A sinusoidal voltage has a peak value of 200 V. Find its RMS value, average value, and form factor.

*Step 1 — RMS value:*
V_rms = V_m/√2 = 200/1.414 = **141.4 V**

*Step 2 — Average value (over half cycle):*
V_avg = (2/π)V_m = (2/3.1416)×200 = 0.6366×200 = **127.3 V**

*Step 3 — Form factor:*
FF = V_rms/V_avg = 141.4/127.3 = **1.11**

---

**Q20. [Unit II | Topic: Average/RMS Values | Type: Numerical | Difficulty: Basic]**

**Question:** A voltage waveform is given by v(t) = 141.4 sin(314t) V. Determine the RMS value, frequency, and time period.

*Step 1 — Identify V_m from the given expression:* Comparing v(t)=V_m sin(ωt) with v(t)=141.4 sin(314t): **V_m = 141.4 V**, **ω = 314 rad/s**.

*Step 2 — RMS value:*
V_rms = V_m/√2 = 141.4/1.414 = **100 V**

*Step 3 — Frequency (from ω = 2πf):*
f = ω/(2π) = 314/(2×3.1416) = 314/6.283 = **50 Hz**

*Step 4 — Time period:*
T = 1/f = 1/50 = **0.02 s (20 ms)**

---

**Q21. [Unit II | Topic: Phasors | Type: Numerical | Difficulty: Basic]**

**Question:** Two alternating currents are given as i₁ = 10 sin(ωt) A and i₂ = 15 sin(ωt − 30°) A. Represent them as phasors and find the phase difference.

*Step 1 — Represent as phasors (using peak values as magnitude, standard convention here; angle = phase at t=0):*
I₁ = 10∠0° A
I₂ = 15∠−30° A

*Step 2 — Phase difference:*
Δφ = φ₁ − φ₂ = 0° − (−30°) = **30°**

*Step 3 — Interpretation:* i₁ **leads** i₂ by 30° (equivalently, i₂ lags i₁ by 30°).

---

**Q22. [Unit II | Topic: RLC Series Circuit | Type: Numerical | Difficulty: Basic]**

**Question:** A series RL circuit has R = 10 Ω and L = 0.05 H, connected to a 230 V, 50 Hz supply. Find the impedance, current, and power factor.

*Step 1 — Compute inductive reactance:*
X_L = 2πfL = 2×3.1416×50×0.05 = 314.16×0.05 = **15.71 Ω**

*Step 2 — Compute impedance magnitude (series RL, right-triangle relation):*
Z = √(R² + X_L²) = √(10² + 15.71²) = √(100 + 246.8) = √346.8 = **18.62 Ω**

*Step 3 — Current:*
I = V/Z = 230/18.62 = **12.35 A**

*Step 4 — Power factor:*
cos φ = R/Z = 10/18.62 = **0.537 (lagging)**, since inductive circuits have current lagging voltage.

---

**Q23. [Unit II | Topic: RLC Series Circuit | Type: Numerical | Difficulty: Basic]**

**Question:** A series RC circuit has R = 15 Ω and C = 100 µF, connected to a 230 V, 50 Hz supply. Find the impedance, current, and phase angle.

*Step 1 — Compute capacitive reactance:*
X_C = 1/(2πfC) = 1/(2×3.1416×50×100×10⁻⁶) = 1/(2×3.1416×50×0.0001)
= 1/(0.03142) = **31.83 Ω**

*Step 2 — Impedance magnitude:*
Z = √(R² + X_C²) = √(15² + 31.83²) = √(225 + 1013.1) = √1238.1 = **35.19 Ω**

*Step 3 — Current:*
I = V/Z = 230/35.19 = **6.54 A**

*Step 4 — Phase angle (current leads voltage in a capacitive circuit):*
φ = tan⁻¹(X_C/R) = tan⁻¹(31.83/15) = tan⁻¹(2.122) = **64.75° (leading)**

---

**Q24. [Unit II | Topic: RLC Series Circuit | Type: Numerical | Difficulty: Intermediate]**

**Question:** A series RLC circuit has R = 10 Ω, L = 0.1 H, and C = 100 µF, connected across a 230 V, 50 Hz supply. Calculate the impedance, current, power factor, and active power consumed.

*Step 1 — Inductive reactance:*
X_L = 2πfL = 2×3.1416×50×0.1 = 314.16×0.1 = **31.42 Ω**

*Step 2 — Capacitive reactance:*
X_C = 1/(2πfC) = 1/(314.16×100×10⁻⁶) = 1/(0.03142) = **31.83 Ω**

*Step 3 — Net reactance (series RLC: X = X_L − X_C):*
X = 31.42 − 31.83 = **−0.41 Ω** (negative ⟹ net capacitive, circuit is very close to resonance)

*Step 4 — Impedance magnitude:*
Z = √(R² + X²) = √(10² + (−0.41)²) = √(100+0.168) = √100.168 = **10.008 Ω**

*Step 5 — Current:*
I = V/Z = 230/10.008 = **22.98 A**

*Step 6 — Power factor:*
cos φ = R/Z = 10/10.008 = **0.9992 (leading, since X is negative/net capacitive)**

*Step 7 — Active power:*
P = VI cos φ = 230 × 22.98 × 0.9992 = **5280 W** (≈5.28 kW)

---

**Q25. [Unit II | Topic: RLC Parallel Circuit | Type: Numerical | Difficulty: Intermediate]**

**Question:** A parallel circuit consists of a resistor of 20 Ω in one branch and an inductor of reactance 15 Ω in the other branch, connected across a 100 V, 50 Hz supply. Find the total current and overall power factor.

*Step 1 — Current in resistive branch (in phase with voltage):*
I_R = V/R = 100/20 = **5 A** (reference phasor, angle 0°)

*Step 2 — Current in inductive branch (lags voltage by 90°):*
I_L = V/X_L = 100/15 = **6.667 A**, at angle −90°

*Step 3 — Add the two branch currents as phasors (perpendicular components — R-branch current is the "in-phase"/real part, L-branch current is the "quadrature"/imaginary part, lagging):*
I_total = √(I_R² + I_L²) = √(5² + 6.667²) = √(25+44.45) = √69.45 = **8.33 A**

*Step 4 — Overall phase angle (current lags voltage, since inductive branch draws reactive current):*
φ = tan⁻¹(I_L/I_R) = tan⁻¹(6.667/5) = tan⁻¹(1.333) = 53.13°

*Step 5 — Overall power factor:*
cos φ = cos(53.13°) = **0.6 (lagging)**

---

**Q26. [Unit II | Topic: Series-Parallel RLC | Type: Numerical | Difficulty: Intermediate]**

**Question:** A circuit has a resistor R = 10 Ω in series with a parallel combination of an inductor (X_L = 8 Ω) and a capacitor (X_C = 12 Ω). Find the total impedance of the circuit when connected to a 50 Hz supply.

*Step 1 — Find the impedance of the parallel L-C branch.* Represent as reactances in complex form: Z_L = j8, Z_C = −j12.

Parallel combination formula: Z_parallel = (Z_L × Z_C)/(Z_L + Z_C)

*Step 2 — Numerator:*
Z_L × Z_C = (j8)(−j12) = −j²×96 = −(−1)×96 = **96** (real number, since j×(−j) = −j² = 1)

*Step 3 — Denominator:*
Z_L + Z_C = j8 + (−j12) = **−j4**

*Step 4 — Divide:*
Z_parallel = 96/(−j4) = 96/(−j4) × (j/j) = 96j/(−j²×4) = 96j/(4) = **j24**

(Explanation of the division step: multiplying numerator and denominator by j converts the denominator to a real number, since j×(−j4) = −j²×4 = 4.)

*Step 5 — Add the series 10Ω resistor:*
Z_total = R + Z_parallel = 10 + j24

*Step 6 — Compute the magnitude of total impedance:*
|Z_total| = √(10² + 24²) = √(100+576) = √676 = **26 Ω**

*Result:* **Total impedance = 26 Ω** (specifically, Z_total = 10 + j24 Ω, i.e., 26∠67.38° Ω).

---

**Q27. [Unit II | Topic: Resonance | Type: Numerical | Difficulty: Intermediate]**

**Question:** A series RLC circuit has R = 5 Ω, L = 0.2 H, and C = 20 µF. Find the resonant frequency, Q-factor, and bandwidth.

*Step 1 — Resonant frequency:*
f_r = 1/(2π√(LC))

First compute LC: LC = 0.2 × 20×10⁻⁶ = 4×10⁻⁶

√(LC) = √(4×10⁻⁶) = 2×10⁻³

f_r = 1/(2π × 2×10⁻³) = 1/(0.01257) = **79.58 Hz**

*Step 2 — Q-factor at resonance:*
Q = (1/R)√(L/C)

L/C = 0.2/(20×10⁻⁶) = 0.2/0.00002 = 10,000

√(L/C) = √10000 = 100

Q = 100/5 = **20**

*Step 3 — Bandwidth:*
BW = f_r/Q = 79.58/20 = **3.98 Hz**

---

**Q28. [Unit II | Topic: Resonance | Type: Numerical | Difficulty: Intermediate]**

**Question:** A series RLC circuit resonates at 1000 Hz with R = 10 Ω, L = 0.05 H. Determine the value of C and the Q-factor at resonance.

*Step 1 — Use the resonance condition to solve for C:*
f_r = 1/(2π√(LC))  ⟹  √(LC) = 1/(2πf_r)  ⟹  LC = 1/(2πf_r)²

Compute (2πf_r)² = (2×3.1416×1000)² = (6283.2)² = 39,478,600 (approximately 3.948×10⁷)

LC = 1/(3.948×10⁷) = 2.533×10⁻⁸

*Step 2 — Solve for C:*
C = LC/L = 2.533×10⁻⁸/0.05 = **5.066×10⁻⁷ F ≈ 0.507 µF**

*Step 3 — Q-factor:*
Q = (1/R)√(L/C) = (1/10)√(0.05/5.066×10⁻⁷)

Compute L/C = 0.05/5.066×10⁻⁷ = 98,700 (approx)

√(L/C) = √98700 ≈ 314.2

Q = 314.2/10 = **31.42**

*(Cross-check via alternate formula Q = 2πf_rL/R = 2×3.1416×1000×0.05/10 = 314.16/10 = 31.42 ✓ — matches)*

---

**Q29. [Unit II | Topic: Three-Phase Star Connection | Type: Numerical | Difficulty: Basic]**

**Question:** A balanced star-connected load has a phase voltage of 230 V. Find the line voltage and, if the phase current is 10 A, find the line current.

*Step 1 — Line voltage (star relation):*
V_L = √3 × V_ph = 1.732 × 230 = **398.4 V**

*Step 2 — Line current (star relation: line current = phase current):*
I_L = I_ph = **10 A**

---

**Q30. [Unit II | Topic: Three-Phase Delta Connection | Type: Numerical | Difficulty: Basic]**

**Question:** A balanced delta-connected load has a line voltage of 400 V and a phase current of 10 A. Find the phase voltage, line current, and total power if the power factor is 0.8.

*Step 1 — Phase voltage (delta relation: phase voltage = line voltage):*
V_ph = V_L = **400 V**

*Step 2 — Line current (delta relation):*
I_L = √3 × I_ph = 1.732 × 10 = **17.32 A**

*Step 3 — Total power:*
P = √3 × V_L × I_L × cos φ = 1.732 × 400 × 17.32 × 0.8

Compute step by step: 1.732×400 = 692.8; 692.8×17.32 = 12,000 (approx); 12,000×0.8 = **9600 W (9.6 kW)**

---

**Q31. [Unit II | Topic: Three-Phase Power | Type: Numerical | Difficulty: Intermediate]**

**Question:** A balanced three-phase load draws a line current of 20 A from a 400 V (line) supply at a power factor of 0.85 lagging. Calculate the total active power, reactive power, and apparent power.

*Step 1 — Active power:*
P = √3 × V_L × I_L × cos φ = 1.732 × 400 × 20 × 0.85

1.732×400 = 692.8; 692.8×20 = 13,856; 13,856×0.85 = **11,777.6 W ≈ 11.78 kW**

*Step 2 — Apparent power:*
S = √3 × V_L × I_L = 692.8 × 20 = **13,856 VA ≈ 13.86 kVA**

*Step 3 — Reactive power (using sin φ, found from cos φ=0.85):*
sin φ = √(1−cos²φ) = √(1−0.7225) = √0.2775 = 0.5268

Q_reactive = √3 × V_L × I_L × sin φ = 13,856 × 0.5268 = **7300 VAR ≈ 7.3 kVAR**

*Step 4 — Cross-check:* S² should equal P²+Q²: 13856² ≈ 1.92×10⁸; P²+Q² = 11777.6²+7300² ≈ 1.387×10⁸+5.33×10⁷ ≈ 1.92×10⁸ ✓ (matches, confirming consistency)

---

### Section C: Advanced Theory & Numericals

**Q32. [Unit II | Topic: Resonance | Type: Theory | Difficulty: Advanced]**

**Question:** Derive the expression for resonant frequency of a series RLC circuit from first principles by equating inductive and capacitive reactance, and explain the variation of current with frequency near resonance using a labeled response curve description.

*Step 1 — Set up impedance of a series RLC circuit:*
Z = R + j(X_L − X_C) = R + j(ωL − 1/(ωC))

*Step 2 — Condition for resonance:* Resonance is defined as the frequency at which the net reactive part is zero, i.e., the circuit behaves purely resistively:
ωL − 1/(ωC) = 0
ωL = 1/(ωC)
ω² = 1/(LC)
**ω_r = 1/√(LC)**, hence **f_r = ω_r/(2π) = 1/(2π√(LC))**

*Step 3 — Describe current variation with frequency (response curve):* Current magnitude is I = V/Z = V/√(R² + (ωL−1/ωC)²).

- At very low frequency: X_C is very large (capacitor behaves nearly open), so Z is large and I is small.
- As frequency increases toward f_r: the reactive term (ωL−1/ωC) shrinks toward zero, so Z decreases toward its minimum value (Z=R), and I rises toward its **maximum value I_max = V/R**.
- At f = f_r exactly: Z = R (purely resistive, minimum), I = I_max, and voltage/current are in phase (φ=0).
- Beyond f_r: X_L begins to dominate (grows with frequency while X_C shrinks), so the reactive term grows again (now positive/inductive), Z increases again, and I falls back down.

*Shape of the curve:* A characteristic bell-shaped (resonance) peak — current rises from near-zero, peaks sharply at f_r (peak height and sharpness depending on Q-factor — higher Q gives a taller, narrower peak), then falls again symmetrically-ish about f_r on a linear frequency scale (exactly symmetric on a logarithmic scale). The width of this peak at the 0.707×I_max level defines the bandwidth.

---

**Q33. [Unit II | Topic: Power Measurement | Type: Numerical | Difficulty: Advanced]**

**Question:** In a two-wattmeter method used to measure power in a balanced three-phase load, the two wattmeters read W₁ = 5000 W and W₂ = 2000 W. Determine the total power, power factor, and the phase angle of the load.

*Step 1 — Total power:*
P_total = W₁ + W₂ = 5000 + 2000 = **7000 W (7 kW)**

*Step 2 — Compute tan φ using the two-wattmeter formula:*
tan φ = √3 × (W₁−W₂)/(W₁+W₂) = 1.732 × (5000−2000)/7000 = 1.732 × 3000/7000 = 1.732 × 0.4286 = **0.7423**

*Step 3 — Find φ:*
φ = tan⁻¹(0.7423) = **36.55°**

*Step 4 — Power factor:*
cos φ = cos(36.55°) = **0.803 (lagging)**

---

**Q34. [Unit II | Topic: Series-Parallel RLC | Type: Numerical | Difficulty: Advanced]**

**Question:** A series-parallel AC circuit has a 10 Ω resistor in series with a parallel branch of (R = 15 Ω, L giving X_L = 10 Ω) and (C giving X_C = 20 Ω), all connected to a 230 V, 50 Hz supply. Find the total current, total power factor, and total active power drawn from the supply.

*Step 1 — Express the two parallel branches as complex impedances:*
Branch 1 (R+jX_L): Z₁ = 15 + j10 Ω
Branch 2 (pure capacitive): Z₂ = −j20 Ω

*Step 2 — Compute the parallel combination Z_p = (Z₁Z₂)/(Z₁+Z₂).*

Numerator: Z₁×Z₂ = (15+j10)(−j20) = 15×(−j20) + j10×(−j20) = −j300 − j²200 = −j300 + 200 = **200 − j300**
(using −j²=+1, so j10×(−j20) = −j²×200 = 200)

Denominator: Z₁+Z₂ = (15+j10) + (0−j20) = 15 − j10

*Step 3 — Divide (200−j300)/(15−j10) by multiplying numerator and denominator by the conjugate of the denominator (15+j10):*

Denominator becomes: (15−j10)(15+j10) = 15² − (j10)² = 225 − (−100) = 225+100 = 325

Numerator becomes: (200−j300)(15+j10)
= 200×15 + 200×j10 − j300×15 − j300×j10
= 3000 + j2000 − j4500 − j²3000
= 3000 + j2000 − j4500 + 3000  (since −j²3000 = +3000)
= (3000+3000) + j(2000−4500)
= 6000 − j2500

So Z_p = (6000 − j2500)/325 = **18.46 − j7.69 Ω**

*Step 4 — Add the series 10Ω resistor:*
Z_total = 10 + (18.46 − j7.69) = **28.46 − j7.69 Ω**

*Step 5 — Magnitude of total impedance:*
|Z_total| = √(28.46² + 7.69²) = √(810.0 + 59.1) = √869.2 = **29.48 Ω**

*Step 6 — Total current:*
I_total = V/|Z_total| = 230/29.48 = **7.80 A**

*Step 7 — Phase angle and power factor:*
φ = tan⁻¹(−7.69/28.46) = tan⁻¹(−0.270) = **−15.13°** (negative ⟹ net capacitive, current leads voltage)
cos φ = cos(15.13°) = **0.966 (leading)**

*Step 8 — Total active power:*
P = VI cos φ = 230 × 7.80 × 0.966 = **1732 W ≈ 1.73 kW**

---

**Q35. [Unit II | Topic: Three-Phase Circuits | Type: Numerical | Difficulty: Advanced]**

**Question:** An unbalanced star-connected three-phase load has phase impedances Z₁ = 10∠0° Ω, Z₂ = 10∠30° Ω, Z₃ = 10∠−30° Ω, connected to a balanced 400 V three-phase supply. Find the phase currents in each branch (assume a four-wire system with neutral).

*Step 1 — Find phase voltage (star, 4-wire system — neutral provides a fixed reference, so each phase sees its own phase voltage independently regardless of load imbalance):*
V_ph = V_L/√3 = 400/1.732 = **230.9 V**

*Step 2 — Set up phase voltage phasors (standard balanced supply, 120° apart):*
V₁ = 230.9∠0° V
V₂ = 230.9∠−120° V
V₃ = 230.9∠120° V (equivalently ∠−240°)

*Step 3 — Because a solid neutral (4-wire) is present, each phase current is found completely independently (the neutral carries whatever unbalance current results — it does not affect each phase's own current, since the neutral point is held fixed by the neutral wire at 0V):*

I₁ = V₁/Z₁ = 230.9∠0° / 10∠0° = **23.09∠0° A**

I₂ = V₂/Z₂ = 230.9∠−120° / 10∠30° = (230.9/10)∠(−120°−30°) = **23.09∠−150° A**

I₃ = V₃/Z₃ = 230.9∠120° / 10∠−30° = (230.9/10)∠(120°−(−30°)) = **23.09∠150° A**

*(Step showing the division rule used: when dividing phasors, magnitudes divide and angles subtract: |V|/|Z| for magnitude, angle(V) − angle(Z) for the resulting angle.)*

*Result:* **I₁ = 23.09∠0° A, I₂ = 23.09∠−150° A, I₃ = 23.09∠150° A** — note all three have equal magnitude here (since all |Z| are equal at 10Ω) but different phase angles due to the differing impedance angles, illustrating that even with equal impedance magnitudes, differing impedance *angles* alone create phase imbalance among the currents (though here, interestingly, current magnitudes stayed balanced — imbalance shows up only in the phase angles, since all |Z_i| were equal).

---

**Q36. [Unit II | Topic: Resonance + Q-factor | Type: Numerical | Difficulty: Advanced]**

**Question:** A parallel RLC circuit has R = 100 Ω, L = 0.5 H, C = 10 µF. Find the resonant frequency, the dynamic resistance at resonance, and the Q-factor. Explain how parallel resonance differs physically from series resonance in this case.

*Step 1 — Resonant frequency (for a parallel RLC circuit with R only in the resistive branch — using the same basic formula as series resonance, valid when R is small compared to reactances, which is the standard approximation used at this level):*
f_r = 1/(2π√(LC))

LC = 0.5 × 10×10⁻⁶ = 5×10⁻⁶
√(LC) = √(5×10⁻⁶) = 2.236×10⁻³

f_r = 1/(2π × 2.236×10⁻³) = 1/(0.01405) = **71.18 Hz**

*Step 2 — Dynamic resistance at resonance (the impedance the parallel combination presents at f_r, which for a parallel RLC circuit is given by R_dynamic = L/(RC)):*
R_dynamic = L/(RC) = 0.5/(100×10×10⁻⁶) = 0.5/(0.001) = **500 Ω**

*Step 3 — Q-factor:*
Q = R/(ω_rL) — for a parallel circuit, Q is the ratio of the resistive branch to the reactive branch (inverse form compared to series), or equivalently Q = R√(C/L):

Q = R√(C/L) = 100×√(10×10⁻⁶/0.5) = 100×√(2×10⁻⁵) = 100×0.004472 = **0.4472**

*(Note: this low Q value, since R=100Ω here acts as a shunt/parallel loss resistance — a smaller parallel R means more loss, hence lower Q, which is the opposite sense from the series case where smaller R means less loss and higher Q. This sign/role reversal is a key conceptual difference to note between series and parallel RLC circuits.)*

*Step 4 — Explain how parallel resonance differs physically from series resonance:* In series resonance, impedance is **minimum** at f_r, so **line current is maximum** — the circuit "accepts" that frequency strongly (an "acceptor" circuit). In parallel resonance, impedance is **maximum** (=R_dynamic) at f_r, so the **line current drawn from the supply is minimum**, even though a large **circulating current** flows internally back and forth between the L and C branches (since the L branch and C branch currents are equal in magnitude but opposite in phase at resonance, largely canceling in the line but persisting as an internal circulating current) — hence a parallel resonant circuit is called a "rejector" circuit, since it presents high impedance (rejects/blocks current flow from the source) exactly at resonance.

-e 

---

## Detailed Step-Wise Solutions — UNIT III: Magnetic Circuits & Single-Phase Transformers

---

### Section A: Definitions & Concept Questions

**Q1. [Unit III | Topic: Magnetic Circuit | Type: Theory | Difficulty: Basic]**

**Question:** Define magnetomotive force (MMF) and magnetic reluctance. State their units.

*Concept from scratch:*
- **Magnetomotive force (MMF):** The "driving force" that establishes magnetic flux in a magnetic circuit, produced by current flowing through a coil of N turns. MMF = N × I. Unit: **ampere-turns (AT)**.
- **Reluctance (S or R_m):** The opposition offered by a magnetic material/path to the establishment of magnetic flux — the magnetic analog of electrical resistance. S = l/(μA), where l=mean length, μ=permeability, A=cross-sectional area. Unit: **AT/Wb (ampere-turns per weber)**.

---

**Q2. [Unit III | Topic: Magnetic Circuit | Type: Theory | Difficulty: Basic]**

**Question:** Define magnetic flux and flux density. State their SI units.

*Concept from scratch:*
- **Magnetic flux (Φ):** The total number of magnetic field lines passing through a given area. Unit: **weber (Wb)**.
- **Flux density (B):** The flux per unit cross-sectional area, B = Φ/A. Unit: **tesla (T)**, equivalently Wb/m².

---

**Q3. [Unit III | Topic: Magnetic Circuit | Type: Theory | Difficulty: Basic]**

**Question:** State the analogy between a magnetic circuit and an electric circuit (MMF↔EMF, flux↔current, reluctance↔resistance).

*Concept from scratch — the electric-magnetic circuit analogy:*

| Magnetic circuit quantity | Electric circuit analog |
|---|---|
| MMF (N I) | EMF (V) |
| Flux (Φ) | Current (I) |
| Reluctance (S) | Resistance (R) |

Just as EMF drives current through resistance (V=IR), MMF drives flux through reluctance: **MMF = Φ × S**. This analogy lets magnetic circuits be analyzed using techniques similar to Ohm's law and Kirchhoff's laws.

---

**Q4. [Unit III | Topic: B-H Curve | Type: Theory | Difficulty: Basic]**

**Question:** What is a B-H curve (magnetization curve)? What does its non-linear shape indicate about the magnetic material?

*Concept from scratch:* A B-H curve (magnetization curve) plots the flux density B produced in a magnetic material against the magnetizing force H (=NI/l) applied to it.

*Significance of non-linearity:* Unlike air or vacuum (where B and H are simply proportional via B=μ₀H, a straight line), ferromagnetic materials show a curve that rises steeply at first, then bends over and flattens out at high H — this flattening is called **saturation**, meaning beyond a certain point, increasing the magnetizing current produces little additional flux because nearly all the magnetic domains in the material are already aligned. This non-linearity means the material's effective permeability (μ = B/H, the slope) is not constant but changes with the operating point.

---

**Q5. [Unit III | Topic: Hysteresis | Type: Theory | Difficulty: Basic]**

**Question:** Define magnetic hysteresis. What does the area of the hysteresis loop represent?

*Concept from scratch:* **Magnetic hysteresis** is the phenomenon where the flux density B in a ferromagnetic material lags behind the applied magnetizing force H, such that B does not retrace the same path when H is decreased as it did when H was increased — tracing out a closed loop (the hysteresis loop) over one complete cycle of magnetization.

*Significance of loop area:* The area enclosed by the hysteresis loop represents the **energy lost as heat per unit volume per cycle** of magnetization (due to the work done in repeatedly reorienting magnetic domains) — this is the source of hysteresis loss in AC-excited magnetic devices like transformers.

---

**Q6. [Unit III | Topic: Hysteresis Loss | Type: Theory | Difficulty: Basic]**

**Question:** Define hysteresis loss in a magnetic material. Write Steinmetz's formula for hysteresis loss.

*Concept from scratch:* **Hysteresis loss** is the energy dissipated as heat in a magnetic core due to the repeated reversal of magnetic domain alignment as the material is cyclically magnetized by an AC supply — proportional to the area of the hysteresis loop and the number of cycles per second.

**Steinmetz's formula:**
P_h = η B_max^1.6 f V   (watts)

where η = Steinmetz's hysteresis coefficient (depends on material), B_max = maximum flux density (T), f = frequency (Hz), V = volume of the core (m³), and the exponent 1.6 (the "Steinmetz exponent") is empirically found to fit most magnetic materials over their typical operating range.

---

**Q7. [Unit III | Topic: Eddy Current Loss | Type: Theory | Difficulty: Basic]**

**Question:** Define eddy current loss. Why are transformer cores laminated?

*Concept from scratch:* When the magnetic flux in a core varies with time, it induces circulating currents within the body of the core material itself (by Faraday's law, since the core is an electrical conductor) — these are called **eddy currents**. As they flow through the core's own resistance, they dissipate energy as I²R heat, called **eddy current loss**.

*Why cores are laminated:* If the core were a single solid block, eddy currents could flow in large loops with very little resistance, causing large losses. By building the core from thin, electrically-**insulated** laminations (sheets) stacked together, the possible eddy-current loop paths are broken into many small loops confined within each thin sheet. Since eddy current loss is proportional to the square of the lamination thickness, using thin laminations drastically reduces the loss (while an insulating coating between laminations, e.g. varnish, prevents current from bridging across sheets).

---

**Q8. [Unit III | Topic: Transformer Principle | Type: Theory | Difficulty: Basic]**

**Question:** State the working principle of a transformer.

*Concept from scratch:* A transformer works on the principle of **mutual electromagnetic induction (Faraday's law)** — when an alternating current flows through the primary winding, it produces a time-varying magnetic flux in the core. This changing flux links the secondary winding (via the shared magnetic core) and, by Faraday's law, induces an alternating EMF in the secondary winding, whose magnitude depends on the number of secondary turns. No direct electrical connection exists between primary and secondary — energy transfer occurs entirely through the changing magnetic field.

---

**Q9. [Unit III | Topic: Transformer Construction | Type: Theory | Difficulty: Basic]**

**Question:** Describe the basic construction of a single-phase transformer, naming its main parts.

*Concept from scratch:* A single-phase transformer's main parts are:

1. **Core:** A closed magnetic path made of thin, laminated silicon-steel sheets (to minimize eddy current and hysteresis losses), which carries and confines the magnetic flux linking the two windings.

2. **Primary winding:** The winding connected to the input (source) supply, which sets up the flux in the core.

3. **Secondary winding:** The winding connected to the output (load), in which the EMF is induced by the mutual flux.

4. **Insulation:** Between windings and between windings and core, to prevent electrical breakdown.

5. **Tank and cooling arrangement** (for larger transformers): Houses the core-winding assembly, often filled with insulating/cooling oil, with radiators/fins for heat dissipation.

6. **Bushings/terminals:** Insulated connectors bringing the winding leads out through the tank for external connection.

---

**Q10. [Unit III | Topic: EMF Equation | Type: Theory | Difficulty: Basic]**

**Question:** Define turns ratio (transformation ratio) of a transformer.

*Concept from scratch:* **Turns ratio (transformation ratio, K)** is the ratio of the number of secondary turns to the number of primary turns:

K = N₂/N₁ = E₂/E₁ (also approximately equal to V₂/V₁ under near-ideal conditions)

If K > 1, it's a step-up transformer (secondary voltage higher); if K < 1, it's a step-down transformer.

---

**Q11. [Unit III | Topic: Transformer Losses | Type: Theory | Difficulty: Basic]**

**Question:** List the different types of power losses that occur in a transformer.

*Concept from scratch:* Transformer losses fall into two main categories:

1. **Iron losses (core losses):** Occur in the core due to the alternating flux, independent of load current. These consist of:
   - **Hysteresis loss** (from repeated domain realignment)
   - **Eddy current loss** (from induced circulating currents in the core)

2. **Copper losses (I²R losses):** Occur in the primary and secondary winding resistances due to the load current flowing through them — these losses vary with the square of the load current, so they change with loading (unlike iron losses, which stay roughly constant since flux and hence core excitation stays roughly constant across loads).

---

**Q12. [Unit III | Topic: Efficiency | Type: Theory | Difficulty: Basic]**

**Question:** Define the efficiency of a transformer. Write the general formula.

*Concept from scratch:* **Efficiency (η)** of a transformer is the ratio of output power delivered to the load, to input power drawn from the supply:

η = (Output Power)/(Input Power) = (Output Power)/(Output Power + Losses) = P_out/(P_out + P_iron + P_copper)

Often expressed as a percentage.

---

**Q13. [Unit III | Topic: Efficiency | Type: Theory | Difficulty: Intermediate]**

**Question:** State the condition for maximum efficiency of a transformer in terms of its losses.

*Concept from scratch:* Maximum efficiency of a transformer occurs at the load current where the **variable copper loss equals the constant iron loss**:

**Copper loss (at that load) = Iron loss**

(This is because iron loss is essentially constant with load, while copper loss grows as the square of load current — efficiency is maximized at the load where the sum of these two losses, relative to output, is minimized, which mathematically works out to the point where they're equal — proven formally in Q30.)

---

**Q14. [Unit III | Topic: O.C. and S.C. Tests | Type: Theory | Difficulty: Basic]**

**Question:** What is the purpose of the Open Circuit (O.C.) test on a transformer? What quantities are measured?

*Concept from scratch:* The **Open Circuit (O.C.) test** is performed with the secondary winding left open (no load) and rated voltage applied to the primary. Since no load current flows in the secondary, the primary draws only the small no-load (magnetizing + core-loss) current.

*Purpose and quantities measured:* This test determines the **iron (core) losses** of the transformer (since with negligible current, copper loss is essentially zero, so the wattmeter reading directly represents core loss) and gives the parameters of the shunt magnetizing branch of the equivalent circuit (no-load current I₀, its two components — magnetizing I_μ and working/core-loss I_w — and hence the no-load power factor).

---

**Q15. [Unit III | Topic: O.C. and S.C. Tests | Type: Theory | Difficulty: Basic]**

**Question:** What is the purpose of the Short Circuit (S.C.) test on a transformer? What quantities are measured?

*Concept from scratch:* The **Short Circuit (S.C.) test** is performed with the secondary winding short-circuited and a small, **reduced** voltage applied to the primary — just enough to circulate rated full-load current in the windings.

*Purpose and quantities measured:* Since the applied voltage is very low, the flux in the core is very low, making iron losses negligible — so the wattmeter reading in this test represents essentially only the **copper losses** at (or scaled to) full load. This test gives the equivalent resistance and reactance of the transformer (referred to the side on which the test is performed), used to predict voltage regulation and full-load efficiency.

---

**Q16. [Unit III | Topic: O.C. and S.C. Tests | Type: Theory | Difficulty: Intermediate]**

**Question:** Explain why the O.C. test is performed on the low-voltage side and the S.C. test on the high-voltage side of a transformer (or as per standard practice).

*Concept from scratch:* The **O.C. test is done on the low-voltage (LV) side** because it needs to be conducted at full **rated voltage** (to correctly establish the normal working flux for accurate iron-loss measurement), and it is safer and more convenient to apply/measure the full rated voltage on the LV side using standard low-range meters, rather than working with the higher rated voltage of the HV side.

The **S.C. test is done on the HV side** because the test requires only a small percentage of rated voltage (just enough to drive rated current through the winding impedance) — since HV windings have proportionally higher impedance and lower rated current, this small test voltage and current are more conveniently measured/handled using standard instrument ranges. Conducting the S.C. test on the LV side instead would require an extremely small test voltage that is hard to measure/control accurately, along with an inconveniently large test current, so HV-side testing is standard practice for accuracy and instrument convenience.

---

**Q17. [Unit III | Topic: Auto Transformer | Type: Theory | Difficulty: Basic]**

**Question:** What is an auto-transformer? How does it differ from a two-winding transformer?

*Concept from scratch:* An **auto-transformer** is a transformer with only a **single winding**, part of which is common to both the primary and secondary circuits — a tapping point on this single winding divides it to provide the second voltage level. Unlike a conventional two-winding transformer, there is a **direct electrical (galvanic) connection** between the primary and secondary sides, not just a magnetic coupling — energy is transferred both inductively (through mutual flux, like a normal transformer) and conductively (directly, through the shared winding portion).

---

**Q18. [Unit III | Topic: Auto Transformer | Type: Theory | Difficulty: Intermediate]**

**Question:** State the advantages and disadvantages of an auto-transformer compared to a conventional two-winding transformer.

*Concept from scratch:*

**Advantages:**
- Requires **less copper** for a given rating (since part of the winding is shared, not duplicated), making it cheaper and lighter, especially for transformation ratios close to 1.
- **Higher efficiency** (lower copper losses due to less material and less I²R dissipation in the shared winding).
- **Better voltage regulation** (lower leakage reactance due to closer winding coupling).
- Smaller size for the same kVA rating, since not all power is transferred inductively — some passes directly (conductively) through the shared winding.

**Disadvantages:**
- **No electrical isolation** between primary and secondary — a fault or high voltage on one side can directly appear on the other side, which is a safety hazard (especially dangerous if the primary is at high voltage and secondary supplies low-voltage equipment/people).
- If the common winding portion breaks/opens, the full primary voltage can appear across the load — a serious safety risk.
- The saving in size/cost diminishes as the transformation ratio moves further from 1 (for large ratios, an auto-transformer offers little advantage over a conventional transformer).

---

### Section B: Numerical Problems

**Q19. [Unit III | Topic: Magnetic Circuit | Type: Numerical | Difficulty: Basic]**

**Question:** A magnetic circuit has a mean length of 0.5 m, cross-sectional area of 0.001 m², and relative permeability of 1000. Find the reluctance of the circuit.

*Step 1 — Recall reluctance formula:*
S = l/(μ₀ μ_r A)

*Step 2 — Substitute values (μ₀ = 4π×10⁻⁷ H/m):*
S = 0.5/[(4π×10⁻⁷)(1000)(0.001)]

*Step 3 — Compute denominator step by step:*
4π×10⁻⁷ = 1.2566×10⁻⁶
1.2566×10⁻⁶ × 1000 = 1.2566×10⁻³
1.2566×10⁻³ × 0.001 = 1.2566×10⁻⁶

*Step 4 — Divide:*
S = 0.5/(1.2566×10⁻⁶) = **397,887 AT/Wb ≈ 3.98×10⁵ AT/Wb**

---

**Q20. [Unit III | Topic: Magnetic Circuit | Type: Numerical | Difficulty: Intermediate]**

**Question:** A coil of 500 turns is wound on a magnetic core with a reluctance of 50000 AT/Wb. If the coil carries a current of 2 A, find the MMF and the flux produced.

*Step 1 — Compute MMF:*
MMF = N × I = 500 × 2 = **1000 AT**

*Step 2 — Compute flux using the magnetic-circuit "Ohm's law": MMF = Φ × S ⟹ Φ = MMF/S:*
Φ = 1000/50,000 = **0.02 Wb**

---

**Q21. [Unit III | Topic: Hysteresis Loss | Type: Numerical | Difficulty: Intermediate]**

**Question:** A transformer core has a volume of 0.02 m³, operates at a maximum flux density of 1.2 T and a frequency of 50 Hz. Using Steinmetz's coefficient η = 150 (SI units) and exponent 1.6, calculate the hysteresis loss.

*Step 1 — Recall Steinmetz's formula:*
P_h = η B_max^1.6 f V

*Step 2 — Compute B_max^1.6 = 1.2^1.6:*
ln(1.2) = 0.1823; 0.1823 × 1.6 = 0.2917; e^0.2917 = **1.339**
So 1.2^1.6 ≈ 1.339

*Step 3 — Substitute all values:*
P_h = 150 × 1.339 × 50 × 0.02

*Step 4 — Multiply step by step:*
150 × 1.339 = 200.85
200.85 × 50 = 10,042.5
10,042.5 × 0.02 = **200.85 W ≈ 201 W**

---

**Q22. [Unit III | Topic: EMF Equation | Type: Numerical | Difficulty: Basic]**

**Question:** A single-phase transformer has 300 primary turns and 900 secondary turns. If the maximum flux in the core is 0.05 Wb at 50 Hz, find the primary and secondary induced EMFs.

*Step 1 — Recall the transformer EMF equation:*
E = 4.44 f N Φ_max

*Step 2 — Primary EMF:*
E₁ = 4.44 × 50 × 300 × 0.05

Compute: 4.44×50 = 222; 222×300 = 66,600; 66,600×0.05 = **3330 V**

*Step 3 — Secondary EMF:*
E₂ = 4.44 × 50 × 900 × 0.05

Compute: 4.44×50=222; 222×900=199,800; 199,800×0.05 = **9990 V**

*Step 4 — Cross-check via turns ratio:* E₂/E₁ should equal N₂/N₁ = 900/300 = 3. Check: 9990/3330 = 3 ✓

---

**Q23. [Unit III | Topic: EMF Equation | Type: Numerical | Difficulty: Basic]**

**Question:** A transformer is connected to a 230 V, 50 Hz supply on the primary and has a turns ratio of 1:4. Find the secondary voltage and the maximum flux in the core if the primary has 200 turns.

*Step 1 — Secondary voltage using turns ratio:*
V₂ = V₁ × (N₂/N₁) = 230 × 4 = **920 V**

*Step 2 — Find N₂ (needed only conceptually — turns ratio 1:4 with N₁=200 means N₂=800; not required further here but useful to state):* N₂ = 4×N₁ = 4×200 = 800

*Step 3 — Find maximum flux using the EMF equation, rearranged for Φ_max, applied to the primary side:*
E₁ = 4.44 f N₁ Φ_max ⟹ Φ_max = E₁/(4.44 f N₁)

(Approximating E₁ ≈ V₁ = 230V, as is standard practice at this level, ignoring small internal drops)

Φ_max = 230/(4.44 × 50 × 200)

*Step 4 — Compute denominator:*
4.44×50 = 222; 222×200 = 44,400

*Step 5 — Divide:*
Φ_max = 230/44,400 = **0.00518 Wb ≈ 5.18 mWb**

---

**Q24. [Unit III | Topic: Efficiency | Type: Numerical | Difficulty: Intermediate]**

**Question:** A 20 kVA transformer has iron losses of 200 W and full-load copper losses of 300 W. Calculate its efficiency at full load and at 0.8 power factor.

*Step 1 — Compute output power at full load:*
P_out = kVA × cos φ = 20,000 × 0.8 = **16,000 W**

*Step 2 — Total losses at full load:*
P_losses = P_iron + P_copper = 200 + 300 = **500 W**

*Step 3 — Efficiency:*
η = P_out/(P_out + P_losses) = 16,000/(16,000+500) = 16,000/16,500 = 0.9697

**η ≈ 96.97%**

---

**Q25. [Unit III | Topic: Efficiency | Type: Numerical | Difficulty: Intermediate]**

**Question:** For the transformer in the previous question, find the load at which maximum efficiency occurs and calculate that maximum efficiency (at unity power factor).

*Step 1 — Recall the condition for maximum efficiency:* Copper loss (at load fraction x of full load) = Iron loss, i.e., x² × P_cu(FL) = P_iron

*Step 2 — Solve for x (fraction of full load):*
x² = P_iron/P_cu(FL) = 200/300 = 0.6667
x = √0.6667 = **0.8165 (i.e., ≈81.65% of full load)**

*Step 3 — Load kVA at maximum efficiency:*
Load = x × 20 kVA = 0.8165 × 20 = **16.33 kVA**

*Step 4 — Output power at this load, unity p.f.:*
P_out = 16.33 × 1000 × 1 = **16,330 W**

*Step 5 — At maximum efficiency, copper loss = iron loss = 200W each, so total loss = 200+200 = 400W*

*Step 6 — Maximum efficiency:*
η_max = P_out/(P_out+losses) = 16,330/(16,330+400) = 16,330/16,730 = 0.9761

**η_max ≈ 97.61%**

---

**Q26. [Unit III | Topic: O.C. Test | Type: Numerical | Difficulty: Intermediate]**

**Question:** In an O.C. test on a transformer, the readings on the LV side are: V = 230 V, I = 3 A, W = 100 W. Calculate the no-load power factor, the magnetizing component of current, and the working (core-loss) component of current.

*Step 1 — No-load power factor:*
cos φ₀ = W₀/(V₀ I₀) = 100/(230×3) = 100/690 = **0.1449**

*Step 2 — Find φ₀:*
φ₀ = cos⁻¹(0.1449) = **81.67°**

*Step 3 — Working (core-loss) component of current:*
I_w = I₀ cos φ₀ = 3 × 0.1449 = **0.435 A**

*Step 4 — Magnetizing component of current:*
I_μ = I₀ sin φ₀

First find sin φ₀ = √(1−cos²φ₀) = √(1−0.1449²) = √(1−0.021) = √0.979 = 0.9895

I_μ = 3 × 0.9895 = **2.968 A**

*Step 5 — Cross-check:* I₀ = √(I_w² + I_μ²) = √(0.435² + 2.968²) = √(0.189+8.809) = √8.998 ≈ 3.0 A ✓

---

**Q27. [Unit III | Topic: S.C. Test | Type: Numerical | Difficulty: Intermediate]**

**Question:** In an S.C. test on a transformer, the readings on the HV side are: V = 40 V, I = 10 A (rated), W = 200 W. Calculate the equivalent resistance and equivalent reactance referred to the HV side.

*Step 1 — Equivalent resistance (referred to HV side, since test performed there):*
R_eq = W/I² = 200/10² = 200/100 = **2 Ω**

*Step 2 — Equivalent impedance:*
Z_eq = V/I = 40/10 = **4 Ω**

*Step 3 — Equivalent reactance (using Z² = R² + X²):*
X_eq = √(Z_eq² − R_eq²) = √(4² − 2²) = √(16−4) = √12 = **3.46 Ω**

---

**Q28. [Unit III | Topic: Auto Transformer | Type: Numerical | Difficulty: Basic]**

**Question:** A single-phase auto-transformer has a total winding of 400 turns, with the tapping at 100 turns from the common point, connected to a 230 V supply. Find the output voltage.

*Step 1 — Concept:* In a step-down auto-transformer, the input is applied across the full winding (400 turns), and the output is taken across a portion of it (100 turns) — the ratio of output to input voltage follows the same turns-ratio principle as a normal transformer.

*Step 2 — Compute output voltage:*
V_out = V_in × (N_tap/N_total) = 230 × (100/400) = 230 × 0.25 = **57.5 V**

---

### Section C: Advanced Theory & Numericals

**Q29. [Unit III | Topic: EMF Equation | Type: Theory | Difficulty: Advanced]**

**Question:** Derive the EMF equation of a transformer from first principles, starting from Faraday's law of electromagnetic induction, and clearly define every symbol used.

*Step 1 — Start from Faraday's law of electromagnetic induction:* The EMF induced in a coil of N turns due to a changing flux Φ linking it is:
e = −N (dΦ/dt)

*Step 2 — Assume the core flux varies sinusoidally with time (since it's produced by a sinusoidal AC supply):*
Φ(t) = Φ_max sin(ωt)

*Step 3 — Differentiate Φ(t) with respect to time:*
dΦ/dt = Φ_max ω cos(ωt)

*Step 4 — Substitute into Faraday's law (dropping the negative sign, since it only indicates direction per Lenz's law, and we're interested in magnitude):*
e = N Φ_max ω cos(ωt)

*Step 5 — Identify the maximum (peak) value of induced EMF:*
E_max = N Φ_max ω = N Φ_max (2πf) = 2π f N Φ_max

*Step 6 — Convert peak EMF to RMS value (since EMF varies as a cosine, its RMS value is peak/√2, exactly like any sinusoid):*
E_rms = E_max/√2 = (2π f N Φ_max)/√2

*Step 7 — Simplify the constant 2π/√2:*
2π/√2 = 2×3.1416/1.4142 = 6.2832/1.4142 = **4.44**

*Step 8 — Final EMF equation:*
**E = 4.44 f N Φ_max**

*Step 9 — Apply this separately to each winding (define symbols):*
E₁ = 4.44 f N₁ Φ_max  (primary induced EMF)
E₂ = 4.44 f N₂ Φ_max  (secondary induced EMF)

where: f = supply frequency (Hz), N₁, N₂ = number of primary/secondary turns, Φ_max = maximum value of core flux (Wb), and 4.44 is a fixed numerical constant arising purely from the sinusoidal waveform shape (=2π/√2) as derived above.

---

**Q30. [Unit III | Topic: Efficiency | Type: Theory | Difficulty: Advanced]**

**Question:** Derive the condition for maximum efficiency of a transformer, starting from the general efficiency expression in terms of output, copper loss, and iron loss. Show that maximum efficiency occurs when copper loss equals iron loss.

*Step 1 — Write the general efficiency expression at a fraction x of full load, output power factor cos φ, rated output S(kVA) at full load:*
Output power at load fraction x: P_out = x·S·cos φ
Copper loss at load fraction x (scales with square of current, hence square of x): P_cu = x² P_cu(FL)
Iron loss: P_i (essentially constant regardless of load, since it depends on flux/voltage, not current)

η = P_out/(P_out + P_i + P_cu) = (x S cos φ)/(x S cos φ + P_i + x² P_cu(FL))

*Step 2 — To maximize η, it's easier to minimize its reciprocal, 1/η, with respect to x:*
1/η = (x S cos φ + P_i + x² P_cu(FL))/(x S cos φ) = 1 + P_i/(x S cos φ) + x P_cu(FL)/(S cos φ)

*Step 3 — Differentiate 1/η with respect to x, treating S, cos φ, P_i, P_cu(FL) as constants:*
d(1/η)/dx = −P_i/(x² S cos φ) + P_cu(FL)/(S cos φ)

*Step 4 — Set the derivative to zero for the extremum (minimum of 1/η ⟺ maximum of η):*
−P_i/(x² S cos φ) + P_cu(FL)/(S cos φ) = 0

*Step 5 — Multiply through by (S cos φ) to simplify:*
−P_i/x² + P_cu(FL) = 0
P_cu(FL) = P_i/x²
x² P_cu(FL) = P_i

*Step 6 — Recognize that x² P_cu(FL) is exactly the copper loss at load fraction x (from Step 1's definition):*
**Copper loss (at that load) = P_i = Iron loss**

*Step 7 — Confirm it's a maximum (not minimum) of η:* Since 1/η → ∞ as x→0 (P_i/x term dominates) and 1/η increases again for very large x (x·P_cu(FL) term dominates), the stationary point found must correspond to a **minimum of 1/η**, i.e., a **maximum of η**. This confirms: **Maximum efficiency occurs at the load where variable copper loss equals the (constant) iron loss.**

---

**Q31. [Unit III | Topic: O.C. and S.C. Tests | Type: Numerical | Difficulty: Advanced]**

**Question:** From an O.C. test (V = 230 V, I₀ = 2 A, W₀ = 150 W, LV side) and an S.C. test (V = 25 V, I = 10 A, W = 120 W, HV side) on a single-phase transformer of turns ratio 1:5, determine: (a) the equivalent circuit parameters R₀ and X₀ (shunt branch) referred to the LV side, and (b) the equivalent resistance and reactance referred to the HV side. Then calculate the efficiency at 75% of full load, 0.8 p.f. lagging.

*Step 1 — No-load power factor:*
cos φ₀ = W₀/(V₀I₀) = 150/(230×2) = 150/460 = **0.3261**

*Step 2 — Working component of current:*
I_w = I₀ cos φ₀ = 2 × 0.3261 = **0.6522 A**

*Step 3 — Magnetizing component:*
sin φ₀ = √(1−0.3261²) = √(1−0.1063) = √0.8937 = 0.9453
I_μ = I₀ sin φ₀ = 2 × 0.9453 = **1.8906 A**

*Step 4 — Shunt resistance R₀ (representing core loss):*
R₀ = V₀/I_w = 230/0.6522 = **352.7 Ω**

*Step 5 — Shunt reactance X₀ (representing magnetization):*
X₀ = V₀/I_μ = 230/1.8906 = **121.6 Ω**

**Part (b): Series (equivalent resistance/reactance) parameters referred to HV side (from S.C. test)**

*Step 6 — Equivalent resistance (HV side, since test performed there):*
R_eq(HV) = W/I² = 120/10² = 120/100 = **1.2 Ω**

*Step 7 — Equivalent impedance:*
Z_eq(HV) = V/I = 25/10 = **2.5 Ω**

*Step 8 — Equivalent reactance:*
X_eq(HV) = √(Z_eq² − R_eq²) = √(2.5² − 1.2²) = √(6.25−1.44) = √4.81 = **2.193 Ω**

**Part (c): Efficiency at 75% of full load, 0.8 p.f. lagging**

*Step 9 — Determine full-load rating.* Since the S.C. test was run at I=10A (this is the rated/full-load current on the HV side, as S.C. tests are conventionally run at rated current), full-load HV current = 10A. Full-load copper loss (from S.C. test wattmeter, at full rated current) = W = **120 W** (this already represents full-load copper loss, since the test was performed exactly at rated current).

*Step 10 — Copper loss at 75% load (scales with square of load fraction):*
P_cu(75%) = (0.75)² × 120 = 0.5625 × 120 = **67.5 W**

*Step 11 — Iron loss (constant regardless of load, taken from O.C. test):*
P_iron = W₀ = **150 W**

*Step 12 — Determine full-load kVA rating (using HV side values: V=25V is only the reduced test voltage, not the rated voltage — we need the transformer's actual HV rated voltage. Since turns ratio is 1:5 (step-up from LV to HV) and LV O.C. test was run at 230V (which is the LV rated voltage), the HV rated voltage = 230×5 = 1150V).*

Full-load HV current = 10A (from S.C. test, at rated current)
Full-load kVA = (V_HV,rated × I_HV,rated)/1000 = (1150×10)/1000 = **11.5 kVA**

*Step 13 — Output power at 75% load, 0.8 p.f. lagging:*
P_out = 0.75 × 11.5 kVA × 1000 × 0.8 = 0.75×11,500×0.8

Compute: 0.75×11,500 = 8625; 8625×0.8 = **6900 W**

*Step 14 — Total losses at 75% load:*
P_losses = P_cu(75%) + P_iron = 67.5 + 150 = **217.5 W**

*Step 15 — Efficiency:*
η = P_out/(P_out+P_losses) = 6900/(6900+217.5) = 6900/7117.5 = 0.9694

**η ≈ 96.94%**

---

**Q32. [Unit III | Topic: Auto Transformer | Type: Numerical | Difficulty: Advanced]**

**Question:** A 400 V/200 V, 10 kVA two-winding transformer is reconnected as a step-down auto-transformer for a 400 V/200 V conversion. Calculate the maximum kVA rating of the auto-transformer and the saving in copper as compared to operation as a two-winding transformer.

*Step 1 — Concept:* When a two-winding transformer is reconnected as an auto-transformer, the same physical windings (rated for the same current and voltage as before) are now connected in series (instead of being magnetically-only coupled), allowing part of the power to be transferred **conductively** rather than purely inductively — this lets the auto-transformer handle a larger kVA than its original two-winding rating for the same winding size.

*Step 2 — Determine the transformation ratio K (secondary/primary):*
K = 200/400 = **0.5**

*Step 3 — Auto-transformer kVA rating formula (in terms of the original two-winding rating W and ratio K):*
kVA(auto) = W/(1−K)  [for step-down auto-transformer configuration]

*Step 4 — Substitute:*
kVA(auto) = 10/(1−0.5) = 10/0.5 = **20 kVA**

*Step 5 — Saving in copper (standard result): the fractional saving in copper compared to using a conventional two-winding transformer of the same rating is:*
Saving fraction = K (for this standard step-down auto-transformer configuration)

Saving = K × W_conventional_copper, but more usefully expressed as a percentage of the copper that *would* be needed in an ordinary two-winding transformer of the new (20kVA) rating:

Saving (%) = K × 100% = 0.5 × 100 = **50%**

*Step 6 — Interpretation:* The auto-transformer, built from the same windings as the original 10kVA two-winding unit, can now supply **20 kVA**, while using only **50% of the copper** that a conventional two-winding transformer of that same 20kVA rating would require — a substantial material saving, consistent with the general principle that auto-transformer savings are largest when the transformation ratio K is close to 1 (i.e., primary and secondary voltages are close together, as they are here: 400V and 200V, K=0.5 — a "moderate" saving case, not an extreme one).

---

**Q33. [Unit III | Topic: Magnetic Circuit + Hysteresis | Type: Numerical | Difficulty: Advanced]**

**Question:** A magnetic core forms a closed ring of mean length 0.4 m with a 2 mm air gap, cross-sectional area 0.0015 m², relative permeability of the core material 1200. A coil of 800 turns carries a current sufficient to produce a flux of 0.0012 Wb. Calculate the total MMF required, accounting separately for the core and air-gap reluctances.

*Step 1 — Concept:* The total magnetic circuit is a series combination of the core's reluctance and the air gap's reluctance (they're traversed by the same flux, one after another around the loop) — total MMF required = MMF for core + MMF for air gap.

*Step 2 — Core length (subtract the air gap from the total mean length, since the 0.4m mean length includes the gap):*
l_core = 0.4 − 0.002 = **0.398 m**

*Step 3 — Core reluctance:*
S_core = l_core/(μ₀ μ_r A) = 0.398/[(4π×10⁻⁷)(1200)(0.0015)]

Compute denominator: 4π×10⁻⁷ = 1.2566×10⁻⁶
1.2566×10⁻⁶ × 1200 = 1.508×10⁻³
1.508×10⁻³ × 0.0015 = 2.262×10⁻⁶

S_core = 0.398/(2.262×10⁻⁶) = **175,950 AT/Wb**

*Step 4 — Air gap reluctance (μ_r = 1 for air, since it's non-magnetic):*
S_gap = l_gap/(μ₀ × 1 × A) = 0.002/[(1.2566×10⁻⁶)(0.0015)]

Compute denominator: 1.2566×10⁻⁶ × 0.0015 = 1.885×10⁻⁹

S_gap = 0.002/(1.885×10⁻⁹) = **1,061,000 AT/Wb (≈1.061×10⁶)**

*Step 5 — Note the huge disparity:* The air gap's reluctance (≈1.06×10⁶) is about 6 times larger than the core's reluctance (≈1.76×10⁵), despite being only 2mm long versus 398mm for the core — this illustrates how strongly air (low permeability) resists flux compared to a ferromagnetic core, even over a tiny length.

*Step 6 — Total reluctance (series sum):*
S_total = S_core + S_gap = 175,950 + 1,061,000 = **1,236,950 AT/Wb**

*Step 7 — Total MMF required (MMF = Φ × S_total):*
MMF = 0.0012 × 1,236,950 = **1484.3 AT**

*Step 8 — Breakdown (for completeness, showing each contribution separately):*
MMF for core = Φ × S_core = 0.0012 × 175,950 = **211.1 AT**
MMF for air gap = Φ × S_gap = 0.0012 × 1,061,000 = **1273.2 AT**
Check: 211.1 + 1273.2 = 1484.3 AT ✓ (matches Step 7)

*Result:* **Total MMF required ≈ 1484.3 AT**, of which the tiny 2mm air gap alone demands **≈1273.2 AT (about 86% of the total MMF)** — a striking illustration of why air gaps dominate magnetic circuit design even when physically very short.

-e 

---

## Detailed Step-Wise Solutions — UNIT IV: Electrical Machines (DC Machines, Single-Phase & Three-Phase Induction Motors)

---

### Section A: Definitions & Concept Questions

**Q1. [Unit IV | Topic: Electromechanical Energy Conversion | Type: Theory | Difficulty: Basic]**

**Question:** What is meant by electromechanical energy conversion? Name the basic principle governing energy conversion in rotating electrical machines.

*Concept from scratch:* Electromechanical energy conversion is the process of converting electrical energy into mechanical energy (as in a motor) or mechanical energy into electrical energy (as in a generator), through the medium of a magnetic field acting as the energy-transfer link.

*Basic principle:* This conversion in rotating machines is governed by **Faraday's law of electromagnetic induction** (a conductor moving through a magnetic field, or experiencing a changing flux, has an EMF induced in it — the basis of generator action) together with the **Biot–Savart / motor principle** (a current-carrying conductor placed in a magnetic field experiences a mechanical force, F = BIl — the basis of motor action). Every rotating electrical machine relies on this two-way interaction between current, magnetic field, and mechanical motion.

---

**Q2. [Unit IV | Topic: DC Machine Types | Type: Theory | Difficulty: Basic]**

**Question:** List the different types of DC generators based on excitation (separately excited, shunt, series, compound).

*Concept from scratch:* DC generators are classified by how the field winding is excited (supplied with current):

1. **Separately excited:** Field winding is supplied from an independent external DC source, separate from the armature.

2. **Self-excited — shunt:** Field winding is connected in parallel (shunt) with the armature, drawing its excitation from the generator's own output.

3. **Self-excited — series:** Field winding is connected in series with the armature circuit, so it carries the full armature (load) current.

4. **Self-excited — compound:** Has both a shunt and a series field winding together (further divided into short-shunt and long-shunt, and cumulative/differential compound based on how the two fields interact).

---

**Q3. [Unit IV | Topic: DC Machine Types | Type: Theory | Difficulty: Basic]**

**Question:** List the different types of DC motors based on excitation, similar to DC generators.

*Concept from scratch:* DC motors follow the same excitation-based classification as generators:

1. **Separately excited motor**

2. **Shunt motor** (field winding in parallel with armature)

3. **Series motor** (field winding in series with armature, carries full armature current)

4. **Compound motor** (both shunt and series field windings — cumulative or differential compound)

---

**Q4. [Unit IV | Topic: EMF Equation | Type: Theory | Difficulty: Basic]**

**Question:** Write the EMF equation of a DC generator and define each term used in it.

*Concept from scratch:* The EMF equation of a DC generator:

**E_g = (ΦZN P)/(60 A)**

where: Φ = flux per pole (Wb), Z = total number of armature conductors, N = speed of armature (rpm), P = number of poles, A = number of parallel paths in the armature winding (A=P for lap winding, A=2 for wave winding).

---

**Q5. [Unit IV | Topic: Torque Equation | Type: Theory | Difficulty: Basic]**

**Question:** Write the torque equation of a DC motor and define each term used in it.

*Concept from scratch:* The torque equation of a DC motor:

**T = (0.159 Φ Z I_a P)/A**  (in newton-metres, where the constant 0.159 ≈ 1/(2π))

or equivalently, derived from power balance E_bI_a = Tω: T = (ΦZI_aP)/(2πA)

where: Φ = flux per pole (Wb), Z = total armature conductors, I_a = armature current (A), P = number of poles, A = number of parallel paths.

---

**Q6. [Unit IV | Topic: Commutator | Type: Theory | Difficulty: Basic]**

**Question:** What is the function of a commutator in a DC machine?

*Concept from scratch:* The **commutator** is a mechanical rectifier — a set of copper segments mounted on the armature shaft, insulated from each other and from the shaft, contacted by stationary carbon brushes. Its function is to reverse the connection between the armature winding and the external circuit at exactly the right instants (as the armature rotates) so that:
- In a **generator**, the internally-induced AC EMF in the armature conductors is converted into a unidirectional (DC) output at the brushes.
- In a **motor**, the DC supply current is switched into the correct armature conductors at the correct instants to maintain a continuous, unidirectional torque in one direction as the armature rotates.

---

**Q7. [Unit IV | Topic: Back EMF | Type: Theory | Difficulty: Basic]**

**Question:** Define back EMF in a DC motor. What is its significance in speed control and torque production?

*Concept from scratch:* **Back EMF (E_b)** is the EMF induced in the armature conductors of a DC motor as they rotate through the magnetic field — by Lenz's law, this induced EMF opposes the applied supply voltage (hence "back" EMF). E_b = V − I_aR_a.

*Significance:*
- **Speed control:** Since E_b = (ΦZNP)/(60A) ∝ ΦN, and E_b ≈ V − I_aR_a is largely set by the supply and loading, controlling either the field flux Φ or the armature circuit resistance/voltage effectively controls the motor's speed N.
- **Torque production / self-regulation:** Back EMF automatically limits the armature current to just what's needed to meet the load torque — if the load increases, the motor slows slightly, E_b drops, and armature current I_a=(V−E_b)/R_a increases (increasing torque to match the new load); the motor thus self-regulates without external intervention.

---

**Q8. [Unit IV | Topic: Generator Characteristics | Type: Theory | Difficulty: Basic]**

**Question:** Define the open-circuit characteristic (O.C.C. / magnetization characteristic) of a DC generator.

*Concept from scratch:* The **open-circuit characteristic (O.C.C.)**, also called the magnetization characteristic, is a plot of the generator's induced EMF (E) against field current (I_f), with the generator running at constant (rated) speed and the armature terminals left open (no load current flowing). It shows how the generated EMF grows with field current, following the shape of the machine's magnetic B-H characteristic — rising nearly linearly at low field current, then flattening as the core approaches magnetic saturation. It's used to predict the generator's no-load voltage for any given field excitation.

---

**Q9. [Unit IV | Topic: Motor Characteristics | Type: Theory | Difficulty: Basic]**

**Question:** Sketch and briefly describe the speed-torque characteristic of a DC shunt motor.

*Concept from scratch (DC shunt motor speed-torque characteristic):* In a shunt motor, the field winding is connected directly across the supply, so flux Φ remains **essentially constant** regardless of load (armature current). Since T ∝ ΦI_a and N ∝ E_b/Φ (with E_b nearly constant, dropping only slightly as I_a increases due to the I_aR_a drop), the speed **drops only slightly** as load (torque) increases — giving a nearly flat, gently drooping straight-line speed-torque characteristic. This makes the shunt motor essentially a **constant-speed** machine, suitable for applications needing steady speed under varying load, like machine tools and fans.

---

**Q10. [Unit IV | Topic: Motor Characteristics | Type: Theory | Difficulty: Basic]**

**Question:** Sketch and briefly describe the speed-torque characteristic of a DC series motor.

*Concept from scratch (DC series motor speed-torque characteristic):* In a series motor, the field winding carries the full armature current, so flux Φ is **not constant** — it varies (increases) with armature current I_a (approximately proportional to I_a before saturation). Since T ∝ ΦI_a ∝ I_a² (before saturation), torque rises very steeply with current — giving very **high starting torque**. Since N ∝ E_b/Φ, and Φ ∝ I_a, at light load (low I_a, low Φ) the speed becomes very **high** (theoretically dangerously high or unbounded at no load — series motors must never be run unloaded/belt-driven without a fixed coupling). This produces a characteristic **hyperbola-like curve**: very high torque at low speed, and very high speed at low torque — well suited to traction/hoist applications (e.g., cranes, trains) needing high starting torque under heavy load.

---

**Q11. [Unit IV | Topic: Single-Phase Induction Motor | Type: Theory | Difficulty: Basic]**

**Question:** Explain the "double revolving field theory" as applied to a single-phase induction motor.

*Concept from scratch:* The **double revolving field theory** explains the behavior of a single-phase induction motor's pulsating (alternating, non-rotating) stator MMF by mathematically decomposing it into **two equal-magnitude rotating magnetic fields**, rotating at synchronous speed in **opposite directions** — one "forward" (in the direction the motor is meant to run) and one "backward."

Each of these two rotating fields independently induces its own torque on the rotor (exactly as in a normal three-phase induction motor, but each with half the total effective MMF). At standstill, both fields produce equal-magnitude torques but in opposite directions, so the **net torque is zero at standstill**. Once the rotor is started (by some external means), the slip with respect to the forward field decreases while slip with respect to the backward field increases; this makes the forward-field torque dominate over the (now much weaker) backward-field torque, producing a **net non-zero torque** in the direction of rotation, which sustains the motor's running operation.

---

**Q12. [Unit IV | Topic: Single-Phase Induction Motor | Type: Theory | Difficulty: Basic]**

**Question:** Why is a single-phase induction motor not self-starting?

*Concept from scratch:* At standstill, a single-phase stator winding produces a **purely pulsating (alternating) magnetic field** along one fixed axis, not a rotating field (unlike a three-phase winding, whose currents, being 120° apart in time and space, combine to produce a genuinely rotating field). As explained by the double revolving field theory (Q11), this pulsating field is equivalent to two counter-rotating fields of equal magnitude — since they're equal at standstill, they produce equal and opposite torques, which exactly **cancel out**, giving **zero net starting torque**. Hence a single-phase induction motor cannot start on its own and needs an auxiliary starting mechanism to create an initial rotating-field effect (or an initial push) to break this symmetry.

---

**Q13. [Unit IV | Topic: Single-Phase Induction Motor Starting | Type: Theory | Difficulty: Basic]**

**Question:** Name the different starting methods used for single-phase induction motors.

*Concept from scratch:* Common starting methods for single-phase induction motors:

1. **Split-phase (resistance-start) motor**

2. **Capacitor-start induction-run motor**

3. **Capacitor-start capacitor-run motor**

4. **Permanent split-capacitor (PSC) motor**

5. **Shaded-pole motor**

Each method creates an artificial phase difference between two stator windings (main and auxiliary) so their combined MMF approximates a rotating field at starting, breaking the standstill torque symmetry described in Q12.

---

**Q14. [Unit IV | Topic: Single-Phase Induction Motor Starting | Type: Theory | Difficulty: Intermediate]**

**Question:** Explain the working of a capacitor-start induction-run single-phase motor.

*Concept from scratch:* This motor has two stator windings — a **main winding** and an **auxiliary (starting) winding** — placed 90° apart in space. A capacitor is connected in series with the auxiliary winding.

*Working:* At starting, both windings are connected across the supply. The capacitor in the auxiliary winding branch causes the current in that winding to lead the current in the main winding by close to 90° in time (ideally). Combined with their 90° spatial displacement, these two out-of-phase currents in spatially-displaced windings produce a genuine (or near-genuine) **rotating magnetic field** at starting, giving the motor good starting torque — this breaks the standstill symmetry and starts rotation. Once the motor reaches about 70–80% of its rated (synchronous) speed, a **centrifugal switch** automatically disconnects the auxiliary winding (and capacitor) from the circuit, and the motor continues running on the main winding alone (behaving like a normal running single-phase induction motor, sustained by the running torque from the double-revolving-field mechanism once already in motion).

---

**Q15. [Unit IV | Topic: Three-Phase Induction Motor Types | Type: Theory | Difficulty: Basic]**

**Question:** Distinguish between a squirrel-cage induction motor and a slip-ring (wound-rotor) induction motor.

*Concept from scratch:*
- **Squirrel-cage induction motor:** The rotor consists of copper/aluminum bars embedded in slots around the rotor core, short-circuited at both ends by end rings (resembling a rotating "squirrel cage" — hence the name) — there is no external electrical connection to the rotor, and no provision to insert external resistance.
- **Slip-ring (wound-rotor) induction motor:** The rotor winding is a proper three-phase winding (similar to the stator), with its three winding ends brought out to three insulated slip rings mounted on the shaft, contacted by brushes — this allows external resistance to be connected into the rotor circuit (useful for speed control and improving starting torque), unlike the squirrel-cage type.

---

**Q16. [Unit IV | Topic: Three-Phase Induction Motor | Type: Theory | Difficulty: Basic]**

**Question:** Define slip in a three-phase induction motor. Write its formula.

*Concept from scratch:* **Slip (s)** is the fractional difference between the synchronous speed (speed of the rotating stator field) and the actual rotor speed, expressed relative to synchronous speed — it exists because the rotor must always rotate slightly slower than the stator field (otherwise no relative motion, no induced rotor EMF, and no torque would be produced — hence induction motors are also called "asynchronous" motors).

**s = (N_s − N_r)/N_s**

where N_s = synchronous speed, N_r = actual rotor speed. Often expressed as a percentage.

---

**Q17. [Unit IV | Topic: Torque-Slip Characteristic | Type: Theory | Difficulty: Intermediate]**

**Question:** Describe the torque-slip characteristic of a three-phase induction motor, identifying the starting, maximum (pull-out), and running-torque regions.

*Concept from scratch:* The torque-slip characteristic of a three-phase induction motor shows torque plotted against slip, from s=0 (synchronous speed, zero slip) to s=1 (standstill, full slip):

- **Starting region (s=1, near standstill):** Torque starts at a certain finite value (the starting torque) — the exact value depends on rotor resistance.
- **Low-slip / normal running region (small s, near s=0):** In this region, torque is **approximately proportional to slip** — a nearly straight-line, stable relationship. The motor operates here under normal running conditions, where torque increases roughly linearly as load (and hence slip) increases from no-load to full-load.
- **Maximum (pull-out) torque region:** As slip increases beyond the normal running range, torque rises to a maximum value (called breakdown or pull-out torque) at a particular slip value s_m, beyond which further increase in slip actually causes torque to **decrease** again. Operating beyond this point is unstable — if the load torque exceeds the pull-out torque, the motor stalls (slip runs away toward s=1) rather than finding a new stable operating point.

*Overall shape:* Torque rises from its starting value, through the linear low-slip region, up to a peak (pull-out torque) at some intermediate slip, then falls back down as slip approaches 1 — a distinctive rising-then-falling curve.

---

**Q18. [Unit IV | Topic: Three-Phase Induction Motor | Type: Theory | Difficulty: Basic]**

**Question:** Define synchronous speed of a three-phase induction motor and write its formula in terms of supply frequency and number of poles.

*Concept from scratch:* **Synchronous speed (N_s)** is the speed at which the rotating magnetic field produced by the stator windings rotates — determined purely by the supply frequency and the number of poles the winding is designed for:

**N_s = (120 f)/P**

where f = supply frequency (Hz), P = number of poles. (The rotor itself always runs slightly slower than this, as explained in Q16.)

---

### Section B: Numerical Problems

**Q19. [Unit IV | Topic: EMF Equation | Type: Numerical | Difficulty: Basic]**

**Question:** A 4-pole DC generator has 500 armature conductors, wave-wound, and runs at 1200 rpm. If the flux per pole is 0.02 Wb, calculate the generated EMF.

*Step 1 — For wave winding, number of parallel paths A=2 (fixed, regardless of number of poles).*

*Step 2 — Apply the EMF equation:*
E_g = (ΦZNP)/(60A)

*Step 3 — Substitute:*
E_g = (0.02 × 500 × 1200 × 4)/(60 × 2)

*Step 4 — Compute numerator step by step:*
0.02 × 500 = 10
10 × 1200 = 12,000
12,000 × 4 = 48,000

*Step 5 — Compute denominator:*
60 × 2 = 120

*Step 6 — Divide:*
E_g = 48,000/120 = **400 V**

---

**Q20. [Unit IV | Topic: EMF Equation | Type: Numerical | Difficulty: Basic]**

**Question:** A DC generator with a lap-wound armature has 6 poles, 720 conductors, and generates an EMF of 240 V at 1000 rpm. Find the flux per pole.

*Step 1 — For lap winding, number of parallel paths A=P=6.*

*Step 2 — Apply the EMF equation, rearranged to solve for Φ:*
E_g = (ΦZNP)/(60A)  ⟹  Φ = (E_g × 60A)/(ZNP)

*Step 3 — Substitute:*
Φ = (240 × 60 × 6)/(720 × 1000 × 6)

*Step 4 — Compute numerator:*
240×60 = 14,400
14,400×6 = 86,400

*Step 5 — Compute denominator:*
720×1000 = 720,000
720,000×6 = 4,320,000

*Step 6 — Divide:*
Φ = 86,400/4,320,000 = **0.02 Wb**

---

**Q21. [Unit IV | Topic: Torque Equation | Type: Numerical | Difficulty: Intermediate]**

**Question:** A DC motor draws an armature current of 25 A at 220 V and runs at 1000 rpm. The armature resistance is 0.5 Ω. Calculate the back EMF and the electromagnetic torque developed.

*Step 1 — Compute back EMF:*
E_b = V − I_aR_a = 220 − (25×0.5) = 220 − 12.5 = **207.5 V**

*Step 2 — Compute electromagnetic torque using the power-balance relation T = (E_b × I_a × 60)/(2πN):*

*Step 2a — First compute the gross mechanical power developed:*
P_dev = E_b × I_a = 207.5 × 25 = **5187.5 W**

*Step 2b — Convert rotational speed to angular velocity ω (rad/s):*
ω = 2πN/60 = (2×3.1416×1000)/60 = 6283.2/60 = **104.72 rad/s**

*Step 2c — Torque = Power/angular velocity:*
T = P_dev/ω = 5187.5/104.72 = **49.53 N·m**

---

**Q22. [Unit IV | Topic: DC Motor Speed | Type: Numerical | Difficulty: Intermediate]**

**Question:** A DC shunt motor takes 20 A from a 230 V supply and has an armature resistance of 0.4 Ω. If the flux per pole is constant, find the speed of the motor if the no-load speed (at the same flux) was 1000 rpm with a back EMF of 220 V and the loaded back EMF is now 214 V.

*Step 1 — Concept:* Since flux Φ is constant (shunt motor, constant field), speed is directly proportional to back EMF: N ∝ E_b. So we can find the new speed using a simple ratio.

*Step 2 — Set up the proportion:*
N₂/N₁ = E_b2/E_b1

*Step 3 — Solve for N₂:*
N₂ = N₁ × (E_b2/E_b1) = 1000 × (214/220) = 1000 × 0.9727 = **972.7 rpm**

*(Note: The given armature current 20A and R_a=0.4Ω are consistent background data — e.g., confirming E_b2 = V−I R_a = 230−20×0.4 = 230−8 = 222V would be the value if I=20A applied at loaded condition; the problem directly supplies E_b2=214V for the actual loaded condition, so that value is used directly as given.)*

---

**Q23. [Unit IV | Topic: DC Generator Characteristics | Type: Numerical | Difficulty: Basic]**

**Question:** A shunt generator has a terminal voltage of 220 V, supplies a load current of 50 A, has an armature resistance of 0.2 Ω, and a field current of 2 A. Find the generated EMF and the armature current.

*Step 1 — Concept:* In a shunt generator, the armature supplies both the load current and the field current (since the field winding is connected in parallel with the armature/load, drawing from the same source):
I_a = I_load + I_field

*Step 2 — Compute armature current:*
I_a = 50 + 2 = **52 A**

*Step 3 — Compute generated EMF (armature must supply the terminal voltage plus the internal I_aR_a drop):*
E_g = V + I_aR_a = 220 + (52×0.2) = 220 + 10.4 = **230.4 V**

---

**Q24. [Unit IV | Topic: Three-Phase Induction Motor Slip | Type: Numerical | Difficulty: Basic]**

**Question:** A 4-pole, three-phase induction motor is connected to a 50 Hz supply. If the rotor runs at 1440 rpm, calculate the synchronous speed and the slip.

*Step 1 — Synchronous speed:*
N_s = (120f)/P = (120×50)/4 = 6000/4 = **1500 rpm**

*Step 2 — Slip:*
s = (N_s−N_r)/N_s = (1500−1440)/1500 = 60/1500 = 0.04

**s = 0.04 = 4%**

---

**Q25. [Unit IV | Topic: Three-Phase Induction Motor Slip | Type: Numerical | Difficulty: Basic]**

**Question:** A 6-pole induction motor operates on a 50 Hz supply with a slip of 4%. Determine the synchronous speed and the actual rotor speed.

*Step 1 — Synchronous speed:*
N_s = (120f)/P = (120×50)/6 = 6000/6 = **1000 rpm**

*Step 2 — Rearrange slip formula to find rotor speed:*
s = (N_s−N_r)/N_s  ⟹  N_r = N_s(1−s)

*Step 3 — Substitute:*
N_r = 1000 × (1−0.04) = 1000 × 0.96 = **960 rpm**

---

**Q26. [Unit IV | Topic: Rotor Frequency | Type: Numerical | Difficulty: Intermediate]**

**Question:** A three-phase induction motor has a synchronous speed of 1500 rpm and runs at 1425 rpm on full load. If the supply frequency is 50 Hz, find the slip and the rotor (frequency of induced EMF) frequency.

*Step 1 — Compute slip:*
s = (N_s−N_r)/N_s = (1500−1425)/1500 = 75/1500 = **0.05 (5%)**

*Step 2 — Rotor (induced EMF) frequency:* Since the rotor's induced EMF frequency depends on the relative speed between the rotating field and the rotor (i.e., the slip speed), the rotor frequency is simply the slip multiplied by the supply frequency:
f_r = s × f = 0.05 × 50 = **2.5 Hz**

---

**Q27. [Unit IV | Topic: DC Motor Power | Type: Numerical | Difficulty: Intermediate]**

**Question:** A DC series motor takes 30 A from a 230 V supply. The armature resistance is 0.3 Ω and the series field resistance is 0.2 Ω. Calculate the back EMF, the power developed by the armature, and the electromagnetic torque if the motor runs at 900 rpm.

*Step 1 — Total armature-circuit resistance (armature + series field, both carry the same current I=30A in a series motor):*
R_total = R_a + R_se = 0.3+0.2 = **0.5 Ω**

*Step 2 — Back EMF:*
E_b = V − I×R_total = 230 − (30×0.5) = 230−15 = **215 V**

*Step 3 — Power developed by the armature:*
P_dev = E_b × I = 215 × 30 = **6450 W**

*Step 4 — Convert speed to angular velocity:*
ω = 2πN/60 = (2×3.1416×900)/60 = 5654.9/60 = **94.25 rad/s**

*Step 5 — Electromagnetic torque:*
T = P_dev/ω = 6450/94.25 = **68.44 N·m**

---

### Section C: Advanced Theory & Numericals

**Q28. [Unit IV | Topic: EMF Equation | Type: Theory | Difficulty: Advanced]**

**Question:** Derive the EMF equation of a DC generator from first principles, starting with the EMF induced in a single conductor and extending it to the complete armature winding with A parallel paths.

*Step 1 — EMF induced in a single conductor.* As the armature rotates at N rpm, each conductor moves through the magnetic field. Consider one pole pair: in one revolution, a conductor sweeps past all P poles, cutting the total flux (Φ per pole × P poles) = PΦ webers of flux linkage change, in the time taken for one revolution.

*Step 2 — Time for one revolution:*
Speed N is in rpm, so revolutions per second = N/60. Time for one revolution, t = 60/N seconds.

*Step 3 — EMF induced in a single conductor (by Faraday's law, e = rate of change of flux linkage):*
e_conductor = (Total flux cut per revolution)/(time per revolution) = (PΦ)/(60/N) = **PΦN/60**

*Step 4 — Extend to the full armature winding.* The armature has Z total conductors, arranged into A parallel paths (so each parallel path contains Z/A conductors in series).

*Step 5 — EMF of one parallel path (conductors in series add their EMFs):*
E_path = (Z/A) × e_conductor = (Z/A) × (PΦN/60)

*Step 6 — Recognize that all A parallel paths are connected between the same two brushes, so they all present the same EMF (each path being electrically identical by winding symmetry) — hence the total generated EMF equals the EMF of just one path (parallel paths of equal EMF don't add in series; the terminal EMF is simply that of one path):*

**E_g = (ΦZNP)/(60A)**

*Step 7 — Definition of symbols:* Φ = flux per pole (Wb); Z = total number of armature conductors; N = armature speed (rpm); P = number of poles; A = number of parallel paths in the armature winding (A=P for lap winding, A=2 for wave winding).

---

**Q29. [Unit IV | Topic: Torque-Slip Characteristic | Type: Theory | Difficulty: Advanced]**

**Question:** Derive the expression for torque developed by a three-phase induction motor in terms of slip, and show mathematically how maximum torque and the slip at which it occurs are obtained from this expression.

*Step 1 — Set up the rotor-circuit equivalent per phase.* At slip s, the rotor induced EMF per phase is E₂s = sE₂ (where E₂ is the standstill rotor EMF per phase), the rotor reactance per phase becomes X₂s = sX₂ (since reactance is frequency-dependent, and rotor frequency scales with slip), while rotor resistance R₂ stays constant (resistance doesn't depend on frequency).

*Step 2 — Rotor current per phase at slip s:*
I₂ = (sE₂)/√(R₂² + (sX₂)²)

*Step 3 — Torque is proportional to (rotor current) × (rotor EMF) × (power factor of rotor circuit), which combines to the standard induction-motor torque expression:*

T ∝ (E₂² s R₂) / [R₂² + (sX₂)²]

(Derivation intuition: Torque ∝ Rotor Cu-loss-generating power/synchronous speed, and rotor power per phase = I₂² R₂/s = [s²E₂²/(R₂²+(sX₂)²)] × R₂/s = sE₂²R₂/(R₂²+(sX₂)²), consistent with the above.)

*Step 4 — Introduce a proportionality constant k (absorbing synchronous speed and phase-number factors) for a cleaner working expression:*

**T = k · (sE₂²R₂) / (R₂² + s²X₂²)**

*Step 5 — Maximize T with respect to slip s.* Treat T as a function of s; differentiate using the quotient rule, with numerator u = sE₂²R₂ (so du/ds = E₂²R₂) and denominator w = R₂²+s²X₂² (so dw/ds = 2sX₂²):

dT/ds = k · [ (R₂²+s²X₂²)(E₂²R₂) − (sE₂²R₂)(2sX₂²) ] / (R₂²+s²X₂²)²

*Step 6 — Simplify the numerator:*
= k E₂²R₂ [ (R₂²+s²X₂²) − 2s²X₂² ] / (R₂²+s²X₂²)²
= k E₂²R₂ [ R₂² − s²X₂² ] / (R₂²+s²X₂²)²

*Step 7 — Set numerator to zero for the stationary point (since E₂²R₂ ≠ 0):*
R₂² − s²X₂² = 0
s²X₂² = R₂²
**s_m = R₂/X₂** (taking the positive root, since slip is a positive quantity in the motoring region)

*Step 8 — This is the slip at which maximum (pull-out) torque occurs.* Substitute s_m = R₂/X₂ back into the torque expression (Step 4) to find T_max:

T_max = k · [(R₂/X₂)E₂²R₂] / [R₂² + (R₂/X₂)²X₂²]
= k · [E₂²R₂²/X₂] / [R₂² + R₂²]
= k · [E₂²R₂²/X₂] / [2R₂²]
= k · E₂²/(2X₂)

**T_max = k E₂²/(2X₂)**

*Step 9 — Key observations:* Notice T_max is **independent of rotor resistance R₂** — changing R₂ (e.g., via external rotor resistance in a slip-ring motor) does not change the *value* of maximum torque, but it does change the *slip* s_m = R₂/X₂ at which that maximum occurs — increasing R₂ shifts the peak toward higher slip (useful for improving starting torque in wound-rotor motors, since a higher R₂ can move the peak torque point all the way to s=1, i.e., to standstill).

---

**Q30. [Unit IV | Topic: DC Motor Speed Control | Type: Numerical | Difficulty: Advanced]**

**Question:** A DC shunt motor runs at 1000 rpm on a 230 V supply, drawing an armature current of 20 A with armature resistance 0.5 Ω. Find the additional resistance to be inserted in the armature circuit to reduce the speed to 800 rpm at the same torque (same armature current), assuming flux remains constant.

*Step 1 — Compute back EMF at the original condition (before adding extra resistance):*
E_b1 = V − I_aR_a = 230 − (20×0.5) = 230−10 = **220 V**

*Step 2 — Since flux Φ is constant (given), speed is proportional to back EMF: N ∝ E_b. Use this to find the required back EMF at the new (lower) speed:*
E_b2/E_b1 = N₂/N₁
E_b2 = E_b1 × (N₂/N₁) = 220 × (800/1000) = 220 × 0.8 = **176 V**

*Step 3 — Since armature current I_a is unchanged (same torque, same flux, so same I_a needed by T∝ΦI_a), write the new voltage equation including the extra series resistance R_x:*
V = E_b2 + I_a(R_a + R_x)

*Step 4 — Rearrange to solve for R_x:*
V − E_b2 = I_a(R_a+R_x)
(V−E_b2)/I_a = R_a + R_x
R_x = (V−E_b2)/I_a − R_a

*Step 5 — Substitute values:*
R_x = (230−176)/20 − 0.5 = 54/20 − 0.5 = 2.7 − 0.5 = **2.2 Ω**

*Result:* An additional **2.2 Ω** resistance must be inserted in series with the armature circuit to reduce the speed from 1000 rpm to 800 rpm at the same armature current (same torque).

---

**Q31. [Unit IV | Topic: Three-Phase Induction Motor Torque | Type: Numerical | Difficulty: Advanced]**

**Question:** A three-phase, 4-pole, 50 Hz induction motor has a full-load slip of 4%. The rotor standstill EMF per phase is 100 V and the rotor resistance and standstill reactance per phase are 0.3 Ω and 1.5 Ω respectively. Calculate the full-load torque developed and the maximum torque, along with the slip at which maximum torque occurs.

*Step 1 — Synchronous speed:*
N_s = 120f/P = (120×50)/4 = **1500 rpm**

*Step 2 — Full-load torque, using the torque expression T = k·sE₂²R₂/(R₂²+s²X₂²), where k = 3/(2πN_s/60) [the "3" accounts for three phases; here we compute the proportionality constant explicitly to get actual torque in N·m]:*

*Step 2a — Compute ω_s (synchronous angular speed):*
ω_s = 2πN_s/60 = (2×3.1416×1500)/60 = 9424.8/60 = **157.08 rad/s**

*Step 2b — Full torque formula (per-phase rotor power/synchronous speed, ×3 for three phases):*
T = 3 × [s E₂² R₂ / (R₂² + s²X₂²)] / ω_s

*Step 3 — At full load, s=0.04:*

Compute s²X₂² = (0.04)² × (1.5)² = 0.0016 × 2.25 = 0.0036
R₂² = 0.3² = 0.09
Denominator = R₂² + s²X₂² = 0.09+0.0036 = 0.0936

Numerator (before ×3 and /ω_s) = s E₂² R₂ = 0.04 × 100² × 0.3 = 0.04×10000×0.3 = 120

So [sE₂²R₂/(R₂²+s²X₂²)] = 120/0.0936 = 1282.05

*Step 4 — Full-load torque:*
T_FL = 3 × 1282.05 / 157.08 = 3846.15/157.08 = **24.49 N·m**

*Step 5 — Maximum torque: first find slip at maximum torque, s_m = R₂/X₂:*
s_m = 0.3/1.5 = **0.2 (20%)**

*Step 6 — Maximum torque value using T_max = k E₂²/(2X₂), with the same constant structure as above (3/ω_s replacing k):*
T_max = 3 × [E₂²/(2X₂)] / ω_s = 3 × [100²/(2×1.5)] / 157.08 = 3 × [10000/3] / 157.08 = 3 × 3333.3/157.08 = 10,000/157.08

**T_max = 63.66 N·m**

*Step 7 — Summary:* **Full-load torque ≈ 24.49 N·m** (at s=0.04), **Maximum (pull-out) torque ≈ 63.66 N·m** (at s_m=0.2) — confirming the motor operates well below its pull-out torque at full load (a healthy margin, roughly 2.6× the full-load torque, typical for practical induction motor design).

---

**Q32. [Unit IV | Topic: Single-Phase Induction Motor | Type: Theory | Difficulty: Advanced]**

**Question:** Using the double revolving field theory, explain quantitatively how the forward and backward rotating flux components produce a net starting torque of zero but a non-zero net running torque once the rotor is set in motion by an external means.

*Step 1 — Represent the pulsating stator MMF mathematically.* A single-phase winding carrying alternating current I_m cos(ωt) produces a stationary (non-rotating), pulsating MMF wave along its axis:
F(θ,t) = F_max cos(θ) cos(ωt)

where θ is the spatial angle around the airgap.

*Step 2 — Decompose using the product-to-sum trigonometric identity:*
cos(θ)cos(ωt) = ½cos(θ−ωt) + ½cos(θ+ωt)

So: F(θ,t) = (F_max/2)cos(θ−ωt) + (F_max/2)cos(θ+ωt)

*Step 3 — Interpret each term as a traveling wave:*
- The term (F_max/2)cos(θ−ωt) represents a wave of constant amplitude F_max/2 that travels in the **+θ direction** (forward) at synchronous angular speed ω — this is the **forward rotating field**.
- The term (F_max/2)cos(θ+ωt) represents a wave of the same amplitude F_max/2 traveling in the **−θ direction** (backward) at the same synchronous speed — the **backward rotating field**.

*Step 4 — At standstill (rotor speed = 0):* The rotor's slip with respect to the forward field is s_f = 1 (full slip, exactly as in a normal motor at standstill), and its slip with respect to the backward field is also s_b = 1 (equal full slip, since the backward field also appears to move at full synchronous speed relative to the stationary rotor, just in the opposite direction). Since both fields have equal magnitude (F_max/2 each) and equal slip (s=1 each) relative to the stationary rotor, they induce **equal-magnitude torques acting in opposite directions** — these torques exactly cancel: **T_net = T_forward − T_backward = 0** at standstill.

*Step 5 — Once the rotor is started (say, in the forward direction) by an external means, reaching some speed N_r:* The slip with respect to the forward field decreases: s_f = (N_s−N_r)/N_s < 1. But the slip with respect to the backward field (which appears to move in the opposite direction, so the rotor now moves "against" it even more) becomes: s_b = (−N_s−N_r)/(−N_s) = (N_s+N_r)/N_s = 2−s_f, which is **greater than 1**.

*Step 6 — Since torque generally decreases as slip moves away from the low-slip region toward and beyond the pull-out point (referring to the standard torque-slip curve shape from Q17, here evaluated at large slip values close to or above 1, well past the peak), the backward field's torque (at its now-high slip s_b>1, actually now acting as a **retarding/braking** torque in the direction of rotation, since s_b>1 corresponds to the "plugging" braking region of that field's own torque-slip curve) becomes significantly **smaller in magnitude** than the forward field's torque (now at its much more favorable, lower slip s_f<1, closer to its own peak-torque region).**

*Step 7 — Net result:* T_net = T_forward(s_f) − T_backward(s_b) is now **non-zero and positive** (in the direction of rotation), since T_forward has grown relatively larger (lower, more favorable slip) while T_backward has shrunk (higher, less favorable slip, now even acting as increased drag) — this net torque **sustains and reinforces** the rotor's motion in the direction it was started, allowing the motor to continue running and accelerate up toward its normal operating speed, even though it could not start on its own from rest.

---

**Q33. [Unit IV | Topic: DC Machine Losses & Efficiency | Type: Numerical | Difficulty: Advanced]**

**Question:** A DC shunt generator delivers 100 A at 220 V. The armature resistance is 0.1 Ω, the shunt field resistance is 110 Ω, and the rotational (stray) losses are 500 W. Calculate the generated EMF, the copper losses, and the overall efficiency of the generator.

*Step 1 — Field current:*
I_field = V/R_field = 220/110 = **2 A**

*Step 2 — Armature current (shunt generator supplies both load and field current):*
I_a = I_load + I_field = 100+2 = **102 A**

*Step 3 — Generated EMF:*
E_g = V + I_aR_a = 220 + (102×0.1) = 220+10.2 = **230.2 V**

*Step 4 — Copper losses.* Two components:

*Armature copper loss:*
P_cu,a = I_a²R_a = 102² × 0.1 = 10,404 × 0.1 = **1040.4 W**

*Field copper loss (constant power dissipated in the field winding):*
P_cu,field = V × I_field = 220 × 2 = **440 W**

*Total copper losses:*
P_cu,total = 1040.4 + 440 = **1480.4 W**

*Step 5 — Total losses (copper + rotational/stray, which represents mechanical + iron losses combined as given):*
P_losses,total = P_cu,total + P_rotational = 1480.4 + 500 = **1980.4 W**

*Step 6 — Output power (electrical power delivered to the external load):*
P_out = V × I_load = 220 × 100 = **22,000 W**

*Step 7 — Input power (mechanical power supplied to the generator shaft = output + all losses):*
P_input = P_out + P_losses,total = 22,000 + 1980.4 = **23,980.4 W**

*Step 8 — Overall efficiency:*
η = P_out/P_input = 22,000/23,980.4 = 0.9174

**η ≈ 91.74%**

-e 

---

