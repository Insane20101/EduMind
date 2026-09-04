# BEC-154 — Basic Electronic Components and Circuits
## Complete Unit-Wise Question Bank (Theory + Numericals, Basic → Advanced)

> **Course:** BEC-154 — Basic Electronic Components and Circuits
> **Credits:** 4
> **Coverage:** Strictly mapped to the 4-unit syllabus below. No topics outside the syllabus are included (in particular, no communication-systems/CO5-type content, as that unit is not part of this syllabus).
> **Format note:** Each question is tagged with `Unit`, `Topic`, `Type` (Theory/Numerical), and `Difficulty` (Basic/Intermediate/Advanced) for structured retrieval.

---

## Syllabus Reference (source of truth for this question bank)

- **Unit I:** Semiconductor materials and properties, energy bands, intrinsic/extrinsic semiconductors, p-n junction diode, depletion layer, V-I characteristics, diode applications in rectifiers/filters/voltage multipliers/clippers/clampers, breakdown mechanisms, Zener diode as shunt regulator.
- **Unit II:** Transistors (BJT and FET) — construction, transistor action, CB/CE/CC configurations, biasing methods, transistor amplifier analysis, h-parameter model, gain computations for CE and CC configurations.
- **Unit III:** JFET & MOSFET/Switching Theory — construction, transistor action, pinch-off, drain characteristics, biasing, MOSFET as amplifier/switch; Number systems, Boolean algebra, logic gates, universal gates, canonical forms, K-map minimization.
- **Unit IV:** Operational Amplifier — ideal op-amp parameters, inverting/non-inverting/unity-gain amplifiers, adders, difference amplifiers, integrators, and other op-amp based circuits.

---

## UNIT I — Semiconductor Diodes and Applications

### Section A: Definitions & Concept Questions (Basic, 2–3 Marks)

1. **[Unit I | Topic: Semiconductor Materials | Type: Theory | Difficulty: Basic]**
   Define a semiconductor. Name two elemental and two compound semiconductor materials.

2. **[Unit I | Topic: Energy Bands | Type: Theory | Difficulty: Basic]**
   Define the valence band, conduction band, and forbidden energy gap.

3. **[Unit I | Topic: Energy Bands | Type: Theory | Difficulty: Basic]**
   Distinguish between a conductor, an insulator, and a semiconductor on the basis of energy band gap.

4. **[Unit I | Topic: Intrinsic/Extrinsic Semiconductors | Type: Theory | Difficulty: Basic]**
   Describe the difference between intrinsic and extrinsic semiconductors.

5. **[Unit I | Topic: Doping | Type: Theory | Difficulty: Basic]**
   Define doping. Distinguish between a donor impurity and an acceptor impurity.

6. **[Unit I | Topic: n-type/p-type Semiconductors | Type: Theory | Difficulty: Basic]**
   Define n-type and p-type semiconductors, naming the majority and minority charge carriers in each.

7. **[Unit I | Topic: p-n Junction | Type: Theory | Difficulty: Basic]**
   What is a p-n junction? Briefly describe how it is formed.

8. **[Unit I | Topic: Depletion Layer | Type: Theory | Difficulty: Basic]**
   Define the depletion layer (depletion region) of a p-n junction. What is the barrier potential?

9. **[Unit I | Topic: Diode Biasing | Type: Theory | Difficulty: Basic]**
   Define forward bias and reverse bias of a p-n junction diode.

10. **[Unit I | Topic: V-I Characteristics | Type: Theory | Difficulty: Basic]**
    Sketch the general shape of the V-I characteristic of a p-n junction diode and identify the knee (cut-in) voltage.

11. **[Unit I | Topic: Diode Parameters | Type: Theory | Difficulty: Basic]**
    Define the cut-in (threshold) voltage of a diode. State its typical value for silicon and germanium diodes.

12. **[Unit I | Topic: Rectifiers | Type: Theory | Difficulty: Basic]**
    Define rectification. Distinguish between a half-wave and a full-wave rectifier.

13. **[Unit I | Topic: Rectifiers | Type: Theory | Difficulty: Basic]**
    Define ripple factor and efficiency of a rectifier.

14. **[Unit I | Topic: Filters | Type: Theory | Difficulty: Basic]**
    What is the purpose of a filter circuit following a rectifier? Name two common types of filter.

15. **[Unit I | Topic: Voltage Multipliers | Type: Theory | Difficulty: Basic]**
    Define a voltage doubler. What is its basic principle?

