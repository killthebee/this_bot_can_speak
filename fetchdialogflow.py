import dialogflow
from google.api_core.exceptions import InvalidArgument
import os


DIALOGFLOW_PROJECT_ID= os.environ.get(['DIALOGFLOW_PROJECT_ID'])

def fetch_dialogflow(session_id, message):

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, session_id)

    text_input = dialogflow.types.TextInput(text=message, language_code='ru')
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise
    return {
        'text': response.query_result.fulfillment_text,
        'is_fallback': response.query_result.intent.is_fallback
    }
