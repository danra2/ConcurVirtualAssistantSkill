from __future__ import print_function

def lambda_handler(event, context):
    #This is the first function that is hit upon request everytime.
    #The entire object is being passed to the event parameter.
    #You can parse the object of the event for further details for logic implementation.
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
    #So this is where we are parsing through the event log and checking out which intent is being called. It's not a launch request, it's most likely a Intent request.
    #Next we will go to our method that check for intents, and see which exactly is the proper intent for the question asked, or which it's classified under.

def on_session_started(session_started_request, session):
    #Called when the session starts

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    #Called when the user launches the skill without specifying what they want
    #Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    # Called when the user specifies an intent for this skill

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "GeneralIntent":
        return get_general_info_response()
    elif intent_name == "DirectoryIntent":
        return get_directory_info_response(intent_request)
    elif intent_name == "HelpIntent":
        return get_help_response()
    elif intent_name == "PhoneIntent":
        return get_directory_phone_number(intent_request)
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    # Called when the user ends the session.
    # Is not called when the skill returns should_end_session=true

    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Concur virtual assistant."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with the same text.
    reprompt_text = speech_output
    #This is what is repeated if Alexa doesn't get a response, or if you ask for Alexa to repeat.
    should_end_session = False
    #This determines whether or not the session is open to taking more inputs, or just closed and have to be revoked from the beginning again.
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    #This is what is sent to the response JSON object. Lambda response essentially builds and sends it back.


def get_help_response():
    session_attributes = {}
    card_title = "help"
    speech_output = "Welcome to the help section for the Concur Virtual Assistant. A couple of examples of phrases that you can except are... What is Travis Johnsons phone number?... or , who do I contact for the lost and found? Lets get started now by trying one of these."
    reprompt_text = speech_output
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(card_title,speech_output,reprompt_text,should_end_session))


def get_general_info_response():
    session_attributes = {}
    card_title = "Directory_Info"
    speech_output = "Concur's virtual assistant is a voice activated wiki that can be used to make general inquires."
    reprompt_text = speech_output
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(card_title,speech_output,reprompt_text,should_end_session))


def get_directory_info_response(intent_request):
    session_attributes = {}
    card_title = "Directory_Info"
    speech_output = ""
    directory_type = intent_request["intent"]["slots"]["directory"]["value"]

    if directory_type == "lost and found":
        speech_output = "The Concur Lost and found is located on the 10th floor, and is accessible anytime from 8 AM - 5 PM monday through friday. If you require immediate assistance, please contact them at 206 883 9091."
    elif directory_type == "security":
        speech_output = "The Concur Security team is located on the 11th floor. They are open 24 hours a day. If you require immediate assistance, you can reach them at 206 972 3378."
    elif directory_type == "front desk":
        speech_output = "The Concur Front Desk is located on the 10th floor, and is accessible anytime from 8 AM - 5 PM monday through friday. If you require immediate assistance, please contact them at 206 883 9091."
    else:
        speech_output = "Sorry, the Concur virtual assistant does not have a directory that matches what you have asked for."
    reprompt_text = speech_output
    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(card_title,speech_output,reprompt_text,should_end_session))

def get_directory_phone_number(intent_request):
    session_attributes = {}
    card_title = "Directory_Info"
    speech_output = ""
    first_name = intent_request["intent"]["slots"]["first"]["value"]
    last_name = intent_request["intent"]["slots"]["last"]["value"]
    whole_name = first_name + " " + last_name
    if whole_name == "John Nguyen":
        speech_output = "The number for John Nguyen is 2 0 6 6 1 9 1 3 2 4"
    elif whole_name == "Travis Johnson":
        speech_output = "The number for Travis Johnson is 2 0 6 8 8 3 9 0 9 1"
    elif whole_name == "Daniel Ra":
        speech_output = "The number for Daniel Ra is 2 0 6 8 8 3 9 0 9 1"
    elif whole_name == "Tim Escue":
        speech_output = "The number for Tim Escue 3 6 0 6 0 9 3 7 2 8"
    else:
        speech_output = "Sorry, that persons name does not exist within our directory."

    reprompt_text = speech_output
    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(card_title,speech_output,reprompt_text,should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using Concur Virtual Assistant! Goodbye."
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
