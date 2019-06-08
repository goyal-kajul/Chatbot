import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client-secret.json"

import dialogflow_v2 as dialogflow
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "newsbot-tjvipb"

import wikipedia
from apiclient.discovery import build
api_key="AIzaSyCrAKi21-BSN5czEU-pjOMV7LcSMEPAYyg"

from pymongo import MongoClient

def add_db(parameters):
	client = MongoClient('mongodb+srv://test:test@cluster0-jifwq.mongodb.net/test?retryWrites=true&w=majority')
	db = client.get_database('record_db')
	records = db.first
	key=list(parameters.keys())
	i=0
	value=[]
	for item in key:
		value.append(parameters.get(item))
		rec={item:value[i]}
		i+=1
		records.insert_one(rec)

def get_info(parameters):
	try:
		query=parameters.get("query")
		return query.capitalize() +"\n\n"+wikipedia.summary(query,sentences=5)
	except:
		return "Try to be more specific"

def get_youtube(parameters):
	youtube = build('youtube','v3',developerKey="AIzaSyCrAKi21-BSN5czEU-pjOMV7LcSMEPAYyg")
	req=youtube.search().list(q=parameters.get("req_video"),part='snippet')
	res=req.execute()
	title_li=[]
	id_li=[]
	for i in range(4):
		title_li.append(res['items'][i]['snippet']['title'])
		id_li.append(res['items'][i]['snippet']['channelId'])
	url=res['items'][0]['snippet']['thumbnails']['default']['url']
	data="Your requested videos :\n\n"
	for i in range(4):
		data+="Title : "+title_li[i]+"\nChannel id : "+id_li[i]+"\n"
	return data,url


def detect_intent_from_text(text, session_id, language_code='en'):
	session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
	text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
	query_input = dialogflow.types.QueryInput(text=text_input)
	response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
	return response.query_result


def fetch_reply(msg, session_id):
	response = detect_intent_from_text(msg, session_id)
	if response.intent.display_name == 'get_info':
		add_db(dict(response.parameters))
		query_str = get_info(dict(response.parameters))
		return query_str
	elif response.intent.display_name == 'get_youtube':
		add_db(dict(response.parameters))
		data,url=get_youtube(dict(response.parameters))
		file={1:data,2:url}
		return file
	else:
		return response.fulfillment_text
