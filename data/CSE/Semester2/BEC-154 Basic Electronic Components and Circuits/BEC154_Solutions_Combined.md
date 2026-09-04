# BEC-154 — Basic Electronic Components and Circuits
## Detailed Step-Wise Solutions — Units I–IV (Combined)

> Every question is restated in full before its answer. Every answer builds the underlying concept from scratch before solving. No algebraic or reasoning step is skipped. Tags match the question bank exactly for RAG cross-referencing.

---


## Detailed Step-Wise Solutions — UNIT I: Semiconductor Diodes and Applications

---

### Section A: Definitions & Concept Questions

**Q1. [Unit I | Topic: Semiconductor Materials | Type: Theory | Difficulty: Basic]**

**Question:** Define a semiconductor. Name two elemental and two compound semiconductor materials.

*Concept from scratch:* A **semiconductor** is a material whose electrical conductivity lies between that of a conductor and an insulator, and — critically — can be controllably altered (by doping, temperature, or an applied field) over many orders of magnitude, which is what makes it useful for building electronic devices.

- **Elemental semiconductors** (single element): **Silicon (Si)**, **Germanium (Ge)**.
- **Compound semiconductors** (two or more elements): **Gallium Arsenide (GaAs)**, **Indium Phosphide (InP)** (also acceptable: Cadmium Sulphide (CdS)).

---

**Q2. [Unit I | Topic: Energy Bands | Type: Theory | Difficulty: Basic]**

**Question:** Define the valence band, conduction band, and forbidden energy gap.

*Concept from scratch:* In a solid, electron energy levels group into bands (due to overlapping atomic orbitals in the crystal lattice):
- **Valence band:** The highest range of electron energies in which electrons are normally present at absolute zero — these electrons are bound to individual atoms and participate in bonding.
- **Conduction band:** The energy band above the valence band in which electrons are free to move through the crystal and conduct electric current.
- **Forbidden energy gap (band gap, E_g):** The range of energies between the top of the valence band and the bottom of the conduction band in which no electron states exist — an electron must acquire at least this much energy to jump from the valence band to the conduction band.

---

**Q3. [Unit I | Topic: Energy Bands | Type: Theory | Difficulty: Basic]**

**Question:** Distinguish between a conductor, an insulator, and a semiconductor on the basis of energy band gap.

*Concept from scratch:* The size of the forbidden energy gap (E_g) determines how easily electrons can cross from the valence band to the conduction band, which determines conductivity:
- **Conductor:** No forbidden gap — valence and conduction bands overlap, so free electrons are abundant even at very low energy (e.g., metals like copper).
- **Insulator:** Very large E_g (typically > 5 eV, e.g., ~6 eV for diamond) — electrons essentially never acquire enough thermal energy to cross into the conduction band, so conductivity is negligible.
- **Semiconductor:** Small E_g (typically ~1 eV — e.g., 1.1 eV for silicon, 0.7 eV for germanium) — at room temperature, a modest number of electrons do gain enough thermal energy to cross into the conduction band, giving conductivity intermediate between conductor and insulator, and one that is strongly temperature/doping dependent.

---

**Q4. [Unit I | Topic: Intrinsic/Extrinsic Semiconductors | Type: Theory | Difficulty: Basic]**

**Question:** Describe the difference between intrinsic and extrinsic semiconductors.

*Concept from scratch:*
- **Intrinsic semiconductor:** A pure semiconductor material (no impurities added) in which the number of free electrons exactly equals the number of holes, both generated purely by thermal breaking of covalent bonds. Conductivity is low and strongly temperature-dependent.
- **Extrinsic semiconductor:** A semiconductor into which controlled impurities have been deliberately added (doped) to increase and control its conductivity, creating either an excess of free electrons (n-type) or an excess of holes (p-type), depending on the impurity used.

---

**Q5. [Unit I | Topic: Doping | Type: Theory | Difficulty: Basic]**

**Question:** Define doping. Distinguish between a donor impurity and an acceptor impurity.

*Concept from scratch:* **Doping** is the deliberate, controlled addition of a small, specific concentration of impurity atoms into a pure (intrinsic) semiconductor crystal to alter its electrical properties.
- **Donor impurity:** A pentavalent (5 valence electrons) impurity atom (e.g., Phosphorus, Arsenic) added to a tetravalent semiconductor (Si/Ge) — four of its electrons form covalent bonds with neighboring atoms, and the fifth is loosely bound and easily "donated" to the conduction band, creating a free electron. Produces an **n-type** semiconductor.
- **Acceptor impurity:** A trivalent (3 valence electrons) impurity atom (e.g., Boron, Indium, Gallium) added to a tetravalent semiconductor — it forms only three covalent bonds with neighboring atoms, leaving one bond incomplete (a "hole") that readily accepts an electron from a neighboring bond. Produces a **p-type** semiconductor.

---

**Q6. [Unit I | Topic: n-type/p-type Semiconductors | Type: Theory | Difficulty: Basic]**

**Question:** Define n-type and p-type semiconductors, naming the majority and minority charge carriers in each.

*Concept from scratch:*
- **n-type semiconductor:** Formed by doping with a donor (pentavalent) impurity. **Majority carriers: free electrons.** **Minority carriers: holes** (thermally generated).
- **p-type semiconductor:** Formed by doping with an acceptor (trivalent) impurity. **Majority carriers: holes.** **Minority carriers: free electrons** (thermally generated).

---

**Q7. [Unit I | Topic: p-n Junction | Type: Theory | Difficulty: Basic]**

**Question:** What is a p-n junction? Briefly describe how it is formed.

*Concept from scratch:* A **p-n junction** is the boundary/interface formed when a p-type semiconductor region and an n-type semiconductor region are joined together within a single continuous crystal (not simply glued — it must be a continuous crystal lattice for proper junction behavior). It is typically formed by doping different regions of the same silicon/germanium crystal with acceptor impurities on one side and donor impurities on the other (e.g., by diffusion or ion implantation), creating a p-region and n-region that meet at a metallurgical junction. This junction is the fundamental building block of the semiconductor diode.

---

**Q8. [Unit I | Topic: Depletion Layer | Type: Theory | Difficulty: Basic]**

**Question:** Define the depletion layer (depletion region) of a p-n junction. What is the barrier potential?

*Concept from scratch:* When a p-n junction forms, free electrons near the junction on the n-side diffuse across into the p-side (where hole concentration is high), and holes similarly diffuse from the p-side into the n-side — this diffusion leaves behind fixed, uncompensated ionized dopant atoms near the junction (positive ions on the n-side, negative ions on the p-side), with no free mobile carriers left in this narrow region.

- **Depletion layer (depletion region):** This narrow region on either side of the junction that has been "depleted" of mobile charge carriers, containing only fixed (immobile) ionized donor/acceptor atoms.
- **Barrier potential:** The electric field set up by these fixed ions across the depletion region opposes further diffusion of carriers — this built-in potential difference that must be overcome for current to flow is the barrier potential (typically ≈0.7 V for silicon, ≈0.3 V for germanium, at room temperature).

---

**Q9. [Unit I | Topic: Diode Biasing | Type: Theory | Difficulty: Basic]**

**Question:** Define forward bias and reverse bias of a p-n junction diode.

*Concept from scratch:*
- **Forward bias:** The p-side is connected to the positive terminal of an external source and the n-side to the negative terminal. This reduces the effective barrier potential, narrows the depletion region, and allows majority carriers to flow easily across the junction — the diode conducts significant current.
- **Reverse bias:** The p-side is connected to the negative terminal and the n-side to the positive terminal. This increases the effective barrier potential, widens the depletion region, and allows only a very small leakage (minority-carrier) current to flow — the diode is essentially non-conducting.

---

**Q10. [Unit I | Topic: V-I Characteristics | Type: Theory | Difficulty: Basic]**

**Question:** Sketch the general shape of the V-I characteristic of a p-n junction diode and identify the knee (cut-in) voltage.

*Concept from scratch (description of the curve, since this is a sketch-based question):* In the **forward-bias** region (positive V-axis), the current stays very close to zero until the applied voltage approaches the barrier potential; beyond this point (the **knee or cut-in voltage**, ≈0.7 V for Si, ≈0.3 V for Ge), current rises steeply and almost linearly with further increase in voltage. In the **reverse-bias** region (negative V-axis), only a tiny, almost constant leakage (saturation) current flows, essentially independent of the reverse voltage magnitude — until the reverse voltage becomes large enough to reach the breakdown voltage, at which point reverse current rises sharply.

The **knee (cut-in) voltage** is the forward voltage at which the diode current begins to increase rapidly — i.e., the point marking the transition from the near-flat, negligible-current region to the steep, conducting region of the forward characteristic.

---

**Q11. [Unit I | Topic: Diode Parameters | Type: Theory | Difficulty: Basic]**

**Question:** Define the cut-in (threshold) voltage of a diode. State its typical value for silicon and germanium diodes.

*Concept from scratch:* The **cut-in voltage** is the minimum forward voltage that must be applied across a diode before it begins to conduct appreciable (significant) current — below this voltage, the diode current is negligible; beyond it, current rises sharply.

**Typical values:** **Silicon (Si): ≈0.7 V**, **Germanium (Ge): ≈0.3 V**.

---

**Q12. [Unit I | Topic: Rectifiers | Type: Theory | Difficulty: Basic]**

**Question:** Define rectification. Distinguish between a half-wave and a full-wave rectifier.

*Concept from scratch:* **Rectification** is the process of converting an alternating current (AC) input into a unidirectional (pulsating DC) output, using the one-way conducting property of a diode.

- **Half-wave rectifier:** Uses a single diode, and conducts (produces output) during only **one half-cycle** (say, the positive half) of the input AC waveform; during the other half-cycle, the diode is reverse-biased and output is zero.
- **Full-wave rectifier:** Uses either a center-tapped transformer with two diodes, or four diodes in a bridge configuration, and produces output current during **both half-cycles** of the input — the output during the negative half-cycle is "flipped" to also flow in the same direction through the load, giving a more continuous (less pulsating) DC output.

---

**Q13. [Unit I | Topic: Rectifiers | Type: Theory | Difficulty: Basic]**

**Question:** Define ripple factor and efficiency of a rectifier.

*Concept from scratch:*
- **Ripple factor (γ):** A measure of the AC (fluctuating) content remaining in the rectifier's DC output, defined as the ratio of the RMS value of the AC (ripple) component of the output to the DC (average) component of the output: γ = V_ac(rms)/V_dc. A lower ripple factor indicates a "smoother" (more purely DC) output.
- **Rectification efficiency (η):** The ratio of the DC output power delivered to the load, to the total AC input power supplied to the rectifier circuit: η = P_dc/P_ac. It indicates how effectively the rectifier converts AC power into usable DC power.

---

**Q14. [Unit I | Topic: Filters | Type: Theory | Difficulty: Basic]**

**Question:** What is the purpose of a filter circuit following a rectifier? Name two common types of filter.

*Concept from scratch:* A rectifier alone produces a *pulsating* DC output (still containing significant AC ripple component, especially for a half-wave rectifier). A **filter circuit** is placed after the rectifier to smooth out this pulsating output into a much steadier, near-constant DC voltage, by using reactive components (capacitors/inductors) that store energy during the peaks of the pulsations and release it during the troughs, reducing the ripple.

**Common filter types:** **Capacitor (shunt-C) filter**, **Inductor (series-L) filter** (also acceptable: LC filter, π-filter/CLC filter).

---

**Q15. [Unit I | Topic: Voltage Multipliers | Type: Theory | Difficulty: Basic]**

**Question:** Define a voltage doubler. What is its basic principle?

*Concept from scratch:* A **voltage doubler** is a diode-capacitor circuit that produces a DC output voltage approximately **twice** the peak value of the AC input voltage, without requiring a step-up transformer.

**Basic principle:** It uses diodes to successively charge two (or more) capacitors to the peak input voltage during alternate half-cycles, then combines (adds) these charged-capacitor voltages in series to produce a combined output equal to roughly twice the peak input — essentially cascading two half-wave rectifier-and-clamper-like actions.

---

**Q16. [Unit I | Topic: Clippers | Type: Theory | Difficulty: Basic]**

**Question:** Define a clipper (limiter) circuit. Distinguish between series and shunt (parallel) clippers.

*Concept from scratch:* A **clipper (limiter) circuit** is a diode circuit that "clips off" (removes) a portion of the input waveform above and/or below a certain reference voltage level, without affecting the rest of the waveform — used for waveshaping and protection.

- **Series clipper:** The diode is connected **in series** with the load; the diode conducts (passes the signal to the load) during the portion of the cycle where it is forward-biased, and blocks (clips) the signal during the portion where it is reverse-biased.
- **Shunt (parallel) clipper:** The diode is connected **in parallel** with the load (across the output); when the diode conducts, it effectively short-circuits (clamps) the output to a fixed reference level, clipping that portion of the waveform, while for the rest of the cycle (diode reverse-biased/open), the input passes through to the output largely unaffected.

---

**Q17. [Unit I | Topic: Clampers | Type: Theory | Difficulty: Basic]**

**Question:** Define a clamper circuit. How does it differ functionally from a clipper?

*Concept from scratch:* A **clamper circuit** (DC restorer) is a diode-capacitor circuit that shifts an entire AC waveform up or down by a fixed DC level, without changing its shape — it "clamps" one extremity of the waveform (its peak or trough) to a fixed reference voltage level.

**Difference from a clipper:** A clipper **removes/cuts off** a portion of the waveform (changing its shape), whereas a clamper **preserves the full shape** of the waveform entirely, merely **shifting its DC level** (repositioning the whole waveform vertically) without altering the shape itself.

---

**Q18. [Unit I | Topic: Breakdown Mechanisms | Type: Theory | Difficulty: Basic]**

**Question:** Name the two breakdown mechanisms in a p-n junction diode under reverse bias.

*Concept from scratch:* When the reverse bias voltage across a p-n junction is increased beyond a certain limit, the junction "breaks down" and conducts a large reverse current. The two mechanisms are:

1. **Zener breakdown**

2. **Avalanche breakdown**

---

**Q19. [Unit I | Topic: Breakdown Mechanisms | Type: Theory | Difficulty: Basic]**

**Question:** Distinguish between Zener breakdown and avalanche breakdown.

*Concept from scratch:*
- **Zener breakdown:** Occurs in **heavily doped** junctions with a **narrow** depletion region. The very high electric field (even at relatively low reverse voltage) directly breaks (ruptures) covalent bonds within the depletion region, generating a large number of electron-hole pairs directly via this strong field — occurs typically at reverse voltages below about 5–6 V.
- **Avalanche breakdown:** Occurs in **lightly doped** junctions with a **wider** depletion region, at **higher** reverse voltages. Minority carriers crossing the depletion region are accelerated by the field to high velocities and collide with the crystal lattice, knocking loose additional electron-hole pairs (impact ionization); these newly freed carriers are, in turn, also accelerated and cause further collisions, creating a multiplying, "avalanche" chain reaction of carrier generation.

---

**Q20. [Unit I | Topic: Zener Diode | Type: Theory | Difficulty: Basic]**

**Question:** Define a Zener diode. How does its V-I characteristic differ from a normal p-n junction diode?

*Concept from scratch:* A **Zener diode** is a specially designed, heavily-doped p-n junction diode intended to operate in the **reverse breakdown region** in normal (intentional) use, unlike a regular diode which is normally kept out of breakdown to avoid damage.

**Difference in V-I characteristic:** In the forward direction, a Zener diode behaves like an ordinary diode. In the reverse direction, however, once the reverse voltage reaches the diode's rated **Zener voltage (V_Z)**, the current increases very sharply for almost no further increase in voltage — i.e., the reverse characteristic becomes nearly **vertical** at V_Z, which is precisely the property exploited for voltage regulation, since the voltage across the diode stays essentially constant (=V_Z) over a wide range of reverse current.

---

**Q21. [Unit I | Topic: Zener Diode as Regulator | Type: Theory | Difficulty: Basic]**

**Question:** Explain the basic principle by which a Zener diode acts as a voltage (shunt) regulator.

*Concept from scratch:* A Zener diode, operated in reverse breakdown, maintains a nearly constant voltage (V_Z) across itself over a wide range of current through it. By connecting the Zener diode in **parallel (shunt) with the load**, and a series resistor (R_S) between the (possibly varying) supply and this parallel combination, any variation in supply voltage or load current is absorbed by a corresponding change in the current through the Zener diode (I_Z) — since the diode's own voltage stays essentially fixed at V_Z, the voltage across the load (which is in parallel with the Zener) also stays essentially fixed at V_Z, regardless of these variations, as long as the Zener remains within its rated current/power range.

---

**Q22. [Unit I | Topic: Diode Approximations | Type: Theory | Difficulty: Basic]**

**Question:** Define the ideal diode model. State its assumed forward and reverse characteristics.

*Concept from scratch:* The **ideal diode model** is a simplified approximation used for quick circuit analysis, treating the diode as a perfect one-way switch:
- **Forward bias (conducting):** Assumed to behave as a **short circuit** (zero resistance, zero voltage drop) — conducts current with no opposition whatsoever.
- **Reverse bias (non-conducting):** Assumed to behave as an **open circuit** (infinite resistance) — allows absolutely no current to flow, regardless of the reverse voltage magnitude.

