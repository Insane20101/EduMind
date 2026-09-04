# BSM-156 — Applied Probability and Statistics
## Detailed Step-Wise Solutions — Units I–IV (Combined)

> Every question is restated in full before its answer. Every answer builds the underlying concept from scratch before solving. No algebraic or reasoning step is skipped. Tags match the question bank exactly for RAG cross-referencing.

---

## Detailed Step-Wise Solutions — UNIT I: Basic Statistics & Curve Fitting

---

### Section A: Definitions & Concept Questions

**Q1. [Unit I | Topic: Frequency Distribution | Type: Theory | Difficulty: Basic]**

**Question:** Define frequency distribution. Distinguish between discrete and continuous frequency distributions.

*Concept from scratch:* A **frequency distribution** is a tabular arrangement of data that shows how many times (the frequency) each value, or each interval of values, of a variable occurs in a dataset.

- **Discrete frequency distribution:** The variable takes only specific, isolated (countable) values (e.g., number of children per family: 0,1,2,3,...), and each distinct value is listed against its own frequency.
- **Continuous frequency distribution:** The variable can take any value within a range, so the data is grouped into class **intervals** (e.g., 10–20, 20–30, ...), and the frequency recorded is the count of observations falling within each interval.

---

**Q2. [Unit I | Topic: Measures of Central Tendency | Type: Theory | Difficulty: Basic]**

**Question:** Define mean, median, and mode of a frequency distribution.

*Concept from scratch:*
- **Mean (x̄):** The arithmetic average — sum of all observations (each weighted by its frequency) divided by the total number of observations: x̄ = Σfx/Σf.
- **Median:** The value that divides the ordered dataset exactly in half — 50% of observations lie below it, 50% above. For grouped data, it is located within the class interval containing the (N/2)-th observation.
- **Mode:** The value (or class interval) that occurs with the greatest frequency — the most "typical" or common value in the dataset.

---

**Q3. [Unit I | Topic: Empirical Relation | Type: Theory | Difficulty: Basic]**

**Question:** Write the empirical relationship between mean, median, and mode.

*Concept from scratch:* For a moderately skewed (asymmetric) distribution, Karl Pearson observed an approximate empirical relation connecting the three measures:

**Mode = 3 Median − 2 Mean**

(Equivalently: Mean − Mode = 3(Mean − Median), used to estimate any one of the three quantities from the other two when direct calculation is difficult.)

---

**Q4. [Unit I | Topic: Central Moments | Type: Theory | Difficulty: Basic]**

**Question:** Define the r-th moment about the mean (central moment) of a distribution.

*Concept from scratch:* The **r-th central moment** measures the average of the r-th power of each observation's deviation from the mean:

**μᵣ = (1/N) Σ f(x − x̄)ʳ**

(where the sum runs over all observations/classes, weighted by frequency f, and N=Σf). Central moments describe the *shape* of a distribution: μ₂ is the variance, μ₃ relates to skewness, μ₄ relates to kurtosis.

---

**Q5. [Unit I | Topic: Raw Moments | Type: Theory | Difficulty: Basic]**

**Question:** Define the r-th moment about an arbitrary point (raw moment).

*Concept from scratch:* The **r-th raw moment about an arbitrary point A** is defined analogously to the central moment, but measuring deviations from a chosen constant A instead of from the mean:

**μᵣ' = (1/N) Σ f(x − A)ʳ**

This is often computationally easier (especially by hand, choosing A to be a convenient round number near the data), and the central moments can then be recovered from the raw moments using the conversion formulas (Q6).

---

**Q6. [Unit I | Topic: Moment Conversion | Type: Theory | Difficulty: Basic]**

**Question:** Write the relation connecting the first four central moments to the raw moments (about an arbitrary origin).

*Concept:* If μᵣ' denotes the r-th moment about an arbitrary point A, and μᵣ the r-th moment about the true mean, then:

- **μ₁ = 0** (always, by definition of the mean)
- **μ₂ = μ₂' − μ₁'²**
- **μ₃ = μ₃' − 3μ₁'μ₂' + 2μ₁'³**
- **μ₄ = μ₄' − 4μ₁'μ₃' + 6μ₁'²μ₂' − 3μ₁'⁴**

