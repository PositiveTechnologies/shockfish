import os
import sys
import argparse
from shockfish.constants import _default_config_dir
from shockfish.utils import Locator
from shockfish.configurator import Configurator

if sys.version_info < (3, 5):
        sys.exit("Python < 3.5 is not supported")

parser = argparse.ArgumentParser()
parser.add_argument("--config", "-c", 
    action="store",
    help="Config file." )

args = parser.parse_args()
config_path = ""

if args.config:
    config_path = args.config
else:
    for loc in os.curdir, os.path.expanduser("~"), _default_config_dir:
        path = os.path.join(loc,"shockfish.json")
        if os.path.isfile(path):
            config_path = path
            break
    else:
        print("Shockfish config file not found")
        logger.debug("Shockfish config file not found")
        sys.exit(1)


config = Configurator(config_path)
Locator.load("Config", config)

from shockfish.core import runProxy
runProxy()
