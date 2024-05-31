import toml
import os


class Config:
    def __init__(self, config_file='logger_config.toml'):
        self._config_file = config_file
        self._config = {}
        self._load_config()

    def _load_config(self):
        if os.path.exists(self._config_file):
            self._config = toml.load(self._config_file)
        else:
            self._config = {
                'logger': {
                    'filename': 'app.log',
                    'max_bytes': 100000,
                    'backup_count': 1
                }
            }

    def _save_config(self):
        with open(self._config_file, 'w') as f:
            toml.dump(self._config, f)

    def create_config(self, filename):
        self._config = {
            'logger': {
                'filename': filename,
                'max_bytes': 0,
                'backup_count': 0
            }
        }
        self._save_config()

    def get_config(self):
        return self._config