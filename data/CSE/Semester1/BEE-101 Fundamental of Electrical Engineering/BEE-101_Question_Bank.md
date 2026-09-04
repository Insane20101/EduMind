# BEE-101 — Fundamentals of Electrical Engineering
## Complete Unit-Wise Question Bank (Theory + Numericals, Basic → Advanced)

> **Course:** BEE-101 — Fundamentals of Electrical Engineering
> **Credits:** 5
> **Coverage:** Strictly mapped to the 4-unit syllabus below. No topics outside the syllabus are included.
> **Format note:** Each question is tagged with `Unit`, `Topic`, `Type` (Theory/Numerical), and `Difficulty` (Basic/Intermediate/Advanced) for structured retrieval.

---

## Syllabus Reference (source of truth for this question bank)

- **Unit I:** DC Circuit Analysis and Network Theorems — network concepts, active/passive elements, voltage/current sources, linearity, source transformation, Kirchhoff's laws, loop and nodal analysis, star-delta transformation, Superposition, Thevenin's, Norton's, Maximum Power Transfer theorems.
- **Unit II:** Steady-State Analysis of Single-Phase AC Circuits — sinusoidal/square/triangular waveforms, average/effective values, phasors, series/parallel/series-parallel RLC circuits, resonance. Three Phase AC Circuits — star/delta connections, balanced supply/load, power measurement.
- **Unit III:** Magnetic Circuit & Single-Phase Transformers — magnetic circuit concepts, B-H curve, hysteresis, eddy current losses. Transformer: principle, construction, EMF equation, power losses, efficiency, O.C. & S.C. tests, auto transformer.
- **Unit IV:** Electrical Machines — electromechanical energy conversion, DC machine types, EMF/torque equations, generator/motor characteristics; Single Phase Induction Motor — principle, starting methods; Three Phase Induction Motor — types, torque-slip characteristics.

---

## UNIT I — DC Circuit Analysis and Network Theorems

### Section A: Definitions & Concept Questions (Basic, 2–3 Marks)

1. **[Unit I | Topic: Network Concepts | Type: Theory | Difficulty: Basic]**
   Define the terms: node, branch, loop, and mesh in an electrical network.

2. **[Unit I | Topic: Active/Passive Elements | Type: Theory | Difficulty: Basic]**
   Distinguish between active and passive circuit elements with examples.

3. **[Unit I | Topic: Sources | Type: Theory | Difficulty: Basic]**
   Differentiate between an ideal voltage source and an ideal current source.

4. **[Unit I | Topic: Sources | Type: Theory | Difficulty: Basic]**
   Define a practical (real) voltage source and a practical current source. Draw their equivalent circuits.

5. **[Unit I | Topic: Linearity | Type: Theory | Difficulty: Basic]**
   State the properties that make a circuit "linear." Give one linear and one non-linear circuit element.

6. **[Unit I | Topic: Source Transformation | Type: Theory | Difficulty: Basic]**
   What is source transformation? State the condition under which a voltage source can be converted to an equivalent current source.

