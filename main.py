from MeowerBot import Bot, __version__
from logging import basicConfig, DEBUG
import requests, time, random

#basicConfig(level=DEBUG)

#User(bot, username)

bot = Bot()

lastTime = time.time()






actions = ["rock","paper","scissors"]
compliments = ["I like your shoes, ","Have a great day, ","You're a nice person, ","Nice shirt, ","You're funny, ","You deserve a cookie, ","You're cool, ","Insert compliment here, ","I like your profile picture, ","I hope you have a day as nice as you, ","I like your hair, "]
prompts = []
responses = []
settingmode = False
savedusername = ""

def login(*_, **__):
	print("login CB")
	bot.send_msg("This is a test", to='9bf5bddd-cd1a-4c0d-a34c-31ae554ed4a7')





def on_message(message, bot=bot):       
	if message.user.username == bot.username: return
	if message.chat != "9bf5bddd-cd1a-4c0d-a34c-31ae554ed4a7": return
	# '''
	# if message.user.username == "Sharkydude":
	# 	message.ctx.send_msg("Shut up, Sharky.")
	# 	return
	# '''
	# try:
	# 	if message.user.username == bot.username: return
	# 	if not message.data.startswith(bot.prefix): return
	# 	message.data = message.data.split(bot.prefix, 1)[1]
	# 	bot.run_command(message)
	# except:
	# 	message.ctx.send_msg("Error")
	# print("new message")
	# print(message)
	data = {
		"model": "gpt-3.5-turbo",
		"messages": [{
                            "role": "user",
                            "content": f"This is a test. Respond to the following message: {message}"
                    }]
		
		}
	headers = {
		"Content-Type": "application/json",
		'Origin': 'https://gptcall.net/',
        'Referer': 'https://gptcall.net/'
		}

	response = requests.post("https://reverse.mubi.tech/v1/chat/completions",json=data,headers=headers)
	print(response)
	if response:
		responseText = response.text
		print(type(responseText))
		bot.send_msg(f"@{message.user.username} {responseText}",to="9bf5bddd-cd1a-4c0d-a34c-31ae554ed4a7")
		#message.ctx.send_msg("aaaa")
		#message.ctx.send_msg(responseText)



bot.callback(login, cbid="login")
bot.callback(on_message, cbid="message")

bot.run("ModTrainingBot","derpyownsthisaccount123")









