#!/usr/bin/env python3
"""
Count effective moduli and verify the asymptotic N_eff(D) ≍ D/(log D)^{45/46}.

An integer q is an effective modulus if all its prime factors satisfy
p ≡ 1 (mod 47). By the Landau–Ramanujan theorem generalized to primes
in arithmetic progressions (density δ = 1/46), we have:

    N_eff(D) = #{q ≤ D : q ∈ Q_eff} ≍ D / (log D)^{45/46}

This script computes N_eff(D) exactly and fits the constant.

Author: Ruqing Chen
Repository: https://github.com/Ruqing1963/Q47-Null-Sparse-Decomposition
"""

import math
import csv
import os


def sieve_primes(n: int) -> list:
    """Sieve of Eratosthenes up to n."""
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(2, n + 1) if is_prime[i]]


def count_effective_moduli(D: int) -> int:
    """
    Count integers q ∈ [1, D] all of whose prime factors are ≡ 1 (mod 47).

    Uses a sieve: start with all numbers marked as effective,
    then unmark any number divisible by a non-effective prime.
    """
    is_eff = [True] * (D + 1)
    is_eff[0] = False  # 0 is not a positive integer

    primes = sieve_primes(D)
    for p in primes:
        if (p - 1) % 47 != 0:
            # p is NOT an effective prime; remove all its multiples
            for m in range(p, D + 1, p):
                is_eff[m] = False

    return sum(is_eff)


def main():
    print("=" * 65)
    print("  Effective Moduli Count: N_eff(D) vs D/(log D)^{45/46}")
    print("  Q_eff = {q : p|q => p ≡ 1 (mod 47)}")
    print("=" * 65)
    print()

    checkpoints = [
        100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 1000000
    ]

    print(f"{'D':>10}  {'N_eff(D)':>10}  {'D/(logD)^45/46':>16}  "
          f"{'Ratio':>8}  {'D fraction':>12}")
    print("-" * 65)

    results = []
    for D in checkpoints:
        N = count_effective_moduli(D)
        asymp = D / math.log(D) ** (45 / 46)
        ratio = N / asymp if asymp > 0 else 0
        frac = N / D * 100

        print(f"{D:>10,}  {N:>10,}  {asymp:>16,.2f}  "
              f"{ratio:>8.4f}  {frac:>10.4f}%")

        results.append((D, N, asymp, ratio, frac))

    print("-" * 65)

    # Null fraction
    print()
    print("Null moduli fraction (q ∉ Q_eff):")
    for D, N, _, _, frac in results[-3:]:
        null_pct = 100 - frac
        print(f"  D = {D:>10,}: {null_pct:.2f}% of moduli contribute "
              f"zero to BV error")

    # Verify the exponent
    print()
    print("Exponent verification (log-log fit):")
    D1, N1 = results[-2][0], results[-2][1]
    D2, N2 = results[-1][0], results[-1][1]
    if N1 > 0 and N2 > 0:
        # N_eff(D) ~ C * D / (log D)^alpha
        # log(N/D) ~ log(C) - alpha * log(log(D))
        x1 = math.log(math.log(D1))
        x2 = math.log(math.log(D2))
        y1 = math.log(N1 / D1)
        y2 = math.log(N2 / D2)
        alpha_fit = -(y2 - y1) / (x2 - x1)
        print(f"  Fitted exponent alpha = {alpha_fit:.4f}")
        print(f"  Theoretical value     = {45/46:.4f} = 45/46")
        print(f"  Relative error        = {abs(alpha_fit - 45/46)/(45/46)*100:.2f}%")

    # Save CSV
    os.makedirs("data", exist_ok=True)
    with open("data/effective_moduli_count.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["# N_eff(D) = #{q ≤ D : q ∈ Q_eff}"])
        writer.writerow(["D", "N_eff", "Asymptotic_D_over_logD_45_46",
                         "Ratio", "Fraction_percent"])
        for D, N, asymp, ratio, frac in results:
            writer.writerow([D, N, f"{asymp:.2f}", f"{ratio:.4f}",
                           f"{frac:.4f}"])
    print("\n  Results saved to data/effective_moduli_count.csv")


if __name__ == "__main__":
    main()
