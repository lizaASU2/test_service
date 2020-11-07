from flask import Flask
from flask import request
import requests
from flask import jsonify
import pickle 

import os
import json
from ast import literal_eval
import traceback

application = Flask(__name__)


#загружаем модели из файла
md = pickle.load(open("model.pickle", "rb"))
vec=pickle.load(open("vectorizer.pickle", "rb"))

def annotate_text(text):
    response = requests.get(url="http://webengineering.ins.hs-anhalt.de:43720/rest/annotate",
                            params={"text": text, "confidence": 0.5},
                            headers={'accept': 'application/json'},
                            verify=False)
    response=response.json()
    return response

def named_entities(data):
  out = {}
  try:
    data = data['Resources']
    
    for i in data:
      out[i['@URI']] = i['@surfaceForm']
  finally:
    return out

@application.route("/")  
def hello():
    resp = {'message':"Server is available"}
    
    response = jsonify(resp)
    
    return response

# предикт категории
@application.route("/categoryPrediction", methods=['GET', 'POST'])  
def registration():
    resp = {'message':'ok'
           ,'question_text': 'error'
           }

    try:
        getData = request.get_data()
        json_params = json.loads(getData) 
        
        #category = model.predict(vec.transform([json_params['user_message']]).toarray()).tolist()
        result=md.predict(vec.transform([json_params['user_message']]))
        resp['question_text'] = json_params['user_message']
        resp['named_entities'] =named_entities(annotate_text(resp['question_text']))
        resp['relation'] = result[0]
    except Exception as e: 
        print(e)
        resp['message'] = e
      
    response = jsonify(resp)
    
    return response

        

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    application.run(debug=False, port=port, host='0.0.0.0' , threaded=True)
