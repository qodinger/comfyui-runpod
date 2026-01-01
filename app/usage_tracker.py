"""
Usage Tracking System for API Requests

Tracks API usage per key for billing and analytics.
"""
from __future__ import annotations
import json
import os
import time
import logging
from typing import Dict, List, Optional
from collections import defaultdict
from datetime import datetime
import folder_paths


class UsageRecord:
    """Represents a single usage record"""
    def __init__(self, key_id: str, endpoint: str, timestamp: float,
                 duration: float, success: bool, metadata: Optional[Dict] = None):
        self.key_id = key_id
        self.endpoint = endpoint
        self.timestamp = timestamp
        self.duration = duration  # in seconds
        self.success = success
        self.metadata = metadata or {}

    def to_dict(self) -> Dict:
        return {
            "key_id": self.key_id,
            "endpoint": self.endpoint,
            "timestamp": self.timestamp,
            "duration": self.duration,
            "success": self.success,
            "metadata": self.metadata
        }


class UsageTracker:
    """Tracks API usage for billing and analytics"""

    def __init__(self, max_records: int = 10000):
        self.usage_file = os.path.join(folder_paths.get_user_directory(), "api_usage.json")
        self.max_records = max_records
        self.records: List[UsageRecord] = []
        self.hourly_counts: Dict[str, Dict[int, int]] = defaultdict(lambda: defaultdict(int))
        self.load_usage()

    def load_usage(self):
        """Load usage records from disk"""
        if os.path.exists(self.usage_file):
            try:
                with open(self.usage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.records = [
                        UsageRecord(**record) for record in data.get("records", [])
                    ]
                logging.info("Loaded %d usage records", len(self.records))
            except Exception as e:
                logging.error("Failed to load usage records: %s", e)
                self.records = []

    def save_usage(self):
        """Save usage records to disk"""
        try:
            os.makedirs(os.path.dirname(self.usage_file), exist_ok=True)
            data = {
                "records": [record.to_dict() for record in self.records[-self.max_records:]]
            }
            with open(self.usage_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logging.error("Failed to save usage records: %s", e)

    def record_usage(self, key_id: str, endpoint: str, duration: float,
                     success: bool = True, metadata: Optional[Dict] = None,
                     skip_hourly_increment: bool = False):
        """
        Record an API usage event

        Args:
            key_id: The API key ID
            endpoint: The endpoint that was called
            duration: Request duration in seconds
            success: Whether the request was successful
            metadata: Additional metadata
            skip_hourly_increment: If True, don't increment hourly count (already done in rate_limit_middleware)
        """
        record = UsageRecord(
            key_id=key_id,
            endpoint=endpoint,
            timestamp=time.time(),
            duration=duration,
            success=success,
            metadata=metadata
        )

        self.records.append(record)

        # Track hourly counts for rate limiting
        # Skip if already incremented in rate_limit_middleware to prevent double-counting
        hour_key = int(record.timestamp // 3600)
        if not skip_hourly_increment:
            self.hourly_counts[key_id][hour_key] += 1

        # Clean up old hourly counts (keep last 24 hours)
        cutoff_hour = hour_key - 24
        self.hourly_counts[key_id] = {
            h: c for h, c in self.hourly_counts[key_id].items()
            if h > cutoff_hour
        }

        # Trim records if too many
        if len(self.records) > self.max_records:
            self.records = self.records[-self.max_records:]

        # Periodically save (every 10 records)
        if len(self.records) % 10 == 0:
            self.save_usage()

    def get_usage_count(self, key_id: str, hours: int = 1) -> int:
        """Get usage count for a key in the last N hours"""
        current_hour = int(time.time() // 3600)
        cutoff_hour = current_hour - hours

        total = 0
        for hour, count in self.hourly_counts[key_id].items():
            if hour >= cutoff_hour:  # Fixed: use >= to include cutoff hour
                total += count

        return total

    def increment_usage_count(self, key_id: str) -> int:
        """
        Atomically increment usage count for rate limiting.
        Returns the new count for the current hour.
        This prevents TOCTOU race conditions.
        """
        current_hour = int(time.time() // 3600)
        self.hourly_counts[key_id][current_hour] += 1
        return self.hourly_counts[key_id][current_hour]

    def get_usage_stats(self, key_id: str, days: int = 30) -> Dict:
        """Get usage statistics for a key"""
        cutoff_time = time.time() - (days * 24 * 3600)

        relevant_records = [
            r for r in self.records
            if r.key_id == key_id and r.timestamp >= cutoff_time
        ]

        if not relevant_records:
            return {
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
                "total_duration": 0,
                "average_duration": 0,
                "requests_per_day": {}
            }

        successful = sum(1 for r in relevant_records if r.success)
        total_duration = sum(r.duration for r in relevant_records)

        # Group by day
        requests_per_day = defaultdict(int)
        for record in relevant_records:
            day = datetime.fromtimestamp(record.timestamp).date().isoformat()
            requests_per_day[day] += 1

        return {
            "total_requests": len(relevant_records),
            "successful_requests": successful,
            "failed_requests": len(relevant_records) - successful,
            "total_duration": total_duration,
            "average_duration": total_duration / len(relevant_records) if relevant_records else 0,
            "requests_per_day": dict(requests_per_day)
        }

    def get_all_usage_stats(self, days: int = 30) -> Dict[str, Dict]:
        """Get usage statistics for all keys"""
        all_key_ids = set(r.key_id for r in self.records)
        return {
            key_id: self.get_usage_stats(key_id, days)
            for key_id in all_key_ids
        }
