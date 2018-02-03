


import os.path
import sys
import yaml
import pprint
from config import *
import pymysql
import pandas as pd
from django.contrib.admin.templatetags.admin_list import results




try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai


def db_query(parameter_json):
    return [parameter_json]

def connect_to_db():
    db = pymysql.Connection(host = host_inventory,
                            user = user_inventory,
                            passwd = passwd,
                            db = database)
    return db

def get_ifsc_json(city):
    db = connect_to_db()
    query = 'Select * From ggc.bank_details where '
    if city != '':
        query = query + "CITY='%s'" %(city)
    print (query)
    df_type = pd.read_sql(query, db)
    print (df_type)
    results = df_type.to_dict(orient='records')
    print (results)
    return results



def call_api(dict_input):
    out_dict = {}
    out_dict['messageText'] = []
    out_dict['messageSource'] = dict_input['messageSource']
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.lang = 'de'
    request.resetContexts = False
    request.session_id = dict_input['user_id']
    request.query = dict_input['messageText']
    response = yaml.load(request.getresponse())
    pp = pprint.PrettyPrinter(indent=4)
    if response['result']['metadata']['intentName'] == 'login':
        if response['result']['parameters']['account'] == '':
            pp.pprint(response['result']['fulfillment']['messages'][0]['speech'])
            out_dict['messageText'].append(response['result']['fulfillment']['messages'][0]['speech'])
            out_dict["plugin"] = {'name': 'autofill', 'type': 'items', 'data': sign_in}
            return out_dict
        elif response['result']['parameters']['account'] == 'employer':
            out_dict['messageText'].append(employer_signin)
            return out_dict
        else:
            out_dict['messageText'].append(employer_signin)
            return out_dict
            
            
            
        
    ent_dict = response['result']['parameters']
    ent_dict['_id'] = request.session_id
    
    

    return out_dict









