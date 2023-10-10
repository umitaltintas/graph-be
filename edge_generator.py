import random
import string

def generate_random_nodes(count):
    """
    Generate a random set of node labels with the specified count.

    Parameters:
    - count: Number of nodes to generate

    Returns:
    - List of node labels
    """
    all_possible_nodes = [a + b for a in string.ascii_lowercase for b in string.ascii_lowercase]
    if count > len(all_possible_nodes):
        raise ValueError(f"Can only generate up to {len(all_possible_nodes)} unique node labels")
    return random.sample(all_possible_nodes, count)

def generate_random_graph(node_count, num_edges):
    """
    Generate a random graph with a specified number of nodes and edges.

    Parameters:
    - node_count: Number of nodes to generate
    - num_edges: Number of edges to generate

    Returns:
    - nodes: List of node labels
    - edges: List of edges as tuples
    """
    nodes = generate_random_nodes(node_count)
    
    if num_edges > len(nodes) * (len(nodes) - 1) // 2:
        raise ValueError("Too many edges requested for the number of nodes")

    edges = set()
    while len(edges) < num_edges:
        # Randomly select two distinct nodes
        node1, node2 = random.sample(nodes, 2)
        
        # Ensure we haven't already added this edge
        edge = tuple(sorted([node1, node2]))
        if edge not in edges:
            edges.add(edge)
            
    return nodes, list(edges)

# Node count and number of edges
node_count = 30
num_edges = 150

# Generate the graph
nodes, edges = generate_random_graph(node_count, num_edges)

# Convert nodes and edges to specified format
formatted_nodes = ", ".join(nodes)
formatted_edges = ", ".join([f"{edge[0]}-{edge[1]}" for edge in edges])

print(f"nodes: {formatted_nodes}")
print(f"edges: {formatted_edges}")
