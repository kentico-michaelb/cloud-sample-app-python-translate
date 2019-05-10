import json

# May be able to set self.config attribute to a class atributute (just config = read_config() instead of self.config)

class ConfigHelper():
    # def __init__(self):
    #     self.config = self.read_config()
    #     self.environment = self.config["ENVIRONMENT"]

    # def get_env_value(self, env_value):            
    #     env_value = self.config["ENVIRONMENTS"][self.environment][env_value]
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