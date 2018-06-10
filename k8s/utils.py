import yaml


def parse_as_yaml_file(file_name):
    with open(file_name) as f:
        config_dict = yaml.load(f)
    return config_dict

