# Q47-Null-Sparse-Decomposition

**On the Distribution of the Cyclotomic Norm Form $n^{47}-(n-1)^{47}$ in Arithmetic Progressions**

**Author:** Ruqing Chen, GUT Geoservice Inc., Montreal, Canada

---

## Overview

This repository contains the paper, data, and verification scripts for the null–sparse decomposition of the Bombieri–Vinogradov error sum for the cyclotomic norm polynomial:

$$Q(n) = n^{47} - (n-1)^{47}$$

The key insight is that the rigid arithmetic structure of $Q(n)$ — arising from its identity as a norm form from $\mathbb{Q}(\zeta_{47})$ — forces the Bombieri–Vinogradov error sum to decompose into a **null part** (where the main term vanishes identically) and a **sparse part** (supported on a thin set of effective moduli).

## Main Results

| # | Result | Type |
|---|--------|------|
| **Prop 2.1** | $\omega(p) = 0$ for $p \not\equiv 1 \pmod{47}$ and $p = 47$; $\omega(p) = 46$ for $p \equiv 1 \pmod{47}$ | Proved |
| **Prop 3.2** | $\rho(q) = 0$ for all $q \notin \mathcal{Q}_{\mathrm{eff}}$ | Proved |
| **Rmk 3.3** | $N_{\mathrm{eff}}(D) \asymp D(\log D)^{-45/46}$ | Proved |
| **Thm 4.1** | Null–sparse decomposition of the BV error sum | Proved |
| **Prop 5.2** | Global BDH + Cauchy–Schwarz → exponent $(46B-45)/92$; falls short for $B=1$ | Proved |
| **Thm 5.5** | Restricted variance + double sparsity → $\theta = 1/2$ with $(\log x)^{-11/23}$ saving | Conditional |

### The Double Sparsity Factor

The central observation is that when the Cauchy–Schwarz inequality is applied *within* the effective moduli $\mathcal{Q}_{\mathrm{eff}}$, both the counting factor and the variance factor carry $N_{\mathrm{eff}}(D)$, producing:

$$[N_{\mathrm{eff}}(D)]^2 \asymp \frac{D^2}{(\log D)^{45/23}}$$

After taking the square root, this contributes $(\log x)^{-45/46}$ — exactly **twice** the logarithmic saving of the global case — comfortably overcoming $(\log x)^{B'/2}$ for $B' \leq 1$.

## Repository Structure

```
Q47-Null-Sparse-Decomposition/
├── README.md
├── LICENSE
├── .gitignore
├── paper/
│   ├── CyclotomicNormForm_Q47.tex       # LaTeX source (7 pages)
│   └── CyclotomicNormForm_Q47.pdf       # Compiled paper
├── data/
│   ├── local_root_structure.csv          # ω(p) for all primes p ≤ 6299
│   ├── effective_moduli_count.csv        # N_eff(D) vs D/(log D)^{45/46}
│   └── cauchy_schwarz_comparison.csv     # Global vs restricted exponents
└── scripts/
    ├── verify_local_roots.py             # Brute-force ω(p) verification
    ├── count_effective_moduli.py          # N_eff(D) computation and fit
    └── verify_double_sparsity.py         # Numerical check of Thm 5.5 exponents
```

## Quick Start

### Verify Local Root Structure (Proposition 2.1)
```bash
python scripts/verify_local_roots.py
```
Brute-force verifies $\omega(p)$ for all primes $p \leq 6299$, confirming the trichotomy: $\omega(47) = 0$, $\omega(p) = 0$ for $p \not\equiv 1 \pmod{47}$, $\omega(p) = 46$ for $p \equiv 1 \pmod{47}$.

### Count Effective Moduli (Remark 3.3)
```bash
python scripts/count_effective_moduli.py
```
Computes $N_{\mathrm{eff}}(D)$ for $D$ up to $10^6$ and fits against the asymptotic $D(\log D)^{-45/46}$.

### Verify Double Sparsity Exponents (Theorem 5.5)
```bash
python scripts/verify_double_sparsity.py
```
Numerically verifies the critical exponents: $(46B - 45)/92 = 1/92 > 0$ (global, fails) vs $(23B' - 45)/46 = -11/23 < 0$ (restricted, succeeds).

## Companion Papers

1. **Titan paper** (algebraic + computational foundations):
   R. Chen, *Prime Values of a Cyclotomic Norm Polynomial and a Conjectural Bounded Gap Phenomenon*, Preprint (2026),
   [Zenodo](https://zenodo.org/records/18521551)

2. **Landau–Siegel paper** (15.4M primes, spectral gap analysis):
   R. Chen, *Experimental Constraints on Landau–Siegel Zeros: A 2-Billion Point Spectral Gap Analysis of Q₄₇*, Preprint (2026),
   [Zenodo](https://zenodo.org/records/18315796)

## Citation

```bibtex
@article{chen2026nullsparse,
  title   = {On the Distribution of the Cyclotomic Norm Form
             {$n^{47}-(n-1)^{47}$} in Arithmetic Progressions},
  author  = {Chen, Ruqing},
  year    = {2026},
  note    = {Preprint, \url{https://github.com/Ruqing1963/Q47-Null-Sparse-Decomposition}}
}
```

## License

MIT License. See [LICENSE](LICENSE) for details.
