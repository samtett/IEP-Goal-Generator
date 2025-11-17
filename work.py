import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# Since mermaid service is unavailable, create a Plotly-based flowchart
# Define the nodes and their positions
nodes = [
    # Input Layer
    {"name": "Student Info", "layer": 0, "x": 2, "y": 8, "type": "input"},
    
    # Data Sources Layer (Offline)
    {"name": "BLS Handbook", "layer": 1, "x": 0, "y": 6, "type": "offline"},
    {"name": "Iowa Standards", "layer": 1, "x": 2, "y": 6, "type": "offline"},
    {"name": "IEP Database", "layer": 1, "x": 4, "y": 6, "type": "offline"},
    
    # Processing Layer (Offline)
    {"name": "Text Extract", "layer": 2, "x": 1, "y": 5, "type": "offline"},
    {"name": "Embeddings", "layer": 2, "x": 2, "y": 4, "type": "offline"},
    {"name": "Vector DB", "layer": 2, "x": 3, "y": 3, "type": "offline"},
    
    # RAG Pipeline (Online)
    {"name": "Query Embed", "layer": 3, "x": 1, "y": 2, "type": "online"},
    {"name": "Similarity", "layer": 3, "x": 2, "y": 1.5, "type": "online"},
    {"name": "Context Asm", "layer": 3, "x": 3, "y": 1, "type": "online"},
    
    # Generation Layer (Online)
    {"name": "Prompt Eng", "layer": 4, "x": 2, "y": 0, "type": "online"},
    {"name": "GPT-4", "layer": 4, "x": 2, "y": -1, "type": "online"},
    
    # Output Layer
    {"name": "Measure Goals", "layer": 5, "x": 0, "y": -2.5, "type": "output"},
    {"name": "IEP Goals", "layer": 5, "x": 2, "y": -2.5, "type": "output"},
    {"name": "Standards", "layer": 5, "x": 4, "y": -2.5, "type": "output"},
    
    # Interface
    {"name": "Interface", "layer": 6, "x": 2, "y": -4, "type": "interface"}
]

# Define connections
connections = [
    # Input to query
    (0, 7),  # Student Info -> Query Embed
    
    # Data sources to processing
    (1, 4),  # BLS -> Text Extract
    (2, 4),  # Iowa -> Text Extract  
    (3, 4),  # IEP DB -> Text Extract
    
    # Processing flow
    (4, 5),  # Text Extract -> Embeddings
    (5, 6),  # Embeddings -> Vector DB
    
    # RAG pipeline
    (7, 8),  # Query Embed -> Similarity
    (6, 8),  # Vector DB -> Similarity
    (8, 9),  # Similarity -> Context
    
    # Generation
    (9, 10), # Context -> Prompt
    (10, 11), # Prompt -> GPT-4
    
    # Output
    (11, 12), # GPT-4 -> Measure Goals
    (11, 13), # GPT-4 -> IEP Goals
    (11, 14), # GPT-4 -> Standards
    
    # Interface
    (0, 15),  # Student Info -> Interface
    (12, 15), # Measure Goals -> Interface
    (13, 15), # IEP Goals -> Interface
    (14, 15)  # Standards -> Interface
]

# Create the plot
fig = go.Figure()

# Color mapping
colors = {
    "input": "#1FB8CD",
    "offline": "#B3E5EC", 
    "online": "#A5D6A7",
    "output": "#DB4545",
    "interface": "#D2BA4C"
}

# Add nodes
for i, node in enumerate(nodes):
    fig.add_trace(go.Scatter(
        x=[node["x"]], 
        y=[node["y"]],
        mode='markers+text',
        marker=dict(
            size=50,
            color=colors[node["type"]],
            line=dict(width=2, color='black')
        ),
        text=node["name"],
        textposition="middle center",
        textfont=dict(size=10, color="black"),
        showlegend=False,
        hoverinfo='text',
        hovertext=f"{node['name']}<br>Layer: {node['layer']}<br>Type: {node['type']}"
    ))

# Add connections
for start, end in connections:
    start_node = nodes[start]
    end_node = nodes[end]
    
    fig.add_trace(go.Scatter(
        x=[start_node["x"], end_node["x"]],
        y=[start_node["y"], end_node["y"]],
        mode='lines',
        line=dict(width=2, color='gray'),
        showlegend=False,
        hoverinfo='none'
    ))

# Add arrows (simplified approach using annotations)
for start, end in connections:
    start_node = nodes[start]
    end_node = nodes[end]
    
    # Calculate arrow position (midpoint)
    arrow_x = (start_node["x"] + end_node["x"]) / 2
    arrow_y = (start_node["y"] + end_node["y"]) / 2
    
    # Calculate arrow direction
    dx = end_node["x"] - start_node["x"]
    dy = end_node["y"] - start_node["y"]
    length = np.sqrt(dx**2 + dy**2)
    
    if length > 0:
        # Normalize direction
        dx_norm = dx / length * 0.1
        dy_norm = dy / length * 0.1
        
        fig.add_annotation(
            x=arrow_x + dx_norm,
            y=arrow_y + dy_norm,
            ax=arrow_x - dx_norm,
            ay=arrow_y - dy_norm,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor='gray',
            showarrow=True
        )

# Update layout
fig.update_layout(
    title="RAG System Architecture for IEP Goals",
    showlegend=False,
    xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
    yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
    plot_bgcolor='white',
    font=dict(size=12)
)

# Save the chart
fig.write_image("rag_architecture.png")
fig.write_image("rag_architecture.svg", format="svg")

print("RAG Architecture chart created successfully!")