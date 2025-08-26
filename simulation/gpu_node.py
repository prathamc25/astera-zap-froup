import simpy
import random
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

class GPUState(Enum):
    IDLE = "idle"
    BUSY = "busy"
    OFFLINE = "offline"
    THROTTLED = "throttled"

@dataclass
class GPUTelemetry:
    temperature: float = 30.0
    power_usage: float = 0.0
    memory_usage: float = 0.0
    utilization: float = 0.0
    state: GPUState = GPUState.IDLE

class GPUNode:
    """Simulates a single GPU node with telemetry and task execution"""
    
    def __init__(self, env: simpy.Environment, node_id: int, gpu_type: str = "A100"):
        self.env = env
        self.node_id = node_id
        self.gpu_type = gpu_type
        self.telemetry = GPUTelemetry()
        self.current_task: Optional[Dict[str, Any]] = None
        self.task_completion_event: Optional[simpy.Event] = None
        
        # Start background processes
        self.telemetry_process = env.process(self._update_telemetry())
    
    def _update_telemetry(self):
        """Continuously update telemetry data based on current state"""
        while True:
            if self.telemetry.state == GPUState.BUSY and self.current_task:
                # Increase temperature and power when busy
                self.telemetry.temperature = min(
                    self.telemetry.temperature + random.uniform(0.5, 2.0),
                    95.0  # Absolute max
                )
                self.telemetry.power_usage = random.uniform(200, 300)
                self.telemetry.utilization = random.uniform(80, 99)
            else:
                # Cool down when idle
                self.telemetry.temperature = max(
                    self.telemetry.temperature - random.uniform(0.1, 0.5),
                    25.0  # Room temperature
                )
                self.telemetry.power_usage = random.uniform(10, 30)
                self.telemetry.utilization = 0.0
                
            # Check for thermal throttling
            if self.telemetry.temperature > 85:
                self.telemetry.state = GPUState.THROTTLED
            elif self.telemetry.state == GPUState.THROTTLED and self.telemetry.temperature < 80:
                self.telemetry.state = GPUState.IDLE
                
            yield self.env.timeout(1)  # Update every simulated second
    
    def execute_task(self, task: Dict[str, Any]) -> simpy.Event:
        """Execute a task on this GPU node"""
        if self.telemetry.state in [GPUState.BUSY, GPUState.THROTTLED]:
            raise ValueError("GPU is not available for task execution")
        
        self.current_task = task
        self.telemetry.state = GPUState.BUSY
        self.task_completion_event = self.env.event()
        
        # Simulate task execution
        task_duration = task.get('duration', 10)
        self.env.process(self._run_task(task_duration))
        
        return self.task_completion_event
    
    def _run_task(self, duration: int):
        """Internal task execution process"""
        try:
            yield self.env.timeout(duration)
            self.current_task = None
            self.telemetry.state = GPUState.IDLE
            if self.task_completion_event:
                self.task_completion_event.succeed({"status": "completed", "node_id": self.node_id})
        except simpy.Interrupt:
            if self.task_completion_event:
                self.task_completion_event.fail({"status": "failed", "node_id": self.node_id})
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of the GPU node"""
        return {
            "node_id": self.node_id,
            "gpu_type": self.gpu_type,
            "state": self.telemetry.state.value,
            "telemetry": {
                "temperature": round(self.telemetry.temperature, 2),
                "power_usage": round(self.telemetry.power_usage, 2),
                "memory_usage": round(self.telemetry.memory_usage, 2),
                "utilization": round(self.telemetry.utilization, 2),
            },
            "current_task": self.current_task,
        }