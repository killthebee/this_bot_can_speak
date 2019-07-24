import os
import requests
import sys
import io
import dialogflow_v2 as dialogflow


DIALOGFLOW_PROJECT_ID = os.environ.get('DIALOGFLOW_PROJECT_ID')
DIALOGFLOW_LANGUAGE_CODE = 'ru'


def create_intent(project_id, display_name, training_phrases_parts,
                  message_texts):

    intents_client = dialogflow.IntentsClient()

    parent = intents_client.project_agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.types.Intent.TrainingPhrase.Part(
            text=training_phrases_part)
        training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.types.Intent.Message.Text(text=message_texts)
    message = dialogflow.types.Intent.Message(text=text)

    intent = dialogflow.types.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message])

    response = intents_client.create_intent(parent, intent)

def main():

    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')
    url = 'https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json'
    response = requests.get(url)
    resp_unpckd = response.json()
    for intent in range(0,len(list(resp_unpckd.keys()))-1):
        intent_message = []
        intent_message.append(
        str(resp_unpckd[list(resp_unpckd.keys())[intent]]['answer'])
        )
        create_intent(
        DIALOGFLOW_PROJECT_ID,
        list(resp_unpckd.keys())[intent],
        resp_unpckd[list(resp_unpckd.keys())[intent]]['questions'],
        intent_message
        )


if __name__ == '__main__':
    main()
