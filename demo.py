"""
Demo script for STEP Contact Matrix Analyzer

This script demonstrates the capabilities of the STEP contact analyzer
with both synthetic data and real STEP files (if available).
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from step_contact_analyzer import STEPContactAnalyzer, create_demo_analysis
from utils import create_simple_step_example, analyze_contact_matrix_properties
from output_manager import output_manager
import numpy as np
import matplotlib.pyplot as plt


def demo_synthetic_data():
    """
    Demonstrate the analyzer with synthetic contact data
    """
    print("\n" + "="*50)
    print("DEMO 1: Synthetic Contact Data")
    print("="*50)
    
    # Create synthetic data for a mechanical assembly
    part_names = ["Frame", "Motor", "Gearbox", "Output_Shaft", "Coupling", "Load"]
    
    # Define realistic contact relationships
    contact_matrix = np.array([
        [1, 1, 0, 0, 0, 0],  # Frame contacts Motor
        [1, 1, 1, 0, 0, 0],  # Motor contacts Frame and Gearbox
        [0, 1, 1, 1, 0, 0],  # Gearbox contacts Motor and Output_Shaft
        [0, 0, 1, 1, 1, 0],  # Output_Shaft contacts Gearbox and Coupling
        [0, 0, 0, 1, 1, 1],  # Coupling contacts Output_Shaft and Load
        [0, 0, 0, 0, 1, 1]   # Load contacts Coupling
    ])
    
    # Analyze properties
    properties = analyze_contact_matrix_properties(contact_matrix)
    
    print(f"Assembly: {len(part_names)} parts")
    print(f"Parts: {', '.join(part_names)}")
    print(f"Total contacts: {properties['total_contacts']}")
    print(f"Contact density: {properties['contact_density']:.2%}")
    print(f"Average connections per part: {properties['avg_connections']:.1f}")
    
    # Create and visualize graph
    import networkx as nx
    
    G = nx.Graph()
    for i, name in enumerate(part_names):
        G.add_node(i, name=name)
    
    for i in range(len(part_names)):
        for j in range(i + 1, len(part_names)):
            if contact_matrix[i, j] == 1:
                G.add_edge(i, j)
    
    # Visualize
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, k=3, iterations=50, seed=42)
    
    # Draw nodes with different colors based on connectivity
    node_colors = [properties['avg_connections'] + np.sum(contact_matrix[i]) - 1 for i in range(len(part_names))]
    
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                          node_size=2000, alpha=0.8, cmap=plt.cm.viridis)
    nx.draw_networkx_edges(G, pos, edge_color='gray', width=3, alpha=0.6)
    
    labels = {i: name for i, name in enumerate(part_names)}
    nx.draw_networkx_labels(G, pos, labels, font_size=10, font_weight='bold')
    
    plt.title("Mechanical Assembly Contact Graph", fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    
    # Use output manager for save path
    save_path = output_manager.get_graph_path("demo_mechanical_assembly", ensure_unique=False)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
    
    print("Contact matrix:")
    print(contact_matrix)


def demo_step_file_analysis():
    """
    Demonstrate analysis with a real STEP file
    """
    print("\n" + "="*50)
    print("DEMO 2: STEP File Analysis")
    print("="*50)
    
    # First, try to create an example STEP file
    print("Creating example STEP file...")
    if create_simple_step_example():
        # Get the path where the file was created
        step_file = output_manager.step_files_dir / "example_assembly.step"
        
        # Analyze the STEP file
        analyzer = STEPContactAnalyzer(tolerance=1e-2)
        
        print(f"Loading STEP file: {step_file}")
        if analyzer.load_step_file(str(step_file)):
            print(f"Successfully loaded {len(analyzer.parts)} parts")
            
            print("Computing contact matrix...")
            contact_matrix = analyzer.compute_contact_matrix()
            
            print("Analyzing contact properties...")
            properties = analyze_contact_matrix_properties(contact_matrix)
            
            print(f"Analysis results:")
            print(f"  - Total parts: {properties['n_parts']}")
            print(f"  - Total contacts: {properties['total_contacts']}")
            print(f"  - Contact density: {properties['contact_density']:.2%}")
            print(f"  - Max connections: {properties['max_connections']}")
            print(f"  - Isolated parts: {properties['isolated_parts']}")
            
            print("Generating visualization...")
            save_path = output_manager.get_graph_path("step_file_analysis", ensure_unique=False)
            analyzer.visualize_contact_graph(save_path=save_path)
            
            analyzer.print_contact_summary()
        else:
            print("Failed to load STEP file")
    else:
        print("Could not create example STEP file")
        print("This might be due to PythonOCC configuration issues")


def demo_graph_algorithms():
    """
    Demonstrate graph analysis algorithms on contact networks
    """
    print("\n" + "="*50)
    print("DEMO 3: Graph Analysis Algorithms")
    print("="*50)
    
    # Create a more complex assembly
    part_names = ["Base", "Column1", "Column2", "Beam1", "Beam2", "Platform", "Support1", "Support2"]
    
    # Structural framework contact matrix
    contact_matrix = np.array([
        [1, 1, 1, 0, 0, 0, 1, 1],  # Base
        [1, 1, 0, 1, 0, 0, 0, 0],  # Column1
        [1, 0, 1, 0, 1, 0, 0, 0],  # Column2
        [0, 1, 0, 1, 1, 1, 0, 0],  # Beam1
        [0, 0, 1, 1, 1, 1, 0, 0],  # Beam2
        [0, 0, 0, 1, 1, 1, 0, 0],  # Platform
        [1, 0, 0, 0, 0, 0, 1, 0],  # Support1
        [1, 0, 0, 0, 0, 0, 0, 1]   # Support2
    ])
    
    import networkx as nx
    
    # Create graph
    G = nx.Graph()
    for i, name in enumerate(part_names):
        G.add_node(i, name=name)
    
    for i in range(len(part_names)):
        for j in range(i + 1, len(part_names)):
            if contact_matrix[i, j] == 1:
                G.add_edge(i, j)
    
    print("Graph Analysis Results:")
    print(f"Number of nodes: {G.number_of_nodes()}")
    print(f"Number of edges: {G.number_of_edges()}")
    
    # Centrality measures
    degree_centrality = nx.degree_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)
    closeness_centrality = nx.closeness_centrality(G)
    
    print("\nCentrality Analysis (most important parts):")
    
    # Sort by degree centrality
    sorted_by_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)
    print("By degree centrality:")
    for node, centrality in sorted_by_degree[:3]:
        print(f"  {part_names[node]}: {centrality:.3f}")
    
    # Find critical connections (bridges)
    bridges = list(nx.bridges(G))
    print(f"\nCritical connections (bridges): {len(bridges)}")
    for bridge in bridges:
        print(f"  {part_names[bridge[0]]} <-> {part_names[bridge[1]]}")
    
    # Connected components
    components = list(nx.connected_components(G))
    print(f"\nConnected components: {len(components)}")
    
    # Visualize with centrality-based sizing
    plt.figure(figsize=(14, 10))
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    
    # Node sizes based on degree centrality
    node_sizes = [3000 * degree_centrality[node] for node in G.nodes()]
    
    # Draw graph
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, 
                          node_color='lightgreen', alpha=0.8)
    nx.draw_networkx_edges(G, pos, edge_color='blue', width=2, alpha=0.6)
    
    # Highlight bridges in red
    if bridges:
        nx.draw_networkx_edges(G, pos, edgelist=bridges, 
                              edge_color='red', width=4, alpha=0.8)
    
    labels = {i: name for i, name in enumerate(part_names)}
    nx.draw_networkx_labels(G, pos, labels, font_size=9, font_weight='bold')
    
    plt.title("Structural Assembly with Critical Connections", fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    
    save_path = output_manager.get_graph_path("demo_graph_analysis", ensure_unique=False)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def main():
    """
    Run all demos
    """
    print("STEP Contact Matrix Analyzer - Demo Suite")
    print("="*60)
    
    # Initialize output system
    output_manager.clean_old_demo_files()
    
    try:
        # Demo 1: Synthetic data
        demo_synthetic_data()
        
        # Demo 2: STEP file analysis
        demo_step_file_analysis()
        
        # Demo 3: Graph algorithms
        demo_graph_algorithms()
        
        print("\n" + "="*60)
        print("Demo completed successfully!")
        
        # Show output summary
        summary = output_manager.get_summary()
        print(f"\nGenerated files in outputs folder:")
        print(f"  - Graphs: {summary['graphs']} files")
        print(f"  - STEP files: {summary['step_files']} files")
        print(f"  - Matrices: {summary['matrices']} files")
        print(f"  - Total size: {summary['total_size_mb']} MB")
        
        print(f"\nFiles organized in: {output_manager.base_dir}")
        
    except Exception as e:
        print(f"Error during demo: {e}")
        print("This might be due to missing dependencies or configuration issues")


if __name__ == "__main__":
    main()
