import os
from pyvis.network import Network
import networkx as nx
import ipycytoscape
from IPython import get_ipython
from IPython.display import display, HTML
import webbrowser

from prometheux_chain.client.jarvispy_client import JarvisPyClient


"""
Predicate Graph Visualization Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""

def visualize_predicate_graph(vada_file_path: str):
    """
    Reads a Vadalog file, extracts its content, and sends it to the /api/v1/visualize endpoint.
    Automatically chooses the visualization method based on the environment.
    """
    try:
        with open(vada_file_path, 'r') as file:
            file_content = file.read()

        response = JarvisPyClient.visualize_predicate_graph(file_content)

        if response.get('status') == 'success':
            graph_structure = response.get('data')
        else:
            raise Exception(f"Visualization failed: {response.get('message')}")

        nodes, edges = __transform_schema_data(graph_structure)

        if __in_notebook():
            try:
                __visualize_with_cytoscape(nodes, edges)
            except Exception as e:
                print(f"Failed to visualize with Cytoscape: {e}. Falling back to Pyvis.")
                __visualize_with_pyvis(nodes, edges)
        else:
            __visualize_with_pyvis(nodes, edges)

    except IOError as e:
        raise Exception(f"Error opening file {vada_file_path}: {e}")
    except Exception as e:
        raise Exception(f"Error during schema visualization: {e}")


def __in_notebook():
    """Check if running in a Jupyter notebook."""
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True
        elif shell == 'TerminalInteractiveShell':
            return False
        else:
            return False
    except NameError:
        return False


def __transform_schema_data(schema_data):
    raw_nodes = schema_data.get("nodes", [])
    raw_edges = schema_data.get("edges", [])

    node_map = {}
    for node_item in raw_nodes:
        if isinstance(node_item, dict):
            node_id = node_item.get("id")
            node_type = node_item.get("type", "predicate")
            node_item["label"] = node_id
            node_map[node_id] = node_item
        else:
            node_id = str(node_item)
            node_type = "database" if node_id.endswith(".csv") else "predicate"
            node_map[node_id] = {
                "id": node_id,
                "type": node_type,
                "label": node_id
            }

    final_edges = []
    for edge_item in raw_edges:
        source = edge_item.get("source")
        target = edge_item.get("target")
        label = edge_item.get("label", "")

        if source and source not in node_map:
            node_map[source] = {
                "id": source,
                "type": "database" if source.endswith(".csv") else "rule",
                "label": source
            }
        if target and target not in node_map:
            node_map[target] = {
                "id": target,
                "type": "database" if target.endswith(".csv") else "rule",
                "label": target
            }

        final_edges.append({
            "source": source,
            "target": target,
            "label": label
        })

    final_nodes = list(node_map.values())
    return final_nodes, final_edges


def __visualize_with_pyvis(nodes, edges):
    net = Network(notebook=__in_notebook(), directed=True, cdn_resources='in_line')

    net.toggle_physics(False)
    net.set_options("""
    var options = {
      layout: {
        hierarchical: {
          enabled: true,
          levelSeparation: 100,
          nodeSpacing: 100,
          treeSpacing: 200,
          direction: 'UD',   // up-down
          sortMethod: 'directed'
        }
      }
    }
    """)

    for node in nodes:
        node_id = node['id']
        node_type = node.get('type', 'predicate')
        node_label = node.get('label', node_id)

        if node_type == "database":
            net.add_node(
                node_id,
                label=node_label,
                title=node_type,
                shape='box',
                color='#FF6666'
            )
        elif node_type == "predicate":
            net.add_node(
                node_id,
                label=node_label,
                title=node_type,
                shape='ellipse',
                color='#66B2FF'
            )
        elif node_type == "linear":
            # Same shape (diamond) as 'join' but different color
            net.add_node(
                node_id,
                label=node_label,
                title=node_type,       # "linear"
                shape='diamond',
                color='#FFA500'        # e.g. orange
            )
        elif node_type == "join":
            net.add_node(
                node_id,
                label=node_label,
                title=node_type,       # "join"
                shape='diamond',
                color='#32CD32'        # e.g. limegreen
            )
        else:
            net.add_node(
                node_id,
                label=node_label,
                title=node_type,
                shape='circle',
                color='#CCCCCC'
            )

    # Add edges with label
    for edge in edges:
        net.add_edge(
            edge['source'],
            edge['target'],
            title=edge.get('label', ''),
            label=edge.get('label', '')
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
    G = nx.DiGraph()

    for node in nodes:
        node_id = node['id']
        node_type = node.get('type', 'predicate')
        node_label = node.get('label', node_id)
        G.add_node(node_id, label=node_label, node_type=node_type)

    for edge in edges:
        src = edge['source']
        tgt = edge['target']
        lbl = edge.get('label', '')
        G.add_edge(src, tgt, label=lbl)

    cyto_widget = ipycytoscape.CytoscapeWidget()
    cyto_widget.layout.width = '900px'
    cyto_widget.layout.height = '600px'
    cyto_widget.graph.add_graph_from_networkx(G)

    style_list = [
        {
            'selector': 'node[node_type = "database"]',
            'style': {
                'background-color': '#FF6666',
                'shape': 'hexagon',
                'label': 'data(label)'
            }
        },
        {
            'selector': 'node[node_type = "predicate"]',
            'style': {
                'background-color': '#66B2FF',
                'shape': 'ellipse',
                'label': 'data(label)'
            }
        },
        {
            'selector': 'node[node_type = "linear"]',
            'style': {
                'background-color': '#FFA500',
                'shape': 'diamond',
                'label': 'data(label)'
            }
        },
        {
            'selector': 'node[node_type = "join"]',
            'style': {
                'background-color': '#32CD32',
                'shape': 'diamond',
                'label': 'data(label)'
            }
        },
        {
            'selector': 'edge',
            'style': {
                'label': 'data(label)',
                'line-color': '#A3C4BC',
                'width': 2,
                'target-arrow-shape': 'triangle',
                'target-arrow-color': '#A3C4BC',
                'curve-style': 'bezier'
            }
        }
    ]
    cyto_widget.set_style(style_list)

    # 'breadthfirst' or 'dagre' or 'cose'
    cyto_widget.set_layout(name='dagre')

    display(cyto_widget)