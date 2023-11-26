import unittest
from app import app  # Replace with the actual name of your module
import json
import networkx as nx

class FlaskTestCase(unittest.TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_generate_graph_missing_json(self):
        response = self.client.post('/generate_graph', data={})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing JSON in request', response.json['error'])

    def setUp(self):
        self.client = app.test_client()
    def test_generate_graph_success(self):
        data = {
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B'), ('B', 'C')],
            'threshold': 2
        }
        response = self.client.post('/generate_graph', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        # Add more assertions here to verify the response data

    def test_generate_graph_missing_nodes(self):
        data = {
            'edges': [('A', 'B'), ('B', 'C')],
            'threshold': 2
        }
        response = self.client.post('/generate_graph', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Nodes or edges are missing', response.json['error'])
        
    def test_generate_graph_missing_edges(self):
        data = {
            'nodes': ['A', 'B', 'C'],
            'threshold': 2
        }
        response = self.client.post('/generate_graph', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Nodes or edges are missing', response.json['error'])
    
    def test_generate_graph_missing_threshold(self):
        data = {
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B'), ('B', 'C')]
        }
        response = self.client.post('/generate_graph', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        # Add more assertions here to verify the response data
    
    # test on big graph
    def test_generate_graph_big_graph(self):
        data = {
            'nodes': ['A', 'B', 'C','D','E','F','G','H','I'],
            'edges': [('A', 'B'), ('B', 'C'),('C','D'),('D','E'),('E','F'),('F','G'),('G','H'),('H','I'),('I','A')],
            'threshold': 2
        }
        response = self.client.post('/generate_graph', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        # Add more assertions here to verify the response data

    # test with nx graph
    def test_generate_graph_nx_graph(self):
        G = nx.Graph()
        G=nx.complete_graph(10)
        data = {
            'nodes': list(G.nodes),
            'edges': list(G.edges),
            'threshold': 15
        }
        response = self.client.post('/generate_graph', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        
        

if __name__ == '__main__':
    unittest.main()
