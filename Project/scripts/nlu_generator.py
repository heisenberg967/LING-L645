import json
import string

FORBIDDEN_INTENT_CHARS = ":,$&%*()+?~#/?"

def load_dataset(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)
        return data

def has_only_english_chars(text):
    text = text.replace(" ", "")
    char_set = string.ascii_letters + string.digits + string.punctuation
    return all((True if x in char_set else False for x in text))
    
def is_intent_valid(intent_name):
        if len(intent_name) > 50 or len(intent_name) == 0:
            return False

        if not has_only_english_chars(intent_name):
            return False

        for ch in intent_name:
            if ch in FORBIDDEN_INTENT_CHARS:
                return False
        return True

def get_utterances_wiki(utterance_list, utterance_char_limit):
    utterances = list(set(utterance_list))
    for utterance in utterances:
        if len(utterance) > utterance_char_limit:
            utterances.remove(utterance)
    return utterances

def get_utterances_quizbowl(utterance_list, utterance_char_limit):
    for utterance in utterance_list:
        if len(utterance) > utterance_char_limit:
            utterance_list.remove(utterance)
    return utterance_list