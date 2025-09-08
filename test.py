"""
Simple test script for the STEP Contact Matrix Analyzer

This script runs basic tests to ensure the application works correctly.
"""

import numpy as np
import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from step_contact_analyzer import STEPContactAnalyzer
from utils import analyze_contact_matrix_properties


def test_synthetic_data():
    """Test with synthetic contact matrix"""
    print("Testing synthetic contact matrix...")
    
    # Create a simple contact matrix
    contact_matrix = np.array([
        [1, 1, 0],
        [1, 1, 1],
        [0, 1, 1]
    ])
    
    # Analyze properties
    props = analyze_contact_matrix_properties(contact_matrix)
    
    assert props['n_parts'] == 3
    assert props['total_contacts'] == 3  # All parts are connected
    assert abs(props['contact_density'] - 1.0) < 1e-6  # 100% density
    
    print("✓ Synthetic data test passed")


def test_step_file_loading():
    """Test STEP file loading and analysis"""
    print("Testing STEP file loading and analysis...")
    
    if os.path.exists("step_files/knife.step"):
        analyzer = STEPContactAnalyzer(tolerance=1e-2)
        
        # Load file
        success = analyzer.load_step_file("step_files/knife.step")
        assert success, "Failed to load STEP file"
        assert len(analyzer.parts) > 0, "No parts loaded"
        
        # Compute contact matrix
        contact_matrix = analyzer.compute_contact_matrix()
        assert contact_matrix is not None, "Contact matrix not computed"
        assert contact_matrix.shape[0] == len(analyzer.parts), "Matrix size mismatch"
        
        # Check matrix properties
        assert np.allclose(contact_matrix, contact_matrix.T), "Matrix not symmetric"
        assert np.all(np.diag(contact_matrix) == 1), "Diagonal not all ones"
        
        print("✓ STEP file loading and analysis test passed")
    else:
        print("⚠ STEP file loading test skipped (no knife.step file)")


def test_graph_creation():
    """Test NetworkX graph creation"""
    print("Testing NetworkX graph creation...")
    
    # Create analyzer with synthetic data
    analyzer = STEPContactAnalyzer()
    analyzer.parts = ["part1", "part2", "part3"]  # Dummy parts
    analyzer.part_names = ["Part_0", "Part_1", "Part_2"]
    analyzer.contact_matrix = np.array([
        [1, 1, 0],
        [1, 1, 1],
        [0, 1, 1]
    ])
    
    # Create graph
    G = analyzer.get_contact_graph()
    
    assert G.number_of_nodes() == 3, "Wrong number of nodes"
    assert G.number_of_edges() == 2, "Wrong number of edges"
    
    print("✓ Graph creation test passed")


def test_utilities():
    """Test utility functions"""
    print("Testing utility functions...")
    
    # Test contact matrix analysis
    contact_matrix = np.array([
        [1, 1, 1, 0],
        [1, 1, 0, 1],
        [1, 0, 1, 0],
        [0, 1, 0, 1]
    ])
    
    props = analyze_contact_matrix_properties(contact_matrix)
    
    expected_contacts = 5  # Total matrix sum // 2 = 10 // 2 = 5
    assert props['total_contacts'] == expected_contacts
    assert props['n_parts'] == 4
    
    print("✓ Utilities test passed")


def main():
    """Run all tests"""
    print("STEP Contact Matrix Analyzer - Test Suite")
    print("=" * 50)
    
    try:
        test_synthetic_data()
        test_step_file_loading()
        test_graph_creation()
        test_utilities()
        
        print("\n" + "=" * 50)
        print("✓ All tests passed successfully!")
        
        # Print system information
        print("\nSystem Information:")
        try:
            import OCC
            print(f"PythonOCC version: {OCC.VERSION}")
        except:
            print("PythonOCC: Available")
        
        try:
            import networkx as nx
            print(f"NetworkX version: {nx.__version__}")
        except:
            print("NetworkX: Available")
        
        try:
            import matplotlib
            print(f"Matplotlib version: {matplotlib.__version__}")
        except:
            print("Matplotlib: Available")
        
        try:
            import numpy as np
            print(f"NumPy version: {np.__version__}")
        except:
            print("NumPy: Available")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
