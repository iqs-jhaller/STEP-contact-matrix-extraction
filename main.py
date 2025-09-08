"""
Main script for STEP Contact Matrix Analyzer

Usage:
    python main.py                         # Analyze default file (step_files/knife.step)
    python main.py <file.step>             # Analyze specified STEP file
    python main.py test                    # Run test suite
"""

import sys
import os
from pathlib import Path

# Default STEP file to analyze
DEFAULT_STEP_FILE = "step_files/knife.step"

def show_help():
    """Display help information"""
    print(__doc__)


def analyze_step_file(file_path):
    """Analyze a STEP file"""
    from step_contact_analyzer import STEPContactAnalyzer
    
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return False
    
    print(f"Analyzing STEP file: {file_path}")
    
    analyzer = STEPContactAnalyzer(tolerance=1e-3)
    
    if analyzer.load_step_file(file_path):
        print(f"Loaded {len(analyzer.parts)} parts")
        
        # Compute contact matrix
        analyzer.compute_contact_matrix()
        
        # Generate visualization
        file_stem = Path(file_path).stem
        output_path = f"results/{file_stem}_analysis.png"
        analyzer.visualize_contact_graph(save_path=output_path)
        
        # Print summary
        analyzer.print_contact_summary()
        
        print(f"\nVisualization saved as: {output_path}")
        return True
    else:
        print("Failed to load STEP file")
        return False


def run_tests():
    """Run the test suite"""
    from test import main as test_main
    return test_main()


def main():
    """Main entry point"""
    # Ensure results directory exists
    Path("results").mkdir(exist_ok=True)
    
    # Handle different argument patterns
    if len(sys.argv) == 1:
        # No arguments - analyze default file
        if os.path.exists(DEFAULT_STEP_FILE):
            print(f"Analyzing default file: {DEFAULT_STEP_FILE}")
            analyze_step_file(DEFAULT_STEP_FILE)
        else:
            print(f"Default file not found: {DEFAULT_STEP_FILE}")
            print("Please provide a STEP file path or create the default file.")
            print("Usage: python main.py <file.step>")
            sys.exit(1)
        return
    
    # Get first argument
    command = sys.argv[1].lower()
    
    # Check if it's a help command
    if command in ['help', '-h', '--help']:
        show_help()
    
    # Check if it's the test command
    elif command == 'test':
        print("Running test suite...")
        success = run_tests()
        sys.exit(0 if success else 1)
    
    # Check if it's a file path (ends with .step or .stp, or exists as file)
    elif command.endswith(('.step', '.stp')) or os.path.exists(sys.argv[1]):
        file_path = sys.argv[1]
        success = analyze_step_file(file_path)
        sys.exit(0 if success else 1)
    
    # Unknown command
    else:
        print(f"Unknown command or file not found: {command}")
        show_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
