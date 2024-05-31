from colorama import init, Fore
from datetime import datetime
import argparse

from .config import Config
from .log_handler import LogHandler


init(autoreset=True)


class Logger:
    def __init__(self, config_file='logger_config.toml'):
        self._config = Config(config_file).get_config()
        self._log_handler = LogHandler(self._config)
        self.config_file = config_file
        self.level = 'INFO'

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            self.level = 'INFO'
            timestamp = datetime.now().timestamp()
            args_str = ', '.join(map(repr, args))
            kwargs_str = ', '.join(f'{k}={v!r}' for k, v in kwargs.items())
            all_args = ', '.join(filter(None, [args_str, kwargs_str]))

            
            color = Fore.RED if self.level == 'ERROR' else Fore.BLUE
            stop_color = Fore.RESET

            log_message = f'{color}[{self.level}]{stop_color} [{timestamp}] {func.__name__}({all_args})'
            self._log_handler.log_message(log_message)
            
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                self.level = 'ERROR'
                color = Fore.RED if self.level == 'ERROR' else Fore.BLUE
                stop_color = Fore.WHITE
                error_message = f'{color}[{self.level}]{stop_color} [{timestamp}] {func.__name__}({all_args}) - ERROR: {e}'
                self._log_handler.log_message(error_message)
                raise
            return result
        return wrapper

    def _create_config(self, filename):
        self._config = Config(self.config_file).create_config(filename)

    def _handle_command(self):
        parser = argparse.ArgumentParser(description='Утилита для работы с логгером')
        subparsers = parser.add_subparsers(dest='command')

        create_config_parser = subparsers.add_parser('create-config', help='Создать файл конфигурации TOML')
        create_config_parser.add_argument('filename', type=str, help='Имя файла конфигурации')

        args = parser.parse_args()

        if args.command == 'create-config':
            self._create_config(args.filename)
