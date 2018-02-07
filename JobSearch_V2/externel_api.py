


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



def connect_to_db():
    db = pymysql.Connection(host = host_inventory,
                            user = user_inventory,
                            passwd = passwd,
                            db = database)
    return db



def call_api(dict_input):
    out_dict = {}
    out_dict['messageText'] = []
    out_dict['messageSource'] = 'messageFromBot'
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.lang = 'de'
    request.resetContexts = False
    request.session_id = dict_input['user_id']
    request.query = dict_input['messageText']
    response = yaml.load(request.getresponse())
    pp = pprint.PrettyPrinter(indent=4)
    entity_json = response['result']['parameters']
    pp.pprint(response)
    if response['result']['metadata']['intentName'] == 'login':
        if response['result']['parameters']['account'] == '':
            pp.pprint(response['result']['fulfillment']['messages'][0]['speech'])
            out_dict['messageText'].append(response['result']['fulfillment']['messages'][0]['speech'])
            #out_dict["plugin"] = {'name': 'autofill', 'type': 'items', 'data': sign_in}
            return out_dict
        elif response['result']['parameters']['account'] == 'employer':
            out_dict['messageText'].append(employer_signin)
            return out_dict
        else:
            out_dict['messageText'].append(jobseeker_signin)
            return out_dict
            
    elif response['result']['metadata']['intentName'] == 'register':
        if response['result']['parameters']['account'] == '':
            pp.pprint(response['result']['fulfillment']['messages'][0]['speech'])
            out_dict['messageText'].append(response['result']['fulfillment']['messages'][0]['speech'])
            #out_dict["plugin"] = {'name': 'autofill', 'type': 'items', 'data': sign_in}
            return out_dict
        elif response['result']['parameters']['account'] == 'employer':
            out_dict['messageText'].append(employer_register)
            return out_dict
        else:
            out_dict['messageText'].append(jobseeker_register)
            return out_dict
    elif response['result']['metadata']['intentName'] == 'jobsearch':
        if entity_json['location'] == '':
            out_dict["messageText"].append(ask_location)
            out_dict["plugin"] = {'type': 'manufacturers', 'data': locations, 'name': 'popup'}
            print out_dict
        elif entity_json['job_category'] == []:
            out_dict["messageText"].append(ask_category)
            out_dict["plugin"] = {'type': 'manufacturers', 'data': categories, 'name': 'popup'}
            print out_dict
            return out_dict
        elif entity_json['career_level'] == []:
            out_dict['messageText'].append(ask_career_level)
            out_dict["plugin"] = {'name': 'popup', 'type': 'manufacturers', 'data': career_level}
            return out_dict
        elif entity_json['vacancy_type'] == []:
            out_dict['messageText'].append(ask_vacancy_type)
            out_dict["plugin"] = {'name': 'popup', 'type': 'manufacturers', 'data': vacancy_type}
            return out_dict
        else:
            out_dict['messageText'].append(conclusions)
            out_dict['ResultBuyer'] = [entity_json]
            return out_dict
    else:
        out_dict['messageText'].append(response['result']['fulfillment']['speech'])
    return out_dict










