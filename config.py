import json
import os
from typing import Dict, Any

class Config:
    """Configuration management for the GPU orchestrator"""
    
    # Simulation settings
    SIMULATION_SPEED = 1.0  # Real-time factor
    NUM_GPU_NODES = 8       # Default number of GPU nodes to simulate
    MAX_GPU_TEMPERATURE = 85  # °C - thermal throttling threshold
    MAX_GPU_POWER = 300     # Watts - max power consumption
    
    # API settings
    API_HOST = "0.0.0.0"
    API_PORT = 8000
    DASHBOARD_PORT = 8050
    
    # Scheduler settings
    SCHEDULER_INTERVAL = 5  # seconds between scheduling runs
    MAX_TASK_DURATION = 300  # seconds
    
    # Default GPU node configurations
    GPU_CONFIGS = {
        "A100": {"memory_gb": 40, "tflops": 312, "power_w": 250},
        "V100": {"memory_gb": 32, "tflops": 125, "power_w": 250},
        "RTX4090": {"memory_gb": 24, "tflops": 330, "power_w": 450},
    }
    
    @classmethod
    def load_from_file(cls, config_path: str):
        """Load configuration from JSON file"""
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config_data = json.load(f)
                for key, value in config_data.items():
                    if hasattr(cls, key):
                        setattr(cls, key, value)
    
    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {key: value for key, value in cls.__dict__.items() 
                if not key.startswith('_') and not callable(value)}