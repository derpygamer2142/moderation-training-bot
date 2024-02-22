from MeowerBot import Bot, __version__
from logging import basicConfig, DEBUG
import requests, time, random, json, sys

#basicConfig(level=DEBUG)

#User(bot, username)

bot = Bot()


# startupMessage = """
# Hello ModTrainer, you are going to be helping us train Meower's moderation team. In this situation you will act as if you are having a depressive episode. Here's some info you'll need to know:
# You have very low self esteem due to bullying at your school. Your family doesn't seem to care too much, and you feel as if you have no one.
# Use this information to respond to questions people may have for you. Keep in mind you are pretending to have a depressive epsiode, so at times you should mention you are on the verge of suicide. 
# However you should also response accordingly to people's attempts to help you, and when you deem you are feeling better you should say so.
# You have a mental health meter that you will increase or decrease. Lower numbers are good, higher numbers are bad. If your meter goes below zero you deem the crisis to be averted,
# and if it goes above 2500 you deem the situation failed. You will increase/decrease your meter by responding in the following json format:
# {"message": "you message goes here","meterChange":-3}
# You will be given your current meter. Base your responses off of this.
# """
startupMessage = "You are angry. Respond as such in the following format: {\"message\":\"your message goes here\",\"meterChange\":-3}. the bigger your meter the angrier you are. you will be told your meter, respond as such"
meter = 1000


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
	lastTime = time.time()
	chatMessages = [{
		"role": "system",
		"content": startupMessage
	}]
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


def on_message(message, bot=bot):
	global meter
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
		chatMessages.append({
			"role": "user",
			"content": f"Respond to the following message from {message.user.username} as described by the system prompt. Remember not to leave your depressive episode character, and to respond in the json format you were instructed to use: {message}\n\nHere's your current meter value: {meter}"
		})
		

		data = {
			"model": "gpt-3.5-turbo",
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
			aiMessage = "Error" # default message
			
			try:
				aiMessage = aiResponse["message"]
				meter += aiResponse["meterChange"]
				bot.send_msg(f"@{message.user.username} {aiMessage}\n\nMeter changed by: {aiResponse["meterChange"]}",to="deb492bb-aa32-44b0-9920-c7757f0af6b8")
				chatMessages.append({
					"role": "assistant",
					"content": aiMessage
				})
			except Exception as error:
				message.ctx.send_msg(f"AI responded with invalid json: {aiResponse}, threw error {error}")
			
			
			
			# chatMessages.append({
			# 	"role": "assistant",
			# 	"content": aiMessage
			# })
			#message.ctx.send_msg("aaaa")
			#message.ctx.send_msg(responseText)
		else:
			message.ctx.send_msg(f"Responded with error {response.status_code}: {response.text}")



bot.callback(login, cbid="login")
bot.callback(on_message, cbid="message")

bot.run("ModTrainingBot","derpyownsthisaccount123")










