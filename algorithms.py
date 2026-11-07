"""Both divide and conquer algorithms + file readers."""
import math, sys
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)   # allow million-digit ints

# ---------------------------------------------------------------- readers
def read_points(path):
    with open(path) as f:
        n = int(f.readline())
        pts = []
        for line in f:
            x, y = line.split()
            pts.append((float(x), float(y)))
    return pts[:n]

def read_numbers(path):
    with open(path) as f:
        return int(f.readline().strip()), int(f.readline().strip())

def detect_type(path):
    """'cp' if first line is n and second line is 'x y'; else 'im'."""
    with open(path) as f:
        f.readline()
        second = f.readline()
    return "cp" if " " in second.strip() else "im"

# ------------------------------------------------------- closest pair (5.4)
def _d2(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

def _brute(P):
    best = (float("inf"), None, None)
    for i in range(len(P)):
        for j in range(i + 1, len(P)):
            d = _d2(P[i], P[j])
            if d < best[0]:
                best = (d, P[i], P[j])
    return best

def closest_pair(points, log=None):
    """Returns (distance, point_a, point_b). points = list of (x, y).
    log(event_dict) is called at each step if given (used by the UI)."""
    if len(points) < 2:
        raise ValueError("need at least 2 points")
    # tag each point with its index so equal points stay distinct
    pts = [(x, y, i) for i, (x, y) in enumerate(points)]
    Px = sorted(pts)                                   # sorted by x
    Py = sorted(pts, key=lambda p: (p[1], p[0], p[2])) # sorted by y

    def rec(Px, Py):
        n = len(Px)
        if n <= 3:                                     # base case
            d, a, b = _brute(Px)
            if log: log({"type": "base", "pts": Px, "pair": (a, b), "d": math.sqrt(d)})
            return d, a, b
        mid = n // 2
        split = Px[mid - 1]
        xline = split[0]
        if log: log({"type": "divide", "pts": Px, "xline": xline})
        Lx, Rx = Px[:mid], Px[mid:]
        Ly = [p for p in Py if p <= split]             # same order as Px
        Ry = [p for p in Py if p > split]
        dl, al, bl = rec(Lx, Ly)
        dr, ar, br = rec(Rx, Ry)
        d, a, b = (dl, al, bl) if dl <= dr else (dr, ar, br)
        # strip: points closer than delta to the dividing line, sorted by y
        strip = [p for p in Py if (p[0] - xline) ** 2 < d]
        d_before = d
        tested = []
        for i in range(len(strip)):
            for j in range(i + 1, min(i + 8, len(strip))):   # only next 7 needed
                if log: tested.append((strip[i][2], strip[j][2]))
                dd = _d2(strip[i], strip[j])
                if dd < d:
                    d, a, b = dd, strip[i], strip[j]
        if log: log({"type": "combine", "pts": Px, "xline": xline,
                     "delta": math.sqrt(d_before), "strip": strip, "tested": tested,
                     "pair": (a, b), "d": math.sqrt(d), "improved": d < d_before})
        return d, a, b

    d, a, b = rec(Px, Py)
    return math.sqrt(d), a[:2], b[:2]

def closest_pair_brute(points):          # only for testing
    d, a, b = _brute(points)
    return math.sqrt(d)

# ---------------------------------------------------------- Karatsuba
_p10 = {}
def _pow10(m):
    if m not in _p10:
        _p10[m] = 10 ** m
    return _p10[m]

def karatsuba(x, y, n, cutoff=64, log=None, depth=0):
    """x, y non-negative ints with at most n digits each."""
    if x == 0 or y == 0 or n <= cutoff:
        r = x * y                         # schoolbook / base case
        if log: log(depth, f"BASE  {x} x {y} = {r}")
        return r
    m = n // 2
    p = _pow10(m)
    xh, xl = divmod(x, p)
    yh, yl = divmod(y, p)
    if log: log(depth, f"SPLIT {x} x {y}  (m={m})\n"
                       f"      xh={xh}  xl={xl}\n      yh={yh}  yl={yl}")
    z2 = karatsuba(xh, yh, n - m, cutoff, log, depth + 1)
    z0 = karatsuba(xl, yl, m, cutoff, log, depth + 1)
    z1 = karatsuba(xh + xl, yh + yl, n - m + 1, cutoff, log, depth + 1) - z2 - z0
    r = z2 * p * p + z1 * p + z0
    if log: log(depth, f"COMBINE z2={z2}, z0={z0}, z1={z1}\n      => {r}")
    return r

def multiply(x, y, cutoff=64, log=None):
    n = max(len(str(x)), len(str(y)))
    return karatsuba(x, y, n, cutoff, log)
