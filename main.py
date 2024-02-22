from MeowerBot import Bot, __version__
from logging import basicConfig, DEBUG
import requests, time, random, json

#basicConfig(level=DEBUG)

#User(bot, username)

bot = Bot()

lastTime = time.time()
chatMessages = [{
	"role": "system",
	"content": "Hello ModTrainer, you are going to be helping us train Meower's moderation team. In this situation you will act as if you are having a depressive episode. Here's some info you'll need to know: You have very low self esteem due to bullying at your school. Your family doesn't seem to care too much, and you feel as if you have no one. Use this information to respond to questions people may have for you. Keep in mind you are pretending to have a depressive epsiode, so at times you should mention you are on the verge of suicide. However you should also response accordingly to people's attempts to help you, and when you deem you are feeling better you should say so."
}]






def login(*_, **__):
	print("login CB")
	bot.send_msg("This is a test",to="deb492bb-aa32-44b0-9920-c7757f0af6b8")





def on_message(message, bot=bot):       
    if message.user.username == bot.username: return
    if message.chat != "deb492bb-aa32-44b0-9920-c7757f0af6b8": return
    if time.time() - lastTime < 5: return
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
    chatMessages.append({
        "role": "user",
		"content": f"Respond to the following message from {message.user.username} as described by the system prompt: {message}"
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
        aiMessage = json.loads(responseText)["choices"][0]["message"]["content"]
        bot.send_msg(f"@{message.user.username} {aiMessage}",to="deb492bb-aa32-44b0-9920-c7757f0af6b8")
		
        chatMessages.append({
			"role": "assistant",
            "content": aiMessage
        })
		#message.ctx.send_msg("aaaa")
		#message.ctx.send_msg(responseText)



bot.callback(login, cbid="login")
bot.callback(on_message, cbid="message")

bot.run("ModTrainingBot","derpyownsthisaccount123")










