from typing import Dict, List, Optional
from .models import Task, TaskRequest, TaskStatus
from simulation.gpu_grid import GPUGrid
import simpy

class BaseScheduler:
    """Base scheduler class"""
    
    def __init__(self, grid: GPUGrid):
        self.grid = grid
        self.task_queue: List[Task] = []
        self.running_tasks: Dict[str, Task] = {}
    
    def add_task(self, task_request: TaskRequest) -> Task:
        """Add a new task to the scheduler"""
        task = Task(
            task_id=task_request.task_id,
            status=TaskStatus.PENDING,
            request=task_request
        )
        self.task_queue.append(task)
        return task
    
    def schedule(self) -> List[Task]:
        """Schedule tasks from the queue - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement schedule method")
    
    def get_queue_status(self) -> Dict[str, any]:
        """Get current status of the task queue"""
        return {
            "pending_tasks": len(self.task_queue),
            "running_tasks": len(self.running_tasks),
            "queued_tasks": [task.dict() for task in self.task_queue],
            "running_tasks_info": [task.dict() for task in self.running_tasks.values()],
        }

class FIFOScheduler(BaseScheduler):
    """First-In-First-Out scheduler"""
    
    def schedule(self) -> List[Task]:
        """Schedule tasks in FIFO order"""
        scheduled = []
        for task in self.task_queue[:]:
            available_nodes = self.grid.get_available_nodes()
            if available_nodes:
                # Assign to first available node
                node = available_nodes[0]
                try:
                    event = self.grid.execute_task_on_node(node.node_id, task.request.dict())
                    task.assigned_node = node.node_id
                    task.status = TaskStatus.RUNNING
                    self.running_tasks[task.task_id] = task
                    self.task_queue.remove(task)
                    scheduled.append(task)
                except Exception as e:
                    print(f"Failed to schedule task {task.task_id}: {e}")
        return scheduled

class IntelligentScheduler(BaseScheduler):
    """Intelligent scheduler that considers telemetry data"""
    
    def schedule(self) -> List[Task]:
        """Schedule tasks based on telemetry and resource awareness"""
        scheduled = []
        for task in self.task_queue[:]:
            best_node = self._find_optimal_node(task)
            if best_node:
                try:
                    event = self.grid.execute_task_on_node(best_node.node_id, task.request.dict())
                    task.assigned_node = best_node.node_id
                    task.status = TaskStatus.RUNNING
                    self.running_tasks[task.task_id] = task
                    self.task_queue.remove(task)
                    scheduled.append(task)
                except Exception as e:
                    print(f"Failed to schedule task {task.task_id}: {e}")
        return scheduled
    
    def _find_optimal_node(self, task: Task) -> Optional[any]:
        """Find the best node for a task based on telemetry and requirements"""
        available_nodes = self.grid.get_available_nodes()
        if not available_nodes:
            return None
        
        # Score nodes based on multiple factors
        scored_nodes = []
        for node in available_nodes:
            score = self._calculate_node_score(node, task)
            scored_nodes.append((score, node))
        
        # Return node with highest score
        scored_nodes.sort(key=lambda x: x[0], reverse=True)
        return scored_nodes[0][1] if scored_nodes else None
    
    def _calculate_node_score(self, node, task: Task) -> float:
        """Calculate a score for a node based on multiple factors"""
        score = 0.0
        
        # Prefer cooler nodes
        temperature = node.telemetry.temperature
        score += (85 - temperature) / 85 * 0.4  # 40% weight to temperature
        
        # Prefer nodes with appropriate memory
        memory_required = task.request.memory_required
        # This is simplified - in real implementation we'd check actual memory capacity
        score += 0.3  # 30% base score for memory suitability
        
        # Prefer nodes with lower current utilization
        utilization = node.telemetry.utilization
        score += (100 - utilization) / 100 * 0.3  # 30% weight to utilization
        
        return score