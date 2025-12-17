"""
Export functionality for analysis results.
"""

import json
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import pandas as pd
from logger import get_logger

logger = get_logger("export")

# Create exports directory
EXPORT_DIR = Path("exports")
EXPORT_DIR.mkdir(exist_ok=True)


class ExportManager:
    """Manages export of analysis results to various formats."""
    
    def __init__(self):
        """Initialize export manager."""
        self.export_dir = EXPORT_DIR
    
    def export_json(self, data: Dict[str, Any], filename: str = None) -> Path:
        """
        Export data to JSON file.
        
        Args:
            data: Data to export
            filename: Optional filename (without extension)
            
        Returns:
            Path to exported file
        """
        if filename is None:
            filename = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        filepath = self.export_dir / f"{filename}.json"
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
            
            logger.info(f"Exported JSON to {filepath}")
            return filepath
        
        except Exception as e:
            logger.error(f"Error exporting JSON: {str(e)}")
            raise
    
    def export_csv(self, data: List[Dict[str, Any]], filename: str = None) -> Path:
        """
        Export data to CSV file.
        
        Args:
            data: List of dictionaries to export
            filename: Optional filename (without extension)
            
        Returns:
            Path to exported file
        """
        if filename is None:
            filename = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        filepath = self.export_dir / f"{filename}.csv"
        
        try:
            if not data:
                raise ValueError("No data to export")
            
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=False, encoding='utf-8')
            
            logger.info(f"Exported CSV to {filepath}")
            return filepath
        
        except Exception as e:
            logger.error(f"Error exporting CSV: {str(e)}")
            raise
    
    def export_comparison_table(self, comparison_data: Dict[str, List], filename: str = None) -> Path:
        """
        Export comparison table to CSV.
        
        Args:
            comparison_data: Dictionary with 'Metric' key and stock symbols as keys
            filename: Optional filename (without extension)
            
        Returns:
            Path to exported file
        """
        if filename is None:
            filename = f"comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        filepath = self.export_dir / f"{filename}.csv"
        
        try:
            df = pd.DataFrame(comparison_data)
            df.to_csv(filepath, index=False, encoding='utf-8')
            
            logger.info(f"Exported comparison table to {filepath}")
            return filepath
        
        except Exception as e:
            logger.error(f"Error exporting comparison table: {str(e)}")
            raise
    
    def export_analysis_report(self, analysis_data: Dict[str, Any], filename: str = None) -> Path:
        """
        Export a complete analysis report to JSON.
        
        Args:
            analysis_data: Complete analysis data including stocks, metrics, AI response, etc.
            filename: Optional filename (without extension)
            
        Returns:
            Path to exported file
        """
        if filename is None:
            stocks = analysis_data.get('stocks', 'unknown')
            filename = f"report_{stocks.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Add metadata
        report = {
            'metadata': {
                'exported_at': datetime.now().isoformat(),
                'version': '1.0'
            },
            'analysis': analysis_data
        }
        
        return self.export_json(report, filename)
    
    def get_export_history(self) -> List[Dict[str, Any]]:
        """
        Get list of exported files.
        
        Returns:
            List of export file information
        """
        exports = []
        
        for filepath in sorted(self.export_dir.glob("*.*"), key=lambda p: p.stat().st_mtime, reverse=True):
            try:
                stat = filepath.stat()
                exports.append({
                    'filename': filepath.name,
                    'path': str(filepath),
                    'size_mb': round(stat.st_size / (1024 * 1024), 2),
                    'created_at': datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
            except Exception as e:
                logger.error(f"Error reading export file {filepath}: {str(e)}")
        
        return exports


# Global export manager instance
export_manager = ExportManager()
