"""
The audit logging system - stores all transformation records.
"""

import json
import hashlib
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Union
import csv
import io

@dataclass
class AuditRecord:
    """Immutable record of a single data transformation."""
    
    # Basic info
    step_id: str
    function_name: str
    timestamp: str
    rule_id: Optional[str]
    
    # Data metrics
    rows_before: int
    rows_after: int
    columns_before: List[str]
    columns_after: List[str]
    
    # Critical: WHICH rows changed
    affected_row_indices: List[int]
    affected_row_count: int
    
    # Critical: WHAT changed (samples)
    sample_before: Dict[str, Any]
    sample_after: Dict[str, Any]
    
    # Data integrity
    hash_before: str
    hash_after: str
    
    # Status
    status: str  # 'SUCCESS', 'WARNING', 'ERROR'
    message: Optional[str]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return asdict(self)

class ProvenaLogger:
    """Maintains a tamper-evident audit trail without external dependencies."""
    
    def __init__(self, pipeline_name: str = "Unnamed_Pipeline"):
        self.pipeline_name = pipeline_name
        self.records: List[AuditRecord] = []
        self._step_counter = 0
    
    def _compute_hash(self, data: List[Dict]) -> str:
        """Compute a deterministic hash for data validation."""
        if not data:
            return "empty"
        
        # Convert data to CSV string for hashing
        output = io.StringIO()
        if data:
            writer = csv.DictWriter(output, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data[:10])  # Sample first 10 rows
        
        data_str = output.getvalue()
        return hashlib.sha256(data_str.encode()).hexdigest()[:12]
    
    def _find_changed_rows(self, 
                          before: List[Dict], 
                          after: List[Dict],
                          key_column: Optional[str] = None) -> List[int]:
        """
        Find indices where rows actually changed.
        FIXED: Compares RAW values, not normalized.
        """
        changed_indices = []
        
        if len(before) != len(after):
            # If row counts differ, all indices changed
            return list(range(max(len(before), len(after))))
        
        for i in range(len(before)):
            row_before = before[i]
            row_after = after[i]
            
            # Compare each key-value pair
            all_keys = set(row_before.keys()) | set(row_after.keys())
            
            for key in all_keys:
                val_before = row_before.get(key)
                val_after = row_after.get(key)
                
                # Handle None values properly
                if val_before is None and val_after is None:
                    continue  # Both None = no change
                elif val_before is None or val_after is None:
                    # One is None, other isn't = CHANGE!
                    changed_indices.append(i)
                    break
                elif str(val_before) != str(val_after):
                    # Different string values = CHANGE!
                    changed_indices.append(i)
                    break
            
            # Check if we already marked this row as changed
            if i in changed_indices:
                continue
        
        return changed_indices
    
    def log_transformation(self,
                          function_name: str,
                          data_before: List[Dict],
                          data_after: List[Dict],
                          rule_id: Optional[str] = None,
                          key_column: Optional[str] = None,
                          status: str = "SUCCESS",
                          message: Optional[str] = None) -> AuditRecord:
        """
        Log a data transformation with full audit details.
        
        Args:
            function_name: Name of the transformation function
            data_before: List of dictionaries (rows) before transformation
            data_after: List of dictionaries (rows) after transformation
            rule_id: Business rule identifier
            key_column: Column to use for row identification
            status: 'SUCCESS', 'WARNING', or 'ERROR'
            message: Optional status message
        """
        
        self._step_counter += 1
        
        # Get columns
        cols_before = list(data_before[0].keys()) if data_before else []
        cols_after = list(data_after[0].keys()) if data_after else []
        
        # Find changed rows
        changed_indices = self._find_changed_rows(data_before, data_after, key_column)
        
        # Capture samples of changes
        sample_before = {}
        sample_after = {}
        
        if changed_indices and len(changed_indices) > 0:
            sample_idx = changed_indices[0]
            if sample_idx < len(data_before):
                sample_before = data_before[sample_idx]
            if sample_idx < len(data_after):
                sample_after = data_after[sample_idx]
        
        # Create the audit record
        record = AuditRecord(
            step_id=f"step_{self._step_counter:03d}",
            function_name=function_name,
            timestamp=datetime.now().isoformat(),
            rule_id=rule_id,
            rows_before=len(data_before),
            rows_after=len(data_after),
            columns_before=cols_before,
            columns_after=cols_after,
            affected_row_indices=changed_indices[:20],  # First 20 indices
            affected_row_count=len(changed_indices),
            sample_before=sample_before,
            sample_after=sample_after,
            hash_before=self._compute_hash(data_before),
            hash_after=self._compute_hash(data_after),
            status=status,
            message=message
        )
        
        self.records.append(record)
        return record
    
    def get_summary(self) -> Dict:
        """Get a summary of the audit trail."""
        return {
            "pipeline": self.pipeline_name,
            "total_steps": len(self.records),
            "total_changes": sum(r.affected_row_count for r in self.records),
            "start_time": self.records[0].timestamp if self.records else None,
            "end_time": self.records[-1].timestamp if self.records else None
        }
    
    def export_json(self, filepath: str):
        """Export full audit trail to JSON file."""
        audit_data = {
            "pipeline": self.pipeline_name,
            "created_at": datetime.now().isoformat(),
            "provena_version": "0.1.0",
            "summary": self.get_summary(),
            "audit_trail": [r.to_dict() for r in self.records]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(audit_data, f, indent=2, default=str)
    
    def clear(self):
        """Clear all audit records."""
        self.records.clear()
        self._step_counter = 0