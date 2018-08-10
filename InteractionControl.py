# main python program
import json, re, random, urllib3, requests, bs4, re

# lambda function handler - including specific reference to our skill
def lambda_handler(event, context):
    # if skill ID does not match my ID then raise error
    if (event["session"]["application"]["applicationId"] !=
            "amzn1.ask.skill.c4f72dcb-b8ae-451d-b3a7-cbc8c2f507b4"):
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

    if intent_name == "LatestNews":
        return latest_news()
    elif intent_name == "NextNews":
        return next_news()
    elif intent_name == "LastNews":
        return last_news()
    elif intent_name == "MultipleNews":
        return multiple_news(intent)
    elif intent_name == "LatestResult":
            return latest_result()
    elif intent_name == "NextGame":
            return next_fixture()
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    elif intent_name == "AMAZON.FallbackIntent":
        return fall_back_reponse()
    else:
        raise ValueError("Invalid intent")

# define end session
def on_session_ended(session_ended_request, session):
    print("Ending session")

# handle end of session
def handle_session_end_request():
    card_title = "Thanks"
    speech_output = "Everything you heard is the great work of the T W T D team, come on you blues!"
    should_end_session = True
    speech_output = "<speak>" + speech_output + "</speak>"
    card_output = cleanssml(speech_output)
    return build_response({}, build_speechlet_response(card_title, speech_output, card_output, None, should_end_session))

# define welcome intent
def get_welcome_response():
    session_attributes = {}    
    
    # prepare Json - extract site HTML and structure articles ready for the skills
    loadJson = prepareJson()
    # if Json loaded ok then, respond to user
    if loadJson == True:
        speech_output = "Welcome to the unofficial Alexa Skill of the unofficial Ipswich Town news site T W T D, all credit to the content of this skill goes to the T W T D team, you can ask me for the latest news, the most recent result or the next game?"
        reprompt_text = speech_output
        card_title = "Welcome to the unofficial Alexa Skill"
        should_end_session = False
    else:
        speech_output = "I'm sorry I am currently unable to retrieve the news from the T W T D site, there must be something exciting happening, please try again later"
        reprompt_text = speech_output
        card_title = "Sorry TWTD is unavailiable"
        should_end_session = True

    speech_output = "<speak>" + speech_output + "</speak>"
    card_output = cleanssml(speech_output)
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, card_output, reprompt_text, should_end_session))

# what can you do
def what_can_you_do():
    session_attributes = {}    
    # set default value for numPoints
    card_title = "Help"
    speech_output = "There is so much I can do, here are some of the things you can ask me me for, " + generatebreakstring(500,"ms") + "our latest result, " + generatebreakstring(500,"ms") + "our next fixture, " + generatebreakstring(500,"ms") + "and the latest news, what would you like to know about?"
    reprompt_text = speech_output
    should_end_session = False
    speech_output = "<speak>" + speech_output + "</speak>"
    card_output = cleanssml(speech_output)
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, card_output, reprompt_text, should_end_session))

# define fallback intent
def fall_back_reponse():
    session_attributes = {}    
    # set default value for numPoints
    card_title = "Sorry"
    speech_output = "I'm sorry I didn't recognise your request, if you need help with what you can ask me, then ask me what I can do?"
    reprompt_text = speech_output
    should_end_session = False
    speech_output = "<speak>" + speech_output + "</speak>"
    card_output = cleanssml(speech_output)
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, card_output, reprompt_text, should_end_session))

# define welcome intent
def latest_news():
    session_attributes = {}
    
    # latest news is always the first record in the Json
    speech_output = HTMLdata['articles'][0]['summary'] + generatebreakstring(500,"ms") + ", " + HTMLdata['articles'][0]['detail'] + generatebreakstring(500,"ms") + ", you can ask me for the next article or the full story?"

    card_title = "Headline"
    reprompt_text = "You can ask me for the next article or the full story?"
    should_end_session = False
    speech_output = "<speak>" + speech_output + "</speak>"
    card_output = cleanssml(speech_output)
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, card_output, reprompt_text, should_end_session))

