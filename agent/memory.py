"""Persistence layer for LeetCode Auto-Solver using JSON storage"""

import json
import os
from datetime import datetime, timezone
from typing import Optional, Dict, List
import threading
import logging

logger = logging.getLogger(__name__)


class MemoryStore:
    """JSON-based hash map for solved problems"""
    
    def __init__(self, file_path: str):
        """Initialize JSON database
        
        Args:
            file_path: Path to problems.json file
        """
        self.file_path = file_path
        self.lock = threading.Lock()  # Thread-safe operations
        self._ensure_file_exists()
        logger.info(f"Memory store initialized at {file_path}")
    
    def _ensure_file_exists(self):
        """Create empty JSON file if not exists"""
        if not os.path.exists(self.file_path):
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            with open(self.file_path, 'w') as f:
                json.dump({}, f)
            logger.info(f"Created new memory file: {self.file_path}")
    
    def get(self, problem_slug: str) -> Optional[Dict]:
        """Retrieve problem record by slug
        
        Args:
            problem_slug: LeetCode problem identifier (e.g., 'two-sum')
        
        Returns:
            dict or None: Problem record if exists, else None
            {
                "slug": str,
                "status": "pass" | "fail" | "timeout",
                "code": str,
                "timestamp": str (ISO 8601),
                "attempts": int
            }
        """
        try:
            with self.lock:
                with open(self.file_path, 'r') as f:
                    data = json.load(f)
                result = data.get(problem_slug)
                if result:
                    logger.info(f"Found cached solution for {problem_slug}")
                return result
        except Exception as e:
            logger.error(f"Error reading memory for {problem_slug}: {e}")
            return None
    
    def save(self, problem_slug: str, status: str, code: str, attempts: int = 1) -> bool:
        """Save or update problem record
        
        Args:
            problem_slug: Problem identifier
            status: 'pass', 'fail', or 'timeout'
            code: Python solution code
            attempts: Number of generation attempts
        
        Returns:
            bool: True if save successful
        
        Raises:
            ValueError: If status not in valid enum
        """
        if status not in ["pass", "fail", "timeout"]:
            raise ValueError(f"Invalid status: {status}")
        
        record = {
            "slug": problem_slug,
            "status": status,
            "code": code,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "attempts": attempts
        }
        
        try:
            with self.lock:
                with open(self.file_path, 'r') as f:
                    data = json.load(f)
                data[problem_slug] = record
                with open(self.file_path, 'w') as f:
                    json.dump(data, f, indent=2)
            logger.info(f"Saved {problem_slug}: {status} (attempts: {attempts})")
            return True
        except Exception as e:
            logger.error(f"Error saving memory for {problem_slug}: {e}")
            return False
    
    def get_all_solved(self) -> List[Dict]:
        """Get all problems with status='pass'
        
        Returns:
            list: List of solved problem records
        """
        try:
            with self.lock:
                with open(self.file_path, 'r') as f:
                    data = json.load(f)
            return [v for v in data.values() if v["status"] == "pass"]
        except Exception as e:
            logger.error(f"Error getting solved problems: {e}")
            return []
    
    def get_stats(self) -> Dict:
        """Get solving statistics
        
        Returns:
            dict: {
                "total": int,
                "solved": int,
                "failed": int,
                "timeout": int,
                "success_rate": float
            }
        """
        try:
            with self.lock:
                with open(self.file_path, 'r') as f:
                    data = json.load(f)
            
            total = len(data)
            solved = sum(1 for v in data.values() if v["status"] == "pass")
            failed = sum(1 for v in data.values() if v["status"] == "fail")
            timeout = sum(1 for v in data.values() if v["status"] == "timeout")
            
            return {
                "total": total,
                "solved": solved,
                "failed": failed,
                "timeout": timeout,
                "success_rate": solved / total if total > 0 else 0.0
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {
                "total": 0,
                "solved": 0,
                "failed": 0,
                "timeout": 0,
                "success_rate": 0.0
            }