16. **[Unit I | Topic: Clippers | Type: Theory | Difficulty: Basic]**
    Define a clipper (limiter) circuit. Distinguish between series and shunt (parallel) clippers.

17. **[Unit I | Topic: Clampers | Type: Theory | Difficulty: Basic]**
    Define a clamper circuit. How does it differ functionally from a clipper?

18. **[Unit I | Topic: Breakdown Mechanisms | Type: Theory | Difficulty: Basic]**
    Name the two breakdown mechanisms in a p-n junction diode under reverse bias.

19. **[Unit I | Topic: Breakdown Mechanisms | Type: Theory | Difficulty: Basic]**
    Distinguish between Zener breakdown and avalanche breakdown.

20. **[Unit I | Topic: Zener Diode | Type: Theory | Difficulty: Basic]**
    Define a Zener diode. How does its V-I characteristic differ from a normal p-n junction diode?

21. **[Unit I | Topic: Zener Diode as Regulator | Type: Theory | Difficulty: Basic]**
    Explain the basic principle by which a Zener diode acts as a voltage (shunt) regulator.

22. **[Unit I | Topic: Diode Approximations | Type: Theory | Difficulty: Basic]**
    Define the ideal diode model. State its assumed forward and reverse characteristics.

### Section B: Computational & Applied Problems (Intermediate, 7 Marks)

23. **[Unit I | Topic: Rectifiers | Type: Numerical | Difficulty: Intermediate]**
    A half-wave rectifier is fed from a transformer secondary of RMS voltage 30 V. Assuming an ideal diode, find the peak output voltage, DC output voltage, and ripple factor.

24. **[Unit I | Topic: Rectifiers | Type: Numerical | Difficulty: Intermediate]**
    A full-wave bridge rectifier has a transformer secondary RMS voltage of 20 V (center-tap not used, bridge configuration) and a load resistance of 1 kΩ. Assuming ideal diodes, find the DC output voltage, DC output current, and ripple factor.

25. **[Unit I | Topic: Full-Wave Bridge Rectifier | Type: Theory | Difficulty: Intermediate]**
    Draw the circuit diagram of a full-wave bridge rectifier and explain its working during both half-cycles of the input, indicating which diodes conduct in each half-cycle.

26. **[Unit I | Topic: Clippers | Type: Numerical | Difficulty: Intermediate]**
    A series clipper circuit uses an ideal diode in series with a 1 kΩ resistor, with the diode oriented to conduct for positive input. For a sinusoidal input of peak 20 V, sketch and describe the output waveform.

27. **[Unit I | Topic: Clippers | Type: Numerical | Difficulty: Intermediate]**
    A parallel (shunt) clipper uses an ideal diode with a 4 V battery in series with it (biasing the clipping level), across a 1 kΩ series resistor, for a square-wave input alternating between +20 V and −5 V. Determine the output voltage levels.

28. **[Unit I | Topic: Clampers | Type: Numerical | Difficulty: Intermediate]**
    A positive clamper circuit (diode, capacitor, resistor) is fed with a square wave of peak values +V and −V (ideal diode, RC time constant much larger than the period). Sketch and explain the output waveform, showing the DC shift introduced.

29. **[Unit I | Topic: Zener Diode Regulator | Type: Numerical | Difficulty: Intermediate]**
    A Zener diode with V_Z = 10 V and P_Z(max) = 400 mW is used as a shunt regulator with a series resistance R_S = 220 Ω, fed from a 20 V source, with a load resistance R_L = 180 Ω. Determine V_L, I_L, I_Z, and I_R, and verify the Zener is within its power rating.

30. **[Unit I | Topic: Voltage Doubler | Type: Numerical | Difficulty: Intermediate]**
    Explain the working of a half-wave voltage doubler circuit (two diodes, two capacitors) fed from a sinusoidal input of peak value V_m, and determine the approximate DC output voltage across the load (ideal diodes and capacitors assumed).

31. **[Unit I | Topic: Diode DC Analysis (Load Line) | Type: Numerical | Difficulty: Intermediate]**
    A silicon diode (cut-in voltage 0.7 V) is connected in series with a 1 kΩ resistor across a 10 V DC source. Using the constant-voltage-drop diode model, find the diode current and the voltage across the resistor.

### Section C: Advanced Theory & Numericals

32. **[Unit I | Topic: p-n Junction Formation | Type: Theory | Difficulty: Advanced]**
    Explain, with the help of energy-band diagrams, the formation of the depletion region and the barrier potential at an unbiased p-n junction. How does this barrier potential change under forward and reverse bias?

