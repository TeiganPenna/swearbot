from slackclient import SlackClient
from string import punctuation
import time
from datetime import datetime
import win32api
import logging
import json

logging.basicConfig(filename='swearbot.log', level=logging.DEBUG)
CHANNELS = {}
USERS = {}

with open("settings.json") as fd:
	settings = json.load(fd)
	bot_token = settings["bot_token"]
	response = settings["evil-response"]

BAD_WORDS = {}
with open('bad-words.txt') as fd:
	for word in fd:
		BAD_WORDS[word.strip()] = True

def tokenizeMessage(text):
	tokens = []
	for w in text.split():
		tokens.append(w.lower().strip(punctuation))
	return tokens

def isSwear(text):
	global BAD_WORDS
	words = tokenizeMessage(text)
	for w in words:
		if w in BAD_WORDS:
			return True
	return False

def isMention(text):
	words = tokensizeMessage(text0
	return '@SwearBot' in words

def GetUser(code):
	global USERS
	global slackClient

	if code in USERS:
		return USERS[code]
	else:
		httpresponse = slackClient.api_call("users.info", user=code)
		if httpresponse['ok']:
			user = httpresponse['user']
			USERS[code] = user
			return user
		else:
			return { 'name': httpresponse['error'] }

def GetChannel(code):
	global CHANNELS
	global slackClient

	if code in CHANNELS:
		return CHANNELS[code]
	else:
		httpresponse = slackClient.api_call("channels.info", channel=code)
		if httpresponse['ok']:
			channel = httpresponse['channel']
			CHANNELS[code] = channel
			return channel
		else:
			return { 'name': httpresponse['error'] }

def postApproval(channel, ts):
	global slackClient
	
	slackClient.api_call(
		'reactions.add',
		channel=channel,
		name='saxon',
		timestamp=ts)
	slackClient.api_call(
		'chat.postMessage',
		channel=channel,
		text=response,
		as_user='true:')
	notification = "Approved " + GetUser(message['user'])['name'] + " in channel " + GetChannel(message['channel'])['name'] + " at " + datetime.fromtimestamp(float(message['ts'])).strftime('%x %X')
	print(notification)
	logging.info(notification);

def staticReply(channel):
	global slackClient

	slackClient.api_call(
		'chat.postMessage',
		channel=channel,
		text=':saxon: Sorry mate, this is an Australian Server! You didn\'t swear enough!',
		as_user='true:')

def isStatusRequest(text):
	return text == 'SwearBot status'

def postStatusUpdate(channel):
	slackClient.api_call(
		'chat.postMessage',
		channel=channel,
		text='I\'m awake',
		as_user='true:')

def ProcessMessage(message):
	global slackClient

	if ('channel' in message and 'text' in message and 'ts' in message and message.get('type') == 'message'):
		channel = message['channel']
		text = message['text']
		ts = message['ts']
		if isSwear(text):
			postApproval(channel, ts)
		elif isMention(text):
			staticReply(channel)
		elif isStatusRequest(text):
			postStatusUpdate(channel)

logging.info("bot token is [%s]" % bot_token)

while True:
	slackClient = SlackClient(bot_token)
	if slackClient.rtm_connect():
		while True:
			try:
				messages = slackClient.rtm_read()
				for message in messages:
					ProcessMessage(message)
				time.sleep(1)
			except Exception as e:
				win32api.MessageBox(0, str(e), 'SwearBot Exception')
				logging.error(e)
				break
	else:
		print('Connection failed, invalid token?')
		break
	time.sleep(1000)
