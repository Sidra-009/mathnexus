"""
Generate human-readable audit reports.
"""

import json
from datetime import datetime
from typing import List
from .logger import ProvenaLogger, AuditRecord

def _get_status_emoji(status: str) -> str:
    """Get emoji for status."""
    emoji_map = {
        "SUCCESS": "✅",
        "WARNING": "⚠️",
        "ERROR": "❌"
    }
    return emoji_map.get(status, "🔹")

def generate_terminal_report(logger: ProvenaLogger) -> str:
    """
    Generate a clean, terminal-friendly audit report.
    
    Returns:
        Formatted string ready to print
    """
    lines = []
    
    # Header
    lines.append("=" * 70)
    lines.append(f"🚀 PROVENA AUDIT REPORT: {logger.pipeline_name}")
    lines.append("=" * 70)
    
    # Summary
    summary = logger.get_summary()
    lines.append(f"\n📊 SUMMARY")
    lines.append(f"   • Steps: {summary['total_steps']}")
    lines.append(f"   • Total Changes: {summary['total_changes']} rows")
    if summary['start_time']:
        lines.append(f"   • Started: {summary['start_time'][:19]}")
    
    lines.append("-" * 70)
    
    # Detailed steps
    for i, record in enumerate(logger.records, 1):
        emoji = _get_status_emoji(record.status)
        
        lines.append(f"\n[{i}] {emoji} {record.function_name}")
        lines.append(f"   • Status: {record.status}")
        lines.append(f"   • Time: {record.timestamp[11:19]}")
        
        if record.rule_id:
            lines.append(f"   • Rule: {record.rule_id}")
        
        lines.append(f"   • Rows: {record.rows_before} → {record.rows_after}")
        
        if record.affected_row_count > 0:
            lines.append(f"   • Changed: {record.affected_row_count} rows")
            
            # Show sample of changed indices
            if record.affected_row_indices:
                indices_str = ", ".join(str(idx) for idx in record.affected_row_indices[:5])
                if len(record.affected_row_indices) > 5:
                    indices_str += f" (+{len(record.affected_row_indices)-5} more)"
                lines.append(f"   • Rows: [{indices_str}]")
            
            # Show sample changes
            if record.sample_before and record.sample_after:
                for key in record.sample_before:
                    if key in record.sample_after:
                        before_val = record.sample_before[key]
                        after_val = record.sample_after[key]
                        if before_val != after_val:
                            # Truncate long values
                            before_str = str(before_val)
                            after_str = str(after_val)
                            if len(before_str) > 20:
                                before_str = before_str[:17] + "..."
                            if len(after_str) > 20:
                                after_str = after_str[:17] + "..."
                            lines.append(f"   • Sample: {key} = {before_str} → {after_str}")
        
        if record.message:
            lines.append(f"   • Note: {record.message}")
    
    # Footer
    lines.append("\n" + "=" * 70)
    lines.append(f"📁 Export: provena export {logger.pipeline_name}.json")
    lines.append("=" * 70)
    
    return "\n".join(lines)

def generate_json_report(logger: ProvenaLogger, filepath: str = None) -> str:
    """
    Generate a machine-readable JSON report.
    
    Args:
        logger: The ProvenaLogger instance
        filepath: Optional path to save the file
    
    Returns:
        JSON string
    """
    report = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "provena_version": "0.1.0",
            "report_type": "audit_trail"
        },
        "pipeline": logger.pipeline_name,
        "summary": logger.get_summary(),
        "steps": [r.to_dict() for r in logger.records]
    }
    
    json_str = json.dumps(report, indent=2, default=str)
    
    if filepath:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(json_str)
    
    return json_str