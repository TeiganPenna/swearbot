from slackclient import SlackClient
from string import punctuation
import time
import win32api
import logging
import json

logging.basicConfig(filename='swearbot.log', level=logging.DEBUG)

with open("settings.json") as fd:
	settings = json.load(fd)
	bot_token = settings["bot_token"]
	response = settings["response"]

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

def ProcessMessage(message):
	global slackClient

	if ('channel' in message and 'text' in message and 'ts' in message and message.get('type') == 'message'):
		channel = message['channel']
		text = message['text']
		ts = message['ts']
		if isSwear(text):
			slackClient.api_call(
				'reactions.add',
				channel=channel,
				name='pooh',
				timestamp=ts)
			slackClient.api_call(
				'chat.postMessage',
				channel=channel,
				text=response,
				as_user='true:')

logging.info("bot token is [%s]" % bot_token)

slackClient = SlackClient(bot_token)
while True:
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