# define welcome intent
def next_news():
    session_attributes = {}

    # find the current news article that was read by looping through the Json
    for news in HTMLdata['articles']:
        if news['current'] == True :
            # store the ID of the article
            currentArcticleID = news['ID']
            # turn off the flag
            news['current'] = False
    
    # increment one to ID for next article, set current flag to true
    nextArticleID = int(currentArcticleID) + 1
    HTMLdata['articles'][nextArticleID]['current'] = True

    # next news article picked up from the Json file using new ID
    speech_output = HTMLdata['articles'][nextArticleID]['summary'] + generatebreakstring(500,"ms") + ", " + HTMLdata['articles'][nextArticleID]['detail'] + generatebreakstring(500,"ms") + ", you can ask me to replay the article, the full story, the next article or for the last article again?"

    card_title = "Headline"
    reprompt_text = "You can ask me to replay the article, the full story, the next article or for the last article again?"
    should_end_session = False
    speech_output = "<speak>" + speech_output + "</speak>"
    card_output = cleanssml(speech_output)
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, card_output, reprompt_text, should_end_session))

# last news intent
def last_news():
    session_attributes = {}

    # find the current news article that was read by looping through the Json
    for news in HTMLdata['articles']:
        if news['current'] == True :
            # store the ID of the article
            currentArcticleID = news['ID']
            # turn off the flag
            news['current'] = False
    
    # if we are on the first article, we can't go back any further
    if currentArcticleID == 0:
        speech_output = "I'm sorry, you just heard the most recent article, please ask me to replay the article, the full story or for the next news article"
    # increment one to ID for next article, set current flag to true 
    else:
        nextArticleID = int(currentArcticleID) - 1
        HTMLdata['articles'][nextArticleID]['current'] = True

        # next news article picked up from the Json file using new ID
        speech_output = HTMLdata['articles'][nextArticleID]['summary'] + generatebreakstring(500,"ms") + ", " + HTMLdata['articles'][nextArticleID]['detail'] + generatebreakstring(500,"ms") + ", you can ask me to replay the article, the full story, the next article or for the last article again?"

    card_title = "Headline"
    reprompt_text = "You can ask me to replay the article, the full story, the next article or for the last article again?"
    should_end_session = False
    speech_output = "<speak>" + speech_output + "</speak>"
    card_output = cleanssml(speech_output)
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, card_output, reprompt_text, should_end_session))

# define mutiple news intent
def multiple_news(intent):
    session_attributes = {}
    speech_output = ""

    # get slot value
    numberofarticles = int(intent['slots']['number']['value'])

    # find the current news article that was read by looping through the Json
    for news in HTMLdata['articles']:
        if news['current'] == True :
            # store the ID of the article
            currentArcticleID = news['ID']
            # turn off the flag
            news['current'] = False
    
    # loop from current article + one to the set number of articles
    for news in range(currentArcticleID+1,currentArcticleID + numberofarticles + 1):
        # increment one to ID for next article, set current flag to true 
        nextArticleID = int(currentArcticleID) + 1
        HTMLdata['articles'][nextArticleID]['current'] = True

        # next news article picked up from the Json file using new ID
        speech_output = speech_output + HTMLdata['articles'][nextArticleID]['summary'] + generatebreakstring(500,"ms") + ", " + HTMLdata['articles'][nextArticleID]['detail'] + generatebreakstring(500,"ms") 

    speech_output = speech_output + ", you can ask me to replay the article, the full story, the next article or for the last article again?"

    card_title = "Headline"
    reprompt_text = "You can ask me to replay the article, the full story, the next article or for the last article again?"
    should_end_session = False
    speech_output = "<speak>" + speech_output + "</speak>"
    card_output = cleanssml(speech_output)
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, card_output, reprompt_text, should_end_session))

# latest result
def latest_result():
    session_attributes = {}    

    # last match, isolate the appropriate tags and extract sought text
    lastMatch = bsObj.find("td",{"style":"background-image: url('/images/customisations/blue-blockback.jpg'); background-repeat:no-repeat; height:600px;"}).findAll({"div"})[7].findAll({"div"})
    speech_output = lastMatch[3].get_text() + lastMatch[1].get_text() + ", you could ask me for the last report?"

    card_title = "Last Match"
    reprompt_text = speech_output
    should_end_session = False
    speech_output = "<speak>" + speech_output + "</speak>"
    card_output = cleanssml(speech_output)
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, card_output, reprompt_text, should_end_session))

