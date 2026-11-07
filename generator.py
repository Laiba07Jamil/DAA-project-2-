"""Generates cp01-cp10 and im01-im10 into ./data  (python generator.py [names...])"""
import random, os, sys
OUT = "datasets"
SEEDS = {f"cp{i:02d}": 1000 + i for i in range(1, 11)}
SEEDS.update({f"im{i:02d}": 2000 + i for i in range(1, 11)})
M = 10 ** 6

def save_points(name, pts, fmt):
    with open(f"{OUT}/{name}.txt", "w") as f:
        f.write(f"{len(pts)}\n")
        f.write("\n".join(fmt % p for p in pts)); f.write("\n")

def save_nums(name, a, b):
    with open(f"{OUT}/{name}.txt", "w") as f:
        f.write(f"{a}\n{b}\n")

def rdigits(rng, n, zero_weight=1):
    if n == 1: return str(rng.randint(1, 9))
    w = [zero_weight] + [1] * 9
    return str(rng.randint(1, 9)) + "".join(rng.choices("0123456789", weights=w, k=n - 1))

def uniform(rng, n, hi=M):
    return [(rng.uniform(0, hi), rng.uniform(0, hi)) for _ in range(n)]

def make(name):
    rng = random.Random(SEEDS[name])
    k = int(name[2:])
    F = "%.4f %.4f"
    if name.startswith("cp"):
        if k <= 4:
            save_points(name, uniform(rng, 10 ** (k + 2)), F)
        elif k == 5:                                   # 10 clusters
            cs = [(rng.uniform(1e5, 9e5), rng.uniform(1e5, 9e5)) for _ in range(10)]
            pts = []
            for _ in range(M):
                cx, cy = rng.choice(cs)
                pts.append((rng.gauss(cx, 5000), rng.gauss(cy, 5000)))
            save_points(name, pts, F)
        elif k == 6:                                   # many duplicates
            save_points(name, [(rng.randint(0, 99), rng.randint(0, 99)) for _ in range(M)], "%d %d")
        elif k == 7:                                   # one vertical line
            save_points(name, [(500000, rng.uniform(0, M)) for _ in range(100000)], F)
        elif k == 8:                                   # 400 x 250 grid, spacing 10
            pts = [(10 * i, 10 * j) for i in range(400) for j in range(250)]
            rng.shuffle(pts)
            save_points(name, pts, "%d %d")
        elif k == 9:                                   # closest pair across the middle
            pts = uniform(rng, M - 2)
            mx = sorted(p[0] for p in pts)[(M - 2) // 2]   # median x = dividing line
            y = rng.uniform(0, M)
            pts += [(mx - 0.0005, y), (mx + 0.0005, y)]
            rng.shuffle(pts)
            save_points(name, pts, F)
        else:                                          # cp10: 101 points
            save_points(name, uniform(rng, 101, 100), F)
    else:
        if k <= 4: save_nums(name, rdigits(rng, 10 ** (k + 2)), rdigits(rng, 10 ** (k + 2)))
        elif k == 5: save_nums(name, rdigits(rng, M), rdigits(rng, 10))
        elif k == 6: save_nums(name, "9" * 100000, rdigits(rng, 100000))
        elif k == 7: save_nums(name, rdigits(rng, 99999, 90), rdigits(rng, 99999, 90))
        elif k == 8: save_nums(name, "1" + "0" * (M - 1), "1" + "0" * (M - 1))
        elif k == 9: save_nums(name, "0", rdigits(rng, M))
        else: save_nums(name, rdigits(rng, 101), rdigits(rng, 101))

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    names = sys.argv[1:] or sorted(SEEDS)
    for n in names:
        make(n); print("wrote", n, "seed", SEEDS[n])
    with open(f"{OUT}/seeds.txt", "w") as f:
        for n in sorted(SEEDS): f.write(f"{n} {SEEDS[n]}\n")
