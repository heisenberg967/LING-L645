import json
import os.path
import sys
 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import nlu_generator

def generate_clu_json(json_params):
    clu_json = {}
    clu_json['projectFileVersion'] = '2022-10-01-preview'
    clu_json['stringIndexType'] = 'Utf16CodeUnit'
    clu_json['metadata'] = {
        "projectKind": "Conversation",
        "settings": {
            "confidenceThreshold": 0
        },
        "projectName": json_params['projectName'],
        "multilingual": False,
        "description": "",
        "language": "en-us"
        }
    clu_json['assets'] = {
        "projectKind": "Conversation",
        "intents": json_params['intents'],
        "entities": [],
        "utterances": json_params['utterances']
    }
    return clu_json

wiki_train_data = nlu_generator.load_dataset('../datasets/wiki_train_data.json')

json_params = {
    'projectName': 'wiki_clu',
    'intents': [], #list of intent_param objects
    'utterances': [] #list of utterance_param objects
}

for ele in wiki_train_data:
    utterances = nlu_generator.get_utterances_wiki(ele["utterances"], 490)
    num_utterances = len(utterances)
    
    if num_utterances > 20 and nlu_generator.is_intent_valid(ele["intent"]):
        intent_param = {
        "category": ""
        }
        intent_param["category"] = ele["intent"]
        json_params["intents"].append(intent_param)

        train_range = round(num_utterances*0.8)
        for i in range(train_range):
            utterance_param = {
            "text": "",
            "language": "en-us",
            "intent": "",
            "entities": [],
            "dataset": ""
            }
            utterance_param["text"] = utterances[i]
            utterance_param["intent"] = ele["intent"]
            utterance_param["dataset"] = "Train"
            json_params["utterances"].append(utterance_param)
        for i in range(train_range,num_utterances):
            utterance_param = {
            "text": "",
            "language": "en-us",
            "intent": "",
            "entities": [],
            "dataset": ""
            }
            utterance_param["text"] = utterances[i]
            utterance_param["intent"] = ele["intent"]
            utterance_param["dataset"] = "Test"
            json_params["utterances"].append(utterance_param)

#print(len(json_params["intents"]))

clu_json = generate_clu_json(json_params)

with open('clu_wiki_data.json', 'w') as outfile:
    json.dump(clu_json, outfile)
