import sys
import os
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Add current directory to sys.path to allow imports from sibling modules as if they were top-level
# This is necessary because the existing code uses `from globals import ...` style imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from encoder import ProblemInstance
from solverHandler import SolverHandler
from encapsulator import Encapsulator

app = FastAPI()

class SolveRequest(BaseModel):
    N: int
    G: int
    S: int
    R: int
    T: int

# Global lock to prevent concurrent execution of the file-based solver
solver_lock = asyncio.Lock()

@app.post("/api/solve")
async def solve(request: SolveRequest):
    async with solver_lock:
        try:
            # We run the synchronous solver logic in a thread pool to avoid blocking the event loop
            # although with the lock it is effectively serial anyway.
            # But the lock is async, so we should be good.
            # However, the underlying code is blocking and file-based.

            # Since the underlying code relies on specific file paths in 'data/',
            # we must ensure serial execution.

            # N = G * S check
            if request.N != request.G * request.S:
                 raise HTTPException(status_code=400, detail="Number of players (N) must equal Groups (G) * Group Size (S)")

            # We'll run the blocking code in a separate thread
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, run_solver, request)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

def run_solver(request: SolveRequest):
    # This function runs the blocking solver logic
    pi = ProblemInstance(request.N, request.G, request.S, request.R, request.T)
    solver = SolverHandler(pi)
    encapsulator = Encapsulator(solver.RawResult, request.N, request.R, request.G, request.S)
    return {"schedule": encapsulator.FormatedSchedule}

# Mount static files
# We mount it at the root
app.mount("/", StaticFiles(directory="src/wwwroot", html=True), name="static")