33. **[Unit I | Topic: Rectifiers — Comparative Analysis | Type: Theory | Difficulty: Advanced]**
    Derive the expressions for ripple factor and rectification efficiency for a full-wave rectifier, and compare these values with those of a half-wave rectifier, explaining the reasons for the difference.

34. **[Unit I | Topic: Zener Regulator — Load & Line Regulation | Type: Numerical | Difficulty: Advanced]**
    For a Zener shunt regulator with V_Z = 10 V, R_S = 220 Ω, supplied from a source that varies between 18 V and 22 V, with load resistance fixed at R_L = 500 Ω: determine the Zener current at both source-voltage extremes, and comment on whether the regulator maintains a fixed load voltage over this range (assume Zener current rating is not exceeded).

35. **[Unit I | Topic: Full-Wave Rectifier with Filter | Type: Numerical | Difficulty: Advanced]**
    A full-wave rectifier with a capacitor filter supplies a load current of 100 mA at a DC output voltage of 20 V, with a specified ripple factor of 5%. Using the approximate capacitor-filter ripple formula, determine the required filter capacitance (supply frequency 50 Hz).

36. **[Unit I | Topic: Voltage Doubler & Clamper Combined | Type: Numerical | Difficulty: Advanced]**
    Sketch and explain the working of a full-wave voltage doubler circuit, and derive its approximate DC output voltage in terms of the peak input voltage V_m. Compare its ripple behavior with that of a half-wave voltage doubler.

---

## UNIT II — Transistors (BJT and FET): Configurations, Biasing, and Amplifier Analysis

### Section A: Definitions & Concept Questions (Basic, 2–3 Marks)

1. **[Unit II | Topic: BJT Construction | Type: Theory | Difficulty: Basic]**
   Describe the basic construction of a bipolar junction transistor (BJT), naming its three terminals and two junctions.

2. **[Unit II | Topic: Transistor Action | Type: Theory | Difficulty: Basic]**
   Briefly explain transistor action in an NPN BJT — how does a small base current control a large collector current?

3. **[Unit II | Topic: Transistor Leakage Currents | Type: Theory | Difficulty: Basic]**
   Define I_CBO and I_CEO.

4. **[Unit II | Topic: BJT Configurations | Type: Theory | Difficulty: Basic]**
   Name the three basic BJT configurations (CB, CE, CC) and state which terminal is common to input and output in each.

5. **[Unit II | Topic: BJT Configurations | Type: Theory | Difficulty: Basic]**
   Define current gain α (alpha) for the common-base configuration and β (beta) for the common-emitter configuration.

6. **[Unit II | Topic: BJT Configurations | Type: Theory | Difficulty: Basic]**
   Write the relationship between α and β for a BJT.

7. **[Unit II | Topic: BJT vs FET | Type: Theory | Difficulty: Basic]**
   What are the key operational and structural differences between a Bipolar Junction Transistor (BJT) and a Field Effect Transistor (FET)?

8. **[Unit II | Topic: Transistor Biasing | Type: Theory | Difficulty: Basic]**
   Define DC biasing of a transistor. Why is biasing necessary for amplifier operation?

9. **[Unit II | Topic: Biasing Methods | Type: Theory | Difficulty: Basic]**
   Name three common methods of transistor biasing.

10. **[Unit II | Topic: Biasing — Stability | Type: Theory | Difficulty: Basic]**
    Define the stability factor S of a biasing circuit. Why is a low stability factor desirable?

11. **[Unit II | Topic: Voltage Divider Bias | Type: Theory | Difficulty: Basic]**
    Describe the voltage-divider (self) bias circuit and explain why it provides better stability than fixed bias.

12. **[Unit II | Topic: Operating Point | Type: Theory | Difficulty: Basic]**
    Define the operating point (Q-point) of a transistor. Why is it usually located at the center of the DC load line for amplifier applications?

13. **[Unit II | Topic: CE Characteristics | Type: Theory | Difficulty: Basic]**
    Sketch the general shape of the common-emitter output (V-I) characteristics of an NPN BJT, identifying the active, saturation, and cut-off regions.

14. **[Unit II | Topic: h-parameter Model | Type: Theory | Difficulty: Basic]**
    Define the four h-parameters (h_i, h_r, h_f, h_o) of a two-port network, stating their units.

15. **[Unit II | Topic: h-parameter Model | Type: Theory | Difficulty: Basic]**
    Write the h-parameter equivalent circuit equations for a transistor in terms of input/output voltage and current.

