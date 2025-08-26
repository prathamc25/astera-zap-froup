import simpy
import random
from typing import Dict, List, Any, Optional
from .gpu_node import GPUNode, GPUState

class GPUGrid:
    """Simulates a grid of GPU nodes"""
    
    def __init__(self, env: simpy.Environment, num_nodes: int = 8):
        self.env = env
        self.nodes: List[GPUNode] = []
        self._initialize_nodes(num_nodes)
    
    def _initialize_nodes(self, num_nodes: int):
        """Initialize GPU nodes with different types"""
        gpu_types = ["A100", "V100", "RTX4090"]
        for i in range(num_nodes):
            gpu_type = random.choice(gpu_types)
            node = GPUNode(self.env, i, gpu_type)
            self.nodes.append(node)
    
    def get_available_nodes(self) -> List[GPUNode]:
        """Get list of available nodes that can accept tasks"""
        return [node for node in self.nodes 
                if node.telemetry.state in [GPUState.IDLE]]
    
    def get_node_by_id(self, node_id: int) -> Optional[GPUNode]:
        """Get a specific node by its ID"""
        if 0 <= node_id < len(self.nodes):
            return self.nodes[node_id]
        return None
    
    def get_grid_status(self) -> Dict[str, Any]:
        """Get status of all nodes in the grid"""
        return {
            "timestamp": self.env.now,
            "nodes": [node.get_status() for node in self.nodes],
            "available_nodes": len(self.get_available_nodes()),
            "total_nodes": len(self.nodes)
        }
    
    def execute_task_on_node(self, node_id: int, task: Dict[str, Any]) -> Any:
        """Execute a task on a specific node"""
        node = self.get_node_by_id(node_id)
        if node:
            return node.execute_task(task)
        raise ValueError(f"Node {node_id} not found")