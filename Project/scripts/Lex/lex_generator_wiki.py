import json
import os
import sys
 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import nlu_generator

def generate_intent_json(intent_utterance_params):
    intent_json = {
        "name":intent_utterance_params["intentName"],
        "identifier":"9UA9ALDXAJ",
        "description":None,
        "parentIntentSignature":None,
        "sampleUtterances":[],
        "intentConfirmationSetting":None,
        "intentClosingSetting":{
            "isActive":True,
            "closingResponse":{
                "allowInterrupt":True,
                "messageGroupsList":[{
                    "message":{
                        "imageResponseCard":None,
                        "ssmlMessage":None,
                        "customPayload":None,
                        "plainTextMessage":{
                            "value":intent_utterance_params["intentResponseMessage"]
                        }
                    },
                    "variations":None
                }]
            },
            "nextStep":{
                "intent":{
                    "name":None,
                    "slots":None
                },
                "dialogAction":{
                    "type":"EndConversation",
                    "suppressNextMessage":None,
                    "slotToElicit":None
                },
                "sessionAttributes":None
            }
        },
        "initialResponseSetting":{
            "initialResponse":None,
            "codeHook":None,
            "conditional":None,
            "nextStep":{
                "intent":{
                    "name":None,
                    "slots":None
                },
                "dialogAction":{
                    "type":"CloseIntent",
                    "suppressNextMessage":None,
                    "slotToElicit":None
                },
                "sessionAttributes":None
            }
        },
        "inputContexts":None,
        "outputContexts":None,
        "kendraConfiguration":None,
        "dialogCodeHook":None,
        "fulfillmentCodeHook":None,
        "slotPriorities":[]
    }

    for utterance in intent_utterance_params["utterances"]:
        intent_json["sampleUtterances"].append({
                "utterance":utterance
            })

    return intent_json

def generate_fallback_intent_json():
    fallback_intent_json = {
        "name":"FallbackIntent","identifier":"FALLBCKINT","description":"Default intent when no other intent matches","parentIntentSignature":"AMAZON.FallbackIntent","sampleUtterances":None,"intentConfirmationSetting":None,"intentClosingSetting":None,"initialResponseSetting":{"initialResponse": None,"codeHook":{"isActive":True,"enableCodeHookInvocation":True,"invocationLabel":None,"postCodeHookSpecification":{"failureResponse":None,"failureNextStep":{"intent":None,"dialogAction":{"type":"EndConversation","suppressNextMessage":None,"slotToElicit":None},"sessionAttributes":None},"failureConditional":None,"successConditional":None,"timeoutResponse":None,"timeoutNextStep":{"intent":None,"dialogAction":{"type":"EndConversation","suppressNextMessage":None,"slotToElicit":None},"sessionAttributes":None},"timeoutConditional":None,"successNextStep":{"intent":None,"dialogAction":{"type":"EndConversation","suppressNextMessage":None,"slotToElicit":None},"sessionAttributes":None},"successResponse":None}},"conditional":None,"nextStep":{"intent":None,"dialogAction":{"type":"InvokeDialogCodeHook","suppressNextMessage":None,"slotToElicit":None},"sessionAttributes":None}},"inputContexts":None,"outputContexts":None,"kendraConfiguration":None,"dialogCodeHook":None,"fulfillmentCodeHook":None,"slotPriorities":[]
    }

    return fallback_intent_json

def generate_bot_locale_json():
    bot_locale_json = {
        "name":"English (US)","identifier":"en_US","version":None,"description":None,"voiceSettings":{"voiceId":"Ivy","engine":"neural"},"nluConfidenceThreshold":0.4
    }

    return bot_locale_json

def generate_bot_json():
    bot_json = {
        "name":"wiki_bot","version":"DRAFT","description":None,"identifier":"PTVTD8YVN2","dataPrivacy":{"childDirected":False},"idleSessionTTLInSeconds":300
    }

    return bot_json

def generate_manifest_json():
    manifest_json = {
        "metaData":{"schemaVersion":"1","resourceType":"BOT","fileFormat":"LexJson"}
    }

    return manifest_json

