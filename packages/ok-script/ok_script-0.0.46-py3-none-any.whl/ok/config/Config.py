from ok.gui.Communicate import communicate
from ok.util.json import read_json_file, write_json_file
from ok.util.path import get_path_relative_to_exe


class Config:
    def __init__(self, default, folder, name, validator=None):
        super().__init__()
        self.default = default
        self.validator = validator
        self.config_file = get_path_relative_to_exe(folder, f"{name}.json")
        self.config = read_json_file(self.config_file)
        if self.config is None:
            self.config = default
        elif self.verify_config(self.config, default):
            self.save_file()

    def save_file(self):
        write_json_file(self.config_file, self.config)

    def reset_to_default(self):
        self.config.clear()
        self.update(self.default)
        self.save_file()

    def update(self, *args, **kwargs):
        self.config.update(*args, **kwargs)
        self.save_file()

    def get(self, key, default=None):
        return self.config.get(key, default)

    def keys(self):
        return self.config.keys()

    def values(self):
        return self.config.values()

    def items(self):
        return self.config.items()

    def pop(self, key, default=None):
        result = self.config.pop(key, default)
        self.save_file()
        return result

    def popitem(self):
        result = self.config.popitem()
        self.save_file()
        return result

    def setdefault(self, key, default=None):
        result = self.config.setdefault(key, default)
        self.save_file()
        return result

    def clear(self):
        self.config.clear()
        self.save_file()

    def __len__(self):
        return len(self.config)

    def __setitem__(self, key, value):
        if self.validate(key, value):
            self.config[key] = value
            self.save_file()

    def __getitem__(self, key):
        return self.config[key]

    def validate(self, key, value):
        if self.validator is not None:
            valid, message = self.validator(key, value)
            if not valid:
                communicate.config_validation.emit(message)
                return False
        return True

    def verify_config(self, config, default_config):
        modified = False

        # Remove entries that do not exist in default_config
        for key in list(config.keys()):
            if key not in default_config:
                del config[key]
                modified = True

        # Check entries in default_config
        for key, default_value in default_config.items():
            if key not in config or (default_value is not None and type(config[key]) != type(default_value)):
                config[key] = default_value
                modified = True
            elif self.validator is not None:
                valid = self.validate(key, self.config[key])
                if not valid:
                    config[key] = default_value
                    modified = True

        return not modified
