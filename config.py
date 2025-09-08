# STEP Contact Matrix Analyzer Configuration

# Contact Detection Settings
TOLERANCE = 1e-3  # Distance tolerance for contact detection (in model units)
                  # Smaller values = more strict contact detection
                  # Larger values = more lenient contact detection
                  # Typical values: 1e-6 (very strict) to 1e-1 (lenient)

# Visualization Settings
GRAPH_LAYOUT = "spring"  # Options: spring, kamada_kawai, circular, spectral
FIGURE_SIZE = (12, 8)    # Width, height in inches
DPI = 300               # Resolution for saved images
NODE_SIZE = 1500        # Size of nodes in graph
EDGE_WIDTH = 2          # Width of edges in graph
ALPHA = 0.7            # Transparency (0.0 = transparent, 1.0 = opaque)

# Analysis Settings
SHOW_ISOLATED_PARTS = True     # Include parts with no connections in analysis
COMPUTE_CENTRALITY = True      # Calculate centrality measures
FIND_BRIDGES = True           # Find critical connections
MAX_PARTS_FOR_DETAILED_ANALYSIS = 50  # Limit for detailed graph analysis

# Output Settings
SAVE_IMAGES = True            # Automatically save visualizations
SAVE_CSV = False             # Export contact matrices to CSV
VERBOSE_OUTPUT = True        # Show detailed analysis information
LOG_LEVEL = "INFO"          # Logging level: DEBUG, INFO, WARNING, ERROR

# File Format Settings
STEP_ENCODING = "utf-8"      # Text encoding for STEP files
CSV_DELIMITER = ","          # Delimiter for CSV exports
IMAGE_FORMAT = "png"         # Format for saved images: png, pdf, svg

# Performance Settings
PARALLEL_PROCESSING = False   # Use multiprocessing for large assemblies
MAX_WORKERS = 4              # Number of parallel workers
CHUNK_SIZE = 100            # Batch size for parallel processing

# Advanced Settings
USE_BOUNDING_BOX_FILTER = True    # Pre-filter using bounding boxes
GEOMETRIC_PRECISION = 1e-12       # Internal geometric computation precision
SHAPE_TOLERANCE = 1e-7           # Shape comparison tolerance
