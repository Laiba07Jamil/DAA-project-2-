"""FastAPI backend. Run:  uvicorn server:app --reload   then open http://127.0.0.1:8000"""
import os, time
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from algorithms import *

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA, OUT = os.path.join(ROOT, "datasets"), os.path.join(ROOT, "outputs")
os.makedirs(OUT, exist_ok=True)
SMALL_POINTS, SMALL_DIGITS = 300, 300      # <= this -> step-by-step mode
app = FastAPI()

def path_of(name):
    p = os.path.join(DATA, os.path.basename(name) + ".txt")
    if not os.path.isfile(p): raise HTTPException(404, "file not found")
    return p

@app.get("/api/files")
def files():
    out = []
    for f in sorted(os.listdir(DATA)):
        if f.endswith(".txt") and f != "seeds.txt":
            p = os.path.join(DATA, f)
            out.append({"name": f[:-4], "type": detect_type(p), "bytes": os.path.getsize(p)})
    return out

class Req(BaseModel):
    name: str

@app.post("/api/run")                       # plain def -> runs in a worker thread
def run(req: Req):
    p = path_of(req.name)
    if detect_type(p) == "cp":
        pts = read_points(p)
        small = len(pts) <= SMALL_POINTS
        raw = []
        t = time.perf_counter()
        d, a, b = closest_pair(pts, log=raw.append if small else None)
        ms = (time.perf_counter() - t) * 1000
        res = {"type": "cp", "name": req.name, "n": len(pts), "time_ms": ms,
               "distance": d, "a": a, "b": b, "mode": "steps" if small else "summary"}
        if small:
            res["points"] = pts
            res["steps"] = [{**e, "pts": [q[2] for q in e["pts"]],
                             "pair": [e["pair"][0][2], e["pair"][1][2]] if "pair" in e else None,
                             **({"strip": [q[2] for q in e["strip"]]} if "strip" in e else {})}
                            for e in raw]
        return res
    x, y = read_numbers(p)
    n = max(len(str(x)), len(str(y)))
    small = n <= SMALL_DIGITS
    steps = []
    t = time.perf_counter()
    r = multiply(x, y, cutoff=20 if small else 64,
                 log=(lambda d, s: steps.append({"depth": d, "kind": s.split()[0], "text": s})) if small else None)
    ms = (time.perf_counter() - t) * 1000
    s = str(r)
    with open(os.path.join(OUT, req.name + "_product.txt"), "w") as f:
        f.write(s + "\n")
    res = {"type": "im", "name": req.name, "digits": [len(str(x)), len(str(y))], "time_ms": ms,
           "product_digits": len(s), "preview": s if len(s) <= 120 else s[:50] + " ... " + s[-50:],
           "mode": "steps" if small else "summary"}
    if small: res.update(x=str(x), y=str(y), steps=steps, product=s)
    return res

@app.get("/api/product/{name}")
def product(name: str):
    p = os.path.join(OUT, os.path.basename(name) + "_product.txt")
    if not os.path.isfile(p): raise HTTPException(404, "run the file first")
    return FileResponse(p, filename=os.path.basename(p))

app.mount("/", StaticFiles(directory=os.path.join(ROOT, "frontend"), html=True))
