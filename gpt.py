import toml
from revChatGPT.V1 import Chatbot

with open('config.toml', 'r') as f:
    data = toml.load(f)
key = data['gptkey']

chatbot = Chatbot(config=
{
  "access_token": key
})
def gptbot(userInput):
    print("Chatbot: ")
    output = ""
    prev_text = ""
    print(f"Userinput: {userInput}")
    for data in chatbot.ask(
        userInput,
    ):
        message = data["message"][len(prev_text) :]
        output += message
        print(message, end="", flush=True)
        prev_text = data["message"]
    print()
    return output


if __name__ == "__main__":
    bot_message = gptbot("Hello can you hear me?")
    print(f"bot_message: {bot_message}")
