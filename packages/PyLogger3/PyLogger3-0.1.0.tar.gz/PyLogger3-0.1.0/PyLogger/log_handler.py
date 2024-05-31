import os



class LogHandler:
    def __init__(self, config):
        self._config = config

    def log_message(self, message):
        if self._check_file_size():
            self._rotate_logs()
        with open(self._config['logger']['filename'], 'a') as f:
            f.write(message + '\n')

    def _check_file_size(self):
        filename = self._config['logger']['filename']
        max_bytes = self._config['logger'].get('max_bytes', 0)
        if os.path.exists(filename):
            return os.path.getsize(filename) >= max_bytes
        return False

    def _rotate_logs(self):
        filename = self._config['logger']['filename']
        backup_count = self._config['logger'].get('backup_count', 0)
        if backup_count > 0:
            for i in range(backup_count - 1, 0, -1):
                if os.path.exists(f"{filename}.{i}"):
                    os.rename(f"{filename}.{i}", f"{filename}.{i + 1}")
            if os.path.exists(filename):
                os.rename(filename, f"{filename}.1")