"""
Utility functions for STEP file handling and contact analysis
"""

import numpy as np
from typing import List, Tuple
import os
from pathlib import Path


def analyze_contact_matrix_properties(contact_matrix: np.ndarray) -> dict:
    """
    Analyze properties of a contact matrix
    
    Args:
        contact_matrix: Binary contact matrix
        
    Returns:
        Dictionary with analysis results
    """
    n_parts = contact_matrix.shape[0]
    
    # Basic properties
    total_contacts = np.sum(contact_matrix) // 2  # Divide by 2 for symmetry
    max_possible_contacts = n_parts * (n_parts - 1) // 2
    density = total_contacts / max_possible_contacts if max_possible_contacts > 0 else 0
    
    # Connectivity analysis
    degree_sequence = np.sum(contact_matrix, axis=1) - 1  # Subtract diagonal
    max_connections = np.max(degree_sequence)
    min_connections = np.min(degree_sequence)
    avg_connections = np.mean(degree_sequence)
    
    # Find isolated parts (no connections)
    isolated_parts = np.sum(degree_sequence == 0)
    
    return {
        'n_parts': n_parts,
        'total_contacts': total_contacts,
        'contact_density': density,
        'max_connections': max_connections,
        'min_connections': min_connections,
        'avg_connections': avg_connections,
        'isolated_parts': isolated_parts
    }


def export_contact_matrix_csv(contact_matrix: np.ndarray, part_names: List[str], filename: str = None):
    """
    Export contact matrix to CSV file
    
    Args:
        contact_matrix: Binary contact matrix
        part_names: List of part names
        filename: Output CSV filename (if None, uses default name in results folder)
    """
    import csv
    
    # Simple file path handling
    if filename is None:
        Path("results").mkdir(exist_ok=True)
        file_path = "results/contact_matrix.csv"
    else:
        file_path = filename
    
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow([''] + part_names)
        
        # Write matrix rows
        for i, part_name in enumerate(part_names):
            row = [part_name] + contact_matrix[i].tolist()
            writer.writerow(row)
    
    print(f"Contact matrix exported to {file_path}")
    return file_path


def load_contact_matrix_csv(filename: str) -> Tuple[np.ndarray, List[str]]:
    """
    Load contact matrix from CSV file
    
    Args:
        filename: CSV filename to load
        
    Returns:
        Tuple of (contact_matrix, part_names)
    """
    import csv
    
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
    
    # Extract part names from header (skip first empty cell)
    part_names = rows[0][1:]
    
    # Extract matrix data
    matrix_data = []
    for row in rows[1:]:
        matrix_data.append([int(x) for x in row[1:]])
    
    contact_matrix = np.array(matrix_data)
    
    return contact_matrix, part_names


def validate_step_file(file_path: str) -> bool:
    """
    Validate if a file is a valid STEP file
    
    Args:
        file_path: Path to the file to validate
        
    Returns:
        True if valid STEP file, False otherwise
    """
    if not os.path.exists(file_path):
        return False
    
    # Check file extension
    if not file_path.lower().endswith(('.step', '.stp')):
        return False
    
    # Check file header
    try:
        with open(file_path, 'r') as f:
            first_line = f.readline().strip()
            return first_line.startswith('ISO-10303')
    except:
        return False


def get_recommended_layout(n_nodes: int) -> str:
    """
    Get recommended NetworkX layout based on number of nodes
    
    Args:
        n_nodes: Number of nodes in the graph
        
    Returns:
        Recommended layout name
    """
    if n_nodes <= 10:
        return 'spring'
    elif n_nodes <= 20:
        return 'kamada_kawai'
    elif n_nodes <= 50:
        return 'fruchterman_reingold'
    else:
        return 'spectral'


if __name__ == "__main__":
    # Test utility functions if run directly
    print("STEP Contact Matrix Analyzer - Utilities")
    print("Run main.py to analyze STEP files")
