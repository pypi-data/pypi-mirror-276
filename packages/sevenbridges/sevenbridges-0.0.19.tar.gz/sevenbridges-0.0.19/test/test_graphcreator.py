#%%
import numpy as np
import pandas as pd
import pytest
from sevenbridges.graphcreator import graph_generator

# Sample latitude and longitude data
latitude_longitude_data = np.array([
    [40.09068, 116.17355],
    [40.00395, 116.20531],
    [39.91441, 116.18424],
    [39.81513, 116.17115],
    [39.742767, 116.13605],
    [39.987312, 116.28745],
    [39.98205, 116.3974],
    [39.95405, 116.34899],
])

# DataFrame creation
df = pd.DataFrame(latitude_longitude_data, columns=['lat', 'lon'])
df.insert(0, 'node_name', ['node1', 'node2', 'node3', 'node4', 'node5', 'node6', 'node7', 'node8'])

# Test graph generation
def test_graph_generator():
    generator = graph_generator()
    generator.knn(df)
    generator.summary_statistics()

    # Check if graph is created
    assert generator.G is not None, "Graph was not created."
    
    # Check if nodes are correctly added
    assert len(generator.G.nodes) == len(df), "Not all nodes were added to the graph."
    
    # Check adjacency matrix creation
    generator.create_adjacency_matrix()
    assert generator.adjacency_matrix.shape == (len(df), len(df)), "Adjacency matrix shape is incorrect."
    
    # Check some property of the adjacency matrix (e.g., symmetry)
    assert np.array_equal(generator.adjacency_matrix, generator.adjacency_matrix.T), "Adjacency matrix is not symmetric."

# Test plot (optional, since it's visual)
def test_plot():
    generator = graph_generator()
    generator.knn(df)
    generator.plot(show_node_names=True, node_size=500)
    # Visual inspection or automated check for plot generation can be done here if needed.

# Run tests if this file is executed (useful for local testing)
if __name__ == "__main__":
    pytest.main()
