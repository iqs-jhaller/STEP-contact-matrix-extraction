# STEP Contact Matrix Analyzer

A Python application that analyzes STEP (Standard for the Exchange of Product Data) files to create contact matrices showing which parts touch or are connected to each other, and visualizes the results as interactive graphs using NetworkX.

## Features

- **STEP File Loading**: Parse and load 3D CAD models from STEP files
- **Contact Detection**: Automatically detect which parts are in contact based on geometric proximity
- **Contact Matrix Generation**: Create binary matrices representing part-to-part contacts
- **Graph Visualization**: Convert contact relationships into NetworkX graphs with customizable layouts
- **Analysis Tools**: Compute centrality measures, find critical connections, and analyze assembly structure
- **Export/Import**: Save contact matrices to CSV files for further analysis
- **Simple Organization**: Clean folder structure with inputs and results separated
- **Easy Usage**: Simple command-line interface for direct file analysis

## Installation

### Prerequisites

- Python 3.11+
- Conda package manager

### Setup Environment

1. Clone or download this repository
2. Create and activate the conda environment:

```bash
conda create -n step-contact-matrix python=3.11 -y
conda activate step-contact-matrix
```

3. Install required packages:

```bash
conda install -c conda-forge pythonocc-core networkx matplotlib numpy scipy -y
```

### Package Dependencies

- **pythonocc-core**: Python bindings for OpenCASCADE (3D modeling kernel)
- **networkx**: Graph analysis and visualization
- **matplotlib**: Plotting and visualization
- **numpy**: Numerical computations
- **scipy**: Scientific computing utilities

## Repository Structure

The project uses a simple, logical folder organization:

```
step-contact-matrix/
├── step_contact_analyzer.py    # Main analyzer class
├── utils.py                    # Utility functions  
├── test.py                     # Test suite
├── main.py                     # Command-line interface
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── README.md                   # Documentation
├── .gitignore                  # Git ignore rules
├── step_files/                 # Input STEP files
│   └── knife.step              # Example knife assembly
└── results/                    # Generated output files
    ├── *.png                   # Graph visualizations
    └── *.csv                   # Contact matrices
```