# next fixture
def next_fixture():
    session_attributes = {}    

    # last match, isolate the appropriate tags and extract sought text
            # fixtures
        # next match, isolate the appropriate tags and extract sought text
    nextMatch = bsObj.find("td",{"style":"background-image: url('/images/customisations/blue-blockback.jpg'); background-repeat:no-repeat; height:600px;"}).find({"div"}).findAll({"div"}) 
    speech_output = nextMatch[3].get_text() + nextMatch[1].get_text()+ ", what would you like next?"

    card_title = "Last Match"
    reprompt_text = speech_output
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

# HTML
def prepareJson():
    global bsObj
    # setup Json
    setupJson()
    # setup urllib3 and http
    urllib3.disable_warnings()  
    http = urllib3.PoolManager()
    # make call and load url details into a python object
    webUrl = http.request('GET', 'https://www.twtd.co.uk')
    # test status code / 200 == successful call i.e. if the website is down, don't knock over the code
    if webUrl.status == 200:
        # read date into python object
        webHTML = webUrl.data
        # write html into a beautful soup object
        bsObj = bs4.BeautifulSoup(webHTML, "html.parser")
        #print(bsObj.prettify())
        #writeHTML(bsObj.prettify())
        
        # main article
        summary = bsObj.find(id="maincontent").find({"a"}).get_text()
        webURL = bsObj.find(id="maincontent").find({"a"})["href"]
        date = bsObj.find(id="maincontent").find({"a"}).find("span").get_text()      
        detail = bsObj.findAll("a",{"href":webURL})[1].get_text()
        #remove date from article
        summary = summary.replace(date,"")
        #print(article, detail, date, webURL)
        # add main article to Json
        addarticletoJson(len(HTMLdata['articles']),removeunicode(summary),removeunicode(detail),removeunicode(date),webURL,True)

        # current news
        for article in bsObj.findAll("table")[3].findAll({"a"}):
            summary = article.findAll("span")[0].get_text()
            detail = article.findAll("span")[1].get_text()
            date = article.findAll("span")[2].get_text()
            webURL = article["href"]
            
            # add to json file
            addarticletoJson(len(HTMLdata['articles']),removeunicode(summary),removeunicode(detail),removeunicode(date),webURL,False)
        
        # earlier news block
        for article in bsObj.findAll("table")[9].findAll({"a"}):
            if article.get_text() != "News archive":
                summary = article.get_text()
                webURL = article["href"]
                addarticletoJson(len(HTMLdata['articles']),removeunicode(summary),"","",webURL,False)
    
        # links to match articles
        lastMatchReport = bsObj.find("td",{"style":"background-image: url('/images/customisations/blue-blockback.jpg'); background-repeat:no-repeat; height:600px;"}).findAll({"div"})[7].findAll({"div"})[4].findAll({"a"})
        matchreportlink = lastMatchReport[0]["href"]
        managerreactionlink = lastMatchReport[1]["href"]
        fanreactionlink = lastMatchReport[2]["href"]
        paperreview = lastMatchReport[3]["href"]
        playerratings = lastMatchReport[4]["href"]

        return True
    # if we can't hit the webpage then throw error back    
    else:
        return False

# remove unicode characters
def removeunicode(text):
    text = re.sub(r'\\[u]\S\S\S\S[s]', "", text)
    text = re.sub(r'\\[u]\S\S\S\S', "", text)
    return text

# setup Json for players
def setupJson() :
    global HTMLdata
    HTMLdata = {}
    HTMLdata['articles'] = []
    #HTMLdata['fixtures'] = []

# add article to json
def addarticletoJson(ID,Summary,Detail,Date,URL,Current) :
    HTMLdata['articles'].append({    
    'ID': ID,
    'summary': removeunicode(Summary),
    'detail': removeunicode(Detail),
    'date': removeunicode(Date),
    'url': URL,
    'current':Current
    })