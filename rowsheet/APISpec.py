import yaml
import json
import os
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

class APISpec:
    def __init__(self, api_dir):
        self.spec = None
        spec_files = [f for f in os.listdir(api_dir) if f.endswith('.yaml')]
        for spec_file in spec_files:
            self.parse_config_file(os.path.join(api_dir, spec_file))

    def parse_config_string(self, version, config_string):
        fd = StringIO(config_string)
        loaded = yaml.safe_load(fd)
        if self.spec is None:
            self.spec = {}
        self.spec[version] = loaded

    def parse_config_file(self, filepath):
        version = os.path.basename(filepath).split(".")[0]
        with open(filepath, "r") as config_file:
            config_string = config_file.read()
            self.parse_config_string(version, config_string)

    def get_config(self):
        return self.spec

    def dump_json(self):
        dump = json.dumps(self.spec, indent=4, sort_keys=False)
        return dump

if __name__ == "__main__":

    api_spec = APISpec("../api/")
    print(api_spec.dump_json())
    exit()

    raw = """ 
    name: John
    age: 30
    """
    api_spec = APISpec()
    api_spec.parse_config_string(raw)
    print(api_spec.dump_json())
