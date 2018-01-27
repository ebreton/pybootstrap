import os
import yaml
import logging


def yaml_file_to_dict(config_file, base_config=None):
    """ Adds extra configuration information to given base_config """
    # validate input
    base_config = base_config or {}
    if not os.path.exists(config_file):
        raise SystemExit("Extra config file not found: {}".format(config_file))

    # load config from yaml
    extra_config = yaml.load(open(config_file, 'r'))

    # return base config enriched (and overriden) with yaml config
    return {**base_config, **extra_config}


def yaml_include():
    """ Defining necessary to allow usage of "!include" in YAML files.
    Given path to include file can be relative to :
    - Python script location
    - YAML file from which "include" is done

    This can be use to include a value for a key. This value can be just a string or a complex (hiearchical)
    YAML file.
    Ex:
    my_key: !include file/with/value.yml
    """
    def _yaml_loader(loader, node):
        local_file = os.path.join(os.path.dirname(loader.stream.name), node.value)

        # if file to include exists with given valu
        if os.path.exists(node.value):
            include_file = node.value
        # if file exists with relative path to current YAML file
        elif os.path.exists(local_file):
            include_file = local_file
        else:
            error_message = "YAML include in '{}' - file to include doesn't exists: {}".format(
                loader.stream.name, node.value)
            logging.error(error_message)
            raise ValueError(error_message)

        with open(include_file) as inputfile:
            return yaml.load(inputfile)

    return _yaml_loader


def yaml_from_csv(csv_dict):
    """
    Defining necessary to retrieve a value (given by field name) from a dict

    Ex (in YAML file):
    my_key: !from_csv field_name
    """
    def _yaml_loader(loader, node, csv_dict=csv_dict):
        # If value not exists, store the error
        if csv_dict.get(node.value, None) is None:
            logging.error(
                "YAML file CSV reference '%s' missing. Can be given with option \
                '--extra-config=<YAML>'. YAML content example: '%s: <value>'",
                node.value,
                node.value)
            # We don't replace value because we can't...
            return node.value
        else:
            # No error, we return the value
            return csv_dict[node.value]

    return _yaml_loader
