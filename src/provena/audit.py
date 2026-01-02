"""
The @audit_trail decorator - adds automatic logging to any function.
"""

import functools
import copy
from typing import Callable, Any, Optional, List, Dict
from .logger import ProvenaLogger

def audit_trail(rule_id: Optional[str] = None):
    """
    Decorator that automatically logs data transformations.
    
    Args:
        rule_id: Business rule identifier (e.g., 'GDPR_MASKING_v1')
    
    Example:
        @audit_trail(rule_id='EMAIL_VALIDATION')
        def clean_emails(data):
            # Your cleaning logic
            return data
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(data: List[Dict], *args, **kwargs):
            # Extract logger from kwargs or create default
            logger = kwargs.pop('provena_logger', None)
            if logger is None:
                logger = ProvenaLogger(pipeline_name=func.__name__)
            
            # Make a DEEP copy of the data before transformation
            data_before = copy.deepcopy(data)  # CRITICAL: Deep copy!
            
            # Execute the transformation
            try:
                # Pass a COPY to the function, not the original
                data_after = func(copy.deepcopy(data), *args, **kwargs)
                status = "SUCCESS"
                message = None
            except Exception as e:
                # If transformation fails, log the error
                data_after = data_before
                status = "ERROR"
                message = f"Transformation failed: {str(e)}"
            
            # Log the transformation
            logger.log_transformation(
                function_name=func.__name__,
                data_before=data_before,  # Original unchanged data
                data_after=data_after,    # Result after transformation
                rule_id=rule_id,
                status=status,
                message=message
            )
            
            # Return the result
            return data_after
        return wrapper
    return decorator

def audit_pipeline(pipeline_name: str = "Data_Pipeline"):
    """
    Context manager for running multiple transformations in a pipeline.
    
    Example:
        with audit_pipeline("Customer_Cleaning") as logger:
            data = step1(data, provena_logger=logger)
            data = step2(data, provena_logger=logger)
        # logger contains full audit trail
    """
    class PipelineContext:
        def __init__(self, name):
            self.logger = ProvenaLogger(name)
            self.data = None
        
        def __enter__(self):
            return self.logger
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            # Export audit trail automatically
            if self.logger.records:
                filename = f"{self.logger.pipeline_name}_audit.json"
                self.logger.export_json(filename)
                print(f"📁 Audit trail saved to: {filename}")
    
    return PipelineContext(pipeline_name)