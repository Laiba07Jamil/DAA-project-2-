Divide and Conquer Visualizer

Two divide and conquer algorithms with a web interface that shows how they work:

Closest pair of points (2-D): O(n log n), as in Kleinberg, Section 5.4
Integer multiplication: Karatsuba, switching to ordinary (schoolbook) multiplication for small numbers

The backend is Python + FastAPI. The frontend is React, served by the same FastAPI server, so there is only one thing to start.

How to run

You need Python 3.9 or newer. You do not need Node or npm. You do need an internet connection when you open the page, because React is loaded from a CDN.

bash
# 1. Install the two dependencies
python -m pip install -r requirements.txt

# 2. Generate all 20 input files into datasets/
python generator.py

# 3. Start the server
python -m uvicorn server:app

Then open http://127.0.0.1:8000 in your browser. Keep the terminal open while you use the page.

On Windows, if python is not found, use py instead (for example py -m uvicorn server:app). Use python -m uvicorn, not plain uvicorn, because plain uvicorn is often not on the PATH.

Using the interface
Pick an input file from the dropdown.
Press Run.
Small files (up to 300 points or digits, such as cp10 and im10) show step by step. Use Previous, Next, Play/Pause or the slider.
Large files show only the final result and the running time. Step-by-step is turned off so the browser does not freeze. Files with millions of items can take 30 seconds or more.
Run all files from the command line (no browser)
bash
python run_all.py

This runs both algorithms on every file in datasets/ and prints a table of results and times.

Project structure
.
├── server.py          # FastAPI backend (API + serves the frontend)
├── algorithms.py      # Closest pair + Karatsuba + file readers
├── generator.py       # Creates all input files (fixed seeds)
├── run_all.py         # Runs every file and prints a results table
├── requirements.txt
├── frontend/
│   └── index.html     # React user interface
└── datasets/          # Input files (cp01-cp10, im01-im10) + seeds.txt
