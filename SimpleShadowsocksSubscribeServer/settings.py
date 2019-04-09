import pathlib

PROJECT_ROOT = pathlib.Path(__file__).parent
SHADOWSOCKS_TOML_PATH = pathlib.Path.joinpath(PROJECT_ROOT.parent, 'shadowsocks.toml')
