"""
API Key Management System for ComfyUI API

Provides API key generation, validation, and management for external API access.
"""
from __future__ import annotations
import json
import os
import secrets
import hashlib
import time
import logging
from typing import Optional, Dict, List
import folder_paths


class APIKey:
    """Represents an API key with metadata"""
    def __init__(self, key_id: str, key_hash: str, name: str, created_at: float,
                 last_used: Optional[float] = None, rate_limit: int = 100,
                 is_active: bool = True, metadata: Optional[Dict] = None):
        self.key_id = key_id
        self.key_hash = key_hash
        self.name = name
        self.created_at = created_at
        self.last_used = last_used
        self.rate_limit = rate_limit  # requests per hour
        self.is_active = is_active
        self.metadata = metadata or {}

    def to_dict(self, include_hash: bool = False) -> Dict:
        """Convert to dictionary for storage/API response"""
        result = {
            "key_id": self.key_id,
            "name": self.name,
            "created_at": self.created_at,
            "last_used": self.last_used,
            "rate_limit": self.rate_limit,
            "is_active": self.is_active,
            "metadata": self.metadata
        }
        if include_hash:
            result["key_hash"] = self.key_hash
        return result

    @classmethod
    def from_dict(cls, data: Dict) -> 'APIKey':
        """Create APIKey from dictionary"""
        return cls(
            key_id=data["key_id"],
            key_hash=data["key_hash"],
            name=data["name"],
            created_at=data["created_at"],
            last_used=data.get("last_used"),
            rate_limit=data.get("rate_limit", 100),
            is_active=data.get("is_active", True),
            metadata=data.get("metadata", {})
        )


class APIKeyManager:
    """Manages API keys for external API access"""

    def __init__(self):
        self.keys_file = os.path.join(folder_paths.get_user_directory(), "api_keys.json")
        self.keys: Dict[str, APIKey] = {}
        self.load_keys()

    def load_keys(self):
        """Load API keys from disk"""
        if os.path.exists(self.keys_file):
            try:
                with open(self.keys_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.keys = {
                        key_id: APIKey.from_dict(key_data)
                        for key_id, key_data in data.items()
                    }
                logging.info("Loaded %d API keys", len(self.keys))
            except Exception as e:
                logging.error("Failed to load API keys: %s", e)
                self.keys = {}
        else:
            self.keys = {}

    def save_keys(self):
        """Save API keys to disk"""
        try:
            os.makedirs(os.path.dirname(self.keys_file), exist_ok=True)
            data = {
                key_id: key.to_dict(include_hash=True)
                for key_id, key in self.keys.items()
            }
            with open(self.keys_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logging.error("Failed to save API keys: %s", e)

    def generate_key(self, name: str, rate_limit: int = 100,
                    metadata: Optional[Dict] = None) -> tuple[str, str]:
        """
        Generate a new API key

        Returns:
            tuple: (key_id, plaintext_key) - The plaintext key is only shown once
        """
        # Generate a secure random key
        plaintext_key = f"comfy_{secrets.token_urlsafe(32)}"

        # Hash the key for storage (using SHA-256)
        key_hash = hashlib.sha256(plaintext_key.encode()).hexdigest()

        # Generate a unique key ID
        key_id = secrets.token_urlsafe(16)

        # Create APIKey object
        api_key = APIKey(
            key_id=key_id,
            key_hash=key_hash,
            name=name,
            created_at=time.time(),
            rate_limit=rate_limit,
            is_active=True,
            metadata=metadata or {}
        )

        self.keys[key_id] = api_key
        self.save_keys()

        logging.info("Generated new API key: %s (ID: %s)", name, key_id)
        return key_id, plaintext_key

    def validate_key(self, api_key: str) -> Optional[APIKey]:
        """
        Validate an API key and return the APIKey object if valid

        Args:
            api_key: The plaintext API key to validate

        Returns:
            APIKey object if valid, None otherwise
        """
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()

        for key in self.keys.values():
            if key.key_hash == key_hash and key.is_active:
                # Update last used timestamp
                key.last_used = time.time()
                self.save_keys()
                return key

        return None

    def get_key(self, key_id: str) -> Optional[APIKey]:
        """Get an API key by ID"""
        return self.keys.get(key_id)

    def list_keys(self) -> List[Dict]:
        """List all API keys (without hashes)"""
        return [key.to_dict() for key in self.keys.values()]

    def delete_key(self, key_id: str) -> bool:
        """Delete an API key"""
        if key_id in self.keys:
            del self.keys[key_id]
            self.save_keys()
            logging.info("Deleted API key: %s", key_id)
            return True
        return False

    def update_key(self, key_id: str, name: Optional[str] = None,
                   rate_limit: Optional[int] = None,
                   is_active: Optional[bool] = None) -> bool:
        """Update an API key's properties"""
        if key_id not in self.keys:
            return False

        key = self.keys[key_id]
        if name is not None:
            key.name = name
        if rate_limit is not None:
            key.rate_limit = rate_limit
        if is_active is not None:
            key.is_active = is_active

        self.save_keys()
        return True
