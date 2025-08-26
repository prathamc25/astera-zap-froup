# AI GPU Cluster Orchestrator

A software-defined control plane for intelligent orchestration and telemetry in AI GPU clusters, built with Python and modern web technologies.

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green)
![Dash](https://img.shields.io/badge/Dash-2.14.2-purple)
![SimPy](https://img.shields.io/badge/SimPy-4.1.1-orange)

## Overview

This project implements a simulated environment for managing and orchestrating tasks across a GPU cluster. It features a decoupled architecture with a behavioral model of GPU nodes, an intelligent scheduler that considers telemetry data, and a real-time dashboard for monitoring cluster performance.

## Key Features

- **GPU Grid Simulation**: Behavioral model of a distributed GPU cluster with up to 32 nodes
- **Intelligent Orchestration**: Resource-aware task scheduling based on telemetry data
- **RESTful API**: FastAPI implementation for cluster management
- **Real-time Dashboard**: Interactive visualization of cluster status and performance metrics
- **Modular Architecture**: Clean separation between simulation, control plane, and visualization

## Architecture

The system follows a decoupled architecture:

- **Data Plane**: Simulated GPU nodes with telemetry reporting
- **Control Plane**: Management logic for orchestration and scheduling
- **API Layer**: RESTful interface for interaction
- **Dashboard**: Web-based visualization of cluster state

## Technology Stack

- **Python 3.8+**: Core programming language
- **FastAPI**: Modern, high-performance web framework for building APIs
- **SimPy**: Discrete-event simulation library
- **Dash**: Python framework for building analytical web applications
- **Plotly**: Interactive graphing library
- **Pydantic**: Data validation using Python type annotations

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ai-gpu-orchestrator.git
   cd ai-gpu-orchestrator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

4. Access the components:
   - API: http://localhost:8000
   - Dashboard: http://localhost:8050

## Project Structure

```
ai-gpu-orchestrator/
├── simulation/           # GPU simulation components
│   ├── __init__.py
│   ├── gpu_grid.py      # GPU grid management
│   └── gpu_node.py      # Individual GPU node simulation
├── control_plane/       # Control plane components
│   ├── __init__.py
│   ├── api.py          # FastAPI implementation
│   ├── scheduler.py    # Task scheduling algorithms
│   └── models.py       # Pydantic models
├── dashboard/          # Visualization components
│   ├── __init__.py
│   └── app.py         # Dash application
├── config.py          # Configuration management
├── main.py           # Application entry point
├── requirements.txt   # Python dependencies
└── README.md         # Project documentation
```

## API Documentation

Once the application is running, interactive API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Key Endpoints

- `GET /`: API root with endpoint documentation
- `POST /tasks`: Submit a new task to the cluster
- `GET /tasks`: Get all tasks (queued and running)
- `GET /tasks/{task_id}`: Get a specific task by ID
- `GET /cluster/status`: Get current cluster status
- `GET /nodes`: Get all nodes in the cluster
- `GET /nodes/{node_id}`: Get a specific node by ID
- `POST /scheduler/run`: Manually trigger the scheduler

## Schedulers

### FIFO Scheduler
Basic first-in-first-out task scheduling without considering resource constraints.

### Intelligent Scheduler
Resource-aware scheduling that considers multiple factors:
- GPU temperature (avoids thermal throttling)
- Memory requirements
- Current utilization
- Power consumption

The intelligent scheduler uses a scoring system to select the optimal node for each task.

## Configuration

Modify `config.py` to adjust system parameters:

- Number of GPU nodes to simulate
- Simulation speed and parameters
- API host and port settings
- Scheduler behavior and intervals
- GPU type configurations

## Usage Examples

### Submitting a Task

```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "task_001",
    "duration": 60,
    "memory_required": 16,
    "priority": "high"
  }'
```

### Checking Cluster Status

```bash
curl "http://localhost:8000/cluster/status"
```

### Getting Node Information

```bash
curl "http://localhost:8000/nodes/0"
```

## Troubleshooting

### Dashboard Access Issues

If you cannot access the dashboard at http://localhost:8050:

1. **Check if the server is running**:
   ```bash
   netstat -ano | findstr :8050
   ```

2. **Try a different browser** or clear your browser cache

3. **Check firewall settings** to ensure port 8050 is not blocked

4. **Verify the dashboard process is running**:
   ```bash
   ps aux | grep dash
   ```

### Port Conflicts

If you encounter port conflicts (especially with ports 8000 or 8050):

1. Change the port in `config.py`:
   ```python
   API_PORT = 8001  # Instead of 8000
   DASHBOARD_PORT = 8051  # Instead of 8050
   ```

2. Alternatively, terminate processes using the ports:
   ```bash
   # Find process using port 8000
   lsof -ti:8000 | xargs kill -9
   ```

### Dependency Issues

If you encounter dependency conflicts:

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Contributing

We welcome contributions to this project! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a pull request

Please ensure your code follows PEP 8 style guidelines and includes appropriate tests.

## Future Enhancements

- Support for actual GPU hardware integration
- More sophisticated scheduling algorithms (machine learning-based)
- Advanced telemetry and forecasting capabilities
- Multi-cluster support
- Energy efficiency optimization features
- Authentication and authorization system
- Containerization with Docker

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by research in software-defined infrastructure and GPU cluster management
- Built with amazing open-source tools including FastAPI, SimPy, Dash, and Plotly

## Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Search existing GitHub issues
3. Create a new issue with detailed information about your problem

---

**Note**: This is a simulation environment for research and demonstration purposes. It does not execute actual AI/ML workloads on real GPU hardware.