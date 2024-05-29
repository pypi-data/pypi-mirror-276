from palimpzest.constants import PZ_DIR

import os
import sys
import tempfile
import yaml


class Config:
    def __init__(self, name: str="default", llmservice: str="openai", parallel: bool=False):
        self.configfilepath = os.path.join(PZ_DIR, f"config_{name}.yaml")
        if not os.path.exists(PZ_DIR):
            raise Exception(f"Target config directory does not exist at {PZ_DIR} :: Something is wrong with the installation.")

        if not os.path.exists(self.configfilepath):
            # Get the system's temporary directory
            temp_dir = tempfile.gettempdir()
            pz_file_cache_dir = os.path.join(temp_dir, "pz")
            self.config = {"name": name, "llmservice": llmservice, "parallel": parallel, "filecachedir": pz_file_cache_dir}
            self._save_config()

        self.config = self._load_config()
        if not "filecachedir" in self.config:
            # Get the system's temporary directory
            temp_dir = tempfile.gettempdir()
            pz_file_cache_dir = os.path.join(temp_dir, "pz")
            self.config["filecachedir"] = pz_file_cache_dir
            self._save_config()

        self.name = self.config['name']

    def get(self, key, default=None):
        return self.config[key] if key in self.config else default

    def set(self, key, value):
        self.config[key] = value
        self._save_config()

    def set_current_config(self):
        current_config_dict = {"current_config_name": self.name}
        current_config_path = os.path.join(PZ_DIR, "current_config.yaml")
        with open(current_config_path, 'w') as f:
            yaml.dump(current_config_dict, f)

    def remove_config(self):
        # check to ensure you don't delete default config
        if self.name == "default":
            raise Exception("Cannot remove default config.")

        # reset current config if this config was the current config
        current_config_path = os.path.join(PZ_DIR, "current_config.yaml")
        current_config_dict = {}
        with open(current_config_path, 'r') as f:
            current_config_dict = yaml.safe_load(f)

        if current_config_dict["current_config_name"] == self.name:
            current_config_dict["current_config_name"] = "default"
    
            with open(current_config_path, 'w') as f:
                yaml.dump(current_config_dict, f)

        # delete config file
        os.remove(self.configfilepath)

    def _load_config(self):
        """Load YAML configuration from the specified path."""
        try:
            with open(self.configfilepath, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            print(f"Error loading configuration file: {e}")
            sys.exit(1)

    def _save_config(self):
        """Save the configuration to the specified path."""
        try:
            with open(self.configfilepath, 'w') as file:
                yaml.dump(self.config, file)
        except Exception as e:
            print(f"Error saving configuration file: {e}")
            sys.exit(1)
