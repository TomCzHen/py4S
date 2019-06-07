import pathlib

PROJECT_ROOT = pathlib.Path(__file__).parent
CONFIG_DIR = pathlib.Path.joinpath(PROJECT_ROOT.parent, 'config')
CONFIG_FILE = pathlib.Path.joinpath(CONFIG_DIR, 'config.toml')
SUBSCRIBE_FILE = pathlib.Path.joinpath(CONFIG_DIR, 'subscribe.toml')
