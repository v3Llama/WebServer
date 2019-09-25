import os
import yaml

DEFAULT_CONFIG = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "config.yaml"))

class Config(object):

    def load_config(self, path=DEFAULT_CONFIG):

        with open(path, "r") as config:

            self.config = yaml.safe_load(config)

    def get_param(self, name):

        return self.config[name]