def generate_lex_agent(lex_agent_params):
    manifest_json = generate_manifest_json()
    bot_json = generate_bot_json()
    bot_locale_json = generate_bot_locale_json()
    fallback_intent_json = generate_fallback_intent_json()

    dir_name = lex_agent_params['agent_params']['projectName']
    
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
    if not os.path.isdir(dir_name+'/'+dir_name):
        os.mkdir(dir_name+'/'+dir_name)
    if not os.path.isdir(dir_name+'/'+dir_name+'/BotLocales'):
        os.mkdir(dir_name+'/'+dir_name+'/BotLocales')
    if not os.path.isdir(dir_name+'/'+dir_name+'/BotLocales/en_US'):
        os.mkdir(dir_name+'/'+dir_name+'/BotLocales/en_US')
    if not os.path.isdir(dir_name+'/'+dir_name+'/BotLocales/en_US/Intents'):
        os.mkdir(dir_name+'/'+dir_name+'/BotLocales/en_US/Intents')

    for i in range(len(lex_agent_params['intents'])):
        intent_name = "_".join(lex_agent_params['intents'][i].split())
        intent_name = lex_agent_params['intents'][i].replace(r' ', "_")
        intent_name = lex_agent_params['intents'][i].replace("'", "")
        
        intent_utterance_params = {
            'intentName': intent_name,
            'intentResponseMessage': 'Intent Received: ' + intent_name,
            'utterances': lex_agent_params['utterances'][i]
        }

        intent_json = generate_intent_json(intent_utterance_params)

        if not os.path.isdir(dir_name+'/'+dir_name+'/BotLocales/en_US/Intents/'+intent_name):
            os.mkdir(dir_name+'/'+dir_name+'/BotLocales/en_US/Intents/'+intent_name)

        with open(dir_name+'/'+dir_name+'/BotLocales/en_US/Intents/'+intent_name+'/Intent.json', 'w') as outfile:
            json.dump(intent_json, outfile)

    if not os.path.isdir(dir_name+'/'+dir_name+'/BotLocales/en_US/Intents/FallbackIntent'):
            os.mkdir(dir_name+'/'+dir_name+'/BotLocales/en_US/Intents/FallbackIntent')
    with open(dir_name+'/'+dir_name+'/BotLocales/en_US/Intents/FallbackIntent/Intent.json', 'w') as outfile:
            json.dump(fallback_intent_json, outfile)

    with open(dir_name+'/Manifest.json', 'w') as outfile:
        json.dump(manifest_json, outfile)

    with open(dir_name+'/'+dir_name+'/Bot.json', 'w') as outfile:
        json.dump(bot_json, outfile)

    with open(dir_name+'/'+dir_name+'/BotLocales/en_US/BotLocale.json', 'w') as outfile:
        json.dump(bot_locale_json, outfile)


wiki_train_data = nlu_generator.load_dataset('../datasets/wiki_train_data.json')

lex_agent_params = {
    'agent_params': {
    'description': 'Wiki QnA Bot',
    'projectName': 'wiki_bot',
    },
    'intents': [], #list of intent_param objects
    'utterances': [], #list of utterance_param objects 
    'testIntentUtteranceMapping': [] #list of utterances to test
}

for ele in wiki_train_data:
    utterances = nlu_generator.get_utterances_wiki(ele["utterances"], 490)
    num_utterances = len(utterances)
    
    if num_utterances > 20 and nlu_generator.is_intent_valid(ele["intent"]):
        
        lex_agent_params["intents"].append(ele["intent"].replace(" ", "_"))

        train_range = round(num_utterances*0.8)
        train_utterances = []
        for i in range(train_range):
            train_utterances.append(ele["utterances"][i])
        lex_agent_params["utterances"].append(train_utterances)

        for i in range(train_range,num_utterances):
            lex_agent_params["testIntentUtteranceMapping"].append({
                ele["intent"]: ele["utterances"][i]
                })

#print(len(lex_agent_params["intents"]))

generate_lex_agent(lex_agent_params)

with open('wiki_bot_test.json', 'w') as outfile:
    json.dump(lex_agent_params["testIntentUtteranceMapping"], outfile)