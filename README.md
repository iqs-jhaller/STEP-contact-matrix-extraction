## +++ Repository moved +++
I moved the repository to https://gitlab.com/TIBHannover/human-decision/source-code/STEP-contact-matrix-extraction, where it will be further developed.
The Github version remains unchanged after 01.10.2025.

# STEP Contact Matrix Analyzer

A Python application that analyzes STEP (Standard for the Exchange of Product Data) files to create contact matrices showing which parts touch or are connected to each other, and visualizes the results as interactive graphs using NetworkX.

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
├── LICENSE                     # MIT License
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
- **publication/**: Academic diagrams and documentation (ignored by git)
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

## Core Classes and Functions

### STEPContactAnalyzer

Main class for analyzing STEP files and computing contact matrices.

**Key Methods:**
- `load_step_file(file_path)`: Load and parse a STEP file, extracting part names from metadata
- `compute_contact_matrix()`: Calculate part-to-part contact relationships
- `get_contact_graph()`: Convert contact matrix to NetworkX graph
- `visualize_contact_graph()`: Create and display graph visualization  
- `print_contact_summary()`: Display analysis results

**Features:**
- Automatically extracts meaningful part names from STEP file PRODUCT entities
- Falls back to generic names (Part_0, Part_1, etc.) if extraction fails
- Uses exact geometric distance calculation via OpenCASCADE

**Parameters:**
- `tolerance`: Distance threshold for considering parts in contact (default: 1e-6)

### Utility Functions

**Contact Analysis:**
- `analyze_contact_matrix_properties()`: Compute basic contact statistics
- `export_contact_matrix_csv()`: Save contact matrix to CSV file
- `load_contact_matrix_csv()`: Load contact matrix from CSV file

**STEP File Handling:**
- `validate_step_file()`: Check if file is a valid STEP format


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

## File Formats

### Supported Input Formats

#### STEP Files (.step, .stp)
Primary 3D CAD exchange format following ISO 10303 standard.

#### CSV Files (.csv)
Pre-computed contact matrices can be imported using the following format:

```csv
,Part_A,Part_B,Part_C
Part_A,1,1,0
Part_B,1,1,1
Part_C,0,1,1
```

**Format Requirements:**
- First row: Header with empty first cell, followed by part names
- Subsequent rows: Part name in first column, followed by contact values (0 or 1)
- Matrix must be square and symmetric
- Diagonal elements should be 1 (self-contact)
- Values: 1 = contact, 0 = no contact

**Usage:**
```python
from utils import load_contact_matrix_csv
contact_matrix, part_names = load_contact_matrix_csv("contact_matrix.csv")
```

### Output Formats
- **PNG**: Graph visualizations
- **CSV**: Contact matrices for external analysis


### Performance Considerations

- **Large Assemblies**: Contact computation is O(n²) where n = number of parts
- **Memory Usage**: Contact matrices require n² memory
- **Visualization**: Large graphs (>50 nodes) may be slow to render

**Optimization Tips:**
- Use appropriate tolerance values
- Consider analyzing sub-assemblies separately

## Contributing

Contributions are welcome! Areas for improvement:
- Advanced contact detection algorithms
- Performance optimizations
- Additional analysis features

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## References

- [OpenCASCADE Documentation](https://dev.opencascade.org/)
- [PythonOCC Examples](https://github.com/tpaviot/pythonocc-demos)
- [NetworkX Documentation](https://networkx.org/documentation/)
- [STEP File Format Specification](https://www.iso.org/standard/63141.html)
