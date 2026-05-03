"""
Configuration management for GitBob Assistant
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv


class Config:
    """Configuration manager for GitBob Assistant"""
    
    DEFAULT_CONFIG_PATH = Path.home() / ".gitbob" / "config.yaml"
    
    DEFAULT_CONFIG = {
        "ibm_bob": {
            "api_key": "FMq72sTULUh1_f25NR7Qjd23IrsTKxnXj_sAKUYX7A72",
            "endpoint": "https://api.ibm.com/bob/v1",
            "model": "bob-large",
            "timeout": 30,
            "max_retries": 3,
        },
        "git": {
            "default_branch": "main",
            "branch_prefixes": ["feature/", "bugfix/", "hotfix/", "chore/"],
        },
        "commit": {
            "conventional_commits": True,
            "max_subject_length": 72,
            "max_body_length": 100,
            "include_scope": True,
            "types": ["feat", "fix", "docs", "style", "refactor", "test", "chore"],
        },
        "pr": {
            "template": "default",
            "include_checklist": True,
            "auto_link_issues": True,
            "sections": ["Summary", "Changes", "Testing", "Related Issues"],
        },
        "cache": {
            "enabled": True,
            "ttl": 3600,
            "directory": str(Path.home() / ".gitbob" / "cache"),
            "max_size_mb": 50,
        },
        "output": {
            "color": True,
            "verbose": False,
            "show_diff": True,
        },
    }
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize configuration
        
        Args:
            config_path: Path to configuration file. If None, uses default location.
        """
        load_dotenv()  # Load environment variables from .env file
        
        self.config_path = config_path or self.DEFAULT_CONFIG_PATH
        self.config = self._load_config()
        self._resolve_env_vars()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or use defaults"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    user_config = yaml.safe_load(f) or {}
                return self._merge_configs(self.DEFAULT_CONFIG, user_config)
            except Exception as e:
                print(f"Warning: Failed to load config from {self.config_path}: {e}")
                print("Using default configuration")
        
        return self.DEFAULT_CONFIG.copy()
    
    def _merge_configs(self, default: Dict, user: Dict) -> Dict:
        """Recursively merge user config with defaults"""
        result = default.copy()
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        return result
    
    def _resolve_env_vars(self):
        """Resolve environment variables in configuration"""
        # Resolve IBM Bob API key from environment
        api_key = self.config["ibm_bob"].get("api_key")
        if api_key and api_key.startswith("${") and api_key.endswith("}"):
            env_var = api_key[2:-1]
            self.config["ibm_bob"]["api_key"] = os.getenv(env_var)
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """Get configuration value using dot notation
        
        Args:
            key_path: Configuration key path (e.g., "ibm_bob.api_key")
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key_path.split(".")
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any):
        """Set configuration value using dot notation
        
        Args:
            key_path: Configuration key path (e.g., "ibm_bob.api_key")
            value: Value to set
        """
        keys = key_path.split(".")
        config = self.config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
    
    def save(self):
        """Save configuration to file"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
    
    def ensure_cache_dir(self) -> Path:
        """Ensure cache directory exists and return path"""
        cache_dir = Path(self.get("cache.directory"))
        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir
    
    def validate(self) -> bool:
        """Validate configuration
        
        Returns:
            True if configuration is valid, False otherwise
        """
        # Check if API key is set
        api_key = self.get("ibm_bob.api_key")
        if not api_key:
            print("Error: IBM Bob API key not configured")
            print("Set IBM_BOB_API_KEY environment variable or configure in config.yaml")
            return False
        
        return True


# Global configuration instance
_config: Optional[Config] = None


def get_config(config_path: Optional[Path] = None) -> Config:
    """Get global configuration instance
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Configuration instance
    """
    global _config
    if _config is None:
        _config = Config(config_path)
    return _config


def reset_config():
    """Reset global configuration instance"""
    global _config
    _config = None

# Made with Bob
