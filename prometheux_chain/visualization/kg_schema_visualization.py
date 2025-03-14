import os
from pyvis.network import Network
import networkx as nx
import ipycytoscape
from IPython import get_ipython
from IPython.display import display, HTML
import webbrowser
import matplotlib.pyplot as plt

from prometheux_chain.client.jarvispy_client import JarvisPyClient

"""
Virtual Knowledge Graph Visualization Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


def visualize_kg_schema(vada_file_path: str):
    """
    Visualizes the knowledge graph schema returned by JarvisPyClient.visualize_kg_schema(...).
    """
    try:
        with open(vada_file_path, 'r') as file:
            file_content = file.read()

        # 1. Call the KG schema endpoint (now returning aggregated type-level nodes/edges)
        response = JarvisPyClient.visualize_kg_schema(file_content)

        # 2. Check response
        if response.get('status') == 'success':
            graph_structure = response.get('data')
        else:
            raise Exception(f"KG Schema visualization failed: {response.get('message')}")

        # 3. Transform the data (no complex aggregation needed)
        nodes, edges = __transform_kg_schema_data(graph_structure)

        # 4. Visualize
        if __in_notebook():
            try:
                __visualize_with_cytoscape(nodes, edges)
            except Exception as e:
                print(f"Failed Cytoscape visualization: {e}. Falling back to PyVis.")
                __visualize_with_pyvis(nodes, edges)
        else:
            __visualize_with_pyvis(nodes, edges)

    except IOError as e:
        raise Exception(f"Error opening file {vada_file_path}: {e}")
    except Exception as e:
        raise Exception(f"Error during KG schema visualization: {e}")


def __transform_kg_schema_data(schema_data):
    """
    The backend now returns a single node for each type, e.g.:
    {
      "nodes": [
        { "type": "person", "id": "person" },
        { "type": "bank",   "id": "bank" }
      ],
      "edges": [
        { "type": "loans_to", "source": "bank", "target": "company" },
        ...
      ]
    }
    We just need to turn that into final `nodes` and `edges` lists for visualization.
    """
    raw_nodes = schema_data.get("nodes", [])
    raw_edges = schema_data.get("edges", [])

    # 1) Build a list of node dicts
    # Example node = { "type": "bank", "id": "bank" }
    nodes = []
    node_map = {}  # track unique IDs just in case

    for node in raw_nodes:
        node_id = node["id"]
        node_type = node["type"]
        if node_id not in node_map:
            node_map[node_id] = {
                "id": node_id,
                "type": node_type,
                "label": node_id  # or f"{node_id} ({node_type})" if you prefer
            }
    # 2) Build edges
    # Example edge = { "type": "loans_to", "source": "bank", "target": "company" }
    edges = []
    for edge in raw_edges:
        edge_type = edge["type"]
        source_id = edge["source"]
        target_id = edge["target"]

        # If the source/target doesn't appear in node_map, add a placeholder
        if source_id not in node_map:
            node_map[source_id] = {
                "id": source_id,
                "type": source_id,  # fallback
                "label": source_id
            }
        if target_id not in node_map:
            node_map[target_id] = {
                "id": target_id,
                "type": target_id,  # fallback
                "label": target_id
            }

        edges.append({
            "source": source_id,
            "target": target_id,
            "label": edge_type
        })

    # Convert node_map to a list
    nodes = list(node_map.values())
    return nodes, edges


def __in_notebook():
    """Check if running in a Jupyter notebook."""
    try:
        shell = get_ipython().__class__.__name__
        return shell == 'ZMQInteractiveShell'
    except NameError:
        return False


def __generate_color_palette(node_types):
    """
    Generate a distinct color for each node type using a color palette.
    """
    num_types = len(node_types)
    colormap = plt.get_cmap("tab10")  # Categorical colormap (cycles through 10 distinct colors)
    
    color_dict = {}
    for i, node_type in enumerate(node_types):
        color_dict[node_type] = "#{:02x}{:02x}{:02x}".format(
            int(colormap(i % 10)[0] * 255),
            int(colormap(i % 10)[1] * 255),
            int(colormap(i % 10)[2] * 255)
        )
    return color_dict


def __visualize_with_pyvis(nodes, edges):
    net = Network(notebook=__in_notebook(), directed=True, cdn_resources='in_line')

    node_types = set(node["type"] for node in nodes)
    color_map = __generate_color_palette(node_types)

    # Add nodes
    for node in nodes:
        node_id = node["id"]
        node_type = node["type"]
        node_label = node["label"]
        node_color = color_map.get(node_type, "#CCCCCC")
        net.add_node(node_id, label=node_label, shape='ellipse', color=node_color)

    # Add edges: set a unique 'id' for each so PyVis doesn't collapse them
    for i, edge in enumerate(edges):
        src = edge["source"]
        tgt = edge["target"]
        lbl = edge["label"]

        # Provide a unique ID for each edge
        net.add_edge(
            source=src,
            to=tgt,
            label=lbl,
            title=lbl,
            id=f"edge_{i}"  # unique ID
        )

    output_file = "schema_visualization.html"
    if os.path.exists(output_file):
        os.remove(output_file)
    net.write_html(output_file)

    if __in_notebook():
        with open(output_file, 'r') as f:
            html_content = f.read()
            display(HTML(html_content))
    else:
        webbrowser.open('file://' + os.path.realpath(output_file))


def __visualize_with_cytoscape(nodes, edges):
    """
    Visualizes the graph using Cytoscape, assigning unique colors dynamically
    based on node type, allowing multiple edges between the same source/target.
    """
    # Use MultiDiGraph instead of DiGraph
    G = nx.MultiDiGraph()

    node_types = set(node["type"] for node in nodes)
    color_map = __generate_color_palette(node_types)

    for node in nodes:
        node_id = node["id"]
        node_type = node["type"]
        node_label = node["label"]
        # In a MultiDiGraph, adding the same node_id won't cause collisions
        G.add_node(node_id, label=node_label, node_type=node_type)

    # Now each edge can be added even if source=target is the same
    for edge in edges:
        src = edge["source"]
        tgt = edge["target"]
        lbl = edge["label"]
        # Each distinct edge is stored by NX using a unique edge key
        G.add_edge(src, tgt, label=lbl)

    # Create ipycytoscape widget
    cyto_widget = ipycytoscape.CytoscapeWidget()
    cyto_widget.layout.width = '900px'
    cyto_widget.layout.height = '600px'
    cyto_widget.graph.add_graph_from_networkx(G)

    # Build style_list dynamically
    style_list = []
    for node_type, color in color_map.items():
        style_list.append({
            'selector': f'node[node_type = "{node_type}"]',
            'style': {
                'background-color': color,
                'shape': 'ellipse',
                'label': 'data(label)'
            }
        })

    # Let edges use an unbundled-bezier style so parallel edges are visible
    style_list.append({
        'selector': 'edge',
        'style': {
            'label': 'data(label)',
            'line-color': '#A3C4BC',
            'width': 2,
            'target-arrow-shape': 'triangle',
            'target-arrow-color': '#A3C4BC',
            'curve-style': 'unbundled-bezier',  # or 'bezier'
            'control-point-distances': '40 -40 60',  # Adjust to spread edges
            'control-point-weights': '0.25 0.75 0.5'
        }
    })

    cyto_widget.set_style(style_list)
    cyto_widget.set_layout(name='cose')  # e.g., 'cose', 'dagre', etc.

    display(cyto_widget)
