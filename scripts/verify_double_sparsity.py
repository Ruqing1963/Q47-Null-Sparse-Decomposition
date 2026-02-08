#!/usr/bin/env python3
"""
Verify the double sparsity exponents from Proposition 5.2 and Theorem 5.5.

The paper proves two Cauchy-Schwarz bounds for the sparse part of
the Bombieri-Vinogradov error sum:

  GLOBAL (Prop 5.2):     exponent = (46B - 45)/92
  RESTRICTED (Thm 5.5):  exponent = (23B' - 45)/46

The key insight is that the restricted case doubles the sparsity factor,
making the exponent negative for B' = 1 (standard BDH value), while
the global case yields a positive exponent.

Author: Ruqing Chen
Repository: https://github.com/Ruqing1963/Q47-Null-Sparse-Decomposition
"""

import csv
import os


def global_exponent(B: float) -> float:
    """Exponent from Prop 5.2: (46B - 45) / 92."""
    return (46 * B - 45) / 92


def restricted_exponent(Bp: float) -> float:
    """Exponent from Thm 5.5: (23B' - 45) / 46."""
    return (23 * Bp - 45) / 46


def main():
    print("=" * 70)
    print("  Double Sparsity Factor Verification")
    print("  Global (Prop 5.2) vs Restricted (Thm 5.5)")
    print("=" * 70)
    print()

    # ── Key parameters ──
    delta = 1 / 46  # Dirichlet density of effective primes
    alpha = 1 - delta  # = 45/46, Landau-Ramanujan exponent

    print(f"Effective prime density:  δ = 1/φ(47) = 1/46 ≈ {delta:.6f}")
    print(f"Landau-Ramanujan exponent: 1 - δ = 45/46 ≈ {alpha:.6f}")
    print()

    # ── Critical thresholds ──
    B_crit_global = 45 / 46
    Bp_crit_restricted = 45 / 23

    print("Critical thresholds (exponent = 0):")
    print(f"  Global:     B_crit  = 45/46  ≈ {B_crit_global:.6f}")
    print(f"  Restricted: B'_crit = 45/23  ≈ {Bp_crit_restricted:.6f}")
    print()

    # ── Standard BDH value B = B' = 1 ──
    B_std = 1.0
    exp_global = global_exponent(B_std)
    exp_restricted = restricted_exponent(B_std)

    print(f"Standard BDH value B = B' = 1:")
    print(f"  Global exponent:     (46×1 - 45)/92  = {exp_global:+.6f}"
          f"  {'> 0 ⇒ FAILS' if exp_global > 0 else '< 0 ⇒ SUCCEEDS'}")
    print(f"  Restricted exponent: (23×1 - 45)/46  = {exp_restricted:+.6f}"
          f"  {'> 0 ⇒ FAILS' if exp_restricted > 0 else '< 0 ⇒ SUCCEEDS'}")
    print()

    # ── Verify specific values ──
    print(f"  Global:     1/92       = {1/92:.6f}  ← barely positive")
    print(f"  Restricted: -11/23     = {-11/23:.6f}  ← comfortably negative")
    print(f"  Ratio of savings: (-11/23) / (-45/92) = "
          f"{(-11/23) / (-45/92):.4f}  ← ~2× the saving")
    print()

    # ── Why "double" sparsity ──
    print("Why 'double sparsity':")
    print(f"  Global:     1 factor of N_eff → (log x)^{{-45/92}} saving")
    print(f"  Restricted: 2 factors of N_eff → (log x)^{{-45/46}} saving")
    print(f"  Ratio: (45/46) / (45/92) = 2.00 ← exactly double")
    print()

    # ── Table: exponents for various B values ──
    print(f"{'B':>6}  {'Global':>12}  {'Status':>8}  {'Restricted':>12}  {'Status':>8}")
    print("-" * 52)

    results = []
    B_values = [0.5, 0.8, 0.9, 45/46, 0.98, 1.0, 1.5, 45/23]

    for B in B_values:
        eg = global_exponent(B)
        er = restricted_exponent(B)
        sg = "θ=1/2" if eg < 0 else "FAILS"
        sr = "θ=1/2" if er < 0 else "FAILS"

        B_label = f"{B:.4f}"
        if abs(B - 45/46) < 1e-6:
            B_label = "45/46"
        elif abs(B - 45/23) < 1e-6:
            B_label = "45/23"

        print(f"{B_label:>6}  {eg:>+12.6f}  {sg:>8}  {er:>+12.6f}  {sr:>8}")
        results.append((B_label, eg, sg, er, sr))

    print("-" * 52)
    print()
    print("Conclusion: The restricted variance hypothesis (Thm 5.5)")
    print("achieves θ = 1/2 for all B' < 45/23 ≈ 1.957, while the")
    print("global hypothesis (Prop 5.2) requires B < 45/46 ≈ 0.978.")
    print("At the standard BDH value B = 1, only the restricted")
    print("version succeeds, thanks to the double sparsity factor.")

    # Save CSV
    os.makedirs("data", exist_ok=True)
    with open("data/cauchy_schwarz_comparison.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["# Cauchy-Schwarz exponent comparison"])
        writer.writerow(["# Global (Prop 5.2): (46B-45)/92"])
        writer.writerow(["# Restricted (Thm 5.5): (23B'-45)/46"])
        writer.writerow(["B", "Global_Exponent", "Global_Status",
                         "Restricted_Exponent", "Restricted_Status"])
        for B_label, eg, sg, er, sr in results:
            writer.writerow([B_label, f"{eg:+.6f}", sg, f"{er:+.6f}", sr])
    print("\n  Results saved to data/cauchy_schwarz_comparison.csv")


if __name__ == "__main__":
    main()
