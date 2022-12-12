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

quizbowl_train_data = nlu_generator.load_dataset('../datasets/quizbowl_train_data.json')

json_params = {
    'projectName': 'clu_quanta_quizbowl',
    'intents': [], #list of intent_param objects
    'utterances': [] #list of utterance_param objects
}

for ele in quizbowl_train_data:
    if nlu_generator.is_intent_valid(ele):
        utterances = nlu_generator.get_utterances_quizbowl(quizbowl_train_data[ele], 490)
        num_utterances = len(utterances)
        intent_param = {
        "category": ""
        }
        intent_param["category"] = ele
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
            utterance = str(utterances[i])
            if len(utterance) < 490:
                utterance_param["text"] = utterance
            else:
                utterance_param["text"] = utterance[:490]
            utterance_param["intent"] = ele
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
            utterance = str(utterances[i])
            if len(utterance) < 490:
                utterance_param["text"] = utterance
            else:
                utterance_param["text"] = utterance[:490]
            utterance_param["intent"] = ele
            utterance_param["dataset"] = "Test"
            json_params["utterances"].append(utterance_param)

#print(len(json_params["intents"]))

clu_json = generate_clu_json(json_params)

with open('clu_quizbowl_data.json', 'w') as outfile:
    json.dump(clu_json, outfile)
