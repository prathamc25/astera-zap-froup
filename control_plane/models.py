from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from enum import Enum

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class TaskStatus(str, Enum):
    PENDING = "pending"
    SCHEDULED = "scheduled"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class TaskRequest(BaseModel):
    task_id: str
    duration: int = Field(gt=0, le=300, description="Task duration in seconds")
    memory_required: float = Field(ge=1, le=40, description="Memory required in GB")
    priority: TaskPriority = TaskPriority.MEDIUM
    metadata: Optional[Dict[str, Any]] = None

class Task(BaseModel):
    task_id: str
    status: TaskStatus
    assigned_node: Optional[int] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    request: TaskRequest

class GPUNodeStatus(BaseModel):
    node_id: int
    gpu_type: str
    state: str
    telemetry: Dict[str, float]
    current_task: Optional[Dict[str, Any]] = None

class ClusterStatus(BaseModel):
    timestamp: float
    nodes: List[GPUNodeStatus]
    available_nodes: int
    total_nodes: int
    pending_tasks: int
    running_tasks: int