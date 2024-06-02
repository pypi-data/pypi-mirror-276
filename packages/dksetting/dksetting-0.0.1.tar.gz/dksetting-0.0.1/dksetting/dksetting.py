import json
import os

class dksetting:
    def __init__(self, file_path):
        self.file_path = file_path
        self.settings = {}
        if os.path.exists(file_path):
            self.load_settings()

    def load_settings(self):
        with open(self.file_path, 'r') as f:
            self.settings = json.load(f)

    def save_settings(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def get_setting(self, key):
        return self.settings.get(key)

    def set_setting(self, key, value):
        if isinstance(value, (int, str, bool, dict, list)):
            self.settings[key] = value
            self.save_settings()
        else:
            raise ValueError("Invalid type for setting value")

    def get_int(self, key):
        value = self.get_setting(key)
        if isinstance(value, int):
            return value
        else:
            raise TypeError(f"Expected int for key '{key}', got {type(value)}")

    def get_string(self, key):
        value = self.get_setting(key)
        if isinstance(value, str):
            return value
        else:
            raise TypeError(f"Expected str for key '{key}', got {type(value)}")

    def get_bool(self, key):
        value = self.get_setting(key)
        if isinstance(value, bool):
            return value
        else:
            raise TypeError(f"Expected bool for key '{key}', got {type(value)}")

    def get_dict(self, key):
        value = self.get_setting(key)
        if isinstance(value, dict):
            return value
        else:
            raise TypeError(f"Expected dict for key '{key}', got {type(value)}")

    def get_list(self, key):
        value = self.get_setting(key)
        if isinstance(value, list):
            return value
        else:
            raise TypeError(f"Expected list for key '{key}', got {type(value)}")

    def set_int(self, key, value):
        if isinstance(value, int):
            self.set_setting(key, value)
        else:
            raise TypeError("Expected int value")

    def set_string(self, key, value):
        if isinstance(value, str):
            self.set_setting(key, value)
        else:
            raise TypeError("Expected str value")

    def set_bool(self, key, value):
        if isinstance(value, bool):
            self.set_setting(key, value)
        else:
            raise TypeError("Expected bool value")

    def set_dict(self, key, value):
        if isinstance(value, dict):
            self.set_setting(key, value)
        else:
            raise TypeError("Expected dict value")

    def set_list(self, key, value):
        if isinstance(value, list):
            self.set_setting(key, value)
        else:
            raise TypeError("Expected list value")
