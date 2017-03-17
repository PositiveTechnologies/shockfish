import logging
import json
import sys

class Configurator(object):
    """ Configuration. """

    def __init__(self, filename):
        """ Initialize config. """
        config = self._read_config(filename)
        self._logger = logging.getLogger(__name__)
        self._init_logger(config)
        self.backend = self._get_backend(config)
        self.protectors = self._get_protectors(config)
        self.virtualServer = self._get_virtualServer(config)
        self.sources = self._get_sources(config)

    def _read_config(self, filename):
        try:
            with open(filename) as json_data_file:
                data = json.load(json_data_file)
        except IOError as err:
            print(err)
            sys.exit(1)
        return data

    def _init_logger(self, config):
            """ Initialize logger. """
            config_log_level = config["logs"]["level"].upper()
            log_level = getattr(logging, config_log_level)
            logging.basicConfig(
                filename=config["logs"]["file"],
                level=log_level,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )

    def _get_virtualServer(self, config):
        """ Read and retun configuration. """
        return {
            "interface": config["virtual"]["interface"] or "localhost",
            "port": int(config["virtual"]["port"]) or 8080
        }

    def _get_protectors(self, config):
        """ Read and retun configuration. """
        protectors = {}
        for item, value in config.get("protectors").items():
            protectors[item] = value
        return protectors

    def _get_backend(self, config):
        return  {
            "host": config["backend"]["host"],
            "port": int(config["backend"]["port"]) or 80
        }

    def _get_sources(self, config):
        return  config.get("sources")
