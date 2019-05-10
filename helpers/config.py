import json

class ConfigHelper():
    @staticmethod
    def get_env_value(env_value):
        config = ConfigHelper.read_config()
        environment = config["ENVIRONMENT"]           
        env_value = config["ENVIRONMENTS"][environment][env_value]
        
        return env_value

    @staticmethod
    def read_config():
        with open('config.json', 'r') as f:
            config = json.load(f)

        return config