16. **[Unit II | Topic: Amplifier Parameters | Type: Theory | Difficulty: Basic]**
    Define voltage gain, current gain, input impedance, and output impedance of a transistor amplifier.

17. **[Unit II | Topic: CE Amplifier | Type: Theory | Difficulty: Basic]**
    State the typical phase relationship between input and output voltage in a CE amplifier.

18. **[Unit II | Topic: CC Amplifier | Type: Theory | Difficulty: Basic]**
    What is another common name for the common-collector configuration, and why? State its typical voltage gain (approximately).

### Section B: Computational Fluency (Intermediate, 7 Marks)

19. **[Unit II | Topic: BJT Current Relations | Type: Numerical | Difficulty: Intermediate]**
    A transistor has α = 0.98. Find the value of β and the ratio I_C/I_B.

20. **[Unit II | Topic: BJT Current Relations | Type: Numerical | Difficulty: Intermediate]**
    A transistor has β = 100 and I_B = 20 µA. Find I_C and I_E (neglecting leakage current).

21. **[Unit II | Topic: Fixed Bias Circuit | Type: Numerical | Difficulty: Intermediate]**
    In a fixed-bias circuit, V_CC = 12 V, R_B = 240 kΩ, R_C = 2 kΩ, and β = 100 (V_BE = 0.7 V). Find I_B, I_C, and V_CE.

22. **[Unit II | Topic: Voltage Divider Bias | Type: Numerical | Difficulty: Intermediate]**
    In a voltage-divider bias circuit, V_CC = 20 V, R_1 = 39 kΩ, R_2 = 3.9 kΩ, R_C = 4 kΩ, R_E = 1.5 kΩ, β = 100 (V_BE = 0.7 V). Using the approximate analysis (assuming the base current is negligible compared to the divider current), find V_B, V_E, I_E, I_C, and V_CE.

23. **[Unit II | Topic: h-parameter Analysis — CE Gain | Type: Numerical | Difficulty: Intermediate]**
    A CE amplifier has h_ie = 1.1 kΩ, h_fe = 100, h_oe = 25 µA/V, h_re (negligible), and is driving a load resistance R_L = 2 kΩ. Compute the current gain A_I = I_C/I_B and the voltage gain A_V.

24. **[Unit II | Topic: h-parameter Analysis — Input Impedance | Type: Numerical | Difficulty: Intermediate]**
    For the amplifier of the previous question, compute the input impedance R_i seen at the base terminals.

25. **[Unit II | Topic: h-parameter Analysis — CC Gain | Type: Numerical | Difficulty: Intermediate]**
    A common-collector (emitter-follower) amplifier has h_ic = 1.1 kΩ, h_fc = −101, h_oc = 25 µA/V, and a load resistance R_L = 1 kΩ. Compute the current gain A_I and voltage gain A_V, and comment on why the voltage gain is close to unity.

26. **[Unit II | Topic: DC Load Line | Type: Numerical | Difficulty: Intermediate]**
    For a CE amplifier with V_CC = 15 V, R_C = 3 kΩ, R_E = 1 kΩ, sketch the DC load line and determine its saturation current point and cut-off voltage point.

27. **[Unit II | Topic: Transistor as a Switch | Type: Numerical | Difficulty: Intermediate]**
    A BJT with β = 50 is used as a switch with R_C = 1 kΩ and V_CC = 5 V. Determine the minimum base current required to drive the transistor into saturation (assume V_CE(sat) ≈ 0 V).

### Section C: Advanced Theory & Numericals

28. **[Unit II | Topic: CE Configuration — Characteristics | Type: Theory | Difficulty: Advanced]**
    Draw the common-emitter configuration of an NPN BJT and explain it with the help of input and output V-I characteristic curves, clearly identifying the active, saturation, cut-off, and breakdown regions on the output characteristics.

29. **[Unit II | Topic: h-parameter Derivation | Type: Theory | Difficulty: Advanced]**
    Starting from the two-port h-parameter equations for a transistor amplifier with a load resistance R_L, derive the general expressions for current gain A_I, input impedance R_i, voltage gain A_V, and output impedance R_o in terms of the h-parameters.

30. **[Unit II | Topic: Voltage Divider Bias — Stability Analysis | Type: Numerical | Difficulty: Advanced]**
    For a voltage-divider bias circuit with V_CC = 20 V, R_1 = 39 kΩ, R_2 = 3.9 kΩ, R_C = 4 kΩ, R_E = 1.5 kΩ, β = 100, find the exact (Thevenin-equivalent) values of I_B, I_C, and V_CE without using the approximation that base current is negligible, and compare the result with the approximate method.

