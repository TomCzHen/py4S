import pathlib

PROJECT_ROOT = pathlib.Path(__file__).parent
CONFIG_PATH = pathlib.Path.joinpath(PROJECT_ROOT.parent, 'config', 'config.toml')
SUBSCRIBE_PATH = pathlib.Path.joinpath(PROJECT_ROOT.parent, 'config', 'subscribe.toml')
