import json
import pandas as pd
import networkx as nx
import ipycytoscape
from pyvis.network import Network
from IPython import get_ipython
from IPython.display import display, HTML
import webbrowser
import os
from time import sleep
from ..client.JarvisClient import JarvisClient
from ..logic.Fact import Fact


def in_notebook():
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


def visualize_chase_explanation_with_pyvis(chase_explanation_json, is_in_notebook):
    chase_explanation = json.loads(chase_explanation_json)

    # Initialize the Pyvis network
    net = Network(notebook=is_in_notebook, directed=True, cdn_resources='in_line')

    # Process each item in the chase explanation JSON
    for item in chase_explanation:
        data = item['data']
        if 'source' in data and 'target' in data:
            net.add_edge(data['source'], data['target'], title=data['label'], label=data['label'])
        else:
            net.add_node(data['id'], label=data['label'], title=data['label'])

    # Limit the physics so nodes don't keep moving after initial rendering
    net.toggle_physics(False)

    # Generate the network visualization
    output_file = os.path.join(os.getcwd(), "chase_explanation.html")
    if os.path.exists(output_file):
        os.remove(output_file)
    net.write_html(output_file)
    sleep(1)

    if os.path.exists(output_file):
        if is_in_notebook:
            # Running in a regular Jupyter notebook
            with open(output_file, 'r') as f:
                html_content = f.read()
                display(HTML(html_content))
        else:
            # Running in a regular Python script
            webbrowser.open('file://' + os.path.realpath(output_file))
    else:
        print("Error: The HTML file was not generated.")


def visualize_chase_explanation_with_cytoscape(chase_explanation_json):
    chase_explanation = json.loads(chase_explanation_json)
    G = nx.DiGraph()

    # Process each item in the chase explanation JSON
    for item in chase_explanation:
        data = item['data']

        if 'source' in data and 'target' in data:
            # This is an edge
            G.add_edge(data['source'], data['target'], label=data['label'])
        else:
            # This is a node
            G.add_node(data['id'], label=data['label'])

    # Create an ipycytoscape widget and load the NetworkX graph into it
    cyto_widget = ipycytoscape.CytoscapeWidget()
    cyto_widget.graph.add_graph_from_networkx(G)

    # Optionally, you can set styles and layout
    cyto_widget.set_style([{
        'selector': 'node',
        'style': {
            'label': 'data(label)',
            'background-color': '#BFD7B5'
        }
    }, {
        'selector': 'edge',
        'style': {
            'label': 'data(label)',
            'line-color': '#A3C4BC',
            'width': 2,
            'target-arrow-shape': 'triangle',
            'target-arrow-color': '#A3C4BC',
            'curve-style': 'bezier'
        }
    }])

    # Set the layout (optional)
    cyto_widget.set_layout(name='dagre')  # Other options: 'cose', 'grid', 'circle', 'breadthfirst', etc.

    # Display the widget
    display(cyto_widget)


'''
    Alternative visualization with cytoscape application for large graphs 
    (directly in cytoscape ide, in jupyter lab only a png can be visualized with this approach)
'''


# def visualize_chase_explanation_with_cytoscape(chase_explanation_json):
#     chase_explanation = json.loads(chase_explanation_json)
#     nodes_data = []
#     edges_data = []

#     # Process each item in the chase explanation JSON
#     for item in chase_explanation:
#         data = item['data']

#         if 'source' in data and 'target' in data:
#             # This is an edge
#             edges_data.append({
#                 'source': data['source'],
#                 'target': data['target'],
#                 'interaction': data['label']
#             })
#         else:
#             # This is a node
#             nodes_data.append({
#                 'id': data['id'],
#                 'label': data['label'],
#                 'type': data.get('type', 'CHASE_NODE')
#             })

#     # Convert lists to DataFrames
#     nodes_df = pd.DataFrame(nodes_data)
#     edges_df = pd.DataFrame(edges_data)

#     # Create the network in Cytoscape from dataframes
#     network_suid = p4c.create_network_from_data_frames(nodes=nodes_df, edges=edges_df, title='Chase Explanation', collection='Chase Explanations')