31. **[Unit II | Topic: CE and CC Gain Comparison | Type: Numerical | Difficulty: Advanced]**
    For a transistor with h_ie = 1 kΩ, h_fe = 120, h_oe = 20 µA/V (h_re negligible), operating with R_L = 2.2 kΩ, compute the voltage gain, current gain, input impedance, and output impedance in both the CE and CC configurations, and tabulate the comparison, explaining the key application-relevant differences.

32. **[Unit II | Topic: Biasing Stability Factor Derivation | Type: Theory | Difficulty: Advanced]**
    Derive the expression for the stability factor S = ∂I_C/∂I_CO for a fixed-bias circuit, and show mathematically why voltage-divider bias yields a lower (better) stability factor than fixed bias.

---

## UNIT III — JFET, MOSFET & Switching Theory

### Section A: Definitions & Concept Questions (Basic, 2–3 Marks)

1. **[Unit III | Topic: JFET Construction | Type: Theory | Difficulty: Basic]**
   Describe the basic construction of an n-channel JFET, naming its three terminals.

2. **[Unit III | Topic: JFET Action | Type: Theory | Difficulty: Basic]**
   Briefly explain how the drain current in a JFET is controlled by the gate-source voltage.

3. **[Unit III | Topic: Pinch-Off | Type: Theory | Difficulty: Basic]**
   Define the pinch-off voltage of a JFET.

4. **[Unit III | Topic: JFET Characteristics | Type: Theory | Difficulty: Basic]**
   Sketch the general shape of the JFET drain (output) characteristics, identifying the ohmic and saturation (pinch-off) regions.

5. **[Unit III | Topic: JFET Parameters | Type: Theory | Difficulty: Basic]**
   Define transconductance (g_m) of a JFET. State its typical unit.

6. **[Unit III | Topic: JFET Biasing | Type: Theory | Difficulty: Basic]**
   Name two common methods of biasing a JFET.

7. **[Unit III | Topic: MOSFET Types | Type: Theory | Difficulty: Basic]**
   Name the two basic types of MOSFET based on construction/operation mode.

8. **[Unit III | Topic: MOSFET Construction | Type: Theory | Difficulty: Basic]**
   Describe the basic construction of an enhancement-type MOSFET, naming its four terminals.

9. **[Unit III | Topic: MOSFET vs JFET | Type: Theory | Difficulty: Basic]**
   State one key structural difference between a MOSFET and a JFET (relating to the gate).

10. **[Unit III | Topic: Depletion vs Enhancement MOSFET | Type: Theory | Difficulty: Basic]**
    Differentiate between depletion-type and enhancement-type MOSFETs in terms of channel existence at V_GS = 0.

11. **[Unit III | Topic: MOSFET as Switch | Type: Theory | Difficulty: Basic]**
    Explain briefly how a MOSFET can be used as an electronic switch, referring to its cut-off and ohmic (triode) regions.

12. **[Unit III | Topic: Number Systems | Type: Theory | Difficulty: Basic]**
    Name four common number systems used in digital electronics, along with their bases.

13. **[Unit III | Topic: Boolean Algebra | Type: Theory | Difficulty: Basic]**
    State the commutative, associative, and distributive laws of Boolean algebra.

