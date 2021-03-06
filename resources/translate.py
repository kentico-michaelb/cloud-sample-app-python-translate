from flask import request
from flask_restful import Resource, reqparse
from repositories.item import ItemRepo
from services.translator import TranslatorService
from helpers.config import ConfigHelper
from helpers.validation import ValidationHelper

class Translate(Resource):
# Create the parser to get data out of the request
    parser = reqparse.RequestParser()

    parser.add_argument("data",
        type=dict,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument("message",
        type=dict,
        required=True,
        help="This field cannot be blank."
    )


    def post(self):

        # Parse the body of the request
        data = self.parser.parse_args()
        lang_param = request.args.get("lang")
        default_config = ConfigHelper.get_env_value("KC_DEFAULT_LANG")

        # Only execute on publish events
        if data["message"]["operation"] == "publish":
            project_id = ConfigHelper.get_env_value("KC_PROJECT_ID")

            # Ensure that the culture code is present and valid for the translation service
            if lang_param:
                try:
                    valid_language = ValidationHelper.check_valid_culture(lang_param)
                except:
                    return {"message":"invalid language parameter. Set ?lang= to a supported culture."}, 400
            else:
                return {"message":"API requires ?lang parameter to be set to the target language."}, 400

            if valid_language:
                # Due to Linked content, there can be multiple content items in webhook's "items" array   
                for content_item in data["data"]["items"]:
                    # One way translation: only translate the default language into other languages
                    if content_item["language"] != "default" and content_item["language"] != default_config:
                        continue
                    item = ItemRepo(content_item["codename"], content_item["language"])

                    json_data = item.get_content_item(project_id)
                    
                    if json_data:
                        # Convert the JSON to a Python dictionary object that we can pass to the translator
                        elements, non_translateable_elements = item.convert_json_to_dict(json_data)

                        # Ensure that the element string length is valid for the translation service limits
                        try:
                            valid_length = ValidationHelper.check_valid_length(elements)
                        except:
                            return {"message":"Maximum string length exceeded."}, 400

                        if valid_length is True:
                            # Pass the Python dictionary to the translation service that uses the Google library
                            translated_item = TranslatorService.translate_content_item(elements, item.language, lang_param)

                            # Add arrays (assets, taxonomies, multiple choice, etc.) to the item
                            translated_item.update(non_translateable_elements)

                            # Import the dictionary as JSON into Kentico Cloud using the Content Management API
                            item.import_content_item(translated_item, project_id, item.codename, lang_param)     
                            continue
                    return {"message":"Source content item {} doesn't exist.".format(content_item["codename"])}, 400       
                return {"message":"Translation script completed without error."}, 200
        return {"message":"Not a publish event. No translation required."}, 200        

   





        