import uvicorn
import threading
from control_plane.api import app
from dashboard.app import app as dash_app
from simulation.gpu_grid import GPUGrid
import simpy
from control_plane.scheduler import IntelligentScheduler
import time

def run_simulation():
    """Run the simulation in a separate thread"""
    env = simpy.Environment()
    grid = GPUGrid(env, num_nodes=8)
    scheduler = IntelligentScheduler(grid)
    
    # Store in global context if needed, or use a shared state solution
    print("Simulation started...")
    while True:
        env.run(until=env.now + 10)
        scheduler.schedule()
        time.sleep(1)  # Real-time throttle

if __name__ == "__main__":
    # Start simulation thread
    sim_thread = threading.Thread(target=run_simulation, daemon=True)
    sim_thread.start()
    
    # Start API server
    print("Starting API server on http://localhost:8000")
    print("Starting Dashboard on http://localhost:8050")
    
    # Run FastAPI app
    uvicorn.run(app, host="0.0.0.0", port=8000)