14. **[Unit III | Topic: Boolean Algebra — De Morgan's Theorem | Type: Theory | Difficulty: Basic]**
    State De Morgan's theorems.

15. **[Unit III | Topic: Logic Gates | Type: Theory | Difficulty: Basic]**
    Define the AND, OR, and NOT logic gates, giving their truth tables.

16. **[Unit III | Topic: Universal Gates | Type: Theory | Difficulty: Basic]**
    Which are the universal logic gates? Why are they called "universal"?

17. **[Unit III | Topic: Canonical Forms | Type: Theory | Difficulty: Basic]**
    Define the Sum-of-Products (SOP) and Product-of-Sums (POS) canonical forms of a Boolean expression.

18. **[Unit III | Topic: K-Map | Type: Theory | Difficulty: Basic]**
    What is a Karnaugh map (K-map)? State its purpose in digital logic design.

### Section B: Computational Fluency (Intermediate, 7 Marks)

19. **[Unit III | Topic: JFET Biasing | Type: Numerical | Difficulty: Intermediate]**
    A JFET has I_DSS = 10 mA and V_P = −4 V. Using the Shockley equation, find the drain current I_D at V_GS = −2 V.

20. **[Unit III | Topic: JFET Transconductance | Type: Numerical | Difficulty: Intermediate]**
    For the JFET of the previous question, find the transconductance g_m at V_GS = −2 V, given g_m0 (at V_GS=0) = 5 mA/V.

21. **[Unit III | Topic: Number System Conversion | Type: Numerical | Difficulty: Intermediate]**
    Convert the following: (i) (110010110)₂ = ( )₁₆  (ii) (B2D)₁₆ = ( )₈  (iii) (21.25)₁₀ = ( )₂

22. **[Unit III | Topic: r's Complement Subtraction | Type: Numerical | Difficulty: Intermediate]**
    Subtract the following using r's complement method: (i) (76548)₁₀ − (96541)₁₀  (ii) (11010011)₂ − (10110011)₂

23. **[Unit III | Topic: Boolean Simplification | Type: Numerical | Difficulty: Intermediate]**
    Simplify the Boolean expression F = A'B'C + A'BC + AB'C + ABC using Boolean algebra laws.

24. **[Unit III | Topic: K-Map Minimization | Type: Numerical | Difficulty: Intermediate]**
    Minimize the expression f(A,B,C) = Σm(1,3,5,6,7) using a K-map, and write the simplified SOP expression.

25. **[Unit III | Topic: Universal Gate Realization | Type: Numerical | Difficulty: Intermediate]**
    Design a 2-input AND gate using only NAND gates.

26. **[Unit III | Topic: Universal Gate Realization | Type: Numerical | Difficulty: Intermediate]**
    Design a 2-input OR gate using only NOR gates.

27. **[Unit III | Topic: MOSFET Biasing | Type: Numerical | Difficulty: Intermediate]**
    An enhancement MOSFET has V_T = 2 V and k = 0.5 mA/V². Find the drain current I_D at V_GS = 5 V (in the saturation region), using I_D = k(V_GS−V_T)².

### Section C: Advanced Theory & Numericals

28. **[Unit III | Topic: JFET Construction & Working | Type: Theory | Difficulty: Advanced]**
    Draw the construction and explain the working of an n-channel JFET, describing how the depletion regions widen with increasing reverse gate-source voltage, and clearly explain the pinch-off condition.

29. **[Unit III | Topic: Enhancement MOSFET Channel Formation | Type: Theory | Difficulty: Advanced]**
    Explain the channel formation process in an enhancement-type MOSFET as V_GS is increased from zero, and differentiate in detail between depletion-type and enhancement-type MOSFETs (construction, channel at V_GS=0, and typical transfer characteristic shape).

30. **[Unit III | Topic: K-Map Minimization — 4-Variable | Type: Numerical | Difficulty: Advanced]**
    Minimize the expression using a K-map: f(A,B,C,D) = Σm(1,3,7,8,10,11,13,14,15). Implement the minimized expression using NAND gates only.

31. **[Unit III | Topic: NAND Realization of Boolean Function | Type: Numerical | Difficulty: Advanced]**
    State De Morgan's theorem. Realize the given function using NAND gates: F = B'D' + B'C' + A'C'D

32. **[Unit III | Topic: JFET Load Line & Q-Point | Type: Numerical | Difficulty: Advanced]**
    A JFET with I_DSS = 8 mA and V_P = −4 V is self-biased using a source resistor R_S. If the desired quiescent drain current is I_DQ = 2 mA, find the required value of R_S using the Shockley equation (find V_GSQ first, then R_S = |V_GSQ|/I_DQ).

33. **[Unit III | Topic: MOSFET as Amplifier vs Switch | Type: Theory | Difficulty: Advanced]**
    Explain the operation of a MOSFET as an amplifier (biased in the saturation region) versus as a switch (operated between cut-off and the ohmic/triode region), discussing the differences in biasing point and the role of the load line in each mode of operation.

---

## UNIT IV — Operational Amplifier and Applications

### Section A: Definitions & Concept Questions (Basic, 2–3 Marks)

1. **[Unit IV | Topic: Op-Amp Basics | Type: Theory | Difficulty: Basic]**
   Define an operational amplifier (op-amp). Name its main input and output terminals.

2. **[Unit IV | Topic: Ideal Op-Amp Parameters | Type: Theory | Difficulty: Basic]**
   List the parameters of a practical operational amplifier and compare each with the corresponding ideal amplifier value.

3. **[Unit IV | Topic: Virtual Ground | Type: Theory | Difficulty: Basic]**
   Define the concept of virtual ground as applied to an inverting op-amp amplifier.

4. **[Unit IV | Topic: Slew Rate | Type: Theory | Difficulty: Basic]**
   Define slew rate of an op-amp. State its unit.

5. **[Unit IV | Topic: Unity Follower | Type: Theory | Difficulty: Basic]**
   Define a unity (voltage) follower circuit using an op-amp. State its voltage gain and its main application.

6. **[Unit IV | Topic: CMRR | Type: Theory | Difficulty: Basic]**
   What does CMRR indicate? What is the ideal value of CMRR for an op-amp?

7. **[Unit IV | Topic: Differential and Common Mode | Type: Theory | Difficulty: Basic]**
   Define differential-mode gain and common-mode gain of a differential (op-amp) amplifier.

8. **[Unit IV | Topic: Inverting Amplifier | Type: Theory | Difficulty: Basic]**
   Draw the circuit of an inverting op-amp amplifier and write the expression for its voltage gain in terms of the feedback and input resistors.

9. **[Unit IV | Topic: Non-Inverting Amplifier | Type: Theory | Difficulty: Basic]**
   Draw the circuit of a non-inverting op-amp amplifier and write the expression for its voltage gain.

10. **[Unit IV | Topic: Adder Circuit | Type: Theory | Difficulty: Basic]**
    Define a summing amplifier (adder) circuit using an op-amp. Write the general expression for its output in terms of the input voltages and resistors.

11. **[Unit IV | Topic: Difference Amplifier | Type: Theory | Difficulty: Basic]**
    Define a difference amplifier using an op-amp. Write the expression for its output voltage for the case of equal resistor ratios.

12. **[Unit IV | Topic: Integrator | Type: Theory | Difficulty: Basic]**
    Define an op-amp integrator circuit. Write the expression relating its output voltage to the input voltage.

13. **[Unit IV | Topic: Op-Amp Input Impedance/Output Impedance | Type: Theory | Difficulty: Basic]**
    State the ideal values of input impedance, output impedance, and open-loop gain of an op-amp.

14. **[Unit IV | Topic: Op-Amp Golden Rules | Type: Theory | Difficulty: Basic]**
    State the two "golden rules" used for analyzing ideal op-amp circuits with negative feedback.

### Section B: Computational Fluency (Intermediate, 7 Marks)

15. **[Unit IV | Topic: Inverting Amplifier | Type: Numerical | Difficulty: Intermediate]**
    An inverting amplifier has R_in = 20 kΩ and R_f = 100 kΩ, with input voltage V_1 = 1.5 V. Calculate the output voltage V_o.

16. **[Unit IV | Topic: Non-Inverting Amplifier | Type: Numerical | Difficulty: Intermediate]**
    A non-inverting amplifier has R_1 = 1 kΩ (to ground) and R_f = 9 kΩ (feedback), with input voltage V_1 = 0.8 V. Calculate the output voltage V_o.

17. **[Unit IV | Topic: Op-Amp Output Range | Type: Numerical | Difficulty: Intermediate]**
    In an inverting amplifier with R_1 = 20 kΩ and R_f = 200 kΩ, the input voltage varies from 0.1 V to 0.5 V. Find the corresponding range of output voltage.

18. **[Unit IV | Topic: Adder Circuit | Type: Numerical | Difficulty: Intermediate]**
    A summing (inverting adder) amplifier has two input resistors R_1 = R_2 = 10 kΩ and feedback resistor R_f = 10 kΩ, with input voltages V_1 = 2 V and V_2 = 3 V. Find the output voltage.

19. **[Unit IV | Topic: Difference Amplifier | Type: Numerical | Difficulty: Intermediate]**
    A difference amplifier has all four resistors equal to 10 kΩ, with V_1 = 5 V and V_2 = 3 V applied to the inverting and non-inverting inputs respectively (through matched resistor networks). Find the output voltage.

20. **[Unit IV | Topic: Integrator | Type: Numerical | Difficulty: Intermediate]**
    An op-amp integrator has R = 10 kΩ and C = 1 µF, with a constant input voltage V_in = 2 V applied at t=0 (capacitor initially uncharged). Find the output voltage at t = 5 ms.

21. **[Unit IV | Topic: Slew Rate Limitation | Type: Numerical | Difficulty: Intermediate]**
    An op-amp has a slew rate of 0.5 V/µs. Find the maximum frequency at which it can produce an undistorted sinusoidal output of peak amplitude 5 V.

22. **[Unit IV | Topic: CMRR Calculation | Type: Numerical | Difficulty: Intermediate]**
    An op-amp has a differential-mode gain of 100,000 and a common-mode gain of 0.5. Find its CMRR in dB.

### Section C: Advanced Theory & Numericals

23. **[Unit IV | Topic: Non-Inverting Amplifier — Feedback Network | Type: Numerical | Difficulty: Advanced]**
    In a circuit, a signal V_1 (input) is applied through a 20 kΩ resistor to the inverting input of an op-amp, with a 100 kΩ feedback resistor to the output, and the non-inverting input grounded. If V_1 ranges from 0.1 V to 0.5 V, find the range of output voltage, and separately determine the output voltage if instead V_1 = 1.5 V is applied at the non-inverting input through a 20 kΩ resistor with 100 kΩ feedback in a non-inverting configuration — compare the two gains obtained.

24. **[Unit IV | Topic: Op-Amp Circuit with Loading | Type: Numerical | Difficulty: Advanced]**
    For an inverting amplifier circuit consisting of an input resistor R_1 = 20 kΩ, feedback resistor R_f = 100 kΩ, and input V_1 = 1.5 V, applied to a load network as shown in a typical two-resistor potential-divider style figure (1 kΩ across the output), determine V_o at the op-amp output and the corresponding voltage across the load resistor, explaining the effect (or lack of effect) of an ideal op-amp's zero output impedance on the load voltage.

25. **[Unit IV | Topic: Differential Amplifier — CMRR Application | Type: Theory | Difficulty: Advanced]**
    Explain the differential-mode and common-mode operation of an op-amp differential amplifier in detail, and derive the expression for output voltage in terms of differential gain A_d, common-mode gain A_cm, and CMRR, showing how a high CMRR suppresses common-mode noise/interference present identically on both inputs.

26. **[Unit IV | Topic: Integrator — Practical Limitations | Type: Theory | Difficulty: Advanced]**
    Derive the output expression of an op-amp integrator from first principles (starting from the virtual-ground and capacitor charging relations), and explain the practical problem of DC output drift/saturation in a simple integrator circuit, along with one common remedy (e.g., a large feedback resistor in parallel with C).

27. **[Unit IV | Topic: Adder + Difference Amplifier Combined Design | Type: Numerical | Difficulty: Advanced]**
    Design an op-amp circuit that produces an output V_o = −(2V_1 + 3V_2) using a summing amplifier, specifying suitable resistor values (choosing R_f = 30 kΩ), and explain how you would modify the circuit to instead realize V_o = 2V_1 − 3V_2 using a combination of summing and difference amplifier stages.

28. **[Unit IV | Topic: Op-Amp Ideal vs Practical Parameters | Type: Theory | Difficulty: Advanced]**
    Discuss the following with respect to a practical operational amplifier and its deviation from the ideal case: (i) input offset voltage, (ii) input bias current, (iii) finite open-loop gain and its effect on closed-loop gain accuracy, (iv) finite bandwidth (gain-bandwidth product) and its effect on high-frequency amplifier performance.

---

## Coverage Summary

| Unit | Topics Fully Covered | Question Types | Difficulty Range |
|---|---|---|---|
| I — Semiconductor Diodes & Applications | Semiconductor materials, energy bands, intrinsic/extrinsic, p-n junction, depletion layer, V-I characteristics, rectifiers, filters, voltage multipliers, clippers, clampers, breakdown mechanisms, Zener regulator | Theory (22) + Numerical (14) | Basic → Advanced |
| II — Transistors (BJT & FET): Configurations, Biasing, Amplifier Analysis | BJT construction/action, I_CBO/I_CEO, CB/CE/CC configurations, biasing methods & stability, operating point, h-parameter model, gain computations for CE/CC | Theory (18) + Numerical (14) | Basic → Advanced |
| III — JFET, MOSFET & Switching Theory | JFET construction/action/pinch-off/characteristics/biasing, MOSFET types/construction/channel formation/amplifier-switch operation, number systems, Boolean algebra, logic gates, universal gates, canonical forms, K-map minimization | Theory (18) + Numerical (15) | Basic → Advanced |
| IV — Operational Amplifier | Ideal/practical op-amp parameters, virtual ground, slew rate, unity follower, CMRR, differential/common-mode operation, inverting/non-inverting amplifiers, adders, difference amplifiers, integrators | Theory (14) + Numerical (13) | Basic → Advanced |

**Total questions:** 134 (72 Theory, 62 Numerical) across 4 units, all strictly scoped to the given BEC-154 syllabus — no communication-systems/CO5-type content (modulation, wireless/cellular communication, radar, up-linking/down-linking) is included, since that unit is not part of this syllabus, consistent with the earlier syllabus-mapping check on the BEC201 question paper.
