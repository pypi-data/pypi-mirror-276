from configparser import ConfigParser

def get_config_file_obj(config_path):
    """creating config parser"""
    config=ConfigParser()
    config.read(str(config_path))
    return config

def get_configs():
    """reading details from config file"""
    configs_data={}
    config_path="config/config.ini"
    config=get_config_file_obj(config_path)
    sections=['upstox_url']
    for section in sections:
        for key,value in config.items(section):
            configs_data[key]=value
    return configs_data