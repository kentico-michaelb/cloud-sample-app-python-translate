from googletrans import Translator
from bs4 import BeautifulSoup
from helpers.config import ConfigHelper

class TranslatorService(Translator):
   def __init__(self, text, source, target):              
       self.text = text 
       self.src = source 
       self.dest = target
       self.translator = Translator() 


   def translate_string(self):
      translated_result = self.translator.translate(self.text, src=self.src, dest=self.dest)
      
      # Parse HTML for KC Rich Text objects to remove whitespace created by translator 
      soup = BeautifulSoup(translated_result.text, "html.parser")
      for link in soup.findAll("object"):
         link["type"] = "application/kenticocloud"
         translated_result.text = str(soup)
      
      return translated_result.text  


   def translate_content_item(content_item, source, target):
      translated_result = {}
      # Handle KC default language as most translation libraries won't recognize "default" as a valid culture code
      if source == "default":
         source = ConfigHelper.get_env_value("KC_DEFAULT_LANG")

      for key, value in content_item.items():
         text = TranslatorService(value, source, target)
         translated_result[key] = text.translate_string()

      return translated_result