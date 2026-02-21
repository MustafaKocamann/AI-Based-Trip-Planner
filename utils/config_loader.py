import os
import yaml


def load_config(config_path: str = None) -> dict:
    """
    Load and return the YAML configuration file.

    Args:
        config_path: Absolute or relative path to the config YAML file.
                     Defaults to <project_root>/config/config.yaml.

    Returns:
        Parsed configuration as a dictionary.
    """
    if config_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(base_dir, "config", "config.yaml")

    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    return config
