import os
import logging
import yaml
import base64

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

APP_CONFIG_PATH = os.environ.get("APP_CONFIG_PATH", "app_config.yaml")


def load_yaml_config(filepath):
    with open(filepath, "r") as file:
        config = yaml.safe_load(file)
    return config

def load_base64_yaml_config(filepath):
    with open(filepath, 'r') as file:
        base64_str = file.read()

    yaml_str = base64.b64decode(base64_str).decode('utf-8')
    config = yaml.safe_load(yaml_str)
    return config


if APP_CONFIG_PATH.endswith(".yaml") and os.path.exists(APP_CONFIG_PATH):
    app_config = load_yaml_config("app_config.yaml")
elif APP_CONFIG_PATH.endswith(".yaml.b64") and os.path.exists(APP_CONFIG_PATH):
    app_config = load_base64_yaml_config("app_config.yaml.b64")


if app_config and app_config.get("judge") and app_config["judge"].get("api_key"):
    os.environ["OPENAI_API_KEY"] = app_config["judge"]["api_key"]