(Here μ₁' = x̄ − A is the deviation of the true mean from the chosen arbitrary point A.)

---

**Q7. [Unit I | Topic: Moment Generating Function | Type: Theory | Difficulty: Basic]**

**Question:** Define the moment generating function (MGF) of a random variable.

*Concept from scratch:* The **moment generating function** of a random variable X is defined as the expected value of eᵗˣ, treated as a function of the auxiliary variable t:

**M_X(t) = E[eᵗˣ]**

For a discrete random variable: M_X(t) = Σ p(x)eᵗˣ. For a continuous random variable: M_X(t) = ∫ f(x)eᵗˣ dx. It is called "moment generating" because, as shown in Q8, its derivatives at t=0 directly yield the moments of X.

---

**Q8. [Unit I | Topic: Moments from MGF | Type: Theory | Difficulty: Basic]**

**Question:** State how the r-th moment about the mean/origin can be obtained from the MGF.

*Concept from scratch:* Expanding eᵗˣ as a Maclaurin series (eᵗˣ = 1 + tx + t²x²/2! + t³x³/3! + ...) inside the expectation gives:

M_X(t) = 1 + tE[X] + (t²/2!)E[X²] + (t³/3!)E[X³] + ... = Σ (tʳ/r!)μᵣ'

So the r-th raw moment μᵣ' is the **coefficient of tʳ/r! in the Maclaurin expansion of M_X(t)**, or equivalently:

**μᵣ' = [dʳM_X(t)/dtʳ] evaluated at t=0**

---

**Q9. [Unit I | Topic: Skewness | Type: Theory | Difficulty: Basic]**

**Question:** Define skewness. What does positive and negative skewness indicate about a distribution?

*Concept from scratch:* **Skewness** measures the degree of **asymmetry** of a frequency distribution about its mean.

- **Positive skewness:** The distribution has a longer/fatter tail on the **right** (higher-value) side — Mean > Median > Mode.
- **Negative skewness:** The distribution has a longer/fatter tail on the **left** (lower-value) side — Mean < Median < Mode.
- **Zero skewness:** The distribution is symmetric — Mean = Median = Mode.

---

**Q10. [Unit I | Topic: Karl Pearson's Skewness | Type: Theory | Difficulty: Basic]**

**Question:** Define Karl Pearson's coefficient of skewness.

*Concept:* **Sₖ = (Mean − Mode)/Standard Deviation**

When the mode is ill-defined or difficult to compute, the equivalent empirical form (using the relation from Q3) is used instead:

**Sₖ = 3(Mean − Median)/Standard Deviation**

---

**Q11. [Unit I | Topic: Moment-based Skewness | Type: Theory | Difficulty: Basic]**

**Question:** Define the coefficient of skewness based on moments (β₁, γ₁).

*Concept:* **β₁ = μ₃²/μ₂³** (always non-negative, since it's a squared quantity — this loses the sign/direction of skewness).

To retain the direction, define **γ₁ = √β₁**, but assign it the **same sign as μ₃** (since μ₃ itself is positive for right-skewed and negative for left-skewed distributions): γ₁ = μ₃/μ₂^(3/2).

---

**Q12. [Unit I | Topic: Kurtosis | Type: Theory | Difficulty: Basic]**

**Question:** Define kurtosis. Name the three types of kurtosis (leptokurtic, mesokurtic, platykurtic) with their β₂ values.

*Concept from scratch:* **Kurtosis** measures the "peakedness" of a distribution relative to a normal distribution — specifically, how concentrated the data is near the mean versus spread into the tails. It is measured by **β₂ = μ₄/μ₂²**.

- **Leptokurtic (β₂ > 3):** Sharper peak, heavier/fatter tails than normal — more data concentrated near the mean AND more extreme outliers than a normal distribution.
- **Mesokurtic (β₂ = 3):** Same peakedness as the normal distribution (the normal distribution itself is the reference case).
- **Platykurtic (β₂ < 3):** Flatter peak, thinner tails than normal — data more evenly/uniformly spread out.

(Often the **excess kurtosis**, γ₂ = β₂ − 3, is reported instead, so that a normal distribution has γ₂=0.)

---

**Q13. [Unit I | Topic: Method of Least Squares | Type: Theory | Difficulty: Basic]**

**Question:** Define the method of least squares for curve fitting.

*Concept from scratch:* The **method of least squares** is a technique for finding the "best-fitting" curve of a chosen form (e.g., a straight line, parabola, exponential, etc.) through a set of observed data points, by choosing the curve's parameters so as to **minimize the sum of the squares of the vertical deviations** (residuals) between the observed y-values and the values predicted by the fitted curve:

Minimize: **E = Σ(yᵢ − ŷᵢ)²**, where ŷᵢ is the curve's predicted value at xᵢ.

Squaring the deviations (rather than, say, using absolute values) makes the resulting equations for the unknown parameters linear and analytically solvable (by setting partial derivatives of E to zero), and also penalizes large deviations more heavily than small ones.

---

**Q14. [Unit I | Topic: Normal Equations (Line) | Type: Theory | Difficulty: Basic]**

**Question:** Write the normal equations for fitting a straight line y = a + bx by the method of least squares.

*Concept:* Minimizing E = Σ(y − a − bx)² with respect to a and b (setting ∂E/∂a=0 and ∂E/∂b=0) yields the two **normal equations**:

**Σy = na + bΣx**
**Σxy = aΣx + bΣx²**

(where n is the number of data points), which are then solved simultaneously for a and b.

---

**Q15. [Unit I | Topic: Normal Equations (Parabola) | Type: Theory | Difficulty: Basic]**

**Question:** Write the normal equations for fitting a second-degree parabola y = a + bx + cx² by the method of least squares.

*Concept:* Minimizing E = Σ(y − a − bx − cx²)² with respect to a, b, and c yields three normal equations:

**Σy = na + bΣx + cΣx²**
**Σxy = aΣx + bΣx² + cΣx³**
**Σx²y = aΣx² + bΣx³ + cΣx⁴**

(solved simultaneously, typically by elimination, for a, b, c).

### Section B: Computational & Applied Problems

**Q16. [Unit I | Topic: Mean, Median, Mode | Type: Numerical | Difficulty: Intermediate]**

**Question:** Calculate the mean, median, and mode for the following grouped frequency distribution:

| Class interval | 0–10 | 10–20 | 20–30 | 30–40 | 40–50 |
|---|---|---|---|---|---|
| Frequency | 5 | 8 | 15 | 16 | 6 |

*Step 1 — Set up a table with class marks (midpoints) and cumulative frequencies:*

| CI | f | Midpoint (x) | fx | CF |
|---|---|---|---|---|
| 0–10 | 5 | 5 | 25 | 5 |
| 10–20 | 8 | 15 | 120 | 13 |
| 20–30 | 15 | 25 | 375 | 28 |
| 30–40 | 16 | 35 | 560 | 44 |
| 40–50 | 6 | 45 | 270 | 50 |

N = Σf = 5+8+15+16+6 = 50. Σfx = 25+120+375+560+270 = 1350.

*Step 2 — Mean:*
Mean = Σfx/N = 1350/50 = **27**

*Step 3 — Median. Locate N/2 = 25th observation.* From the CF column, the class 20–30 contains the 25th value (CF jumps from 13 to 28), so the median class is **20–30**.
Median = L + [(N/2 − CF)/f]×h, where L=20 (lower boundary), CF=13 (cumulative frequency before median class), f=15 (median class frequency), h=10 (class width).
Median = 20 + [(25−13)/15]×10 = 20 + (12/15)×10 = 20 + 8 = **28**

*Step 4 — Mode. Identify the modal class (highest frequency): 30–40 (f=16).*
Mode = L + [(f₁−f₀)/(2f₁−f₀−f₂)]×h, where L=30, f₁=16 (modal class frequency), f₀=15 (frequency of preceding class), f₂=6 (frequency of following class), h=10.
Mode = 30 + [(16−15)/(2×16−15−6)]×10 = 30 + [1/(32−21)]×10 = 30 + (1/11)×10 = 30 + 0.909 = **30.91**

**Result: Mean = 27, Median = 28, Mode ≈ 30.91.**

*Step 5 — Sanity check via the empirical relation (Q3): Mode ≈ 3(Median) − 2(Mean) = 3(28)−2(27) = 84−54 = 30, close to our directly computed mode of 30.91 — consistent, confirming the calculations are reasonable (small differences are expected since the empirical relation is approximate).*

---

**Q17. [Unit I | Topic: Missing Frequencies from Median | Type: Numerical | Difficulty: Intermediate]**

**Question:** The median of the following distribution is 46, and the total number of observations is 230. Find the missing frequencies f₁ and f₂.

| Class interval | 10–20 | 20–30 | 30–40 | 40–50 | 50–60 | 60–70 | 70–80 |
|---|---|---|---|---|---|---|---|
| Frequency | 12 | 30 | f₁ | 65 | f₂ | 25 | 18 |

*Step 1 — Use the total frequency condition to relate f₁ and f₂:*
12+30+f₁+65+f₂+25+18 = 230
150 + f₁ + f₂ = 230
**f₁ + f₂ = 80** ...(i)

*Step 2 — Identify the median class.* Since the median (46) falls between 40 and 50, the median class is **40–50** (L=40, h=10, f=65 — the frequency of this class).

*Step 3 — Compute the cumulative frequency (CF) just before the median class:*
CF = 12+30+f₁ = 42+f₁

*Step 4 — Apply the median formula:*
Median = L + [(N/2 − CF)/f]×h
46 = 40 + [(115 − (42+f₁))/65]×10

*Step 5 — Solve for f₁. Subtract 40 from both sides:*
6 = [(115−42−f₁)/65]×10
6 = [(73−f₁)/65]×10

*Step 6 — Multiply both sides by 65/10 = 6.5:*
6 × 6.5 = 73 − f₁
39 = 73 − f₁

*Step 7 — Solve for f₁:*
f₁ = 73 − 39 = **34**

*Step 8 — Substitute into equation (i) to find f₂:*
f₂ = 80 − f₁ = 80 − 34 = **46**

**Result: f₁ = 34, f₂ = 46.**

*Step 9 — Verify: total frequency = 12+30+34+65+46+25+18 = 230 ✓. CF before median class = 12+30+34=76; Median = 40+[(115−76)/65]×10 = 40+(39/65)×10 = 40+6 = 46 ✓ (matches the given median exactly).*

---

**Q18. [Unit I | Topic: Moments about a Point | Type: Numerical | Difficulty: Intermediate]**

**Question:** The first four moments of a distribution about the value 5 are 2, 20, 40, and 50. Calculate the moments about the mean, and comment upon the skewness and kurtosis of the distribution.

*Step 1 — Identify the given raw moments about A=5:*
μ₁' = 2, μ₂' = 20, μ₃' = 40, μ₄' = 50

*Step 2 — Find the mean:*
Mean = A + μ₁' = 5 + 2 = **7**

*Step 3 — Compute μ₂ using the conversion formula (Q6):*
μ₂ = μ₂' − μ₁'² = 20 − 2² = 20 − 4 = **16**

*Step 4 — Compute μ₃:*
μ₃ = μ₃' − 3μ₁'μ₂' + 2μ₁'³ = 40 − 3(2)(20) + 2(2)³ = 40 − 120 + 16 = **−64**

*Step 5 — Compute μ₄:*
μ₄ = μ₄' − 4μ₁'μ₃' + 6μ₁'²μ₂' − 3μ₁'⁴
= 50 − 4(2)(40) + 6(2²)(20) − 3(2⁴)
= 50 − 320 + 480 − 48
= **162**

*Step 6 — Compute β₁ (skewness measure):*
β₁ = μ₃²/μ₂³ = (−64)²/16³ = 4096/4096 = **1**

*Step 7 — Compute γ₁ (signed skewness coefficient):*
γ₁ = μ₃/μ₂^(3/2) = −64/16^1.5 = −64/64 = **−1**

Since γ₁ is negative, the distribution is **negatively skewed** (a longer tail on the left).

*Step 8 — Compute β₂ (kurtosis measure):*
β₂ = μ₄/μ₂² = 162/16² = 162/256 = **0.6328**

*Step 9 — Compare with the mesokurtic reference value (β₂=3):* Since 0.6328 < 3, the distribution is **platykurtic** (flatter than normal, with thinner tails).

**Result: Mean=7, μ₂=16 (variance), μ₃=−64, μ₄=162; β₁=1 (γ₁=−1, negatively skewed); β₂=0.6328 (platykurtic).**

---

**Q19. [Unit I | Topic: Straight-Line Fit | Type: Numerical | Difficulty: Intermediate]**

**Question:** Fit a straight line y = a + bx to the following data using the method of least squares, and estimate y at x=6.

| x | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| y | 2 | 5 | 3 | 8 | 7 |

*Step 1 — Compute the required sums:*
n=5. Σx = 1+2+3+4+5 = 15. Σy = 2+5+3+8+7 = 25.
Σx² = 1+4+9+16+25 = 55.
Σxy = (1×2)+(2×5)+(3×3)+(4×8)+(5×7) = 2+10+9+32+35 = 88.

*Step 2 — Write the normal equations (from Q14):*
25 = 5a + 15b ...(i)
88 = 15a + 55b ...(ii)

*Step 3 — Simplify equation (i) by dividing by 5:*
5 = a + 3b ⟹ **a = 5 − 3b** ...(iii)

*Step 4 — Substitute (iii) into (ii):*
88 = 15(5−3b) + 55b = 75 − 45b + 55b = 75 + 10b

*Step 5 — Solve for b:*
88 − 75 = 10b
13 = 10b
**b = 1.3**

*Step 6 — Substitute back into (iii) to find a:*
a = 5 − 3(1.3) = 5 − 3.9 = **1.1**

*Step 7 — Write the fitted line:*
**y = 1.1 + 1.3x**

*Step 8 — Estimate y at x=6:*
y = 1.1 + 1.3(6) = 1.1 + 7.8 = **8.9**

**Result: Fitted line y = 1.1+1.3x; estimated y(6) = 8.9.**

---

**Q20. [Unit I | Topic: Parabola Fit | Type: Numerical | Difficulty: Intermediate]**

**Question:** Fit a parabola of second degree (y = a + bx + cx²) to the following data using the method of least squares, and predict y at x=4.

| X | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| Y | 6 | 4 | 3 | 5 | 4 | 2 |

*Step 1 — Compute all required sums:*
n=6. ΣX = 1+2+3+4+5+6 = 21.
ΣX² = 1+4+9+16+25+36 = 91.
ΣX³ = 1+8+27+64+125+216 = 441.
ΣX⁴ = 1+16+81+256+625+1296 = 2275.
ΣY = 6+4+3+5+4+2 = 24.
ΣXY = (1×6)+(2×4)+(3×3)+(4×5)+(5×4)+(6×2) = 6+8+9+20+20+12 = 75.
ΣX²Y = (1×6)+(4×4)+(9×3)+(16×5)+(25×4)+(36×2) = 6+16+27+80+100+72 = 301.

*Step 2 — Write the three normal equations (from Q15):*
24 = 6a + 21b + 91c ...(1)
75 = 21a + 91b + 441c ...(2)
301 = 91a + 441b + 2275c ...(3)

*Step 3 — Eliminate a between (1) and (2). Multiply (1) by 21 and (2) by 6:*
21×(1): 504 = 126a + 441b + 1911c
6×(2): 450 = 126a + 546b + 2646c

*Step 4 — Subtract the first from the second (to cancel the 126a terms):*
450 − 504 = (546−441)b + (2646−1911)c
−54 = 105b + 735c

*Step 5 — Divide through by 105:*
**−0.5143 = b + 7c** ...(4)

*Step 6 — Eliminate a between (1) and (3). Multiply (1) by 91 and (3) by 6:*
91×(1): 2184 = 546a + 1911b + 8281c
6×(3): 1806 = 546a + 2646b + 13650c

*Step 7 — Subtract the first from the second:*
1806 − 2184 = (2646−1911)b + (13650−8281)c
−378 = 735b + 5369c

*Step 8 — Divide through by 735:*
**−0.5143 = b + 7.3054c** ...(5)

*Step 9 — Subtract equation (4) from equation (5) to eliminate b:*
(−0.5143) − (−0.5143) = (7.3054−7)c
0 = 0.3054c
**c = 0**

*Step 10 — Substitute c=0 into (4) to find b:*
−0.5143 = b + 7(0) ⟹ **b = −0.5143** (exactly −18/35)

*Step 11 — Substitute b and c into equation (1) to find a:*
24 = 6a + 21(−0.5143) + 91(0)
24 = 6a − 10.8
6a = 34.8
**a = 5.8**

*Step 12 — Write the fitted curve:*
**y = 5.8 − 0.5143x + 0×x² = 5.8 − 0.5143x**

*Step 13 — Interpretation: since c came out exactly 0, the least-squares "parabola" degenerates to a straight line for this dataset — this is a valid and meaningful outcome, indicating the underlying trend in this data is essentially linear over the observed range, with no significant curvature.*

*Step 14 — Predict y at x=4:*
y(4) = 5.8 − 0.5143(4) = 5.8 − 2.057 = **3.74**

**Result: Fitted curve y = 5.8 − 0.5143x (c=0, so effectively linear); predicted y(4) ≈ 3.74** (compares reasonably with the observed value of 5 at x=4, given the overall scatter in the data).

---

**Q21. [Unit I | Topic: Beam Deflection Fit | Type: Numerical | Difficulty: Intermediate]**

**Question:** A simply supported beam carries a concentrated load P at its midpoint. The maximum deflection Y for various P is given below. Using the method of least squares, find a law of the type Y = a + bP.

| P | 100 | 120 | 140 | 160 | 180 | 200 |
|---|---|---|---|---|---|---|
| Y | 0.45 | 0.55 | 0.60 | 0.70 | 0.80 | 0.85 |

*Step 1 — Compute the required sums (treating P as the independent variable "x"):*
n=6. ΣP = 100+120+140+160+180+200 = 900.
ΣP² = 100²+120²+140²+160²+180²+200² = 10000+14400+19600+25600+32400+40000 = 142000.
ΣY = 0.45+0.55+0.60+0.70+0.80+0.85 = 3.95.
ΣPY = (100×0.45)+(120×0.55)+(140×0.60)+(160×0.70)+(180×0.80)+(200×0.85)
= 45+66+84+112+144+170 = 621.

*Step 2 — Write the normal equations (from Q14, with x→P):*
3.95 = 6a + 900b ...(i)
621 = 900a + 142000b ...(ii)

*Step 3 — Simplify equation (i) by dividing by 6:*
0.65833 = a + 150b ⟹ **a = 0.65833 − 150b** ...(iii)

*Step 4 — Substitute (iii) into (ii):*
621 = 900(0.65833−150b) + 142000b = 592.5 − 135000b + 142000b = 592.5 + 7000b

*Step 5 — Solve for b:*
621 − 592.5 = 7000b
28.5 = 7000b
**b = 0.004071**

*Step 6 — Substitute back into (iii) to find a:*
a = 0.65833 − 150(0.004071) = 0.65833 − 0.6107 = **0.04767**

*Step 7 — Write the fitted law:*
**Y = 0.0477 + 0.00407 P**

**Result: The deflection law is approximately Y = 0.0477 + 0.00407P**, showing deflection increases nearly linearly with load, as expected physically (consistent with simple beam theory for small deflections).

---

**Q22. [Unit I | Topic: Skewness and Kurtosis from Moments | Type: Theory+Numerical | Difficulty: Intermediate]**

**Question:** Define skewness and kurtosis of a distribution. Given the first four central moments of a distribution as μ₁=0, μ₂=16, μ₃=−64, μ₄=162 (as found in Q18), find the coefficient of skewness and kurtosis.

*Concept:* (Definitions as in Q9 and Q12.)

*Step 1 — Compute β₁:*
β₁ = μ₃²/μ₂³ = (−64)²/(16)³ = 4096/4096 = **1**

*Step 2 — Compute γ₁ (with sign):*
γ₁ = μ₃/μ₂^1.5 = −64/64 = **−1** (negative skewness)

*Step 3 — Compute β₂:*
β₂ = μ₄/μ₂² = 162/256 = **0.6328**

*Step 4 — Interpret:* β₂ < 3 ⟹ **platykurtic**.

**Result: γ₁=−1 (negatively skewed), β₂=0.6328 (platykurtic)** — identical to Q18's result, since this question reuses the same central moments as a direct application exercise.

---

**Q23. [Unit I | Topic: Karl Pearson's Skewness | Type: Numerical | Difficulty: Intermediate]**

**Question:** For a distribution with Mean=27, Median=28, and Standard Deviation=10.5 (using the results from Q16), calculate Karl Pearson's coefficient of skewness and interpret the result.

*Step 1 — Since the mode was already computed in Q16 (Mode≈30.91), use the direct formula:*
Sₖ = (Mean − Mode)/SD = (27 − 30.91)/10.5 = −3.91/10.5 = **−0.372**

*Step 2 — Cross-check using the empirical (median-based) formula:*
Sₖ = 3(Mean−Median)/SD = 3(27−28)/10.5 = 3(−1)/10.5 = −3/10.5 = **−0.286**

*Step 3 — Interpret:* Both forms give a **negative** value, indicating the distribution in Q16 is **slightly negatively skewed** (a longer tail toward lower values) — consistent since Mean(27) < Median(28) < Mode(30.91), the classic ordering for negative skewness (reverse of the usual "Mean>Median>Mode for positive skew" rule).

---

**Q24. [Unit I | Topic: Straight-Line Fit — Goodness of Fit | Type: Numerical | Difficulty: Intermediate]**

**Question:** For the straight line fitted in Q19 (y=1.1+1.3x), compute the fitted (predicted) values at each given x, and comment on the goodness of fit by examining the residuals.

*Step 1 — Compute predicted ŷ at each x using y=1.1+1.3x:*
x=1: ŷ=1.1+1.3=2.4 (actual y=2, residual=2−2.4=−0.4)
x=2: ŷ=1.1+2.6=3.7 (actual y=5, residual=5−3.7=1.3)
x=3: ŷ=1.1+3.9=5.0 (actual y=3, residual=3−5.0=−2.0)
x=4: ŷ=1.1+5.2=6.3 (actual y=8, residual=8−6.3=1.7)
x=5: ŷ=1.1+6.5=7.6 (actual y=7, residual=7−7.6=−0.6)

*Step 2 — Compute the sum of squared residuals (SSE), which the least-squares method guarantees is minimized among all possible straight lines:*
SSE = (−0.4)²+(1.3)²+(−2.0)²+(1.7)²+(−0.6)² = 0.16+1.69+4.0+2.89+0.36 = **9.10**

*Step 3 — Interpret:* The residuals are of moderate size relative to the y-values (which range from 2 to 8), suggesting the linear fit captures the general upward trend but leaves noticeable scatter — consistent with the data not being perfectly linear (as would be expected from a small, somewhat noisy dataset). A lower SSE would indicate a tighter fit; this SSE, while not tiny, is the smallest achievable by ANY straight line through this data (that is the defining property of the least-squares solution).

---

**Q25. [Unit I | Topic: Kurtosis Classification | Type: Numerical | Difficulty: Intermediate]**

**Question:** For a symmetric distribution with standard deviation 5, find the value of the fourth central moment required for the distribution to be (i) leptokurtic, (ii) mesokurtic.

*Step 1 — Recall β₂ = μ₄/μ₂², and μ₂ = σ² = 5² = 25 (variance is the square of the standard deviation).*

*Step 2 — For mesokurtic, β₂ = 3 exactly:*
3 = μ₄/25² = μ₄/625
**μ₄ = 3 × 625 = 1875** (this is the exact boundary value)

*Step 3 — For leptokurtic, β₂ > 3, which means:*
μ₄/625 > 3
**μ₄ > 1875** (any value of the fourth moment greater than 1875 makes the distribution leptokurtic)

**Result: μ₄ = 1875 exactly for mesokurtic; μ₄ > 1875 for leptokurtic** (and, by extension, μ₄ < 1875 would give platykurtic).

### Section C: Advanced Theory & Numericals

**Q26. [Unit I | Topic: Parabola Fit — Full Prediction | Type: Numerical | Difficulty: Advanced]**

**Question:** Fit a parabola y = a + bx + cx² to the data of Q20 using the method of least squares, and predict y at x=7 (extrapolation beyond the observed range).

*Step 1 — Reuse the fitted curve from Q20:*
y = 5.8 − 0.5143x + 0×x² (i.e., c=0, effectively linear over this range)

*Step 2 — Predict at x=7:*
y(7) = 5.8 − 0.5143(7) = 5.8 − 3.6 = **2.2**

*Step 3 — Caution on extrapolation:* Since x=7 lies **outside** the original data range (x=1 to 6), this prediction is an **extrapolation**, which is inherently less reliable than interpolation (predicting within the observed range, as in Q20's x=4 case) — the fitted trend is only guaranteed to describe the data within the range it was fitted to; any curvature or change in trend beyond x=6 would not be captured by this fit.

**Result: Predicted y(7) ≈ 2.2, with the caveat that this is an extrapolated estimate.**

---

**Q27. [Unit I | Topic: Skewness/Kurtosis — Full Analysis | Type: Numerical | Difficulty: Advanced]**

**Question:** Define skewness and kurtosis of a distribution. The first four (central) moments of a distribution are 0, 2.5, 0.7, and 18.71. Find the coefficient of skewness and kurtosis, and comment on the nature of the distribution.

*Concept:* (Definitions as in Q9 and Q12 — these are given directly as **central** moments, since μ₁=0, which only holds for moments about the true mean.)

*Step 1 — Identify the given central moments directly (no conversion needed, since μ₁=0 confirms these are already central moments):*
μ₁=0, μ₂=2.5, μ₃=0.7, μ₄=18.71

*Step 2 — Compute β₁:*
β₁ = μ₃²/μ₂³ = (0.7)²/(2.5)³ = 0.49/15.625 = **0.03136**

*Step 3 — Compute γ₁:*
γ₁ = μ₃/μ₂^1.5 = 0.7/(2.5)^1.5 = 0.7/3.953 = **0.1771**

Since γ₁ is small and **positive**, the distribution is **very slightly positively skewed** (nearly symmetric, with only a marginal lean toward a right tail).

*Step 4 — Compute β₂:*
β₂ = μ₄/μ₂² = 18.71/(2.5)² = 18.71/6.25 = **2.9936**

*Step 5 — Interpret:* Since β₂ (2.9936) is extremely close to 3 (the mesokurtic benchmark), the distribution is **very nearly mesokurtic** — for practical purposes, its peakedness closely resembles that of a normal distribution, with an extremely slight platykurtic tendency (since 2.9936 is fractionally below 3).

**Result: β₁=0.0314, γ₁=0.177 (nearly symmetric, very slight positive skew); β₂=2.994 (essentially mesokurtic).** The overall shape of this distribution closely approximates a normal distribution, based on both its skewness and kurtosis being very near the "ideal" symmetric, normal-like values (γ₁≈0, β₂≈3).

---

**Q28. [Unit I | Topic: Normal Equations Derivation | Type: Theory | Difficulty: Advanced]**

**Question:** Derive the normal equations for fitting a straight line y = a + bx by the method of least squares, starting from the sum-of-squared-errors objective function.

*Step 1 — Define the objective function to be minimized.* For n data points (xᵢ,yᵢ), the fitted line predicts ŷᵢ=a+bxᵢ at each xᵢ. The sum of squared errors (residuals) is:
E(a,b) = Σᵢ(yᵢ − a − bxᵢ)²

*Step 2 — To minimize E with respect to the two unknowns a and b, set both partial derivatives to zero (the standard calculus condition for a minimum of a function of several variables).*

*Step 3 — Compute ∂E/∂a. Using the chain rule on each term of the sum:*
∂E/∂a = Σᵢ 2(yᵢ−a−bxᵢ)(−1) = −2Σᵢ(yᵢ−a−bxᵢ)

*Step 4 — Set this equal to zero and simplify:*
−2Σ(yᵢ−a−bxᵢ) = 0
Σyᵢ − Σa − bΣxᵢ = 0
Σyᵢ − na − bΣxᵢ = 0 (since Σa, summed n times, equals na)

**⟹ Σy = na + bΣx** ...(first normal equation)

*Step 5 — Compute ∂E/∂b:*
∂E/∂b = Σᵢ 2(yᵢ−a−bxᵢ)(−xᵢ) = −2Σᵢxᵢ(yᵢ−a−bxᵢ)

*Step 6 — Set this equal to zero and simplify:*
−2Σxᵢ(yᵢ−a−bxᵢ) = 0
Σxᵢyᵢ − aΣxᵢ − bΣxᵢ² = 0

**⟹ Σxy = aΣx + bΣx²** ...(second normal equation)

*Step 7 — Apply to a small dataset to demonstrate: for the data of Q19 (x:1,2,3,4,5; y:2,5,3,8,7), these normal equations were solved to give a=1.1, b=1.3 (see Q19 for the full numerical solution), confirming the derived formulas produce the same result obtained by direct application of the standard normal-equation formulas.*

**Result: The normal equations Σy=na+bΣx and Σxy=aΣx+bΣx² are derived directly from setting the partial derivatives of the squared-error objective function to zero — this is the fundamental derivation underlying every least-squares curve-fitting formula used throughout this unit.**

---

**Q29. [Unit I | Topic: Moment Conversion Derivation | Type: Theory | Difficulty: Advanced]**

**Question:** Derive the formula μ₂ = μ₂' − μ₁'² expressing the second central moment in terms of raw moments about an arbitrary point A.

*Step 1 — Start from the definition of the central moment (deviation from the true mean x̄), and relate it to deviation from A using the identity (x−x̄) = (x−A) − (x̄−A):*
μ₂ = (1/N)Σf(x−x̄)² = (1/N)Σf[(x−A)−(x̄−A)]²

*Step 2 — Expand the square using (P−Q)² = P²−2PQ+Q², with P=(x−A) and Q=(x̄−A):*
μ₂ = (1/N)Σf[(x−A)² − 2(x−A)(x̄−A) + (x̄−A)²]

*Step 3 — Split the sum into three separate sums (distributing Σf over the three terms):*
μ₂ = (1/N)Σf(x−A)² − (2(x̄−A)/N)Σf(x−A) + (1/N)Σf(x̄−A)²

*Step 4 — Recognize each piece:*
- (1/N)Σf(x−A)² = μ₂' (by definition, the second raw moment about A)
- (1/N)Σf(x−A) = μ₁' (by definition, the first raw moment about A, which equals x̄−A)
- (1/N)Σf(x̄−A)² = (x̄−A)² (since (x̄−A)² is a constant, not depending on x, so summing it N times and dividing by N just returns the constant itself) = μ₁'² (since μ₁'=x̄−A)

*Step 5 — Substitute these back into Step 3:*
μ₂ = μ₂' − 2(μ₁')(μ₁') + μ₁'²
= μ₂' − 2μ₁'² + μ₁'²
= **μ₂' − μ₁'²**

*Step 6 — Verify this matches the formula used throughout Q18/Q22: with μ₁'=2, μ₂'=20: μ₂=20−4=16 ✓ (exactly as computed in Q18, Step 3).*

**Result: μ₂ = μ₂' − μ₁'², derived rigorously from the definition of central moments and the algebraic identity (x−x̄)=(x−A)−(x̄−A).** (The higher-order formulas for μ₃ and μ₄, quoted in Q6, follow from an entirely analogous — though more tedious — binomial expansion of (x−x̄)³ and (x−x̄)⁴ respectively.)

---

**Q30. [Unit I | Topic: MGF and Moments Application | Type: Theory | Difficulty: Advanced]**

**Question:** Explain the significance of the moment generating function. Using the Maclaurin series expansion, derive how the second raw moment (about the origin) can be extracted from the MGF.

*Step 1 — Recall the MGF definition (Q7): M_X(t) = E[eᵗˣ].*

*Step 2 — Expand eᵗˣ as a Maclaurin series in t (standard exponential series expansion):*
eᵗˣ = 1 + tx + (t²x²)/2! + (t³x³)/3! + (t⁴x⁴)/4! + ...

*Step 3 — Take the expectation of both sides term by term (valid since expectation is a linear operator, so it can be distributed across the sum):*
M_X(t) = E[1] + tE[X] + (t²/2!)E[X²] + (t³/3!)E[X³] + (t⁴/4!)E[X⁴] + ...
= 1 + tμ₁' + (t²/2!)μ₂' + (t³/3!)μ₃' + (t⁴/4!)μ₄' + ...

*Step 4 — Differentiate M_X(t) once with respect to t (term by term):*
M_X'(t) = μ₁' + tμ₂' + (t²/2!)μ₃' + (t³/3!)μ₄' + ...

*Step 5 — Evaluate at t=0 (all terms containing t vanish):*
M_X'(0) = μ₁'

*Step 6 — Differentiate again (starting from Step 4) with respect to t:*
M_X''(t) = μ₂' + tμ₃' + (t²/2!)μ₄' + ...

*Step 7 — Evaluate at t=0:*
**M_X''(0) = μ₂'**

*Step 8 — Significance:* This confirms that the r-th derivative of the MGF, evaluated at t=0, directly gives the r-th raw moment — meaning the ENTIRE moment structure of a distribution (mean, variance, skewness, kurtosis, and beyond) is encoded compactly in a single function M_X(t). This makes the MGF a powerful tool: rather than computing each moment separately from its own definition (a separate summation/integration each time), one MGF calculation (often easier, especially for standard distributions like Binomial or Poisson) can be differentiated repeatedly to extract every moment needed.

**Result: μ₂' = M_X''(0), derived by twice differentiating the Maclaurin-expanded MGF and evaluating at t=0** — this is exactly the technique used in Unit IV (Q1, Section C) to derive the mean and variance of the Binomial distribution directly from its MGF.
