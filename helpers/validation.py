from services.languages import LANGUAGES

class ValidationHelper():
    # valid cultures for googletrans found at: https://py-googletrans.readthedocs.io/en/latest/
    def check_valid_culture(lang_param):
        valid_languages = [*LANGUAGES]
        if lang_param not in valid_languages:
            raise Exception("Invalid culture code.") 
        return True


    def check_valid_length(elements):
        for key, value in elements.items():
            if isinstance(value, str):
                # maximum length defined in documentation https://pypi.org/project/googletrans/
                if len(value) > 15000:
                    raise Exception("{} exceeds the maximum string length.".format(len(value)))                    
        return True