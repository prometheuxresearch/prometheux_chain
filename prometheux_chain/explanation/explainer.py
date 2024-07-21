import pandas as pd
import networkx as nx
from ..logic.Fact import Fact
from ..client.JarvisClient import JarvisClient
from ..logic.Fact import Fact

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
        
    for row in df.iterrows():
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


def explain(structured_fact : Fact = None, fact=None, csv_path=None, glossary = None):
    if fact and csv_path:
        return explain_from_file(fact,csv_path)
    
    if fact and not csv_path:
        explanation_response = JarvisClient.explain(fact, glossary)
     
    if structured_fact:
        explanation_response = JarvisClient.explain_by_fact(structured_fact, glossary)

    if explanation_response.status_code != 200:
            raise Exception(f"HTTP error! status: {explanation_response.status_code}, detail: {explanation_response.json()['message']}")
    if explanation_response.status_code == 200:
        structured_fact = Fact.from_dict(explanation_response.json()["data"])
    return structured_fact.textual_explanation

    
