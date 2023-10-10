from flask import Flask, request, jsonify
from flask_cors import CORS
import networkx as nx
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type"]}}, supports_credentials=True)



@app.route('/generate_graph', methods=['POST'])
def generate_graph():
    if not request.is_json:
        app.logger.error('Missing JSON in request')
        return jsonify({'error': 'Missing JSON in request'}), 400

    data = request.get_json()

    nodes = data.get('nodes', [])
    edges = data.get('edges', [])
    if not nodes or not edges:
        app.logger.error('Nodes or edges are missing')
        return jsonify({'error': 'Nodes or edges are missing'}), 400

    app.logger.info('Received request with nodes: %s and edges: %s', nodes, edges)

    G = create_graph_from_data(nodes, edges)

    try:
        result = compute(G)
        return jsonify(result)
    except ValueError as e:
        app.logger.error('Error computing graph: %s', str(e))
        return jsonify({'error': str(e)}), 400

# defaul route
@app.route('/')
def index():
    return 'Hello World!'


def create_graph_from_data(nodes, edges):
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    return G

def compute(G):
    k = 1
    while True:
        coloring = defective_coloring(G, k)
        if coloring:
            return {"num_colors": k, "coloring": coloring}
        k += 1


def defective_coloring(G, k):
    colors = {} 
    for node in G.nodes():
        available_colors = set(range(k))
        for neighbor in G.neighbors(node):
            if neighbor in colors:
                available_colors.discard(colors[neighbor])
        
        if not available_colors:
            return None  # No available colors
        
        chosen_color = min(available_colors)
        neighbor_count_same_color = sum(1 for neighbor in G.neighbors(node) if colors.get(neighbor) == chosen_color)
        
        if neighbor_count_same_color > k:
            return None  # Violates the (k, d)-coloring
        
        colors[node] = chosen_color
        
    return colors





if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