**Key Principles:**
- **step_files/**: Input folder for STEP files (tracked in git)
- **results/**: Output folder for all generated files (ignored by git)
- **Clean Separation**: Inputs and outputs are clearly separated
- **Simple Structure**: No complex nested folders or management systems

## Usage

### Command Line Interface

The application provides a simple command-line interface:

```bash
# Analyze default file (step_files/knife.step)
python main.py

# Analyze a specific STEP file
python main.py your_assembly.step

# Run test suite
python main.py test

# Show help
python main.py help
```

### Basic Programmatic Usage

```python
from step_contact_analyzer import STEPContactAnalyzer

# Initialize analyzer
analyzer = STEPContactAnalyzer(tolerance=1e-3)

# Load STEP file
if analyzer.load_step_file("your_assembly.step"):
    # Compute contact matrix
    contact_matrix = analyzer.compute_contact_matrix()
    
    # Visualize as graph
    analyzer.visualize_contact_graph(save_path="contact_graph.png")
    
    # Print summary
    analyzer.print_contact_summary()
```

### Running Tests

The application includes a comprehensive test suite:

```bash
python main.py test
```

This will test all core functionality using the included knife.step file.

## Core Classes and Functions

### STEPContactAnalyzer

Main class for analyzing STEP files and computing contact matrices.

**Key Methods:**
- `load_step_file(file_path)`: Load and parse a STEP file
- `compute_contact_matrix()`: Calculate part-to-part contact relationships
- `get_contact_graph()`: Convert contact matrix to NetworkX graph
- `visualize_contact_graph()`: Create and display graph visualization
- `print_contact_summary()`: Display analysis results

**Parameters:**
- `tolerance`: Distance threshold for considering parts in contact (default: 1e-6)

### Utility Functions

**Contact Analysis:**
- `analyze_contact_matrix_properties()`: Compute graph metrics and statistics
- `export_contact_matrix_csv()`: Save contact matrix to CSV file
- `load_contact_matrix_csv()`: Load contact matrix from CSV file

**STEP File Handling:**
- `validate_step_file()`: Check if file is a valid STEP format

**Visualization:**
- `get_recommended_layout()`: Suggest optimal graph layout based on size

## Examples

### Example 1: Mechanical Assembly Analysis

```python
# Analyze the knife assembly
analyzer = STEPContactAnalyzer(tolerance=0.1)  # 0.1mm tolerance

if analyzer.load_step_file("step_files/knife.step"):
    # Compute contacts
    contact_matrix = analyzer.compute_contact_matrix()
    
    # Get graph representation
    G = analyzer.get_contact_graph()
    
    # Analyze structure
    import networkx as nx
    central_parts = nx.degree_centrality(G)
    critical_connections = list(nx.bridges(G))
    
    print(f"Most connected part: {max(central_parts, key=central_parts.get)}")
    print(f"Critical connections: {len(critical_connections)}")
```

### Example 2: Custom Visualization

```python
import matplotlib.pyplot as plt
import networkx as nx

# Create custom visualization
G = analyzer.get_contact_graph()

plt.figure(figsize=(15, 10))
pos = nx.spring_layout(G, k=2, iterations=100)

# Color nodes by connectivity
node_colors = [G.degree(node) for node in G.nodes()]

nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                      node_size=1500, cmap=plt.cm.plasma)
nx.draw_networkx_edges(G, pos, alpha=0.5, width=2)
nx.draw_networkx_labels(G, pos, font_size=8)

plt.title("Assembly Contact Network")
plt.axis('off')
plt.show()
```

### Example 3: Export Analysis Results

```python
from utils import export_contact_matrix_csv, analyze_contact_matrix_properties

# Export contact matrix
export_contact_matrix_csv(
    analyzer.contact_matrix, 
    analyzer.part_names, 
    "assembly_contacts.csv"
)

# Analyze properties
props = analyze_contact_matrix_properties(analyzer.contact_matrix)
print(f"Contact density: {props['contact_density']:.2%}")
print(f"Average connections: {props['avg_connections']:.1f}")
```

## Understanding Contact Matrices

A contact matrix is a square binary matrix where:
- Rows and columns represent parts in the assembly
- Element (i,j) = 1 if part i contacts part j
- Element (i,j) = 0 if parts don't contact
- Diagonal elements are always 1 (part contacts itself)
- Matrix is symmetric: contact_matrix[i,j] = contact_matrix[j,i]

**Example:**
```
     Part_A  Part_B  Part_C
Part_A   1      1      0     # Part_A contacts Part_B
Part_B   1      1      1     # Part_B contacts Part_A and Part_C  
Part_C   0      1      1     # Part_C contacts Part_B
```

## Graph Analysis Features

The application provides several graph analysis capabilities:

### Centrality Measures
- **Degree Centrality**: Identifies most connected parts
- **Betweenness Centrality**: Finds parts that bridge different sections
- **Closeness Centrality**: Locates parts with shortest paths to others

### Structural Analysis
- **Bridges**: Critical connections whose removal would disconnect the assembly
- **Connected Components**: Separate sub-assemblies within the model
- **Clustering**: Groups of highly interconnected parts

### Visualization Options
- **Spring Layout**: Good for small to medium assemblies
- **Kamada-Kawai**: Better for structured layouts
- **Circular Layout**: Useful for symmetric assemblies
- **Spectral Layout**: Effective for large, complex assemblies

## File Formats

### Supported Input Formats
- **STEP (.step, .stp)**: Primary 3D CAD exchange format
- **CSV**: For importing pre-computed contact matrices

### Output Formats
- **PNG/PDF**: High-resolution graph visualizations
- **CSV**: Contact matrices for external analysis
- **GraphML**: NetworkX graph format for advanced tools

## Troubleshooting

### Common Issues

**1. Import Errors**
```
ImportError: No module named 'OCC'
```
- Ensure pythonocc-core is installed: `conda install -c conda-forge pythonocc-core`
- Activate the correct conda environment

**2. STEP File Loading Fails**
```
Failed to read STEP file
```
- Verify file is valid STEP format
- Check file permissions
- Ensure file path is correct

**3. Contact Detection Issues**
```
No contacts detected
```
- Adjust tolerance parameter (try larger values like 1e-2 or 1e-1)
- Verify parts are actually touching in the CAD model
- Check for unit conversion issues

**4. Visualization Problems**
```
Empty graph display
```
- Ensure matplotlib backend is properly configured
- Try different graph layouts
- Check if contact matrix has any connections

### Performance Considerations

- **Large Assemblies**: Contact computation is O(n²) where n = number of parts
- **Memory Usage**: Contact matrices require n² memory
- **Visualization**: Large graphs (>100 nodes) may be slow to render

**Optimization Tips:**
- Use appropriate tolerance values
- Consider analyzing sub-assemblies separately
- Use efficient graph layouts for large models

## Advanced Usage

### Custom Contact Detection

```python
class CustomContactAnalyzer(STEPContactAnalyzer):
    def _are_parts_in_contact(self, part1, part2):
        # Implement custom contact detection logic
        # Example: check for overlapping bounding boxes
        return custom_contact_check(part1, part2)
```

### Batch Processing

```python
import glob

# Process multiple STEP files
step_files = glob.glob("assemblies/*.step")

results = {}
for file_path in step_files:
    analyzer = STEPContactAnalyzer()
    if analyzer.load_step_file(file_path):
        analyzer.compute_contact_matrix()
        results[file_path] = analyzer.contact_matrix
```

### Integration with CAD Tools

The application can be integrated with various CAD workflows:
- **FreeCAD**: Use as analysis plugin
- **Blender**: Import results for visualization
- **SolidWorks**: Process exported STEP files
- **Fusion 360**: Analyze assembly contact relationships

## Contributing

Contributions are welcome! Areas for improvement:
- Additional file format support (IGES, STL, etc.)
- Advanced contact detection algorithms
- Interactive 3D visualization
- Performance optimizations
- Additional graph analysis metrics

## License

This project is open source. Please check the license file for details.

## References

- [OpenCASCADE Documentation](https://dev.opencascade.org/)
- [PythonOCC Examples](https://github.com/tpaviot/pythonocc-demos)
- [NetworkX Documentation](https://networkx.org/documentation/)
- [STEP File Format Specification](https://www.iso.org/standard/63141.html)
