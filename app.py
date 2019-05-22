import requests
from flask import Flask, render_template
from flask_restful import Api, reqparse
from resources.translate import Translate
from helpers.config import ConfigHelper

app = Flask(__name__)

api = Api(app)

# Webhook needs to include a lang parameter of the target language; ex: ~/translator/translate?lang=es
api.add_resource(Translate, "/translator/translate")

# Routes for the frontend
@app.route("/", defaults={"language": "default"})

@app.route("/<language>")
def index(language="default"):
    project_id = ConfigHelper.get_env_value("KC_PROJECT_ID")
    limit = ConfigHelper.get_env_value("announcement_limit")

# Banner announcement text from KC
    announcement_response = requests.get("https://deliver.kenticocloud.com/{}/items?system.type=announcement&language={}&limit={}".format(project_id, language, limit))
    if announcement_response:
        items = announcement_response.json()
        
# Language selector text and images from KC
    language_response = requests.get("https://deliver.kenticocloud.com/{}/items?system.type=language_selector&language={}&limit={}".format(project_id, language, limit))
    if language_response:
        languages = language_response.json()
    
    if items and languages:
        return render_template("index.html", items=items["items"], languages=languages["items"])

if __name__=="__main__":
    app.run(port=3000, debug=True)