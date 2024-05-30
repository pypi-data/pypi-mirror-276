__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"

import requests
import json
import ragfmk.utils.CONST as C

class ollama:
    def __init__(self, 
                 urlbase, 
                 model, 
                 temperature, 
                 contextwindow=C.OLLAMA_DEFAULT_CTXWIN):
        self.__modelName = model
        self.__urlbase = urlbase
        self.__temperature = temperature
        self.__contextwindow = contextwindow
        
    @property
    def model(self):
        return self.__modelName
    @property
    def urlbase(self):
        return self.__urlbase
    @property
    def temperature(self):
        return self.__temperature
    
    @property
    def contextwindow(self):
        return self.__contextwindow
    
    def prompt(self, prompt):
        try:
            url = self.urlbase + "/generate"
            params = {"model": self.model,
                      "prompt": prompt, 
                      "stream": False,
                      "temperature": self.temperature,
                      "num_ctx": self.contextwindow}
            response = requests.post(url, json=params)
            if (response.status_code == 200):
                response_text = response.text
                data = json.loads(response_text)
                return data
            else:
                raise Exception("Error while reaching out to the Web Service: {}", str(response.status_code, response.text))
        except Exception as e:
            return str(e)