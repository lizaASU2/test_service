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



# предикт категории
@application.route("/categoryPrediction", methods=['GET', 'POST'])  
def registration():
    resp = {'message':'ok'
           ,'category': -1
           }

    try:
        getData = request.get_data()
        json_params = json.loads(getData) 
        
        #category = model.predict(vec.transform([json_params['user_message']]).toarray()).tolist()
        result=md.predict(vec.transform([json_params['user_message']]))[0]
        resp['category'] = category
    except Exception as e: 
        print(e)
        resp['message'] = e
      
    response = jsonify(resp)
    
    return response

        

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    application.run(debug=False, port=port, host='0.0.0.0' , threaded=True)