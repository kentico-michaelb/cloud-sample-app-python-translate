import requests
from helpers.config import ConfigHelper

class ItemRepo():
    def __init__(self, codename, language):
        self.codename = codename
        self.language = language
        self.cm_api_key = ConfigHelper.get_env_value("KC_CM_API_KEY")
        
        self.headers = {
            "Authorization": self.cm_api_key
        }


    def get_content_item(self, project_id):
        r = requests.get("https://manage.kenticocloud.com/v1/projects/{}/items/codename/{}/variants/codename/{}".format(project_id, self.codename, self.language), headers=self.headers)

        if r:
            return r.json()
        

    def convert_json_to_dict(self, json_data):
 
        elements = {}

        non_translateable_elements = {}

        for key, values in json_data["elements"].items():
            # Do not attempt to translate arrays, numbers, or language codes
            if isinstance(values, str) and key !="translation_code":                         
                elements[key] = values
            else:                                
                non_translateable_elements[key] = values  
        return elements, non_translateable_elements


    def import_content_item(self, content_item, project_id, codename, language):
        payload = {"elements": content_item }

        r = requests.put("https://manage.kenticocloud.com/v1/projects/{}/items/codename/{}/variants/codename/{}".format(project_id, codename, language), json=payload, headers=self.headers)

        r.raise_for_status()
        

        
        