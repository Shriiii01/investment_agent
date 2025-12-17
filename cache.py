"""
Caching utilities for the Investment Agent application.
"""

import hashlib
import json
import pickle
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional
from config import CACHE_DURATION
from logger import get_logger

logger = get_logger("cache")

# Create cache directory
CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)


class CacheManager:
    """Manages caching for API calls and data retrieval."""
    
    def __init__(self, duration: int = CACHE_DURATION):
        """
        Initialize cache manager.
        
        Args:
            duration: Cache duration in seconds
        """
        self.duration = duration
        self.cache_dir = CACHE_DIR
    
    def _get_cache_key(self, key: str) -> str:
        """Generate a cache key hash."""
        return hashlib.md5(key.encode()).hexdigest()
    
    def _get_cache_path(self, key: str) -> Path:
        """Get the cache file path for a key."""
        cache_key = self._get_cache_key(key)
        return self.cache_dir / f"{cache_key}.cache"
    
    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve a value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found/expired
        """
        cache_path = self._get_cache_path(key)
        
        if not cache_path.exists():
            return None
        
        try:
            with open(cache_path, 'rb') as f:
                cache_data = pickle.load(f)
            
            # Check if cache is expired
            if datetime.now() > cache_data['expires_at']:
                cache_path.unlink()  # Delete expired cache
                logger.debug(f"Cache expired for key: {key}")
                return None
            
            logger.debug(f"Cache hit for key: {key}")
            return cache_data['value']
        
        except Exception as e:
            logger.error(f"Error reading cache for key {key}: {str(e)}")
            return None
    
    def set(self, key: str, value: Any) -> bool:
        """
        Store a value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            
        Returns:
            True if successful, False otherwise
        """
        cache_path = self._get_cache_path(key)
        
        try:
            cache_data = {
                'value': value,
                'created_at': datetime.now(),
                'expires_at': datetime.now() + timedelta(seconds=self.duration)
            }
            
            with open(cache_path, 'wb') as f:
                pickle.dump(cache_data, f)
            
            logger.debug(f"Cached value for key: {key}")
            return True
        
        except Exception as e:
            logger.error(f"Error writing cache for key {key}: {str(e)}")
            return False
    
    def clear(self, key: Optional[str] = None) -> bool:
        """
        Clear cache entry or all cache.
        
        Args:
            key: Specific cache key to clear, or None to clear all
            
        Returns:
            True if successful
        """
        try:
            if key:
                cache_path = self._get_cache_path(key)
                if cache_path.exists():
                    cache_path.unlink()
                    logger.debug(f"Cleared cache for key: {key}")
            else:
                # Clear all cache files
                for cache_file in self.cache_dir.glob("*.cache"):
                    cache_file.unlink()
                logger.debug("Cleared all cache")
            return True
        
        except Exception as e:
            logger.error(f"Error clearing cache: {str(e)}")
            return False
    
    def get_stats(self) -> dict:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        cache_files = list(self.cache_dir.glob("*.cache"))
        total_size = sum(f.stat().st_size for f in cache_files)
        
        active_count = 0
        expired_count = 0
        
        for cache_file in cache_files:
            try:
                with open(cache_file, 'rb') as f:
                    cache_data = pickle.load(f)
                if datetime.now() <= cache_data['expires_at']:
                    active_count += 1
                else:
                    expired_count += 1
            except:
                expired_count += 1
        
        return {
            'total_files': len(cache_files),
            'active_entries': active_count,
            'expired_entries': expired_count,
            'total_size_mb': round(total_size / (1024 * 1024), 2)
        }


# Global cache instance
cache_manager = CacheManager()
