
from collections import defaultdict
import operator
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
    version = int(data.get('version', 1))
    threshold = int(data.get('threshold', 2))
    if not nodes or not edges:
        app.logger.error('Nodes or edges are missing')
        return jsonify({'error': 'Nodes or edges are missing'}), 400

    app.logger.info('Received request with nodes: %s and edges: %s', nodes, edges)

    G = create_graph_from_data(nodes, edges)

    try:
        result = compute(G,version,threshold)
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

def compute(G,version,threshold=2):

    if version == 1:
        coloring = basic_alg(G, threshold)
    elif version == 2:
        coloring = defective_coloring_v2(G, threshold)
    elif version == 3:
        coloring = MDIC(G, threshold)
    else:
        raise ValueError('Invalid version: {}'.format(version))
    
    # return coloring and number of colors used
    num_colors = max(coloring.values()) + 1
    if coloring:
        return {"num_colors": num_colors, "coloring": coloring}
        k += 1



def basic_alg(graph, threshold=2):
    # Initialize all nodes with the same color (e.g., color 0)
    colors = defaultdict(lambda: 0)

    # Create a defect number map for nodes
    defect_map = {node: len(list(graph.neighbors(node))) for node in graph.nodes()}

    # Initialize variable for the max defect value
    max_defect = max(defect_map.values())

    # Continue until no node's defect number exceeds the threshold
    while max_defect > threshold:
        # Find the node with the highest defect number
        node = max(defect_map, key=defect_map.get)

        # Previous color of the node
        old_color = colors[node]

        # Recolor the node
        colors[node] += 1
        new_color = colors[node]

        # Adjust the defect number for the recolored node
        defect_map[node] = sum(1 for neighbor in graph.neighbors(node) if colors[neighbor] == new_color)

        # Adjust the defect number for the neighbors
        for neighbor in graph.neighbors(node):
            if colors[neighbor] == old_color:
                defect_map[neighbor] -= 1  # Decrease if the color was the same as the old color
            elif colors[neighbor] == new_color:
                defect_map[neighbor] += 1  # Increase if the color is the same as the new color

        # Recalculate the max defect value
        max_defect = max(defect_map.values())

    return dict(colors)  # Convert defaultdict back to regular dict for output






def defective_coloring_v2(graph, threshold=2):
    # Initialize all nodes with the same color (e.g., color 0)
    colors = defaultdict(lambda: 0)

    # Create a defect number map for nodes
    defect_map = {node: len(list(graph.neighbors(node))) for node in graph.nodes()}

    # Initialize variable for the max defect value
    max_defect = max(defect_map.values())

    # Continue until no node's defect number exceeds the threshold
    color=0
    while max_defect > threshold:
        # Find the node with the highest defect number
        node = max(defect_map, key=defect_map.get)

        # Previous color of the node
        old_color = colors[node]

        # Recolor the node with +1 of max neighbor color if min neighbor color is 0
        colors[node] = max([colors[neighbor] for neighbor in graph.neighbors(node)])+1 if min([colors[neighbor] for neighbor in graph.neighbors(node)])==0 else min([colors[neighbor] for neighbor in graph.neighbors(node)])-1
        color += 1
        new_color = colors[node]

        # Adjust the defect number for the recolored node
        defect_map[node] = sum(1 for neighbor in graph.neighbors(node) if colors[neighbor] == new_color)

        # Adjust the defect number for the neighbors
        for neighbor in graph.neighbors(node):
            if colors[neighbor] == old_color:
                defect_map[neighbor] -= 1  # Decrease if the color was the same as the old color
            elif colors[neighbor] == new_color:
                defect_map[neighbor] += 1  # Increase if the color is the same as the new color

        # Recalculate the max defect value
        max_defect = max(defect_map.values())

    return dict(colors)  # Convert defaultdict back to regular dict for output





def get_smallest_available_color(bitmap):
    for color in range(len(bitmap)):
        if not bitmap[color]:
            return color
    return len(bitmap)

def MDIC(graph, threshold=2):
    colors = defaultdict(lambda: 0)
    bitmaps = {node: [False] * len(graph.nodes()) for node in graph.nodes()}
    defect_map = {node: len(list(graph.neighbors(node))) for node in graph.nodes()}
    max_defect = max(defect_map.values())

    while max_defect > threshold:
        node = max(defect_map, key=defect_map.get)
        old_color = colors[node]

        # Find smallest available color
        new_color = get_smallest_available_color(bitmaps[node])
        colors[node] = new_color

        # Update bitmap for the node and its neighbors
        bitmaps[node][new_color] = True
        for neighbor in graph.neighbors(node):
            bitmaps[neighbor][new_color] = True

            if colors[neighbor] == old_color:
                defect_map[neighbor] -= 1
            elif colors[neighbor] == new_color:
                defect_map[neighbor] += 1

        defect_map[node] = sum(1 for neighbor in graph.neighbors(node) if colors[neighbor] == new_color)
        max_defect = max(defect_map.values())

    return dict(colors)







if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
