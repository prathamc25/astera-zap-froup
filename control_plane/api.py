from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
import simpy
import json

from .models import TaskRequest, Task, ClusterStatus
from .scheduler import IntelligentScheduler, FIFOScheduler
from simulation.gpu_grid import GPUGrid

app = FastAPI(title="AI GPU Cluster Control Plane API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
env = simpy.Environment()
grid = GPUGrid(env, num_nodes=8)
scheduler = IntelligentScheduler(grid)

@app.on_event("startup")
async def startup_event():
    """Start the simulation environment when the app starts"""
    # Start the simulation in the background
    import threading
    def run_simulation():
        while True:
            env.run(until=env.now + 10)  # Run in 10-second increments
    
    thread = threading.Thread(target=run_simulation, daemon=True)
    thread.start()

@app.post("/tasks", response_model=Task)
async def submit_task(task_request: TaskRequest):
    """Submit a new task to the cluster"""
    try:
        task = scheduler.add_task(task_request)
        return task
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    """Get all tasks (queued and running)"""
    all_tasks = scheduler.task_queue + list(scheduler.running_tasks.values())
    return all_tasks

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str):
    """Get a specific task by ID"""
    for task in scheduler.task_queue:
        if task.task_id == task_id:
            return task
    if task_id in scheduler.running_tasks:
        return scheduler.running_tasks[task_id]
    raise HTTPException(status_code=404, detail="Task not found")

@app.get("/cluster/status", response_model=ClusterStatus)
async def get_cluster_status():
    """Get current cluster status"""
    grid_status = grid.get_grid_status()
    
    return ClusterStatus(
        timestamp=grid_status["timestamp"],
        nodes=grid_status["nodes"],
        available_nodes=grid_status["available_nodes"],
        total_nodes=grid_status["total_nodes"],
        pending_tasks=len(scheduler.task_queue),
        running_tasks=len(scheduler.running_tasks)
    )

@app.get("/nodes", response_model=List[Dict[str, Any]])
async def get_nodes():
    """Get all nodes in the cluster"""
    return grid.get_grid_status()["nodes"]

@app.get("/nodes/{node_id}", response_model=Dict[str, Any])
async def get_node(node_id: int):
    """Get a specific node by ID"""
    node = grid.get_node_by_id(node_id)
    if node:
        return node.get_status()
    raise HTTPException(status_code=404, detail="Node not found")

@app.post("/scheduler/run")
async def run_scheduler():
    """Manually trigger the scheduler"""
    try:
        scheduled = scheduler.schedule()
        return {"scheduled_tasks": len(scheduled), "tasks": scheduled}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "AI GPU Cluster Control Plane API",
        "version": "1.0.0",
        "endpoints": {
            "submit_task": "POST /tasks",
            "get_tasks": "GET /tasks",
            "get_cluster_status": "GET /cluster/status",
            "get_nodes": "GET /nodes",
            "run_scheduler": "POST /scheduler/run"
        }
    }
