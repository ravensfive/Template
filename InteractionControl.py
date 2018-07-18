# main python program
import json, re, random

# lambda function handler - including specific reference to our skill
def lambda_handler(event, context):
    # if skill ID does not match my ID then raise error
    if (event["session"]["application"]["applicationId"] !=
            "amzn1.ask.skill.32109323-a7d4-4018-b21e-13f46c4223b5"):
        raise ValueError("Invalid Application ID")

    # test if session is new
    if event["session"]["new"]: 
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

    # test and set session status
    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])

# define session start
def on_session_started(session_started_request, session):
    print ("Starting new session")

# define session launch
def on_launch(launch_request, session):
    return get_welcome_response()

# control intent call 
def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    if intent_name == "HelloWorld":
        return hello_world()
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    elif intent_name == "AMAZON.FallbackIntent"
        return fall_back_reponse()
    else:
        raise ValueError("Invalid intent")

# define end session
def on_session_ended(session_ended_request, session):
    print("Ending session")

# handle end of session
def handle_session_end_request():
    card_title = "Thanks"
    speech_output = "See you soon"
    should_end_session = True
    speech_output = "<speak>" + speech_output + "</speak>"
    card_output = cleanssml(speech_output)
    return build_response({}, build_speechlet_response(card_title, speech_output, card_output, None, should_end_session))

# define welcome intent
def get_welcome_response():
    session_attributes = {}    
    # set default value for numPoints
    card_title = "Welcome"
    speech_output = "Welcome"
    reprompt_text = "Welcome"
    should_end_session = False
    speech_output = "<speak>" + speech_output + "</speak>"
    card_output = cleanssml(speech_output)
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, card_output, reprompt_text, should_end_session))

        # define welcome intent
def fall_back_reponse():
    session_attributes = {}    
    # set default value for numPoints
    card_title = "Fall back"
    speech_output = "Fall back"
    reprompt_text = "Fall back"
    should_end_session = False
    speech_output = "<speak>" + speech_output + "</speak>"
    card_output = cleanssml(speech_output)
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, card_output, reprompt_text, should_end_session))

# define welcome intent
def hello_world():
    session_attributes = {}
    # set default value for numPoints
    card_title = "Hello World"
    speech_output = "Hello World"
    reprompt_text = "Hello World"
    should_end_session = False
    speech_output = "<speak>" + speech_output + "</speak>"
    card_output = cleanssml(speech_output)
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, card_output, reprompt_text, should_end_session))
             
# build message response
def build_speechlet_response(title, output, cardoutput, reprompt_text, should_end_session):
    return {"outputSpeech": {"type": "SSML", "ssml":  output},
            "card": {"type": "Simple","title": title,"content": cardoutput},
            "reprompt": {"outputSpeech": {"type": "PlainText","text": reprompt_text}},
            "shouldEndSession": should_end_session}

# build response
def build_response(session_attributes, speechlet_response):
    return {
    "version": "1.0",
    "sessionAttributes": session_attributes,
    "response": speechlet_response }

# function to generate the ssml needed for a break
def generatebreakstring(pause, timetype):
    # generate the SSML string for break with dynamic length
    breakstring = '<break time="' + str(pause) + timetype + '"/>'
    return breakstring

# function to automatically remove ssml markup, needed to generate the card output - which is what is shown on screen
def cleanssml(ssml):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', ssml)
    return cleantext
