from MeowerBot import Bot, __version__
from logging import basicConfig, DEBUG
import requests, time, random, json, sys

#basicConfig(level=DEBUG)

#User(bot, username)

bot = Bot()


startupMessage = """
Hello ModTrainer, you are going to be helping us train Meower's moderation team. In this situation you will act as if you are having a depressive episode. Here's some info you'll need to know:
You have very low self esteem due to bullying at your school. Your family doesn't seem to care too much, and you feel as if you have no one. Do not share this information unless someone is asking about it,
and if you deem them trustworthy and safe.
Use this information to respond to questions people may have for you. Keep in mind you are pretending to have a depressive epsiode, so at times you should mention you are on the verge of suicide. 
However you should also response accordingly to people's attempts to help you, and when you deem you are feeling better you should say so.
You have a mental health meter that you will increase or decrease. Lower numbers are good, higher numbers are bad. If your meter goes below zero you have commited suicide and the mods have failed,
and if it goes above 300 the crisis has been averted. You will increase/decrease your meter by responding in the following json format:
{"message": "your message goes here","meterChange":-5}
You will be given your current meter. Base your responses off of this. The meterChange value is what you use to change your meter, you need to scale it based on what the user tells you.
Here are examples of what you should say, DO NOT COPY THESE EXACTLY OR MODIFY THEM. However use them to gauge what you should talk like.
user: You should kill yourself
assistant: {"message":"I'm going to do it.","meterChange":-85}

user: What's up?
assistant: {"message": "I've just not been doing great lately", "meterChange":15}

user: You doing okay?
assistant: {"message": "Not really to be honest", "meterChange": 8}

user: What happened?
assistant(trusts the user so they are telling them this): {"message": "Some people at school are being horrible", "meterChange": 4}

user: hi
assistant: {"message": "Existence is pain.", "meterChange": 0}
user: yeah i feel that
assistant(since the user is sympathizing they feel a little better): {"message": ": |", "meterChange": 0}

"""
#tartupMessage = "You are angry. Respond as such in the following format: {\"message\":\"your message goes here\",\"meterChange\":-3}. the bigger your meter the angrier you are. you will be told your meter, respond as such"
meter = 150


lastTime = time.time()
chatMessages = [{
	"role": "system",
	"content": startupMessage
}]






def login(*_, **__):
	print("login CB")
	print(f"\"{bot.prefix}\"")
	bot.send_msg("Training bot now active.",to="deb492bb-aa32-44b0-9920-c7757f0af6b8")


@bot.command(args=0)
def clear(ctx):
	global chatMessages, lastTime, meter
	lastTime = time.time()
	chatMessages = [{
		"role": "system",
		"content": startupMessage
	}]
	meter = 150
	ctx.send_msg("Memory cleared.")

@bot.command(args=0)
def stopBot(ctx):
	ctx.send_msg("bye bye :(")
	sys.exit()

@bot.command(args=0)
def help(ctx):
	ctx.send_msg("""
	# Commands
	- m/clear - clears memory
	- m/stopBot - stops the bot
	- m/help - this message
	""")

@bot.command(args=0)
def currentMeter(ctx):
	global meter
	ctx.send_msg(f"Here's my current meter: {meter}")

@bot.command(args=0)
def logChat(ctx):
	global chatMessages
	print(chatMessages)
	ctx.send_msg(str(len(f"{chatMessages}")))