7. **[Unit I | Topic: Kirchhoff's Laws | Type: Theory | Difficulty: Basic]**
   State Kirchhoff's Current Law (KCL) and Kirchhoff's Voltage Law (KVL).

8. **[Unit I | Topic: Kirchhoff's Laws | Type: Theory | Difficulty: Basic]**
   On what fundamental physical principles are KCL and KVL based?

9. **[Unit I | Topic: Loop/Nodal Analysis | Type: Theory | Difficulty: Basic]**
   Define mesh (loop) current and node voltage as used in circuit analysis.

10. **[Unit I | Topic: Star-Delta Transformation | Type: Theory | Difficulty: Basic]**
    Write the formulae for converting a star-connected resistor network to an equivalent delta network.

11. **[Unit I | Topic: Star-Delta Transformation | Type: Theory | Difficulty: Basic]**
    Write the formulae for converting a delta-connected resistor network to an equivalent star network.

12. **[Unit I | Topic: Superposition Theorem | Type: Theory | Difficulty: Basic]**
    State the Superposition theorem. What condition must the network satisfy for it to be applicable?

13. **[Unit I | Topic: Thevenin's Theorem | Type: Theory | Difficulty: Basic]**
    State Thevenin's theorem. Define Thevenin's voltage (V_th) and Thevenin's resistance (R_th).

14. **[Unit I | Topic: Norton's Theorem | Type: Theory | Difficulty: Basic]**
    State Norton's theorem. Define Norton's current (I_N) and Norton's resistance (R_N).

15. **[Unit I | Topic: Thevenin/Norton Equivalence | Type: Theory | Difficulty: Basic]**
    State the relationship between Thevenin's and Norton's equivalent circuit parameters.

16. **[Unit I | Topic: Maximum Power Transfer | Type: Theory | Difficulty: Basic]**
    State the Maximum Power Transfer theorem for a DC circuit.

17. **[Unit I | Topic: Maximum Power Transfer | Type: Theory | Difficulty: Intermediate]**
    Derive the condition for maximum power transfer to the load resistance R_L from a source with internal resistance R_s.

18. **[Unit I | Topic: Network Concepts | Type: Theory | Difficulty: Intermediate]**
    Explain the difference between a planar and a non-planar network. Why does mesh analysis apply only to planar networks?

19. **[Unit I | Topic: Loop/Nodal Analysis | Type: Theory | Difficulty: Intermediate]**
    Compare mesh (loop) analysis and nodal analysis — when is one preferred over the other?

20. **[Unit I | Topic: Superposition Theorem | Type: Theory | Difficulty: Intermediate]**
    Explain why the Superposition theorem is not valid for power calculations directly.

### Section B: Numerical Problems (Basic → Intermediate)

21. **[Unit I | Topic: Kirchhoff's Laws | Type: Numerical | Difficulty: Basic]**
    A circuit has three resistors of 2 Ω, 3 Ω, and 5 Ω connected in series across a 20 V DC source. Find the current through each resistor and the voltage drop across each.

22. **[Unit I | Topic: Kirchhoff's Laws | Type: Numerical | Difficulty: Basic]**
    Three resistors of 4 Ω, 6 Ω, and 12 Ω are connected in parallel across a 24 V supply. Find the total current drawn from the source and the current through each branch.

23. **[Unit I | Topic: Star-Delta Transformation | Type: Numerical | Difficulty: Basic]**
    A star-connected network has resistances R_a = 10 Ω, R_b = 10 Ω, R_c = 10 Ω. Find the equivalent delta network resistances.

24. **[Unit I | Topic: Star-Delta Transformation | Type: Numerical | Difficulty: Intermediate]**
    A delta network has R_AB = 30 Ω, R_BC = 30 Ω, R_CA = 30 Ω. Convert it into an equivalent star network and verify the total resistance between any two terminals matches in both configurations.

25. **[Unit I | Topic: Loop Analysis | Type: Numerical | Difficulty: Intermediate]**
    Using mesh analysis, find the current in each branch of a two-loop DC network containing two voltage sources (10 V and 5 V) and three resistors (2 Ω, 3 Ω, 4 Ω) arranged in a standard two-mesh configuration.

26. **[Unit I | Topic: Nodal Analysis | Type: Numerical | Difficulty: Intermediate]**
    Using nodal analysis, determine the node voltages of a circuit with two nodes, a 10 A current source at node 1, a 5 A current source at node 2, and interconnecting resistors of 2 Ω, 4 Ω, and 5 Ω.

27. **[Unit I | Topic: Source Transformation | Type: Numerical | Difficulty: Basic]**
    A voltage source of 12 V with an internal resistance of 4 Ω is to be converted into an equivalent current source. Find the value of the equivalent current source and its parallel resistance.

28. **[Unit I | Topic: Superposition Theorem | Type: Numerical | Difficulty: Intermediate]**
    A circuit has two sources: a 20 V voltage source and a 2 A current source, both acting on a network of 5 Ω and 10 Ω resistors. Using the Superposition theorem, find the current through the 5 Ω resistor.

29. **[Unit I | Topic: Thevenin's Theorem | Type: Numerical | Difficulty: Intermediate]**
    Find the Thevenin's equivalent circuit (V_th and R_th) as seen from terminals A-B for a network consisting of a 20 V source, a 4 Ω series resistor, and a 6 Ω resistor across the output terminals.

30. **[Unit I | Topic: Norton's Theorem | Type: Numerical | Difficulty: Intermediate]**
    For the same network as above, find the Norton's equivalent circuit (I_N and R_N) as seen from terminals A-B.

31. **[Unit I | Topic: Maximum Power Transfer | Type: Numerical | Difficulty: Intermediate]**
    A DC source has an EMF of 30 V and an internal resistance of 5 Ω. Find the value of load resistance R_L for maximum power transfer and calculate the maximum power delivered to the load.

### Section C: Advanced Theory & Numericals

32. **[Unit I | Topic: Loop/Nodal Analysis | Type: Theory | Difficulty: Advanced]**
    Explain the supermesh and supernode techniques used when a current source (respectively voltage source) is shared between two loops (respectively nodes). Illustrate with a labeled circuit diagram description.

33. **[Unit I | Topic: Thevenin's Theorem | Type: Numerical | Difficulty: Advanced]**
    A bridge-type resistive network (five resistors: 10 Ω, 10 Ω, 10 Ω, 10 Ω, and a 20 Ω galvanometer branch) is connected to a 20 V source. Using Thevenin's theorem, find the current through the 20 Ω galvanometer branch.

34. **[Unit I | Topic: Superposition + Source Transformation | Type: Numerical | Difficulty: Advanced]**
    A network contains two voltage sources (15 V, 10 V) and one current source (3 A) distributed across a three-loop resistive network. Using a combination of source transformation and superposition, find the current through the common branch.

35. **[Unit I | Topic: Star-Delta + Nodal Analysis | Type: Numerical | Difficulty: Advanced]**
    A network contains a delta-connected set of three 15 Ω resistors embedded within a larger resistive circuit with two independent sources. Convert the delta to star, redraw the simplified network, and use nodal analysis to find all node voltages.

36. **[Unit I | Topic: Maximum Power Transfer | Type: Numerical | Difficulty: Advanced]**
    For a network with a variable load R_L connected to a Thevenin equivalent (V_th = 24 V, R_th = 8 Ω) in series with a fixed 4 Ω resistor, find R_L for maximum power transfer to R_L and calculate that maximum power. Comment on how the fixed series resistor changes the standard R_L = R_th condition.

---

## UNIT II — Steady-State Analysis of Single-Phase & Three-Phase AC Circuits

### Section A: Definitions & Concept Questions (Basic, 2–3 Marks)

1. **[Unit II | Topic: Waveforms | Type: Theory | Difficulty: Basic]**
   Define a sinusoidal waveform. Write its general mathematical expression.

2. **[Unit II | Topic: Waveforms | Type: Theory | Difficulty: Basic]**
   Sketch and describe a square waveform and a triangular waveform, stating one application of each.

3. **[Unit II | Topic: Average/RMS Values | Type: Theory | Difficulty: Basic]**
   Define the average value and RMS (effective) value of an AC waveform.

4. **[Unit II | Topic: Average/RMS Values | Type: Theory | Difficulty: Basic]**
   Define form factor and peak factor (crest factor) of an AC waveform.

5. **[Unit II | Topic: Phasors | Type: Theory | Difficulty: Basic]**
   What is a phasor? Why is phasor representation used for AC circuit analysis?

6. **[Unit II | Topic: Phasors | Type: Theory | Difficulty: Basic]**
   Define phase and phase difference between two alternating quantities.

7. **[Unit II | Topic: RLC Circuits | Type: Theory | Difficulty: Basic]**
   Define impedance and admittance of an AC circuit. State their SI units.

8. **[Unit II | Topic: RLC Circuits | Type: Theory | Difficulty: Basic]**
   Define reactance. Distinguish between inductive reactance and capacitive reactance.

9. **[Unit II | Topic: RLC Circuits | Type: Theory | Difficulty: Basic]**
   Define power factor. State its significance in AC power systems.

10. **[Unit II | Topic: Resonance | Type: Theory | Difficulty: Basic]**
    Define resonance in a series RLC circuit. Write the expression for resonant frequency.

11. **[Unit II | Topic: Resonance | Type: Theory | Difficulty: Basic]**
    Define bandwidth and quality factor (Q-factor) of a resonant circuit.

12. **[Unit II | Topic: Resonance | Type: Theory | Difficulty: Intermediate]**
    Distinguish between series resonance and parallel resonance in terms of impedance behavior at resonant frequency.

13. **[Unit II | Topic: Three-Phase Circuits | Type: Theory | Difficulty: Basic]**
    Define a balanced three-phase supply. State the phase relationship between the three voltages.

14. **[Unit II | Topic: Three-Phase Circuits | Type: Theory | Difficulty: Basic]**
    Distinguish between star (Y) and delta (Δ) connections in a three-phase system.

15. **[Unit II | Topic: Three-Phase Circuits | Type: Theory | Difficulty: Basic]**
    Write the relationships between line voltage/phase voltage and line current/phase current for a star connection.

16. **[Unit II | Topic: Three-Phase Circuits | Type: Theory | Difficulty: Basic]**
    Write the relationships between line voltage/phase voltage and line current/phase current for a delta connection.

17. **[Unit II | Topic: Power Measurement | Type: Theory | Difficulty: Intermediate]**
    Describe the two-wattmeter method of power measurement in a three-phase circuit. Write the expressions for total power and power factor derived from the two wattmeter readings.

18. **[Unit II | Topic: Three-Phase Power | Type: Theory | Difficulty: Basic]**
    Write the expression for total power in a balanced three-phase circuit in terms of line voltage, line current, and power factor.

### Section B: Numerical Problems (Basic → Intermediate)

19. **[Unit II | Topic: Average/RMS Values | Type: Numerical | Difficulty: Basic]**
    A sinusoidal voltage has a peak value of 200 V. Find its RMS value, average value, and form factor.

20. **[Unit II | Topic: Average/RMS Values | Type: Numerical | Difficulty: Basic]**
    A voltage waveform is given by v(t) = 141.4 sin(314t) V. Determine the RMS value, frequency, and time period.

21. **[Unit II | Topic: Phasors | Type: Numerical | Difficulty: Basic]**
    Two alternating currents are given as i₁ = 10 sin(ωt) A and i₂ = 15 sin(ωt − 30°) A. Represent them as phasors and find the phase difference.

22. **[Unit II | Topic: RLC Series Circuit | Type: Numerical | Difficulty: Basic]**
    A series RL circuit has R = 10 Ω and L = 0.05 H, connected to a 230 V, 50 Hz supply. Find the impedance, current, and power factor.

23. **[Unit II | Topic: RLC Series Circuit | Type: Numerical | Difficulty: Basic]**
    A series RC circuit has R = 15 Ω and C = 100 µF, connected to a 230 V, 50 Hz supply. Find the impedance, current, and phase angle.

24. **[Unit II | Topic: RLC Series Circuit | Type: Numerical | Difficulty: Intermediate]**
    A series RLC circuit has R = 10 Ω, L = 0.1 H, and C = 100 µF, connected across a 230 V, 50 Hz supply. Calculate the impedance, current, power factor, and active power consumed.

25. **[Unit II | Topic: RLC Parallel Circuit | Type: Numerical | Difficulty: Intermediate]**
    A parallel circuit consists of a resistor of 20 Ω in one branch and an inductor of reactance 15 Ω in the other branch, connected across a 100 V, 50 Hz supply. Find the total current and overall power factor.

26. **[Unit II | Topic: Series-Parallel RLC | Type: Numerical | Difficulty: Intermediate]**
    A circuit has a resistor R = 10 Ω in series with a parallel combination of an inductor (X_L = 8 Ω) and a capacitor (X_C = 12 Ω). Find the total impedance of the circuit when connected to a 50 Hz supply.

27. **[Unit II | Topic: Resonance | Type: Numerical | Difficulty: Intermediate]**
    A series RLC circuit has R = 5 Ω, L = 0.2 H, and C = 20 µF. Find the resonant frequency, Q-factor, and bandwidth.

28. **[Unit II | Topic: Resonance | Type: Numerical | Difficulty: Intermediate]**
    A series RLC circuit resonates at 1000 Hz with R = 10 Ω, L = 0.05 H. Determine the value of C and the Q-factor at resonance.

29. **[Unit II | Topic: Three-Phase Star Connection | Type: Numerical | Difficulty: Basic]**
    A balanced star-connected load has a phase voltage of 230 V. Find the line voltage and, if the phase current is 10 A, find the line current.

30. **[Unit II | Topic: Three-Phase Delta Connection | Type: Numerical | Difficulty: Basic]**
    A balanced delta-connected load has a line voltage of 400 V and a phase current of 10 A. Find the phase voltage, line current, and total power if the power factor is 0.8.

31. **[Unit II | Topic: Three-Phase Power | Type: Numerical | Difficulty: Intermediate]**
    A balanced three-phase load draws a line current of 20 A from a 400 V (line) supply at a power factor of 0.85 lagging. Calculate the total active power, reactive power, and apparent power.

### Section C: Advanced Theory & Numericals

32. **[Unit II | Topic: Resonance | Type: Theory | Difficulty: Advanced]**
    Derive the expression for resonant frequency of a series RLC circuit from first principles by equating inductive and capacitive reactance, and explain the variation of current with frequency near resonance using a labeled response curve description.

33. **[Unit II | Topic: Power Measurement | Type: Numerical | Difficulty: Advanced]**
    In a two-wattmeter method used to measure power in a balanced three-phase load, the two wattmeters read W₁ = 5000 W and W₂ = 2000 W. Determine the total power, power factor, and the phase angle of the load.

34. **[Unit II | Topic: Series-Parallel RLC | Type: Numerical | Difficulty: Advanced]**
    A series-parallel AC circuit has a 10 Ω resistor in series with a parallel branch of (R = 15 Ω, L giving X_L = 10 Ω) and (C giving X_C = 20 Ω), all connected to a 230 V, 50 Hz supply. Find the total current, total power factor, and total active power drawn from the supply.

35. **[Unit II | Topic: Three-Phase Circuits | Type: Numerical | Difficulty: Advanced]**
    An unbalanced star-connected three-phase load has phase impedances Z₁ = 10∠0° Ω, Z₂ = 10∠30° Ω, Z₃ = 10∠−30° Ω, connected to a balanced 400 V three-phase supply. Find the phase currents in each branch (assume a four-wire system with neutral).

36. **[Unit II | Topic: Resonance + Q-factor | Type: Numerical | Difficulty: Advanced]**
    A parallel RLC circuit has R = 100 Ω, L = 0.5 H, C = 10 µF. Find the resonant frequency, the dynamic resistance at resonance, and the Q-factor. Explain how parallel resonance differs physically from series resonance in this case.

---

## UNIT III — Magnetic Circuits & Single-Phase Transformers

### Section A: Definitions & Concept Questions (Basic, 2–3 Marks)

1. **[Unit III | Topic: Magnetic Circuit | Type: Theory | Difficulty: Basic]**
   Define magnetomotive force (MMF) and magnetic reluctance. State their units.

2. **[Unit III | Topic: Magnetic Circuit | Type: Theory | Difficulty: Basic]**
   Define magnetic flux and flux density. State their SI units.

3. **[Unit III | Topic: Magnetic Circuit | Type: Theory | Difficulty: Basic]**
   State the analogy between a magnetic circuit and an electric circuit (MMF↔EMF, flux↔current, reluctance↔resistance).

4. **[Unit III | Topic: B-H Curve | Type: Theory | Difficulty: Basic]**
   What is a B-H curve (magnetization curve)? What does its non-linear shape indicate about the magnetic material?

5. **[Unit III | Topic: Hysteresis | Type: Theory | Difficulty: Basic]**
   Define magnetic hysteresis. What does the area of the hysteresis loop represent?

6. **[Unit III | Topic: Hysteresis Loss | Type: Theory | Difficulty: Basic]**
   Define hysteresis loss in a magnetic material. Write Steinmetz's formula for hysteresis loss.

7. **[Unit III | Topic: Eddy Current Loss | Type: Theory | Difficulty: Basic]**
   Define eddy current loss. Why are transformer cores laminated?

8. **[Unit III | Topic: Transformer Principle | Type: Theory | Difficulty: Basic]**
   State the working principle of a transformer.

9. **[Unit III | Topic: Transformer Construction | Type: Theory | Difficulty: Basic]**
   Describe the basic construction of a single-phase transformer, naming its main parts.

10. **[Unit III | Topic: EMF Equation | Type: Theory | Difficulty: Basic]**
    Define turns ratio (transformation ratio) of a transformer.

11. **[Unit III | Topic: Transformer Losses | Type: Theory | Difficulty: Basic]**
    List the different types of power losses that occur in a transformer.

12. **[Unit III | Topic: Efficiency | Type: Theory | Difficulty: Basic]**
    Define the efficiency of a transformer. Write the general formula.

13. **[Unit III | Topic: Efficiency | Type: Theory | Difficulty: Intermediate]**
    State the condition for maximum efficiency of a transformer in terms of its losses.

14. **[Unit III | Topic: O.C. and S.C. Tests | Type: Theory | Difficulty: Basic]**
    What is the purpose of the Open Circuit (O.C.) test on a transformer? What quantities are measured?

15. **[Unit III | Topic: O.C. and S.C. Tests | Type: Theory | Difficulty: Basic]**
    What is the purpose of the Short Circuit (S.C.) test on a transformer? What quantities are measured?

16. **[Unit III | Topic: O.C. and S.C. Tests | Type: Theory | Difficulty: Intermediate]**
    Explain why the O.C. test is performed on the low-voltage side and the S.C. test on the high-voltage side of a transformer (or as per standard practice).

17. **[Unit III | Topic: Auto Transformer | Type: Theory | Difficulty: Basic]**
    What is an auto-transformer? How does it differ from a two-winding transformer?

18. **[Unit III | Topic: Auto Transformer | Type: Theory | Difficulty: Intermediate]**
    State the advantages and disadvantages of an auto-transformer compared to a conventional two-winding transformer.

### Section B: Numerical Problems (Basic → Intermediate)

19. **[Unit III | Topic: Magnetic Circuit | Type: Numerical | Difficulty: Basic]**
    A magnetic circuit has a mean length of 0.5 m, cross-sectional area of 0.001 m², and relative permeability of 1000. Find the reluctance of the circuit.

20. **[Unit III | Topic: Magnetic Circuit | Type: Numerical | Difficulty: Intermediate]**
    A coil of 500 turns is wound on a magnetic core with a reluctance of 50000 AT/Wb. If the coil carries a current of 2 A, find the MMF and the flux produced.

21. **[Unit III | Topic: Hysteresis Loss | Type: Numerical | Difficulty: Intermediate]**
    A transformer core has a volume of 0.02 m³, operates at a maximum flux density of 1.2 T and a frequency of 50 Hz. Using Steinmetz's coefficient η = 150 (SI units) and exponent 1.6, calculate the hysteresis loss.

22. **[Unit III | Topic: EMF Equation | Type: Numerical | Difficulty: Basic]**
    A single-phase transformer has 300 primary turns and 900 secondary turns. If the maximum flux in the core is 0.05 Wb at 50 Hz, find the primary and secondary induced EMFs.

23. **[Unit III | Topic: EMF Equation | Type: Numerical | Difficulty: Basic]**
    A transformer is connected to a 230 V, 50 Hz supply on the primary and has a turns ratio of 1:4. Find the secondary voltage and the maximum flux in the core if the primary has 200 turns.

24. **[Unit III | Topic: Efficiency | Type: Numerical | Difficulty: Intermediate]**
    A 20 kVA transformer has iron losses of 200 W and full-load copper losses of 300 W. Calculate its efficiency at full load and at 0.8 power factor.

25. **[Unit III | Topic: Efficiency | Type: Numerical | Difficulty: Intermediate]**
    For the transformer in the previous question, find the load at which maximum efficiency occurs and calculate that maximum efficiency (at unity power factor).

26. **[Unit III | Topic: O.C. Test | Type: Numerical | Difficulty: Intermediate]**
    In an O.C. test on a transformer, the readings on the LV side are: V = 230 V, I = 3 A, W = 100 W. Calculate the no-load power factor, the magnetizing component of current, and the working (core-loss) component of current.

27. **[Unit III | Topic: S.C. Test | Type: Numerical | Difficulty: Intermediate]**
    In an S.C. test on a transformer, the readings on the HV side are: V = 40 V, I = 10 A (rated), W = 200 W. Calculate the equivalent resistance and equivalent reactance referred to the HV side.

28. **[Unit III | Topic: Auto Transformer | Type: Numerical | Difficulty: Basic]**
    A single-phase auto-transformer has a total winding of 400 turns, with the tapping at 100 turns from the common point, connected to a 230 V supply. Find the output voltage.

### Section C: Advanced Theory & Numericals

29. **[Unit III | Topic: EMF Equation | Type: Theory | Difficulty: Advanced]**
    Derive the EMF equation of a transformer from first principles, starting from Faraday's law of electromagnetic induction, and clearly define every symbol used.

30. **[Unit III | Topic: Efficiency | Type: Theory | Difficulty: Advanced]**
    Derive the condition for maximum efficiency of a transformer, starting from the general efficiency expression in terms of output, copper loss, and iron loss. Show that maximum efficiency occurs when copper loss equals iron loss.

31. **[Unit III | Topic: O.C. and S.C. Tests | Type: Numerical | Difficulty: Advanced]**
    From an O.C. test (V = 230 V, I₀ = 2 A, W₀ = 150 W, LV side) and an S.C. test (V = 25 V, I = 10 A, W = 120 W, HV side) on a single-phase transformer of turns ratio 1:5, determine: (a) the equivalent circuit parameters R₀ and X₀ (shunt branch) referred to the LV side, and (b) the equivalent resistance and reactance referred to the HV side. Then calculate the efficiency at 75% of full load, 0.8 p.f. lagging.

32. **[Unit III | Topic: Auto Transformer | Type: Numerical | Difficulty: Advanced]**
    A 400 V/200 V, 10 kVA two-winding transformer is reconnected as a step-down auto-transformer for a 400 V/200 V conversion. Calculate the maximum kVA rating of the auto-transformer and the saving in copper as compared to operation as a two-winding transformer.

33. **[Unit III | Topic: Magnetic Circuit + Hysteresis | Type: Numerical | Difficulty: Advanced]**
    A magnetic core forms a closed ring of mean length 0.4 m with a 2 mm air gap, cross-sectional area 0.0015 m², relative permeability of the core material 1200. A coil of 800 turns carries a current sufficient to produce a flux of 0.0012 Wb. Calculate the total MMF required, accounting separately for the core and air-gap reluctances.

---

## UNIT IV — Electrical Machines (DC Machines, Single-Phase & Three-Phase Induction Motors)

### Section A: Definitions & Concept Questions (Basic, 2–3 Marks)

1. **[Unit IV | Topic: Electromechanical Energy Conversion | Type: Theory | Difficulty: Basic]**
   What is meant by electromechanical energy conversion? Name the basic principle governing energy conversion in rotating electrical machines.

2. **[Unit IV | Topic: DC Machine Types | Type: Theory | Difficulty: Basic]**
   List the different types of DC generators based on excitation (separately excited, shunt, series, compound).

3. **[Unit IV | Topic: DC Machine Types | Type: Theory | Difficulty: Basic]**
   List the different types of DC motors based on excitation, similar to DC generators.

4. **[Unit IV | Topic: EMF Equation | Type: Theory | Difficulty: Basic]**
   Write the EMF equation of a DC generator and define each term used in it.

5. **[Unit IV | Topic: Torque Equation | Type: Theory | Difficulty: Basic]**
   Write the torque equation of a DC motor and define each term used in it.

6. **[Unit IV | Topic: Commutator | Type: Theory | Difficulty: Basic]**
   What is the function of a commutator in a DC machine?

7. **[Unit IV | Topic: Back EMF | Type: Theory | Difficulty: Basic]**
   Define back EMF in a DC motor. What is its significance in speed control and torque production?

8. **[Unit IV | Topic: Generator Characteristics | Type: Theory | Difficulty: Basic]**
   Define the open-circuit characteristic (O.C.C. / magnetization characteristic) of a DC generator.

9. **[Unit IV | Topic: Motor Characteristics | Type: Theory | Difficulty: Basic]**
   Sketch and briefly describe the speed-torque characteristic of a DC shunt motor.

10. **[Unit IV | Topic: Motor Characteristics | Type: Theory | Difficulty: Basic]**
    Sketch and briefly describe the speed-torque characteristic of a DC series motor.

11. **[Unit IV | Topic: Single-Phase Induction Motor | Type: Theory | Difficulty: Basic]**
    Explain the "double revolving field theory" as applied to a single-phase induction motor.

12. **[Unit IV | Topic: Single-Phase Induction Motor | Type: Theory | Difficulty: Basic]**
    Why is a single-phase induction motor not self-starting?

13. **[Unit IV | Topic: Single-Phase Induction Motor Starting | Type: Theory | Difficulty: Basic]**
    Name the different starting methods used for single-phase induction motors.

14. **[Unit IV | Topic: Single-Phase Induction Motor Starting | Type: Theory | Difficulty: Intermediate]**
    Explain the working of a capacitor-start induction-run single-phase motor.

15. **[Unit IV | Topic: Three-Phase Induction Motor Types | Type: Theory | Difficulty: Basic]**
    Distinguish between a squirrel-cage induction motor and a slip-ring (wound-rotor) induction motor.

16. **[Unit IV | Topic: Three-Phase Induction Motor | Type: Theory | Difficulty: Basic]**
    Define slip in a three-phase induction motor. Write its formula.

17. **[Unit IV | Topic: Torque-Slip Characteristic | Type: Theory | Difficulty: Intermediate]**
    Describe the torque-slip characteristic of a three-phase induction motor, identifying the starting, maximum (pull-out), and running-torque regions.

18. **[Unit IV | Topic: Three-Phase Induction Motor | Type: Theory | Difficulty: Basic]**
    Define synchronous speed of a three-phase induction motor and write its formula in terms of supply frequency and number of poles.

### Section B: Numerical Problems (Basic → Intermediate)

19. **[Unit IV | Topic: EMF Equation | Type: Numerical | Difficulty: Basic]**
    A 4-pole DC generator has 500 armature conductors, wave-wound, and runs at 1200 rpm. If the flux per pole is 0.02 Wb, calculate the generated EMF.

20. **[Unit IV | Topic: EMF Equation | Type: Numerical | Difficulty: Basic]**
    A DC generator with a lap-wound armature has 6 poles, 720 conductors, and generates an EMF of 240 V at 1000 rpm. Find the flux per pole.

21. **[Unit IV | Topic: Torque Equation | Type: Numerical | Difficulty: Intermediate]**
    A DC motor draws an armature current of 25 A at 220 V and runs at 1000 rpm. The armature resistance is 0.5 Ω. Calculate the back EMF and the electromagnetic torque developed.

22. **[Unit IV | Topic: DC Motor Speed | Type: Numerical | Difficulty: Intermediate]**
    A DC shunt motor takes 20 A from a 230 V supply and has an armature resistance of 0.4 Ω. If the flux per pole is constant, find the speed of the motor if the no-load speed (at the same flux) was 1000 rpm with a back EMF of 220 V and the loaded back EMF is now 214 V.

23. **[Unit IV | Topic: DC Generator Characteristics | Type: Numerical | Difficulty: Basic]**
    A shunt generator has a terminal voltage of 220 V, supplies a load current of 50 A, has an armature resistance of 0.2 Ω, and a field current of 2 A. Find the generated EMF and the armature current.

24. **[Unit IV | Topic: Three-Phase Induction Motor Slip | Type: Numerical | Difficulty: Basic]**
    A 4-pole, three-phase induction motor is connected to a 50 Hz supply. If the rotor runs at 1440 rpm, calculate the synchronous speed and the slip.

25. **[Unit IV | Topic: Three-Phase Induction Motor Slip | Type: Numerical | Difficulty: Basic]**
    A 6-pole induction motor operates on a 50 Hz supply with a slip of 4%. Determine the synchronous speed and the actual rotor speed.

26. **[Unit IV | Topic: Rotor Frequency | Type: Numerical | Difficulty: Intermediate]**
    A three-phase induction motor has a synchronous speed of 1500 rpm and runs at 1425 rpm on full load. If the supply frequency is 50 Hz, find the slip and the rotor (frequency of induced EMF) frequency.

27. **[Unit IV | Topic: DC Motor Power | Type: Numerical | Difficulty: Intermediate]**
    A DC series motor takes 30 A from a 230 V supply. The armature resistance is 0.3 Ω and the series field resistance is 0.2 Ω. Calculate the back EMF, the power developed by the armature, and the electromagnetic torque if the motor runs at 900 rpm.

### Section C: Advanced Theory & Numericals

28. **[Unit IV | Topic: EMF Equation | Type: Theory | Difficulty: Advanced]**
    Derive the EMF equation of a DC generator from first principles, starting with the EMF induced in a single conductor and extending it to the complete armature winding with A parallel paths.

29. **[Unit IV | Topic: Torque-Slip Characteristic | Type: Theory | Difficulty: Advanced]**
    Derive the expression for torque developed by a three-phase induction motor in terms of slip, and show mathematically how maximum torque and the slip at which it occurs are obtained from this expression.

30. **[Unit IV | Topic: DC Motor Speed Control | Type: Numerical | Difficulty: Advanced]**
    A DC shunt motor runs at 1000 rpm on a 230 V supply, drawing an armature current of 20 A with armature resistance 0.5 Ω. Find the additional resistance to be inserted in the armature circuit to reduce the speed to 800 rpm at the same torque (same armature current), assuming flux remains constant.

31. **[Unit IV | Topic: Three-Phase Induction Motor Torque | Type: Numerical | Difficulty: Advanced]**
    A three-phase, 4-pole, 50 Hz induction motor has a full-load slip of 4%. The rotor standstill EMF per phase is 100 V and the rotor resistance and standstill reactance per phase are 0.3 Ω and 1.5 Ω respectively. Calculate the full-load torque developed and the maximum torque, along with the slip at which maximum torque occurs.

32. **[Unit IV | Topic: Single-Phase Induction Motor | Type: Theory | Difficulty: Advanced]**
    Using the double revolving field theory, explain quantitatively how the forward and backward rotating flux components produce a net starting torque of zero but a non-zero net running torque once the rotor is set in motion by an external means.

33. **[Unit IV | Topic: DC Machine Losses & Efficiency | Type: Numerical | Difficulty: Advanced]**
    A DC shunt generator delivers 100 A at 220 V. The armature resistance is 0.1 Ω, the shunt field resistance is 110 Ω, and the rotational (stray) losses are 500 W. Calculate the generated EMF, the copper losses, and the overall efficiency of the generator.

---

## Coverage Summary

| Unit | Topics Fully Covered | Question Types | Difficulty Range |
|---|---|---|---|
| I — DC Circuits & Network Theorems | Network concepts, sources, KCL/KVL, loop/nodal analysis, star-delta, Superposition, Thevenin's, Norton's, Max. Power Transfer | Theory (20) + Numerical (15) | Basic → Advanced |
| II — AC Circuits (1-φ & 3-φ) | Waveforms, avg/RMS values, phasors, series/parallel/series-parallel RLC, resonance, star/delta 3-φ, power measurement | Theory (18) + Numerical (17) | Basic → Advanced |
| III — Magnetic Circuits & Transformers | Magnetic circuit, B-H curve, hysteresis, eddy current loss, transformer principle/construction/EMF/losses/efficiency, O.C./S.C. tests, auto-transformer | Theory (18) + Numerical (15) | Basic → Advanced |
| IV — Electrical Machines | Energy conversion, DC machine types, EMF/torque equations, generator/motor characteristics, 1-φ IM (principle, starting), 3-φ IM (types, torque-slip) | Theory (18) + Numerical (15) | Basic → Advanced |

**Total questions:** 146 (73 Theory, 73 Numerical) across 4 units, all strictly scoped to the given BEE-101 syllabus — no out-of-syllabus content (e.g., electrical installations, SFU, ELCB, bus-bars, cables) is included, consistent with the earlier syllabus-mapping check.
