"""
Output Manager for STEP Contact Matrix Analyzer

Manages file organization and prevents duplicate outputs
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional


class OutputManager:
    """
    Manages output files and directories for the STEP Contact Matrix Analyzer
    """
    
    def __init__(self, base_dir: str = None):
        """
        Initialize the output manager
        
        Args:
            base_dir: Base directory for outputs (defaults to ./outputs)
        """
        if base_dir is None:
            base_dir = Path(__file__).parent / "outputs"
        
        self.base_dir = Path(base_dir)
        self.graphs_dir = self.base_dir / "graphs"
        self.step_files_dir = self.base_dir / "step_files"
        self.matrices_dir = self.base_dir / "matrices"
        
        # Create directories if they don't exist
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create output directories if they don't exist"""
        for directory in [self.base_dir, self.graphs_dir, self.step_files_dir, self.matrices_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def get_unique_filename(self, base_name: str, extension: str, directory: Path) -> Path:
        """
        Generate a unique filename to avoid duplicates
        
        Args:
            base_name: Base name for the file
            extension: File extension (with or without dot)
            directory: Directory where file will be saved
            
        Returns:
            Unique file path
        """
        if not extension.startswith('.'):
            extension = '.' + extension
        
        # Try the base name first
        file_path = directory / f"{base_name}{extension}"
        
        if not file_path.exists():
            return file_path
        
        # If file exists, add timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = directory / f"{base_name}_{timestamp}{extension}"
        
        # If still exists (very unlikely), add counter
        counter = 1
        while file_path.exists():
            file_path = directory / f"{base_name}_{timestamp}_{counter}{extension}"
            counter += 1
        
        return file_path
    
    def get_graph_path(self, name: str, ensure_unique: bool = True) -> Path:
        """
        Get path for graph output file
        
        Args:
            name: Base name for the graph file
            ensure_unique: Whether to ensure filename is unique
            
        Returns:
            Path for the graph file
        """
        if ensure_unique:
            return self.get_unique_filename(name, "png", self.graphs_dir)
        else:
            return self.graphs_dir / f"{name}.png"
    
    def get_step_file_path(self, name: str, ensure_unique: bool = True) -> Path:
        """
        Get path for STEP file output
        
        Args:
            name: Base name for the STEP file
            ensure_unique: Whether to ensure filename is unique
            
        Returns:
            Path for the STEP file
        """
        if ensure_unique:
            return self.get_unique_filename(name, "step", self.step_files_dir)
        else:
            return self.step_files_dir / f"{name}.step"
    
    def get_matrix_path(self, name: str, ensure_unique: bool = True) -> Path:
        """
        Get path for contact matrix CSV file
        
        Args:
            name: Base name for the matrix file
            ensure_unique: Whether to ensure filename is unique
            
        Returns:
            Path for the matrix file
        """
        if ensure_unique:
            return self.get_unique_filename(name, "csv", self.matrices_dir)
        else:
            return self.matrices_dir / f"{name}.csv"
    
    def clean_old_demo_files(self):
        """
        Clean up old demo files to prevent clutter
        Keeps only the most recent version of each demo type
        """
        demo_patterns = {
            "demo_mechanical_assembly": self.graphs_dir,
            "demo_graph_analysis": self.graphs_dir,
            "step_file_analysis": self.graphs_dir,
            "example_assembly": self.step_files_dir
        }
        
        for pattern, directory in demo_patterns.items():
            self._clean_pattern_files(pattern, directory)
    
    def _clean_pattern_files(self, pattern: str, directory: Path):
        """
        Clean files matching a pattern, keeping only the most recent
        
        Args:
            pattern: File name pattern to match
            directory: Directory to search in
        """
        if not directory.exists():
            return
        
        # Find all files matching the pattern
        matching_files = []
        for file_path in directory.iterdir():
            if file_path.is_file() and file_path.stem.startswith(pattern):
                matching_files.append(file_path)
        
        if len(matching_files) <= 1:
            return  # Keep if only one or none
        
        # Sort by modification time (newest first)
        matching_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        # Remove all but the most recent
        for file_path in matching_files[1:]:
            try:
                file_path.unlink()
                print(f"Cleaned up old file: {file_path.name}")
            except Exception as e:
                print(f"Warning: Could not remove {file_path.name}: {e}")
    
    def move_existing_outputs(self):
        """
        Move any existing output files from the root directory to organized folders
        """
        root_dir = self.base_dir.parent  # Project root
        
        # Patterns for different file types
        patterns = {
            '*.png': self.graphs_dir,
            '*.jpg': self.graphs_dir,
            '*.pdf': self.graphs_dir,
            '*.svg': self.graphs_dir,
            '*.step': self.step_files_dir,
            '*.stp': self.step_files_dir,
            '*contact_matrix*.csv': self.matrices_dir,
        }
        
        moved_files = []
        
        for pattern, target_dir in patterns.items():
            for file_path in root_dir.glob(pattern):
                if file_path.is_file() and file_path.parent == root_dir:
                    try:
                        # Generate unique target path
                        target_path = self.get_unique_filename(
                            file_path.stem, 
                            file_path.suffix, 
                            target_dir
                        )
                        
                        shutil.move(str(file_path), str(target_path))
                        moved_files.append((file_path.name, target_path.relative_to(self.base_dir)))
                    except Exception as e:
                        print(f"Warning: Could not move {file_path.name}: {e}")
        
        if moved_files:
            print(f"Moved {len(moved_files)} files to organized folders:")
            for old_name, new_path in moved_files:
                print(f"  {old_name} -> outputs/{new_path}")
    
    def create_readme(self):
        """Create a README file in the outputs directory"""
        readme_path = self.base_dir / "README.md"
        
        readme_content = """# Output Files

This directory contains all output files generated by the STEP Contact Matrix Analyzer.

## Directory Structure

- **graphs/**: Graph visualizations (PNG, PDF, SVG files)
- **step_files/**: Generated or processed STEP files
- **matrices/**: Contact matrices exported as CSV files

## File Naming Convention

Files are automatically organized and timestamped to prevent duplicates:
- Base filename: `analysis_name.extension`
- With timestamp: `analysis_name_YYYYMMDD_HHMMSS.extension`
- With counter: `analysis_name_YYYYMMDD_HHMMSS_N.extension`

## Cleanup

Old demo files are automatically cleaned up to prevent clutter.
Only the most recent version of each demo type is kept.

## Generated Files

This folder is managed automatically by the OutputManager class.
Files are moved here from the project root to keep the repository clean.
"""
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
    
    def get_summary(self) -> dict:
        """
        Get summary of output files
        
        Returns:
            Dictionary with file counts and sizes
        """
        summary = {
            'graphs': 0,
            'step_files': 0,
            'matrices': 0,
            'total_size_mb': 0
        }
        
        for directory, key in [(self.graphs_dir, 'graphs'), 
                              (self.step_files_dir, 'step_files'),
                              (self.matrices_dir, 'matrices')]:
            if directory.exists():
                files = list(directory.iterdir())
                summary[key] = len([f for f in files if f.is_file()])
                
                # Calculate total size
                for file_path in files:
                    if file_path.is_file():
                        summary['total_size_mb'] += file_path.stat().st_size
        
        summary['total_size_mb'] = round(summary['total_size_mb'] / (1024 * 1024), 2)
        
        return summary


# Global output manager instance
output_manager = OutputManager()


def initialize_outputs():
    """Initialize the output system"""
    output_manager.move_existing_outputs()
    output_manager.create_readme()
    print(f"Output system initialized. Files organized in: {output_manager.base_dir}")


if __name__ == "__main__":
    # Initialize when run directly
    initialize_outputs()
    
    # Show summary
    summary = output_manager.get_summary()
    print(f"\nOutput Summary:")
    print(f"  Graphs: {summary['graphs']} files")
    print(f"  STEP files: {summary['step_files']} files")
    print(f"  Matrices: {summary['matrices']} files")
    print(f"  Total size: {summary['total_size_mb']} MB")