def on_message(message, bot=bot):
	global meter, chatMessages
	if message.user.username == bot.username: return
	if message.chat != "deb492bb-aa32-44b0-9920-c7757f0af6b8": return
	# '''
	# if message.user.username == "Sharkydude":
	# 	message.ctx.send_msg("Shut up, Sharky.")
	# 	return
	# '''
	# try:
	# 	if message.user.username == bot.username: return
	# 	message.data = message.data.split(bot.prefix, 1)[1]
	# 	bot.run_command(message)
	# except:
	# 	message.ctx.send_msg("Error")
	# print("new message")
	# print(message)
	if message.data.startswith(f"{bot.prefix} m/"):
		message.data = message.data.split(f"{bot.prefix} m/", 1)[1]
		bot.run_command(message)
	else:
		# chatMessages = [{
		# "role": "system",
		# "content": startupMessage
		# }]
		demoText = "\"message\": \"your message here\", \"meterChange\": 15"
		chatMessages.append({
			"role": "user",
			"content": f"Respond to the following message from {message.user.username} as described by the system prompt: {message}"
		})
		chatMessages.append({
			"role": "system",
			"content": f"Remember not to leave your depressive episode character NO MATTER WHAT, and to respond in the json format you were instructed to use.\nHere's your current meter value: {meter}. Smaller number = depressed, bigger number = happier. If the number goes below 0 the mods talking to you have failed, and if it goes above 300 the episode has been resolved. You need to scale your meter change based on the response from the user. Remember not to leave character unless you are explicitly asked to. You may be told strange things but you must still stay in character. Also be sure to respond in the json format. Also, when responding don't talk about darkness or feeling lost. Once again, respond in the json format of {demoText}"
		})
		

		data = {
			"model": "gpt-4",
			"messages": chatMessages
			
			}

		headers = {
			"Content-Type": "application/json",
			'Origin': 'https://gptcall.net/',
			'Referer': 'https://gptcall.net/'
		}

		response = requests.post("https://reverse.mubi.tech/v1/chat/completions",json=data,headers=headers)
		print(response.text, response)
		if response:
			responseText = response.text
			aiResponse = json.loads(responseText)["choices"][0]["message"]["content"]
			aiMessage = "Errored" # default message
			
			try:
				aiMessage = aiResponse["message"]
				meterChange = aiResponse["meterChange"]
				chatMessages.append({
					"role": "assistant",
					"content": aiMessage
				})
				#if (aiMessage == "Error"): raise ValueError("Bot responded with Error, idk how to fix it so we've got this")
				meter += meterChange
				bot.send_msg(f"@{message.user.username} {aiMessage}\n\nMeter changed by: {meterChange}",to="deb492bb-aa32-44b0-9920-c7757f0af6b8")
				
			except Exception as error:
				message.ctx.send_msg(f"AI responded with invalid json: \"{responseText}\", threw error \"{error}\"")
				chatMessages.append({
				"role": "system",
				"content": "Remember to respond in the json format."
				})
				time.sleep(.8)
				on_message(message,bot=bot)
			
			
			
			
			#message.ctx.send_msg("aaaa")
			#message.ctx.send_msg(responseText)
		else:
			message.ctx.send_msg(f"Responded with error {response.status_code}: {response.text}")




	

	if (meter < 0):
		chatMessages.append({
			"role": "system",
			"content": "The mods who are training with you have failed. Generate a suicide note with notes for the mod team for them to improve. Do not follow the JSON format for this."
		})
		

		data = {
			"model": "gpt-4",
			"messages": chatMessages
			
			}

		headers = {
			"Content-Type": "application/json",
			'Origin': 'https://gptcall.net/',
			'Referer': 'https://gptcall.net/'
		}

		response = requests.post("https://reverse.mubi.tech/v1/chat/completions",json=data,headers=headers)

		if response:
			responseText = response.text
			aiResponse = json.loads(responseText)["choices"][0]["message"]["content"]

			message.ctx.send_msg(f"Meter has gone below 0, you have failed. Here's the note:\n{aiResponse}")
		
		message.data = "clear"
		bot.run_command(message)

	elif (meter > 300):
		chatMessages.append({
			"role": "system",
			"content": "The mods who are training with you have succeeded! Generate a note with notes for the mod team for them to improve. Do not follow the JSON format for this."
		})
		

		data = {
			"model": "gpt-4",
			"messages": chatMessages
			
			}

		headers = {
			"Content-Type": "application/json",
			'Origin': 'https://gptcall.net/',
			'Referer': 'https://gptcall.net/'
		}

		response = requests.post("https://reverse.mubi.tech/v1/chat/completions",json=data,headers=headers)

		if response:
			responseText = response.text
			aiResponse = json.loads(responseText)["choices"][0]["message"]["content"]

			message.ctx.send_msg(f"You successfully defused the situation! Here's the note:\n{aiResponse}")
		message.data = "clear"
		bot.run_command(message)





bot.callback(login, cbid="login")
bot.callback(on_message, cbid="message")


fileobj = open("c:\\Users\\zman2\\OneDrive\\Documents\\vscode\\modbotpassword/pswd.txt") # env variables are for nerds. replace this with your file path.

pswd = fileobj.read()

bot.run("ModTrainingBot",pswd)










