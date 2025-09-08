"""
STEP Contact Matrix Application

This application analyzes STEP files to create contact matrices showing which parts
touch or are connected to each other, and visualizes the results as a graph using NetworkX.
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
import logging
from typing import List, Dict, Tuple, Optional

# PythonOCC imports
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_SOLID
from OCC.Core.BRepExtrema import BRepExtrema_DistShapeShape
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Core.TopoDS import TopoDS_Shape, TopoDS_Solid
from OCC.Core.BRep import BRep_Tool


class STEPContactAnalyzer:
    """
    Analyzes STEP files to determine contact relationships between parts
    """
    
    def __init__(self, tolerance: float = 1e-6):
        """
        Initialize the analyzer
        
        Args:
            tolerance: Distance tolerance for considering parts in contact
        """
        self.tolerance = tolerance
        self.parts = []
        self.contact_matrix = None
        self.part_names = []
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def load_step_file(self, file_path: str) -> bool:
        """
        Load a STEP file and extract all solid parts
        
        Args:
            file_path: Path to the STEP file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Initialize STEP reader
            step_reader = STEPControl_Reader()
            status = step_reader.ReadFile(file_path)
            
            if status != 1:  # IFSelect_RetDone
                self.logger.error(f"Failed to read STEP file: {file_path}")
                return False
            
            # Transfer shapes
            step_reader.TransferRoots()
            shape = step_reader.OneShape()
            
            # Extract all solid parts
            self.parts = []
            self.part_names = []
            
            explorer = TopExp_Explorer(shape, TopAbs_SOLID)
            part_index = 0
            
            while explorer.More():
                solid = explorer.Current()
                self.parts.append(solid)
                self.part_names.append(f"Part_{part_index}")
                part_index += 1
                explorer.Next()
            
            self.logger.info(f"Loaded {len(self.parts)} parts from {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading STEP file: {e}")
            return False
    
    def compute_contact_matrix(self) -> np.ndarray:
        """
        Compute the contact matrix between all parts
        
        Returns:
            Contact matrix where element (i,j) indicates contact between part i and j
        """
        n_parts = len(self.parts)
        self.contact_matrix = np.zeros((n_parts, n_parts), dtype=int)
        
        self.logger.info("Computing contact matrix...")
        
        for i in range(n_parts):
            for j in range(i + 1, n_parts):
                if self._are_parts_in_contact(self.parts[i], self.parts[j]):
                    self.contact_matrix[i, j] = 1
                    self.contact_matrix[j, i] = 1  # Symmetric matrix
        
        # Set diagonal to 1 (part contacts itself)
        np.fill_diagonal(self.contact_matrix, 1)
        
        self.logger.info("Contact matrix computation complete")
        return self.contact_matrix
    
    def _are_parts_in_contact(self, part1: TopoDS_Shape, part2: TopoDS_Shape) -> bool:
        """
        Check if two parts are in contact based on minimum distance
        
        Args:
            part1: First part
            part2: Second part
            
        Returns:
            True if parts are in contact, False otherwise
        """
        try:
            # Compute minimum distance between parts
            distance_calculator = BRepExtrema_DistShapeShape()
            distance_calculator.LoadS1(part1)
            distance_calculator.LoadS2(part2)
            distance_calculator.Perform()
            
            if distance_calculator.IsDone():
                min_distance = distance_calculator.Value()
                return min_distance <= self.tolerance
            
            return False
            
        except Exception as e:
            self.logger.warning(f"Error calculating distance between parts: {e}")
            return False
    
    def get_contact_graph(self) -> nx.Graph:
        """
        Convert contact matrix to a NetworkX graph
        
        Returns:
            NetworkX graph representing part contacts
        """
        if self.contact_matrix is None:
            raise ValueError("Contact matrix not computed. Call compute_contact_matrix() first.")
        
        G = nx.Graph()
        
        # Add nodes
        for i, name in enumerate(self.part_names):
            G.add_node(i, name=name)
        
        # Add edges for contacts
        n_parts = len(self.parts)
        for i in range(n_parts):
            for j in range(i + 1, n_parts):
                if self.contact_matrix[i, j] == 1:
                    G.add_edge(i, j)
        
        return G
    
    def visualize_contact_graph(self, save_path: Optional[str] = None, figsize: Tuple[int, int] = (12, 8)):
        """
        Visualize the contact graph using matplotlib
        
        Args:
            save_path: Optional path to save the plot (if None, uses output manager)
            figsize: Figure size tuple
        """
        if self.contact_matrix is None:
            raise ValueError("Contact matrix not computed. Call compute_contact_matrix() first.")
        
        G = self.get_contact_graph()
        
        plt.figure(figsize=figsize)
        
        # Create layout
        pos = nx.spring_layout(G, k=1, iterations=50)
        
        # Draw the graph
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                              node_size=1000, alpha=0.7)
        nx.draw_networkx_edges(G, pos, edge_color='gray', 
                              width=2, alpha=0.6)
        
        # Add labels
        labels = {i: name for i, name in enumerate(self.part_names)}
        nx.draw_networkx_labels(G, pos, labels, font_size=10)
        
        plt.title("Part Contact Graph", fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        
        # Simple save path handling
        if save_path is None:
            save_path = "results/contact_analysis.png"
        
        # Ensure results directory exists
        Path("results").mkdir(exist_ok=True)
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        self.logger.info(f"Graph saved to {save_path}")
        
        plt.show()
        return save_path
    
    def print_contact_summary(self):
        """
        Print a summary of the contact analysis
        """
        if self.contact_matrix is None:
            print("No contact matrix computed.")
            return
        
        n_parts = len(self.parts)
        total_contacts = np.sum(self.contact_matrix) // 2  # Divide by 2 due to symmetry
        
        print(f"\n=== Contact Analysis Summary ===")
        print(f"Number of parts: {n_parts}")
        print(f"Total contacts: {total_contacts}")
        print(f"Contact density: {total_contacts / (n_parts * (n_parts - 1) / 2):.2%}")
        
        print(f"\nContact Matrix:")
        print(self.contact_matrix)
        
        print(f"\nPart connections:")
        for i, name in enumerate(self.part_names):
            connections = np.sum(self.contact_matrix[i]) - 1  # Subtract self-contact
            connected_parts = [self.part_names[j] for j in range(len(self.part_names)) 
                             if self.contact_matrix[i, j] == 1 and i != j]
            print(f"{name}: {connections} connections -> {connected_parts}")


def main():
    """
    Main function demonstrating the STEP contact analysis
    """
    print("STEP Contact Matrix Analyzer")
    print("=" * 40)
    
    # Example usage
    analyzer = STEPContactAnalyzer(tolerance=1e-3)
    
    # You can replace this with your STEP file path
    step_file_path = "example.step"
    
    if Path(step_file_path).exists():
        print(f"Loading STEP file: {step_file_path}")
        
        if analyzer.load_step_file(step_file_path):
            print("Computing contact matrix...")
            analyzer.compute_contact_matrix()
            
            print("Generating visualization...")
            analyzer.visualize_contact_graph(save_path="contact_graph.png")
            
            analyzer.print_contact_summary()
        else:
            print("Failed to load STEP file")
    else:
        print(f"STEP file not found: {step_file_path}")
        print("Please provide a valid STEP file path")
        
        # Create a simple example for demonstration
        print("\nCreating demonstration with synthetic data...")
        create_demo_analysis()


def create_demo_analysis():
    """
    Create a demonstration analysis with synthetic data
    """
    # Create a simple contact matrix for demonstration
    part_names = ["Base", "Shaft", "Bearing", "Housing", "Cover"]
    n_parts = len(part_names)
    
    # Create a synthetic contact matrix
    contact_matrix = np.array([
        [1, 1, 1, 0, 0],  # Base contacts Shaft and Bearing
        [1, 1, 1, 1, 0],  # Shaft contacts Base, Bearing, and Housing
        [1, 1, 1, 1, 0],  # Bearing contacts Base, Shaft, and Housing
        [0, 1, 1, 1, 1],  # Housing contacts Shaft, Bearing, and Cover
        [0, 0, 0, 1, 1]   # Cover contacts Housing
    ])
    
    # Create NetworkX graph
    G = nx.Graph()
    
    # Add nodes
    for i, name in enumerate(part_names):
        G.add_node(i, name=name)
    
    # Add edges
    for i in range(n_parts):
        for j in range(i + 1, n_parts):
            if contact_matrix[i, j] == 1:
                G.add_edge(i, j)
    
    # Visualize
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, k=2, iterations=50)
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color='lightcoral', 
                          node_size=2000, alpha=0.8)
    # Draw edges
    nx.draw_networkx_edges(G, pos, edge_color='darkblue', 
                          width=3, alpha=0.6)
    # Add labels
    labels = {i: name for i, name in enumerate(part_names)}
    nx.draw_networkx_labels(G, pos, labels, font_size=12, font_weight='bold')
    
    plt.title("Demo: Part Contact Graph", fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig("demo_contact_graph.png", dpi=300, bbox_inches='tight')
    plt.show()
    
    # Print summary
    print(f"\n=== Demo Contact Analysis ===")
    print(f"Parts: {part_names}")
    print(f"Contact Matrix:")
    print(contact_matrix)


if __name__ == "__main__":
    main()
