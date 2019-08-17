import os
import requests
import sys
import io
import dialogflow_v2 as dialogflow


DIALOGFLOW_PROJECT_ID = os.environ.get['DIALOGFLOW_PROJECT_ID']


def create_intent(display_name, training_phrases_parts,
                  message_texts):

    intents_client = dialogflow.IntentsClient()

    parent = intents_client.project_agent_path(DIALOGFLOW_PROJECT_ID)
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
        messages=[message]
        )

    response = intents_client.create_intent(parent, intent)


def check_intent_name(display_name):

    intents_client = dialogflow.IntentsClient()

    parent = intents_client.project_agent_path(DIALOGFLOW_PROJECT_ID)
    intents = intents_client.list_intents(parent)
    intent_names = [
        intent.name for intent in intents
        if intent.display_name == display_name
        ]
    if intent_names == []:
        return True:
    else:
        return False


def unpack_q_and_a(**dictionary):

    return dictionary['questions'], dictionary['answer']


def main():

    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

    url = 'https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json'
    response = requests.get(url)
    response.raise_for_status()
    resp_unpckd = response.json()
    for intents_name in resp_unpckd:
        if check_intent_name(intents_name):
            training_phrases, answer = unpack_q_and_a(**resp_unpckd[intent_name])
            create_intent(
                intents_name,
                training_phrases,
                answer
            )


if __name__ == '__main__':
    main()