(This ignores the real diode's cut-in voltage, forward resistance, and reverse leakage current — refinements captured by more detailed models like the constant-voltage-drop model or the piecewise-linear model.)

---

### Section B: Computational & Applied Problems

**Q23. [Unit I | Topic: Rectifiers | Type: Numerical | Difficulty: Intermediate]**

**Question:** A half-wave rectifier is fed from a transformer secondary of RMS voltage 30 V. Assuming an ideal diode, find the peak output voltage, DC output voltage, and ripple factor.

*Step 1 — Find the peak input voltage from the given RMS value:*
V_rms = V_m/√2  ⟹  V_m = V_rms × √2 = 30 × 1.414 = **42.43 V**

*Step 2 — Peak output voltage (ideal diode, no drop):*
V_m(out) = **42.43 V** (same as input peak, since the ideal diode is assumed to have zero forward voltage drop when conducting)

*Step 3 — DC (average) output voltage for a half-wave rectifier (standard result, derived by averaging a half-sinusoid pulse over the full period):*
V_dc = V_m/π = 42.43/3.1416 = **13.51 V**

*Step 4 — Ripple factor for a half-wave rectifier (standard derived result):*
γ = √[(V_rms(out)/V_dc)² − 1]

For a half-wave rectifier, V_rms(out) = V_m/2 = 42.43/2 = 21.21 V

γ = √[(21.21/13.51)² − 1] = √[(1.570)² − 1] = √[2.465−1] = √1.465 = **1.21**

*(This matches the well-known standard result that a half-wave rectifier has ripple factor ≈1.21, indicating the AC ripple content actually exceeds the DC content — a very "rough" DC output.)*

---

**Q24. [Unit I | Topic: Rectifiers | Type: Numerical | Difficulty: Intermediate]**

**Question:** A full-wave bridge rectifier has a transformer secondary RMS voltage of 20 V (bridge configuration) and a load resistance of 1 kΩ. Assuming ideal diodes, find the DC output voltage, DC output current, and ripple factor.

*Step 1 — Peak input voltage:*
V_m = V_rms × √2 = 20 × 1.414 = **28.28 V**

*Step 2 — DC output voltage for a full-wave (bridge) rectifier (standard result — double that of half-wave, since both half-cycles contribute):*
V_dc = 2V_m/π = (2×28.28)/3.1416 = 56.56/3.1416 = **18.01 V**

*Step 3 — DC output current:*
I_dc = V_dc/R_L = 18.01/1000 = **18.01 mA**

*Step 4 — Ripple factor for a full-wave rectifier (standard derived result):*
For full-wave rectification, V_rms(out) = V_m/√2 = 28.28/1.414 = 20 V (equal to the input RMS, as expected, since the bridge simply "folds" the negative half up without changing RMS magnitude)

γ = √[(V_rms(out)/V_dc)² − 1] = √[(20/18.01)² − 1] = √[(1.1105)² − 1] = √[1.2332−1] = √0.2332 = **0.483**

*(This confirms the standard result that full-wave rectification has a much lower ripple factor (≈0.48) than half-wave (≈1.21) — a significantly smoother DC output.)*

---

**Q25. [Unit I | Topic: Full-Wave Bridge Rectifier | Type: Theory | Difficulty: Intermediate]**

**Question:** Draw the circuit diagram of a full-wave bridge rectifier and explain its working during both half-cycles of the input, indicating which diodes conduct in each half-cycle.

*Concept and working (description, since this is a circuit-diagram/explanation question):* A bridge rectifier uses **four diodes** (D1, D2, D3, D4) arranged in a diamond/bridge configuration, connecting the transformer's two secondary terminals to the load resistor R_L through the diode network, without needing a center-tapped transformer.

*Step 1 — Positive half-cycle:* When the top terminal of the secondary is positive (and the bottom terminal negative), **diodes D1 and D2** (the pair oriented to conduct in this polarity) become forward-biased and conduct, while D3 and D4 remain reverse-biased (blocking). Current flows from the transformer, through D1, through the load R_L (in a defined direction, say top-to-bottom), through D2, and back to the transformer.

*Step 2 — Negative half-cycle:* When the polarity reverses (bottom terminal now positive), **diodes D3 and D4** become forward-biased and conduct instead, while D1 and D2 become reverse-biased. Current now flows from the transformer, through D3, through the load R_L — critically, in the **same direction** as before (top-to-bottom) due to the bridge's diagonal diode arrangement — through D4, and back to the transformer.

*Step 3 — Net effect:* Since current flows through R_L in the same direction during both half-cycles, the output across R_L is a series of unidirectional pulses (one pulse per half-cycle, so two pulses per full input cycle) — this is why the bridge rectifier is a full-wave rectifier, and why it achieves this without needing a center-tapped transformer (unlike the two-diode center-tap full-wave configuration).

---

**Q26. [Unit I | Topic: Clippers | Type: Numerical | Difficulty: Intermediate]**

**Question:** A series clipper circuit uses an ideal diode in series with a 1 kΩ resistor, with the diode oriented to conduct for positive input. For a sinusoidal input of peak 20 V, sketch and describe the output waveform.

*Step 1 — Analyze the positive half-cycle:* Since the diode is oriented to conduct for positive input, during the positive half-cycle the diode is forward-biased (ideal diode ⟹ acts as a short circuit), so the input voltage appears directly (undiminished, since the diode has zero drop) across the output (the 1 kΩ resistor).

*Step 2 — Analyze the negative half-cycle:* During the negative half-cycle, the diode is reverse-biased (acts as an open circuit), so no current flows through the resistor, and the output voltage is **zero** (all the input voltage appears across the now-open diode instead, none across R).

*Step 3 — Describe the resulting output waveform:* The output waveform is a series of **positive half-sine pulses only** — identical in shape to the positive half of the input sine wave (peaking at +20 V), with the entire negative half-cycle **clipped off (flattened to 0 V)**. This is functionally identical to the output of a half-wave rectifier, since a series clipper with this diode orientation *is* essentially a half-wave rectifier circuit.

---

**Q27. [Unit I | Topic: Clippers | Type: Numerical | Difficulty: Intermediate]**

**Question:** A parallel (shunt) clipper uses an ideal diode with a 4 V battery in series with it (biasing the clipping level), across a 1 kΩ series resistor, for a square-wave input alternating between +20 V and −5 V. Determine the output voltage levels.

*Step 1 — Set up the circuit understanding:* The diode (in series with the 4 V battery) is connected in parallel with the output, across which the clipped waveform appears; a 1 kΩ resistor is in series between the input source and this diode-battery parallel branch.

*Step 2 — Determine the diode's conduction condition.* Assume the battery is oriented such that the diode conducts (clamping the output) whenever the input tries to exceed +4 V (a standard configuration for this type of problem, where the 4 V battery sets the clipping reference level).

*Step 3 — Analyze the +20 V portion of the input (input exceeds the 4 V threshold):* The diode becomes forward-biased and conducts, clamping the output to the fixed reference level set by the battery. Since the diode is ideal (zero drop when conducting), the output is clamped at exactly **+4 V** — any input voltage beyond +4 V is dropped entirely across the series 1 kΩ resistor instead.

*Step 4 — Analyze the −5 V portion of the input (input is below the 4 V threshold):* The diode is reverse-biased (input voltage is less than the battery's reference level, so the diode does not conduct) — it acts as an open circuit. With no current flowing through the 1 kΩ resistor (no closed path), there is no voltage drop across it, so the full input voltage appears at the output: output = **−5 V**.

*Result:* **Output = +4 V (clipped/flat) during the portion of the input at +20 V; output = −5 V (unclipped, follows input) during the portion of the input at −5 V.**

---

**Q28. [Unit I | Topic: Clampers | Type: Numerical | Difficulty: Intermediate]**

**Question:** A positive clamper circuit (diode, capacitor, resistor) is fed with a square wave of peak values +V and −V (ideal diode, RC time constant much larger than the period). Sketch and explain the output waveform, showing the DC shift introduced.

*Step 1 — Recall the basic positive clamper configuration:* Input source → series capacitor C → output node (across which R is connected to ground) → diode connected from the output node to ground, oriented to conduct when the output tries to go negative (this orientation makes it a "positive" clamper, since it prevents the output from going below approximately 0 V, effectively pushing/clamping the whole waveform upward).

*Step 2 — Analyze the initial transient (first negative half-cycle of input, assumed to occur first from an initially uncharged capacitor):* When the input first swings to −V, the diode is forward-biased (output tries to go negative, but the diode clamps it near 0 V) and conducts heavily, rapidly charging the capacitor. Since the diode is ideal and clamps the output to ≈0 V during this instant, the capacitor charges to a voltage equal to the full input swing: V_C = V (charged with polarity such that it will oppose/block the diode from conducting again once charged).

*Step 3 — Analyze subsequent cycles (steady state, RC≫T so the capacitor holds its charge essentially constant between input transitions):* Since the capacitor is now charged to V and does not discharge appreciably (large RC time constant), it acts as a constant DC voltage source in series with the input for all subsequent time — effectively adding a **constant DC offset of +V** to the entire input waveform (shifting it upward by V), since output = input + V_C(fixed).

*Step 4 — Determine the resulting output waveform levels:* Original input swung between −V and +V (span of 2V, centered on 0). Adding the fixed +V offset: output now swings between (−V+V)=**0 V** and (+V+V)=**+2V**.

*Result:* **The output waveform retains the exact same square shape as the input, but is shifted upward so it now swings between 0 V and +2V, instead of between −V and +V** — the defining "positive clamping" action: the lower peak of the waveform is clamped at (approximately) 0 V, and the entire waveform is lifted above the zero line, introducing a **DC shift of +V**.

---

**Q29. [Unit I | Topic: Zener Diode Regulator | Type: Numerical | Difficulty: Intermediate]**

**Question:** A Zener diode with V_Z = 10 V and P_Z(max) = 400 mW is used as a shunt regulator with a series resistance R_S = 220 Ω, fed from a 20 V source, with a load resistance R_L = 180 Ω. Determine V_L, I_L, I_Z, and I_R, and verify the Zener is within its power rating.

*Step 1 — Concept:* As long as the Zener diode is conducting in breakdown, the load voltage V_L equals the Zener voltage V_Z directly (since they're in parallel), regardless of small variations, provided the Zener current stays within its rated range.

*Step 2 — Load voltage:*
V_L = V_Z = **10 V**

*Step 3 — Load current:*
I_L = V_L/R_L = 10/180 = **0.0556 A = 55.6 mA**

*Step 4 — Total current from the source, through the series resistor (using the voltage drop across R_S):*
I_R = (V_source − V_Z)/R_S = (20−10)/220 = 10/220 = **0.0455 A = 45.5 mA**

*Step 5 — Zener current, using KCL at the node where R_S, the Zener, and R_L all meet (total current in from R_S splits between the Zener and the load):*
I_R = I_Z + I_L  ⟹  I_Z = I_R − I_L = 45.5 − 55.6 = **−10.1 mA**

*Step 6 — Interpretation of the negative result:* A negative Zener current is not physically possible — this indicates that, with these particular component values, the series resistor **cannot supply enough current** even to meet the load's demand alone (I_R = 45.5 mA < I_L = 55.6 mA required by the load), meaning the Zener diode would need to draw current rather than sink it, which it cannot do. **In this configuration, the Zener diode would actually fall out of regulation** (not conduct in breakdown at all), and the load voltage would instead be determined by simple voltage-divider action between R_S and R_L (not clamped at V_Z).

*Step 7 — Find the actual load voltage in this non-regulating condition (Zener effectively open, since it can't source current):*
V_L(actual) = V_source × R_L/(R_S+R_L) = 20 × 180/(220+180) = 20 × 180/400 = 20×0.45 = **9 V**

*Result and check:* Since this actual voltage (9 V) is **below** V_Z (10 V), the Zener genuinely would not conduct (confirming it's reverse-biased below its breakdown point) — so **V_L ≈ 9 V, I_L = 9/180 = 50 mA, I_Z ≈ 0 mA (Zener not conducting), I_R = I_L = 50 mA** in this particular circuit, and the regulator **fails to regulate** under this load condition (the chosen R_L is too small / draws too much current for this R_S to support proper Zener regulation) — an important design lesson: always check that the minimum available current through R_S exceeds the load's maximum demand before assuming ideal Zener regulation.

---

**Q30. [Unit I | Topic: Voltage Doubler | Type: Numerical | Difficulty: Intermediate]**

**Question:** Explain the working of a half-wave voltage doubler circuit (two diodes, two capacitors) fed from a sinusoidal input of peak value V_m, and determine the approximate DC output voltage across the load (ideal diodes and capacitors assumed).

*Step 1 — Circuit configuration:* Input source → capacitor C1 → node A; diode D1 from node A to ground (oriented to conduct when node A goes negative); diode D2 from node A to output node B (oriented to conduct when current flows from A to B); capacitor C2 from node B to ground, with the load connected across C2.

*Step 2 — Analyze the negative half-cycle of the input (input swings to −V_m):* D1 becomes forward-biased (conducts), clamping node A near 0 V momentarily while charging C1 to the full peak voltage V_m (with a polarity such that node A is held near ground while the source is at −V_m, meaning C1 charges to V_m).

*Step 3 — Analyze the positive half-cycle (input swings to +V_m):* Now the source adds to the voltage already stored on C1 (from Step 2), so node A rises to approximately +2V_m (the source's own +V_m, plus the +V_m already held across C1 acting like a battery in series). D1 is now reverse-biased (blocks), but D2 becomes forward-biased and conducts, charging C2 up to this new peak level at node A.

*Step 4 — Steady-state DC output:* After a few cycles, capacitor C2 charges up to and holds approximately the peak value reached at node A, which is **2V_m**.

**Result: V_out(DC) ≈ 2V_m** — confirming the "doubler" action: the output DC voltage is approximately twice the peak of the input AC voltage, achieved without any step-up transformer, purely through the sequential charge-transfer action of the two diode-capacitor stages.

---

**Q31. [Unit I | Topic: Diode DC Analysis (Load Line) | Type: Numerical | Difficulty: Intermediate]**

**Question:** A silicon diode (cut-in voltage 0.7 V) is connected in series with a 1 kΩ resistor across a 10 V DC source. Using the constant-voltage-drop diode model, find the diode current and the voltage across the resistor.

*Step 1 — Recall the constant-voltage-drop model:* Once conducting, the diode is assumed to maintain a fixed voltage drop equal to its cut-in voltage (0.7 V for silicon), regardless of the current through it.

*Step 2 — Write the KVL equation around the series loop (source, diode, resistor):*
V_source = V_diode + I×R

*Step 3 — Substitute known values:*
10 = 0.7 + I×1000

*Step 4 — Solve for I:*
10 − 0.7 = I×1000
9.3 = I×1000
I = 9.3/1000 = **9.3 mA**

*Step 5 — Voltage across the resistor:*
V_R = I×R = 9.3mA × 1kΩ = **9.3 V**

*Step 6 — Verify with KVL:* V_diode + V_R = 0.7 + 9.3 = 10 V = V_source ✓

---

### Section C: Advanced Theory & Numericals

**Q32. [Unit I | Topic: p-n Junction Formation | Type: Theory | Difficulty: Advanced]**

**Question:** Explain, with the help of energy-band diagrams, the formation of the depletion region and the barrier potential at an unbiased p-n junction. How does this barrier potential change under forward and reverse bias?

*Step 1 — Before joining (separate p and n materials):* In an isolated p-type material, the Fermi level lies close to the valence band (many holes, few electrons); in an isolated n-type material, the Fermi level lies close to the conduction band (many electrons, few holes). Their energy bands, drawn separately, are at different relative heights.

*Step 2 — Immediately upon junction formation (before equilibrium):* Since there's a large concentration gradient of electrons (high in n-side, low in p-side) and holes (high in p-side, low in n-side) across the newly formed junction, diffusion begins: electrons diffuse from n→p, holes diffuse from p→n.

*Step 3 — Formation of the depletion region:* As electrons leave the n-side near the junction, they leave behind fixed, positively-charged donor ions (which cannot move — they're part of the crystal lattice). As holes leave the p-side near the junction, they leave behind fixed, negatively-charged acceptor ions. This creates a narrow region on both sides of the junction that is depleted of mobile carriers — the **depletion region** — containing only these fixed space charges.

*Step 4 — Formation of the barrier potential (built-in electric field):* These fixed, oppositely-charged ions on either side of the junction set up an internal electric field, pointing from the n-side (positive ions) toward the p-side (negative ions). This field opposes further diffusion of majority carriers across the junction (it pushes electrons back toward the n-side and holes back toward the p-side) — a dynamic equilibrium is reached where this field-driven "drift" current exactly balances the concentration-driven "diffusion" current, and no net current flows.

*Step 5 — Energy-band diagram interpretation at equilibrium:* At equilibrium, the Fermi level must be flat (constant) across the entire junction (a fundamental requirement of thermal equilibrium). Since the p-side and n-side had their bands at different relative positions before joining (Step 1), aligning their Fermi levels causes the energy bands to **bend** near the junction — the conduction and valence bands on the n-side sit at lower energy than on the p-side. This band-bending, expressed as an energy difference, directly represents the **barrier potential (V_0)** — physically, it's the potential energy hill that a majority carrier must climb to cross from its own side to the other.

*Step 6 — Effect of forward bias:* Applying a forward bias (p-side positive relative to n-side) opposes the internal field — the external voltage reduces the net barrier, causing the bands to bend less steeply (barrier height reduced by the applied voltage, effectively becoming V_0 − V_applied). This narrows the depletion region and allows majority carrier diffusion to dominate again, resulting in significant forward current once the bias approaches V_0.

*Step 7 — Effect of reverse bias:* Applying a reverse bias (n-side positive relative to p-side) adds to the internal field — the barrier height increases (becomes V_0 + V_applied), causing the bands to bend even more steeply. This widens the depletion region further, suppressing majority-carrier diffusion almost entirely, leaving only the very small minority-carrier drift current (reverse saturation current) to flow.

---

**Q33. [Unit I | Topic: Rectifiers — Comparative Analysis | Type: Theory | Difficulty: Advanced]**

**Question:** Derive the expressions for ripple factor and rectification efficiency for a full-wave rectifier, and compare these values with those of a half-wave rectifier, explaining the reasons for the difference.

*Step 1 — Set up the full-wave rectifier output waveform.* The output is a series of "humps," each hump being the absolute value of a sine wave: i(t) = I_m|sin(ωt)|, repeating with period T/2 (twice the frequency of the original AC input).

*Step 2 — Compute the DC (average) value of this output:*
I_dc = (1/π)∫₀^π I_m sin(θ) dθ = (I_m/π)[−cos θ]₀^π = (I_m/π)[−cos π − (−cos 0)] = (I_m/π)[−(−1)−(−1)] = (I_m/π)[1+1] = **2I_m/π**

*Step 3 — Compute the RMS value of this output:*
I_rms² = (1/π)∫₀^π I_m² sin²(θ) dθ = (I_m²/π)∫₀^π [(1−cos2θ)/2] dθ = (I_m²/2π)[θ − (sin2θ)/2]₀^π = (I_m²/2π)[π−0] = I_m²/2

So **I_rms = I_m/√2**

*Step 4 — Ripple factor, γ = √[(I_rms/I_dc)² − 1]:*
I_rms/I_dc = (I_m/√2)/(2I_m/π) = (π)/(2√2) = 3.1416/2.828 = 1.1107

γ = √[(1.1107)² − 1] = √[1.2336−1] = √0.2336 = **0.482**

*Step 5 — Rectification efficiency, η = P_dc/P_ac = I_dc²R_L / I_rms²(R_L+R_f) — assuming diode forward resistance R_f is negligible compared to R_L for simplicity (standard textbook assumption):*
η = I_dc²/I_rms² = (2I_m/π)² / (I_m/√2)² = (4I_m²/π²) / (I_m²/2) = (4/π²) × 2 = 8/π² = 8/9.87 = **0.812 (81.2%)**

*Step 6 — Repeat for half-wave rectifier (for comparison — standard known results, briefly re-derived):* For half-wave, I_dc = I_m/π, I_rms = I_m/2.

γ(half-wave) = √[(I_rms/I_dc)² − 1] = √[((I_m/2)/(I_m/π))² − 1] = √[(π/2)² − 1] = √[2.467−1] = √1.467 = **1.21**

η(half-wave) = I_dc²/I_rms² = (I_m/π)²/(I_m/2)² = (1/π²)×4 = 4/π² = 4/9.87 = **0.405 (40.5%)**

*Step 7 — Comparison and explanation:*

| Parameter | Half-wave | Full-wave |
|---|---|---|
| Ripple factor | 1.21 | 0.482 |
| Efficiency | 40.5% | 81.2% |

The full-wave rectifier has a **much lower ripple factor** and **double the efficiency** of the half-wave rectifier. This is because the full-wave rectifier utilizes **both half-cycles** of the input to deliver current to the load (doubling the DC output for the same peak input), while the AC/RMS content of the output does not increase in the same proportion (since the "shape" of each output hump is unchanged, and there are just twice as many of them, closer together, making the waveform overall smoother relative to its now-larger DC average) — hence a larger DC-to-AC ratio (lower ripple) and much more effective conversion of input AC power to usable DC output power (higher efficiency).

---

**Q34. [Unit I | Topic: Zener Regulator — Load & Line Regulation | Type: Numerical | Difficulty: Advanced]**

**Question:** For a Zener shunt regulator with V_Z = 10 V, R_S = 220 Ω, supplied from a source that varies between 18 V and 22 V, with load resistance fixed at R_L = 500 Ω: determine the Zener current at both source-voltage extremes, and comment on whether the regulator maintains a fixed load voltage over this range (assume Zener current rating is not exceeded).

*Step 1 — Load current (fixed, since V_L=V_Z=10V is assumed constant as long as the Zener is regulating, and R_L is fixed):*
I_L = V_Z/R_L = 10/500 = **20 mA** (same at both source extremes, as long as regulation holds)

*Step 2 — At V_source = 18 V: total current supplied through R_S:*
I_R = (V_source − V_Z)/R_S = (18−10)/220 = 8/220 = **36.36 mA**

*Step 3 — Zener current at V_source=18V, using KCL (I_R = I_Z + I_L):*
I_Z = I_R − I_L = 36.36 − 20 = **16.36 mA**

*Step 4 — At V_source = 22 V: total current supplied through R_S:*
I_R = (22−10)/220 = 12/220 = **54.55 mA**

*Step 5 — Zener current at V_source=22V:*
I_Z = I_R − I_L = 54.55 − 20 = **34.55 mA**

*Step 6 — Check that the Zener remains conducting (I_Z > 0) at the lower extreme:* At V_source=18V, I_Z=16.36 mA > 0, confirming the Zener does remain in breakdown/regulation at this lower voltage limit (a genuine check that must be verified — if I_Z had come out negative here, the regulator would fail at the low end, as seen in Q29).

*Step 7 — Comment on regulation:* Since the Zener stays in conduction across the *entire* 18 V–22 V source range (I_Z positive throughout, and — per the problem's assumption — within its rated current limit), **the load voltage remains fixed at V_L = V_Z = 10 V regardless of the source voltage varying by ±2V from a nominal 20V** — i.e., the circuit successfully provides "line regulation," absorbing all the source-voltage variation as a change in Zener current (16.36 mA to 34.55 mA) rather than allowing it to affect the load voltage.

---

**Q35. [Unit I | Topic: Full-Wave Rectifier with Filter | Type: Numerical | Difficulty: Advanced]**

**Question:** A full-wave rectifier with a capacitor filter supplies a load current of 100 mA at a DC output voltage of 20 V, with a specified ripple factor of 5%. Using the approximate capacitor-filter ripple formula, determine the required filter capacitance (supply frequency 50 Hz).

*Step 1 — Recall the approximate ripple factor formula for a full-wave rectifier with capacitor filter:*
γ = I_dc / (4√3 f C V_dc)

(This standard approximation arises from treating the capacitor's discharge through the load as approximately linear between successive charging peaks, which occur at twice the line frequency for full-wave rectification.)

*Step 2 — Rearrange to solve for C:*
C = I_dc / (4√3 f γ V_dc)

*Step 3 — Substitute values (I_dc=100mA=0.1A, f=50Hz, γ=0.05, V_dc=20V):*
C = 0.1 / (4 × 1.732 × 50 × 0.05 × 20)

*Step 4 — Compute the denominator step by step:*
4 × 1.732 = 6.928
6.928 × 50 = 346.4
346.4 × 0.05 = 17.32
17.32 × 20 = 346.4

*Step 5 — Divide:*
C = 0.1/346.4 = **2.887×10⁻⁴ F = 288.7 µF**

*Result:* A filter capacitor of approximately **289 µF** (commonly a standard value like 330 µF would be chosen in practice, rounding up to ensure the ripple specification is comfortably met) is required.

---

**Q36. [Unit I | Topic: Voltage Doubler & Clamper Combined | Type: Numerical | Difficulty: Advanced]**

**Question:** Sketch and explain the working of a full-wave voltage doubler circuit, and derive its approximate DC output voltage in terms of the peak input voltage V_m. Compare its ripple behavior with that of a half-wave voltage doubler.

*Step 1 — Circuit configuration (full-wave voltage doubler):* Two diodes D1, D2 and two capacitors C1, C2, connected such that D1 (with C1) charges during one half-cycle and D2 (with C2) charges during the *other* half-cycle — unlike the half-wave doubler (Q30), where the two stages operate in *cascade* (one depends on the other), here the two stages operate roughly *independently*, each charging its own capacitor once per full input cycle, with the two capacitors connected in series to form the total output.

*Step 2 — Analyze the positive half-cycle:* The input drives diode D1 into conduction (D2 reverse-biased), charging capacitor C1 up to the peak input voltage: V_C1 = V_m.

*Step 3 — Analyze the negative half-cycle:* The input (now reversed) drives diode D2 into conduction (D1 reverse-biased), charging capacitor C2 up to the peak input voltage (of the reversed polarity): V_C2 = V_m.

*Step 4 — Combine the two capacitor voltages.* Since C1 and C2 are connected in series (with the output taken across both together), and each independently charges to V_m once every full cycle:

**V_out(DC) = V_C1 + V_C2 = V_m + V_m = 2V_m**

(Same overall DC output level as the half-wave doubler, but achieved through a different, more "balanced" mechanism.)

*Step 5 — Compare ripple behavior:* In the **half-wave doubler**, only capacitor C2 (the output-holding capacitor) is ever recharged, and it is recharged only **once per full input cycle** (during only one specific half-cycle) — between these infrequent recharges, C2 must supply the entire load current on its own for a full cycle period, allowing it to discharge (and hence the ripple to build up) more before the next recharge. In the **full-wave doubler**, by contrast, the two capacitors C1 and C2 are recharged on **alternating half-cycles** (effectively topping up the series combination twice per full input cycle) — meaning the output experiences replenishment at **twice the frequency**, giving it noticeably **lower ripple** for the same capacitor values and load current, exactly analogous to why a full-wave rectifier has lower ripple than a half-wave rectifier (Q33).


## Detailed Step-Wise Solutions — UNIT II: Transistors (BJT and FET): Configurations, Biasing, and Amplifier Analysis

---

### Section A: Definitions & Concept Questions

**Q1. [Unit II | Topic: BJT Construction | Type: Theory | Difficulty: Basic]**

**Question:** Describe the basic construction of a bipolar junction transistor (BJT), naming its three terminals and two junctions.

*Concept from scratch:* A **BJT** is a three-layer semiconductor device formed by sandwiching one type of semiconductor between two layers of the opposite type, in either **NPN** (n-type — p-type — n-type) or **PNP** (p-type — n-type — p-type) arrangement.

**Three terminals:** **Emitter (E)** — heavily doped, emits (injects) majority carriers into the base; **Base (B)** — very thin and lightly doped, the middle/control region; **Collector (C)** — moderately doped and physically larger, collects the carriers that cross the base.

**Two junctions:** **Emitter-base junction (EBJ)** — between emitter and base; **Collector-base junction (CBJ)** — between base and collector.

---

**Q2. [Unit II | Topic: Transistor Action | Type: Theory | Difficulty: Basic]**

**Question:** Briefly explain transistor action in an NPN BJT — how does a small base current control a large collector current?

*Concept from scratch:* In normal (active-region) operation, the emitter-base junction is **forward-biased** and the collector-base junction is **reverse-biased**. The heavily-doped emitter injects a large number of electrons into the thin, lightly-doped base. Because the base is so thin and lightly doped, only a small fraction of these injected electrons recombine with holes in the base (this small recombination current is what constitutes the base current, I_B) — the vast majority of the injected electrons instead diffuse straight across the thin base and are swept into the collector by the strong reverse-bias field at the collector-base junction, constituting the collector current I_C. Since I_C depends on the (large) number of carriers injected by the emitter, while I_B depends only on the (small) recombination fraction, a **small change in I_B** (which controls how much the emitter injection is "allowed" to proceed, via its effect on the forward bias of the EBJ) produces a **proportionally much larger change in I_C** — this is the current-amplifying transistor action, characterized by the current gain β = I_C/I_B (typically 50–200 or more).

---

**Q3. [Unit II | Topic: Transistor Leakage Currents | Type: Theory | Difficulty: Basic]**

**Question:** Define I_CBO and I_CEO.

*Concept from scratch:*
- **I_CBO:** The collector-to-base leakage (reverse saturation) current, measured with the **emitter open-circuited** — i.e., the small reverse current that flows across the collector-base junction due to thermally generated minority carriers, when no emitter current is present.
- **I_CEO:** The collector-to-emitter leakage current, measured with the **base open-circuited** — this is larger than I_CBO because the small I_CBO leakage itself gets amplified by the transistor's own current gain as it flows through the base-emitter region (I_CEO ≈ (β+1)×I_CBO), even with no external base drive.

---

**Q4. [Unit II | Topic: BJT Configurations | Type: Theory | Difficulty: Basic]**

**Question:** Name the three basic BJT configurations (CB, CE, CC) and state which terminal is common to input and output in each.

*Concept from scratch:*
- **Common-Base (CB):** The **base** terminal is common to both the input (emitter-base) and output (collector-base) circuits.
- **Common-Emitter (CE):** The **emitter** terminal is common to both the input (base-emitter) and output (collector-emitter) circuits.
- **Common-Collector (CC):** The **collector** terminal is common to both the input (base-collector) and output (emitter-collector) circuits.

---

**Q5. [Unit II | Topic: BJT Configurations | Type: Theory | Difficulty: Basic]**

**Question:** Define current gain α (alpha) for the common-base configuration and β (beta) for the common-emitter configuration.

*Concept from scratch:*
- **α (alpha):** The ratio of collector current to emitter current in the CB configuration: **α = I_C/I_E**. Since I_C is always slightly less than I_E (a tiny fraction recombines in the base), α is always slightly less than 1 (typically 0.95–0.99).
- **β (beta):** The ratio of collector current to base current in the CE configuration: **β = I_C/I_B**. Since I_B is a small fraction of I_C, β is typically large (50–200 or more).

---

**Q6. [Unit II | Topic: BJT Configurations | Type: Theory | Difficulty: Basic]**

**Question:** Write the relationship between α and β for a BJT.

*Concept from scratch — brief derivation:* Starting from I_E = I_B + I_C (KCL at the transistor), and the definitions α=I_C/I_E, β=I_C/I_B:

**β = α/(1−α)**, equivalently **α = β/(1+β)**

---

**Q7. [Unit II | Topic: BJT vs FET | Type: Theory | Difficulty: Basic]**

**Question:** What are the key operational and structural differences between a Bipolar Junction Transistor (BJT) and a Field Effect Transistor (FET)?

*Concept from scratch:*

| Aspect | BJT | FET |
|---|---|---|
| Carrier type | **Bipolar** — both electrons and holes participate in conduction | **Unipolar** — only one type of carrier (electrons or holes) participates |
| Control mechanism | **Current-controlled** device — output current controlled by input (base) *current* | **Voltage-controlled** device — output current controlled by input (gate) *voltage*, via an electric field |
| Input impedance | Relatively **low** (input is a forward-biased junction, drawing base current) | Very **high** (gate is reverse-biased/insulated, drawing negligible current) |
| Noise | Comparatively higher | Comparatively lower (useful in low-noise front-end applications) |
| Thermal stability | Poorer (more susceptible to thermal runaway) | Better (generally more thermally stable) |

---

**Q8. [Unit II | Topic: Transistor Biasing | Type: Theory | Difficulty: Basic]**

**Question:** Define DC biasing of a transistor. Why is biasing necessary for amplifier operation?

*Concept from scratch:* **DC biasing** is the process of applying suitable fixed DC voltages/currents to a transistor's terminals to establish a specific, stable operating condition (quiescent point) in the **active region**, before any AC signal is applied.

**Why necessary:** An amplifier must faithfully reproduce (amplify) an AC input signal that swings both positive and negative. If the transistor is not biased into the active region (with sufficient "room" on both sides of its operating point on the load line), the output would clip during either the positive or negative half of the input swing (if biased too close to cut-off or saturation) — biasing establishes a stable, mid-active-region starting point (Q-point) so that the transistor can respond linearly to both halves of the input signal without distortion or clipping.

---

**Q9. [Unit II | Topic: Biasing Methods | Type: Theory | Difficulty: Basic]**

**Question:** Name three common methods of transistor biasing.

*Concept from scratch:*

1. **Fixed bias (base bias)**

2. **Collector-to-base bias (feedback bias)**

3. **Voltage-divider bias (self-bias/potential-divider bias)**

---

**Q10. [Unit II | Topic: Biasing — Stability | Type: Theory | Difficulty: Basic]**

**Question:** Define the stability factor S of a biasing circuit. Why is a low stability factor desirable?

*Concept from scratch:* The **stability factor (S)** measures how sensitively the collector current I_C changes in response to changes in the reverse-saturation (leakage) current I_CO (which itself varies strongly with temperature): **S = ∂I_C/∂I_CO**.

**Why low S is desirable:** I_CO increases significantly with temperature; if S is large, even a small temperature-driven change in I_CO would cause a large, unwanted shift in I_C (and hence the operating point) — potentially leading to distortion or even thermal runaway. A **low** stability factor means I_C stays relatively constant despite temperature-induced changes in I_CO, keeping the operating point stable across a range of operating temperatures.

---

**Q11. [Unit II | Topic: Voltage Divider Bias | Type: Theory | Difficulty: Basic]**

**Question:** Describe the voltage-divider (self) bias circuit and explain why it provides better stability than fixed bias.

*Concept from scratch:* In **voltage-divider bias**, two resistors R1 and R2 form a potential divider across the supply V_CC, setting a fixed voltage at the base (largely independent of the transistor's own β, provided the divider current is much larger than the base current). An emitter resistor R_E is also included, connected from the emitter to ground.

**Why more stable:** If I_C tends to increase (say, due to a temperature rise increasing I_CO or β), the emitter current I_E also increases, which increases the voltage drop across R_E (V_E = I_ER_E). Since the base voltage V_B is held essentially fixed by the divider, this rise in V_E **reduces** the effective base-emitter forward bias (V_BE = V_B − V_E), which in turn **reduces** the base current and hence pulls I_C back down — this is a **negative feedback** mechanism, automatically compensating for the initial increase and keeping the operating point far more stable than in fixed bias (which has no such self-correcting mechanism).

---

**Q12. [Unit II | Topic: Operating Point | Type: Theory | Difficulty: Basic]**

**Question:** Define the operating point (Q-point) of a transistor. Why is it usually located at the center of the DC load line for amplifier applications?

*Concept from scratch:* The **operating point (Q-point)** is the specific combination of DC collector current (I_CQ) and collector-emitter voltage (V_CEQ) at which the transistor sits when no AC signal is applied — it's the "resting" or quiescent state established by the biasing circuit.

**Why centered on the load line:** Placing the Q-point at the **center** of the active-region portion of the DC load line gives the output signal the **maximum symmetrical room to swing** in both directions (upward toward cut-off and downward toward saturation) around this point, before hitting either extreme — this allows the largest possible undistorted (unclipped) output signal swing for a given supply voltage and load resistance.

---

**Q13. [Unit II | Topic: CE Characteristics | Type: Theory | Difficulty: Basic]**

**Question:** Sketch the general shape of the common-emitter output (V-I) characteristics of an NPN BJT, identifying the active, saturation, and cut-off regions.

*Concept from scratch (description of the curve family, since this is a sketch-based question):* The CE output characteristics plot I_C (vertical axis) against V_CE (horizontal axis), for a family of curves each corresponding to a different fixed I_B value.

- **Cut-off region:** Near the origin (very low I_C, occurring when I_B ≈ 0) — both junctions are reverse-biased, and the transistor conducts negligible current, behaving like an open switch.
- **Saturation region:** The steep, rising portion of the curves at low V_CE (just after V_CE=0) — both junctions are forward-biased, and I_C rises very sharply for a small increase in V_CE, essentially independent of I_B in this narrow region; the transistor behaves like a closed switch (low V_CE(sat)).
- **Active region:** The broad, nearly-flat, roughly horizontal portion of each curve at higher V_CE — I_C is nearly independent of V_CE (mainly determined by I_B via β), and the curves are spread apart, evenly spaced for equal increments of I_B — this is the region used for linear amplification.

---

**Q14. [Unit II | Topic: h-parameter Model | Type: Theory | Difficulty: Basic]**

**Question:** Define the four h-parameters (h_i, h_r, h_f, h_o) of a two-port network, stating their units.

*Concept from scratch:* The h-parameters ("hybrid parameters") characterize a two-port network (like a transistor in a given configuration) using a mix of impedance and admittance-type quantities (hence "hybrid"):
- **h_i (input impedance):** Ratio of input voltage to input current, with the output short-circuited (AC-wise). Unit: **ohms (Ω)**.
- **h_r (reverse voltage transfer ratio):** Ratio of input voltage to output voltage, with the input open-circuited. **Dimensionless**.
- **h_f (forward current gain):** Ratio of output current to input current, with the output short-circuited. **Dimensionless**.
- **h_o (output admittance):** Ratio of output current to output voltage, with the input open-circuited. Unit: **siemens/mho (S)**.

---

**Q15. [Unit II | Topic: h-parameter Model | Type: Theory | Difficulty: Basic]**

**Question:** Write the h-parameter equivalent circuit equations for a transistor in terms of input/output voltage and current.

*Concept from scratch:* Treating the transistor (in a given configuration) as a two-port network with input voltage V_1, input current I_1, output voltage V_2, output current I_2:

**V_1 = h_i I_1 + h_r V_2**
**I_2 = h_f I_1 + h_o V_2**

(The first equation models the input port as a resistance h_i in series with a voltage-controlled voltage source h_rV_2, representing internal feedback from output to input. The second equation models the output port as a current-controlled current source h_fI_1 in parallel with an output admittance h_o.)

---

**Q16. [Unit II | Topic: Amplifier Parameters | Type: Theory | Difficulty: Basic]**

**Question:** Define voltage gain, current gain, input impedance, and output impedance of a transistor amplifier.

*Concept from scratch:*
- **Voltage gain (A_V):** Ratio of AC output voltage to AC input voltage, A_V = V_out/V_in.
- **Current gain (A_I):** Ratio of AC output current to AC input current, A_I = I_out/I_in.
- **Input impedance (R_i or Z_i):** The impedance "seen" by the signal source looking into the amplifier's input terminals, R_i = V_in/I_in.
- **Output impedance (R_o or Z_o):** The impedance "seen" by the load looking back into the amplifier's output terminals (with the input source set to zero/removed), determining how the output voltage sags under loading.

---

**Q17. [Unit II | Topic: CE Amplifier | Type: Theory | Difficulty: Basic]**

**Question:** State the typical phase relationship between input and output voltage in a CE amplifier.

*Concept from scratch:* A CE amplifier produces an output voltage that is **180° out of phase** (inverted) relative to the input voltage — an increasing input voltage causes an increasing base/collector current, which causes an *increasing* voltage drop across the collector resistor R_C, and hence a *decreasing* collector-emitter voltage V_CE (the output, in a typical CE amplifier configuration) — the output thus moves oppositely to the input.

---

**Q18. [Unit II | Topic: CC Amplifier | Type: Theory | Difficulty: Basic]**

**Question:** What is another common name for the common-collector configuration, and why? State its typical voltage gain (approximately).

*Concept from scratch:* The CC configuration is commonly called an **emitter follower**, because the output (taken at the emitter) closely "follows" the input (applied at the base) — it rises and falls together with the input, in phase, and at nearly the same amplitude.

**Typical voltage gain:** Approximately **unity (A_V ≈ 1, slightly less than 1)** — since V_out (emitter) ≈ V_in (base) − V_BE, and V_BE stays roughly constant, so any change in V_in appears almost fully at V_out.

---

### Section B: Computational Fluency

**Q19. [Unit II | Topic: BJT Current Relations | Type: Numerical | Difficulty: Intermediate]**

**Question:** A transistor has α = 0.98. Find the value of β and the ratio I_C/I_B.

*Step 1 — Recall the relation between α and β:*
β = α/(1−α)

*Step 2 — Substitute:*
β = 0.98/(1−0.98) = 0.98/0.02 = **49**

*Step 3 — Recognize I_C/I_B is, by definition, β itself:*
I_C/I_B = β = **49**

---

**Q20. [Unit II | Topic: BJT Current Relations | Type: Numerical | Difficulty: Intermediate]**

**Question:** A transistor has β = 100 and I_B = 20 µA. Find I_C and I_E (neglecting leakage current).

*Step 1 — Collector current:*
I_C = β × I_B = 100 × 20µA = **2000 µA = 2 mA**

*Step 2 — Emitter current (KCL: I_E = I_B + I_C):*
I_E = I_B + I_C = 20µA + 2000µA = **2020 µA = 2.02 mA**

---

**Q21. [Unit II | Topic: Fixed Bias Circuit | Type: Numerical | Difficulty: Intermediate]**

**Question:** In a fixed-bias circuit, V_CC = 12 V, R_B = 240 kΩ, R_C = 2 kΩ, and β = 100 (V_BE = 0.7 V). Find I_B, I_C, and V_CE.

*Step 1 — Write the KVL equation for the base-emitter loop (V_CC → R_B → base-emitter junction → ground):*
V_CC = I_BR_B + V_BE

*Step 2 — Solve for I_B:*
I_B = (V_CC − V_BE)/R_B = (12−0.7)/240,000 = 11.3/240,000 = **47.08 µA**

*Step 3 — Collector current:*
I_C = β × I_B = 100 × 47.08µA = **4.708 mA**

*Step 4 — Write the KVL equation for the collector-emitter loop (V_CC → R_C → collector-emitter → ground):*
V_CC = I_CR_C + V_CE

*Step 5 — Solve for V_CE:*
V_CE = V_CC − I_CR_C = 12 − (4.708mA × 2kΩ) = 12 − 9.416 = **2.584 V**

---

**Q22. [Unit II | Topic: Voltage Divider Bias | Type: Numerical | Difficulty: Intermediate]**

**Question:** In a voltage-divider bias circuit, V_CC = 20 V, R_1 = 39 kΩ, R_2 = 3.9 kΩ, R_C = 4 kΩ, R_E = 1.5 kΩ, β = 100 (V_BE = 0.7 V). Using the approximate analysis (assuming the base current is negligible compared to the divider current), find V_B, V_E, I_E, I_C, and V_CE.

*Step 1 — Base voltage using the voltage-divider formula (approximate method):*
V_B = V_CC × R_2/(R_1+R_2) = 20 × 3.9/(39+3.9) = 20 × 3.9/42.9 = 20 × 0.0909 = **1.818 V**

*Step 2 — Emitter voltage:*
V_E = V_B − V_BE = 1.818 − 0.7 = **1.118 V**

*Step 3 — Emitter current:*
I_E = V_E/R_E = 1.118/1500 = **0.7453 mA**

*Step 4 — Collector current (approximation: I_C ≈ I_E, since β is large, the base current is a small fraction):*
I_C ≈ I_E = **0.7453 mA**

*Step 5 — Collector-emitter voltage (KVL: V_CC = I_CR_C + V_CE + I_ER_E, approximating I_C≈I_E):*
V_CE = V_CC − I_C(R_C+R_E) = 20 − 0.7453mA×(4000+1500) = 20 − 0.7453mA×5500

Compute: 0.7453×5500 = 4099.15 (in mA×Ω = mV, so this is 4099.15mV = 4.099V)

V_CE = 20 − 4.099 = **15.90 V**

---

**Q23. [Unit II | Topic: h-parameter Analysis — CE Gain | Type: Numerical | Difficulty: Intermediate]**

**Question:** A CE amplifier has h_ie = 1.1 kΩ, h_fe = 100, h_oe = 25 µA/V, h_re (negligible), and is driving a load resistance R_L = 2 kΩ. Compute the current gain A_I = I_C/I_B and the voltage gain A_V.

*Step 1 — Current gain formula (standard h-parameter amplifier result):*
A_I = −h_fe / (1 + h_oeR_L)

*Step 2 — Compute the denominator:*
h_oeR_L = 25×10⁻⁶ × 2000 = 0.05

1 + h_oeR_L = 1.05

*Step 3 — Compute A_I:*
A_I = −100/1.05 = **−95.24**

*(The negative sign reflects the 180° phase inversion characteristic of the CE configuration; magnitude ≈95.24.)*

*Step 4 — Voltage gain formula (standard h-parameter result, with h_re neglected):*
A_V = A_I × R_L/h_ie

*Step 5 — Substitute:*
A_V = (−95.24) × 2000/1100 = −95.24 × 1.818 = **−173.2**

---

**Q24. [Unit II | Topic: h-parameter Analysis — Input Impedance | Type: Numerical | Difficulty: Intermediate]**

**Question:** For the amplifier of the previous question, compute the input impedance R_i seen at the base terminals.

*Step 1 — Recall the input impedance formula (with h_re neglected, this simplifies to just h_ie):*
R_i = h_ie + h_re × A_I × R_L ≈ h_ie (since h_re is given as negligible)

*Step 2 — Result:*
**R_i ≈ h_ie = 1.1 kΩ**

*(In the general case, with h_re non-negligible, the full formula R_i = h_ie − [h_re h_fe R_L/(1+h_oeR_L)] would be used, but since h_re is stated as negligible here, the correction term vanishes.)*

---

**Q25. [Unit II | Topic: h-parameter Analysis — CC Gain | Type: Numerical | Difficulty: Intermediate]**

**Question:** A common-collector (emitter-follower) amplifier has h_ic = 1.1 kΩ, h_fc = −101, h_oc = 25 µA/V, and a load resistance R_L = 1 kΩ. Compute the current gain A_I and voltage gain A_V, and comment on why the voltage gain is close to unity.

*Step 1 — Current gain formula:*
A_I = −h_fc/(1+h_ocR_L)

*Step 2 — Compute the denominator:*
h_ocR_L = 25×10⁻⁶ × 1000 = 0.025
1 + h_ocR_L = 1.025

*Step 3 — Compute A_I:*
A_I = −(−101)/1.025 = 101/1.025 = **98.54**

*(Positive, since the CC configuration is non-inverting.)*

*Step 4 — Voltage gain, using the correct relation A_V = A_I × R_L/R_i (not R_L/h_ic — the denominator must be the amplifier's actual input impedance R_i, not h_ic alone, since for the CC configuration these two are very different).*

*Step 4a — First find R_i (input impedance), using R_i = h_ic − (h_rc h_fc R_L)/(1+h_ocR_L). Taking the standard CC approximation h_rc ≈ 1:*
R_i = h_ic − [1×(−101)×1000]/1.025 = 1100 − (−98,537) = 1100+98,537 = **99,637 Ω ≈ 99.6 kΩ**

*Step 4b — Now compute the voltage gain using this correct R_i:*
A_V = A_I × R_L/R_i = 98.54 × 1000/99,637 = 98.54 × 0.01004 = **0.989**

*Result: A_V ≈ 0.989, confirming the expected near-unity gain.*

*Step 5 — Explanation of why voltage gain is close to unity (conceptual, regardless of the numeric subtlety above):* In the CC configuration, the output is taken across the emitter resistor, and the base-emitter junction maintains an essentially fixed voltage drop V_BE (~0.7V) between the input (base) and output (emitter) nodes. Since this offset is fixed and small compared to typical signal swings, the output voltage tracks the input voltage almost exactly (V_out ≈ V_in − V_BE(constant)), giving a voltage gain very close to (but always slightly less than) 1 — hence the name "emitter follower," or "voltage follower."

---

**Q26. [Unit II | Topic: DC Load Line | Type: Numerical | Difficulty: Intermediate]**

**Question:** For a CE amplifier with V_CC = 15 V, R_C = 3 kΩ, R_E = 1 kΩ, sketch the DC load line and determine its saturation current point and cut-off voltage point.

*Step 1 — Recall the DC load line equation (from KVL around the collector-emitter loop):*
V_CC = I_C(R_C+R_E) + V_CE

*Step 2 — Find the saturation point (set V_CE = 0, the load line's vertical-axis intercept):*
I_C(sat) = V_CC/(R_C+R_E) = 15/(3000+1000) = 15/4000 = **3.75 mA**

*Step 3 — Find the cut-off point (set I_C = 0, the load line's horizontal-axis intercept):*
V_CE(cutoff) = V_CC = **15 V** (when I_C=0, no drop occurs across R_C or R_E, so all of V_CC appears across V_CE)

*Result:* **The DC load line runs from (V_CE=0, I_C=3.75mA) at saturation to (V_CE=15V, I_C=0) at cut-off**, a straight line connecting these two points, on which the Q-point must lie for any given base bias current.

---

**Q27. [Unit II | Topic: Transistor as a Switch | Type: Numerical | Difficulty: Intermediate]**

**Question:** A BJT with β = 50 is used as a switch with R_C = 1 kΩ and V_CC = 5 V. Determine the minimum base current required to drive the transistor into saturation (assume V_CE(sat) ≈ 0 V).

*Step 1 — Find the saturation collector current (with V_CE(sat)≈0, KVL gives):*
I_C(sat) = V_CC/R_C = 5/1000 = **5 mA**

*Step 2 — Find the minimum base current needed to just reach this saturation current, using I_C=βI_B at the boundary:*
I_B(min) = I_C(sat)/β = 5mA/50 = **0.1 mA = 100 µA**

*Step 3 — Practical note:* In actual switching-circuit design, the base current is usually driven somewhat **higher** than this calculated minimum (called "overdrive") to ensure the transistor is driven solidly into saturation despite variations in β from device to device and with temperature — but 100 µA represents the theoretical minimum boundary value.

---

### Section C: Advanced Theory & Numericals

**Q28. [Unit II | Topic: CE Configuration — Characteristics | Type: Theory | Difficulty: Advanced]**

**Question:** Draw the common-emitter configuration of an NPN BJT and explain it with the help of input and output V-I characteristic curves, clearly identifying the active, saturation, cut-off, and breakdown regions on the output characteristics.

*Step 1 — Circuit configuration description:* In the CE configuration, the emitter terminal is grounded (common to both input and output loops). The input signal (and DC bias) is applied between base and emitter (through R_B or a divider network); the output is taken between collector and emitter, with R_C connecting the collector to V_CC.

*Step 2 — Input characteristics (I_B vs V_BE, for a fixed V_CE):* This curve resembles a standard forward-biased diode characteristic — I_B remains very small until V_BE approaches the cut-in voltage (~0.6–0.7V for Si), beyond which I_B rises steeply and nonlinearly with V_BE. Increasing V_CE (for a family of such curves) shifts the curve slightly to the right (due to the Early effect — base-width modulation reducing effective base recombination at higher V_CE), but this effect is typically small and often neglected in basic analysis.

*Step 3 — Output characteristics (I_C vs V_CE, family of curves for different fixed I_B values), described region by region:*

- **Cut-off region:** Occurs for I_B ≈ 0 (or slightly negative, accounting for leakage) — both junctions reverse-biased, I_C is very small (≈I_CEO), and the transistor behaves as an open switch. This corresponds to the bottom-most curve in the family, lying very close to the horizontal (V_CE) axis.

- **Saturation region:** The steep, near-vertical rising portion of each curve at low V_CE (roughly V_CE < 0.2–0.3V for silicon) — here, both the base-emitter and base-collector junctions are forward-biased. I_C rises very sharply with a tiny increase in V_CE and is **not** well-controlled by I_B in this region (multiple I_B curves converge/bunch together near the origin) — the transistor behaves as a closed switch, with a small residual V_CE(sat).

- **Active region:** The broad, nearly-horizontal, evenly-spaced portion of the curves at higher V_CE (beyond the saturation "knee") — here, I_C is almost independent of V_CE (ideally exactly independent, though real curves show a slight upward slope due to the Early effect) and is set almost entirely by I_C=βI_B — this is the linear operating region used for amplification, where the evenly-spaced curves (for equal I_B increments) reflect a constant β.

- **Breakdown region:** At very high V_CE (beyond the rated BV_CEO), the collector-base junction undergoes avalanche breakdown, causing I_C to rise sharply and uncontrollably — this region must always be avoided in normal operation, as it can permanently damage the device.

*Step 4 — Overall shape summary:* The full family of output characteristic curves resembles a "fan" — starting bunched together and rising steeply near the origin (saturation), then spreading apart into nearly horizontal, evenly-spaced lines (active region), before all curves eventually turn sharply upward together again at the high-V_CE breakdown boundary.

---

**Q29. [Unit II | Topic: h-parameter Derivation | Type: Theory | Difficulty: Advanced]**

**Question:** Starting from the two-port h-parameter equations for a transistor amplifier with a load resistance R_L, derive the general expressions for current gain A_I, input impedance R_i, voltage gain A_V, and output impedance R_o in terms of the h-parameters.

*Step 1 — Start from the two h-parameter equations:*
V_1 = h_iI_1 + h_rV_2  ... (i)
I_2 = h_fI_1 + h_oV_2  ... (ii)

*Step 2 — Introduce the load condition:* Since a load resistance R_L is connected at the output, the output current and voltage are related by: V_2 = −I_2R_L (negative sign because I_2, by the two-port sign convention, is defined as flowing *into* the output port, while the load current flows *out* of it).

*Step 3 — Derive current gain A_I = I_2/I_1.* Substitute V_2 = −I_2R_L into equation (ii):
I_2 = h_fI_1 + h_o(−I_2R_L)
I_2 + h_oR_LI_2 = h_fI_1
I_2(1 + h_oR_L) = h_fI_1

**A_I = I_2/I_1 = h_f/(1+h_oR_L)**

(Sign convention note: depending on whether I_2 is defined as flowing into or out of the port, textbooks may present this with a leading negative sign; the magnitude derivation is as shown.)

*Step 4 — Derive input impedance R_i = V_1/I_1.* Substitute V_2 = −I_2R_L into equation (i), and then substitute I_2 = A_I × I_1 from Step 3:
V_1 = h_iI_1 + h_r(−I_2R_L) = h_iI_1 − h_rR_L(A_II_1)
V_1 = I_1[h_i − h_rR_LA_I]

**R_i = V_1/I_1 = h_i − h_rh_fR_L/(1+h_oR_L)**

(substituting the expression for A_I found in Step 3)

*Step 5 — Derive voltage gain A_V = V_2/V_1.* Using V_2 = −I_2R_L = −A_II_1R_L, and V_1 = I_1R_i (from Step 4):
A_V = V_2/V_1 = (−A_II_1R_L)/(I_1R_i) = **−A_IR_L/R_i**

*Step 6 — Derive output admittance/impedance.* To find R_o, set the input source to zero (V_source=0, meaning the input is driven by a source with zero internal signal but retains its source resistance R_s in series, i.e., 0 = I_1R_s + V_1, or for the simplest case with ideal voltage source removed, V_1 relates to I_1 via the source's internal resistance). Using equation (i) with V_1 = −I_1R_s (if a source resistance R_s is assumed) or V_1=0 (if the source is an ideal short, i.e., R_s=0, a common simplifying assumption):

Taking the simplified case R_s=0 (ideal voltage source driving the input, so V_1=0 when its own signal is zero): from (i), 0 = h_iI_1 + h_rV_2 ⟹ I_1 = −h_rV_2/h_i

Substitute into (ii):
I_2 = h_f(−h_rV_2/h_i) + h_oV_2 = V_2[h_o − h_fh_r/h_i]

Output admittance Y_o = I_2/V_2 = h_o − (h_fh_r/h_i)

**R_o = 1/Y_o = 1/[h_o − (h_fh_r/h_i)]**

*Step 7 — Summary of the four derived general h-parameter amplifier formulas:*
- **A_I = h_f/(1+h_oR_L)**
- **R_i = h_i − h_rh_fR_L/(1+h_oR_L)**
- **A_V = −A_IR_L/R_i**
- **R_o = 1/[h_o − h_fh_r/h_i]** (for ideal/zero source resistance; a more general formula includes R_s explicitly)

---

**Q30. [Unit II | Topic: Voltage Divider Bias — Stability Analysis | Type: Numerical | Difficulty: Advanced]**

**Question:** For a voltage-divider bias circuit with V_CC = 20 V, R_1 = 39 kΩ, R_2 = 3.9 kΩ, R_C = 4 kΩ, R_E = 1.5 kΩ, β = 100, find the exact (Thevenin-equivalent) values of I_B, I_C, and V_CE without using the approximation that base current is negligible, and compare the result with the approximate method.

*Step 1 — Find the Thevenin equivalent of the base bias network (R_1, R_2, V_CC), as seen from the base terminal:*

Thevenin voltage: V_TH = V_CC × R_2/(R_1+R_2) = 20 × 3.9/42.9 = **1.818 V** (same as the "approximate" V_B computed in Q22, since this is exactly the open-circuit voltage-divider voltage)

Thevenin resistance: R_TH = (R_1×R_2)/(R_1+R_2) = (39,000×3,900)/42,900 = 152,100,000/42,900 = **3545.5 Ω**

*Step 2 — Write the exact KVL equation for the base loop, now including R_TH explicitly (this is the correction the "approximate method" ignores):*
V_TH = I_BR_TH + V_BE + I_ER_E

*Step 3 — Express I_E in terms of I_B (using I_E = (β+1)I_B, the exact relation from I_E=I_B+I_C=I_B+βI_B):*
V_TH = I_BR_TH + V_BE + I_B(β+1)R_E

*Step 4 — Substitute known values and solve for I_B:*
1.818 = I_B(3545.5) + 0.7 + I_B(101)(1500)
1.818 = I_B(3545.5) + 0.7 + I_B(151,500)
1.818 − 0.7 = I_B(3545.5 + 151,500)
1.118 = I_B(155,045.5)
I_B = 1.118/155,045.5 = **7.211×10⁻⁶ A = 7.211 µA**

*Step 5 — Collector current:*
I_C = β × I_B = 100 × 7.211µA = **0.7211 mA**

*Step 6 — Collector-emitter voltage (using the exact I_E = (β+1)I_B):*
I_E = 101 × 7.211µA = 0.7283 mA

V_CE = V_CC − I_CR_C − I_ER_E = 20 − (0.7211mA×4000) − (0.7283mA×1500)
= 20 − 2.884 − 1.092
= **16.02 V**

*Step 7 — Comparison with the approximate method (from Q22):*

| Quantity | Approximate method (Q22) | Exact (Thevenin) method |
|---|---|---|
| I_C | 0.7453 mA | 0.7211 mA |
| V_CE | 15.90 V | 16.02 V |

*Step 8 — Interpretation:* The two methods agree closely (within about 3% for I_C) because the divider current (through R_1, R_2) is indeed much larger than the base current in this design (a hallmark of a well-designed voltage-divider bias circuit) — confirming that the approximate method is a valid and reasonably accurate shortcut here, though the exact Thevenin method remains the rigorous, always-valid approach, especially important to use when the divider resistors are not small enough relative to βR_E to justify the approximation.

---

**Q31. [Unit II | Topic: CE and CC Gain Comparison | Type: Numerical | Difficulty: Advanced]**

**Question:** For a transistor with h_ie = 1 kΩ, h_fe = 120, h_oe = 20 µA/V (h_re negligible), operating with R_L = 2.2 kΩ, compute the voltage gain, current gain, input impedance, and output impedance in both the CE and CC configurations, and tabulate the comparison, explaining the key application-relevant differences.

**Part (a): CE configuration**

*Step 1 — Current gain:*
A_I(CE) = −h_fe/(1+h_oeR_L) = −120/(1+20×10⁻⁶×2200) = −120/(1+0.044) = −120/1.044 = **−114.9**

*Step 2 — Input impedance (h_re negligible, so R_i ≈ h_ie):*
R_i(CE) ≈ **1 kΩ**

*Step 3 — Voltage gain:*
A_V(CE) = A_I × R_L/R_i = (−114.9) × 2200/1000 = −114.9×2.2 = **−252.8**

*Step 4 — Output impedance (h_re negligible ⟹ R_o ≈ 1/h_oe):*
R_o(CE) = 1/h_oe = 1/(20×10⁻⁶) = **50 kΩ**

**Part (b): CC configuration**

*Step 5 — For CC, the relevant h-parameters relate to CE parameters as: h_ic ≈ h_ie, h_fc ≈ −(1+h_fe), h_oc ≈ h_oe (standard conversion relations, since CB/CE/CC h-parameters are all derivable from one another):*
h_ic = 1 kΩ, h_fc = −(1+120) = −121, h_oc = 20 µA/V

*Step 6 — Current gain:*
A_I(CC) = −h_fc/(1+h_ocR_L) = −(−121)/(1+0.044) = 121/1.044 = **115.9**

*Step 7 — Input impedance:*
R_i(CC) = h_ic − (h_rc·h_fc·R_L)/(1+h_ocR_L)

For CC, h_rc ≈ 1 (standard approximation, since the collector voltage change is nearly fully "reflected" to the base-collector loop) — using this:
R_i(CC) = 1000 − [1×(−121)×2200]/1.044 = 1000 − (−266,200)/1.044 = 1000 + 254,981 = **255,981 Ω ≈ 256 kΩ**

*(This much larger input impedance compared to CE is the hallmark, defining advantage of the emitter-follower/CC configuration.)*

*Step 8 — Voltage gain:*
A_V(CC) = A_I(CC) × R_L/R_i(CC) = 115.9 × 2200/255,981 = 115.9 × 0.00859 = **0.996**

*(Confirms the expected near-unity voltage gain for CC, consistent with the qualitative discussion in Q25.)*

*Step 9 — Output impedance:*
R_o(CC) ≈ 1/h_oc (approximately, using the simplified relation, ignoring the small correction from finite source resistance) = 1/(20×10⁻⁶) = **50 kΩ** (as a first approximation before considering source resistance effects — in practice, CC output impedance is usually much lower than this when a finite source resistance is included in the full formula, since CC characteristically presents very low output impedance; the simplified h_oc-only formula used here is the same structural form as the CE case for consistency, but a fuller treatment including source resistance would show CC's output impedance is typically only tens of ohms in a practical circuit)

**Comparison table:**

| Parameter | CE | CC |
|---|---|---|
| Current gain (A_I) | −114.9 | +115.9 |
| Voltage gain (A_V) | −252.8 (high gain, inverting) | +0.996 (≈unity, non-inverting) |
| Input impedance (R_i) | ≈1 kΩ (low) | ≈256 kΩ (very high) |
| Output impedance (R_o) | ≈50 kΩ (high, simplified estimate) | Characteristically low in practice |

**Application-relevant differences:** The **CE** configuration is preferred where **high voltage/power gain** is the priority (general-purpose voltage amplification stages), at the cost of moderate input impedance and signal inversion. The **CC (emitter-follower)** configuration is preferred as a **buffer/impedance-matching stage** — its very high input impedance avoids loading down a high-impedance signal source, while its low output impedance allows it to drive low-impedance loads effectively, all while providing (near) unity voltage gain and no phase inversion.

---

**Q32. [Unit II | Topic: Biasing Stability Factor Derivation | Type: Theory | Difficulty: Advanced]**

**Question:** Derive the expression for the stability factor S = ∂I_C/∂I_CO for a fixed-bias circuit, and show mathematically why voltage-divider bias yields a lower (better) stability factor than fixed bias.

*Step 1 — Start from the general relation between I_C, I_B, and I_CO (accounting for leakage current explicitly):*
I_C = βI_B + (β+1)I_CO

*Step 2 — For a fixed-bias circuit, write the base-loop KVL equation (I_B is set by V_CC, R_B, V_BE only — notably, it does NOT depend on I_CO at all in the fixed-bias configuration, since there's no feedback path from collector/emitter back to the base bias network):*
V_CC = I_BR_B + V_BE ⟹ I_B = (V_CC−V_BE)/R_B = constant, independent of I_CO

*Step 3 — Differentiate the I_C expression (Step 1) with respect to I_CO, treating I_B as constant (per Step 2, since I_B doesn't depend on I_CO in fixed bias):*
∂I_C/∂I_CO = β(∂I_B/∂I_CO) + (β+1)(∂I_CO/∂I_CO) = β(0) + (β+1)(1) = **(β+1)**

*Step 4 — Result for fixed bias:* **S(fixed bias) = β+1**

Since β is typically large (50–200), this stability factor is correspondingly large — meaning I_C is highly sensitive to changes in I_CO, a poor (undesirable) result.

*Step 5 — Now consider voltage-divider bias. Here, I_B is NOT independent of I_CO, because of the R_E feedback path — as I_C (and hence I_E) changes due to I_CO, the voltage drop across R_E changes, which changes V_BE, which changes I_B. So we must differentiate more carefully, starting from the full KVL loop (from Q30's setup, generalized with Thevenin R_TH):*

V_TH = I_BR_TH + V_BE + I_ER_E, and I_E = I_B + I_C (exact KCL)

Rearranging: I_B = (V_TH − V_BE − I_ER_E)/R_TH = (V_TH−V_BE)/R_TH − (I_ER_E)/R_TH

*Step 6 — Differentiate this I_B expression with respect to I_CO, now allowing I_E (and hence I_C) to vary with I_CO:*
∂I_B/∂I_CO = −(R_E/R_TH)(∂I_E/∂I_CO) = −(R_E/R_TH)(∂I_C/∂I_CO + ∂I_B/∂I_CO)  [since I_E=I_B+I_C]

Let S = ∂I_C/∂I_CO (the quantity we want) and let ∂I_B/∂I_CO = x (unknown, to be found):
x = −(R_E/R_TH)(S + x)
x = −(R_E/R_TH)S − (R_E/R_TH)x
x + (R_E/R_TH)x = −(R_E/R_TH)S
x[1 + R_E/R_TH] = −(R_E/R_TH)S
x = −S × (R_E/R_TH) / [1+R_E/R_TH] = −S × R_E/(R_TH+R_E)

*Step 7 — Now differentiate the original I_C relation (Step 1) with respect to I_CO, using this x = ∂I_B/∂I_CO:*
S = ∂I_C/∂I_CO = βx + (β+1)
S = β[−S×R_E/(R_TH+R_E)] + (β+1)
S = −Sβ×R_E/(R_TH+R_E) + (β+1)
S + Sβ×R_E/(R_TH+R_E) = (β+1)
S[1 + βR_E/(R_TH+R_E)] = (β+1)

**S(voltage-divider) = (β+1) / [1 + βR_E/(R_TH+R_E)]**

*Step 8 — Compare this to fixed bias (S=β+1):* Since the denominator term [1 + βR_E/(R_TH+R_E)] is always **greater than 1** (as long as R_E > 0), the voltage-divider stability factor is always **smaller** than (β+1) — confirming mathematically that voltage-divider bias always gives better (lower) stability than fixed bias. Moreover, as R_TH is made smaller relative to R_E (i.e., a "stiffer," lower-resistance divider — achieved by using smaller R_1, R_2 values, at the cost of drawing more quiescent divider current from the supply), the denominator term grows larger, pushing S closer to its theoretical best-case minimum value of 1 — this is the mathematical basis for the well-known design guideline that a "stiff" (low R_TH) voltage divider gives the best bias stability.


## Detailed Step-Wise Solutions — UNIT III: JFET, MOSFET & Switching Theory

---

### Section A: Definitions & Concept Questions

**Q1. [Unit III | Topic: JFET Construction | Type: Theory | Difficulty: Basic]**

**Question:** Describe the basic construction of an n-channel JFET, naming its three terminals.

*Concept from scratch:* An n-channel JFET consists of a bar of **n-type** semiconductor material (forming the conducting "channel"), with two regions of heavily-doped **p-type** material diffused into opposite sides of this bar, forming two p-n junctions. These two p-regions are internally connected together and brought out as a single terminal.

**Three terminals:** **Source (S)** — where majority carriers (electrons, for n-channel) enter the channel; **Drain (D)** — where majority carriers exit the channel; **Gate (G)** — the (internally connected) p-type region(s), used to control the channel via the reverse-biased gate-channel junction.

---

**Q2. [Unit III | Topic: JFET Action | Type: Theory | Difficulty: Basic]**

**Question:** Briefly explain how the drain current in a JFET is controlled by the gate-source voltage.

*Concept from scratch:* The gate-source junction of a JFET is normally operated **reverse-biased**. As the magnitude of this reverse bias (V_GS, negative for n-channel) is increased, the depletion regions around the gate-channel junctions **widen**, encroaching further into the n-type channel from both sides. Since the depletion region contains no free carriers, this effectively **narrows the conducting channel width**, increasing its resistance and hence **reducing** the drain current (I_D) that can flow for a given V_DS. As V_GS is made more negative, the channel narrows further, until at the pinch-off voltage the channel is fully constricted and I_D drops to a very small value — thus, drain current is controlled purely by an applied **voltage** (V_GS) acting through this depletion-width-modulation mechanism, drawing essentially zero DC gate current.

---

**Q3. [Unit III | Topic: Pinch-Off | Type: Theory | Difficulty: Basic]**

**Question:** Define the pinch-off voltage of a JFET.

*Concept from scratch:* The **pinch-off voltage (V_P)** is the value of the drain-source voltage V_DS (at V_GS=0) at which the depletion regions from the two sides of the channel just meet at the drain end, causing the channel to become fully constricted ("pinched off") at that point. Beyond this V_DS, the drain current I_D levels off and remains nearly constant (saturates) despite further increases in V_DS — this same voltage magnitude, when referenced instead as a gate-source voltage (at V_DS large enough to be in saturation), is also the value of V_GS at which the channel is fully pinched off throughout its length and I_D drops to (near) zero.

---

**Q4. [Unit III | Topic: JFET Characteristics | Type: Theory | Difficulty: Basic]**

**Question:** Sketch the general shape of the JFET drain (output) characteristics, identifying the ohmic and saturation (pinch-off) regions.

*Concept from scratch (description of the curve family, since this is a sketch-based question):* The drain characteristics plot I_D (vertical axis) against V_DS (horizontal axis), for a family of curves at different fixed V_GS values.

- **Ohmic (linear/triode) region:** At low V_DS (near the origin), I_D rises almost linearly with V_DS — the channel behaves approximately like a simple (V_GS-dependent) resistor in this region.
- **Saturation (pinch-off/active) region:** Beyond a certain V_DS (the pinch-off point for that particular V_GS), I_D levels off and becomes nearly constant (flat, horizontal curve), essentially independent of further increases in V_DS — this is the region used for amplifier applications, where I_D is controlled almost purely by V_GS.
- Each successive curve (for progressively more negative V_GS, n-channel) sits **lower** in the family, since increasing reverse bias narrows the channel and reduces the saturation current level.
- **Breakdown region:** At sufficiently high V_DS, the gate-drain junction breaks down (avalanche), and I_D rises sharply — this must be avoided in normal operation.

---

**Q5. [Unit III | Topic: JFET Parameters | Type: Theory | Difficulty: Basic]**

**Question:** Define transconductance (g_m) of a JFET. State its typical unit.

*Concept from scratch:* **Transconductance (g_m)** measures how effectively a change in gate-source voltage produces a change in drain current, at a constant V_DS: **g_m = ∂I_D/∂V_GS** (evaluated at a fixed V_DS, typically in the saturation region).

**Unit:** siemens (S), or equivalently mho — commonly expressed in **mA/V** for practical device values (numerically equivalent to mS).

---

**Q6. [Unit III | Topic: JFET Biasing | Type: Theory | Difficulty: Basic]**

**Question:** Name two common methods of biasing a JFET.

*Concept from scratch:*

1. **Fixed bias** (using a separate negative gate supply, for n-channel)

2. **Self-bias** (using a source resistor R_S, with the gate returned to ground through a large gate resistor R_G, relying on the voltage drop across R_S to provide the necessary reverse gate-source bias without a separate supply)

(Also acceptable: voltage-divider bias, similar in principle to BJT voltage-divider bias.)

---

**Q7. [Unit III | Topic: MOSFET Types | Type: Theory | Difficulty: Basic]**

**Question:** Name the two basic types of MOSFET based on construction/operation mode.

*Concept from scratch:*

1. **Depletion-type (D-MOSFET)** — has a physically-built conducting channel present even at V_GS=0; can be operated in both depletion mode (V_GS reducing channel conductivity) and enhancement mode (V_GS increasing it).

2. **Enhancement-type (E-MOSFET)** — has **no** conducting channel at V_GS=0 (normally off); a channel must be actively "induced" (created) by applying a sufficiently large V_GS beyond the threshold voltage.

---

**Q8. [Unit III | Topic: MOSFET Construction | Type: Theory | Difficulty: Basic]**

**Question:** Describe the basic construction of an enhancement-type MOSFET, naming its four terminals.

*Concept from scratch:* An enhancement MOSFET is built on a lightly-doped semiconductor **substrate** (body) of one type (say p-type, for an n-channel E-MOSFET), into which two heavily-doped regions of the opposite type (n-type) are diffused, forming the **source** and **drain** regions, initially unconnected by any conducting channel. A thin layer of insulating **silicon dioxide (SiO₂)** is grown over the region between source and drain, and a conductive **gate** electrode (metal or polysilicon) is deposited on top of this oxide layer — the gate is thus completely electrically **insulated** from the channel/body by the oxide.

**Four terminals:** **Source (S)**, **Drain (D)**, **Gate (G)**, **Body/Substrate (B)** (often internally connected to the source in discrete devices).

---

**Q9. [Unit III | Topic: MOSFET vs JFET | Type: Theory | Difficulty: Basic]**

**Question:** State one key structural difference between a MOSFET and a JFET (relating to the gate).

*Concept from scratch:* In a **JFET**, the gate forms a **p-n junction** with the channel (a reverse-biased diode junction, through which a very small leakage current can still flow). In a **MOSFET**, the gate is **electrically insulated** from the channel by a thin layer of silicon dioxide (an insulator, not a junction) — this gives the MOSFET an even higher input impedance than the JFET, since essentially **no** current (not even junction leakage current) flows into the gate under normal DC bias conditions.

---

**Q10. [Unit III | Topic: Depletion vs Enhancement MOSFET | Type: Theory | Difficulty: Basic]**

**Question:** Differentiate between depletion-type and enhancement-type MOSFETs in terms of channel existence at V_GS = 0.

*Concept from scratch:*
- **Depletion-type MOSFET:** A physical conducting channel **already exists** between source and drain at V_GS=0 (built in during manufacture) — the device conducts significant I_D even with no gate bias applied ("normally on").
- **Enhancement-type MOSFET:** **No** conducting channel exists at V_GS=0 — the device conducts essentially zero I_D until V_GS exceeds a threshold voltage V_T, at which point a channel is induced ("normally off").

---

**Q11. [Unit III | Topic: MOSFET as Switch | Type: Theory | Difficulty: Basic]**

**Question:** Explain briefly how a MOSFET can be used as an electronic switch, referring to its cut-off and ohmic (triode) regions.

*Concept from scratch:* When used as a switch, a MOSFET is driven between only its two extreme operating states, rather than the linear (saturation) region used for amplification:
- **"OFF" state (cut-off region):** V_GS is kept below the threshold voltage V_T, so no channel exists (or the existing channel is fully depleted) — the MOSFET presents a very high resistance (essentially open circuit) between drain and source, blocking current flow.
- **"ON" state (ohmic/triode region):** V_GS is driven well above V_T (with V_DS kept small), so a low-resistance channel is fully established — the MOSFET behaves like a small resistance (closed switch), allowing current to flow with only a small voltage drop (V_DS(on)) across it.

By rapidly switching V_GS between these two extremes, the MOSFET acts as a fast, efficient electronic switch — this mode of operation (avoiding the intermediate saturation/active region except briefly during transitions) minimizes power dissipation in the device, a key principle used in digital logic circuits and switching power converters.

---

**Q12. [Unit III | Topic: Number Systems | Type: Theory | Difficulty: Basic]**

**Question:** Name four common number systems used in digital electronics, along with their bases.

*Concept from scratch:*

1. **Binary** — base 2 (digits 0, 1)

2. **Octal** — base 8 (digits 0–7)

3. **Decimal** — base 10 (digits 0–9)

4. **Hexadecimal** — base 16 (digits 0–9, A–F)

---

**Q13. [Unit III | Topic: Boolean Algebra | Type: Theory | Difficulty: Basic]**

**Question:** State the commutative, associative, and distributive laws of Boolean algebra.

*Concept from scratch:*
- **Commutative law:** A + B = B + A, and A·B = B·A (order of operands doesn't matter)
- **Associative law:** (A+B)+C = A+(B+C), and (A·B)·C = A·(B·C) (grouping doesn't matter)
- **Distributive law:** A·(B+C) = A·B + A·C, and A+(B·C) = (A+B)·(A+C) (the second form is the Boolean-specific "dual" distributive law, which has no analog in ordinary algebra)

---

**Q14. [Unit III | Topic: Boolean Algebra — De Morgan's Theorem | Type: Theory | Difficulty: Basic]**

**Question:** State De Morgan's theorems.

*Concept from scratch:*

1. **(A+B)' = A'·B'** — the complement of a sum equals the product of the complements.

2. **(A·B)' = A'+B'** — the complement of a product equals the sum of the complements.

(In words: "breaking" a NOT across an OR/AND flips it to an AND/OR, and complements each individual term.)

---

**Q15. [Unit III | Topic: Logic Gates | Type: Theory | Difficulty: Basic]**

**Question:** Define the AND, OR, and NOT logic gates, giving their truth tables.

*Concept from scratch:*
- **AND gate:** Output is 1 only if **all** inputs are 1. Truth table (2-input): (0,0)→0, (0,1)→0, (1,0)→0, (1,1)→1.
- **OR gate:** Output is 1 if **at least one** input is 1. Truth table (2-input): (0,0)→0, (0,1)→1, (1,0)→1, (1,1)→1.
- **NOT gate (inverter):** Output is the complement of the single input. Truth table: 0→1, 1→0.

---

**Q16. [Unit III | Topic: Universal Gates | Type: Theory | Difficulty: Basic]**

**Question:** Which are the universal logic gates? Why are they called "universal"?

*Concept from scratch:* The **NAND** gate and the **NOR** gate are the universal gates.

**Why "universal":** Any Boolean function, and hence any of the basic gates (AND, OR, NOT) themselves, can be realized using **only** NAND gates (or, separately, using only NOR gates), without needing any other gate type — this makes them "universal building blocks" sufficient to construct any digital logic circuit.

---

**Q17. [Unit III | Topic: Canonical Forms | Type: Theory | Difficulty: Basic]**

**Question:** Define the Sum-of-Products (SOP) and Product-of-Sums (POS) canonical forms of a Boolean expression.

*Concept from scratch:*
- **Sum-of-Products (SOP):** A Boolean expression written as an **OR (sum) of AND (product) terms**, where each product term is a minterm (a product involving every variable of the function, either in true or complemented form) — e.g., F = A'BC + AB'C + ABC'.
- **Product-of-Sums (POS):** A Boolean expression written as an **AND (product) of OR (sum) terms**, where each sum term is a maxterm (a sum involving every variable, either true or complemented) — e.g., F = (A+B+C)(A+B'+C)(A'+B+C).

---

**Q18. [Unit III | Topic: K-Map | Type: Theory | Difficulty: Basic]**

**Question:** What is a Karnaugh map (K-map)? State its purpose in digital logic design.

*Concept from scratch:* A **Karnaugh map (K-map)** is a graphical tool — a grid of cells arranged so that adjacent cells differ by only one variable value (a property called adjacency, following a Gray-code-like ordering) — used to represent a Boolean function's truth table visually, with each cell corresponding to one minterm.

**Purpose:** It provides a fast, visual, systematic method for **simplifying (minimizing) Boolean expressions**, by allowing the designer to identify and group adjacent 1s (or 0s) into the largest possible power-of-2-sized rectangular groups, each group directly yielding a simplified product (or sum) term — avoiding the more tedious algebraic manipulation needed with Boolean algebra laws alone.

---

### Section B: Computational Fluency

**Q19. [Unit III | Topic: JFET Biasing | Type: Numerical | Difficulty: Intermediate]**

**Question:** A JFET has I_DSS = 10 mA and V_P = −4 V. Using the Shockley equation, find the drain current I_D at V_GS = −2 V.

*Step 1 — Recall the Shockley equation:*
I_D = I_DSS × [1 − (V_GS/V_P)]²

*Step 2 — Substitute values:*
I_D = 10mA × [1 − (−2/−4)]²

*Step 3 — Compute the ratio inside the brackets:*
V_GS/V_P = (−2)/(−4) = 0.5

*Step 4 — Compute [1−0.5]² = [0.5]² = 0.25*

*Step 5 — Final calculation:*
I_D = 10mA × 0.25 = **2.5 mA**

---

**Q20. [Unit III | Topic: JFET Transconductance | Type: Numerical | Difficulty: Intermediate]**

**Question:** For the JFET of the previous question, find the transconductance g_m at V_GS = −2 V, given g_m0 (at V_GS=0) = 5 mA/V.

*Step 1 — Recall the transconductance formula (derived by differentiating the Shockley equation):*
g_m = g_m0 × [1 − (V_GS/V_P)]

*Step 2 — Substitute values (using V_GS/V_P = 0.5, from the previous question):*
g_m = 5mA/V × [1 − 0.5] = 5mA/V × 0.5 = **2.5 mA/V**

---

**Q21. [Unit III | Topic: Number System Conversion | Type: Numerical | Difficulty: Intermediate]**

**Question:** Convert the following: (i) (110010110)₂ = ( )₁₆  (ii) (B2D)₁₆ = ( )₈  (iii) (21.25)₁₀ = ( )₂

**(i) Binary to Hexadecimal:**

*Step 1 — Group the binary digits into sets of 4, starting from the right (pad the leftmost group with leading zeros if needed):*
110010110 → grouping from the right: 0001 1001 0110

*Step 2 — Convert each 4-bit group to its hex digit:*
0001 = 1
1001 = 9
0110 = 6

**Result: (110010110)₂ = (196)₁₆**

**(ii) Hexadecimal to Octal (convert via binary as an intermediate step):**

*Step 1 — Convert each hex digit to its 4-bit binary equivalent:*
B = 1011
2 = 0010
D = 1101

So (B2D)₁₆ = (101100101101)₂

*Step 2 — Regroup this binary string into sets of 3 (for octal), starting from the right:*
101100101101 → grouping from the right: 101 100 101 101

*Step 3 — Convert each 3-bit group to its octal digit:*
101 = 5
100 = 4
101 = 5
101 = 5

**Result: (B2D)₁₆ = (5455)₈**

**(iii) Decimal to Binary (with fractional part):**

*Step 1 — Convert the integer part (21) using repeated division by 2:*
21÷2 = 10 remainder 1
10÷2 = 5 remainder 0
5÷2 = 2 remainder 1
2÷2 = 1 remainder 0
1÷2 = 0 remainder 1

Reading remainders bottom-to-top: **10101**

*Step 2 — Convert the fractional part (0.25) using repeated multiplication by 2:*
0.25×2 = 0.50 → integer part 0
0.50×2 = 1.00 → integer part 1 (and the fraction is now exactly 0, so we stop)

Reading integer parts top-to-bottom: **.01**

**Result: (21.25)₁₀ = (10101.01)₂**

---

**Q22. [Unit III | Topic: r's Complement Subtraction | Type: Numerical | Difficulty: Intermediate]**

**Question:** Subtract the following using r's complement method: (i) (76548)₁₀ − (96541)₁₀  (ii) (11010011)₂ − (10110011)₂

**(i) Decimal subtraction using 10's complement:**

*Step 1 — Since the subtrahend (96541) is larger than the minuend (76548), we expect a negative result. Find the 10's complement of the subtrahend (96541), for a 5-digit number:*

9's complement of 96541 = (9−9)(9−6)(9−5)(9−4)(9−1) = 03458
10's complement = 9's complement + 1 = 03458+1 = 03459

*Step 2 — Add this 10's complement to the minuend:*
76548 + 03459 = 80007

*Step 3 — Check for a carry out of the leftmost (5th) digit.* Since both numbers are 5-digit and their sum (80007) is still only 5 digits (no carry generated beyond the 5th digit), this indicates the **result is negative**.

*Step 4 — Since there's no carry, take the 10's complement of the result (80007) to find the actual magnitude, and attach a negative sign:*
9's complement of 80007 = (9−8)(9−0)(9−0)(9−0)(9−7) = 19992
10's complement = 19992+1 = 19993

**Result: (76548)₁₀ − (96541)₁₀ = −19993**

*(Quick verification: 96541−76548 = 19993 ✓, confirming the magnitude is correct.)*

**(ii) Binary subtraction using 2's complement:**

*Step 1 — Find the 2's complement of the subtrahend (10110011):*

1's complement of 10110011 = 01001100
2's complement = 1's complement + 1 = 01001100+1 = 01001101

*Step 2 — Add this 2's complement to the minuend (11010011), bit by bit from the right, tracking carries:*

Position 1 (rightmost): 1+1 = 10 → write 0, carry 1
Position 2: 1+0+1(carry) = 10 → write 0, carry 1
Position 3: 0+1+1(carry) = 10 → write 0, carry 1
Position 4: 0+1+1(carry) = 10 → write 0, carry 1
Position 5: 1+0+1(carry) = 10 → write 0, carry 1
Position 6: 0+0+1(carry) = 1 → write 1, carry 0
Position 7: 1+1+0 = 10 → write 0, carry 1
Position 8 (leftmost): 1+0+1(carry) = 10 → write 0, carry 1

*Step 3 — Assemble the result bits (positions 8 down to 1): 0,0,1,0,0,0,0,0 → **00100000**, with a final carry-out of 1 beyond the 8th bit.*

*Step 4 — Since there is a carry-out, the result is positive, and the carry is discarded (standard 2's complement subtraction rule), keeping the 8-bit result:*

**Result: (11010011)₂ − (10110011)₂ = (00100000)₂**

*Step 5 — Verify in decimal:* 11010011₂ = 128+64+16+2+1 = 211. 10110011₂ = 128+32+16+2+1 = 179. 211−179 = 32. And 00100000₂ = 32. ✓ **Matches.**

---

**Q23. [Unit III | Topic: Boolean Simplification | Type: Numerical | Difficulty: Intermediate]**

**Question:** Simplify the Boolean expression F = A'B'C + A'BC + AB'C + ABC using Boolean algebra laws.

*Step 1 — Group terms to factor out common factors. Group the first two terms (both have A'C common) and the last two terms (both have AC common):*
F = A'C(B'+B) + AC(B'+B)

*Step 2 — Apply the complement law (B'+B = 1) to both groups:*
F = A'C(1) + AC(1) = A'C + AC

*Step 3 — Factor out the common C:*
F = C(A'+A)

*Step 4 — Apply the complement law again (A'+A=1):*
F = C(1) = **C**

*Result:* **F = C** — the entire 4-term expression simplifies down to the single variable C (makes sense: the expression includes all four combinations of A and B alongside C, meaning F=1 whenever C=1, regardless of A and B).

---

**Q24. [Unit III | Topic: K-Map Minimization | Type: Numerical | Difficulty: Intermediate]**

**Question:** Minimize the expression f(A,B,C) = Σm(1,3,5,6,7) using a K-map, and write the simplified SOP expression.

*Step 1 — List the minterms with their binary (ABC) representations:*
m1 = 001, m3 = 011, m5 = 101, m6 = 110, m7 = 111

*Step 2 — Set up a 3-variable K-map (rows for A, columns for BC in Gray-code order: 00,01,11,10) and place 1s at the given minterm positions:*

| A\\BC | 00 | 01 | 11 | 10 |
|---|---|---|---|---|
| 0 | 0 (m0) | 1 (m1) | 1 (m3) | 0 (m2) |
| 1 | 0 (m4) | 1 (m5) | 1 (m7) | 1 (m6) |

*Step 3 — Identify groups of adjacent 1s (in powers of 2: groups of 4, then 2, then isolated 1s).*

**Group 1 (quad, size 4):** Cells m1, m3, m5, m7 (column BC=01 and BC=11, across both rows A=0 and A=1) — check adjacency: BC=01 and BC=11 are adjacent (differ only in B), and both rows of A are included. This group covers m1(001), m3(011), m5(101), m7(111) — in this group, A varies (0 and 1) and B varies (0 and 1, since BC=01 has B=0,C=1 and BC=11 has B=1,C=1) — the only variable that stays constant across all four cells is **C=1**. This group simplifies to **C**.

**Group 2 (pair, size 2):** Cells m6(110) and m7(111) — both in row A=1, columns BC=10 and BC=11 (adjacent). In this pair, A=1 (constant) and B=1 (constant), while C varies (0 and 1) — this group simplifies to **AB**.

*Step 4 — Check that all 1s are covered:* m1,m3,m5,m7 covered by Group 1 (C); m6 covered by Group 2 (AB); m7 also covered by Group 2, but it's already covered by Group 1 too — that's fine (overlapping groups are allowed and often necessary in K-map grouping).

*Step 5 — Combine the groups (OR them together) for the final simplified SOP expression:*

**f(A,B,C) = C + AB**

---

**Q25. [Unit III | Topic: Universal Gate Realization | Type: Numerical | Difficulty: Intermediate]**

**Question:** Design a 2-input AND gate using only NAND gates.

*Step 1 — Recall that a NAND gate followed immediately by another NAND gate used as an inverter (both inputs tied together) recovers the AND function, since NAND = NOT(AND), so NOT(NAND) = AND.*

*Step 2 — Stage 1:* Feed the two inputs A and B into a single 2-input NAND gate: Output₁ = (AB)' (i.e., NOT(AB)).

*Step 3 — Stage 2:* Feed Output₁ into a second NAND gate, with **both inputs of this second NAND gate tied together** to Output₁ (this configuration makes a 2-input NAND behave exactly as a NOT gate/inverter, since NAND(X,X) = NOT(X·X) = NOT(X)):
Output₂ = NOT(Output₁) = NOT(NOT(AB)) = **AB**

**Result:** Two NAND gates in cascade — the first a plain 2-input NAND(A,B), the second a NAND used as an inverter (both its inputs tied to the first NAND's output) — realize the function **F = AB**, i.e., a 2-input AND gate.

---

**Q26. [Unit III | Topic: Universal Gate Realization | Type: Numerical | Difficulty: Intermediate]**

**Question:** Design a 2-input OR gate using only NOR gates.

*Step 1 — Recall that a NOR gate followed immediately by another NOR gate used as an inverter recovers the OR function, since NOR = NOT(OR), so NOT(NOR) = OR.*

*Step 2 — Stage 1:* Feed the two inputs A and B into a single 2-input NOR gate: Output₁ = (A+B)' (i.e., NOT(A+B)).

*Step 3 — Stage 2:* Feed Output₁ into a second NOR gate, with **both inputs tied together** to Output₁ (making this second NOR behave as an inverter, since NOR(X,X) = NOT(X+X) = NOT(X)):
Output₂ = NOT(Output₁) = NOT(NOT(A+B)) = **A+B**

**Result:** Two NOR gates in cascade — the first a plain 2-input NOR(A,B), the second a NOR used as an inverter (both its inputs tied to the first NOR's output) — realize the function **F = A+B**, i.e., a 2-input OR gate.

---

**Q27. [Unit III | Topic: MOSFET Biasing | Type: Numerical | Difficulty: Intermediate]**

**Question:** An enhancement MOSFET has V_T = 2 V and k = 0.5 mA/V². Find the drain current I_D at V_GS = 5 V (in the saturation region), using I_D = k(V_GS−V_T)².

*Step 1 — Compute (V_GS−V_T):*
V_GS − V_T = 5 − 2 = **3 V**

*Step 2 — Square this value:*
(V_GS−V_T)² = 3² = **9 V²**

*Step 3 — Multiply by k:*
I_D = k × (V_GS−V_T)² = 0.5mA/V² × 9V² = **4.5 mA**

---

### Section C: Advanced Theory & Numericals

**Q28. [Unit III | Topic: JFET Construction & Working | Type: Theory | Difficulty: Advanced]**

**Question:** Draw the construction and explain the working of an n-channel JFET, describing how the depletion regions widen with increasing reverse gate-source voltage, and clearly explain the pinch-off condition.

*Step 1 — Construction recap:* An n-channel JFET is a bar of n-type silicon with two p-type regions diffused symmetrically into opposite faces of the bar, forming the gate — the p-n junctions thus formed run along most of the length of the n-channel bar. Ohmic contacts at the two ends of the n-bar form the source and drain terminals.

*Step 2 — Condition at V_GS = 0, V_DS = 0:* With no bias applied, small depletion regions exist naturally at the two gate-channel junctions (due to the inherent built-in potential of any p-n junction), but these are thin and leave most of the channel width open for conduction.

*Step 3 — Effect of applying V_DS (with V_GS still = 0):* As V_DS is increased (drain positive relative to source), current begins to flow along the channel from source to drain. However, this current flow itself creates a voltage drop *along the length of the channel* — meaning points closer to the drain sit at a higher potential (relative to the gate, which is typically near source potential in this simplified case) than points closer to the source. Since the gate-channel junction near the drain end thus experiences a **larger effective reverse bias** than near the source end, the depletion region is **wider near the drain and narrower near the source** — the channel takes on a **wedge/tapered shape**, narrower toward the drain.

*Step 4 — Pinch-off condition (V_GS=0 case):* As V_DS is increased further, this tapering becomes more pronounced, until at V_DS = V_P (the pinch-off voltage), the depletion regions from both sides **just touch** at the drain end of the channel — this is the "pinch-off" point. Beyond this V_DS, the pinched-off region (a very short, high-field zone right at the drain end) absorbs any further increase in V_DS, while the current through the channel is limited primarily by the (now largely fixed) resistance of the un-pinched portion of the channel — hence I_D levels off and saturates, remaining nearly constant with further V_DS increase.

*Step 5 — Effect of applying a reverse V_GS (in addition to V_DS):* Applying a reverse bias V_GS (negative for n-channel) directly adds to the reverse bias already present at the gate-channel junction (from the channel's own voltage drop, as in Step 3) — this widens the depletion regions **everywhere along the channel**, not just near the drain, effectively narrowing the entire channel and reducing its conductivity uniformly on top of the tapering effect. Consequently, **pinch-off now occurs at a smaller V_DS** than before (since the channel starts out narrower due to V_GS, less additional narrowing from V_DS is needed to fully pinch it off) — and the saturation current level reached is correspondingly **lower**. As V_GS is made increasingly negative, this pinch-off V_DS shrinks further, and the saturation current drops further, until at V_GS=V_P, the channel is pinched off even at V_DS=0 (fully closed), and I_D≈0 for any V_DS — this is the JFET's cut-off condition.

---

**Q29. [Unit III | Topic: Enhancement MOSFET Channel Formation | Type: Theory | Difficulty: Advanced]**

**Question:** Explain the channel formation process in an enhancement-type MOSFET as V_GS is increased from zero, and differentiate in detail between depletion-type and enhancement-type MOSFETs (construction, channel at V_GS=0, and typical transfer characteristic shape).

*Step 1 — Starting condition (V_GS=0):* Consider an n-channel enhancement MOSFET built on a p-type substrate, with n+ source and drain regions. At V_GS=0, there is no conducting path between source and drain — the two n+ regions are separated by the p-type substrate material, which (along with the two back-to-back p-n junctions this creates with the source/drain) blocks any current flow: I_D≈0 regardless of V_DS.

*Step 2 — Applying a small positive V_GS (below threshold):* As a small positive voltage is applied to the gate (relative to source/substrate), it begins to repel the majority carriers (holes, in the p-type substrate) away from the region directly under the gate oxide, creating a thin depletion region there (similar in concept to reverse-biasing a junction, but here achieved via the field through the insulating oxide rather than through direct current flow) — but as yet, no free electrons are drawn into this region, so still no conducting channel exists.

*Step 3 — Applying V_GS beyond the threshold voltage (V_GS > V_T):* As V_GS is increased further, the electric field through the oxide becomes strong enough to attract minority carriers (electrons, in the p-substrate) from the substrate/source/drain regions toward the surface directly beneath the gate oxide, forming a thin layer of mobile electrons — this process is called **inversion** (the surface layer's effective carrier type has "inverted" from p-type-like to n-type-like). This thin inverted layer of electrons now forms a **conducting n-type channel** directly connecting the source and drain regions.

*Step 4 — Effect of further increasing V_GS beyond V_T:* The strength (electron density, and hence conductivity) of this induced channel continues to increase with further increases in V_GS beyond V_T — this is why it's called an "enhancement" MOSFET: increasing V_GS **enhances** (strengthens) the channel that was induced at threshold, allowing progressively larger I_D for a given V_DS.

**Detailed differentiation:**

| Aspect | Depletion-type MOSFET | Enhancement-type MOSFET |
|---|---|---|
| Construction | Has a **physically diffused, pre-built** conducting channel between source and drain at time of manufacture | Has **no** pre-built channel — source and drain regions are initially separated by the oppositely-doped substrate |
| Channel at V_GS=0 | **Present** — device conducts significant I_D at V_GS=0 ("normally on") | **Absent** — device conducts negligible I_D at V_GS=0 ("normally off") |
| Operating modes | Can operate in **both** depletion mode (V_GS negative for n-channel, narrowing/depleting the existing channel, reducing I_D) and enhancement mode (V_GS positive, widening/enhancing the channel, increasing I_D) | Can operate **only** in enhancement mode (V_GS must exceed the positive threshold V_T, for n-channel, to create and then strengthen a channel) |
| Typical transfer characteristic (I_D vs V_GS) shape | A curve that is **non-zero at V_GS=0** and extends into **negative** V_GS values (depletion region of operation) before cutting off, then continues rising into positive V_GS (enhancement region) — a continuous curve spanning both polarities of V_GS | A curve that is **exactly zero for all V_GS below V_T** (a flat zero segment), then rises (following a roughly square-law shape, I_D∝(V_GS−V_T)²) only for V_GS beyond the positive threshold V_T — curve exists only in the V_GS > V_T region |

---

**Q30. [Unit III | Topic: K-Map Minimization — 4-Variable | Type: Numerical | Difficulty: Advanced]**

**Question:** Minimize the expression using a K-map: f(A,B,C,D) = Σm(1,3,7,8,10,11,13,14,15). Implement the minimized expression using NAND gates only.

*Step 1 — Set up a 4-variable K-map (rows AB in Gray-code order 00,01,11,10; columns CD in Gray-code order 00,01,11,10), and place 1s at the given minterm positions.*

Minterm binary values (ABCD): m1=0001, m3=0011, m7=0111, m8=1000, m10=1010, m11=1011, m13=1101, m14=1110, m15=1111

| AB\\CD | 00 | 01 | 11 | 10 |
|---|---|---|---|---|
| 00 | 0(m0) | 1(m1) | 1(m3) | 0(m2) |
| 01 | 0(m4) | 0(m5) | 1(m7) | 0(m6) |
| 11 | 0(m12) | 1(m13) | 1(m15) | 1(m14) |
| 10 | 1(m8) | 0(m9) | 1(m11) | 1(m10) |

*Step 2 — Identify groups. Look for the largest possible groups first (octets, then quads, then pairs).*

**Group 1 (quad):** Check column CD=11 (m3,m7,m15,m11 — all four rows of AB): m3=1, m7=1, m15=1, m11=1 — **all four are 1!** This is a valid quad: the full column CD=11. In this group, C=1 and D=1 (constant throughout), while A and B both vary across all four combinations — this group simplifies to **CD**.

**Group 2 (pair):** Check m8 and m10 (AB=10 row, CD=00 and CD=10 columns): m8=1, m10=1 — valid pair. In this pair, A=1, B=0 (constant), D=0 (constant, since CD=00 has D=0 and CD=10 has D=0), while C varies — this group simplifies to **AB'D'**.

**Group 3 (quad):** Check row AB=11 combined with row AB=10 at columns CD=10 and CD=11 (m14,m15 from AB=11 row; m10,m11 from AB=10 row): m14=1,m15=1,m10=1,m11=1 — **all four are 1!** Valid quad. In this group, A=1 (constant, since both AB=11 and AB=10 have A=1), C=1 (constant, since both CD=10 and CD=11 have C=1), while B and D vary — this group simplifies to **AC**.

**Remaining coverage check:** After Groups 1–3, covered minterms: m3,m7,m15,m11 (Group1); m8,m10 (Group2); m14,m15,m10,m11 (Group3). Combined: m3,m7,m8,m10,m11,m14,m15. From the original list {1,3,7,8,10,11,13,14,15}, still uncovered: **m1 and m13**.

**Group 4 (pair):** m1(AB=00,CD=01) with its adjacent neighbor m3(AB=00,CD=11) — both in row AB=00: A=0,B=0 (constant), D=1 (constant, since CD=01 and CD=11 both have D=1), C varies — this pair simplifies to **A'B'D**.

**Group 5 (pair):** m13(AB=11,CD=01) with its adjacent neighbor m15(AB=11,CD=11) — both in row AB=11: A=1,B=1 (constant), D=1 (constant), C varies — this pair simplifies to **ABD**.

*Step 3 — Compile the complete minimized SOP expression:*

**f(A,B,C,D) = CD + AC + AB'D' + A'B'D + ABD**

*Step 4 — Implement using NAND gates only.* Apply double complementation and De Morgan's theorem (standard technique: SOP is naturally an OR-of-ANDs, and NAND-NAND realizes exactly this same function when both logic levels use NAND gates):

f = ((CD)' · (AC)' · (AB'D')' · (A'B'D)' · (ABD)')'

*Step 5 — Circuit realization:* This translates to **five first-level NAND gates** (2- or 3-input, one per product term: CD, AC, AB'D', A'B'D, ABD — each computing the NAND of its literals, using single-input NAND gates as inverters to generate the complemented literals B', D', A' as needed), followed by **one 5-input NAND gate** at the second level, combining the outputs of all five first-level NAND gates to produce the final output f — the standard "AND-OR realized as NAND-NAND" implementation structure.

---

**Q31. [Unit III | Topic: NAND Realization of Boolean Function | Type: Numerical | Difficulty: Advanced]**

**Question:** State De Morgan's theorem. Realize the given function using NAND gates: F = B'D' + B'C' + A'C'D

*Step 1 — De Morgan's theorem (restated from Q14):* (A+B)' = A'B', and (AB)' = A'+B'.

*Step 2 — Given SOP expression:*
F = B'D' + B'C' + A'C'D

*Step 3 — Apply double complementation and De Morgan's theorem to convert to NAND-NAND form:*
F = ((B'D')' · (B'C')' · (A'C'D)')'

*Step 4 — Circuit realization, level by level:*

**Level 0 (inverters, realized as single-input NAND gates with both inputs tied together):** Generate the complemented literals needed: A', B', C', D' (all four appear somewhere in the expression: B', D', C', A').

**Level 1 (first-level NAND gates, one per product term):**
- NAND gate 1, inputs (B', D') → output = (B'D')'
- NAND gate 2, inputs (B', C') → output = (B'C')'
- NAND gate 3, inputs (A', C', D) → output = (A'C'D)' (note: D is used directly/uncomplemented here, since the term A'C'D uses true D)

**Level 2 (final NAND gate, combining all first-level outputs):**
- NAND gate 4, inputs = [output of NAND1, output of NAND2, output of NAND3] → output = [(B'D')'·(B'C')'·(A'C'D)']' = **F**

*Step 5 — Total gate count:* 4 inverters (for A', B', C', D' — realized as single-input NAND gates) + 3 first-level NAND gates (one per product term) + 1 final second-level 3-input NAND gate = **8 NAND gates total** (using only NAND gates throughout, confirming the universal-gate realization).

---

**Q32. [Unit III | Topic: JFET Load Line & Q-Point | Type: Numerical | Difficulty: Advanced]**

**Question:** A JFET with I_DSS = 8 mA and V_P = −4 V is self-biased using a source resistor R_S. If the desired quiescent drain current is I_DQ = 2 mA, find the required value of R_S using the Shockley equation (find V_GSQ first, then R_S = |V_GSQ|/I_DQ).

*Step 1 — Use the Shockley equation to find V_GSQ, given the desired I_DQ:*
I_D = I_DSS[1−(V_GS/V_P)]²

2 = 8[1−(V_GS/(−4))]²

*Step 2 — Divide both sides by 8:*
2/8 = [1+(V_GS/4)]²
0.25 = [1+(V_GS/4)]²

*Step 3 — Take the square root of both sides:*
√0.25 = 1+(V_GS/4)
0.5 = 1+(V_GS/4)

(We take the positive root here, since for self-bias with a source resistor, V_GS must be negative and of a magnitude that gives 1+(V_GS/4) a positive value less than 1, consistent with the physical requirement 0 < I_D < I_DSS.)

*Step 4 — Solve for V_GS:*
V_GS/4 = 0.5 − 1 = −0.5
V_GS = −0.5×4 = **−2 V**

*Step 5 — In a self-bias JFET circuit, V_GS is set entirely by the drop across R_S (since the gate is at ≈0V through the large gate resistor R_G, carrying negligible current, and the source sits above ground at I_DR_S): V_GS = −I_DR_S (negative because the source is positive relative to the grounded gate, making the gate negative relative to the source).*

*Step 6 — Solve for R_S using the magnitude relation:*
|V_GSQ| = I_DQ × R_S
R_S = |V_GSQ|/I_DQ = 2/2mA = 2/0.002 = **1000 Ω = 1 kΩ**

---

**Q33. [Unit III | Topic: MOSFET as Amplifier vs Switch | Type: Theory | Difficulty: Advanced]**

**Question:** Explain the operation of a MOSFET as an amplifier (biased in the saturation region) versus as a switch (operated between cut-off and the ohmic/triode region), discussing the differences in biasing point and the role of the load line in each mode of operation.

*Step 1 — MOSFET as an amplifier (linear/analog operation):* For amplification, the MOSFET is DC-biased at a fixed quiescent point (Q-point) that lies well within the **saturation region** of its output characteristics — chosen so that I_D depends on V_GS (via I_D=k(V_GS−V_T)², approximately, ignoring channel-length modulation) in a way that's reasonably linear for small AC signal variations around this Q-point. This Q-point is positioned intentionally **away from both extremes** (cut-off and the triode/ohmic-region boundary) on the DC load line, so that a superimposed small AC input signal on the gate causes I_D (and hence V_DS, via the load resistor) to swing symmetrically up and down around the Q-point without hitting either extreme — this is exactly analogous to the BJT Q-point-centering principle discussed for BJTs. The load line here represents all possible (V_DS, I_D) operating combinations for a given supply voltage and drain resistance, and the Q-point is the specific point on this line selected by the DC bias network; small-signal AC operation is analyzed as small excursions *along* this same load line around the Q-point.

*Step 2 — MOSFET as a switch (digital/switching operation):* For switching, the MOSFET is deliberately driven to the two **extreme ends** of the load line, rather than resting at a fixed intermediate Q-point:
- **"OFF" state:** V_GS is held below V_T (cut-off region) — operating point sits at the load line's horizontal-axis extreme, where I_D≈0 and V_DS≈V_supply (nearly all the supply voltage appears across the "open" MOSFET).
- **"ON" state:** V_GS is driven well above V_T (deep into the triode/ohmic region, with a low V_DS) — operating point sits near the load line's vertical-axis extreme, where I_D is at its maximum (limited by R_D/load) and V_DS is very small (V_DS(on), nearly a short circuit).

*Step 3 — Key difference in biasing philosophy:* In amplifier operation, biasing is designed to place and *hold* the device at one specific, stable **intermediate** point (deliberately avoiding both extremes) to allow linear signal amplification around it. In switching operation, biasing (via the gate drive signal) is designed to rapidly and repeatedly drive the device *between* the two **extreme** points of the load line (cut-off and deep triode/ohmic "on" state), spending as little time as possible in the intermediate (active/saturation) region during transitions — since that intermediate region is where the device simultaneously has significant V_DS *and* significant I_D, meaning it's where power dissipation (P=V_DS×I_D) is highest; switching operation seeks to minimize time spent there specifically to minimize switching power loss, which is the opposite design goal from amplifier operation, where that very same "significant V_DS and I_D" active-region condition is precisely the intended (and only) mode of operation.


## Detailed Step-Wise Solutions — UNIT IV: Operational Amplifier and Applications

---

### Section A: Definitions & Concept Questions

**Q1. [Unit IV | Topic: Op-Amp Basics | Type: Theory | Difficulty: Basic]**

**Question:** Define an operational amplifier (op-amp). Name its main input and output terminals.

*Concept from scratch:* An **operational amplifier (op-amp)** is a high-gain, direct-coupled differential voltage amplifier IC, designed to amplify the difference between two input voltages, originally used to perform mathematical "operations" (addition, subtraction, integration, etc.) in analog computers — hence the name.

**Main terminals:** **Inverting input (−)**, **Non-inverting input (+)**, **Output (V_o)** (also has power supply terminals, +V_CC and −V_EE, not signal terminals).

---

**Q2. [Unit IV | Topic: Ideal Op-Amp Parameters | Type: Theory | Difficulty: Basic]**

**Question:** List the parameters of a practical operational amplifier and compare each with the corresponding ideal amplifier value.

*Concept from scratch:*

| Parameter | Ideal value | Practical (typical) value |
|---|---|---|
| Open-loop voltage gain (A_OL) | Infinite (∞) | Very large but finite, e.g., 10⁵–10⁶ |
| Input impedance (R_i) | Infinite (∞) | Very high but finite, e.g., MΩ–TΩ (higher for FET-input op-amps) |
| Output impedance (R_o) | Zero (0) | Small but non-zero, typically tens to a few hundred ohms |
| Bandwidth | Infinite (∞) | Limited (finite gain-bandwidth product, GBW) |
| CMRR | Infinite (∞) | Very large but finite, e.g., 80–120 dB |
| Input offset voltage | Zero (0) | Small but non-zero, typically µV to a few mV |
| Slew rate | Infinite (∞) | Finite, typically 0.5–20+ V/µs |

---

**Q3. [Unit IV | Topic: Virtual Ground | Type: Theory | Difficulty: Basic]**

**Question:** Define the concept of virtual ground as applied to an inverting op-amp amplifier.

*Concept from scratch:* In an inverting amplifier with negative feedback, the op-amp's very high open-loop gain forces the differential input voltage (V+ − V−) to be essentially zero (since even a tiny differential voltage, multiplied by the enormous open-loop gain, would otherwise drive the output to its supply-rail limits). If the non-inverting input (+) is grounded (0V), then the inverting input (−) must also sit at essentially 0V, **without actually being physically connected to ground**. This node is called a **virtual ground** — it behaves as if grounded (for voltage purposes) but carries no direct connection to ground and can, in principle, still carry current (which flows through the feedback resistor rather than to true ground).

---

**Q4. [Unit IV | Topic: Slew Rate | Type: Theory | Difficulty: Basic]**

**Question:** Define slew rate of an op-amp. State its unit.

*Concept from scratch:* **Slew rate (SR)** is the maximum rate at which an op-amp's output voltage can change in response to a rapidly changing (e.g., step) input — it reflects an internal current-limited charging rate of the op-amp's compensation capacitor. SR = (dV_o/dt)_max.

**Unit:** volts per microsecond (**V/µs**).

---

**Q5. [Unit IV | Topic: Unity Follower | Type: Theory | Difficulty: Basic]**

**Question:** Define a unity (voltage) follower circuit using an op-amp. State its voltage gain and its main application.

*Concept from scratch:* A **unity (voltage) follower** is a non-inverting op-amp configuration in which the **entire output is fed back directly to the inverting input** (i.e., R_f=0 and no input resistor to ground, or equivalently, output directly wired to the inverting input), with the input signal applied at the non-inverting input.

**Voltage gain:** **A_V = 1** (unity — output exactly follows/equals the input).

**Main application:** Used as a **buffer** — to isolate a high-impedance signal source from a low-impedance load, since it provides very high input impedance (drawing negligible current from the source) while presenting very low output impedance (able to drive the load effectively), without altering the signal's voltage level.

---

**Q6. [Unit IV | Topic: CMRR | Type: Theory | Difficulty: Basic]**

**Question:** What does CMRR indicate? What is the ideal value of CMRR for an op-amp?

*Concept from scratch:* **CMRR (Common-Mode Rejection Ratio)** indicates an op-amp's ability to **reject (suppress) signals that are common to both inputs** (common-mode signals, such as noise or interference picked up identically on both input lines) while still amplifying the genuine **difference** between the two inputs (the differential-mode signal). It is defined as the ratio of differential-mode gain to common-mode gain: CMRR = A_d/A_cm (often expressed in dB).

**Ideal value:** **Infinite (∞)** — meaning an ideal op-amp would completely reject any common-mode signal, amplifying only the true differential input.

---

**Q7. [Unit IV | Topic: Differential and Common Mode | Type: Theory | Difficulty: Basic]**

**Question:** Define differential-mode gain and common-mode gain of a differential (op-amp) amplifier.

*Concept from scratch:*
- **Differential-mode gain (A_d):** The gain applied to the **difference** between the two input signals: A_d = V_o/(V1−V2), measured when the two inputs are driven with equal-magnitude, opposite-polarity signals (a pure differential signal).
- **Common-mode gain (A_cm):** The gain applied to any signal that is **common** (identical) to both inputs simultaneously: A_cm = V_o/V_cm, measured when both inputs are driven by the same signal (a pure common-mode signal, with no difference between them). Ideally, A_cm=0 (or as close to zero as possible).

---

**Q8. [Unit IV | Topic: Inverting Amplifier | Type: Theory | Difficulty: Basic]**

**Question:** Draw the circuit of an inverting op-amp amplifier and write the expression for its voltage gain in terms of the feedback and input resistors.

*Concept from scratch (circuit description):* The input signal V_in is applied through an input resistor R_1 to the **inverting (−)** input of the op-amp. A feedback resistor R_f connects from the output back to this same inverting input node. The **non-inverting (+)** input is grounded.

**Voltage gain expression:**

**A_V = V_o/V_in = −R_f/R_1**

(The negative sign reflects the 180° phase inversion characteristic of this configuration.)

---

**Q9. [Unit IV | Topic: Non-Inverting Amplifier | Type: Theory | Difficulty: Basic]**

**Question:** Draw the circuit of a non-inverting op-amp amplifier and write the expression for its voltage gain.

*Concept from scratch (circuit description):* The input signal V_in is applied directly to the **non-inverting (+)** input of the op-amp. The **inverting (−)** input is connected to the junction of a feedback resistor R_f (from the output) and a resistor R_1 (to ground) — forming a voltage-divider feedback network.

**Voltage gain expression:**

**A_V = V_o/V_in = 1 + (R_f/R_1)**

(Positive, since this configuration is non-inverting; gain is always ≥1, unlike the inverting configuration which can have gain magnitude less than, equal to, or greater than 1.)

---

**Q10. [Unit IV | Topic: Adder Circuit | Type: Theory | Difficulty: Basic]**

**Question:** Define a summing amplifier (adder) circuit using an op-amp. Write the general expression for its output in terms of the input voltages and resistors.

*Concept from scratch:* A **summing amplifier (adder)** is an extension of the inverting amplifier, in which **multiple input signals**, each through its own separate input resistor, are all connected to the same inverting (virtual-ground) input node, with a single common feedback resistor R_f.

**General output expression** (for inputs V1, V2, ..., Vn through resistors R1, R2, ..., Rn respectively):

**V_o = −R_f (V1/R1 + V2/R2 + ... + Vn/Rn)**

(For the common special case where all input resistors are equal, R1=R2=...=Rn=R: V_o = −(R_f/R)(V1+V2+...+Vn), giving a scaled sum of all inputs.)

---

**Q11. [Unit IV | Topic: Difference Amplifier | Type: Theory | Difficulty: Basic]**

**Question:** Define a difference amplifier using an op-amp. Write the expression for its output voltage for the case of equal resistor ratios.

*Concept from scratch:* A **difference amplifier** combines both inverting and non-inverting inputs to amplify the **difference** between two input signals V1 and V2 — V1 is applied through a resistor to the inverting input (with feedback resistor R_f), and V2 is applied through a matched resistor network to the non-inverting input (with a resistor to ground, forming a voltage divider).

**Output expression (for the case where the resistor ratios on both sides are matched, i.e., R_f/R1 = R_f'/R2' for the respective input/feedback pairs):**

**V_o = (R_f/R1)(V2 − V1)**

(With V1 applied to the inverting side and V2 to the non-inverting side, through matched resistor ratios — the output is proportional purely to the difference V2−V1.)

---

**Q12. [Unit IV | Topic: Integrator | Type: Theory | Difficulty: Basic]**

**Question:** Define an op-amp integrator circuit. Write the expression relating its output voltage to the input voltage.

*Concept from scratch:* An **op-amp integrator** replaces the feedback resistor of a standard inverting amplifier with a **capacitor (C)**, while retaining an input resistor R. Using the virtual-ground concept, the input current I=V_in/R must flow entirely into the capacitor (since no current enters the op-amp's input terminal), charging it over time, so the output voltage becomes proportional to the **time integral** of the input voltage.

**Output expression:**

**V_o(t) = −(1/RC) ∫V_in(t) dt**

(The output is a scaled, negative, running integral of the input signal over time.)

---

**Q13. [Unit IV | Topic: Op-Amp Input Impedance/Output Impedance | Type: Theory | Difficulty: Basic]**

**Question:** State the ideal values of input impedance, output impedance, and open-loop gain of an op-amp.

*Concept from scratch:* For an **ideal** op-amp:
- **Input impedance (R_i):** **Infinite (∞)** — draws no current at its input terminals.
- **Output impedance (R_o):** **Zero (0)** — output voltage is unaffected by loading, regardless of load current drawn.
- **Open-loop gain (A_OL):** **Infinite (∞)** — allows the "virtual short" (differential input ≈0) assumption to hold exactly under negative feedback.

---

**Q14. [Unit IV | Topic: Op-Amp Golden Rules | Type: Theory | Difficulty: Basic]**

**Question:** State the two "golden rules" used for analyzing ideal op-amp circuits with negative feedback.

*Concept from scratch:* These two simplifying rules follow directly from the ideal parameter assumptions (infinite gain, infinite input impedance) and are valid whenever the op-amp is operating within a negative-feedback loop (not open-loop or saturated):

1. **Rule 1 (virtual short/no differential voltage):** The voltage difference between the two input terminals is zero: **V+ = V−** (the op-amp's output adjusts itself, via the feedback path, to whatever value makes this true).

2. **Rule 2 (no input current):** No current flows into (or out of) either input terminal of the op-amp: **I+ = I− = 0** (since input impedance is assumed infinite).

---

### Section B: Computational Fluency

**Q15. [Unit IV | Topic: Inverting Amplifier | Type: Numerical | Difficulty: Intermediate]**

**Question:** An inverting amplifier has R_in = 20 kΩ and R_f = 100 kΩ, with input voltage V_1 = 1.5 V. Calculate the output voltage V_o.

*Step 1 — Recall the inverting amplifier gain formula:*
A_V = −R_f/R_in

*Step 2 — Substitute:*
A_V = −100kΩ/20kΩ = **−5**

*Step 3 — Compute the output voltage:*
V_o = A_V × V_1 = −5 × 1.5 = **−7.5 V**

---

**Q16. [Unit IV | Topic: Non-Inverting Amplifier | Type: Numerical | Difficulty: Intermediate]**

**Question:** A non-inverting amplifier has R_1 = 1 kΩ (to ground) and R_f = 9 kΩ (feedback), with input voltage V_1 = 0.8 V. Calculate the output voltage V_o.

*Step 1 — Recall the non-inverting amplifier gain formula:*
A_V = 1 + (R_f/R_1)

*Step 2 — Substitute:*
A_V = 1 + (9kΩ/1kΩ) = 1+9 = **10**

*Step 3 — Compute the output voltage:*
V_o = A_V × V_1 = 10 × 0.8 = **8 V**

---

**Q17. [Unit IV | Topic: Op-Amp Output Range | Type: Numerical | Difficulty: Intermediate]**

**Question:** In an inverting amplifier with R_1 = 20 kΩ and R_f = 200 kΩ, the input voltage varies from 0.1 V to 0.5 V. Find the corresponding range of output voltage.

*Step 1 — Compute the gain:*
A_V = −R_f/R_1 = −200kΩ/20kΩ = **−10**

*Step 2 — Compute output at the lower input extreme (V_in=0.1V):*
V_o(min input) = −10 × 0.1 = **−1 V**

*Step 3 — Compute output at the upper input extreme (V_in=0.5V):*
V_o(max input) = −10 × 0.5 = **−5 V**

*Result:* As V_in varies from 0.1 V to 0.5 V, **V_o varies from −1 V to −5 V** (note: due to the inverting gain, the output range is "reversed" in sign/ordering relative to the input — the output becomes more negative as the input increases).

---

**Q18. [Unit IV | Topic: Adder Circuit | Type: Numerical | Difficulty: Intermediate]**

**Question:** A summing (inverting adder) amplifier has two input resistors R_1 = R_2 = 10 kΩ and feedback resistor R_f = 10 kΩ, with input voltages V_1 = 2 V and V_2 = 3 V. Find the output voltage.

*Step 1 — Recall the summing amplifier output formula:*
V_o = −R_f(V1/R1 + V2/R2)

*Step 2 — Substitute values:*
V_o = −10kΩ × (2V/10kΩ + 3V/10kΩ)

*Step 3 — Compute each term inside the brackets:*
2/10kΩ = 0.2 mA
3/10kΩ = 0.3 mA
Sum = 0.5 mA

*Step 4 — Multiply by −R_f:*
V_o = −10kΩ × 0.5mA = −10,000×0.0005 = **−5 V**

*(Cross-check using the equal-resistor shortcut, since R1=R2=Rf here: V_o = −(V1+V2) = −(2+3) = −5V ✓)*

---

**Q19. [Unit IV | Topic: Difference Amplifier | Type: Numerical | Difficulty: Intermediate]**

**Question:** A difference amplifier has all four resistors equal to 10 kΩ, with V_1 = 5 V and V_2 = 3 V applied to the inverting and non-inverting inputs respectively (through matched resistor networks). Find the output voltage.

*Step 1 — Recall the difference amplifier output formula (for matched, equal resistor ratios):*
V_o = (R_f/R1)(V2−V1)

*Step 2 — Since all resistors are equal (R_f=R1=10kΩ), the ratio R_f/R1 = 1:*
V_o = 1×(V2−V1) = (3−5) = **−2 V**

---

**Q20. [Unit IV | Topic: Integrator | Type: Numerical | Difficulty: Intermediate]**

**Question:** An op-amp integrator has R = 10 kΩ and C = 1 µF, with a constant input voltage V_in = 2 V applied at t=0 (capacitor initially uncharged). Find the output voltage at t = 5 ms.

*Step 1 — Recall the integrator output formula:*
V_o(t) = −(1/RC)∫V_in dt

*Step 2 — Since V_in=2V is constant, the integral simplifies to a straightforward multiplication:*
∫₀ᵗ V_in dt = V_in × t (for constant V_in)

*Step 3 — Compute the RC time constant:*
RC = 10,000 × 1×10⁻⁶ = 0.01 s = 10 ms

*Step 4 — Substitute into the output formula:*
V_o(t) = −(1/RC) × V_in × t = −(1/0.01) × 2 × t = −200 × 2 × t = −400t

*Step 5 — Evaluate at t=5ms=0.005s:*
V_o(5ms) = −400 × 0.005 = **−2 V**

---

**Q21. [Unit IV | Topic: Slew Rate Limitation | Type: Numerical | Difficulty: Intermediate]**

**Question:** An op-amp has a slew rate of 0.5 V/µs. Find the maximum frequency at which it can produce an undistorted sinusoidal output of peak amplitude 5 V.

*Step 1 — Recall the full-power bandwidth formula, derived from the maximum rate of change of a sinusoid:*

For v(t) = V_p sin(ωt), the maximum slope occurs at t=0, where dv/dt|_max = V_pω. Setting this equal to the slew rate limit:

SR = V_p × ω_max = V_p × 2πf_max

*Step 2 — Rearrange to solve for f_max:*
f_max = SR/(2πV_p)

*Step 3 — Substitute values (SR=0.5V/µs = 0.5×10⁶ V/s, V_p=5V):*
f_max = (0.5×10⁶)/(2×3.1416×5)

*Step 4 — Compute the denominator:*
2×3.1416×5 = 31.416

*Step 5 — Divide:*
f_max = 500,000/31.416 = **15,915 Hz ≈ 15.9 kHz**

*Result:* Beyond this frequency (for the given 5V peak amplitude), the op-amp's output would fail to keep up with the required rate of change, and the output waveform would distort from a sine wave into a triangular-like shape (slew-rate-limited distortion).

---

**Q22. [Unit IV | Topic: CMRR Calculation | Type: Numerical | Difficulty: Intermediate]**

**Question:** An op-amp has a differential-mode gain of 100,000 and a common-mode gain of 0.5. Find its CMRR in dB.

*Step 1 — Compute the CMRR ratio:*
CMRR = A_d/A_cm = 100,000/0.5 = **200,000**

*Step 2 — Convert to dB:*
CMRR(dB) = 20 log₁₀(200,000)

*Step 3 — Compute log₁₀(200,000):*
log₁₀(200,000) = log₁₀(2×10⁵) = log₁₀(2) + 5 = 0.301+5 = 5.301

*Step 4 — Multiply by 20:*
CMRR(dB) = 20×5.301 = **106.02 dB**

---

### Section C: Advanced Theory & Numericals

**Q23. [Unit IV | Topic: Non-Inverting Amplifier — Feedback Network | Type: Numerical | Difficulty: Advanced]**

**Question:** In a circuit, a signal V_1 (input) is applied through a 20 kΩ resistor to the inverting input of an op-amp, with a 100 kΩ feedback resistor to the output, and the non-inverting input grounded. If V_1 ranges from 0.1 V to 0.5 V, find the range of output voltage, and separately determine the output voltage if instead V_1 = 1.5 V is applied at the non-inverting input through a 20 kΩ resistor with 100 kΩ feedback in a non-inverting configuration — compare the two gains obtained.

**Part (a): Inverting configuration**

*Step 1 — Gain:*
A_V(inv) = −R_f/R_in = −100kΩ/20kΩ = **−5**

*Step 2 — Output at V_1=0.1V:*
V_o = −5×0.1 = **−0.5 V**

*Step 3 — Output at V_1=0.5V:*
V_o = −5×0.5 = **−2.5 V**

**Result: Output ranges from −0.5 V to −2.5 V as V_1 ranges from 0.1V to 0.5V.**

**Part (b): Non-inverting configuration**

*Step 4 — Gain:*
A_V(non-inv) = 1+(R_f/R_1) = 1+(100kΩ/20kΩ) = 1+5 = **6**

*Step 5 — Output at V_1=1.5V:*
V_o = 6×1.5 = **9 V**

**Comparison of the two gains:** The inverting configuration (using the same pair of resistor values, 20kΩ and 100kΩ) gives a gain magnitude of **5** (and inverts the signal), while the non-inverting configuration, using the identical resistor values, gives a gain of **6** (non-inverting) — the non-inverting gain is always exactly **1 greater** in magnitude than the corresponding inverting gain for the same R_f/R_1 ratio, because of the added "+1" term from the direct (unity-gain) path the input signal takes to the non-inverting terminal, which the inverting configuration's virtual-ground input node does not have.

---

**Q24. [Unit IV | Topic: Op-Amp Circuit with Loading | Type: Numerical | Difficulty: Advanced]**

**Question:** For an inverting amplifier circuit consisting of an input resistor R_1 = 20 kΩ, feedback resistor R_f = 100 k�90, and input V_1 = 1.5 V, applied to a load network as shown in a typical two-resistor potential-divider style figure (1 kΩ across the output), determine V_o at the op-amp output and the corresponding voltage across the load resistor, explaining the effect (or lack of effect) of an ideal op-amp's zero output impedance on the load voltage.

*Step 1 — Compute the op-amp's output voltage (unaffected by the load, as we'll justify below) using the standard inverting-amplifier gain formula:*
A_V = −R_f/R_1 = −100kΩ/20kΩ = −5
V_o = A_V × V_1 = −5×1.5 = **−7.5 V**

*Step 2 — Determine the voltage across the 1 kΩ load resistor.* Since the load resistor is connected directly across the op-amp's output terminal (to ground), and an **ideal op-amp has zero output impedance**, the op-amp's output behaves as a perfect (ideal) voltage source at this node — meaning it can supply whatever current the load demands **without any internal voltage drop** of its own. Therefore, the full computed output voltage appears directly and unchanged across the load:

**V_load = V_o = −7.5 V** (same as the op-amp's output voltage, regardless of the load resistance value)

*Step 3 — Explain the underlying reason (zero output impedance):* If the op-amp had a non-zero output impedance R_o, connecting a finite load R_L would form a voltage divider between R_o and R_L, causing V_load = V_o × [R_L/(R_L+R_o)] — i.e., the load voltage would be somewhat **less** than the open-circuit output voltage, and would even change depending on what value of R_L is connected (a phenomenon called "loading effect" or output voltage sag). Because the **ideal** op-amp's R_o=0, this voltage-divider effect vanishes entirely (R_L/(R_L+0)=1 for any R_L>0), and the load always sees the full, load-independent output voltage predicted by the gain formula — this is precisely why the standard gain formulas (like A_V=−R_f/R_1) can be applied directly without needing to separately account for whatever load happens to be connected at the output, as long as the op-amp is treated as ideal.

---

**Q25. [Unit IV | Topic: Differential Amplifier — CMRR Application | Type: Theory | Difficulty: Advanced]**

**Question:** Explain the differential-mode and common-mode operation of an op-amp differential amplifier in detail, and derive the expression for output voltage in terms of differential gain A_d, common-mode gain A_cm, and CMRR, showing how a high CMRR suppresses common-mode noise/interference present identically on both inputs.

*Step 1 — Express the two actual input signals (V1, V2) in terms of a differential component and a common-mode component.* Any pair of input signals can be decomposed as:

Differential-mode input: V_d = V1 − V2
Common-mode input: V_cm = (V1+V2)/2 (the average of the two signals)

(This decomposition is always mathematically possible and reversible: V1 = V_cm + V_d/2, V2 = V_cm − V_d/2.)

*Step 2 — Write the total output as the sum of the amplifier's response to each component separately (valid because op-amp circuits are linear):*
V_o = A_d × V_d + A_cm × V_cm

*Step 3 — Substitute the definition of CMRR (CMRR = A_d/A_cm ⟹ A_cm = A_d/CMRR) to express the output purely in terms of A_d and CMRR:*
V_o = A_d × V_d + (A_d/CMRR) × V_cm
V_o = A_d [V_d + V_cm/CMRR]

*Step 4 — Interpret this expression:* The output is the intended differential-mode response (A_d × V_d) plus an **unwanted error term** (A_d × V_cm/CMRR) arising from imperfect common-mode rejection. As **CMRR → ∞** (the ideal case), this error term → 0, and the output becomes purely V_o = A_d×V_d (a perfectly clean differential-mode amplification, entirely unaffected by whatever common-mode signal V_cm is present).

*Step 5 — Practical application to noise/interference rejection:* Suppose a noise or interference signal (e.g., 50/60 Hz mains hum picked up on both input wires as they run alongside a nearby power cable) appears as an *identical* signal V_noise added to both V1 and V2. By the decomposition in Step 1, this noise contributes entirely to the common-mode component V_cm (it appears equally in both inputs, so it does NOT show up in the difference V_d=V1−V2 at all, since it cancels: if V1=V1(signal)+V_noise and V2=V2(signal)+V_noise, then V_d = V1−V2 = V1(signal)−V2(signal), with V_noise canceling out exactly). The noise thus appears **only** in V_cm, and per Step 4, its contribution to the output is suppressed by a factor of 1/CMRR — with a high CMRR (e.g., 100dB = a factor of 100,000), even a large common-mode noise voltage produces a negligibly small error at the output, while the genuine differential signal (which doesn't depend on CMRR at all, per Step 4's clean term A_d×V_d) is passed through at full gain. This is precisely why differential amplifiers (and differential signaling generally, e.g., in balanced audio/instrumentation wiring) are so effective at rejecting common environmental noise that couples equally onto both signal wires.

---

**Q26. [Unit IV | Topic: Integrator — Practical Limitations | Type: Theory | Difficulty: Advanced]**

**Question:** Derive the output expression of an op-amp integrator from first principles (starting from the virtual-ground and capacitor charging relations), and explain the practical problem of DC output drift/saturation in a simple integrator circuit, along with one common remedy (e.g., a large feedback resistor in parallel with C).

*Step 1 — Set up the circuit relations.* Input V_in is applied through resistor R to the inverting input (virtual ground, by golden rule 1, since the non-inverting input is grounded); the feedback element is a capacitor C, connecting the inverting input node to the output.

*Step 2 — Apply golden rule 1 (virtual short):* Since the non-inverting input is grounded (0V), the inverting input node is also held at 0V (virtual ground): V_(−) = 0.

*Step 3 — Find the current through the input resistor R (using Ohm's law, since one end is at V_in and the other at virtual ground 0V):*
I_R = (V_in − 0)/R = V_in/R

*Step 4 — Apply golden rule 2 (no current into the op-amp's input terminal):* Since no current can flow into the op-amp itself at this node, by KCL, **all** of I_R must instead flow into (or out of) the feedback capacitor C: I_C = I_R = V_in/R.

*Step 5 — Recall the fundamental capacitor charge-current relation:* I_C = C(dV_C/dt), where V_C is the voltage across the capacitor.

*Step 6 — Determine the capacitor voltage's relationship to the output.* The capacitor is connected between the virtual-ground node (0V) and the output node (V_o) — so the voltage across the capacitor, measured from the virtual-ground side to the output side, is V_C = V_o − 0 = V_o (with a sign convention where current I_C, defined as flowing from the virtual-ground node into the capacitor toward the output, corresponds to this polarity).

*Step 7 — Combine Steps 4–6:* Since I_C flows from the input side (virtual ground) toward the output, and this current is actually being drawn *from* the output node (charging the capacitor by pulling charge through it in a direction that makes V_o more negative for positive I_R) — carefully tracking the sign (a positive I_R, flowing into the virtual-ground node from the input resistor, must be matched by an equal current flowing *out* of the virtual-ground node into the capacitor, which — because the capacitor's other plate is at V_o — requires V_o to *decrease* over time for positive I_R):

C(d(−V_o)/dt) = I_R = V_in/R, i.e., −C(dV_o/dt) = V_in/R

*Step 8 — Rearrange:*
dV_o/dt = −V_in/(RC)

*Step 9 — Integrate both sides with respect to time, from 0 to t:*
V_o(t) − V_o(0) = −(1/RC)∫₀ᵗ V_in(τ) dτ

Assuming the capacitor starts uncharged (V_o(0)=0):

**V_o(t) = −(1/RC)∫₀ᵗ V_in(τ) dτ**

*Step 10 — This confirms the integrator output formula stated conceptually in Q12, now derived rigorously from first principles using the two golden rules and basic capacitor physics.*

**Practical problem — DC drift/saturation:**

*Step 11 — Explain the issue:* In a real (non-ideal) op-amp, there is always a small but non-zero **input offset voltage** (V_os, typically µV to a few mV) and/or small **input bias currents**, which act like a tiny, unwanted, essentially-constant "DC input" superimposed on the actual signal, even when the intended input V_in is zero. Because the integrator continuously accumulates (integrates) whatever input it sees over time, this tiny constant offset gets integrated indefinitely: V_o(offset contribution) = −(1/RC)∫V_os dt = −(V_os/RC)×t, which **grows linearly and without bound** as time progresses. Eventually, this accumulated offset drives the output all the way to one of the op-amp's supply rails, where it **saturates** (clips) and can no longer respond usefully to the actual intended input signal — this is the well-known "integrator drift/saturation" problem, a serious practical limitation of the simple (ideal) integrator circuit.

*Step 12 — Common remedy:* Connect a **large resistor R_f in parallel with the feedback capacitor C**. At very low frequencies (including DC, i.e., the problematic offset drift itself), this added R_f provides a finite-gain feedback path (turning the circuit into something closer to an inverting amplifier with gain −R_f/R at DC, rather than an unbounded integrator), which limits/bounds the DC gain and prevents the offset from being integrated without limit — while at higher (signal) frequencies, the capacitor's impedance (1/ωC) becomes much smaller than R_f, so the capacitor still dominates the feedback path and the circuit continues to behave as a proper integrator for the actual AC signal of interest. This modification trades off a small amount of low-frequency integration accuracy for practical, drift-free, stable operation — a standard and necessary compromise in real integrator circuit design.

---

**Q27. [Unit IV | Topic: Adder + Difference Amplifier Combined Design | Type: Numerical | Difficulty: Advanced]**

**Question:** Design an op-amp circuit that produces an output V_o = −(2V_1 + 3V_2) using a summing amplifier, specifying suitable resistor values (choosing R_f = 30 kΩ), and explain how you would modify the circuit to instead realize V_o = 2V_1 − 3V_2 using a combination of summing and difference amplifier stages.

**Part (a): Summing amplifier design for V_o = −(2V_1+3V_2)**

*Step 1 — Recall the general summing-amplifier output formula:*
V_o = −R_f(V1/R1 + V2/R2) = −[(R_f/R1)V1 + (R_f/R2)V2]

*Step 2 — Match coefficients to the desired output.* We need (R_f/R1) = 2 and (R_f/R2) = 3.

*Step 3 — With R_f fixed at 30 kΩ, solve for R1 and R2:*
R_f/R1 = 2  ⟹  R1 = R_f/2 = 30kΩ/2 = **15 kΩ**
R_f/R2 = 3  ⟹  R2 = R_f/3 = 30kΩ/3 = **10 kΩ**

**Design: R1 = 15 kΩ (for V1's input path), R2 = 10 kΩ (for V2's input path), R_f = 30 kΩ (common feedback resistor)** — this inverting summing amplifier realizes V_o = −(2V1+3V2) exactly as required.

**Part (b): Modifying to realize V_o = 2V_1 − 3V_2 (a genuine difference, not both-negative sum)**

*Step 4 — Recognize the challenge:* A single inverting summing amplifier can only produce a **negative-weighted sum** of its inputs (both terms come out with the same overall negative sign structure, scaled by each input's own resistor). To get one term positive (+2V1) and the other negative (−3V2) — with *different* signs — in a *single* op-amp stage requires a **difference amplifier** configuration (one input into the inverting side, one into the non-inverting side) rather than a pure summing amplifier, OR a two-stage cascade.

*Step 5 — Design approach 1 (two-stage cascade using an inverter):* First, build a summing amplifier that produces −(2V1+3V2) as in Part (a) is NOT directly useful here since we want +2V1 not −2V1 — instead:

**Stage 1:** Build a simple inverting amplifier for V2 alone, with gain −3 (using, say, R_in=10kΩ, R_f=30kΩ, giving output = −3V2).

**Stage 2:** Build a summing amplifier combining the *original* V1 (through a resistor set for a gain of −2, e.g., R_in=15kΩ with R_f=30kΩ) together with the *output of Stage 1* (−3V2, through a resistor set for a gain of −1, e.g., R_in=30kΩ with R_f=30kΩ) — this stage's total output = −[(−2)(V1)... 

Let me restate this more carefully and cleanly:

**Cleaner two-stage design:**
- **Stage 1 (inverter for V2):** Inverting amplifier with input V2, gain = −3 (e.g., R_in=10kΩ, R_f=30kΩ). Output of Stage 1 = −3V2.
- **Stage 2 (summing inverter combining V1 and Stage 1's output):** A summing amplifier with two inputs: V1 (through a resistor chosen for gain −2, e.g., R_a=15kΩ with common R_f=30kΩ) and Stage 1's output, −3V2 (through a resistor chosen for gain −1, e.g., R_b=30kΩ with the same R_f=30kΩ). Stage 2's output = −[(−2)(V1)... 

*Step 6 — Apply the summing formula correctly to Stage 2:* Stage 2 output = −[(R_f/R_a)V1 + (R_f/R_b)(−3V2)] = −[2V1 + 1×(−3V2)] = −[2V1−3V2] = **−2V1+3V2**

*Step 7 — This is the negative of what we want (we wanted 2V1−3V2, but got −2V1+3V2) — simply add one more inverting stage (gain −1) to flip the overall sign:*

**Stage 3 (final inverter, gain −1):** Input = Stage 2's output (−2V1+3V2), with R_in=R_f (equal resistors, e.g., both 20kΩ, for gain=−1). Stage 3 output = −1×(−2V1+3V2) = **2V1−3V2** ✓ (matches the desired result)

**Final design summary:** A three-stage cascade — Stage 1 inverts and scales V2 by −3; Stage 2 sums V1 (scaled by −2) with Stage 1's output (scaled by −1 further); Stage 3 inverts the overall result by −1 — together realizing **V_o = 2V1 − 3V2**.

*Step 8 — Alternative, more elegant approach (single difference-amplifier stage, mentioned for completeness):* A more compact solution uses a **single difference amplifier** stage: apply V1 (scaled appropriately) to the non-inverting input through a suitable resistor-divider network, and V2 (scaled appropriately) to the inverting input with its own feedback resistor — by choosing the four resistors of a standard difference-amplifier topology such that the non-inverting-side gain equals +2 (for V1) and the inverting-side gain equals −3 (for V2), a single op-amp stage can realize V_o=2V1−3V2 directly, avoiding the multi-stage cascade of Steps 4–7 — though this requires solving a slightly more involved set of four simultaneous resistor-ratio equations (one pair for each input path) rather than the simpler, more modular (if longer) multi-stage summing/inverting cascade shown above.

---

**Q28. [Unit IV | Topic: Op-Amp Ideal vs Practical Parameters | Type: Theory | Difficulty: Advanced]**

**Question:** Discuss the following with respect to a practical operational amplifier and its deviation from the ideal case: (i) input offset voltage, (ii) input bias current, (iii) finite open-loop gain and its effect on closed-loop gain accuracy, (iv) finite bandwidth (gain-bandwidth product) and its effect on high-frequency amplifier performance.

**(i) Input offset voltage (V_os):**

*Concept:* Due to unavoidable small mismatches in the internal transistor pairs of the op-amp's differential input stage (manufacturing tolerances), the output is not exactly zero even when both inputs are tied to exactly the same voltage (ideally, output should be zero in this case, for an ideal op-amp with zero offset). V_os is defined as the small DC voltage that would need to be applied between the two inputs to force the output to exactly zero, compensating for this internal mismatch.

*Effect:* Appears as a small, constant DC error added to the amplifier's output (scaled by the closed-loop gain) — particularly problematic in DC-coupled precision circuits and, as discussed in Q26, especially severe in integrator circuits where it accumulates (integrates) over time into a growing drift error.

**(ii) Input bias current (I_B):**

*Concept:* Since a real op-amp's input transistors require a small DC current to bias them into their active operating region (even though negligible *signal* current flows in for an ideal op-amp), a small but non-zero current (typically nA to pA, depending on input stage technology — BJT-input op-amps have higher I_B than FET/MOSFET-input op-amps) must actually flow into (or out of) each input terminal.

*Effect:* This bias current, flowing through whatever external resistances are connected to each input (R_1, R_f, etc. in a practical circuit), produces small additional voltage drops that were not accounted for in the ideal (zero-input-current) analysis — introducing a DC output error, particularly significant when large resistor values are used (since voltage error = I_B × R, larger R means larger error for the same I_B). A common mitigation technique is to ensure the DC resistance seen by both input terminals is matched (equal), so that the bias currents (assumed roughly equal for both inputs) produce equal and hence largely self-canceling offset effects.

**(iii) Finite open-loop gain and its effect on closed-loop gain accuracy:**

*Concept:* The ideal closed-loop gain formulas (e.g., A_V=−R_f/R_1 for the inverting amplifier) are derived assuming **infinite** open-loop gain A_OL (which makes the "virtual short" approximation, V+=V−, exact). In reality, A_OL is large but finite.

*Effect — quantitative correction:* The actual closed-loop gain differs from the ideal formula by a factor involving the "loop gain" — for a non-inverting amplifier with ideal gain (1+R_f/R_1), the actual gain is approximately:

A_V(actual) ≈ A_V(ideal) / [1 + A_V(ideal)/A_OL]

As long as A_OL ≫ A_V(ideal) (i.e., the open-loop gain is much larger than the intended closed-loop gain — a condition satisfied by a wide margin in most practical designs, given A_OL is typically 100,000+), this correction factor is very close to 1, and the ideal formula remains an excellent approximation. However, for very high closed-loop gains (approaching a significant fraction of A_OL) or for very precise applications, this deviation becomes non-negligible and must be accounted for.

**(iv) Finite bandwidth (gain-bandwidth product, GBW) and its effect on high-frequency performance:**

*Concept:* A real op-amp's open-loop gain is not actually constant/infinite across all frequencies — it is large only at DC/low frequencies and **rolls off** (decreases) at higher frequencies, typically following a fixed **gain-bandwidth product (GBW)**: the product of the op-amp's gain and the frequency at which that gain is measured remains approximately constant, GBW = A_OL(f) × f (for frequencies beyond the op-amp's internal dominant-pole frequency).

*Effect:* For any given **closed-loop gain** setting (A_V, set by the external R_f/R_1 ratio), the amplifier's usable bandwidth is limited to approximately: **f_(closed-loop bandwidth) ≈ GBW/A_V**. This means **higher gain configurations have proportionally lower usable bandwidth** — a fundamental trade-off. For example, an op-amp with GBW=1MHz configured for a closed-loop gain of 100 would only provide accurate amplification up to about 10kHz, beyond which the actual gain falls below the intended value — this must be carefully considered when designing amplifiers intended to handle higher-frequency signals, often requiring the selection of an op-amp with a sufficiently high GBW rating for the combination of gain and bandwidth the application demands.


