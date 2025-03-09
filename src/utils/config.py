import json
import os
from src.utils.logger import log_activity

class ConfigManager:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config = self._load_config()

    def _load_config(self):
        """Load configuration from file"""
        if not os.path.exists(self.config_file):
            self._create_default_config()
            
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            log_activity(f"Error loading config: {str(e)}", level="error")
            return {}

    def _create_default_config(self):
        """Create default configuration file"""
        self.config = {
            "database": {
                "path": "fitness_inventory.db"
            },
            "email": {
                "smtp_server": "smtp.example.com",
                "smtp_port": 587,
                "email": "admin@example.com",
                "password": ""
            },
            "backup": {
                "directory": "backups",
                "frequency": "daily"
            }
        }
        self.save_config()

    def get(self, key, default=None):
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        try:
            for k in keys:
                value = value[k]
            return value
        except KeyError:
            return default

    def set(self, key, value):
        """Set configuration value"""
        keys = key.split('.')
        current = self.config
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        current[keys[-1]] = value
        self.save_config()

    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
            return True
        except Exception as e:
            log_activity(f"Error saving config: {str(e)}", level="error")
            return False
