#!/usr/bin/env python3
"""
Verify Proposition 2.1 (Local Root Structure) by brute force.

For Q(n) = n^47 - (n-1)^47, computes omega(p) for all primes p up to
a given bound and checks the trichotomy:
  (a) omega(47) = 0
  (b) omega(p) = 0 if p ≠ 47 and p ≢ 1 (mod 47)
  (c) omega(p) = 46 if p ≡ 1 (mod 47)

Also verifies Q(n) ≡ 1 (mod 47) for all residue classes.

Author: Ruqing Chen
Repository: https://github.com/Ruqing1963/Q47-Null-Sparse-Decomposition
"""

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


def omega_brute(p: int) -> int:
    """Brute-force: count n in [0, p-1] with Q(n) ≡ 0 (mod p)."""
    count = 0
    for n in range(p):
        q = (pow(n, 47, p) - pow((n - 1) % p, 47, p)) % p
        if q == 0:
            count += 1
    return count


def omega_theory(p: int) -> int:
    """Theoretical omega from Proposition 2.1."""
    if p == 47:
        return 0
    elif (p - 1) % 47 == 0:
        return 46
    else:
        return 0


def classify(p: int) -> str:
    """Classify a prime by its type."""
    if p == 47:
        return "ramified"
    elif (p - 1) % 47 == 0:
        return "splitting"
    else:
        return "inert"


def verify_mod47():
    """Verify Q(n) ≡ 1 (mod 47) for all 47 residue classes."""
    print("Verifying Q(n) ≡ 1 (mod 47) for all residue classes...")
    for n in range(47):
        q_mod = (pow(n, 47, 47) - pow((n - 1) % 47, 47, 47)) % 47
        if q_mod != 1:
            print(f"  FAIL at n ≡ {n} (mod 47): Q(n) ≡ {q_mod}")
            return False
    print("  [PASS] Q(n) ≡ 1 (mod 47) for all 47 residue classes")
    return True


def main():
    P_MAX = 6299

    print("=" * 60)
    print("  Proposition 2.1 — Local Root Structure Verification")
    print(f"  Q(n) = n^47 - (n-1)^47, all primes p ≤ {P_MAX}")
    print("=" * 60)
    print()

    verify_mod47()
    print()

    primes = sieve_primes(P_MAX)
    print(f"Testing {len(primes)} primes up to {P_MAX}...")
    print(f"{'p':>6}  {'type':>10}  {'theory':>7}  {'brute':>6}  {'match':>6}")
    print("-" * 45)

    all_ok = True
    results = []
    n_inert = 0
    n_split = 0
    n_ramif = 0

    for p in primes:
        brute = omega_brute(p)
        theory = omega_theory(p)
        ptype = classify(p)
        ok = brute == theory

        if ptype == "inert":
            n_inert += 1
        elif ptype == "splitting":
            n_split += 1
        else:
            n_ramif += 1

        results.append((p, ptype, theory, brute, ok))

        if not ok:
            all_ok = False
            print(f"{p:>6}  {ptype:>10}  {theory:>7}  {brute:>6}  {'FAIL':>6}")
        elif ptype != "inert":
            # Print all non-inert primes (splitting + ramified)
            print(f"{p:>6}  {ptype:>10}  {theory:>7}  {brute:>6}  {'OK':>6}")

    print("-" * 45)
    print(f"  Inert primes (ω=0):     {n_inert}")
    print(f"  Splitting primes (ω=46): {n_split}")
    print(f"  Ramified (p=47, ω=0):    {n_ramif}")
    print(f"  Total:                   {len(primes)}")
    print()

    status = "ALL PASS" if all_ok else "SOME FAILED"
    print(f"  [{status}] Proposition 2.1 verified for all primes ≤ {P_MAX}")

    # Save CSV
    os.makedirs("data", exist_ok=True)
    with open("data/local_root_structure.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["# omega(p) for Q(n) = n^47 - (n-1)^47"])
        writer.writerow(["Prime_p", "Type", "omega_theory", "omega_brute", "Match"])
        for p, ptype, theory, brute, ok in results:
            if ptype != "inert" or p <= 53:
                writer.writerow([p, ptype, theory, brute, ok])
    print("  Results saved to data/local_root_structure.csv")


if __name__ == "__main__":
    main()
