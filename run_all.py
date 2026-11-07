"""Part 3: apply both algorithms to every file in ./data, print a results table."""
import os, time
from algorithms import *
print(f"{'file':8}{'size':>10}  {'result':45}{'time(s)':>9}")
for f in sorted(os.listdir("datasets")):
    if not f.endswith(".txt") or f == "seeds.txt": continue
    p = os.path.join("datasets", f)
    if detect_type(p) == "cp":
        pts = read_points(p); t = time.perf_counter(); d, a, b = closest_pair(pts)
        res, n = f"dist = {d:.6f}", len(pts)
    else:
        x, y = read_numbers(p); t = time.perf_counter(); r = multiply(x, y)
        res, n = f"product has {len(str(r))} digits", len(str(max(x, y)))
    print(f"{f[:-4]:8}{n:>10}  {res:45}{time.perf_counter() - t:>9.2f}", flush=True)
