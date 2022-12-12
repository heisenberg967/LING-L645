import uuid
import json
import os
import sys
 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import nlu_generator

def generate_utterance_json(utterance):
    utterance_json = {
        "id": str(uuid.uuid4()),
        "data": [
        {
            "text": utterance,
            "userDefined": False
        }
        ],
        "isTemplate": False,
        "count": 0,
        "lang": "en",
        "updated": 0
    }

    return utterance_json

def generate_intent_utterance_json(utterances):
    intent_utterance_json = []
    
    for utterance in utterances:
        intent_utterance_json.append(generate_utterance_json(utterance))

    return intent_utterance_json

def generate_intent_json(intent_params):
    intent_json = {
        "id": "6f0e3f5e-765a-46b0-9e34-545b8e0621f7",
        "name": intent_params["intentName"],
        "auto": True,
        "contexts": [],
        "responses": [
            {
            "resetContexts": False,
            "action": intent_params["intentName"].replace(" ","_"),
            "affectedContexts": [],
            "parameters": [],
            "messages": [
                {
                "type": "0",
                "title": "",
                "textToSpeech": "",
                "lang": "en",
                "speech": [
                    intent_params["intentResponseMessage"]
                ],
                "condition": ""
                }
            ],
            "speech": []
            }
        ],
        "priority": 500000,
        "webhookUsed": False,
        "webhookForSlotFilling": False,
        "fallbackIntent": True,
        "events": [],
        "conditionalResponses": [],
        "condition": "",
        "conditionalFollowupEvents": []
    }

    return intent_json

def generate_agent_json(agent_params):
    agent_json = {
        "description": agent_params["description"],
        "language": "en",
        "shortDescription": "",
        "examples": "",
        "linkToDocs": "",
        "displayName": agent_params["projectName"],
        "activeAssistantAgents": [
            "smalltalk-domain-on"
        ],
        "disableInteractionLogs": False,
        "disableStackdriverLogs": True,
        "googleAssistant": {
            "googleAssistantCompatible": False,
            "project": "testagent2-1b403",
            "welcomeIntentSignInRequired": True,
            "startIntents": [],
            "systemIntents": [],
            "endIntentIds": [],
            "oAuthLinking": {
            "required": False,
            "providerId": "",
            "authorizationUrl": "",
            "tokenUrl": "",
            "scopes": "",
            "privacyPolicyUrl": "",
            "grantType": "AUTH_CODE_GRANT"
            },
            "voiceType": "MALE_1",
            "capabilities": [],
            "env": "",
            "protocolVersion": "V2",
            "autoPreviewEnabled": False,
            "isDeviceAgent": False
        },
        "defaultTimezone": "America/Los_Angeles",
        "webhook": {
            "url": "",
            "username": "",
            "headers": {},
            "available": False,
            "useForDomains": False,
            "cloudFunctionsEnabled": False,
            "cloudFunctionsInitialized": False
        },
        "isPrivate": True,
        "mlMinConfidence": 0.3,
        "supportedLanguages": [],
        "enableOnePlatformApi": True,
        "onePlatformApiVersion": "v2",
        "secondaryKey": "b7621011afe04840bb069df096794d2d",
        "analyzeQueryTextSentiment": False,
        "enabledKnowledgeBaseNames": [],
        "knowledgeServiceConfidenceAdjustment": -0.4,
        "dialogBuilderMode": False,
        "baseActionPackagesUrl": "",
        "enableSpellCorrection": False
    }

    return agent_json

def generate_package_json():
    package_json = {}
    package_json["version"] = "1.0.0"

    return package_json

def generate_dialogflow_agent(df_agent_params):
    package_json = generate_package_json()

    agent_json = generate_agent_json(df_agent_params['agent_params'])
    
    dir_name = df_agent_params['agent_params']['projectName']
    
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
    if not os.path.isdir(dir_name+'/intents'):
        os.mkdir(dir_name+'/intents')

    for i in range(len(df_agent_params['intents'])):
        intent_params = {
            'intentName': df_agent_params['intents'][i],
            'intentResponseMessage': 'Intent Received: ' + df_agent_params['intents'][i]
        }
        intent_json = generate_intent_json(intent_params)

        utterance_json = generate_intent_utterance_json(df_agent_params['utterances'][i])

        with open(dir_name+'/intents/'+df_agent_params['intents'][i]+'.json', 'w') as outfile:
            json.dump(intent_json, outfile)
        
        with open(dir_name+'/intents/'+df_agent_params['intents'][i]+'_usersays_en.json', 'w') as outfile:
            json.dump(utterance_json, outfile)

    with open(dir_name+'/package.json', 'w') as outfile:
        json.dump(package_json, outfile)

    with open(dir_name+'/agent.json', 'w') as outfile:
        json.dump(agent_json, outfile)
    

wiki_train_data = nlu_generator.load_dataset('../datasets/wiki_train_data.json')

df_agent_params = {
    'agent_params': {
    'description': 'Wiki QnA Bot',
    'projectName': 'wiki_bot',
    },
    'intents': [], #list of intent_param objects
    'utterances': [], #list of utterance_param objects 
    'testPhrases': [], #list of utterances to test
    'testIntentUtteranceMapping': []
}

for ele in wiki_train_data:
    utterances = nlu_generator.get_utterances_wiki(ele["utterances"], 250)
    num_utterances = len(utterances)
    
    if num_utterances > 20 and nlu_generator.is_intent_valid(ele["intent"]):
        
        df_agent_params["intents"].append(ele["intent"])

        train_range = round(num_utterances*0.8)
        train_utterances = []
        for i in range(train_range):
            train_utterances.append(ele["utterances"][i])
        df_agent_params["utterances"].append(train_utterances)

        for i in range(train_range,num_utterances):
            df_agent_params["testPhrases"].append(ele["utterances"][i])
            df_agent_params["testIntentUtteranceMapping"].append({
                ele["intent"]: ele["utterances"][i]
                })

#print(len(df_agent_params["intents"]))

generate_dialogflow_agent(df_agent_params)

with open('wiki_bot_test.txt', 'w') as outfile:
    for utterance in df_agent_params["testPhrases"]:
        outfile.write(utterance)
        outfile.write('\n')

with open('wiki_bot_test.json', 'w') as outfile:
    json.dump(df_agent_params["testIntentUtteranceMapping"], outfile)
