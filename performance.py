"""
Performance monitoring utilities.
"""

import time
from functools import wraps
from typing import Callable, Dict, List
from datetime import datetime
from logger import logger, log_performance

# Performance metrics storage
_performance_metrics: List[Dict[str, any]] = []


def measure_time(func: Callable):
    """
    Decorator to measure function execution time.
    
    Args:
        func: Function to measure
        
    Returns:
        Wrapped function with timing
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            duration = time.time() - start_time
            log_performance(func.__name__, duration)
            
            # Store metric
            _performance_metrics.append({
                'function': func.__name__,
                'duration': duration,
                'timestamp': datetime.now().isoformat(),
                'args_count': len(args),
                'kwargs_count': len(kwargs)
            })
    return wrapper


def get_performance_stats() -> Dict[str, any]:
    """
    Get performance statistics.
    
    Returns:
        Dictionary with performance statistics
    """
    if not _performance_metrics:
        return {
            'total_calls': 0,
            'average_duration': 0,
            'min_duration': 0,
            'max_duration': 0,
            'functions': {}
        }
    
    durations = [m['duration'] for m in _performance_metrics]
    function_stats = {}
    
    for metric in _performance_metrics:
        func_name = metric['function']
        if func_name not in function_stats:
            function_stats[func_name] = {
                'count': 0,
                'total_duration': 0,
                'durations': []
            }
        
        function_stats[func_name]['count'] += 1
        function_stats[func_name]['total_duration'] += metric['duration']
        function_stats[func_name]['durations'].append(metric['duration'])
    
    # Calculate averages
    for func_name in function_stats:
        stats = function_stats[func_name]
        stats['average_duration'] = stats['total_duration'] / stats['count']
        stats['min_duration'] = min(stats['durations'])
        stats['max_duration'] = max(stats['durations'])
        del stats['durations']  # Remove raw durations
    
    return {
        'total_calls': len(_performance_metrics),
        'average_duration': sum(durations) / len(durations),
        'min_duration': min(durations),
        'max_duration': max(durations),
        'functions': function_stats
    }


def reset_performance_metrics():
    """Reset all performance metrics."""
    global _performance_metrics
    _performance_metrics = []
    logger.info("Performance metrics reset")


class PerformanceTimer:
    """Context manager for measuring code block performance."""
    
    def __init__(self, operation_name: str):
        self.operation_name = operation_name
        self.start_time = None
        self.duration = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.duration = time.time() - self.start_time
        log_performance(self.operation_name, self.duration)
        return False
