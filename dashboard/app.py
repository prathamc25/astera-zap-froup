import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import requests
import time
from threading import Thread
import pandas as pd

# API base URL
API_BASE = "http://localhost:8000"

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "AI GPU Cluster Dashboard"

# Layout
app.layout = html.Div([
    html.H1("AI GPU Cluster Orchestrator Dashboard"),
    
    dcc.Interval(
        id='interval-component',
        interval=2*1000,  # Update every 2 seconds
        n_intervals=0
    ),
    
    html.Div([
        html.Div([
            html.H3("Cluster Overview"),
            html.Div(id="cluster-stats")
        ], className="four columns"),
        
        html.Div([
            html.H3("Temperature Monitoring"),
            dcc.Graph(id='temperature-graph')
        ], className="eight columns"),
    ], className="row"),
    
    html.Div([
        html.Div([
            html.H3("GPU Utilization"),
            dcc.Graph(id='utilization-graph')
        ], className="six columns"),
        
        html.Div([
            html.H3("Power Consumption"),
            dcc.Graph(id='power-graph')
        ], className="six columns"),
    ], className="row"),
    
    html.Div([
        html.H3("Task Queue"),
        html.Div(id="task-queue")
    ])
])

# Callbacks
@app.callback(
    [Output('cluster-stats', 'children'),
     Output('temperature-graph', 'figure'),
     Output('utilization-graph', 'figure'),
     Output('power-graph', 'figure'),
     Output('task-queue', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_dashboard(n):
    try:
        # Get cluster status
        response = requests.get(f"{API_BASE}/cluster/status")
        cluster_status = response.json()
        
        # Get tasks
        response = requests.get(f"{API_BASE}/tasks")
        tasks = response.json()
        
        # Cluster stats
        stats = html.Div([
            html.P(f"Total Nodes: {cluster_status['total_nodes']}"),
            html.P(f"Available Nodes: {cluster_status['available_nodes']}"),
            html.P(f"Pending Tasks: {cluster_status['pending_tasks']}"),
            html.P(f"Running Tasks: {cluster_status['running_tasks']}"),
        ])
        
        # Prepare data for graphs
        nodes = cluster_status['nodes']
        node_ids = [f"Node {node['node_id']}" for node in nodes]
        temperatures = [node['telemetry']['temperature'] for node in nodes]
        utilizations = [node['telemetry']['utilization'] for node in nodes]
        power_usage = [node['telemetry']['power_usage'] for node in nodes]
        states = [node['state'] for node in nodes]
        
        # Temperature graph
        temp_fig = go.Figure(
            data=[go.Bar(x=node_ids, y=temperatures, 
                         marker_color=['red' if temp > 80 else 'orange' if temp > 70 else 'green' 
                                       for temp in temperatures])],
            layout=go.Layout(title="GPU Temperatures (°C)")
        )
        temp_fig.add_hline(y=85, line_dash="dash", line_color="red", annotation_text="Danger Zone")
        temp_fig.add_hline(y=70, line_dash="dash", line_color="orange", annotation_text="Warning Zone")
        
        # Utilization graph
        util_fig = go.Figure(
            data=[go.Bar(x=node_ids, y=utilizations,
                        marker_color=['green' if util > 0 else 'blue' for util in utilizations])],
            layout=go.Layout(title="GPU Utilization (%)")
        )
        
        # Power graph
        power_fig = go.Figure(
            data=[go.Bar(x=node_ids, y=power_usage)],
            layout=go.Layout(title="Power Consumption (W)")
        )
        
        # Task queue
        task_list = html.Ul([
            html.Li(f"{task['task_id']} - {task['status']} - "
                   f"Node: {task.get('assigned_node', 'N/A')}")
            for task in tasks
        ])
        
        return stats, temp_fig, util_fig, power_fig, task_list
        
    except Exception as e:
        return html.Div(f"Error: {str(e)}"), {}, {}, {}, html.Div()

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)