#     # Set edge arrows to appear with arrows
#     p4c.set_edge_target_arrow_shape_default('ARROW')
#     p4c.set_edge_source_arrow_shape_default('NONE')
#     p4c.set_edge_label_default('DERIVED BY')

#     p4c.notebook_export_show_image()


def aggregate_data(records):
    aggregated = {}
    for record in records:
        start_node = record[0]
        end_node = record[2]
        if start_node not in aggregated:
            aggregated[start_node] = [end_node]
        else:
            aggregated[start_node].append(end_node)
    return aggregated


def process_aggregate_by_start_node(aggregate_by_start_node):
    def replace_skipped_predicates(predicate):
        predicate_name = predicate.split("(")[0]
        # Skip vatoms
        if "vatom_" in predicate_name:
            final_ancestors = set()
            if predicate in aggregate_by_start_node:
                for child_predicate in aggregate_by_start_node[predicate]:
                    final_ancestors.update(replace_skipped_predicates(child_predicate))
            return final_ancestors
        else:
            return {predicate}

    updated_aggregate = {}
    for key, values in aggregate_by_start_node.items():
        if "vatom_" not in key.split("(")[0]:
            new_values = set()
            for value in values:
                new_values.update(replace_skipped_predicates(value))
            updated_aggregate[key] = new_values

    return updated_aggregate


def explain_from_file(root, csv_path):
    df = pd.read_csv(csv_path)
    G = nx.DiGraph()

    ordered_edges = []

    for index, row in df.iterrows():
        node_to = row['Fact']
        node_from_left = row['ProvenanceLeft']
        node_from_right = row['ProvenanceRight']

        G.add_node(node_to, value=node_to)

        G.add_edge(node_to, node_from_left, description=row['Rule'])

        if pd.notna(node_from_right) and node_from_right != '' and node_from_right != 'nan':
            G.add_edge(node_to, node_from_right, description=row['Rule'])

    if root in G:
        for node in nx.bfs_tree(G, source=root):
            connections = list(G.neighbors(node))
            for neighbor in connections:
                ordered_edges.append([node, 'derived by', neighbor])
    else:
        return "Root not found in the graph."

    aggregated_data = aggregate_data(ordered_edges)
    updated_aggregated = process_aggregate_by_start_node(aggregated_data)

    text_representation = f"Structured explanation of the fact {root}: \n\n"
    for start, ends in updated_aggregated.items():
        text_representation += f"Fact {start} derived by:\n"
        for end in ends:
            text_representation += f"  -> {end}\n"

    return text_representation


def explain(structured_fact: Fact = None, fact=None, csv_path=None, attempts=0):
    if fact and csv_path:
        return explain_from_file(fact, csv_path)

    if fact and not csv_path:
        explanation_response = JarvisClient.explain(fact)

    if structured_fact:
        explanation_response = JarvisClient.explain_by_fact(structured_fact)

    if explanation_response.status_code == 429:
        if attempts == 3:
            raise Exception(
                f"HTTP error! status: {explanation_response.status_code}, detail: {explanation_response.json()['message']}")
        print("Attempt " + attempts + ". " + explanation_response.json()['message'] + ". Retrying after 5 seconds")
        sleep(5)
        attempts = attempts + 1
        explain(structured_fact, fact, csv_path, attempts)

    if explanation_response.status_code != 200:
        raise Exception(
            f"HTTP error! status: {explanation_response.status_code}, detail: {explanation_response.json()['message']}")

    if explanation_response.status_code == 200:
        explanation_data = explanation_response.json().get("data")

        textual_explanation = explanation_data.get("textualExplanation", "")

        chase_explanation = explanation_data.get("chaseExplanation", "")
        if chase_explanation:
            # Check if the user is launching the request from python or from jupyter notebook
            is_in_notebook = in_notebook()

            if is_in_notebook:
                try:
                    # Attempt to use ipycytoscape for visualization
                    # p4c.cytoscape_ping()
                    visualize_chase_explanation_with_cytoscape(chase_explanation)
                except Exception as e:
                    # Fall back to Pyvis
                    visualize_chase_explanation_with_pyvis(chase_explanation, is_in_notebook)
            else:
                visualize_chase_explanation_with_pyvis(chase_explanation, is_in_notebook)

        return textual_explanation
