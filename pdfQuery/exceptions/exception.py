import sys
from pathlib import Path


def error_message_detail(error, error_detail: sys = None) -> str:
    """
    Extract detailed error information from exception traceback.
    
    Args:
        error: The exception/error message
        error_detail: sys module (optional, defaults to sys if None)
    
    Returns:
        str: Formatted error message with file, line number, and error details
    """
    if error_detail is None:
        error_detail = sys
    
    try:
        _, _, exc_tb = error_detail.exc_info()
        if exc_tb is None:
            return f"Error: {str(error)} (No traceback available)"
        
        # Get the most recent frame in the traceback
        file_name = Path(exc_tb.tb_frame.f_code.co_filename).name
        line_number = exc_tb.tb_lineno
        
        error_message = (
            f"Error in Python script '{file_name}' at line {line_number}: {str(error)}"
        )
        
        return error_message
        
    except Exception as e:
        return f"Error: {str(error)} (Failed to extract traceback: {str(e)})"


class PDFQueryException(Exception):
    """
    Custom exception class for PDF querying operations.
    
    Provides detailed error information including file location and line numbers
    to help with debugging PDF processing issues.
    """
    
    def __init__(self, error_message, error_detail: sys = None):
        """
        Initialize the QueryPdfException.
        
        Args:
            error_message (str): Error message describing what went wrong
            error_detail (sys, optional): sys module for traceback extraction
        """
        super().__init__(error_message)
        
        self.original_message = error_message
        self.error_message = error_message_detail(
            error_message, error_detail=error_detail
        )
    
    def __str__(self):
        return self.error_message
    
    def __repr__(self):
        return f"QueryPdfException('{self.original_message}')"
    
    def get_original_message(self):
        """Return the original error message without formatting."""
        return self.original_message
    
    def get_detailed_message(self):
        """Return the detailed error message with traceback info."""
        return self.error_message

