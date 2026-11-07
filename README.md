# Divide and Conquer Visualizer

Two divide and conquer algorithms with a web interface that shows how they work:

1. **Closest pair of points (2-D)**: O(n log n), as in Kleinberg, Section 5.4
2. **Integer multiplication**: Karatsuba, switching to ordinary (schoolbook) multiplication for small numbers

The backend is **Python + FastAPI**. The frontend is **React**, served by the same FastAPI server, so there is only one thing to start.

---

## How to run

You need **Python 3.9 or newer**. You do not need Node or npm. You do need an internet connection when you open the page, because React is loaded from a CDN.

```bash
# 1. Install the two dependencies
python -m pip install -r requirements.txt

# 2. Generate all 20 input files into datasets/
python generator.py

# 3. Start the server
python -m uvicorn server:app
```

Then open **http://127.0.0.1:8000** in your browser. Keep the terminal open while you use the page.

> On Windows, if `python` is not found, use `py` instead (for example `py -m uvicorn server:app`).
> Use `python -m uvicorn`, not plain `uvicorn`, because plain `uvicorn` is often not on the PATH.

### Using the interface

1. Pick an input file from the dropdown.
2. Press **Run**.
3. **Small files** (up to 300 points or digits, such as `cp10` and `im10`) show step by step. Use Previous, Next, Play/Pause or the slider.
4. **Large files** show only the final result and the running time. Step-by-step is turned off so the browser does not freeze. Files with millions of items can take 30 seconds or more.

### Run all files from the command line (no browser)

```bash
python run_all.py
```

This runs both algorithms on every file in `datasets/` and prints a table of results and times.

---

## Project structure

```
.
├── server.py          # FastAPI backend (API + serves the frontend)
├── algorithms.py      # Closest pair + Karatsuba + file readers
├── generator.py       # Creates all input files (fixed seeds)
├── run_all.py         # Runs every file and prints a results table
├── requirements.txt
├── frontend/
│   └── index.html     # React user interface
└── datasets/          # Input files (cp01-cp10, im01-im10) + seeds.txt
```

---

The server detects the file type from its content, so any valid file placed in `datasets/` appears in the dropdown automatically.

### Algorithms (`algorithms.py`)

- **`closest_pair(points)`** sorts the points by x and by y, splits at the median x, solves each half recursively, then checks the strip around the dividing line. Each strip point is compared with only the next 7 points (sorted by y). It returns the distance and the two points. Base case: 3 points or fewer, checked by brute force.
- **`multiply(x, y)`** (Karatsuba) splits each number into a high and a low half. It makes 3 recursive multiplications instead of 4 (`z2 = xh*yh`, `z0 = xl*yl`, `z1 = (xh+xl)*(yh+yl) - z2 - z0`) and combines them as `z2*10^2m + z1*10^m + z0`. Below the cutoff it uses ordinary multiplication.

### Frontend (`frontend/index.html`)

- **Closest pair view:** a canvas that shows the dividing line, the strip, the tested pairs and the best pair so far.
- **Karatsuba view:** a recursion tree showing each split, each base case (schoolbook) and each combine.
- **Summary view:** time, input size, result, and a product preview with copy and download buttons.

---

## Input files

Files are plain text. **Closest pair:** the first line is `n`, then one `x y` pair per line. **Multiplication:** two lines, each holding one number in decimal digits.

| File | Content |
|---|---|
| cp01-cp04 | 10^3, 10^4, 10^5, 10^6 uniform random points in [0, 10^6] |
| cp05 | 1,000,000 points clustered around 10 random centers |
| cp06 | 1,000,000 integer points in a small range (many duplicates, closest distance 0) |
| cp07 | 100,000 points on one vertical line |
| cp08 | 100,000 points on an equally spaced grid (many tied closest pairs) |
| cp09 | 1,000,000 points, closest pair placed across the middle dividing line |
| cp10 | 101 points (step-by-step demo) |
| im01-im04 | Random numbers with 10^3, 10^4, 10^5, 10^6 digits |
| im05 | 1,000,000 digits times 10 digits |
| im06 | 100,000 digits, one number is all 9s |
| im07 | 99,999 digits (odd length), many zeros |
| im08 | Both numbers are powers of 10 (1,000,000 digits each) |
| im09 | One number is 0, the other has 1,000,000 digits |
| im10 | 101 digits (step-by-step demo) |

### Seeds

Every file uses its own fixed seed, so `python generator.py` always produces the same files.

- `cp01` to `cp10`: seeds 1001 to 1010
- `im01` to `im10`: seeds 2001 to 2010

The seeds are also saved in `datasets/seeds.txt`.

To regenerate only some files: `python generator.py cp10 im10`

### About the large files

The repository contains only the files smaller than 1 MB (`cp01`, `cp02`, `cp08`, `cp10`, `im01`, `im02`, `im03`, `im06`, `im07`, `im10`). The larger files are not committed. Run `python generator.py` to create them.

---

## Running times

Approximate times on one test machine (yours will differ): about 16 s for 1,000,000 points and about 27 s for 1,000,000-digit multiplication. The full 1,000,000-digit files run, so the 100,000-digit limit is not needed.
