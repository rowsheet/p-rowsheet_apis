import yaml
import json
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

class APISpec:
    def __init__(self):
        self.config_dict = None

    def parse_config_string(self, config_string):
        # Parse the yaml string.
        fd = StringIO(config_string)
        self.config_dict = yaml.safe_load(fd)

    def parse_config_file(self, filepath):
        with open(filepath, "r") as config_file:
            config_string = config_file.read()
            self.parse_config_string(config_string)

    def get_config(self):
        return self.config_dict

    def dump_json(self):
        dump = json.dumps(self.config_dict, indent=4, sort_keys=False)
        return dump

if __name__ == "__main__":

    api_spec = APISpec()
    api_spec.parse_config_file("../api_spec/v1.yaml")
    print(api_spec.dump_json())
    exit()

    raw = """ 
    name: John
    age: 30
    """
    api_spec = APISpec()
    api_spec.parse_config_string(raw)
    print(api_spec.dump_json())
